#!/usr/bin/env python3

"""
** Allows for extensive testing around communication. **
--------------------------------------------------------
"""

import socket
import threading
import time
import uuid

import pytest

from raisin.communication.abstraction import SocketConn
from raisin.communication.server import Server
from raisin.communication.client import Client
from raisin.communication.request import hello, get_identity
from raisin.communication.handler import get_self_identity


def test_socket_abstraction_conn():
    """
    ** Tests all fonctions of the abstraction. **
    """
    socket1, socket2 = socket.socketpair()
    abstraction1, abstraction2 = SocketConn(socket1), SocketConn(socket2)

    abstraction1.send((b'mes', b'sage1',))
    abstraction2.send((b'hello',))
    abstraction2.send((b'',))
    abstraction1.send((b'message2',))
    assert b''.join(abstraction2.recv()) == b'message1'
    assert b''.join(abstraction2.recv()) == b'message2'
    assert b''.join(abstraction1.recv()) == b'hello'
    assert b''.join(abstraction1.recv()) == b''

    abstraction1.send_obj(0)
    abstraction1.send_obj(1)
    abstraction2.send_obj(2)
    abstraction2.send_obj(3)
    assert abstraction1.recv_obj() == 2
    assert abstraction1.recv_obj() == 3
    assert abstraction2.recv_obj() == 0
    assert abstraction2.recv_obj() == 1

    abstraction1.close()
    abstraction2.close()

def test_formatted():
    """
    ** Verifies that the threads do not mix up the packages. **
    """
    def send_and_recv(conn1, conn2):
        """ Designed to be executed multiple times from multiple threads. """
        for _ in range(10):
            signature = uuid.uuid4().bytes
            content = uuid.uuid4().bytes
            conn1.send_formatted(content, kind='answer', signature=signature)
            assert conn2.recv_formatted(signature=signature) == content

    socket1, socket2 = socket.socketpair()
    with SocketConn(socket1) as conn1, SocketConn(socket2) as conn2:
        threads = [threading.Thread(target=send_and_recv, args=(conn1, conn2)) for _ in range(16)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

def test_simple_server():
    """
    ** Tries to launch a simple server. **
    """
    with Server(9999) as server:
        server.start() # the server is listening
        server.wait_ready()
        server.shutdown() # stops the server

def test_client_interface():
    """
    ** Performs several tests on the client interface. **
    """
    with Server(9999) as server:
        server.start()
        server.wait_ready()
        with Client(None, 9999) as client:
            client.start()
            client.wait_ready()
            assert hello(client) == 'hello'
            assert get_identity(client) == get_self_identity()
            assert client.get_conn_identities() == {None}

def test_server_interface():
    """
    ** Performs several tests on the server interface. **
    """
    with Server(9999) as server:
        server.start()
        server.wait_ready()
        assert server.get_conn_identities() == set()
        with Client(None, 9999) as client:
            client.start()
            client.wait_ready()
            assert server.get_conn_identities() == {get_self_identity()}

def test_malfunctioning():
    """
    ** Tests the exception management in case of abnormal behavior. **
    """
    soc1, soc2 = socket.socketpair()
    with SocketConn(soc1) as con1, SocketConn(soc2):
        with pytest.raises(KeyError):
            con1.recv_obj(dest='unassigned address')
        with pytest.raises(KeyError):
            con1.send_obj(None, dest='unassigned address')
    with pytest.raises(ConnectionError):
        Client(None, 9999)

@pytest.mark.slow
def test_timeout():
    """
    ** Tests the exception management in case of abnormal behavior. **
    """
    with Server(9999) as serv:
        with Client(None, 9999) as client:
            with pytest.raises(TimeoutError):
                hello(client, timeout=2)
            serv.start()
            time.sleep(2)
            client.start()
            time.sleep(2)
            hello(client, timeout=2)
