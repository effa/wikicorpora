#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from collections import defaultdict
#from environment import environment
#from registry.tagsets import TAGSETS
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

    PIPELINES = defaultdict(lambda: "unitok_and_sentences -l other", {
        "ca": "unitok_and_sentences -l other",
        "ru": "/opt/RFTagger/tools/rft-tt-russian.sh",
        "cs": "/opt/majka_pipe/majka-czech.sh",
        "el": "unitok_and_sentences -l other",
        "tg": "unitok_and_sentences -l other",
        "ka": "unitok_and_sentences -l other",
        "my": "unitok_and_sentences -l other",
        "ar": "/opt/stanford_nlptools/stanford_arabic.sh",
        "kk": "unitok_and_sentences -l other",
        "nl": "/opt/TreeTagger/tools/tt-dutch.sh",
        "et": "/opt/TreeTagger/tools/tt-estonian.sh",
        "uk": "unitok_and_sentences -l other",
        "tr": "unitok_and_sentences -l other",
        "fi": "/opt/TreeTagger/tools/tt-finnish.sh",
        "ro": "unitok_and_sentences -l other",
        "yo": "unitok_and_sentences -l yoruba -a",
        "da": "unitok_and_sentences -l other",
        "sl": "unitok_and_sentences -l other",
        "ur": "unitok_and_sentences -l other",
        "sk": "unitok_and_sentences -l other",
        "ml": "",
        "bg": "/opt/TreeTagger/tools/tt-bulgarian.sh",
        "fa": "unitok_and_sentences -l other",
        "yi": "unitok_and_sentences -l other",
        "hy": "unitok_and_sentences -l other",
        "he": "hebtokeniser_and_sentences",
        "sv": "/opt/hunpos_pipe/hunpos_swedish.sh",
        "zh-tw": "/opt/stanford_nlptools/stanford_chinese.sh",
        "md": "unitok_and_sentences -l maldivian -a",
        "es": "",
        "is": "unitok_and_sentences -l other",
        "hu": "/opt/hunpos_pipe/hunpos_hungarian.sh",
        "ja": "/opt/Comainu/script/runMecabUnidicComainu_split.sh",
        "la": "unitok_and_sentences -l other",
        "fr": "/opt/TreeTagger/tools/tt-french.sh",
        "pl": "",
        "lv": "unitok_and_sentences -l other",
        "hi": "unitok_and_sentences -l other",
        "hr": "/opt/hunpos_pipe/hunpos_croatian.sh",
        "eu": "unitok_and_sentences -l other",
        "de": "/opt/RFTagger/tools/rft-tt-german.sh",
        "zh": "/opt/stanford_nlptools/stanford_chinese.sh",
        "ta": "",
        "sr": "/opt/hunpos_pipe/hunpos_serbian.sh",
        "gu": "",
        "bs": "",
        "ko": "/opt/HanNanumTagger/runHanNanumTagger.sh",
        "bn": "unitok_and_sentences -l other",
        "ga": "unitok_and_sentences -l other",
        "lt": "unitok_and_sentences -l other",
        "mt": "unitok_and_sentences -l other",
        "it": "/opt/TreeTagger/tools/tt-italian-mb.sh",
        "tn": "unitok_and_sentences -l other",
        "sw": "unitok_and_sentences -l other",
        "bo": "",
        "vi": "unitok_and_sentences -l other",
        "cy": "unitok_and_sentences -l other",
        "id": "unitok_and_sentences -l other",
        "ms": "unitok_and_sentences -l other",
        "gl": "unitok_and_sentences -l other",
        "ne": "unitok_and_sentences -l devanagari -a",
        "th": "unitok_and_sentences -l other",
        "en": "/opt/TreeTagger/tools/tt-english.sh",
        "pt": "",
        "mn": "unitok_and_sentences -l other",
        "no": "unitok_and_sentences -l other",
        "eo": "unitok_and_sentences -l other",
    })

    ## unitok languages names
    #UNITOK_LANGUAGES = defaultdict(lambda: 'other', (
    #    ('en', 'english'),
    #    ('fr', 'french'),
    #    ('de', 'german'),
    #    ('it', 'italian'),
    #    ('es', 'spanish'),
    #    ('nl', 'dutch'),
    #    ('cs', 'czech'),
    #    ('sv', 'swedish'),
    #    ('fi', 'finnish'),
    #    ('el', 'greek'),
    #    ('da', 'danish'),
    #    ('hi', 'hindi')))

    ## languages allowed for treetagger
    #TREETAGGER_LANGUAGES = defaultdict(lambda: None, (
    #    ('bg', 'bulgarian'),
    #    ('en', 'english'),
    #    ('fi', 'finnish'),
    #    ('fr', 'french'),
    #    ('nl', 'dutch'),
    #    ('de', 'german'),
    #    ('es', 'spanish'),
    #    ('ru', 'russian'),
    #    ('it', 'italian')))

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

    def get_language(self):
        return self._lang

    #def get_unitok_language(self):
    #    """Returns name of language in form which is needed by unitok
    #    """
    #    return self.UNITOK_LANGUAGES[self.get_language()]

    #def get_treetagger_language(self):
    #    """For treetagger-supported languages, returns language full name

    #    :iso_code: unicode (alpha-2 code of the language)

    #    :returns: unicode (name of the language) || None
    #    """
    #    return self.TREETAGGER_LANGUAGES[self.get_language()]

    # ------------------------------------------------------------------------
    #  resources control
    # ------------------------------------------------------------------------

    def close_all_resources(self):
        """Closes all allocated resources
        """
        # NOTE: current implementation can't have any opened resources, but if
        # the behavior chang in the future, use this place to make sure all
        # resources are close
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
        pipeline = self.PIPELINES[language]
        try:
            # handle case of input_path == output_path
            tmp_output_path = vertical_path + '.tmp'
            command = '{pipeline} <{inp} >{outp}'\
                .format(pipeline=pipeline,
                        inp=prevertical_path,
                        outp=tmp_output_path)
            task = Popen(command, shell=True)
            task.wait()
            if task.returncode != 0:
                raise LanguageProcessorException('verticalization pipeline failed')
            call(('mv', tmp_output_path, vertical_path))
        except OSError:
            raise LanguageProcessorException(
                'OSError during verticalization')
