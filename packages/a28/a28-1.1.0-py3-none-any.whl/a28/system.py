"""Manage actions relating to the system running area28.

The actions provided by the system module adds the ability to manage the state
of the computer system running Area28 allowing for developers to maintain the
configuration and paths of the system.
"""
import os
import shutil
from argparse import Namespace, _SubParsersAction
from a28 import utils


def cli_options(mainparser: _SubParsersAction) -> None:
    """System subcommand arguments.

    Define the arguments that the system subcommand can accept. The system
    subcommand supports the following commands:

    clean: Clean all files from the current system.
    exists: Return if the system currently contains a configuration.
    path: Return the current system configuration path.
    """
    parser = mainparser.add_parser(
        'system',
        aliases=['sys'],
        help='system actions'
    )
    subparser = parser.add_subparsers(
        dest='system',
        required=True,
        help='system',
    )
    parser.add_argument(
        '-p',
        '--path',
        default=utils.get_current_config_dir(),
        help='configuration path.',
    )
    parser_exist = subparser.add_parser(
        'exists',
        help='check if the system configuration exists.',
    )
    parser_exist.set_defaults(func=exists)
    parser_clean = subparser.add_parser(
        'clean',
        help='clean (delete) the configuration permanently.',
    )
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force the configuration to be removed bypassing confirmation',
    )
    parser_path = subparser.add_parser(
        'path',
        help='return the location of the configuration path.',
    )
    parser_path.set_defaults(func=path)
    parser_path.add_argument(
        '-m',
        '--minimal',
        action='store_true',
        help='return a minimal version of the path to use in scripts',
    )
    parser_stage = subparser.add_parser(
        'stage',
        help='set the stage of current configuration'
    )
    parser_stage.set_defaults(func=stage)
    parser_stage.add_argument(
        '-s',
        '--stage',
        dest='stage',
        required=True,
        default='prod',
        choices=['prod', 'staging', 'dev'],
        help='switch staging mode'
    )


def clean(args: Namespace) -> None:
    """Clean all the configuration files relating to Area28.

    Using the shutil utilities, delete all the files provided in the STORAGE
    directory. If an error occurs, catch the exception and print it out to the
    STDOUT.

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    message = f'Delete ALL configuration data from "{args.path}"? y/n?'
    if not os.path.isdir(args.path):
        utils.message(f'No configuration to clean at "{args.path}".')
        raise FileNotFoundError

    elif not args.force and not utils.confirm(message):
        utils.message(f'Not deleting {args.path}')
        return

    try:
        shutil.rmtree(args.path)
        utils.message(f'Deleted all files and directories in {args.path}')
    except OSError as e:
        utils.message(f'Error: {args.path} : {e.strerror}')
        raise


def exists(args: Namespace) -> None:
    """Check if the configuration directory exists.

    Using the path provided in the arguments, check if the configuration path
    exists. If no path is provided, the default path defined in the system
    utility is used.

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    if os.path.isdir(args.path):
        utils.message(f'Configuration exists at "{args.path}".')
    else:
        utils.message(f'No configuration exists at "{args.path}".')


def path(args: Namespace) -> None:
    """Print the path of the system configuration.

    Print the path currently used to store the system configuration files. If
    the path option is provided in the ArgParse Namespace, the provided path
    will be returned.

    If the minimal ArgParse namespace is provided and set to boolean True, the
    output will be reduced to only the path.

    It does NOT change the configuration path

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    if args.minimal:
        utils.message(f'{args.path}')
    else:
        utils.message(f'Configuration path set to "{args.path}".')


def stage(args: Namespace) -> None:
    """Set the stage of the environment configuration.

    record the current stage at command line setting file in default path
    Get current config dir/path in utils.py would return the value accordingly

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    devkit_settings = utils.get_devkit_settings()
    devkit_settings['current_stage'] = args.stage
    utils.save_devkit_settings(devkit_settings)
    utils.message(f'Current stage set to {args.stage}')
