#!/usr/bin/env python3

"""
** Serialize functions and classes. **

Rely heavily on the *dill* module.
"""

import dill

from raisin.serialization.constants import HEADER


def serialize_function(obj, compact, **_):
    """
    ** Serialize the functions. **
    """
    yield HEADER['function'][compact]
    yield dill.dumps(obj, recurse=True)

def deserialize_function(pack, gen, **_):
    """
    ** Deserialize the functions. **
    """
    return dill.loads(pack + b''.join(gen))
