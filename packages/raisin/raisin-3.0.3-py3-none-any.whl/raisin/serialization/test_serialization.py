#!/usr/bin/env python3

"""
** Allows for extensive testing around serialization. **
--------------------------------------------------------

There is a function capable of generating many types of objects.
For each of these objects they are serialized then deserialized.
"""

import sys

import pytest

from raisin.serialization.constants import ALPHABET, BUFFER_SIZE
from raisin.serialization import dumps, loads, serialize, deserialize
from raisin.encapsulation.packaging import Argument, Func, Result, Task
from raisin.communication.handler import get_self_identity


# @pytest.mark.skipif(os.name == 'posix', reason="do not run on mac os")


LEN = {
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    15,
    16,
    17,
    31,
    32,
    33,
    63,
    64,
    65,
    127,
    128,
    129,
    255,
    256,
    257,
    1023,
    1024,
    1025,
    2047,
    2048,
    2049,
    BUFFER_SIZE - 1,
    BUFFER_SIZE,
    BUFFER_SIZE + 1,
    2 * BUFFER_SIZE - 1,
    2 * BUFFER_SIZE,
    2 * BUFFER_SIZE + 1,
}


def get_bytes():
    """
    ** Makes somme various bytes string. **
    """
    yield b''
    yield from (bytes([i]) for i in range(256))
    yield from (bytes(l) for l in LEN)

def get_float():
    """
    ** Makes some various floats. **
    """
    yield 0.0
    yield 1.0
    yield 0.123
    yield 0.123456
    yield 0.123456789
    yield 123456789.123456789
    yield sys.float_info.max
    yield -sys.float_info.max
    yield sys.float_info.min
    yield -sys.float_info.min

def get_int():
    """
    ** Makes some various intergers. **
    """
    yield 0
    for i in [2 ** j for j in range(1, 16)]:
        yield 2 ** i - 1
        yield 2 ** i
        yield 2 ** i + 1
        yield -(2 ** i - 1)
        yield -(2 ** i)
        yield -(2 ** i + 1)

def get_list():
    """
    ** Makes some various list. **
    """
    for list_len in [0, 1, 2, 4, 100]:
        yield [None for _ in range(list_len)]

def get_str():
    """
    ** Makes some various str. **
    """
    yield ''
    yield 'a'
    yield 'abcdefghi'
    yield ''.join(chr(i) for i in range(256))

def get_simple_objects():
    """
    ** Yield some vaious simple objects. **
    """
    yield None
    yield True
    yield False
    yield from get_bytes()
    yield from get_float()
    yield from get_int()
    yield from get_list()
    yield from get_str()


def test_ser_gen():
    """
    ** Tests ``raisin.serialization.deserialize``. **
    """
    for obj in get_simple_objects():
        assert deserialize(serialize(obj)) == obj

def _test_dump(obj_gen):
    """
    ** Test for given objects. **
    """
    for obj in obj_gen:
        ser = dumps(obj, compresslevel=1)
        assert all(c in ALPHABET for c in ser)
        assert loads(ser) == obj

def test_dumps():
    """
    ** Tests dumps. **
    """
    _test_dump(obj for obj in get_simple_objects() if sys.getsizeof(obj) <= 10000)

@pytest.mark.slow
def test_dumps_slow():
    """
    ** Tests dumps. **
    """
    _test_dump(obj for obj in get_simple_objects() if 10000 < sys.getsizeof(obj) < 1000000)

def test_raisin_class():
    """
    ** Tests raisin class. **
    """
    arg = Argument(0)
    func = Func(lambda x: x ** 2)
    task = Task(hash(func), (hash(arg),))
    result = Result(0)
    identity = get_self_identity()

    assert deserialize(serialize(arg)) == arg
    assert deserialize(serialize(func)) == func
    assert deserialize(serialize(task)) == task
    assert deserialize(serialize(result)) == result
    assert deserialize(serialize(identity)) == identity

def test_composed_list():
    """
    ** Test the serialization of compound lists. **
    """
    objs = (
        [[]],
        [[[]]],
        [[None]],
        [[], []],
        [[None], [None]])
    for obj in objs:
        assert deserialize(serialize(obj)) == obj
