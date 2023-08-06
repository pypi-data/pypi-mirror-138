#!/usr/bin/env python3

"""
** Offers small and simple tools to help manage generators. **
--------------------------------------------------------------

More specifically, these are functions dedicated to flow management
for serialization and deserialization.
"""

import itertools
import tempfile

from raisin.serialization.constants import BUFFER_SIZE


def anticipate(gen):
    """
    ** Allows to know if the ceded packet is the last one. **

    Parametres
    ----------
    gen : iterable
        Generator of unknown 'length', which gives away objects of unknown length.

    Yields
    ------
    is_end : boolean
        A boolean which is True if the packet is the last one, False otherwise.
    pack
        The packet given up by the input generator.

    Raises
    ------
    RuntimeError
        In case there are no packages to count.

    Notes
    -----
    There is no verification on the entries.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import anticipate
    >>>
    >>> for is_end, pack in anticipate(range(3)):
    ...     print(is_end, pack)
    ...
    False 0
    False 1
    True 2
    >>> list(anticipate(['pack']))
    [(True, 'pack')]
    >>>
    """
    is_empty = True
    current = None

    for i, current in enumerate(gen):
        if i == 0:
            previous = current
            is_empty = False
            continue
        yield False, previous
        previous = current

    if is_empty:
        raise RuntimeError('The generator must not be empty.')
    yield True, current


def concat_gen(gen):
    r"""
    ** Add flags so that you can find the current division. **

    Goes together with the ``deconcat_gen`` function.

    Parameters
    ----------
    gen : generator
        Bytes string generator.

    Yields
    ------
    bytes
        The same packet as the input generator with a flag that
        gives the length of the packet.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import concat_gen
    >>>
    >>> gen = [b'a', b'houla', b'', b'hihi']
    >>> b''.join(concat_gen(gen))
    b'\x81a\x85houla\x80\x84hihi'
    >>>
    """
    yield from (size2tag(len(e)) + e for e in gen)


def data2gen(data):
    """
    ** Transforms the input into a byte generator. **

    Parameters
    ----------
    data
        A serialized object that can take various forms:

        - *bytes* : The entrance is returned as it was.
        - *generator* : The generator must yield strings of bytes or characters.
        - *BufferedReader* : The content of the file is transferred in packages.
        - *str* : (not recommended) The string must be encoded in ascii.
            The binary representation of the string is returned.
        - *TextIOWrapper* : (not recommended) The ascii content of the
            file is transferred in packages.

    Returns
    -------
    bytes
        A packet of bytes that precedes the generator.
    generator
        A byte chain generator.

    Raises
    ------
    ValueError
        In case a string is not written entirely in ascii.
    TypeError
        If the input is not convertible into a byte generator.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import data2gen
    >>>
    >>> pack, gen = data2gen(b'bytes string')
    >>> pack, list(gen)
    (b'bytes string', [])
    >>> pack, gen = data2gen('str string')
    >>> pack, list(gen)
    (b'str string', [])
    >>> pack, gen = data2gen(iter([b'a generator']))
    >>> pack, list(gen)
    (b'', [b'a generator'])
    >>>
    """

    def _file_like(data):
        while True:
            pack = data.read(BUFFER_SIZE)
            if pack:
                if isinstance(pack, bytes):
                    yield pack
                else:
                    try:
                        yield pack.encode(encoding='ascii')
                    except UnicodeEncodeError as err:
                        raise ValueError(
                            'If you want to deserialize a txt file '
                            '(which is not recommended), this file '
                            'must be written entirely in ascii.'
                        ) from err
            else:
                break

    def _iter(data):
        for pack in data:
            if isinstance(pack, bytes):
                yield pack
            elif isinstance(pack, str):
                try:
                    yield pack.encode(encoding='ascii')
                except UnicodeEncodeError as err:
                    raise ValueError(
                        'If you want to deserialize a string generator. '
                        'The strings must be written entirely in ascii.'
                    ) from err
            else:
                raise TypeError(
                    'The packets given by the generator must be of type '
                    f'str or bytes, not {pack.__class__.__name__}.'
                )

    if isinstance(data, bytes):
        return data, (lambda: (yield from []))()
    if isinstance(data, str):
        try:
            return data.encode(encoding='ascii'), (lambda: (yield from []))()
        except UnicodeEncodeError as err:
            raise ValueError(
                'if you want to deserialize a string, the string '
                'must be written entirely in ascii.'
            ) from err
    elif hasattr(data, 'read'):
        return b'', _file_like(data)
    elif hasattr(data, '__iter__'):
        return b'', _iter(data)
    else:
        raise TypeError('The argument provided is not in a supported type.')


