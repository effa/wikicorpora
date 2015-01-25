#!/usr/bin/python
# encoding=utf-8

"""Unit tests for verticaldocument.py module
"""

from __future__ import unicode_literals
from wikicorpus.verticaldocument import VerticalDocument
from registry.tagsets import get_tagset_by_name
import os
import unittest
import yaml

# absolute path to this file
BASE = os.path.abspath(os.path.dirname(__file__))


class TestVerticalDocument(unittest.TestCase):

    """Class of unit tests for verticaldocument.py module"""

    # test samples files
    POSTPROCESSING_SAMPLES_FILE = os.path.join(BASE,
        'test-samples-vertical-postprocessing.yaml')
    INFERENCE_SAMPLES_FILE = os.path.join(BASE,
        'test-samples-terms-inference.yaml')

    # Override some of the TestCase attributes:
    # show diffs of arbitrary length
    maxDiff = None
    # show both my message and standard message
    longMessage = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vertical_postprocessing(self):
        """ Tests for vertical postprocessing when creating VerticalDocument
        """
        self._test_samples(TestVerticalDocument.POSTPROCESSING_SAMPLES_FILE)

    def test_terms_inference(self):
        """ Tests for creating VerticalDocument object with terms inference
        """
        self._test_samples(TestVerticalDocument.INFERENCE_SAMPLES_FILE, True)

    def _test_samples(self, samples_file_name, terms_inference=True):
        """ Helper method for testing VerticalDocument using a file of samples
        """
        # load test samples
        with open(samples_file_name) as samples_file:
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
                terms_inference=terms_inference)
            self.assertEqual(result, unicode(vertical_document).strip(),
                msg='failed test case "{label}"'.format(label=label))
