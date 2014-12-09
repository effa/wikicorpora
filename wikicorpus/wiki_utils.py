#!/usr/bin/env python
# encoding: utf-8

"""Module for utilities concerning Wikipedia
"""

from __future__ import unicode_literals
import re


def create_article_url(prefix, title):
    """Creates url from prefix and title of the article
    """
    title = term2wuri(title)
    return "%s/%s" % (prefix, title)


def term2wuri(term):
    """Creates last part of wikipedia URI ("wuri") from a term

    Examples:
        'duke' -> 'Duke'
        'Channel Islands' -> 'Channel_Islands'
        'early modern period' -> 'Early_modern_period'
    Args:
        term (unicode)
            any word, name, phrase
    Returns:
        unicode
    """
    # TODO: handle namespaces (see wikiextractor.normalizedTitle())

    # strip leading whitespace and underscores
    # and replace spaces with underscores
    wuri = term.strip(' _').replace(' ', '_')

    # replace sequences of underscores with a single underscore
    wuri = re.compile(r'_+').sub('_', wuri)

    # ideally term shouldn't be empty, but it's Wikipedia
    if len(wuri) > 0:
        # first letter always capital
        wuri = wuri[0].upper() + wuri[1:]

    return wuri
