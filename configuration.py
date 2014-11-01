#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import yaml


class Configuration(object):

    """Class for reprezentation of configuration"""

    def __init__(self, path):
        """Loads configuration.

        :path: unicode
            path to configuration file in YAML format

        :returns:
            dictionary with configuration

        :throws:
            ConfigurationException if configuration file doesn't exist
        """
        try:
            with open(path) as config_file:
                self._configuration_dict = yaml.load(config_file)
        except IOError:
            raise ConfigurationException('loading configuration failed')

    def get(self, *args):
        """Returns information from configration.

        :*args: key (or series of keys in case of nesting)
        """
        conf = self._configuration_dict
        try:
            for key in args:
                conf = conf[key]
            return conf
        except KeyError:
            raise ConfigurationException('wrong configuration key')

    def get_nonempty(self, *args):
        """Returns nonempty information from configuration

        :*args: key (or sequence of keys in case of nesting)

        :throws: ConfigurationExcpetion if key is not in configuration or
            if the item is empty
        """
        item = self.get(*args)
        if item is None or item == '':
            raise ConfigurationException(
                'empty configuration item for key {key}'.format(
                    key='/'.join(args)))
        return item


# ------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------

class ConfigurationException(Exception):
    """ Class for exceptions concerning configuration.
    """
    pass
