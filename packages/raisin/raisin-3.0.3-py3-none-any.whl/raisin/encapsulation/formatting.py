#!/usr/bin/env python3

"""
** Adds information and makes verifications. **
-----------------------------------------------

This module provides 2 functions. It allows to encapsulate requests
in order to add information about its function.
But it also allows to make verification at the time of the reception.
"""

import collections

KIND2COMPACT = {
    'request': b'\x00',
    'answer': b'\x01',
    'package': b'\x02',
    'result': b'\x03',
    'welcome': b'\x04',
    'signal': b'\x05',
}
COMPACT2KIND = {value: key for key, value in KIND2COMPACT.items()}


def format_package(content, kind, signature=None):
    """
    ** Allows you to send information by indicating its nature. **

    Parameters
    ----------
    content
        The content of the message, an object of any kind.
    kind : str
        The kind of content :

        - *request* : To ask a question.
        - *answer* : For the results of a request.
    signature : bytes, optional
        A unique identifier to direct the message to the right place upon reception.
        It can for example be issued from the function ``uuid.uuid4().bytes``.

    Raises
    ------
    ValueError
        If *kind* is not one of the possible choices.

    Returns
    -------
    message : tuple
        The request encapsulated in a context.
    """
    try:
        compact_kind = KIND2COMPACT[kind]
    except KeyError as err:
        raise ValueError(
            f"'kind' can only take the values {tuple(KIND2COMPACT)}, "
            f'but this value is {kind}'
            ) from err
    if signature is None:
        return (content, compact_kind)
    return (content, compact_kind, signature)

def unpack_message(message):
    """
    ** Allows to separate the message from the context. **

    Does not check the formatting of the message.

    Parameters
    ----------
    message : tuple
        The request encapsulated in a context,
        indirectly from the ``format_package`` function.

    Returns
    -------
    content
        The content of the sent message.
    context : namedtuple
        Contains the context of the object.

    Examples
    --------
    >>> from raisin.encapsulation.formatting import format_package, unpack_message
    >>> unpack_message(format_package('question', 'request'))
    ('question', context(kind='request', signature=None))
    >>> unpack_message(format_package('response', 'answer'))
    ('response', context(kind='answer', signature=None))
    >>> unpack_message(format_package('response', 'answer', signature=b'abcdefg'))
    ('response', context(kind='answer', signature=b'abcdefg'))
    >>>
    """
    content, compact_kind, *signature = message
    kind = COMPACT2KIND[compact_kind]
    Context = collections.namedtuple('context', ['kind', 'signature'])
    if signature:
        return content, Context(kind, signature[0])
    return content, Context(kind, None)
