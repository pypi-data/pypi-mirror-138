import contextlib
from io import StringIO
from a28 import __version__
from a28.cli import main


def test_a28_no_param():
    temp_stdout = StringIO()

    try:
        with contextlib.redirect_stderr(temp_stdout):
            main()
    except SystemExit as err:
        assert err.code == 2

    assert temp_stdout.getvalue().strip().splitlines()[
               0] == 'usage: a28 [-h] [-v] {api,package,pkg,system,sys,account} ...'


def test_a28_version_param():
    temp_stdout = StringIO()

    try:
        with contextlib.redirect_stdout(temp_stdout):
            main(['-v'])
    except SystemExit as err:
        assert err.code == 0

    assert temp_stdout.getvalue().strip() == f'a28 version {__version__}'


def test_a28_system_exit_on_exception():
    """command line call that fail would trigger a system exit with code other than 0"""
    try:
        main(['account', 'authenticate', '-u', 'joe@example.com', '-p', '234'])
    except SystemExit as err:
        assert err.code != 0
    else:
        assert False
