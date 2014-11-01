#!/usr/bin/env python
# encoding: utf-8

"""Module for represenation of local-default configuration pair"""

from __future__ import unicode_literals
from configuration import Configuration, ConfigurationException


class DoubleConfiguration(object):

    """Class for retrieving environment configuration"""

    def __init__(self, path_local, path_default):
        """Initialization (loading both configurations)

        :path_local: unicode
            path to local configuration file
        :path_default: unicode
            path to default (fallback) configuration file
        # load configuration
        """
        self._local_configuration = Configuration(path_local)
        self._default_configuration = Configuration(path_default)

    def get(self, *args):
        """ Returns information from configration.

        :*args: key (or series of keys in case of nesting)
        """
        try:
            # first, try to find the information in local configuration file
            return self._local_configuration.get(*args)
        except ConfigurationException:
            # as a fallback, use default configuration file
            return self._default_configuration.get(*args)

    def get_nonempty(self, *args):
        """ Returns information from configration.

        :*args: key (or series of keys in case of nesting)
        """
        try:
            # first, try to find the information in local configuration file
            item = self._local_configuration.get(*args)
        except ConfigurationException:
            # as a fallback, use default configuration file
            item = self._default_configuration.get(*args)
        if item is None or item == '':
            raise ConfigurationException(
                'empty configuration item for key {key}'.format(
                    key='/'.join(args)))
        return item
