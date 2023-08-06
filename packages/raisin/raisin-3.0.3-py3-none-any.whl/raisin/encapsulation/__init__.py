#!/usr/bin/env python3

"""
** Used to encapsulate packets before sending them. **
------------------------------------------------------

In particular, when the user wants to execute several tasks through a network,
they are split into small packets. These packets are made up of the function
and the arguments specific to each task.
"""

from raisin.encapsulation.packaging import Argument, Func, Result, Task
from raisin.encapsulation.manager import make_tasks, TasksSharer
from raisin.doc import make_pdoc


__all__ = ['Argument', 'Func', 'Result', 'Task', 'make_tasks', 'TasksSharer']
__pdoc__ = make_pdoc(__all__, locals())
