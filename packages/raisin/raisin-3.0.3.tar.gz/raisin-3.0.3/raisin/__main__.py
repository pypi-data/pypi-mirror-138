#!/usr/bin/env python3

"""
** Allows to use *raisin* in command line. **
---------------------------------------------

- general options :
    - make verbose : ``python -m raisin -vv``
    - get the raisin's version : ``python -m raisin --version``
    - return the result rather than display it : ``python -m raisin --returns``
- install raisin : ``python -m raisin install``
    - install only configuration file : ``python -m raisin install --config_only``
- uninstall raisin : ``python -m raisin uninstall``
    - uninstall only configuration file : ``python -m raisin uninstall --config_only``
- launch the server : ``python -m raisin server``
    - specify port : ``python -m raisin server -p 20001``
- change values in the configuration file :
    - change the port : ``python -m raisin set port 20001``
    - change the verbosity : ``python -m raisin set verbosity 0``
- see all parameters of the configuration file : ``python -m raisin get``
    - see the default port : ``python -m raisin get --parameters port``
    - see the default verbosity level : ``python -m raisin get --parameters verbosity``
"""


import argparse
import pprint
import sys

from context_verbose import printer as ctp

from raisin.application import config_file
from raisin.application.install import install_app
from raisin.application.uninstall import uninstall_app
from raisin.communication.server import Server
from raisin import __version__ as VERSION

# main functions

def parse():
    """
    ** Does the parsing of the arguments. **
    """
    parser = argparse.ArgumentParser(description='simple raisin API')

    # general options
    subparsers = parser.add_subparsers(dest='parser_name')
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        default=0,
        help="increases code verbosity, the more v's there are, the more verbose the program is"
    )
    parser.add_argument(
        '--version',
        action='store_true',
        default=False,
        help='returns the version and exists')
    parser.add_argument(
        '--returns',
        '-r',
        action='store_true',
        default=False,
        help='makes silent, takes over -v'
    )

    # installation
    install_parser = subparsers.add_parser('install', help='installs the raisin application')
    install_parser.add_argument(
        '--config_only',
        action='store_true',
        default=False,
        help='installs only the configuration file'
    )

    # uninstallation
    uninstall_parser = subparsers.add_parser('uninstall', help='uninstalls the raisin application')
    uninstall_parser.add_argument(
        '--config_only',
        action='store_true',
        default=False,
        help='uninstalls only the configuration file'
    )

    # lunch server
    server_parser = subparsers.add_parser('server', help='launch tasks in background')
    server_parser.add_argument(
        '--port',
        '-p',
        default=config_file['port'],
        type=int,
        help=(f'the listening port, the default value ({config_file["port"]}) '
               'comes from the configuration file')
    )

    # change the configuration
    set_parser = subparsers.add_parser('set', help='change the default values')
    set_parser.add_argument(
        'parameter',
        choices=list(config_file),
        help='the name of the parameter to be changed')
    set_parser.add_argument('value', type=str, help='the new value of the parameter')

    # get the configuration
    get_parser = subparsers.add_parser('get', help='retrieve parameter values')
    get_parser.add_argument(
        '--parameters',
        '--params',
        '-p',
        choices=list(config_file),
        nargs='*',
        help='the name of the parameter to retrieve, by default, all parameters are read'
        )
    return parser

def catch_result(func):
    """
    ** Decorator that transforms python output to bash output. **

    - If the function raises an exception, returns a non-zero
        integer that corresponds the error code.
    - If the function does not raise an exception, the decorated function returns 0.
        Otherwise it returns 1 if an error has occurred.
    - Only catches errors derived from *Exception*, not *BaseException*.
    - If the function returns something other than None,
        the output is intercepted and displayed in the stdout.

    Parameters
    ----------
    func : callable
        The function to decorate.

    Returns
    -------
    decorated_func : callable
        The decorate function which performs the same thing but can
        handle exceptions and output value differently.

    Examples
    --------
    >>> from raisin.__main__ import catch_result
    >>> @catch_result
    ... def func(x):
    ...     return 1/x
    ...
    >>> func(0)
    ZeroDivisionError(division by zero)
    1
    >>> func(2)
    0.5
    0
    >>>
    """

    def fonc_dec(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as err:
            print(f'{err.__class__.__name__}({err})')
            return 1
        else:
            if res is not None:
                pprint.pprint(res)
            return 0

    return fonc_dec

def main(args_list=None):
    """
    ** Interprets the commands. **

    Allows you to use *raisin* on the command line.

    Parameters
    ----------
    args : list
        The list of arguments provided.

    Returns
    -------
    func_out
        The output of the called functions.
    """

    def run(args):
        if args.version:
            return VERSION
        func = globals().get(f'_parse_{args.parser_name}')
        if func is None:
            raise SyntaxError(
                f"invalid argument, for more information run '{sys.executable} -m raisin --help'"
            )
        return func(args)

    # arguments parsing
    parser = parse()
    if args_list is not None:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()
    if args.verbose:
        ctp.set_max_depth(args.verbose)
    return(run if args.returns else catch_result(run))(args)


# utilities functions

def _parse_install(args):
    return install_app(config_only=args.config_only)

def _parse_uninstall(args):
    return uninstall_app(config_only=args.config_only)

def _parse_server(args):
    with Server(args.port) as server:
        return server.serve_forever()

def _parse_set(args):
    config_file[args.parameter] = args.value

def _parse_get(args):
    parameters = args.parameters
    if not parameters:
        parameters = list(config_file)
    values = {parameter: config_file[parameter] for parameter in parameters}
    if len(values) == 1:
        return list(values.values()).pop()
    return values

if __name__ == '__main__':
    main()
