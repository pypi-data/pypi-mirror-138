#!/usr/bin/env python3

"""
** Forms the packages. **
-------------------------

Allows to generate packages.
"""

import threading

from context_verbose import printer as ctp

from raisin.encapsulation.packaging import Argument, Func, Task
from raisin.communication.request import send_package


__pdoc__ = {
    'TasksSharer.__enter__': True,
    'TasksSharer.__exit__': True,
    'TasksSharer.__next__': True,
    'TasksSharer.__iter__': True,
}


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

    with ctp('Creation of computing tasks...'):
        pointers2hashes = {}  # To each object address, associates its hash.
        args_hashes = set()  # The hash value of each argument.
        nbr_tasks = -1
        for nbr_tasks, (func, args) in enumerate(zip(functions, arguments)):
            with ctp(f'Task associated to the func {func} and the args {args}...'):
                new_args = [(a, Argument(a)) for a in args if id(a) not in pointers2hashes]
                pointers2hashes.update({id(p): a.__hash__() for p, a in new_args})
                new_args = [a for _, a in new_args if check_and_add(args_hashes, a.__hash__())]

                new_func = Func(func) if id(func) not in pointers2hashes else None
                if new_func is not None:
                    pointers2hashes[id(func)] = new_func.__hash__()

                new_packages = new_args if new_func is None else new_args + [new_func]
                task = Task(
                    func_hash=pointers2hashes[id(func)],
                    arg_hashes=[pointers2hashes[id(a)] for a in args],
                )
                ctp.print(f'new packages : {new_packages}')
                ctp.print(f'task : {task}')
                yield new_packages, task
        ctp.print(f'{nbr_tasks+1} tasks generated')
        ctp.print(f'{len(args_hashes)} arguments generated')


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
    ...         tasks_sharer.start() # or 'tasks_sharer.run()' to wait for the end of the sending
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

        self.conn = conn
        self.tasks_iterator = tasks_iterator

        self._all_is_sent = False # becomes True as soon as all the stains have been emitted
        self._nbr_emitted_tasks = 0 # the number of tasks sent
        self._nbr_recovered_tasks = 0 # the number of tasks recovered

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

    def __next__(self):
        """
        ** Get the next result that comes in. **

        Listen to the connection and get the first result it sends.

        Returns
        -------
        result : raisin.encapsulation.packaging.Result
            The result associated with one of the sent tasks.
            The results are returned in order of arrival,
            which does not necessarily correspond to the order in which the tasks were sent.

        Raises
        ------
        IterationError
            If all the results have been collected.
        """
        if self._all_is_sent and self._nbr_recovered_tasks == self._nbr_emitted_tasks:
            raise StopIteration

        with ctp(f'Recovery of {self._nbr_recovered_tasks+1}th result...'):
            result = self.conn.recv_formatted(kind='result')
            self._nbr_recovered_tasks += 1
            ctp.print(f'recovered result: {result}')
            return result

    def __iter__(self):
        """
        ** Yields the results as they come in. **

        Yields
        ------
        result : raisin.encapsulation.packaging.Result
            Returns successively the results returned by the ``TasksSharer.__next__`` method.
        """
        return self

    def run(self):
        """
        ** Sends the work to be done. **

        This method just sends the set of arguments, functions and tasks to the connection.

        Notes
        -----
        This method does not return until all is sent.
        That's why it is possible to launch it asynchronously by invoking ``self.start()``.
        """
        with ctp('Emission of the successive tasks...'):
            for new_packages, task in self.tasks_iterator:
                for new_package in new_packages:
                    send_package(self.conn, new_package)
                send_package(self.conn, task)
                self._nbr_emitted_tasks += 1
                ctp.print(f'the {self._nbr_emitted_tasks}th task is emitted')
            self._all_is_sent = True
            ctp.print(f'the {self._nbr_emitted_tasks} tasks have been successfully sent')
