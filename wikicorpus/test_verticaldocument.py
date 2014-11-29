#!/usr/bin/python
# encoding=utf-8

"""Unit tests for verticaldocument.py module
"""

from __future__ import unicode_literals
from verticaldocument import VerticalDocument
from registry import get_tagset_by_name
import unittest
import yaml


class TestVerticalDocument(unittest.TestCase):

    """Class of unit tests for verticaldocument.py module"""

    # test samples files
    INFERENCE_SAMPLES_FILE = './test-samples-terms-inference.yaml'

    # Override some of the TestCase attributes:
    # show diffs of arbitrary length
    maxDiff = None
    # show both my message and standard message
    longMessage = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # TODO: testovani dalsich casti modulu verticaldocument.py
    #  napr. vytvoreni vertikalu bez inference pojmu

    def test_terms_inference(self):
        """ Tests for creating VerticalDocument object with terms inference
        """
        # load test samples
        with open(TestVerticalDocument.INFERENCE_SAMPLES_FILE) as samples_file:
            samples = yaml.load(samples_file)
        for sample in samples:
            # read samples from yaml file, decode to unicode
            # and strip last new line character
            # NOTE: each entry can be either str or unicode, so it's important
            # to call unicode() instead of sample[x].decode('utf-8')
            label, tagset, vert_text, result = (unicode(sample[x]).strip()
                for x in ['label', 'tagset', 'vertical', 'result'])
            tagset = get_tagset_by_name(tagset)
            vertical_document = VerticalDocument(vert_text, tagset,
                terms_inference=True)
            self.assertEqual(result, unicode(vertical_document),
                msg='failed test case "{label}"'.format(label=label))
