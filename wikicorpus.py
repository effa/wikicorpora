#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
#from lxml import etree
#import bz2
import os
import yaml


class WikiCorpus(object):

    CORPUS_CONFIG_PATH = './config.yaml'

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

        # load configuration
        with open(WikiCorpus.CORPUS_CONFIG_PATH) as config_file:
            self._configuration_dict = yaml.load(config_file)

    # ------------------------------------------------------------------------
    # getters and setters
    # ------------------------------------------------------------------------

    def get_corpus_name(self):
        """ Returns corpus name
        """
        if self.is_sample():
            return self._config('sample-corpus-name').format(
                lang=self.language(),
                size=self.sample_size())
        else:
            return self._config('corpus-name').format(
                lang=self.language())

    def get_dump_path(self):
        """ Returns path to dump
        """
        # full dumps are bzipped, while sample dumps are uncompressed
        if self.is_sample():
            extension = self._config('extensions', 'uncompressed-dump')
        else:
            extension = self._config('extensions', 'compressed-dump')

        # dump file name = corpus name + extension
        dump_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=extension)

        # path = path to verticals + dump file name
        path = os.path.join(self.get_verticals_dir_path(), dump_file_name)
        return path

    def get_prevertical_path(self):
        """ Returns path to prevertical
        """
        # prevertical file name = corpus name + extension
        prevertical_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=self._config('extensions', 'prevertical'))

        # path = path to verticals + prevertical file name
        path = os.path.join(
            self.get_verticals_dir_path(),
            prevertical_file_name)
        return path

    def get_vertical_path(self):
        """ Returns path to vertical
        """
        # vertical file name = corpus name + extension
        vertical_file_name = '{name}.{ext}'.format(
            name=self.get_corpus_name(),
            ext=self._config('extensions', 'vertical'))

        # path = path to verticals + vertical file name
        path = os.path.join(self.get_verticals_dir_path(), vertical_file_name)
        return path

    def get_verticals_dir_path(self):
        """ Returns path to directory with verticals for this corpus
        """
        return os.path.join(
            self._config('all-verticals-path'),
            self.get_corpus_name())

    def get_compiled_corpus_path(self):
        """ Returns path to directory with compiled corpus
        """
        return os.path.join(
            self._config('all-compiled-corpora-path'),
            self.get_corpus_name())

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
        dump_path = self.get_dump_path()
        print '->', dump_path
        #raise NotImplementedError

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

    def _config(self, *args):
        """ Returns information from configration.

        :*args: key (or series of keys in case of nesting)
        """
        # TODO: wrong key handling
        conf = self._configuration_dict
        for key in args:
            conf = conf[key]
        return conf

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
