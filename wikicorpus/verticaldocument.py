#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from registry.tagsets import TAGSETS
from termstrie import TermsTrie
import re

# -----------------------------------------------------------------------------
#  regular expressions
# -----------------------------------------------------------------------------

## regex matching a document sgml tag
#DOCUMENT_TAG = re.compile(r"""
#        ^
#        <doc
#        \s+
#        id="(?P<id>.*?)"        # id
#        \s+
#        url="(?P<url>.*?)"      # url
#        \s+
#        title="(?P<title>.*?)"  # title
#        >
#        $
#        """, re.VERBOSE)

# regex matching a term sgml tag
TERM_TAG = re.compile(r"""
        ^
        <term
        \s+
        wuri="(?P<wuri>.*?)"
        >
        $
        """, re.VERBOSE)

## regex matching a paragraph sgml tag
#PARAGRAPH_TAG = re.compile(r"""
#        ^
#        <p
#        \s+
#        (?:heading="(?P<name>.*?)")?  # optional heading flag
#        >
#        $
#        """, re.VERBOSE)

## regex matching a sentence sgml tag
#SENTENCE_TAG = re.compile(r"""
#        ^
#        <s
#        .*  # ignoring attributes for now
#        >
#        $
#        """, re.VERBOSE)


# -----------------------------------------------------------------------------
#  Token class
# -----------------------------------------------------------------------------

class Token(object):

    """Token representation"""

    def __init__(self, line, tagset):
        """
        :line: [unicode] one line (one token) of vertical file
        :tagset: [registry.Tagset] tagset of the vertical
        """
        parts = line.split('\t')
        self._word = parts[0]
        self._lemma = None
        self._tag = None
        self._tagset = tagset
        if tagset == TAGSETS.DESAMB:
            # desamb: 2nd column is lemma, 3rd is tag
            self._lemma = parts[1]
            self._tag = parts[2]
            # for numbers, use actual numbers as the lemma
            if self._lemma.startswith('#num#'):
                self._lemma = self._word + self._lemma[5:]
        elif tagset == TAGSETS.TREETAGGER:
            # treetagger: 2nd column is tag, 3rd is lemma
            self._tag = parts[1]
            self._lemma = parts[2]
            # for numbers, use actual numbers as the lemma
            if self._lemma.startswith('@card@'):
                self._lemma = self._word + self._lemma[6:]

    def get_word(self):
        return self._word

    def get_tag(self, default=None):
        return self._tag if self._tag is not None else default

    def get_lemma(self, word_fallback=True):
        """Returns lemma of the token

        :word_fallback: [Bool] if True and lemma is missing, use word instead
        """
        if self._lemma is None and word_fallback:
            return self._word
        return self._lemma

    def __unicode__(self):
        """Returns unicode representation of the token (as one line)
        """
        if self._tagset == TAGSETS.DESAMB:
            return '{word}\t{lemma}\t{tag}'.format(
                word=self.get_word(),
                lemma=self.get_lemma(),
                tag=self.get_tag())
        elif self._tagset == TAGSETS.TREETAGGER:
            return '{word}\t{tag}\t{lemma}'.format(
                word=self.get_word(),
                tag=self.get_tag(),
                lemma=self.get_lemma())
        else:
            return self.get_word()


# -----------------------------------------------------------------------------
#  VerticalDocument class
# -----------------------------------------------------------------------------

"""
Poznamka o algoritmu k odvozeni vyskytu pojmu:

    Inference vyskytu pojmu je zalozena na longest-matching pomoci trie
    se slozitost O(n), kde n je delka textu. Prochazime cely vstupni text
    a v kazdem bode hledame vyskyt pojmu. Protoze trie umoznuje hledani
    ukoncit, kdyz uz se nejedna o prefix zadneho pojmu, a soucet vsech delek
    vsech vyskytu pojmu v textu je nejvyse rovna delce celeho textu (pokud
    by byl slozen ze samych pojmu), je slozitost vypoctu O(n + 2n) = O(n).

    Alternativa by bylo sestupne hledani v m hashovacich tabulkach pro ruzne
    delky pojmu s horsi asymptotickou casovou slozitosti O(n * m), kde n je
    delka textu a m delka nejdelsiho pojmu (v poctu slov).

    Urcite ale existuji i efektivnejsi zpusoby, takze muze stat za to vyzkouset
    neco dalsiho. Asymptotickeho zrychleni oproti O(n) uz vsak samozrejme
    dosahnout nelze.
"""


