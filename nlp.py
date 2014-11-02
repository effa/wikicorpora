#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from collections import defaultdict
from environment import environment
from subprocess import Popen, call

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

    #def can_lemmatize(self):
    #    return self.lang() in NaturalLanguageProcessor.LEMMATIZABLE_LANGUAGES

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
        unitok_path = environment.get_unitok_path()
        # TODO: tahle podminka by mela byt nadbytecna (viz configuration.py)
        #if not unitok_path:
        #    raise LanguageProcessorException(
        #        'No path for unitok in configuration.')
        try:
            unitok_command = '{unitok} --language={lang} {prevert} > {vert}'\
                .format(unitok=unitok_path,
                        lang=self.get_unitok_language_name(),
                        prevert=prevertical_path,
                        vert=vertical_path)
            task = Popen(unitok_command, shell=True)
            task.wait()
            if task.returncode != 0:
                raise LanguageProcessorException('unitok failed')
        except OSError:
            raise LanguageProcessorException('OSError when calling unitok')

    def morfologize(self, input_path, output_path,
                    add_tags=True, add_lemmas=True):
        """Adds tags and/or lemmas to given vertical.
        """
        # TODO: podle popisu na http://nlp.fi.muni.cz/ma/ by mela majka
        # fungovat pro Czech, Slovak, Polish, Swedish, German, French, Italian,
        # English, Portuguese, Catalan, Welsh, Spanish, Galician, Asturian
        # and Russian.
        # TODO: umoznit udelat pro cestinu jen tagy / jen lemmata:
        if self.get_language() == 'cs':
            # for czech language, use desamb
            desamb_path = environment.get_desamb_path()
            try:
                # handle frequent case of input_path == output_path
                tmp_output_path = output_path + '.tmp'
                desamb_command = '{desamb} {inputp} > {outputp}'\
                    .format(desamb=desamb_path,
                            inputp=input_path,
                            outputp=tmp_output_path)
                task = Popen(desamb_command, shell=True)
                task.wait()
                if task.returncode != 0:
                    raise LanguageProcessorException('desamb failed')
                call(('mv', tmp_output_path, output_path))
            except OSError:
                raise LanguageProcessorException('OSError when calling desamb')
        else:
            if add_tags and add_lemmas:
                wanted_task = 'adding tags and lemmas'
            elif add_lemmas:
                wanted_task = 'adding lemmas'
            else:
                wanted_task = 'adding tags'
            raise LanguageProcessorException(
                'No known tool for adding morfologization information for '
                + wanted_task + ' for ' + self.get_language())

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
