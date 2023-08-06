#!/usr/bin/env python3

"""
** Unitary creation of packets. **
----------------------------------

This is where there are the basic classes that represent the fundamental
packets for transferring data across the network.
"""

import abc
import hashlib

from raisin.serialization import deserialize, serialize

__pdoc__ = {
    'Package.__repr__': True,
    'Package.__hash__': True,
    'Package.__eq__': True,
    'Package.__getstate__': True,
    'Package.__setstate__': True}


class Package:
    """
    ** Base class to represent a package. **
    """

    def __repr__(self):
        """
        ** Improve representation. **

        Returns an evaluable representation in a particular context
        of the dynamic instance of an object inherited from this class.

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Package
        >>> Package()
        Package()
        >>>
        """
        return f'{self.__class__.__name__}()'

    def __hash__(self):
        """
        ** Compute a real unique hash. **

        The hash calculation is based on the content of the object,
        not on the addresses in memory.

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Package
        >>> {Package(), Package()}
        {Package()}
        >>>
        """
        if self.__class__.__name__ == 'Package':
            return 0
        return int(
            hashlib.sha1(
                b''.join(serialize(self.__getstate__(), compresslevel=1))
            ).hexdigest(),
            base=16
        ) % (2**64) # TODO : Make a real hash function!

    def __eq__(self, other):
        """
        ** Compare 2 objects based on the hash. **

        2 objects are equal if they are exactly
        the same type and have the same hash value.
        This function is essential to be able to apply
        hashable collections on ``Package`` instance.

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Package
        >>> Package() == Package()
        True
        >>>
        """
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        return hash(self) == hash(other)

    @abc.abstractmethod
    def __getstate__(self, as_iter=False, **kwds):
        """
        ** Help for the serialization. **

        Must be overwritten.

        Parameters
        ----------
        as_iter : boolean
            If True, returns a generator rather than binary.
            This can be useful to preserve RAM.
        **kwds : dict
            Arguments passed to the function ``raisin.serialization.serialize``.

        Returns
        -------
        state : bytes or iterable
            Sufficient information to reconstruct the object.
        """
        raise NotImplementedError('this abstract method must be overwritten')

    @abc.abstractmethod
    def __setstate__(self, state, **kwds):
        """
        ** Allows you to reconstruct the object. **

        Must be overwritten.
        This method replaces *__init__*. It is for example used by *pickle*.

        Parameters
        ----------
        state : bytes or iterable
            The state of the object is the value returned
            by the method ``Argument.__getstate__``.
        **kwds : dict
            Arguments passed to the function ``raisin.serialization.deserialize``.
        """
        raise NotImplementedError('this abstract method must be overwritten')


class Argument(Package):
    """
    ** Represents an argument for a function. **
    """

    def __init__(self, arg):
        self._arg = arg

    def get_value(self):
        """
        ** Accessor to retrieve the value of the argument. **

        Example
        -------
        >>> from raisin.encapsulation.packaging import Argument
        >>> Argument(0)
        Argument(0)
        >>> _.get_value()
        0
        >>>
        """
        return self._arg

    def __repr__(self):
        """
        ** Improve representation. **

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Argument
        >>> Argument(0)
        Argument(0)
        >>> a = 1
        >>> Argument(a)
        Argument(1)
        >>> Argument('toto')
        Argument('toto')
        >>> Argument(10**100)
        Argument(<arg>)
        >>>
        """
        arg_name = repr(self._arg)
        if len(arg_name) > 100:
            arg_name = '<arg>'
        return f'Argument({arg_name})'

    def __getstate__(self, as_iter=False, **kwds):
        """
        ** Implementation of ``Package.__getstate__``. **

        Examples
        --------
        >>> from pickle import dumps
        >>> from raisin.encapsulation.packaging import Argument
        >>> Argument(0)
        Argument(0)
        >>> type(dumps(_))
        <class 'bytes'>
        >>>
        """
        if as_iter is False:
            return b''.join(self.__getstate__(as_iter=True, **kwds))
        return serialize(self.get_value(), **kwds)

    def __setstate__(self, state, **kwds):
        """
        ** Implementation of ``Package.__setstate__``. **

        Examples
        --------
        >>> from pickle import dumps, loads
        >>> from raisin.encapsulation.packaging import Argument
        >>> Argument(0)
        Argument(0)
        >>> loads(dumps(_))
        Argument(0)
        >>>
        """
        self._arg = deserialize(state, **kwds)


