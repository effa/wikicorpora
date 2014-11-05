#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from wikicorpus.environment import environment
from wikicorpus.samplewikicorpus import SampleWikiCorpus
from subprocess import call
from wikicorpus.wikicorpus import WikiCorpus, CorpusException
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
    language_group.add_argument('-l', '--language',
        help='2-letter code of language (ISO-639-1)')

    # sample options
    sample_group = parser.add_argument_group('sample options')
    sample_group.add_argument('-s', '--sample-size', type=int,
        help='sample size specification')
    specific_or_not_group = sample_group.add_mutually_exclusive_group()
    specific_or_not_group.add_argument('--create-sample',
        action='store_true',
        help='create sample from first SAMPLE_SIZE articles')
    specific_or_not_group.add_argument('--create-specific-sample',
        action='store_true',
        help='create sample from selected articles')

    # download options
    download_group = parser.add_argument_group('download options')
    soft_or_force_group = download_group.add_mutually_exclusive_group()
    soft_or_force_group.add_argument('--soft-download', action='store_true',
        help='download dump if not already downloaded')
    soft_or_force_group.add_argument('--force-download', action='store_true',
        help='download dump (even if a dump already exists)')

    # options concerning phases
    phases_group = parser.add_argument_group('corpus processing phases')
    phases_group.add_argument('--prevertical', '-p', action='store_true',
        help='process dump to prevertical')
    phases_group.add_argument('--tokenization', '-t', action='store_true',
        help='tokenize prevertical')
    phases_group.add_argument('--tagging', '-m', action='store_true',
        help='add morphological tag to each token')
    phases_group.add_argument('--lemmatization', '-f', action='store_true',
        help='add lemma (canonical form) to each token')
    phases_group.add_argument('--terms-inference', '-i', action='store_true',
        help='infere all terms occurences')
    phases_group.add_argument('--all-phases', '-a', action='store_true',
        help='execute all corpus processing steps')

    # compilaton options
    compilation_group = parser.add_argument_group('compilation options')
    compilation_group.add_argument('--compile', '-c', action='store_true',
        help='create configuration file and compile corpus')

    # general options
    #parser.add_argument('--logfile',
    #    help='path to logfile')
    parser.add_argument('--info', action='store_true',
        help='print corpus summary')

    args = parser.parse_args()

    # if no action is specified, we will print corpus info
    no_action = not any([args.force_download, args.soft_download,
        args.create_sample, args.create_specific_sample,
        args.prevertical, args.tokenization, args.tagging, args.lemmatization,
        args.terms_inference, args.all_phases, args.compile])

    # sample_size has to be either int or None
    sample_size = int(args.sample_size) if args.sample_size else None

    try:
        # no language specified (can be either mistake or command for info
        # about all corpora)
        if not args.language:
            # if it's a call without any options or with --info option only,
            # -> show all corpora
            if no_action and not args.sample_size:
                list_all_corpora()
            else:
                # othewise print error message and command usage
                print 'No language specified (-l XX or --language=XX).'
                parser.print_usage()
            return

        # specific sample
        if args.create_specific_sample:
            # ask for titles
            size = 0
            titles = []
            if sample_size:
                print 'Input {n} titles for new sample.'\
                    .format(n=args.sample_size)
            else:
                print 'Input titles for new sample, '\
                    + 'finish by entering an empty string.'
            while not sample_size or size < sample_size:
                title = raw_input('Title {n}: '.format(n=size + 1))
                if title:
                    titles.append(title.decode('utf-8'))
                    size += 1
                else:
                    # if user inputs empty string and sample_size is not
                    # specified, set sample_size to current size, which
                    # makes the input loop terminate
                    if not sample_size:
                        sample_size = size

        # create corpus instance for given language (and sample_size)
        if sample_size:
            corpus = SampleWikiCorpus(args.language, sample_size)
        else:
            corpus = WikiCorpus(args.language)

        # download dump
        if args.soft_download or args.force_download:
            corpus.download_dump(force=args.force_download)

        # sampling
        if args.create_specific_sample:
            corpus.create_sample_dump(titles)
        elif args.create_sample:
            if not sample_size:
                raise CorpusException('Sample size (--sample-size=X) has to '
                    + ' be specified in order to create sample')
            corpus.create_sample_dump()

        # parsing dump (preverticalization)
        if args.prevertical or args.all_phases:
            corpus.create_prevertical()

        # tokenization
        if args.tokenization or args.all_phases:
            corpus.tokenize_prevertical()

        # morfologization
        if args.tagging or args.lemmatization or args.all_phases:
            corpus.morfologize_vertical(
                add_tags=args.tagging or args.all_phases,
                add_lemmas=args.lemmatization or args.all_phases)

        # terms occurences inference
        if args.terms_inference or args.all_phases:
            corpus.infere_terms_occurences()

        # corpus compilation
        if args.compile:
            corpus.compile_corpus()

        # corpus information
        if args.info or no_action:
            corpus.print_info()

    except CorpusException as e:
        print 'Error during building corpus:\n ', e.message


# ---------------------------------------------------------------------------
#  helper functions
# ---------------------------------------------------------------------------

def list_all_corpora():
    try:
        # uncompiled corpora
        print 'All uncompiled corpora:'
        # use tree command to list all corpora with their files including sizes
        # NOTE: content size (--du) printing needs tree>=1.6 but there is
        #       only 1.5 version on Aurora server installed
        call(['tree', environment.verticals_path(),
              #'-h',           # with human readable sizes
              #'--du',         # for directories display content size
              '--noreport'])  # without summary about number of files/dirs

        # compile corpora
        print '\nAll compiled corpora:'
        call(['tree', environment.compiled_corpora_path(),
              #'-h',           # human readable sizes
              '-d',           # directories only
              #'--du',         # for directories display content size
              '--noreport'])  # without summary about number of files/dirs
    except OSError:
        print "You need to have 'tree' installed"\
            + " for listing corpora."


# ---------------------------------------------------------------------------
#  running module -> call main() function
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()
