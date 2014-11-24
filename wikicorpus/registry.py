#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from language_utils import get_language_name

# TODO: absolutni cesty!!!!!!!!!
TEMPLATE_DIR = 'registry-templates/'


class Registry(object):

    """Class representing a corpus registry file."""

    def __init__(self, path, lang, vertical_path, compiled_path,
            tagset, structures):
        """
        :path: [unicode] path to registry file
        :lang: [unicode] 2-letter language code
        :vertical_path: [unicode] path to vertical file
        :compiled_path: [unicode] path to directory with compiled corpus
        :tagset: [Tagset] which tagset is used in corpus
        :structures: [set of unicodes] which structures are used in corpus
        """
        self._path = path
        self._lang = lang
        self._vertical_path = vertical_path
        self._compiled_path = compiled_path
        self._tagset = tagset
        self._structures = structures

    def store(self):
        """Writes registry to file.
        """
        # TODO: working with templates :)
        print render_registry_template('registry-main',
            language=get_language_name(self._lang),
            iso=self._lang,
            compiled_corpus_path=self._compiled_path,
            vertical_path=self._vertical_path,
            tagsetdoc='TODO',
            attributes='TODO',
            structures='TODO')
        # TODO.....


# TODO:
#class RegistryReader(object):


class Tagset:
    """Simple enum class for tagsets
    """
    BASIC = ''
    # TODO: zkontrolovat:
    DESAMB = 'http://nlp.fi.muni.cz/projekty/ajka/tags.pdf'
    TREETAGGER = \
        'https://www.sketchengine.co.uk/documentation/wiki/tagsets/penn'


# -----------------------------------------------------------------------------
#  utilities
# -----------------------------------------------------------------------------

def render_registry_template(template_file_name, **kwargs):
    """Renders registry template.
    """
    with open(TEMPLATE_DIR + template_file_name) as f:
        template = f.read().decode('utf-8')
    # NOTE: if more tricks needed, use jinja2
    return template.format(**kwargs)
