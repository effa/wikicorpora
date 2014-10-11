#!/usr/bin/env python
# encoding: utf-8


def download_dump(lang, path=None):
    """ Downloads wikipedia dump for given language
    """
    raise NotImplementedError


def create_sample_dump(lang, size=10, dump_path=None, sample_dump_path=None):
    """ Creates smaller sample dump from large dump of given language

    (taking first N articles...)
    """
    raise NotImplementedError


def dump_to_prevertical(lang, dump_path=None, prevertical_path=None):
    """ Parses dump (outer XML and inner Wiki Markup) and creates prevertical
    """
    raise NotImplementedError


def tokenize_prevertical(lang, prevertical_path=None, vertical_path=None):
    """ Tokenizes given prevertical
    """
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
    raise NotImplementedError

if __name__ == '__main__':
    main()
