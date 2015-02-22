#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from utils.language_utils import get_language_name
#from tagsets import get_tagset_by_name
#import errno
import os
#import re

# component root path
BASE = os.path.abspath(os.path.dirname(__file__))

# path to directory with registry templates
TEMPLATE_DIR = os.path.join(BASE, 'registry-templates')

# regular expression for tagset statement in registry file
#TAGSET_RE = re.compile(r'^#tagset=(\w*)')


def store_registry(path, lang, vertical_path, compiled_path):
    """Stores registry to file.

    :path: [unicode] path to registry file
    :lang: [unicode] 2-letter language code
    :vertical_path: [unicode] path to vertical file
    :compiled_path: [unicode] path to directory with compiled corpus
    :tagset: [Tagset] which tagset is used in corpus
    """
    language = get_language_name(lang, capitalized=False)
    # NOTE: each language has its own template
    registry_string = render_registry_template('wiki_' + language,
        #language=get_language_name(lang),
        #iso=lang,
        compiled_corpus_path=compiled_path,
        vertical_path=vertical_path)

    ## attributes
    #template_file = 'attributes-{name}'.format(name=tagset.name)
    #attributes_configuration = render_registry_template(template_file)

    ## complete registry file
    #registry_string = render_registry_template('registry-main',
    #    language=get_language_name(lang),
    #    iso=lang,
    #    compiled_corpus_path=compiled_path,
    #    vertical_path=vertical_path,
    #    tagsetdoc=tagset.doc,  # TODO: co kdyz prazdny
    #    attributes=attributes_configuration)

    # store registry string
    with open(path, 'w') as registry_file:
        registry_file.write(registry_string)


#def get_registry_tagset(path):
#    """Retuns tagset as stated in registry file on given path

#    :throws: RegistryException if registry not found
#    """
#    try:
#        with open(path) as registry_file:
#            registry_lines = registry_file.readlines()
#    except IOError as exc:
#        if exc.errno == errno.ENOENT:
#            raise RegistryException('Registry file not found.')
#        else:
#            raise RegistryException('IOError on attempt to read registry.')

#    for line in registry_lines:
#        match = TAGSET_RE.search(line)
#        if match:
#            tagset_name = match.group(1)
#            tagset = get_tagset_by_name(tagset_name)
#            if tagset:
#                return tagset
#            else:
#                raise RegistryException('Uknown tagset: ' + tagset_name)
#    raise RegistryException('Tagset statement not found.'
#        + ' Add "# tagset=<basic|desamb|treetagger>" to registry.')


# -----------------------------------------------------------------------------
#  utilities
# -----------------------------------------------------------------------------

def render_registry_template(template_file_name, **kwargs):
    """Renders registry template.
    """
    with open(os.path.join(TEMPLATE_DIR, template_file_name)) as f:
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
