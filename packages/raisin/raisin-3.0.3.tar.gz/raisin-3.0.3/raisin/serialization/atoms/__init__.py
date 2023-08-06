#!/usr/bin/env python3

"""
** Lists the atomic functions that serialize each case separately. **
---------------------------------------------------------------------

The main serialization function ``raisin.serialization.serialize``,
looks at the nature of the object to serialize.
It applies the appropriate function by picking it up here.
It is also here that the deserialization function
``raisin.serialization.deserialize`` will draw the right function.
"""

import inspect

from raisin.serialization.atoms import (small, dumps,
    raisin_class, iterator, source_code)


__all__ = ['SERIALIZE_TABLE', 'DESERIALIZE_TABLE']

MODULES = (small, dumps, raisin_class, iterator, source_code)
SERIALIZE_TABLE = {
    func_name[10:]: func
    for module in MODULES
    for func_name, func in inspect.getmembers(module)
    if func_name.startswith('serialize_')
}
DESERIALIZE_TABLE = {
    func_name[12:]: func
    for module in MODULES
    for func_name, func in inspect.getmembers(module)
    if func_name.startswith('deserialize_')
}

__pdoc__ = {}
__pdoc__['SERIALIZE_TABLE'] = (
    'Dictionary that has each type of object, associates the function that allows to serialize it.'
)
__pdoc__['DESERIALIZE_TABLE'] = (
    'Dictionary that associates to each type of serialized object, '
    'the function that allows to deserialize it.'
)
