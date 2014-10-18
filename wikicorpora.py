#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from system_utils import choose_path
#from wikidownloader import download_dump
#from wikisampler import create_sample_dump
import argparse


def dump_to_prevertical(lang, dump_path=None, prevertical_path=None):
    """ Parses dump (outer XML and inner Wiki Markup) and creates prevertical
    """
    # pomoci lxml prochazet velke xml clanek po clanku (viz wikiindexer.py)
    # a parsovat jednotlive clanky viz puvodni wikicorpora.py, vysledny
    # prevertikal prubezne zapisovat do vystupniho souboru
    raise NotImplementedError


def tokenize_prevertical(lang, prevertical_path=None, vertical_path=None):
    """ Tokenizes given prevertical
    """
    prevertical_path = prevertical_path or choose_path(lang, 'prevert')
    vertical_path = vertical_path or choose_path(lang, 'vert')
    raise NotImplementedError


def tag_and_lemmatize_vertical(lang, input_vertical_path=None,
                               output_vertical_path=None):
    """ Adds POS tag and lemma for each token in the vertical
    """
    raise NotImplementedError


def terms_exploration(lang, input_vertical_path=None,
                      output_vertical_path=None):
    """ Labels all occurences of terms
    """
    raise NotImplementedError


def compile_corpus(lang, vertical_path=None, compiled_corpus_path=None):
    """ Compiles given corpora
    """
    # Creates configuration file, if it hasn't existed already
    raise NotImplementedError


def main():
    """ Main function handling calling this script with arguments
    """
    parser = argparse.ArgumentParser()

    # requried arugments
    required_group = parser.add_argument_group('required')
    required_group.add_argument('-l', '--language', required=True,
                        help='2-letter code of language (ISO-639-1)')

    # general options
    parser.add_argument('-s', '--sample-size',
                        help='create sample from first SAMPLE_SIZE articles')
    parser.add_argument('--logfile',
                        help='path to logfile')

    # options concerning phases
    phases_group = parser.add_argument_group('phases',
        description='You can specify phases to carry out. If no phase is'
            + ' explicitly selected, all steps are executed.')
    phases_group.add_argument('-d', '--download', action='store_true',
                              help='download dump')
    phases_group.add_argument('-p', '--prevertical', action='store_true',
                              help='process dump to prevertical')
    phases_group.add_argument('-t', '--tokenization', action='store_true',
                              help='tokenize prevertical')
    phases_group.add_argument('-m', '--tagging', action='store_true',
                              help='add morphological tag to each token')
    phases_group.add_argument('-f', '--lemmatization', action='store_true',
                              help='add lemma (canonical form) to each token')
    phases_group.add_argument('-i', '--terms-inference', action='store_true',
                              help='infere all terms occurences')
    phases_group.add_argument('-c', '--compile', action='store_true',
                              help='create configuration file and'
                                   + ' compile corpus')

    # options concerning phases
    reexecution_group = parser.add_argument_group('re-execution behaviour',
        description='If required output file (of any phase) already exists,'
            + ' default behaviour is to ask whether re-execute the phase.'
            + ' You can change this behavious to either never re-execute'
            + ' (--never-re-execute) or always re-execute'
            + ' (--always-re-execute)')
    reexecution_group.add_argument('--never-re-execute', action='store_true',
                              help='if output file exists, do nothing')
    reexecution_group.add_argument('--always-re-execute', action='store_true',
                              help='force re-execution')

    args = parser.parse_args()

    print args


if __name__ == '__main__':
    main()
