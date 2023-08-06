#!/usr/bin/env python3

"""
** Processes requests. **
-------------------------

Whether it is a client or a server that asks for something, it doesn't change much.
In all cases it is TCP sockets that request and render services.
That's why once the communication is established,
clients and servers use the same function to communicate.
"""

import collections
import os
import platform
import sys
import threading
import uuid

from context_verbose import printer as ctp

from raisin.encapsulation.packaging import Argument, Func, Task, Result
from raisin.communication.request import send_result, send_welcome, shut_rdwr


__pdoc__ = {
    'Handler.__enter__': True,
    'Handler.__exit__': True,
}


def get_self_identity(cls=False):
    """
    ** Recover the identity of this program. **

    The values are returned through an *namedtuple*.

    Paremeters
    ----------
    cls : boolean
        If True, returns the uninstantiated *Identity* class.

    Returns
    -------
    mac : str
        The mac address of the PC.
    username : str
        The username of the user who runs this program.
    version : str
        The version of python.
    admin : boolean
        True if this script is run as administrator, False if the rights are restricted.
    platform : str
        The general name of the operating system.

    Examples
    --------
    >>> from raisin.communication.handler import get_self_identity
    >>> get_self_identity(cls=True)
    <class 'raisin.communication.handler.Identity'>
    >>> identity = get_self_identity()
    >>> identity # doctest: +SKIP
    Identity(mac='fd:86:63:3e:c8:fd', username='robin', version='3.8.10', admin=False, os='linux')
    >>>
    """
    Identity = collections.namedtuple('Identity', ['mac', 'username', 'version', 'admin', 'os'])
    if cls:
        return Identity

    mac = ':'.join([f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 8*6, 8)][::-1])
    try:
        username = os.environ['USERNAME']
    except KeyError:
        username = os.path.basename(os.path.expanduser('~'))
    version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        except PermissionError:
            admin = False
        else:
            admin = True
    else:
        admin = ('SUDO_USER' in os.environ and os.geteuid() == 0)
    os_ = platform.system().lower()

    return Identity(mac, username, version, admin, os_)


class Handler(threading.Thread):
    """
    ** Helps a socket to communicate. **

    Attributes
    ----------
    conn : raisin.communication.abstraction.AbstractConn
        The abstract connection that allows communication.
    """

    def __init__(self, conn):
        """
        Parameters
        ----------
        conn : raisin.communication.abstraction.AbstractConn
            An entity able to communicate.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn = conn

        self._args = {}
        self._func = {}

    def run(self):
        """
        ** Wait for the requests to answer them. **

        This method must be launched asynchronously by invoking the *start* method.
        It listens for the arrival of a request through the 'conn' attribute.
        As soon as a request arrives, it is processed. Once the request is processed,
        this method starts listening for the next request.
        """
        with ctp(f'Listening to the {self.conn} connection...'):
            send_welcome(self.conn)
            self.conn.is_welcomed = True
            while True:
                try:
                    ask, context = self.conn.recv_formatted(
                        kind={'request', 'package', 'signal'},
                        get_context=True,
                    )
                except ConnectionResetError:
                    break

                ctp.print(f'ask: {ask}')
                ctp.print(f'context: {context}')

                if context.kind == 'signal' and ask == 'shut_rdwr':
                    with ctp('Shutdown itself...'):
                        self.handler_close()
                        break
                if ask == 'hello':
                    with ctp('Courteous answer...'):
                        self.conn.send_formatted(
                            'hello',
                            kind='answer',
                            signature=context.signature
                    )
                elif ask == 'id':
                    with ctp('Sending the local identity...'):
                        self.conn.send_formatted(
                            get_self_identity(),
                            kind='answer',
                            signature=context.signature,
                        )
                elif isinstance(ask, Argument):
                    with ctp('Memorization of the argument...'):
                        self._args[ask.__hash__()] = ask
                elif isinstance(ask, Func):
                    with ctp('Memorization of the function...'):
                        self._func[ask.__hash__()] = ask
                elif isinstance(ask, Task):
                    with ctp('Preparation of an environment for the task...'):
                        # TODO : s'assurer qu'il y ai les arguments et la fonction dispo
                        func = self._func[ask.func_hash]
                        args = [self._args[arg_hash].get_value() for arg_hash in ask.arg_hashes]
                        # TODO : calculer le resultat dans un autre processus
                        res = Result(func(*args))
                        send_result(self.conn, res)

                else:
                    raise NotImplementedError(f"impossible to process {ask}, it's not coded")

    def handler_close(self):
        """
        ** Clean up the connection. **
        """
        # shut_rdwr(self.conn)
        self.conn.close()

    def __enter__(self):
        """
        ** Allows to manage the closure through a context manager. **
        """
        return self

    def __exit__(self, exc_type, value, traceback):
        """
        ** Guaranteed that the connection closes in all cases. **
        """
        self.handler_close()
