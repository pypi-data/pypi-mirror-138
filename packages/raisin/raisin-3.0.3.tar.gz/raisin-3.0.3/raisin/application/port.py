#!/usr/bin/env python3

"""
** Manages the reading, writing and verification of the port. **

The port considered is the listening port of the *raisin* server.
The accessors to the port are used in ``raisin.application.configuration.ConfigFile``.
"""

import re


DEFAULT_PORT = 20001


def _get_candidates(file_content):
    pattern = re.compile(r"""
        (?<!\S)
        port (?:[\s:=])*
        (?P<port>[0-9]+ (?:_[0-9]+)*)""",
        re.VERBOSE | re.IGNORECASE
    )
    return [
        match for match in re.finditer(pattern, file_content)
        if '#' not in file_content[:match.start()].split('\n')[-1]
        and 1 <= int(match['port']) <= 65535
    ]

def get_port(file_content=None):
    r"""
    ** Recover the value of the default port. **

    Parameters
    ----------
    file_content : str
        The contents of the configuration file.
        If not provided, the default value of the port is returned.

    Returns
    -------
    int
        The value of the port.

    Raises
    ------
    SyntaxeError
        If the port is misdetected.

    Examples
    --------
    >>> from raisin.application.port import get_port
    >>> get_port('port 20001')
    20001
    >>> get_port('PORT 20001')
    20001
    >>> get_port('port20001')
    20001
    >>> get_port('port:20001')
    20001
    >>> get_port('port=20001')
    20001
    >>> get_port('port: 20001')
    20001
    >>> get_port('port = 20001')
    20001
    >>> get_port('\tport = 20001')
    20001
    >>> get_port('port\n\t20001')
    20001
    >>> get_port('port=20001\nport=123456789')
    20001
    >>> get_port('port=20001 # port=8080')
    20001
    >>> get_port('port=20001\npassport=8080')
    20001
    >>>
    """
    if file_content is None:
        return DEFAULT_PORT
    candidates = {int(match['port']) for match in _get_candidates(file_content)}
    if len(candidates) > 1:
        raise SyntaxError(
            'the value of the port is ambiguous, '
            f'{" and ".join(map(str, candidates))} seem possible'
        )
    if not candidates:
        raise SyntaxError('no port detected')
    return candidates.pop()

def set_port(port=DEFAULT_PORT, file_content=None):
    """
    ** Updates the value of the new port in the configuration file. **

    Parameters
    ----------
    port : int
        The new value of the port.
    file_content : str
        The file where you have to change the value of the port.
        If the file is not provided or the port is not found in the file,
        a new line is added.

    Returns
    -------
    new_content : str
        The new content of the file with the updated port.

    Examples
    --------
    >>> from raisin.application.port import set_port
    >>> set_port(port=20001, file_content='port 8080')
    'port 20001'
    >>> set_port(port=20001, file_content='port 8080 # comment')
    'port 20001 # comment'
    >>> set_port(port=20001, file_content='port 8080, port 22')
    'port 20001, port 20001'
    >>> set_port(port=20001, file_content='port 8080 # port 22')
    'port 20001 # port 22'
    >>>
    """
    if file_content is None:
        file_content = ''
    candidates = _get_candidates(file_content)
    if not candidates:
        file_content += (
            '# This is the port on which the server will be listening,\n'
            f'# by default, it is {DEFAULT_PORT}.\n'
            '# If you change it, make sure it is not taken by another application.\n'
            f'port = {port}\n'
        )
        return file_content
    candidates = [match for match in candidates if int(match['port']) != port]
    if not candidates:
        return file_content
    start, end = candidates.pop(0).span('port')
    file_content = file_content[:start] + str(port) + file_content[end:]
    if len(candidates):
        return set_port(port=port, file_content=file_content)
    return file_content
