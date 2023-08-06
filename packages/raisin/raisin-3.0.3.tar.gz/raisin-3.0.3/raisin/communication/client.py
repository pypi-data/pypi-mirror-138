#!/usr/bin/env python3

"""
** Client TCP. **
-----------------

As soon as you want to connect to a server, you have
to create a client, even if it is for a small communication.
These clients are meant to be created and deleted in large numbers if needed.
"""

import socket
import threading

from raisin.communication.abstraction import SocketConn
from raisin.communication.handler import Handler


__pdoc__ = {
    'Client.__del__': True,
    'Client.__enter__': True,
    'Client.__exit__': True,
    'Client.__repr__': True,
    'Client.__str__': True
}


class BaseClient(threading.Thread, SocketConn):
    """
    ** TCP Client. **

    This client is both able to listen in ipv4 and ipv6.

    Attributes
    ----------
    host : str
        The ip address of the connection in ipv4 or ipv6.
        It can also be a hostname or a domain name.
    port : int
        The communication port.
    tcp_socket : socket.socket
        The tcp socket which allows low level communication.
    """

    def __init__(self, host, port):
        """
        Parameters
        ----------
        ip : str
            The server address.
        port : int
            The server's listening port.

        Raises
        ------
        ConnectionError
            If we can't connect.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.host = host
        self.port = port
        self.tcp_socket = BaseClient._init_tcp_socket(self.host, self.port)
        SocketConn.__init__(self, self.tcp_socket)

    @staticmethod
    def _init_tcp_socket(host, port):
        """
        ** Help for the ``BaseServer.__init__``. **

        Paremeters
        ----------
        port : int
            The port to listen on.

        Returns
        -------
        tcp_socket : socket.socket
            The TCP socket ready to communicate.
        """
        tcp_socket = None
        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            family, socktype, proto, _, sockaddr = res
            try:
                tcp_socket = socket.socket(family, socktype, proto)
            except OSError:
                tcp_socket = None
                continue
            try:
                tcp_socket.connect(sockaddr)
            except OSError:
                tcp_socket.close()
                tcp_socket = None
                continue
            break
        if tcp_socket is None:
            raise ConnectionError('could not open socket')
        return tcp_socket

    def run(self):
        """
        ** Puts the client on asynchronous listening mode. **

        Should not be called as is. It is the call of the
        *start* method that executes run.
        """
        Handler(self).run()

    def shutdown(self):
        """
        Tell the ``BaseClient.run`` loop to stop and wait until it does.
        ``BaseClient.shutdown`` must be called while ``BaseClient.run``
        is running in a different thread otherwise it will deadlock.
        """
        self.client_close()
        while self.is_alive():
            continue

    def client_close(self):
        """
        ** Clean up the client. **

        Should not be called if the client is encapsulated
        in a context manager (*with* statement).
        Can be called several times.
        """
        self.close()


class Client(BaseClient):
    """
    ** Enables you to enrich the ``raisin.communication.client.BaseClient``. **
    """

    def __del__(self):
        """
        ** Help for the garbage-collector. **
        """
        try:
            self.client_close()
        except AttributeError:
            pass

    def __enter__(self):
        """
        ** Prepared for easy client closing. **

        Allows you to use the *with* statement which allows
        you to set up a context manager.
        """
        return self

    def __exit__(self, *_):
        """
        ** Stop the client. **

        Goes together with ``Client.__enter__``.
        """
        self.shutdown()

    def __repr__(self):
        """
        ** Gives a simple representation of the client. **
        """
        return f'Client({self.host}, {self.port})'

    def __str__(self):
        r"""
        ** Provides a complete representation of the client. **
        """
        return (
            f'TCP Client:\n'
            f'    host={self.host}\n'
            f'    port={self.port}\n'
            f'    tcp_socket={self.tcp_socket}')
