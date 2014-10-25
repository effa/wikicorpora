#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
#from lxml import etree
from wikicorpus import WikiCorpus, CorpusException
#import bz2


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

    #def is_sample(self):
    #    """ Returns True if this is a sample corpus
    #    """
    #    return bool(self.sample_size())

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
        parent_corpus = WikiCorpus(self.language())
        dump_path = parent_corpus.get_dump_path()
        sample_path = self.get_dump_path()
        print dump_path, '->', sample_path
        #raise NotImplementedError

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
