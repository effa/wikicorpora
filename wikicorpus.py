#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals


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
            assert type(sample_size) == int and sample_size > 0
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

    def create_prevertical():
        """ Parses dump (outer XML, inner Wiki Markup) and creates prevertical
        """
        # pomoci lxml prochazet velke xml clanek po clanku (viz wikiindexer.py)
        # a parsovat jednotlive clanky viz puvodni wikicorpora.py, vysledny
        # prevertikal prubezne zapisovat do vystupniho souboru
        raise NotImplementedError

    def tokenize_prevertical():
        """ Performes tokenization of prevertical
        """
        raise NotImplementedError

    def morfologize_vertical(add_tags=True, add_lemmas=True):
        """ Adds morfological tag and/or lemma for each token in the vertical
        """
        raise NotImplementedError

    def infere_terms_occurence():
        """ Labels all occurences of terms in morfolgized vertical
        """
        raise NotImplementedError

    def compile_corpus():
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
