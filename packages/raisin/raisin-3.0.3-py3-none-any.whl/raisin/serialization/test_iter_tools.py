#!/usr/bin/env python3

"""
** Allows for extensive testing around serialization. **
--------------------------------------------------------

There is a function capable of generating many types of objects.
For each of these objects they are serialized then deserialized.
"""

import itertools

import pytest

from raisin.serialization.constants import BUFFER_SIZE
from raisin.serialization.iter_tools import (
    anticipate,
    concat_gen,
    deconcat_gen,
    relocate,
    resize,
    size2tag,
    tag2size,
    to_gen,
)


def test_anticipate():
    """
    ** Tests ``raisin.serialization.iter_tools.anticipate``. **
    """
    assert list(anticipate([''])) == [(True, '')]
    assert list(anticipate(['', ''])) == [(False, ''), (True, '')]
    assert list(anticipate(['', '', ''])) == [(False, ''), (False, ''), (True, '')]
    with pytest.raises(RuntimeError):
        list(anticipate([]))

def test_concat():
    """
    ** Tests ``raisin.serialization.iter_tools.concat_gen``. **
    """
    for gen in ([], [b''], [b'', b''], [b'a'], [b'a', b'b'], [b'', b'b'], [b'a', b'']):
        assert list(deconcat_gen(gen=concat_gen(gen))) == gen
        assert list(deconcat_gen(pack=b''.join(concat_gen(gen)))) == gen
    for gen in ([b'a'], [b'a', b'b']):
        with pytest.raises(ValueError): # without header
            list(deconcat_gen(pack=b''.join(concat_gen(gen))[1:]))
        with pytest.raises(ValueError):
            list(deconcat_gen(pack=b''.join(concat_gen(gen))[:-1]))

def test_relocate():
    """
    ** Tests ``raisin.serialization.iter_tools.relocate``. **
    """
    iterator = iter([])
    iterator_bis = relocate(iterator)
    with pytest.raises(StopIteration):
        next(iterator_bis)
    with pytest.raises(StopIteration):
        next(iterator)
    for gen in (
        [b'a'],
        [b'a', b'b', b'c'],
        itertools.chain([b'a'], (b'b' * BUFFER_SIZE for _ in range(10))),
    ):
        iterator = iter(gen)
        iterator_bis = relocate(iterator)
        with pytest.raises(StopIteration):
            next(iterator)
        assert next(iterator_bis) == b'a'

def test_resize():
    """
    ** Tests ``raisin.serialization.iter_tools.resize``. **
    """
    for nbr in [0, 1, 2, 10, 100, 1000]:
        for pack_len in [0, 1, 2, 10, 100, 1000]:
            for gen_len in [0, 1, 2, 4]:
                for gen_item_len in [0, 1, 100, 500]:
                    pack = bytes(pack_len)
                    gen = (bytes(gen_item_len) for _ in range(gen_len))
                    if nbr <= pack_len + gen_len * gen_item_len:
                        pack_, gen_ = resize(nbr, pack=pack, gen=gen)
                        assert len(pack_) == nbr
                        assert len(pack_ + b''.join(gen_)) == pack_len + gen_len * gen_item_len
                    else:
                        with pytest.raises(RuntimeError):
                            resize(nbr, pack=pack, gen=gen)

def test_to_gen():
    """
    ** Tests ``raisin.serialization.iter_tools.to_gen``. **
    """
    for size in [1, 2, 1000, BUFFER_SIZE]:
        for gen in (
            [],
            [b''],
            [b'a'],
            [b'a' * size],
            [b'a' * (size - 1)],
            [b'a' * (size + 1)],
            [b'', b''],
            [b'a' * ((2 ** l) % (2 * size)) for l in range(100)],
        ):
            l_in = [len(e) for e in gen]
            l_out = [len(e) for e in to_gen(gen=gen, size=size)]
            assert sum(l_in) == sum(l_out)
            assert all(s == size for s in l_out[:-1])
            assert l_out[-1] <= size
            l_out = [len(e) for e in to_gen(pack=b''.join(gen), size=size)]
            assert sum(l_in) == sum(l_out)
            assert all(s == size for s in l_out[:-1])
            assert l_out[-1] <= size

def test_size_tag():
    """
    ** Tests ``raisin.serialization.iter_tools.size2tag``. **
    """
    with pytest.raises(StopIteration):
        tag2size(pack=b'')
    for size in [0, 1, 2, 127, 128, 129, 123456789123456789]:
        pack = size2tag(size)
        assert tag2size(pack=pack)[0] == size
        if len(pack) >= 2:
            with pytest.raises(RuntimeError):
                tag2size(pack=pack[:-1])
