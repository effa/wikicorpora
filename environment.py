#!/usr/bin/env python
# encoding: utf-8

"""Module for reading local environment configuration."""

from __future__ import unicode_literals
from doubleconfiguration import DoubleConfiguration
import os


# project base directory
PROJECT_BASE = os.path.dirname(__file__)


class EnvironmentConfiguration(DoubleConfiguration):

    # paths to environment configuration files
    ENVIRONMENT_CONFIG_LOCAL = os.path.join(PROJECT_BASE,
        'environment-config.yaml')
    ENVIRONMENT_CONFIG_DEFAULT = os.path.join(PROJECT_BASE,
        'environment-config-default.yaml')

    """Class for retrieving environment configuration"""

    def __init__(self):
        # call superclass init (load local and default config)
        super(EnvironmentConfiguration, self).__init__(
            EnvironmentConfiguration.ENVIRONMENT_CONFIG_LOCAL,
            EnvironmentConfiguration.ENVIRONMENT_CONFIG_DEFAULT)

    def verticals_path(self):
        """Returns path to parent directory for all verticals
        """
        return self.get('paths', 'verticals')

    def compiled_corpora_path(self):
        """Returns path to parent directory for all compiled corpora
        """
        return self.get('paths', 'compiled-corpora')

    def get_unitok_path(self):
        """Returns path to unitok

        Raises:
            ConfigurationException if there si no path for unitok
        """
        return self.get_nonempty('tools', 'unitok')

    def get_desamb_path(self):
        """Returns path to desamb

        Raises:
            ConfigurationException if there si no path for desamb
        """
        return self.get_nonempty('tools', 'desamb')

# create environment singleton
environment = EnvironmentConfiguration()