class VerticalDocument(object):

    """Class for in-memory representation of one document in vertical format"""

    def __init__(self, lines, tagset, terms_inference=False):
        """
        :lines: [list<unicode>] OR unicode
        :tagset: [registry.Tagset]
        """
        # check :lines: is unicode or list of unicode
        if isinstance(lines, unicode):
            # if it's unicode, slit it to list of lines
            lines = lines.split('\n')
        elif not isinstance(lines, list):
            raise ValueError(':lines: should be unicode or list of unicodes')

        # building representation of vertical (store lines, tranform tokens to
        # Token objects) and trie of all terms in text
        self._tagset = tagset
        self._lines = []
        self._termstrie = TermsTrie()
        reading_term = False
        term_canonical_form = None
        for line in lines:
            line = line.strip()
            # skip empty lines
            if not line:
                continue

            # if it's sgml tag, leave it as a string,
            # but if it's a token, use Token class to represent it
            if is_sgml_tag(line):

                # remove desamb hacks
                if line.startswith('<s hack'):
                    # remove last 3 lines: <g/>, ., </s>
                    del self._lines[-3:]
                    continue

                # ignore sentence tags, if inside <term> (they are incorrect)
                if reading_term and re.search(r'^</?s', line):
                    continue

                self._lines.append(line)

                # try to match a term sgml tag
                match = TERM_TAG.match(line)
                if match:
                    # term reading start
                    term_wuri = match.group('wuri')
                    term_canonical_form = []
                    reading_term = True

                if line == '</term>':
                    # term reading finished
                    self._termstrie.add(term_wuri, term_canonical_form)
                    reading_term = False
            else:
                # use Token class to represent tokens
                token = Token(line, tagset)
                self._lines.append(token)
                # if reading a term, remember the lemma
                if reading_term:
                    term_canonical_form.append(token.get_lemma(True))

        # apply terms inference
        if terms_inference:
            self._terms_occurences_inference()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        # NOTE: some lines are Tokens and some are strings
        return '\n'.join(map(unicode, self._lines)) + '\n'

    def get(self, index):
        """Returns line (Token or sgml tag in unicode) on given index
        """
        return self._lines[index]

    def _longest_matching_term(self, pos):
        """Returns longest matching term and its length from given position

        :returns: (unicode, int) or (None, 0) if no term found
        """
        max_length = 0
        current_length = 0
        longest_term = None
        self._termstrie.search_start()
        while True:
            try:
                line = self.get(pos + current_length)
                if is_sgml_tag(line):
                    # break term search if there is a new paragraph or a term
                    if line == '</p>' or line.startswith('<term '):
                        break
                    else:
                        continue
                lemma = self.get(pos + current_length).get_lemma()
                if not self._termstrie.search_continue(lemma):
                    break
                found_term = self._termstrie.search_result()
                if found_term:
                    longest_term = found_term
                    # TODO: prepsat jasneji
                    max_length = current_length + 1
            finally:
                # go to next line, even if "continue" was called
                current_length += 1
                # check the end of the vertical
                if pos + current_length >= len(self._lines):
                    break
        return (longest_term, max_length)

    def _terms_occurences_inference(self):
        new_lines = []
        new_term_rest_length = 0
        new_term_reading = False
        old_term_reading = False
        for i, line in enumerate(self._lines):
            if is_sgml_tag(line):
                # ignore sentence tags, if inside <term>
                # (becaucse they are probably incorrect)
                if not new_term_reading or not re.search(r'^</?s', line):
                    new_lines.append(line)
                # inside old terms, swith of new term search
                if line.startswith('<term'):
                    old_term_reading = True
                elif line == '</term>':
                    old_term_reading = False
            else:
                if not new_term_reading and not old_term_reading:
                    term_wuri, term_length = self._longest_matching_term(i)
                    if term_length > 0:
                        term_tag = '<term wuri="{name}" uncertainty="1">'\
                            .format(name=term_wuri)
                        new_lines.append(term_tag)
                        new_term_reading = True
                        new_term_rest_length = term_length
                new_lines.append(unicode(line))
                if new_term_reading:
                    new_term_rest_length -= 1
                    if new_term_rest_length == 0:
                        new_lines.append('</term>')
                        new_term_reading = False
        self._lines = new_lines


# -----------------------------------------------------------------------------
#  Vertical File Line - utilities
# -----------------------------------------------------------------------------

def is_sgml_tag(line):
    """Returns True if line is s sgml tag, False otherwise

    :line: unicode || Token
    """
    # TODO: a co kdyz je < ve vstupnim textu???
    if isinstance(line, Token):
        return False
    return line.startswith('<')
