#!/usr/bin/python
# encoding=utf-8

"""Unit tests for wikimarkup.py module
"""

# NOTE: wikimarkup module is deprecated

#from __future__ import unicode_literals
#from wikimarkup import term2wuri, parse_wikimarkup
#import unittest
#import yaml


#class TestWikiCorpora(unittest.TestCase):

#    """Class of unit tests for wikimarkup.py module"""

#    TEST_SAMPLES_FILE = './test-samples-wikimarkup.yaml'

#    def setUp(self):
#        pass

#    def tearDown(self):
#        pass

#    def test_term2wuri(self):
#        """ Tests for term2wuri function
#        """
#        self.assertEqual('Duke', term2wuri('duke'))
#        self.assertEqual('Channel_Islands', term2wuri('Channel Islands'))
#        self.assertEqual('Early_old_period', term2wuri('early old period'))

#    def test_parse_wikimarkup(self):
#        """ Tests for parse_wikimarkup function
#        """
#        with open(TestWikiCorpora.TEST_SAMPLES_FILE) as samples_file:
#            samples = yaml.load(samples_file)
#        for sample in samples:
#            # read samples from yaml file, decode to unicode
#            # and strip alst new line character
#            text, title, result = (sample[x].decode('utf-8').strip()
#                for x in ['text', 'title', 'result'])
#            prevertical = parse_wikimarkup(text, title)
#            self.assertEqual(result, prevertical)
