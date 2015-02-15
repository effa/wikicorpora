#!/usr/bin/env python
# encoding: utf-8

"""Module for reading local environment configuration."""

from __future__ import unicode_literals
from configuration.doubleconfiguration import DoubleConfiguration
from setup import project_path


class EnvironmentConfiguration(DoubleConfiguration):

    # paths to environment configuration files
    ENVIRONMENT_CONFIG_LOCAL = project_path(
        'environment-config.yaml')
    ENVIRONMENT_CONFIG_DEFAULT = project_path(
        'environment-config-default.yaml')

    """Class for retrieving environment configuration"""

    def __init__(self):
        # call superclass init (load local and default config)
        super(EnvironmentConfiguration, self).__init__(
            EnvironmentConfiguration.ENVIRONMENT_CONFIG_LOCAL,
            EnvironmentConfiguration.ENVIRONMENT_CONFIG_DEFAULT)

    def compiled_corpora_path(self):
        """Returns path to parent directory for all compiled corpora
        """
        return self.get('paths', 'compiled-corpora')

    def registry_path(self):
        """Returns path to parent directory for registry (corpora protocols)
        """
        return self.get('paths', 'registry')

    def verticals_path(self):
        """Returns path to parent directory for all verticals
        """
        return self.get('paths', 'verticals')

    #def get_desamb_path(self):
    #    """Returns path to desamb

    #    Raises:
    #        ConfigurationException if there si no path for desamb
    #    """
    #    return self.get_nonempty('tools', 'desamb')

    #def get_treetagger_path(self, language):
    #    """Returns path to a treetagger script

    #    Raises:
    #        ConfigurationException if there si no path for treetagger
    #    """
    #    assert len(language) > 2, 'full language name needed'
    #    # english has a new version of a treetagger script which should be used
    #    if language == 'english':
    #        tt_script = self.get_nonempty('tools', 'treetagger-en')
    #    else:
    #        tt_template = self.get_nonempty('tools', 'treetagger')
    #        tt_script = tt_template.format(lang=language)
    #    return tt_script

    #def get_sentencetagger_path(self):
    #    """Returns path to sentence-tagger script

    #    Raises:
    #        ConfigurationException if there si no path for sentence-tagger
    #    """
    #    return self.get_nonempty('tools', 'sentence-tagger')

    #def get_unitok_path(self):
    #    """Returns path to unitok

    #    Raises:
    #        ConfigurationException if there si no path for unitok
    #    """
    #    return self.get_nonempty('tools', 'unitok')

    def get_logfile_path(self):
        """Returns path to logfile

        Raises:
            ConfigurationException if there si no path for logfile
        """
        return self.get_nonempty('paths', 'logfile')

# create environment instance
environment = EnvironmentConfiguration()
