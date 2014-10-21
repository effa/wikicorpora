#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
#from wikidownloader import download_dump
#from wikisampler import create_sample_dump
from wikicorpus import WikiCorpus
import argparse

"""
This is a main file for wikicorpora command line application.
It parses arguments and performes selected actions.
"""


def main():
    """ Main function handling calling this script with arguments
    """
    parser = argparse.ArgumentParser()

    # language arguments
    language_group = parser.add_argument_group('corpus language')
    language_group.add_argument('-l', '--language', required=True,
        help='2-letter code of language (ISO-639-1)')

    # sample options
    sample_group = parser.add_argument_group('sample options')
    sample_group.add_argument('-s', '--sample-size',
        help='create sample from first SAMPLE_SIZE articles')

    # general options
    parser.add_argument('--logfile',
        help='path to logfile')
    parser.add_argument('--info', action='store_true',
        help='print corpus summary')

    # download options
    download_group = parser.add_argument_group('download options')
    soft_or_force_group = download_group.add_mutually_exclusive_group()
    soft_or_force_group.add_argument('--soft-download', action='store_true',
        help='download dump if not already downloaded')
    soft_or_force_group.add_argument('--force-download', action='store_true',
        help='download dump (even if a dump already exists)')

    # options concerning phases
    phases_group = parser.add_argument_group('corpus processing phases')
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
    phases_group.add_argument('-a', '--all-phases', action='store_true',
        help='execute all corpus processing steps')

    # compilaton options
    compilation_group = parser.add_argument_group('compilation options')
    compilation_group.add_argument('-c', '--compile', action='store_true',
        help='create configuration file and compile corpus')

    args = parser.parse_args()

    # if no action is specified, print corpus info
    no_action = not any([args.force_download, args.soft_download,
        args.sample_size, args.prevertical, args.tokenization, args.tagging,
        args.lemmatization, args.terms_inference, args.compile])
    if no_action:
        args.info = True

    sample_size = int(args.sample_size) if args.sample_size else None
    corpus_builder = WikiCorpus(args.language, sample_size)
    print corpus_builder

    #success = True
    #if args.download or execute_all_phases:
    #    success = corpus_builder.download_corpus()
    #if success and (args.prevertical or execute_all_phases)

    print args


if __name__ == '__main__':
    main()