def deconcat_gen(*, pack=b'', gen=(lambda: (yield from []))()):
    r"""
    ** Reconcile and re-cut the packets to their original shape. **

    Goes together with the ``concat_gen`` function.

    Parameters
    ----------
    pack : bytes
        The first element of the generator.
    gen : generator
        The rest of the packages to be rearranged.

    Yields
    ------
    bytes
        The reordered packages like the ones that were once provided
        at the input of the ``concat_gen`` function.

    Raises
    ------
    ValueError
        If there is an inconsistency in the packages.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import deconcat_gen
    >>> list(deconcat_gen(pack=b'\x81a\x85houla\x80\x84hihi'))
    [b'a', b'houla', b'', b'hihi']
    >>> list(deconcat_gen(gen=[b'\x81a\x85ho', b'ula\x80\x84hihi']))
    [b'a', b'houla', b'', b'hihi']
    >>>
    """
    n_pack = 0

    while True:
        # length recovery
        n_pack += 1
        try:
            size, pack, gen = tag2size(pack=pack, gen=gen)
        except RuntimeError as err:
            raise ValueError(
                'error in the header of package number ' f'{n_pack}. The flag is corrupted.'
            ) from err
        except StopIteration:
            break

        # concatenation of the enough number of data
        while len(pack) < size:
            try:
                pack += next(gen)
            except StopIteration as err:
                raise ValueError(
                    f'The package number {n_pack} is incomplete.\n'
                    f'Expected length: {size}\n'
                    f'Available length: {len(pack)}'
                ) from err

        # truncation to the exact length
        yield pack[:size]
        pack = pack[size:]


def relocate(gen):
    """
    ** Exhausts the input generator, identity function. **

    Parameters
    ----------
    gen : generator
        A byte string generator.

    Returns
    -------
    generator
        A kind of copy of the generator *gen*.

    Notes
    -----
    If the cumulative size of the data transferred by the *gen* generator
    does not exceed *BUFFER_SIZE*, then the buffering is done in RAM,
    otherwise the packets are stored in a temporary file in order to preserve RAM.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import relocate
    >>>
    >>> gen = iter([b'a', b'b'])
    >>> next(gen)
    b'a'
    >>> gen_copy = relocate(gen)
    >>> next(gen)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration
    >>> next(gen_copy)
    b'b'
    >>>
    """
    # the garbage collector is responsible for closing the file
    file = tempfile.SpooledTemporaryFile(max_size=BUFFER_SIZE, mode='w+b')
    for pack in concat_gen(gen):
        file.write(pack)
    file.seek(0)
    pack, gen = data2gen(file)
    return deconcat_gen(pack=pack, gen=gen)


def resize(nbr, *, pack=b'', gen=(lambda: (yield from []))()):
    """
    ** Allows to extract a precise number of bytes. **

    Parameters
    ----------
    nbr : int
        The precise number of bytes to extract.
    pack : bytes
        The first element of the generator.
    gen : generator
        The rest of the packages to be rearranged.

    Returns
    -------
    pack : bytes
        A string that contains exactly *nbr* bytes.
    gen : generator
        The generator provides in input possibly iterated or on the contrary,
        possibly lengthened if the input *pack* is bigger than the output one.

    Raises
    ------
    RuntimeError
        If there is not enough data to reach the requested length.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import resize
    >>> s = lambda out: (out[0], b''.join(out[1]))
    >>> s(resize(0))
    (b'', b'')
    >>> s(resize(0, pack=b'a'))
    (b'', b'a')
    >>> s(resize(0, gen=[b'a']))
    (b'', b'a')
    >>> s(resize(0, pack=b'a', gen=[b'b']))
    (b'', b'ab')
    >>> s(resize(1, pack=b'abc', gen=[b'de', b'fgh']))
    (b'a', b'bcdefgh')
    >>> s(resize(4, pack=b'abc', gen=[b'de', b'fgh']))
    (b'abcd', b'efgh')
    >>>
    """
    iter_gen = iter(gen)
    while len(pack) < nbr:
        try:
            pack += next(iter_gen)
        except StopIteration as err:
            raise RuntimeError(
                f'only {len(pack)} bytes are available while {nbr} are requested'
            ) from err
    if len(pack) > nbr:
        ext_gen = itertools.chain([pack[nbr:]], iter_gen)
        pack = pack[:nbr]
        return pack, ext_gen
    return pack, iter_gen


