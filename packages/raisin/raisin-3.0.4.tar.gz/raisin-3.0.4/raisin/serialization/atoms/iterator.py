#!/usr/bin/env python3

"""
** Allows to serialize and deserialize generators. **

More particularly, it allows to serialize iterators,
often containers like (*list*, *tuple*, *set*...).
On the other hand, deserialization is presented in the form of a generator.
It will be necessary to recast in the right type.
"""

from raisin.serialization.constants import HEADER
from raisin.serialization.iter_tools import anticipate, size2tag, tag2size


def _ser_generator(obj, compact, copy_file, paralleling_rate):
    r"""
    ** Serialize the content of any iterable object. **

    Don't give in to the urge!
    This function is meant to be used for serialization of other containers.

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import _ser_generator
    >>> s = lambda obj: b''.join(
    ...     _ser_generator(obj, compact=True, copy_file=False, paralleling_rate=0))
    >>> s([])
    b''
    >>> s([None])
    b'\x82\x01\x13'
    >>> s([None, None])
    b'\x82\x01\x13\x82\x01\x13'
    >>>
    """
    from raisin.serialization.core import serialize
    try:
        yield from (
            size2tag(1 + len(pack)) + bytes([is_end]) + pack
            for item in obj
            for is_end, pack in anticipate(
                serialize(
                    item,
                    compresslevel=compact,
                    copy_file=copy_file,
                    psw=None,
                    authenticity=False,
                    paralleling_rate=paralleling_rate,
                )
            )
        )
    except RuntimeError:  # if the generator is empty
        pass


def serialize_generator(obj, compact, copy_file, paralleling_rate):
    r"""
    ** Serialize the generators. **

    Be careful, iter on the object, in the case of a generator for example,
    it will be exhausted after the call of this function.

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import serialize_generator
    >>> s = lambda obj: b''.join(
    ...     serialize_generator(obj, compact=True, copy_file=False, paralleling_rate=0))
    >>> s([])
    b'\x18'
    >>> s([None])
    b'\x18\x82\x01\x13'
    >>> s([None, None])
    b'\x18\x82\x01\x13\x82\x01\x13'
    >>>
    """
    yield HEADER['generator'][compact]
    yield from _ser_generator(obj, compact, copy_file, paralleling_rate)


def deserialize_generator(pack, gen, psw, paralleling_rate):
    r"""
    ** Gives up the elements of the serialized iterator. **

    Yields
    ------
    The deserialized elements are equivalent to those present
    in the initial iterable, before it was serialized.

    Raises
    ------
    ValueError
        If there is an inconsistency in the data.
    RuntimeError
        If there is not enough data available.

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import deserialize_generator
    >>> list(deserialize_generator(b'', [], None, 0))
    []
    >>> list(deserialize_generator(b'\x82\x01\x13', [], None, 0))
    [None]
    >>> list(deserialize_generator(b'\x82\x01\x13\x82\x01\x13', [], None, 0))
    [None, None]
    >>>
    """
    from raisin.serialization.core import deserialize

    class IsEnd(Exception):
        """ raising to announce the end """

    class SubItems:
        """help for iter into an over iterator"""

        def __init__(self, pack, gen):
            self.pack = pack
            self.gen = iter(gen)

        def item_raw(self, item_range):
            """give away the raw data of an item"""
            subitem_range = 0
            while True:
                try:
                    size, self.pack, self.gen = tag2size(pack=self.pack, gen=self.gen)
                except StopIteration as err:
                    raise IsEnd from err
                except RuntimeError as err:
                    raise RuntimeError(
                        f'the header of subpackage n {subitem_range} '
                        f'of element n {item_range} is incomplete.'
                    ) from err

                while len(self.pack) < size:
                    try:
                        self.pack += next(self.gen)
                    except StopIteration as err:
                        raise RuntimeError(
                            f'we expect subpackage n {subitem_range} element n {item_range} to be '
                            f'serialized with {size} bytes, but only {len(self.pack)} are available'
                        ) from err
                is_end, self.pack = self.pack[0], self.pack[1:]
                if is_end > 1:
                    raise ValueError(
                        f'the byte which designates if the subpackage n {subitem_range} of element '
                        f'n {item_range} is the last one is a boolean which can only take '
                        f'the values 0 or 1, and it is {is_end}'
                    )

                data, self.pack = self.pack[:size-1], self.pack[size-1:]
                yield data
                if is_end:
                    break
                subitem_range += 1

        def get_item(self, item_range, psw, paralleling_rate):
            """deserialize the item"""
            return deserialize(
                pack=b'', gen=self.item_raw(item_range), psw=psw, paralleling_rate=paralleling_rate
            )

    sub_items = SubItems(pack=pack, gen=gen)
    item_range = 0
    while True:
        try:
            yield sub_items.get_item(item_range, psw=psw, paralleling_rate=paralleling_rate)
        except IsEnd:
            break
        item_range += 1


def serialize_tuple(obj, compact, copy_file, paralleling_rate):
    r"""
    ** Serialize tuple. **

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import serialize_tuple
    >>> s = lambda obj: b''.join(
    ...     serialize_tuple(obj, compact=True, copy_file=False, paralleling_rate=0))
    >>> s(())
    b'\x0e'
    >>> s((None,))
    b'\x0e\x82\x01\x13'
    >>> s((None, None))
    b'\x0e\x82\x01\x13\x82\x01\x13'
    >>>
    """
    yield HEADER['tuple'][compact]
    yield from _ser_generator(obj, compact, copy_file, paralleling_rate)


def deserialize_tuple(pack, gen, psw, paralleling_rate):
    r"""
    ** Deserialize tuple. **

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import deserialize_tuple
    >>> deserialize_tuple(b'', [], None, 0)
    ()
    >>> deserialize_tuple(b'\x82\x01\x13', [], None, 0)
    (None,)
    >>> deserialize_tuple(b'\x82\x01\x13\x82\x01\x13', [], None, 0)
    (None, None)
    >>>
    """
    return tuple(
        deserialize_generator(pack=pack, gen=gen, psw=psw, paralleling_rate=paralleling_rate)
    )


def serialize_list(obj, compact, copy_file, paralleling_rate):
    r"""
    ** Serialize liste. **

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import serialize_list
    >>> s = lambda obj: b''.join(
    ...     serialize_list(obj, compact=True, copy_file=False, paralleling_rate=0))
    >>> s([])
    b'\r'
    >>> s([None])
    b'\r\x82\x01\x13'
    >>> s([None, None])
    b'\r\x82\x01\x13\x82\x01\x13'
    >>>
    """
    yield HEADER['list'][compact]
    yield from _ser_generator(obj, compact, copy_file, paralleling_rate)


def deserialize_list(pack, gen, psw, paralleling_rate):
    r"""
    ** Deserialize liste. **

    Examples
    --------
    >>> from raisin.serialization.atoms.iterator import deserialize_list
    >>> deserialize_list(b'', [], None, 0)
    []
    >>> deserialize_list(b'\x82\x01\x13', [], None, 0)
    [None]
    >>> deserialize_list(b'\x82\x01\x13\x82\x01\x13', [], None, 0)
    [None, None]
    >>>
    """
    return list(
        deserialize_generator(pack=pack, gen=gen, psw=psw, paralleling_rate=paralleling_rate)
    )
