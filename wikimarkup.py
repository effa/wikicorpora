#!/usr/bin/env python
# encoding: utf-8

"""Module for WikiMarkup parsing
"""

from __future__ import unicode_literals
import mwparserfromhell as parser

# TODO: zkusit jiny parser, problem soucasneho: [[step]]s

# -----------------------------------------------------------------------------
#  public module functions
# -----------------------------------------------------------------------------


def parse_wikimarkup(wikitext, title=None):
    """
    Converts WikiMarkup to prevertical format

    Args:
        wikitext (unicode):
            text in WikiMarkup
        title (unicode) [optional]:
            title of the article
    Returns:
        unicode
    """
    assert type(wikitext) == unicode

    # parse wikitext
    parsed_wikitext = parser.parse(wikitext)

    # create prevertical-xml list
    if title:
        article_wuri = term2wuri(title)
        prevertical = ['<doc wuri="{wuri}">'.format(wuri=article_wuri)]
    else:
        prevertical = ['<doc>']
    open_sections = []
    for node in parsed_wikitext.get_sections(flat=True, include_lead=True):
        headings = node.filter_headings()
        heading = headings[0] if len(headings) == 1 else None
        if heading:
            title = heading.title.strip()
            level = heading.level
            # close previous section (and subsections)
            while len(open_sections) > 0 and open_sections[-1] >= level:
                open_sections.pop()
                prevertical.append('</section>')
            prevertical.append('<section title="{title}">'.format(title=title))
            open_sections.append(level)
        processed_section = _process_section(node)
        prevertical.extend(processed_section)

    # close all sections and the document
    for i in range(len(open_sections)):
        prevertical.append('</section>')
    prevertical.append('</doc>')

    # join result in one string
    return '\n'.join(prevertical)


def term2wuri(term):
    """ Creates last part of wikipedia URI ("wuri") from a term

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
    wuri = term.strip().replace(' ', '_')
    wuri = wuri[0].upper() + wuri[1:]  # first letter always capital
    return wuri


# -----------------------------------------------------------------------------
#  private helper functions
# -----------------------------------------------------------------------------

def _process_section(section):
    """
    Converts wiki section (without a headline) to the vertical format

    Args:
        section: mwparserfromhell.wikicode
            wikicode node representing one section (paragraph)
    Returns:
        list of unicodes
    """
    parts = []
    for node in section.ifilter(recursive=False):
        # plain text
        if isinstance(node, parser.nodes.text.Text):
            parts.append(node.value.strip())
        # wikilinks
        elif isinstance(node, parser.nodes.wikilink.Wikilink):
            text = node.text or node.title
            wuri = term2wuri(node.title)
            parts.append('<term wuri="{wuri}">'.format(wuri=wuri))
            parts.append(text.strip())
            parts.append('</term>')
        # tags
        elif isinstance(node, parser.nodes.tag.Tag):
            # parse content of style tags (''' (strong) and '' (italics))
            if node.wiki_markup in {"'''", "''"}:
                # recursive content parsing
                parts.extend(_process_section(node.contents))
    #return '\n'.join(parts)
    return parts
