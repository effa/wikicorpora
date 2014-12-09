#!/usr/bin/python
# encoding=utf-8

"""Unit tests for wikiextractor.py module
"""

from __future__ import unicode_literals
from wikicorpus.wikiextractor import parse_wikimarkup
import os
import unittest
import yaml

# absolute path to this file
BASE = os.path.abspath(os.path.dirname(__file__))


class TestWikiCorpora(unittest.TestCase):

    """Class of unit tests for wikiextractor.py module"""

    TEST_SAMPLES_FILE = os.path.join(BASE, 'test-samples-wikimarkup.yaml')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_wikimarkup(self):
        """ Tests for parse_wikimarkup function
        """
        with open(TestWikiCorpora.TEST_SAMPLES_FILE) as samples_file:
            samples = yaml.load(samples_file)
        # show diffs of arbitrary length
        self.maxDiff = None
        for sample in samples:
            # read samples from yaml file, decode to unicode
            # and strip last new line character
            id_number = sample['id']
            title, url_prefix, text, result = \
                (unicode(sample[x]).strip()
                    for x in ['title', 'url_prefix', 'text', 'result'])
            # NOTE: each entry can be either str or unicode, so it's important
            # to call unicode() instead of sample[x].decode('utf-8')
            prevertical = parse_wikimarkup(id_number, title, url_prefix, text)
            self.assertEqual(result, prevertical)
