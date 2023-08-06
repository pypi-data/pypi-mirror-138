#!/usr/bin/env python3

"""
** Lists the locations of the files. **
---------------------------------------

- DIR_PATH : the location of the main directory
- CONFIG_PATH : the configuration file
"""

import os

DIR_PATH = os.path.join(os.path.expanduser('~'), '.raisin')
CONFIG_PATH = os.path.join(DIR_PATH , 'raisin.conf')
