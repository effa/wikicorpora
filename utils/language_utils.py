#!/usr/bin/env python
# encoding: utf-8

"""Module for working with language names and iso codes.
"""

import json
import os

# component root path
BASE = os.path.abspath(os.path.dirname(__file__))

# path to JSON file with languages
LANGUAGES_FILE = os.path.join(BASE, 'languages.json')

# loads dictionary of languages
with open(LANGUAGES_FILE) as languages_file:
    LANGUAGES = json.load(languages_file)


def get_language_name(iso, capitalized=True):
    """Returns full name of language given by two-letter iso code

    @param iso: [unicode] two-letter iso code (ISO_639-1)
    @param capitalized: [bool] if True, returns capitalized name
                        (e.g. "Norwegian Nynorsk"), otherwise in lower letters

    @returns [unicode]

    @throws: ValueError when :iso: is not a valid iso code
    """
    if iso not in LANGUAGES:
        raise ValueError('%s is not a valid 2-letter language code' % iso)
    name = LANGUAGES[iso]
    if capitalized:
        name = name.title()
    else:
        name = name.lower()
    return name
