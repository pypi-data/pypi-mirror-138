#!/usr/bin/env python3

r"""
** Raisin: To perform cluster work easily! **
---------------------------------------------

The main aim of project *raisin*  is to **share physical resources**
of your laptop with a community.
In counterpart, you can  **benefit from the community resources** .

For more information on the philosophy of the project,
see https://framagit.org/robinechuca/raisin/-/blob/master/README.rst .

Global vision
-------------

Organization of the files:

.. figure:: http://raisin-docs.ddns.net/packages.png

Class diagram:

.. figure:: http://raisin-docs.ddns.net/classes.png

Examples
--------

In a separate process, run the command ``python -m raisin server``.

>>> import raisin
>>> def f(x): return x**2
...
>>> for res in raisin.imap_unordered(f, range(3)): # doctest: +SKIP
...     res
...
0
1
4
>>>
"""

# * To generate the documentation, you have to install the package *pdoc3* with *pip* for example.
# * To run the test benches, you have to install the package *pytest* with *pip* for example.
#     Then you have to type the following command:
#     * ``clear && pytest --doctest-modules raisin/
#         && find raisin/ -regex '.*test.*\.py' -exec pytest {} \;``
# * Docstrings respect the following convention:
#     * ``https://numpydoc.readthedocs.io/en/latest/format.html``
# * For text formatting:
#     * ``black -C -S -l 100 raisin``

import inspect

from context_verbose import printer as ctp

from raisin.raisin import imap_unordered
from raisin.application import config_file, install_app as install, uninstall_app as uninstall
from raisin.serialization import deserialize, dump, dumps, load, loads, serialize
from raisin.communication import Client, Server
from raisin.doc import make_pdoc

ctp.set_max_depth(config_file['verbosity'])

__version__ = '3.0.4'
__author__ = 'Robin RICHARD (robinechuca) <raisin@ecomail.fr>'
__license__ = 'GNU Affero General Public License v3 or later (AGPLv3+)'
__all__ = [
    'imap_unordered',
    'deserialize', 'dump', 'dumps', 'load', 'loads', 'serialize',
    'Client', 'Server',
    'config_file', 'install', 'uninstall'
]
__pdoc__ = make_pdoc(__all__, locals())
__pdoc__['raisin.__main__'] = True
