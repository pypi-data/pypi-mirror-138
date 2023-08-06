#!/usr/bin/env python3

"""
** Forms the packages. **
-------------------------

Allows to generate packages.
"""

import queue
import threading

from raisin.encapsulation.packaging import Argument, Func, Task
from raisin.communication.request import send_package


__pdoc__ = {
    'TasksSharer.__enter__': True,
    'TasksSharer.__exit__': True,
    'TasksSharer.__iter__': True}


def make_tasks(functions, arguments):
    r"""
    ** Generates the tasks to be performed. **

    Parameters
    ----------
    functions : iterable
        Generator that assigns each function associated with each task.
        In the case of map, this iterator must yield the same function at each iteration.
    arguments : iterable
        Generator that assigns the set of arguments for each task. At each iteration
        the arguments must be provided via a tuple of size *n*, with *n* the number
        of arguments that the function associated with this task takes.

    Yields
    ------
    new_packages : list
        The list of packets to send for the proper functioning of the task.
        This list contains packets of type ``raisin.encapsulation.packaging.Func``
        or ``raisin.encapsulation.packaging.Argument``.
        This list does not contain packages that have already been assigned
        to a previous task, even if they are also needed for the current task.
    task : ``raisin.encapsulation.packaging.Task``
        The task to execute, which contains the address of the function and its arguments.

    Notes
    -----
    - There is no verification on the inputs, they must be verified by higher level functions.
    - For functions, the detection of redundancy is done from the address of the memory pointer.

    Examples
    --------
    >>> from itertools import cycle
    >>> from raisin.encapsulation.manager import make_tasks
    >>>
    >>> def f(x, y):
    ...     return x**2 + y**2
    ...
    >>> def pprint(job):
    ...    for i, (new_packages, task) in enumerate(job):
    ...        print(f'iter {i}:\n    new: {new_packages}\n    task: {task}')
    ...
    >>> pprint(make_tasks(cycle((f,)), [(1, 2), (2, 3)]))
    iter 0:
        new: [Argument(1), Argument(2), Func(f)]
        task: Task(3689584644591251701, [12402937695876512259, 15584102817361292984])
    iter 1:
        new: [Argument(3)]
        task: Task(3689584644591251701, [15584102817361292984, 15229981472126021560])
    >>>
    """

    def check_and_add(set_, element):
        if element in set_:
            return False
        set_.add(element)
        return True

    pointers2hashes = {}  # To each object address, associates its hash.
    args_hashes = set()  # The hash value of each argument.
    for func, args in zip(functions, arguments):
        new_args = [(a, Argument(a)) for a in args if id(a) not in pointers2hashes]
        pointers2hashes.update({id(p): a.__hash__() for p, a in new_args})
        new_args = [a for _, a in new_args if check_and_add(args_hashes, a.__hash__())]

        new_func = Func(func) if id(func) not in pointers2hashes else None
        if new_func is not None:
            pointers2hashes[id(func)] = new_func.__hash__()

        new_packages = new_args if new_func is None else new_args + [new_func]
        task = Task(
            func_hash=pointers2hashes[id(func)], arg_hashes=[pointers2hashes[id(a)] for a in args]
        )
        yield new_packages, task


class TasksSharer(threading.Thread):
    """
    ** Communicate packets with the local server. **

    Attributes
    ----------
    res_queue : Queue
        The FIFO queue which contains the result packets of type
        ``raisin.encapsulation.packaging.Result` in the order they arrive.
    conn : raisin.communication.abstraction.AbstractConn
        The connection that takes care of sending the work.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.encapsulation.manager import make_tasks, TasksSharer
    >>>
    >>> def f(x): return x**2
    ...
    >>> soc1, soc2 = socket.socketpair()
    >>> with Handler(SocketConn(soc1)) as hand, SocketConn(soc2) as conn:
    ...     hand.start()
    ...     tasks_generator = make_tasks((f, f), ([2], [3]))
    ...     with TasksSharer(tasks_generator, conn) as tasks_sharer:
    ...         tasks_sharer.start()
    ...         for res in tasks_sharer:
    ...             res
    ...
    Result(4)
    Result(9)
    >>>
    """

    def __init__(self, tasks_iterator, conn):
        """
        Parameters
        ----------
        tasks_iterator : iterator
            Gives for each task, the list of packages of type
            ``raisin.encapsulation.packaging.Func``
            or ``raisin.encapsulation.packaging.Argument`` and also the task to execute
            (of type ``raisin.encapsulation.packaging.Task``). For example, the generator
            ``raisin.encapsulation.manager.make_tasks`` can do the job.
        conn : raisin.communication.abstraction.AbstractConn
            A linked connection has a receiver listening.

        Notes
        -----
        - There is no verification on the inputs, they must be verified by higher level functions.
        - You have to start the thread with the *start()* method to establish
            asynchronous communication with the server.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.res_queue = queue.Queue()
        self.conn = conn
        self._tasks_iterator = tasks_iterator
        self._is_collected = False # 'True' when all the results are receved

    def __enter__(self):
        """
        ** Allows to cut the connection in case of error. **

        Instead of quitting the server without warning, this context
        manager allows you to quit the dialog cleanly.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        ** Stops and closes the dialog with the local server. **

        Goes together with ``TasksSharer.__enter__``.
        This is where you break the connection with the server.
        """
        return None

    def __iter__(self, poll_interval=0.5):
        """
        ** Yields the results as they come in. **

        Results are not necessarily assigned in the order in which they are issued.

        Parameters
        ----------
        poll_interval : float
            Interval of time in which an incident in the thread takes to get back here.

        Yields
        ------
        result : raisin.encapsulation.packaging.Result
            The result encapsulated with all its context.
        """
        while not self._is_collected or not self.res_queue.empty():
            try:
                yield self.res_queue.get(timeout=poll_interval)
            except queue.Empty as err:
                if not self.is_alive():
                    raise ConnectionError('the connection seems interrupted') from err

    def run(self):
        """
        ** Represents the thread activity. **

        This method is the first method that will be executed when the thread is launched.
        It must not be called directly. It is the call of the 'start' method which
        takes care in the background to launch this method.
        """
        nbr_tasks = 0
        for new_packages, task in self._tasks_iterator:
            for new_package in new_packages:
                send_package(self.conn, new_package)
            send_package(self.conn, task)
            nbr_tasks += 1
        while nbr_tasks > 0:
            self.res_queue.put(self.conn.recv_formatted(kind='result'))
            nbr_tasks -= 1
        self._is_collected = True
