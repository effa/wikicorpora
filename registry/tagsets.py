#!/usr/bin/env python
# encoding: utf-8

"""Module for tagsets representation
"""
from collections import namedtuple


# create class for a tagset representation
Tagset = namedtuple('Tagset', ['name', 'doc'])


class TAGSETS:
    """Simple enum class for tagsets
    """
    BASIC = Tagset(
        name='basic',
        doc='TODO....')
    # TODO: zkontrolovat:
    DESAMB = Tagset(
        name='desamb',
        doc='http://nlp.fi.muni.cz/projekty/ajka/tags.pdf')
    TREETAGGER = Tagset(
        name='treetagger',
        doc='https://www.sketchengine.co.uk/documentation/wiki/tagsets/penn')
    # list of all available tagsets
    available_tagsets = [BASIC, DESAMB, TREETAGGER]


def get_tagset_by_name(name):
    """Returns tagset corresponding to given name
    """
    for tagset in TAGSETS.available_tagsets:
        if tagset.name == name:
            return tagset
    else:
        return None
