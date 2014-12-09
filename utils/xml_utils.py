#!/usr/bin/env python
# encoding: utf-8

"""Module for utilities concerning XML
"""

from __future__ import unicode_literals


def qualified_name(name, namespace):
    """Creates qualified element name for lxml library: '{namespace}name'

    :name: unicode
    :namespace: unicode

    :returns: unicode
    """
    return '{{{namespace}}}{name}'.format(namespace=namespace, name=name)
