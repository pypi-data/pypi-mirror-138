#!/usr/bin/env python3

"""
** Simplifies the API to create simple functions. **
----------------------------------------------------
"""

import itertools

from raisin.application import config_file
from raisin.encapsulation.manager import make_tasks, TasksSharer
from raisin.communication.client import Client


def imap_unordered(func, iterable, *, context=False):
    """
    ** Apply the arguments to the function. **

    Parameters
    ----------
    func : callable
        A function that takes a single argument.
    iterable : iterable
        The iterable that assigns each argument that
        will be applied to the *func* function.
    context : boolean, default=False
        If True returns not the value of the result but a
        ``raisin.encapsulation.packaging.Result`` object
        that contains the context information of the result.

    Yields
    ------
    res
        The result of the function for each argument.
    """
    tasks_generator = make_tasks(itertools.cycle([func]), ([arg] for arg in iterable))
    with Client(None, config_file['port']) as client:
        client.start()
        client.wait_ready()
        with TasksSharer(tasks_generator, client) as tasks_sharer:
            # tasks_sharer.start()
            tasks_sharer.run()
            if context:
                yield from tasks_sharer
            else:
                yield from (res.get_value() for res in tasks_sharer)
