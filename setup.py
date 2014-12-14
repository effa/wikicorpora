#!/usr/bin/env python
# encoding: utf-8

"""Module for easier and transparent handling of absolute paths
    ?(and also imports from another component during testing)?
    ?(and later possibly for application installing)?
"""

import sys
import os

# absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def load_project_root():
    """Adds project root to PYTHONPATH
    """
    sys.path.insert(0, PROJECT_ROOT)


def project_path(path):
    """Returns absolute path of :path: which is relative to project root

    @param path: relative path to a file (relative from project root)
    @return: absolute path of the file
    """
    return os.path.join(PROJECT_ROOT, path)
