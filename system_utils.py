#!/usr/bin/env python
# encoding: utf-8

""" Module for utilities providing system services
"""

import os


def choose_path(lang, extension, description=''):
    """ Returns appropriate path for given corpus file parameters
    """
    # TODO: directory (absolute path)
    corpus_name = 'wiki-{lang}'.format(lang=lang)
    dir_path = 'vert/{corpus_name}/'.format(corpus_name=corpus_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if description:
        file_name = '{corpus_name}_{description}.{extension}'.format(
            corpus_name=corpus_name,
            description=description,
            extension=extension)
    else:
        file_name = '{corpus_name}.{extension}'.format(
            corpus_name=corpus_name,
            extension=extension)
    path = '{dir_path}{name}'.format(dir_path=dir_path, name=file_name)
    return path
