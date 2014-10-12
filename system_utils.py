#!/usr/bin/env python
# encoding: utf-8

""" Module for utilities providing system services
"""

import os


def choose_path(lang, extension):
    """ Returns appropriate path for given corpus file parameters
    """
    # TODO: directory (absolute path)
    corpus_name = 'wiki-{lang}'.format(lang=lang)
    dir_path = 'vert/{corpus_name}/'.format(corpus_name=corpus_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path = '{dir_path}{name}.{ext}'.format(dir_path=dir_path, name=corpus_name,
                                           ext=extension)
    return path
