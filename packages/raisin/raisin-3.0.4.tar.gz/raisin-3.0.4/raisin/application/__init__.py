#!/usr/bin/env python3

"""
** Allows you to manage the settings and the server. **
-------------------------------------------------------

To work, there must be a server listening continuously.
This module allows to manage that.
"""

import inspect

from raisin.application.install import install_app
from raisin.application.uninstall import uninstall_app
from raisin.application.configuration import ConfigFile
from raisin.doc import make_pdoc


config_file = ConfigFile()

__all__ = ['config_file', 'install_app', 'uninstall_app']
__pdoc__ = make_pdoc(__all__, locals())
