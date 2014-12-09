#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from collections import namedtuple
from language_utils import get_language_name
import re

# TODO: absolutni cesty!!!!!!!!!
TEMPLATE_DIR = 'registry-templates/'

# regular expression for tagset statement in registry file
TAGSET_RE = re.compile(r'^#tagset=(\w*)')

#class Registry(object):

#    """Class representing a corpus registry file."""

#    def __init__(self, path, lang, vertical_path, compiled_path,
#            tagset, structures):
#        """
#        :path: [unicode] path to registry file
#        :lang: [unicode] 2-letter language code
#        :vertical_path: [unicode] path to vertical file
#        :compiled_path: [unicode] path to directory with compiled corpus
#        :tagset: [Tagset] which tagset is used in corpus
#        :structures: [set of unicodes] which structures are used in corpus
#        """
#        self._path = path
#        self._lang = lang
#        self._vertical_path = vertical_path
#        self._compiled_path = compiled_path
#        self._tagset = tagset
#        self._structures = structures


def store_registry(path, lang, vertical_path, compiled_path,
        tagset, structures):
    """Stores registry to file.

    :path: [unicode] path to registry file
    :lang: [unicode] 2-letter language code
    :vertical_path: [unicode] path to vertical file
    :compiled_path: [unicode] path to directory with compiled corpus
    :tagset: [Tagset] which tagset is used in corpus
    :structures: [set of unicodes] which structures are used in corpus
    """
    # structures
    structures_configuration = []
    for structure_name in structures:
        template_file = 'structure-{name}'.format(name=structure_name)
        config_str = render_registry_template(template_file)
        structures_configuration.append(config_str)
    structures_configuration = '\n'.join(structures_configuration)
    # attributes
    template_file = 'attributes-{name}'.format(name=tagset.name)
    attributes_configuration = render_registry_template(template_file)
    # complete registry file
    registry_string = render_registry_template('registry-main',
        language=get_language_name(lang),
        iso=lang,
        compiled_corpus_path=compiled_path,
        vertical_path=vertical_path,
        tagsetdoc=tagset.doc,  # TODO: co kdyz prazdny
        attributes=attributes_configuration,
        structures=structures_configuration)
    # store registry string
    with open(path, 'w') as registry_file:
        registry_file.write(registry_string)


def get_registry_tagset(path):
    """Retuns tagset as stated in registry file on given path

    :throws: RegistryException if registry not found
    """
    with open(path) as registry_file:
        registry_lines = registry_file.readlines()
    for line in registry_lines:
        match = TAGSET_RE.search(line)
        if match:
            tagset_name = match.group(1)
            tagset = get_tagset_by_name(tagset_name)
            if tagset:
                return tagset
            else:
                raise RegistryException('Uknown tagset: ' + tagset_name)
    raise RegistryException('Tagset statement not found.'
        + ' Add "# tagset=<basic|desamb|treetagger>" to registry.')

# -----------------------------------------------------------------------------
#  tagsets representation
# -----------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
#  Exceptions
# ---------------------------------------------------------------------------

class RegistryException(Exception):
    """ Registry file parsing error
    """
    pass
