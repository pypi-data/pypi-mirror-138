#!/usr/bin/env python3

"""
** Allows to serialize and deserialize the classes of the module. **

As the source code of these classes is already known,
it is useless to serialize it too.
That's why we treat these classes separately.
"""

from raisin.serialization.constants import HEADER
from raisin.serialization.iter_tools import to_gen


def _init_class(cls, state, **kwds):
    """
    ** Constructs and instantiates a class via *__setstate__* method. **
    """
    inst = cls.__new__(cls)
    inst.__setstate__(state, **kwds)
    return inst


def serialize_argument(obj, compact, **kwds):
    r"""
    ** Serialize the ``raisin.encapsulation.packaging.Argument``. **

    Examples
    --------
    >>> from raisin.encapsulation.packaging import Argument
    >>> from raisin.serialization.atoms.raisin_class import serialize_argument
    >>> arg = Argument(0)
    >>> b''.join(serialize_argument(arg, compact=True))
    b'%\x03\x00'
    >>>
    """
    yield HEADER['argument'][compact]
    yield from obj.__getstate__(as_iter=True, compresslevel=compact, **kwds)


def deserialize_argument(pack, gen, **kwds):
    r"""
    ** Deserialize ``raisin.encapsulation.packaging.Argument``. **

    Examples
    --------
    >>> from raisin.serialization.atoms.raisin_class import deserialize_argument
    >>> deserialize_argument(pack=b'\x03\x00', gen=[])
    Argument(0)
    >>>
    """
    from raisin.encapsulation.packaging import Argument
    return _init_class(Argument, to_gen(pack=pack, gen=gen), **kwds)


def serialize_func(obj, compact, **kwds):
    r"""
    ** Serialize the ``raisin.encapsulation.packaging.Func``. **

    Examples
    --------
    >>> from raisin.encapsulation.packaging import Func
    >>> from raisin.serialization.atoms.raisin_class import serialize_func
    >>> Func(lambda x: x**2)
    Func(<lambda>)
    >>> data = b''.join(serialize_func(_, compact=True))
    >>> type(data)
    <class 'bytes'>
    >>> data != b''
    True
    >>>
    """
    yield HEADER['func'][compact]
    yield from obj.__getstate__(as_iter=True, compresslevel=compact, **kwds)


def deserialize_func(pack, gen, **kwds):
    r"""
    ** Deserialize ``raisin.encapsulation.packaging.Func``. **

    Examples
    --------
    >>> from raisin.encapsulation.packaging import Func
    >>> from raisin.serialization.atoms.raisin_class import serialize_func, deserialize_func
    >>> Func(lambda x: x**2)
    Func(<lambda>)
    >>> data = b''.join(serialize_func(_, compact=True))
    >>> deserialize_func(pack=data, gen=[])
    Func(<lambda>)
    >>>
    """
    from raisin.encapsulation.packaging import Func
    return _init_class(Func, to_gen(pack=pack, gen=gen), **kwds)


def serialize_task(obj, compact, **kwds):
    r"""
    ** Serialize the ``raisin.encapsulation.packaging.Task``. **

    Examples
    --------
    >>> from pprint import pprint
    >>> from raisin.encapsulation.packaging import Argument, Func, Task
    >>> from raisin.serialization.atoms.raisin_class import serialize_task
    >>> arg = Argument(0)
    >>> func = Func(lambda x : x**2)
    >>> task = Task(func.__hash__(), (arg.__hash__(),))
    >>> pprint(b''.join(serialize_task(task, compact=True)))
    (b"'\x0e\x8a\x01\x03~\xc3\xe6\x03#\xe6\xab\x90\x82\x00\x0e\x8c\x01\x8a\x01"
     b'\x03w\x06z\xe3!\xd2A\xdc')
    >>>
    """
    yield HEADER['task'][compact]
    yield from obj.__getstate__(as_iter=True, compresslevel=compact, **kwds)


def deserialize_task(pack, gen, **kwds):
    r"""
    ** Deserialize ``raisin.encapsulation.packaging.Task``. **

    Examples
    --------
    >>> from raisin.serialization.atoms.raisin_class import deserialize_task
    >>> pack = (b'\x0e\x8a\x01\x03~\xc3\xe6\x03#\xe6\xab\x90\x82\x00\x0e'
    ...         b'\x8c\x01\x8a\x01\x03w\x06z\xe3!\xd2A\xdc')
    >>> deserialize_task(pack=pack, gen=[])
    Task(9134397370399107984, (8576677656317280732,))
    >>>
    """
    from raisin.encapsulation.packaging import Task
    return _init_class(Task, to_gen(pack=pack, gen=gen), **kwds)


def serialize_result(obj, compact, **kwds):
    r"""
    ** Serialize the ``raisin.encapsulation.packaging.Result``. **

    Examples
    --------
    >>> from raisin.encapsulation.packaging import Result
    >>> from raisin.serialization.atoms.raisin_class import serialize_result
    >>> res = Result(0)
    >>> b''.join(serialize_result(res, compact=True))
    b'(\x03\x00'
    >>>
    """
    yield HEADER['result'][compact]
    yield from obj.__getstate__(as_iter=True, compresslevel=compact, **kwds)


def deserialize_result(pack, gen, **kwds):
    r"""
    ** Deserialize ``raisin.encapsulation.packaging.Result``. **

    Examples
    --------
    >>> from raisin.serialization.atoms.raisin_class import deserialize_result
    >>> deserialize_result(pack=b'\x03\x00', gen=[])
    Result(0)
    >>>
    """
    from raisin.encapsulation.packaging import Result
    return _init_class(Result, to_gen(pack=pack, gen=gen), **kwds)

def serialize_identity(obj, compact, **_):
    """
    ** Serialise the ``raisin.communication.handler.get_self_identity`` output. **

    Examples
    --------
    >>> from raisin.communication.handler import get_self_identity
    >>> from raisin.serialization.atoms.raisin_class import serialize_identity
    >>> identity = get_self_identity()
    >>> data = b''.join(serialize_identity(identity, compact=True))
    >>>
    """
    from raisin.serialization.atoms.iterator import _ser_generator
    yield HEADER['identity'][compact]
    yield from _ser_generator(obj, compact, copy_file=False, paralleling_rate=0)

def deserialize_identity(pack, gen, psw, paralleling_rate):
    """
    ** Deserialize ``raisin.communication.handler.get_self_identity`` output. **

    Examples
    --------
    >>> from raisin.communication.handler import get_self_identity
    >>> from raisin.serialization.atoms.raisin_class import serialize_identity, deserialize_identity
    >>> identity = get_self_identity()
    >>> identity # doctest: +SKIP
    Identity(mac='fd:86:63:3e:c8:fd', username='robin', version='3.6.15', admin=False, os='linux')
    >>> data = b''.join(serialize_identity(identity, compact=True))[1:]
    >>> id_bis = deserialize_identity(data, [], None, 0)
    >>> id_bis # doctest: +SKIP
    Identity(mac='fd:86:63:3e:c8:fd', username='robin', version='3.6.15', admin=False, os='linux')
    >>> identity == id_bis
    True
    >>>
    """
    from raisin.serialization.atoms.iterator import deserialize_generator
    from raisin.communication.handler import get_self_identity
    return get_self_identity(cls=True)(*deserialize_generator(pack, gen, psw, paralleling_rate))
