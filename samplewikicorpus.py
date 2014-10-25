#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from lxml import etree
from wikicorpus import WikiCorpus, CorpusException


class SampleWikiCorpus(WikiCorpus):

    """Class representing sample corpus from Wikipedia of one language """

    def __init__(self, language, sample_size=None):
        """Initalization of WikiCorpus instance

        :language: unicode
        """
        # superclass inititalization
        super(SampleWikiCorpus, self).__init__(language)

        # sample size
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

    def create_sample_dump(self):
        """ Creates smaller sample dump from large dump of given language
        """
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

        # iterate through xml and build a sample file
        with parent._open_dump() as dump_file:
            page_tag = '{{{namespace}}}page'.format(namespace=namespace)
            context = etree.iterparse(dump_file, events=('end',), tag=page_tag)
            sample_root = etree.Element('mediawiki', nsmap={None: namespace})
            pages = 0
            for event, elem in context:
                sample_root.append(elem)
                pages += 1
                if pages == self.sample_size():
                    break
            del context

        # write sample xml to file
        with open(sample_path, 'w') as sample_file:
            sample_file.write(etree.tostring(sample_root, pretty_print=True))

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
