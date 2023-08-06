#!/usr/bin/env python3

"""
** Allows to manage the installation of 'raisin'. **
----------------------------------------------------

To work properly, 'grape' needs to install small things.
Installing 'grape' allows to make a server start at startup without any need to do anything.
But the installation also allows to make persistent configuration settings.
"""

import os

from context_verbose import printer as ctp

from raisin.application.location import DIR_PATH, CONFIG_PATH


def _make_raisin_dir():
    """
    ** Create if it does not exist, the folder '~/.raisin'. **
    """
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
        ctp.print(f'the {DIR_PATH} directory has just been created')

def install_config_file():
    """
    ** Create a configuration file with default values. **

    The created file is located in '~/.raisin/raisin.conf'.
    Symmetric function of ``raisin.application.uninstall.uninstall_config_file``.

    If the file already exists, it is not modified.
    """
    from raisin.application import config_file
    with ctp('Creation of the configuration file...'):
        _make_raisin_dir()
        if os.path.exists(CONFIG_PATH):
            ctp.print('the configuration file already exists, it is not modified')
            return None
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            file.write(
                '# RAISIN CONFIGURATION FILE\n'
                '\n'
                '# Allows to set the default behavior. '
                    'The parameters are reloaded directly from the file as soon as '
                    'they are needed, so they are taken into account immediately.\n'
                '\n'
                '# This file allows a great flexibility because the parameters are recovered '
                    'by the analysis of the formatted file by regular expressions.\n'
                "# All the characters of a line which follow the character '#' are ignored.\n"
                '# The case does not matter.\n'
                '\n'
                )
        for param in config_file:
            with open(CONFIG_PATH, 'a', encoding='utf-8') as file:
                file.write('\n')
            config_file[param] = None
        ctp.print(f'the {CONFIG_PATH} file has just been created')

def install_app(*, config_only=False):
    """
    ** Entry point to install everything. **

    Parameters
    ----------
    config_only : boolean, default=False
        If True, call only the ``install_config_file`` function.
    """
    with ctp('Application installation...'):
        if config_only:
            ctp.print('installs only the configuration file')
            install_config_file()
        else:
            ctp.print('installs all')
            install_config_file()
