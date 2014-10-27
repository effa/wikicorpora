#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from lxml import etree
from xml_utils import qualified_name
from wikicorpus import WikiCorpus, CorpusException


class SampleWikiCorpus(WikiCorpus):

    """Class representing sample corpus from Wikipedia of one language """

    def __init__(self, language, sample_size=None):
        """Initalization of WikiCorpus instance

        :language: unicode
        """
        # superclass inititalization
        super(SampleWikiCorpus, self).__init__(language)

        # set sample size
        if not isinstance(sample_size, int) or sample_size <= 0:
            raise SampleCorpusException(
                'Sample size has to be positive integer')
        self._sample_size = sample_size

    # ------------------------------------------------------------------------
    # getters and setters
    # ------------------------------------------------------------------------

    def get_corpus_name(self):
        """ Returns corpus name
        """
        return self._configuration.get('sample-corpus-name').format(
            lang=self.language(),
            size=self.sample_size())

    def get_parent_corpus(self):
        """Returns parent corpus instance (e.g. corpus for full language)
        """
        return WikiCorpus(self.language())

    def is_dump_compressed(self):
        """Returns True if dumps is compress, False otherwise.
        """
        # dumps for samples are always uncompressed
        return False

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
        # since this is a sample dump, we will download parent (full) dump
        self.get_parent_corpus().download_dump(force)

    def create_sample_dump(self, articles=None):
        """ Creates smaller sample dump from large dump of given language

        :articles: list/set of unicodes [optional]
            Titles of articles you want to appear in sample. Number of titles
            is arbitrary, if there are too many of them, some will be ommited,
            if there are too few, smaller dump will be created and message
            will be displayed.
        """
        # TODO: check that all items of articles are unicodes, not just str

        # find parent dump
        parent = self.get_parent_corpus()

        # select sample path
        sample_path = self.get_dump_path()

        # find the namespace
        with parent._open_dump() as dump_file:
            # read first event, which is ('start', root element),
            context_for_ns = etree.iterparse(dump_file, events=('start',))
            _, root = context_for_ns.next()
            # get namespace information from the root element,
            # None means implicit namespace (without prefix)
            namespace = root.nsmap[None]
            del context_for_ns

        # articles specified
        if articles:
            specific_sample = True
            articles = set(articles)
        else:
            specific_sample = False

        # create qualified names (= names with namespaces) for tags we need
        page_tag = qualified_name('page', namespace)
        title_tag = qualified_name('title', namespace)
        redirect_tag = qualified_name('redirect', namespace)

        # iterate through xml and build a sample file
        with parent._open_dump() as dump_file:
            context = etree.iterparse(dump_file, events=('end',), tag=page_tag)
            sample_root = etree.Element('mediawiki', nsmap={None: namespace})
            pages = 0
            # omit first 3 articles (Main page and similar meta-articles)
            for _ in range(3):
                next(context)
            for event, elem in context:
                # ignore redirect pages
                if elem.find(redirect_tag) is not None:
                    continue
                # find content of title element
                title = elem.findtext(title_tag)
                # if articles are not specified, take any article,
                # if they are specified, check if this is wanted article
                if not specific_sample or title in articles:
                    sample_root.append(elem)
                    pages += 1
                    if pages == self.sample_size():
                        break
                    if specific_sample:
                        articles.remove(title)
                # TODO: cleanup ?! (je mozne, ze bude prochazate cely dump!)
            del context

        # check if sample is of required size
        if pages < self.sample_size():
            # TODO: logging
            print 'Failed to create sample of {number} pages.'.format(
                number=self.sample_size())
            if articles:
                print 'Following articles not found:'
                print '\n'.join(['- ' + title for title in articles])

        # write sample xml to file
        with open(sample_path, 'w') as sample_file:
            sample_file.write(etree.tostring(sample_root,
                pretty_print=True,
                xml_declaration=True))

        # log info (TODO: logging)
        print 'Sample of {pages} pages created at {path}'.format(
            pages=pages, path=sample_path)

    # ------------------------------------------------------------------------
    #  magic methods
    # ------------------------------------------------------------------------

    def __repr__(self):
        return 'WikiCorpus(language={lang}, sample_size={size})'\
            .format(lang=self.language(), size=self.sample_size())


# ---------------------------------------------------------------------------
#  Exceptions
# ---------------------------------------------------------------------------

class SampleCorpusException(CorpusException):
    """Exceptions raised while working with sample corpus
    """
    pass
