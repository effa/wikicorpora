#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from collections import defaultdict
from environment import environment
from subprocess import Popen

"""
Module for natural language processing tasks.
"""


class NaturalLanguageProcessor(object):

    """Class for natural language processor of given language.

    Instance of this class can be used in with-statement as follows:

        with NaturalLanguageProcessor('cs') as language_processor:
            <use language_processor>

    This way, all resources will be closed after end of the with-statement.
    """

    #LEMMATIZABLE_LANGUAGES = ['cs', 'en']

    # unitok languages names
    UNITOK_LANGUAGES = defaultdict(lambda: 'other', (
        ('en', 'english'),
        ('fr', 'french'),
        ('de', 'german'),
        ('it', 'italian'),
        ('es', 'spanish'),
        ('nl', 'dutch'),
        ('cs', 'czech'),
        ('sv', 'swedish'),
        ('fi', 'finnish'),
        ('el', 'greek'),
        ('da', 'danish'),
        ('hi', 'hindi')))

    # ------------------------------------------------------------------------
    #  magic methods
    # ------------------------------------------------------------------------

    def __init__(self, lang=''):
        """ Initalization of the processor

        :lang: unicode (alpha-2 code of the language)
        """
        self._lang = lang

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close_all_resources()

    def __repr__(self):
        return "NaturalLanguageProcessor('{lang}')".format(lang=self.lang())

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.__repr__()

    # ------------------------------------------------------------------------
    #  property access methods
    # ------------------------------------------------------------------------

    def can_lemmatize(self):
        return self.lang() in NaturalLanguageProcessor.LEMMATIZABLE_LANGUAGES

    def get_language(self):
        return self._lang

    def get_unitok_language_name(self):
        """Returns name of language in form which is needed by unitok
        """
        return NaturalLanguageProcessor.UNITOK_LANGUAGES[self.get_language()]

    # ------------------------------------------------------------------------
    #  resources control
    # ------------------------------------------------------------------------

    def close_all_resources(self):
        """Closes all allocated resources
        """
        # TODO: make sure all resources are closed
        pass

    # ------------------------------------------------------------------------
    #  natural language processing
    # ------------------------------------------------------------------------

    def tokenize(self, prevertical_path, vertical_path):
        """Tokenizes prevertical.

        :prevertical_path: unicode
            path to prevertical file
        :vertical_path: unicode
            where to store result vertical file
        """
        language = self.get_unitok_language_name()
        unitok_path = environment.get_unitok_path()
        if not unitok_path:
            raise LanguageProcessorException(
                'No path for unitok in configuration.')
        try:
            task = Popen(args=(unitok_path,
                            '--language={l}'.format(l=language),
                            prevertical_path,
                            '>',
                            vertical_path))
        except OSError:
            raise LanguageProcessorException('OSError')
        task.wait()
        if task.returncode != 0:
            raise LanguageProcessorException('unitok failed')

    # ------------------------------------------------------------------------
    #  private methods
    # ------------------------------------------------------------------------


# ---------------------------------------------------------------------------
#  Exceptions
# ---------------------------------------------------------------------------
class LanguageProcessorException(Exception):
    """ Class for reprezentation of exception raised during language processing
    """
    pass