def size2tag(size):
    r"""
    ** Creates a flag that allows to group *size* bytes. **

    Parameters
    ----------
    size : int
        The number that can be encoded in the flag. >= 0

    Returns
    -------
    bytes
        The flags of variable size according to the size
        of the message to encode.

    Notes
    -----
    Can be very useful to record the size of a frame and be able
    to reconstruct it using the ``tag2size`` function.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import size2tag
    >>> p_bin = lambda flag: ', '.join(bin(o) for o in flag)
    >>>
    >>> size2tag(0)
    b'\x80'
    >>> p_bin(_)
    '0b10000000'
    >>> size2tag(1)
    b'\x81'
    >>> p_bin(_)
    '0b10000001'
    >>> size2tag(127)
    b'\xff'
    >>> p_bin(_)
    '0b11111111'
    >>> size2tag(128)
    b'\x01\x80'
    >>> p_bin(_)
    '0b1, 0b10000000'
    >>> size2tag(2**(7*3))
    b'\x01\x00\x00\x80'
    >>> p_bin(_)
    '0b1, 0b0, 0b0, 0b10000000'
    >>>
    """
    if size == 0:
        return b'\x80'
    flags_list = []
    while size:
        size, rest = divmod(size, 2 ** 7)
        flags_list.append(rest)
    flags_list.reverse()
    flags_list[-1] += 1 << 7
    return bytes(flags_list)


def tag2size(*, pack=b'', gen=(lambda: (yield from []))()):
    r"""
    ** Allows to find the number encoded in a flag. **

    Parameters
    ----------
    pack : bytes
        The first package of the *gen* generator.
        Must contain the beginning of the flag.
    gen : generator
        The generator that contains the sequence of bytes
        if they are not all specified in *pack*.

    Returns
    -------
    size : int
        The length represented by the flag.
    pack : bytes
        The entry package without the flag.
    gen : generator
        The *gen* generator possibly slightly iterated.

    Raises
    ------
    StopIteration
        If the flag is empty.
    RuntimeError
        If the flag is incomplete.

    Notes
    -----
    This is the bijection of the ``tag2size`` function.

    Examples
    --------
    >>> from raisin.serialization.iter_tools import tag2size
    >>>
    >>> tag2size(pack=b'\x80')[0]
    0
    >>> tag2size(pack=b'\x81')[0]
    1
    >>> tag2size(pack=b'\xff')[0]
    127
    >>> tag2size(pack=b'\x01\x80')[0]
    128
    >>> tag2size(pack=b'\x01\x00\x00\x80')[0]
    2097152
    >>>
    """
    gen = iter(gen)
    size = 0
    while True:
        if pack:
            octet, pack = pack[0], pack[1:]
        else:
            while not pack:
                try:
                    pack = next(gen)
                except StopIteration as err:
                    if size:
                        raise RuntimeError('the flag is not complete') from err
                    raise StopIteration('there are no data') from err
            octet, pack = pack[0], pack[1:]
        if octet & 0b10000000:  # if we reach the end of the flag
            size = (size << 7) + (octet - 0b10000000)
            return size, pack, gen
        size = (size << 7) + octet


def to_gen(*, gen=(lambda: (yield from []))(), size=BUFFER_SIZE, **pack_container):
    r"""
    ** Normalize the size of the packages. **

    Group the ceded packets by 'gen' in order to cede packets
    of normalized length.

    Parameters
    ----------
    pack : bytes
        The first pack.
    gen : generator
        The generator that assigns the sequence of pack.
    size : int or None, default=BUFFER_SIZE
        Size of yieled packages (if int).
        (if None), just make a generator whose first element is 'pack'.
        All the packets transferred are then identical to those of
        the input generator.

    Yields
    ------
    bytes
        A packet of size *size*, created by concatenating the input data.

    Notes
    -----
    There is no verification on the entries.

    Examples
    --------
    >>> import random
    >>> from raisin.serialization.iter_tools import to_gen
    >>>
    >>> random.seed(0)
    >>>
    >>> l = [b'\x00'*random.randint(0, 1000) for i in range(4)]
    >>> [len(e) for e in l]
    [864, 394, 776, 911]
    >>>
    >>> [len(e) for e in to_gen(gen=l, size=500)]
    [500, 500, 500, 500, 500, 445]
    >>> [len(e) for e in to_gen(pack=b'', gen=l, size=500)]
    [500, 500, 500, 500, 500, 445]
    >>> [len(e) for e in to_gen(pack=b'\x00'*55, gen=l, size=500)]
    [500, 500, 500, 500, 500, 500]
    >>> [len(e) for e in to_gen(pack=b'\x00'*56, gen=l, size=500)]
    [500, 500, 500, 500, 500, 500, 1]
    >>>
    >>> [len(e) for e in to_gen(gen=l, size=None)]
    [864, 394, 776, 911]
    >>> [len(e) for e in to_gen(pack=b'\x00'*55, gen=l, size=None)]
    [55, 864, 394, 776, 911]
    >>> [len(e) for e in to_gen(pack=b'', gen=l, size=None)]
    [0, 864, 394, 776, 911]
    >>>
    """
    assert set(pack_container).issubset({'pack'})

    if size is None:
        if 'pack' in pack_container:
            yield pack_container['pack']
        yield from gen
    else:
        pack = pack_container.get('pack', b'')
        while len(pack) > size:
            yield pack[:size]
            pack = pack[size:]
        for data in gen:
            pack += data
            while len(pack) > size:
                yield pack[:size]
                pack = pack[size:]
        yield pack
