#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from configuration import Configuration  # , ConfigurationException
from downloader import download_large_file, get_online_file
from environment import environment
from system_utils import makedirs
#from lxml import etree
#import bz2
import os


class WikiCorpus(object):

    """Class representing corpus from Wikipedia of one language """

    # configuration file
    CORPUS_CONFIG_PATH = 'corpus-config.yaml'

    # original dump file name
    DUMP_ORIGINAL_NAME = 'pages-articles.xml.bz2'

    # dump url
    DUMP_URL_GENERAL = 'http://dumps.wikimedia.org/{lang}wiki/latest/'\
        + '{lang}wiki-latest-' + DUMP_ORIGINAL_NAME

    # md5 checksum file url
    MD5_URL_GENERAL = 'http://dumps.wikimedia.org/{lang}wiki/latest/'\
        + '{lang}wiki-latest-md5sums.txt'

    def __init__(self, language, sample_size=None, logfile=None):
        """Initalization of WikiCorpus instance

        :language: unicode
        :logfile: unicode
        """
        # TODO: check if language is in dictionary of iso codes
        self._language = language

        # make sure sample size is either positive integer or None
        if sample_size is None:
            self._sample_size = None
        else:
            if not isinstance(sample_size, int) or sample_size <= 0:
                raise CorpusException('Sample size has to be positive integer')
            self._sample_size = sample_size

        # TODO: logging
        self._logfile = logfile

        # load configuration
        self._configuration = Configuration(WikiCorpus.CORPUS_CONFIG_PATH)

    # ------------------------------------------------------------------------
    # getters and setters
    # ------------------------------------------------------------------------

    def get_corpus_name(self):
        """ Returns corpus name
        """
        if self.is_sample():
            return self._configuration.get('sample-corpus-name').format(
                lang=self.language(),
                size=self.sample_size())
        else:
            return self._configuration.get('corpus-name').format(
                lang=self.language())

    def get_dump_path(self):
        """ Returns path to dump
        """
        # full dumps are bzipped, while sample dumps are uncompressed
        if self.is_sample():
            ext = self._configuration.get('extensions', 'uncompressed-dump')
        else:
            ext = self._configuration.get('extensions', 'compressed-dump')

        # dump file name = corpus name + extension
        dump_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=ext)

        # path = path to verticals + dump file name
        path = os.path.join(
            self.get_uncompiled_corpus_path(),
            dump_file_name)
        return path

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

    def is_sample(self):
        """ Returns True if this is a sample corpus
        """
        return bool(self.sample_size())

    def language(self):
        """ Returns corpus language
        """
        return self._language

    def sample_size(self):
        """ Returns sample size if this is a sample corpus,
            None otherwise
        """
        return self._sample_size

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
            # TODO: use logging instead of prins (everywhere)
            print 'Dump {name} already exists.'.format(name=dump_path)
            return

        # select dump url
        dump_url = WikiCorpus.DUMP_URL_GENERAL.format(lang=self.language())

        # TODO: logging
        print 'Start downloading {lang}-wiki dump from {url} into {path}'\
            .format(lang=self.language(), url=dump_url, path=dump_path)

        # find MD5 checksum
        md5_url = WikiCorpus.MD5_URL_GENERAL.format(lang=self.language())
        md5sums = get_online_file(md5_url, lines=True)
        for file_md5, file_name in map(lambda x: x.split(), md5sums):
            if file_name.endswith(WikiCorpus.DUMP_ORIGINAL_NAME):
                md5sum = file_md5
                break
        else:
            # TODO logging
            print 'no matching MD5 checksum for the dump found'
            md5sum = None

        # downloading
        download_large_file(dump_url, dump_path, md5sum=md5sum)

        # TODO: logging
        print 'Downloading finished: {lang}-wiki dump is in {path}'.format(
            lang=self.language(),
            path=dump_path)

    def create_sample_dump(self):
        """ Creates smaller sample dump from large dump of given language
        """
        parent_corpus = WikiCorpus(self.language())
        dump_path = parent_corpus.get_dump_path()
        sample_path = self.get_dump_path()
        print dump_path, '->', sample_path
        #raise NotImplementedError

    def create_prevertical(self):
        """ Parses dump (outer XML, inner Wiki Markup) and creates prevertical
        """
        # pomoci lxml prochazet velke xml clanek po clanku (viz wikiindexer.py)
        # a parsovat jednotlive clanky viz puvodni wikicorpora.py, vysledny
        # prevertikal prubezne zapisovat do vystupniho souboru

        dump_path = self.get_dump_path()
        prevertical_path = self.get_prevertical_path()
        print dump_path, '->', prevertical_path
        #raise NotImplementedError

    def tokenize_prevertical(self):
        """ Performes tokenization of prevertical
        """
        prevertical_path = self.get_prevertical_path()
        vertical_path = self.get_vertical_path()
        print prevertical_path, '->', vertical_path
        #raise NotImplementedError

    def morfologize_vertical(self, add_tags=True, add_lemmas=True):
        """ Adds morfological tag and/or lemma for each token in the vertical
        """
        vertical_path = self.get_vertical_path()
        print '<->', vertical_path
        #raise NotImplementedError

    def infere_terms_occurences(self):
        """ Labels all occurences of terms in morfolgized vertical
        """
        vertical_path = self.get_vertical_path()
        print '<->', vertical_path
        #raise NotImplementedError

    def compile_corpus(self):
        """ Compiles given corpora
        """
        # Creates configuration file, if it hasn't existed already
        vertical_path = self.get_vertical_path()
        compiled_corpus_path = self.get_compiled_corpus_path()
        print vertical_path, '->', compiled_corpus_path
        #raise NotImplementedError

    # ------------------------------------------------------------------------
    #
    # ------------------------------------------------------------------------

    def print_info(self):
        """ Returns corpus summary
        """
        print 'corpus name:', self.get_corpus_name
        #raise NotImplementedError

    # ------------------------------------------------------------------------
    #  private methods
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    #  magic methods
    # ------------------------------------------------------------------------

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        if self.is_sample():
            return 'WikiCorpus(language={lang}, sample_size={size})'\
                .format(lang=self.language(), size=self.sample_size())
        else:
            return 'WikiCorpus({lang})'.format(lang=self.language())

    def __unicode__(self):
        return repr(self)


class CorpusException(Exception):
    """ Class for reprezentation of exception raised during building corpus
    """
    pass
