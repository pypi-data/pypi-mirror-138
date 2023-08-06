#!/usr/bin/env python3

"""
** Manages the reading, writing and verification of the verbosity level. **

The level of verbosity allows you to mute or display with more or less detail
the operations that *raisin* is performing.
The accessors to the verbosity are used in ``raisin.application.configuration.ConfigFile``.
"""

import re


DEFAULT_VERBOSITY = 0


def _get_candidates(file_content):
    pattern = re.compile(r"""
        (?<!\S)
        (?:verbosity|verbose)
        (?:[\s:=])*
        (?P<level>
            [0-9]+ (?:_[0-9]+)*
          | (?<!\S)true
          | (?<!\S)false
        )""",
        re.VERBOSE | re.IGNORECASE
    )
    return [
        match for match in re.finditer(pattern, file_content)
        if '#' not in file_content[:match.start()].split('\n')[-1]
    ]

def get_verbosity(file_content=None):
    r"""
    ** Recover the value of the default verbosity level. **

    Parameters
    ----------
    file_content : str
        The contents of the configuration file.
        If not provided, the default value of the verbosity is returned.

    Returns
    -------
    int
        The value of verbosity level. 0 allows to be mute,
        the higher the number, the more caustic *raisin* will be.

    Raises
    ------
    SyntaxeError
        If the verbosity is misdetected.

    Examples
    --------
    >>> from raisin.application.verbosity import get_verbosity
    >>> get_verbosity('verbosity 0')
    0
    >>> get_verbosity('verbose 0')
    0
    >>> get_verbosity('VERBOSITY 0')
    0
    >>> get_verbosity('verbosity false')
    0
    >>> get_verbosity('verbosity true')
    1
    >>> get_verbosity('verbosity 2')
    2
    >>> get_verbosity('verbosity 10')
    10
    >>> get_verbosity('verbosity0')
    0
    >>> get_verbosity('verbosity:0')
    0
    >>> get_verbosity('verbosity=0')
    0
    >>> get_verbosity('verbosity: 0')
    0
    >>> get_verbosity('verbosity = 0')
    0
    >>> get_verbosity('\tverbosity = 0')
    0
    >>> get_verbosity('verbosity\n\t0')
    0
    >>> get_verbosity('verbosity=0 # verbosity=1')
    0
    >>> get_verbosity('verbosity=0\nholaverbosity=1')
    0
    >>>
    """
    if file_content is None:
        return DEFAULT_VERBOSITY
    candidates = {
        int(match['level']) if match['level'].isdigit() else {'true': 1, 'false': 0}[match['level']]
        for match in _get_candidates(file_content)}
    if len(candidates) > 1:
        raise SyntaxError(
            'the value of the verbosity level is ambiguous, '
            f'{" and ".join(map(str, candidates))} seem possible'
        )
    if not candidates:
        raise SyntaxError('no verbosity level detected')
    return candidates.pop()

def set_verbosity(verbosity=DEFAULT_VERBOSITY, file_content=None):
    """
    ** Updates the value of the new verbosity level in the configuration file. **

    Parameters
    ----------
    verbosity : int or boolean
        The new value of the verbosity.
    file_content : str
        The file where you have to change the value of the verbosity.
        If the file is not provided or the verbosity is not found in the file,
        a new line is added.

    Returns
    -------
    new_content : str
        The new content of the file with the updated verbosity.

    Examples
    --------
    >>> from raisin.application.verbosity import set_verbosity
    >>> set_verbosity(verbosity=1, file_content='verbosity 0')
    'verbosity 1'
    >>> set_verbosity(verbosity=1, file_content='verbosity false')
    'verbosity 1'
    >>> set_verbosity(verbosity=1, file_content='verbosity true')
    'verbosity 1'
    >>> set_verbosity(verbosity=True, file_content='verbosity 0')
    'verbosity true'
    >>> set_verbosity(verbosity=1, file_content='verbose 0')
    'verbose 1'
    >>> set_verbosity(verbosity=1, file_content='verbosity false # comment')
    'verbosity 1 # comment'
    >>> set_verbosity(verbosity=1, file_content='verbosity false, verbosity 2')
    'verbosity 1, verbosity 1'
    >>> set_verbosity(verbosity=1, file_content='verbosity false # verbosity 2')
    'verbosity 1 # verbosity 2'
    >>>
    """
    if file_content is None:
        file_content = ''
    candidates = _get_candidates(file_content)
    if not candidates:
        file_content += (
            "# This value allows to make 'grape' silent so as not to pollute 'stdout'.\n"
            "# But if you want, it is also possible to make 'grape' verbose, \n"
            "# either for debugging or to have an idea of the state of the current calculations.\n"
            "The display is managed by the 'context-verbose' module, so the value provided is the\n"
            "maximum depth of nested sections. The value '0' or 'false' makes 'raisin' mute.\n"
            "The values '1', 'true', '2', '3', ... 'n' allow it on the contrary to be verbose.\n"
            f'verbosity = {str(verbosity).lower()}\n'
        )
        return file_content
    candidates = [
        match for match in candidates
        if str(match['level']).lower() != str(verbosity).lower()
    ]
    if not candidates:
        return file_content
    start, end = candidates.pop(0).span('level')
    file_content = file_content[:start] + str(verbosity).lower() + file_content[end:]
    if len(candidates):
        return set_verbosity(verbosity=verbosity, file_content=file_content)
    return file_content