class Func(Package):
    """
    ** Encapsulate a simple function. **
    """

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        """
        ** Metamorphose this object into a function. **
        """
        return self._func(*args, **kwargs)

    def __repr__(self):
        """
        ** Improve representation. **

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Func
        >>> def f(): pass
        >>> Func(f)
        Func(f)
        >>> g = f
        >>> Func(g)
        Func(f)
        >>> Func(lambda x : None)
        Func(<lambda>)
        >>>
        """
        try:
            return f'Func({self._func.__name__})'
        except AttributeError:
            return 'Func(<lambda>)'

    def __hash__(self):
        """
        ** Implementation of ``Package.__hash__``. **
        """
        return int(
            hashlib.sha1(self._func.__name__.encode()).hexdigest(), base=16
        ) % (2**64) # TODO : Make a real hash function!

    def __getstate__(self, as_iter=False, **kwds):
        """
        ** Implementation of ``Package.__getstate__``. **

        Examples
        --------
        >>> from pickle import dumps
        >>> from raisin.encapsulation.packaging import Func
        >>> Func(lambda x: x**2)
        Func(<lambda>)
        >>> type(dumps(_))
        <class 'bytes'>
        >>>
        """
        if as_iter is False:
            return b''.join(self.__getstate__(as_iter=True, **kwds))
        return serialize(self._func, **kwds)

    def __setstate__(self, state, **kwds):
        """
        ** Implementation of ``Package.__setstate__``. **

        Examples
        --------
        >>> from pickle import dumps, loads
        >>> from raisin.encapsulation.packaging import Func
        >>> Func(lambda x: x**2)
        Func(<lambda>)
        >>> loads(dumps(_))
        Func(<lambda>)
        >>>
        """
        self._func = deserialize(state, **kwds)


class Result(Package):
    """
    ** Represents the result of a job. **
    """

    def __init__(self, res):
        self._res = res

    def get_value(self):
        """
        ** Accessor to retrieve the value of the argument. **

        Example
        -------
        >>> from raisin.encapsulation.packaging import Result
        >>> Result(0)
        Result(0)
        >>> _.get_value()
        0
        >>>
        """
        return self._res

    def __repr__(self):
        """
        ** Improve representation. **

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Result
        >>> Result(0)
        Result(0)
        >>> a = 1
        >>> Result(a)
        Result(1)
        >>> Result('toto')
        Result('toto')
        >>> Result(10**100)
        Result(<res>)
        >>>
        """
        res_name = repr(self._res)
        if len(res_name) > 100:
            res_name = '<res>'
        return f'Result({res_name})'

    def __getstate__(self, as_iter=False, **kwds):
        """
        ** Implementation of ``Package.__getstate__``. **

        Examples
        --------
        >>> from pickle import dumps
        >>> from raisin.encapsulation.packaging import Result
        >>> Result(0)
        Result(0)
        >>> type(dumps(_))
        <class 'bytes'>
        >>>
        """
        if as_iter is False:
            return b''.join(self.__getstate__(as_iter=True, **kwds))
        return serialize(self.get_value(), **kwds)

    def __setstate__(self, state, **kwds):
        """
        ** Implementation of ``Package.__setstate__``. **

        Examples
        --------
        >>> from pickle import dumps, loads
        >>> from raisin.encapsulation.packaging import Result
        >>> Result(0)
        Result(0)
        >>> loads(dumps(_))
        Result(0)
        >>>
        """
        self._res = deserialize(state, **kwds)



class Task(Package):
    """
    ** Complete block to perform a calculation. **
    """

    def __init__(self, func_hash, arg_hashes):
        self.func_hash = func_hash
        self.arg_hashes = arg_hashes

    def __repr__(self):
        """
        ** Improve representation. **

        Examples
        --------
        >>> from raisin.encapsulation.packaging import Argument, Func, Task
        >>> func = Func(lambda x: x**2)
        >>> arg1 = Argument(0)
        >>> arg2 = Argument(1)
        >>> Task(func.__hash__(), (arg1.__hash__(), arg2.__hash__()))
        Task(9134397370399107984, (8576677656317280732, 12402937695876512259))
        >>>
        """
        return f'Task({self.func_hash}, {self.arg_hashes})'

    def __getstate__(self, as_iter=False, **kwds):
        """
        ** Implementation of ``Package.__getstate__``. **

        Examples
        --------
        >>> from pickle import dumps
        >>> from raisin.encapsulation.packaging import Argument, Func, Task
        >>> func = Func(lambda x: x**2)
        >>> arg1 = Argument(0)
        >>> arg2 = Argument(1)
        >>> Task(func.__hash__(), (arg1.__hash__(), arg2.__hash__()))
        Task(9134397370399107984, (8576677656317280732, 12402937695876512259))
        >>> type(dumps(_))
        <class 'bytes'>
        >>>
        """
        if as_iter is False:
            return b''.join(self.__getstate__(as_iter=True, **kwds))
        return serialize((self.func_hash, self.arg_hashes), **kwds)

    def __setstate__(self, state, **kwds):
        """
        ** Implementation of ``Package.__setstate__``. **

        Examples
        --------
        >>> from pickle import dumps, loads
        >>> from raisin.encapsulation.packaging import Argument, Func, Task
        >>> func = Func(lambda x: x**2)
        >>> arg1 = Argument(0)
        >>> arg2 = Argument(1)
        >>> Task(func.__hash__(), (arg1.__hash__(), arg2.__hash__()))
        Task(9134397370399107984, (8576677656317280732, 12402937695876512259))
        >>> loads(dumps(_))
        Task(9134397370399107984, (8576677656317280732, 12402937695876512259))
        >>>
        """
        self.func_hash, self.arg_hashes = deserialize(state, **kwds)
