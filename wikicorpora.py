#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from environment import environment
from subprocess import call
from wikicorpus.samplewikicorpus import SampleWikiCorpus
from wikicorpus.wikicorpus import WikiCorpus, CorpusException
import argparse

"""
This is a main file for wikicorpora command line application.
It parses arguments and performes selected actions.
"""

TOOL_DESCRIPTION = 'WikiCorpora is a tool for building corpora from Wikipedia.'


def main():
    """ Main function handling calling this script with arguments
    """
    parser = argparse.ArgumentParser()  # description=(TOOL_DESCRIPTION))

    # corpus specification arguments
    #language_group = parser.add_argument_group('corpus language')
    #language_group.add_argument('-l', '--language', metavar='L',
    #    help='2-letter code of language (ISO-639-1)')
    specification_group = parser.add_argument_group('corpus specification')
    specification_group.add_argument('language', nargs='?',
        help='2-letter code of language (ISO-639-1)')
    specification_group.add_argument('size', nargs='?',
        help='sample size specification')

    # sample options
    sample_group = parser.add_argument_group('sampling tasks')
    #sample_group.add_argument('-s', '--size', type=int,
    #    help='sample size specification', metavar='N')
    specific_or_not_group = sample_group.add_mutually_exclusive_group()
    specific_or_not_group.add_argument('--create-sample',
        action='store_true',
        help='create sample from first N articles')
    specific_or_not_group.add_argument('--create-own-sample',
        action='store_true',
        help='create sample from selected articles')

    # download options
    download_group = parser.add_argument_group('downloading tasks')
    soft_or_force_group = download_group.add_mutually_exclusive_group()
    soft_or_force_group.add_argument('--soft-download', action='store_true',
        help='download dump if not already downloaded')
    soft_or_force_group.add_argument('--force-download', action='store_true',
        help='download dump (even if a dump already exists)')

    # options concerning phases
    phases_group = parser.add_argument_group('corpus processing tasks')
    phases_group.add_argument('--prevertical', '-p', action='store_true',
        help='process dump to prevertical')
    phases_group.add_argument('--vertical', '-v', action='store_true',
        help='process prevertical to vertical')
    phases_group.add_argument('--terms-inference', '-t', action='store_true',
        help='infere all terms occurences')
    phases_group.add_argument('--all-processing-tasks', '-a',
        action='store_true',
        help='execute all corpus processing steps')

    # compilaton options
    compilation_group = parser.add_argument_group('compilation tasks')
    compilation_group.add_argument('--compile', '-c', action='store_true',
        help='create configuration file and compile corpus')
    compilation_group.add_argument('--check', action='store_true',
        help='print compiled corpus status generated by corpcheck')
    compilation_group.add_argument('--query',
        help='print concordances of a given CQL query')

    # general options
    #parser.add_argument('--logfile',
    #    help='path to logfile')
    parser.add_argument('--usage', action='store_true',
        help='show program usage')
    parser.add_argument('--info', action='store_true',
        help='print corpus summary')

    # set own usage descriptin
    parser.usage = 'wikicorpora.py [language] [size] [TASKS]'

    args = parser.parse_args()

    # if no action is specified, we will print corpus info
    no_action = not any([args.force_download, args.soft_download,
        args.create_sample, args.create_own_sample,
        args.prevertical, args.vertical,
        args.terms_inference, args.all_processing_tasks,
        args.compile, args.check, args.query])

    # sample_size has to be either int or None
    sample_size = int(args.size) if args.size else None

    try:
        # no language specified (can be either mistake or command for info
        # about all corpora or a call without any parameters)
        if not args.language:
            # if size or an action is specified, then a language is
            # probably ommited by mistake
            if args.size or not no_action:
                # print error message and command usage
                print 'No language specified (-l XX or --language=XX).'
                parser.print_usage()
            # if it's a call with --info option, show all corpora
            elif args.info:
                list_all_corpora()
            # if it's a call with --usage option, show usage
            elif args.usage:
                parser.print_usage()
            # otherwise it's empty call -> show short help and usage
            else:
                print TOOL_DESCRIPTION
                parser.print_usage()
                print 'For usage description use "wikicorpora.py --help".'
            return

        # own sample
        if args.create_own_sample:
            # ask for titles
            size = 0
            titles = []
            if sample_size:
                print 'Input {n} titles for new sample.'\
                    .format(n=args.size)
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

        # extract dump (only force if download is forced as well)
        #if args.extract
        #    corpus.extract_dump(force=args.force_download)

        # sampling
        if args.create_own_sample:
            corpus.create_sample_dump(titles)
        elif args.create_sample:
            if not sample_size:
                raise CorpusException('Sample size (--sample-size=X) has to '
                    + ' be specified in order to create sample')
            corpus.create_sample_dump()

        # parsing dump (preverticalization)
        if args.prevertical or args.all_processing_tasks:
            corpus.create_prevertical()

        # tokonenization and tagging (verticalization)
        if args.vertical or args.all_processing_tasks:
            corpus.create_vertical()

        # terms occurences inference
        if args.terms_inference or args.all_processing_tasks:
            corpus.infere_terms_occurences()

        # corpus compilation
        if args.compile:
            corpus.compile_corpus()

        # corpus compilation
        if args.check:
            corpus.check_corpus()

        # execute query
        if args.query:
            corpus.print_concordances(args.query)

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

        # registry files
        print '\nAll registry files:'
        call(['tree', environment.registry_path(),
              '--noreport'])  # without summary about number of files/dirs

        # compiled corpora
        print '\nAll compiled corpora:'
        call(['tree', environment.compiled_corpora_path(),
              '-L', '1',        # one level only (do not descend)
              '-d',             # directories only
              '--noreport'])    # without summary about number of files/dirs
    except OSError:
        print "You need to have 'tree' installed"\
            + " for listing corpora."


# ---------------------------------------------------------------------------
#  running module -> call main() function
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()
