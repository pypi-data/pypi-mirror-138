#!/usr/bin/env python3

"""
** Interacts with the configuration file. **
--------------------------------------------

The configuration file is located in *~/.raisin/raisin.conf*.
It contains various information which is parsed here.
"""

import logging
import os
import sys

from raisin.application.port import get_port, set_port
from raisin.application.verbosity import get_verbosity, set_verbosity
from raisin.application.location import CONFIG_PATH


__pdoc__ = {
    'ConfigFile.__getitem__': True,
    'ConfigFile.__setitem__': True,
    'ConfigFile.__iter__': True,
}


class ConfigFile:
    """
    ** Allows you to manipulate the configuration file. **
    """
    def __init__(self):
        self._show_warning = True

    def get_file_content(self):
        """
        ** Reads the configuration file. **

        If the file does not exist, issues a warning urging the user to follow the steps.

        Returns
        -------
        file_content : str
            The raw content without formatting of the configuration file.
        """
        if not os.path.exists(CONFIG_PATH):
            if self._show_warning:
                message = (
                    f'impossible to find the configuration file {CONFIG_PATH}, '
                    "to create this file please end the installation of 'raisin' by typing "
                    f"'{sys.executable} -m raisin install --config_only'"
                )
                logging.warning(message)
            self._show_warning = False
            return None
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def set_file_content(file_content):
        """
        ** Write for real the new configuration file. **

        Parameters
        ----------
        file_content : str
            The entire content of the new file. The old content, if it exists,
            will be overwritten to be replaced by this one.
        """
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(
                "impossible to save the configuration file as long as 'raisin' is not installed, "
                f"to remedy this please run '{sys.executable} -m raisin install --config_only'"
            )
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            file.write(file_content)

    def __getitem__(self, item):
        """
        ** Allows you to retrieve values from the configuration file. **

        Parameters
        ----------
        item : str
            The name of the parameter to retrieve.

        Returns
        -------
        parameter_value
            The value of the parameter.

        Examples
        --------
        >>> from raisin.application import config_file
        >>> config_file['verbosity']
        0
        >>>
        """
        func_get = {
            'port': get_port,
            'verbosity': get_verbosity,
        }.get(item)
        if func_get is None:
            raise KeyError(f'there are no elements corresponding to {item}')
        return func_get(self.get_file_content())

    def __setitem__(self, item, value):
        """
        ** Allows you to simply modify certain values in the configuration file. **

        Parameters
        ----------
        item : str
            The name of the parameter to be modified.
        value
            The new value of the parameter.
            If 'None', the default value is used.

        Examples
        --------
        >>> from raisin.application import config_file
        >>> for param in config_file:
        ...     value = config_file[param]
        ...     config_file[param] = value
        ...
        >>>
        """
        func_set = {
            'port': set_port,
            'verbosity': set_verbosity,
        }.get(item)
        if item is None:
            raise KeyError(f'there are no elements corresponding to {item}')
        if value is not None:
            self.set_file_content(func_set(value, file_content=self.get_file_content()))
        else:
            self.set_file_content(func_set(file_content=self.get_file_content()))

    @staticmethod
    def __iter__():
        """
        ** Iterated on the name of the parameters. **

        This makes it possible to give a behavior similar to that of the dictionaries.

        Examples
        --------
        >>> from raisin.application import config_file
        >>> list(config_file)
        ['port', 'verbosity']
        >>>
        """
        yield 'port'
        yield 'verbosity'
