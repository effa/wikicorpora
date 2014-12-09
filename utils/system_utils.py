#!/usr/bin/env python
# encoding: utf-8

""" Module for utilities providing system services
"""

import errno
import os


def makedirs(path):
    """Creates missing directories on :path:

    :path: unicode
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            # path already exists
            pass
        else:
            # some other error occured
            raise
