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

    # languages allowed for treetagger
    TREETAGGER_LANGUAGES = defaultdict(lambda: None, (
        ('bg', 'bulgarian'),
        ('en', 'english'),
        ('fr', 'french'),
        ('nl', 'dutch'),
        ('de', 'german'),
        ('es', 'spanish'),
        ('ru', 'russian'),
        ('it', 'italian')))

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
    #  static methods
    # ------------------------------------------------------------------------

    #@staticmethod
    #def get_treetagger_language(iso_code):
    #    """For treetagger-supported languages, returns language full name

    #    :iso_code: unicode (alpha-2 code of the language)

    #    :returns: unicode (name of the language) || None
    #    """
    #    return NaturalLanguageProcessor.TREETAGGER_LANGUAGES[iso_code]

    # ------------------------------------------------------------------------
    #  property access methods
    # ------------------------------------------------------------------------

    def get_language(self):
        return self._lang

    def get_unitok_language(self):
        """Returns name of language in form which is needed by unitok
        """
        return self.UNITOK_LANGUAGES[self.get_language()]

    def get_treetagger_language(self):
        """For treetagger-supported languages, returns language full name

        :iso_code: unicode (alpha-2 code of the language)

        :returns: unicode (name of the language) || None
        """
        return self.TREETAGGER_LANGUAGES[self.get_language()]
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

    def create_vertical_file(self, prevertical_path, vertical_path):
        """ Creates a vertical file.

        Performes tokenization of prevertical and for some languages
        also morfologization (adding morfological tag and lemma/lempos)

        :prevertical_path: unicode
            path to prevertical file
        :vertical_path: unicode
            where to store result vertical file
        """
        language = self.get_language()
        if language == 'cs':
            # for czech language, use unitok + desamb
            self.tokenize(prevertical_path, vertical_path)
            self.desamb_morfologization(vertical_path, vertical_path)
        elif language in self.TREETAGGER_LANGUAGES:
            # use a treetagger script for both tokenization and morfologization
            treetagger_path = environment.get_treetagger_path(
                self.get_treetagger_language())
            try:
                # handle case of input_path == output_path
                tmp_output_path = vertical_path + '.tmp'
                ## treetagger needs file in iso-8858-1 encoding, so we need
                ## convert it first
                #command = '{conv} <{inp} | {treetagger} {lang} {opt} >{outp}'\
                #    .format(treetagger=treetagger_path,
                #            lang=self.get_treetagger_language(language),
                #            opt='-token -lemma -no-unknown -sgml',
                #            conv='iconv -f utf-8 -t iso-8859-1//TRANSLIT',
                #            inp=prevertical_path,
                #            outp=tmp_output_path)
                command = '{treetagger} <{inp} >{outp}'\
                    .format(treetagger=treetagger_path,
                            inp=prevertical_path,
                            outp=tmp_output_path)
                task = Popen(command, shell=True)
                task.wait()
                if task.returncode != 0:
                    raise LanguageProcessorException('treetagger failed')
                call(('mv', tmp_output_path, vertical_path))
            except OSError:
                raise LanguageProcessorException(
                    'OSError when calling treetagger')
        else:
            # for other languages, at least tokenize them
            self.tokenize()

    def desamb_morfologization(self, input_path, output_path):
        """Uses desamb for adding tags and lemmas [works for czech only]

        :input_path: unicode
        :output_path: unicode
        """
        assert self.get_language() == 'cs', 'desamb works only for czech'
        desamb_path = environment.get_desamb_path()
        # handle frequent case of input_path == output_path
        tmp_output_path = output_path + '.tmp'
        try:
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

    def tokenize(self, prevertical_path, vertical_path):
        """Tokenizes prevertical.

        :prevertical_path: unicode
            path to prevertical file
        :vertical_path: unicode
            where to store result vertical file
        """
        assert prevertical_path != vertical_path
        unitok_path = environment.get_unitok_path()
        try:
            unitok_command = '{unitok} --language={lang} {prevert} > {vert}'\
                .format(unitok=unitok_path,
                        lang=self.get_unitok_language(),
                        prevert=prevertical_path,
                        vert=vertical_path)
            task = Popen(unitok_command, shell=True)
            task.wait()
            if task.returncode != 0:
                raise LanguageProcessorException('unitok failed')
        except OSError:
            raise LanguageProcessorException('OSError when calling unitok')


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
