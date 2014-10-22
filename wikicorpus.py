#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
#from lxml import etree
#import bz2


class WikiCorpus(object):

    """Class representing corpus from Wikipedia of one language """

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

    # ------------------------------------------------------------------------
    # getters and setters
    # ------------------------------------------------------------------------

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
            if True, downloads dump even if some dump with
            target name is already downloaded
        """
        raise NotImplementedError

    def create_sample_dump(self):
        """ Creates smaller sample dump from large dump of given language
        """
        raise NotImplementedError

    def create_prevertical(self):
        """ Parses dump (outer XML, inner Wiki Markup) and creates prevertical
        """
        # pomoci lxml prochazet velke xml clanek po clanku (viz wikiindexer.py)
        # a parsovat jednotlive clanky viz puvodni wikicorpora.py, vysledny
        # prevertikal prubezne zapisovat do vystupniho souboru
        raise NotImplementedError

    def tokenize_prevertical(self):
        """ Performes tokenization of prevertical
        """
        raise NotImplementedError

    def morfologize_vertical(self, add_tags=True, add_lemmas=True):
        """ Adds morfological tag and/or lemma for each token in the vertical
        """
        raise NotImplementedError

    def infere_terms_occurences(self):
        """ Labels all occurences of terms in morfolgized vertical
        """
        raise NotImplementedError

    def compile_corpus(self):
        """ Compiles given corpora
        """
        # Creates configuration file, if it hasn't existed already
        raise NotImplementedError

    # ------------------------------------------------------------------------
    #
    # ------------------------------------------------------------------------

    def print_info(self):
        """ Returns corpus summary
        """
        raise NotImplementedError

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
    """ Class for exception reprezentation raised during building corpus
    """
    pass
