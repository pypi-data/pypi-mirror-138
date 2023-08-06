#!/usr/bin/env python3

"""
** Manages all client/server tcp communication. **
--------------------------------------------------

This is where the main classes representing the client and the servers are defined.
The verifications and the communication protocols are also defined here.
"""

from raisin.communication.client import Client
from raisin.communication.server import Server
from raisin.doc import make_pdoc

__all__ = ['Client', 'Server']
__pdoc__ = make_pdoc(__all__, locals())
