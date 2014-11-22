#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from copy import deepcopy
from lxml import etree
from progressbar import ProgressBar
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
        namespace = parent.get_namespace()

        # articles specified
        if articles:
            specific_sample = True
            articles = set(articles)
        else:
            specific_sample = False

        # create qualified names (= names with namespaces) for tags we need
        TEXT_TAG = qualified_name('text', namespace)
        TITLE_TAG = qualified_name('title', namespace)
        REDIRECT_TAG = qualified_name('redirect', namespace)
        NS_TAG = qualified_name('ns', namespace)

        # iterate through xml and build a sample file
        with parent._open_dump() as dump_file:
            context = etree.iterparse(dump_file, events=('end',))
            # create root under which we will add sample articles
            sample_root = etree.Element('mediawiki', nsmap={None: namespace})
            skip = True
            pages = 0
            last_title = None
            if specific_sample:
                # in case of specific sample, it's easily possible
                # that we will need to go through the whole dump
                # -> meassure progress as a ratio of processed part
                progressbar = ProgressBar(parent.get_dump_length())
            else:
                progressbar = ProgressBar(self.sample_size())
            for event, elem in context:
                if elem.tag == REDIRECT_TAG:
                    # ignore redirect pages
                    skip = True
                elif elem.tag == NS_TAG:
                    last_ns = elem.text
                    if elem.text != WikiCorpus.ARTICLE_NS:
                        skip = True
                elif elem.tag == TITLE_TAG:
                    # remember the title
                    last_title = elem.text
                elif elem.tag == TEXT_TAG:
                    if skip:
                        skip = False
                        continue
                    # if articles are not specified, take any article,
                    # if they are specified, check if this is wanted article
                    if not specific_sample or last_title in articles:
                        # build page node with title and text subelements
                        page_node = etree.Element('page')
                        title_node = etree.SubElement(page_node, 'title')
                        title_node.text = last_title
                        ns_node = etree.SubElement(page_node, 'ns')
                        ns_node.text = last_ns
                        page_node.append(deepcopy(elem))  # text
                        # append this node to sample articles
                        sample_root.append(page_node)
                        pages += 1
                        if specific_sample:
                            articles.remove(last_title)
                        if pages == self.sample_size():
                            break
                    # progress update
                    if specific_sample:
                        progressbar.update(dump_file.tell())
                    else:
                        progressbar.update(pages)
                # cleanup
                elem.clear()
                #while elem.getprevious() is not None:
                #    del elem.getparent()[0]
                for ancestor in elem.xpath('ancestor-or-self::*'):
                    while ancestor.getprevious() is not None:
                        del ancestor.getparent()[0]
            del context
            progressbar.finish()

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
        print 'Sample of {pages} pages created\nat: {path}'.format(
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