#        if language == 'cs':
#            # for czech language, use unitok + desamb
#            self.tokenize(prevertical_path, vertical_path)
#            self.desamb_morfologization(vertical_path, vertical_path)
#            return TAGSETS.DESAMB
##        elif language in self.TREETAGGER_LANGUAGES:
#            # use a treetagger script for both tokenization and morfologization
#            self.treetagger_morfologization(prevertical_path, vertical_path)
#            return TAGSETS.TREETAGGER
#        else:
#            # for other languages, at least tokenize them and tag sentences
#            self.tokenize(prevertical_path, vertical_path)
#            self.tag_sentences(vertical_path)
#            return TAGSETS.BASIC

    #def desamb_morfologization(self, input_path, output_path):
    #    """Uses desamb for adding tags and lemmas [works for czech only]

    #    :input_path: unicode
    #    :output_path: unicode
    #    """
    #    assert self.get_language() == 'cs', 'desamb works only for czech'
    #    desamb_path = environment.get_desamb_path()
    #    # handle frequent case of input_path == output_path
    #    tmp_output_path = output_path + '.tmp'
    #    try:
    #        desamb_command = '{desamb} {inputp} > {outputp}'\
    #            .format(desamb=desamb_path,
    #                    inputp=input_path,
    #                    outputp=tmp_output_path)
    #        task = Popen(desamb_command, shell=True)
    #        task.wait()
    #        if task.returncode != 0:
    #            raise LanguageProcessorException('desamb failed')
    #        call(('mv', tmp_output_path, output_path))
    #    except OSError:
    #        raise LanguageProcessorException('OSError when calling desamb')

    #def tag_sentences(self, vertical_path):
    #    """Tag sentences in tokenized vertical file.

    #    :vertical_path: unicode
    #        path to vertical file
    #    """
    #    try:
    #        tmp_output_path = vertical_path + '.tmp'
    #        sentence_tagger_cmd = '{tagger} <{inp} >{outp}'\
    #            .format(tagger=environment.get_sentencetagger_path(),
    #                    inp=vertical_path,
    #                    outp=tmp_output_path)
    #        task = Popen(sentence_tagger_cmd, shell=True)
    #        task.wait()
    #        if task.returncode != 0:
    #            raise LanguageProcessorException('sentence-tagger failed')
    #        call(('mv', tmp_output_path, vertical_path))
    #    except OSError:
    #        raise LanguageProcessorException(
    #            'OSError when calling sentence tagger')

    #def tokenize(self, prevertical_path, vertical_path):
    #    """Tokenizes prevertical.

    #    :prevertical_path: unicode
    #        path to prevertical file
    #    :vertical_path: unicode
    #        where to store result vertical file
    #    """
    #    assert prevertical_path != vertical_path
    #    unitok_path = environment.get_unitok_path()
    #    try:
    #        unitok_cmd = '{unitok} --language={lang} -a {prevert} > {vert}'\
    #            .format(unitok=unitok_path,
    #                    lang=self.get_unitok_language(),
    #                    prevert=prevertical_path,
    #                    vert=vertical_path)
    #        # -a ... better support for abbreviations
    #        task = Popen(unitok_cmd, shell=True)
    #        task.wait()
    #        if task.returncode != 0:
    #            raise LanguageProcessorException('unitok failed')
    #    except OSError:
    #        raise LanguageProcessorException('OSError when calling unitok')

    #def treetagger_morfologization(self, input_path, output_path):
    #    """Uses TreeTagger for adding tags and lemmas

    #    :input_path: unicode
    #    :output_path: unicode
    #    """
    #    assert self.get_language() in self.TREETAGGER_LANGUAGES
    #    treetagger_path = environment.get_treetagger_path(
    #        self.get_treetagger_language())
    #    try:
    #        # handle case of input_path == output_path
    #        tmp_output_path = output_path + '.tmp'
    #        # call treetagger script
    #        command = '{treetagger} <{inp} >{outp}'\
    #            .format(treetagger=treetagger_path,
    #                    inp=input_path,
    #                    outp=tmp_output_path)
    #        task = Popen(command, shell=True)
    #        task.wait()
    #        if task.returncode != 0:
    #            raise LanguageProcessorException('treetagger failed')
    #        call(('mv', tmp_output_path, output_path))
    #    except OSError:
    #        raise LanguageProcessorException(
    #            'OSError when calling treetagger')


# ---------------------------------------------------------------------------
#  Exceptions
# ---------------------------------------------------------------------------
class LanguageProcessorException(Exception):
    """ Class for reprezentation of exception raised during language processing
    """
    pass
