#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from configuration.configuration import Configuration, ConfigurationException
from contextlib import contextmanager
from environment import environment
from lxml import etree
from nlp import NaturalLanguageProcessor, LanguageProcessorException
from registry.registry import store_registry
from registry.registry import get_registry_tagset, RegistryException
from setup import project_path
from subprocess import Popen, call
from utils.downloader import download_large_file, get_online_file
from utils.progressbar import ProgressBar
from utils.system_utils import makedirs
from utils.xml_utils import qualified_name
from verticaldocument import VerticalDocument
from wikiextractor import parse_wikimarkup
import errno
import bz2
import logging
import os


class WikiCorpus(object):

    """Class representing corpus from Wikipedia of one language """

    # configuration file
    CORPUS_CONFIG_PATH = project_path('wikicorpus/corpus-config.yaml')

    # original dump file name
    DUMP_ORIGINAL_NAME = 'pages-articles.xml.bz2'

    # dump url
    DUMP_URL_GENERAL = 'http://dumps.wikimedia.org/{lang}wiki/latest/'\
        + '{lang}wiki-latest-' + DUMP_ORIGINAL_NAME

    # md5 checksum file url
    MD5_URL_GENERAL = 'http://dumps.wikimedia.org/{lang}wiki/latest/'\
        + '{lang}wiki-latest-md5sums.txt'

    # Wikipedia namespace number label for articles
    ARTICLE_NS = '0'

    # basic set of structures in a vertical file
    #_BASIC_STRUCTURES = {'doc', 'p', 's', 'g', 'term'}

    def __init__(self, language):
        """Initalization of WikiCorpus instance

        :language: unicode
        """
        # TODO: check if language is in dictionary of iso codes
        self._language = language

        # load configuration
        self._configuration = Configuration(WikiCorpus.CORPUS_CONFIG_PATH)

        # vertical info
        self._tagset = None
        #self._structures = None  # always _BASIC_STRUCTURES

    # ------------------------------------------------------------------------
    # getters and setters
    # ------------------------------------------------------------------------

    def get_corpus_name(self):
        """ Returns corpus name
        """
        return self._configuration.get('corpus-name').format(
            lang=self.language())

    def get_dump_path(self):
        """ Returns path to dump
        """
        # full dumps are bzipped, while sample dumps are uncompressed
        if self.is_dump_compressed():
            ext = self._configuration.get('extensions', 'compressed-dump')
        else:
            ext = self._configuration.get('extensions', 'uncompressed-dump')

        # dump file name = corpus name + extension
        dump_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=ext)

        # path = path to verticals + dump file name
        path = os.path.join(
            self.get_uncompiled_corpus_path(),
            dump_file_name)
        return path

    def get_dump_length(self):
        """Returns length of the dump

        Note: For compressed dumps, this is larger number than file size.
        """
        if self.is_dump_compressed():
            print 'Calculating uncompressed dump length...'
            with self._open_dump() as dump_file:
                dump_file.seek(0, os.SEEK_END)
                length = dump_file.tell()
                return length
        else:
            return os.path.getsize(self.get_dump_path())

    def get_namespace(self):
        """Returns namespace of the wiki dump
        """
        with self._open_dump() as dump_file:
            # read first event, which is ('start', root element),
            context_for_ns = etree.iterparse(dump_file, events=('start',))
            _, root = context_for_ns.next()
            # get namespace information from the root element,
            # None means implicit namespace (without prefix)
            namespace = root.nsmap[None]
            del context_for_ns
        return namespace

    def get_prevertical_path(self):
        """ Returns path to prevertical
        """
        # prevertical file name = corpus name + extension
        prevertical_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=self._configuration.get('extensions', 'prevertical'))

        # path = path to verticals + prevertical file name
        path = os.path.join(
            self.get_uncompiled_corpus_path(),
            prevertical_file_name)
        return path

    def get_registry_path(self):
        """ Returns path to registry file.

        It will also creates non-existing directories on this path
        """
        registry_dir = environment.registry_path()
        makedirs(registry_dir)
        path = os.path.join(
            registry_dir,
            self.get_corpus_name())
        return path

    def get_tagset(self):
        """Returns tagset of the corpus.

        @return: [registry.tagsets.tagset] || None
        @throws: RegistryException
        """
        # first, if _tagset is None, update the tagset ifnormation
        if self._tagset is None:
            self._tagset = get_registry_tagset(self.get_registry_path())
        return self._tagset

    def get_url_prefix(self):
        """Returns url prefix for all articles in the corpus.
        """
        return 'http://{lang}.wikipedia.org/wiki'.format(lang=self.language())

    def get_vertical_path(self):
        """ Returns path to vertical
        """
        # vertical file name = corpus name + extension
        vertical_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=self._configuration.get('extensions', 'vertical'))

        # path = path to verticals + vertical file name
        path = os.path.join(
            self.get_uncompiled_corpus_path(),
            vertical_file_name)
        return path

    def get_uncompiled_corpus_path(self):
        """ Returns path to directory with verticals for this corpus

        It will also creates non-existing directories on this path
        """
        path = os.path.join(
            environment.verticals_path(),
            self.get_corpus_name())
        makedirs(path)
        return path

    def get_compiled_corpus_path(self):
        """ Returns path to directory with compiled corpus

        It will also creates non-existing directories on this path
        """
        path = os.path.join(
            environment.compiled_corpora_path(),
            self.get_corpus_name())
        makedirs(path)
        return path

    #def is_sample(self):
    #    """ Returns True if this is a sample corpus
    #    """
    #    return bool(self.sample_size())

    def is_dump_compressed(self):
        """Returns True if dumps is compress, False otherwise.
        """
        # dumps for full languages are always compressed
        return True

    def language(self):
        """ Returns corpus language
        """
        return self._language

    def prevertical_file_exists(self):
        return os.path.exists(self.get_prevertical_path())

    def vertical_file_exists(self):
        return os.path.exists(self.get_vertical_path())

    # ------------------------------------------------------------------------
    #  corpus building methods
    # ------------------------------------------------------------------------

    def download_dump(self, force=False):
        """ Downloads dump of Wikipedia

        :force: Boolean
            if True, it downloads dump even if some dump with
            target name is already downloaded
        """
        # select dump path
        dump_path = self.get_dump_path()
        if os.path.exists(dump_path) and not force:
            logging.info('Dump {name} already exists.'.format(name=dump_path))
            return

        # select dump url
        dump_url = WikiCorpus.DUMP_URL_GENERAL.format(lang=self.language())

        logging.info('Started downloading {l}-wiki dump from {url}'
            .format(l=self.language(), url=dump_url))

        # find MD5 checksum
        md5_url = WikiCorpus.MD5_URL_GENERAL.format(lang=self.language())
        md5sums = get_online_file(md5_url, lines=True)
        for file_md5, file_name in map(lambda x: x.split(), md5sums):
            if file_name.endswith(WikiCorpus.DUMP_ORIGINAL_NAME):
                md5sum = file_md5
                break
        else:
            logging.warning('no matching MD5 checksum for the dump found')
            md5sum = None

        # downloading
        download_large_file(dump_url, dump_path, md5sum=md5sum)

        logging.info('Downloading of {lang}-wiki dump finished'.format(
            lang=self.language(),
            path=dump_path))

    def create_prevertical(self):
        """ Parses dump (outer XML, inner Wiki Markup) and creates prevertical
        """
        prevertical_path = self.get_prevertical_path()
        namespace = self.get_namespace()

        # create qualified names (= names with namespaces) for tags we need
        TEXT_TAG = qualified_name('text', namespace)
        TITLE_TAG = qualified_name('title', namespace)
        REDIRECT_TAG = qualified_name('redirect', namespace)
        NS_TAG = qualified_name('ns', namespace)

        logging.info('Preverticalization of {name} started...'.format(
            name=self.get_corpus_name()))

        # iterate through xml and build a sample file
        with open(prevertical_path, 'w') as prevertical_file:
            with self._open_dump() as dump_file:
                context = etree.iterparse(dump_file, events=('end',))
                progressbar = ProgressBar(self.get_dump_length())
                last_title = None
                id_number = 0
                # skip first page in full (copressed) dump since it's Main Page
                skip = True if self.is_dump_compressed() else False

                # iterate through end-events
                for event, elem in context:
                    if elem.tag == REDIRECT_TAG:
                        # ignore redirect pages
                        skip = True
                    elif elem.tag == NS_TAG:
                        # ignore nonarticle pages (such as "Help:" etc.)
                        if elem.text != WikiCorpus.ARTICLE_NS:
                            skip = True
                    elif elem.tag == TITLE_TAG:
                        # remember the title
                        last_title = elem.text
                    elif elem.tag == TEXT_TAG:
                        if skip:
                            skip = False
                            continue
                        # new id
                        id_number += 1
                        parsed_doc = parse_wikimarkup(id_number, last_title,
                            self.get_url_prefix(), elem.text) + '\n'
                        prevertical_file.write(parsed_doc.encode('utf-8'))
                        # approximate work done by positin in dump file
                        progressbar.update(dump_file.tell())

                    # cleanup
                    elem.clear()
                    #while elem.getprevious() is not None:
                    #    del elem.getparent()[0]
                    for ancestor in elem.xpath('ancestor-or-self::*'):
                        while ancestor.getprevious() is not None:
                            del ancestor.getparent()[0]
                del context
        progressbar.finish()

        logging.info('Prevertical of {name} created at: {path}'.format(
            name=self.get_corpus_name(), path=prevertical_path))

    def create_vertical(self):
        """ Creates a vertical file.

        Performes tokenization of prevertical and for some languages
        also morfologization (adding morfological tag and lemma/lempos)
        """
        prevertical_path = self.get_prevertical_path()
        vertical_path = self.get_vertical_path()
        # check if prevertical file already exists
        if not self.prevertical_file_exists():
            raise CorpusException('Verticalization failed: '
                + 'Missing prevertical file.')
        logging.info('Verticalization of {name} started...'.format(
            name=self.get_corpus_name()))
        try:
            # create vertical file
            with NaturalLanguageProcessor(self.language()) as lp:
                tags = lp.create_vertical_file(prevertical_path, vertical_path)
                self._tagset = tags
                #self._structures = WikiCorpus._BASIC_STRUCTURES
            # create registry file
            self.create_registry()
            logging.info('Vertical of {name} created at: {path}'.format(
                name=self.get_corpus_name(),
                path=vertical_path))
        except ConfigurationException as exc:
            raise CorpusException('Verticalization failed: ' + exc.message)
        except LanguageProcessorException as exc:
            raise CorpusException('Verticalization failed: ' + exc.message)

    def infere_terms_occurences(self):
        """ Labels all occurences of terms in morfolgized vertical

        During terms-inference some postprocessing is done as well
        (removing desamb hacks, using actual numbers as lemmata).
        """
        vertical_path = self.get_vertical_path()
        try:
            logging.info('Terms occurences inference in {name} started'.format(
                name=self.get_corpus_name()))

            # TODO: jmeno vertikalu bez termu - vzit z konfiguarku
            original_vertical_path = vertical_path + '.before-inference'
            call(('cp', vertical_path, original_vertical_path))

            # find tagset (throws exception if registry file not found)
            tagset = self.get_tagset()

            with open(original_vertical_path) as input_file:
                with open(vertical_path, 'w') as output_file:
                    for line in input_file:
                        line = line.decode('utf-8').strip()
                        # TODO: ?osetrit prazdne radky a podobne veci??
                        if line.startswith('<doc'):
                            document = [line]
                        else:
                            document.append(line)
                        # check if the end of document is reached
                        if line == '</doc>':
                            vertical = VerticalDocument(document,
                                tagset=tagset,
                                terms_inference=True)
                            output_file.write(str(vertical))

            logging.info('Terms occurences inference in {name} finished.'
                .format(name=self.get_corpus_name()))

        except CorpusException as exc:
            raise CorpusException('Terms inference failed: ' + exc.message)

        except RegistryException as exc:
            raise CorpusException('Terms inference failed: ' + exc.message)

        except LanguageProcessorException as exc:
            raise CorpusException('Terms inference failed: ' + exc.message)

    def create_registry(self):
        """ Creates registry file
        """
        store_registry(
            path=self.get_registry_path(),
            lang=self.language(),
            vertical_path=self.get_vertical_path(),
            compiled_path=self.get_compiled_corpus_path(),
            tagset=self.get_tagset())

    def compile_corpus(self):
        """ Compiles given corpora
        """
        task = Popen(('compilecorp',
            '--recompile-corpus',
            self.get_registry_path(),
            self.get_vertical_path()))
        task.wait()
        if task.returncode != 0:
            raise CorpusException('Compilation failed.')
        logging.info('Corpus compiled:' + self.get_compiled_corpus_path())

    def check_corpus(self):
        """Prints compiled corpus status generated by corpcheck.
        """
        task = Popen(('corpcheck', self.get_registry_path()))
        task.wait()
        if task.returncode != 0:
            raise CorpusException('Compiled corpus checking failed.')

    def print_concordances(self, query):
        """Prints concordances of a given query

        @param query: query string in CQL
        """
        call(('corpquery', self.get_registry_path(), query,
            '-h', '10',     # limit of 10 results,
            '-c', '10',     # left and right context of 10 words
            '-a', 'word',   # only show words in the result
            '-s', 'p,doc'))  # only show p and doc structures

    def print_info(self):
        """ Returns corpus summary
        """
        # check if corpus exists
        verticals_path = self.get_uncompiled_corpus_path()
        if not os.listdir(verticals_path):
            print 'Corpus %s does not exist.' % self.get_corpus_name()
            return

        print 'Corpus name:', self.get_corpus_name()

        # verticals
        print 'Vertical files:', verticals_path
        call(('ls', '-lhtcr', verticals_path))

        # registry
        registry_path = self.get_registry_path()
        if os.path.isfile(registry_path):
            print 'Registry:', registry_path
        else:
            print 'Registry: no'
            # if there is no registry file, it can't be compiled
            return

        # compilation
        compiled_path = self.get_compiled_corpus_path()
        print 'Compiled:',
        if os.listdir(compiled_path):
            print compiled_path
        else:
            print 'no'

    # ------------------------------------------------------------------------
    #  private methods
    # ------------------------------------------------------------------------

    @contextmanager
    def _open_dump(self):
        """Opened dump (prepared for reading) with statement manager

        Allows to write:
            with self._open_dump() as dump_file:
                do something
        And dump will be closed automatically no matter what.
        """
        dump_path = self.get_dump_path()
        try:
            # open dump
            if self.is_dump_compressed():
                dump_file = bz2.BZ2File(dump_path, 'r')
            else:
                dump_file = open(dump_path)
            try:
                yield dump_file
                # [after yield, the body of with statement will be executed]
            finally:
                dump_file.close()
        except IOError as exc:
            # errno.ENOENT = "No such file or directory"
            if exc.errno == errno.ENOENT:
                raise CorpusException('Dump file {name} doesn\'t exist.'
                    .format(name=dump_path))

    # ------------------------------------------------------------------------
    #  magic methods
    # ------------------------------------------------------------------------

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return 'WikiCorpus({lang})'.format(lang=self.language())

    def __unicode__(self):
        return repr(self)


# ---------------------------------------------------------------------------
#  Exceptions
# ---------------------------------------------------------------------------

class CorpusException(Exception):
    """ Class for reprezentation of exception raised during building corpus
    """
    pass
