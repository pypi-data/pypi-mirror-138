#!/usr/bin/env python3

"""
** Establishes small communications. **
---------------------------------------

Allows via ``raisin.communication.abstraction.SelectiveConn``,
to take small requests or short exchanges.
The connection must in most cases be connected to another listening connection.
That is, indirectly connected to a ``raisin.communication.handler.Handler``.
"""

import uuid


def get_identity(conn, **kwargs):
    """
    ** Recover the identity of the connection. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.dialog`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.communication.request import get_identity
    >>>
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     identity = get_identity(conn)
    ...
    >>> identity # doctest: +SKIP
    Identity(mac='fd:86:63:3e:c8:fd', username='robin', version='3.6.15', admin=False, os='linux')
    >>>
    """
    return conn.dialog('id', **kwargs)


def hello(conn, **kwargs):
    """
    ** Sends a 'hello' and expects a 'hello' in return. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.dialog`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.communication.request import hello
    >>>
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     hello(conn)
    ...
    'hello'
    >>>
    """
    return conn.dialog('hello', **kwargs)


def send_package(conn, package, **kwargs):
    """
    ** Sends an ``raisin.encapsulation.packaging.Package``. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    package : raisin.encapsulation.packaging.Package
        A package that allows to contribute to the execution of a task.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.send_formatted`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.encapsulation.packaging import Argument
    >>> from raisin.communication.request import send_package
    >>>
    >>> arg = Argument(0)
    >>> soc, _ = socket.socketpair()
    >>> with SocketConn(soc) as conn:
    ...     send_package(conn, arg)
    ...
    >>>
    """
    conn.send_formatted(package, kind='package', **kwargs)


def send_result(conn, result, **kwargs):
    """
    ** Sends an ``raisin.encapsulation.packaging.Result``. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    result : raisin.encapsulation.packaging.Result
        The result of the task.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.send_formatted`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.encapsulation.packaging import Result
    >>> from raisin.communication.request import send_result
    >>>
    >>> res = Result(0)
    >>> soc, _ = socket.socketpair()
    >>> with SocketConn(soc) as conn:
    ...     send_result(conn, res)
    ...
    >>>
    """
    conn.send_formatted(result, kind='result', **kwargs)


def send_welcome(conn, message='I am at your disposal!', **kwargs):
    """
    ** Sends welcome message. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    message : str
        The greeting message.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.send_formatted`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.request import send_welcome
    >>>
    >>> soc, _ = socket.socketpair()
    >>> with SocketConn(soc) as conn:
    ...     send_welcome(conn)
    ...
    >>>
    """
    conn.send_formatted(message, kind='welcome', **kwargs)


def shut_rdwr(conn, **kwargs):
    """
    ** Informs the peer that the call is ending. **

    Parameters
    ----------
    conn : raisin.communication.abstraction.SelectiveConn
        A connection to a ``raisin.communication.handler.Handler``.
    **kwargs : dict
        The parameters directly transmitted to the
        ``raisin.communication.abstraction.SelectiveConn.send_formatted`` method.

    Examples
    --------
    >>> import socket
    >>> from raisin.communication.abstraction import SocketConn
    >>> from raisin.communication.handler import Handler
    >>> from raisin.communication.request import shut_rdwr
    >>>
    >>> soc1, soc2 = socket.socketpair()
    >>> with SocketConn(soc1) as conn, Handler(SocketConn(soc2)) as handler:
    ...     handler.start()
    ...     shut_rdwr(conn)
    ...     handler.join()
    ...
    >>>
    """
    signature = kwargs.get('signature', None)
    if signature is None:
        signature = uuid.uuid4().bytes
    try:
        conn.send_formatted('shut_rdwr', kind='signal', **kwargs)
    except ConnectionError:
        pass
