"""The purpose of the code is to give two methods a unit test to make sure that they are working properly"""
from slogpy.slog import Slog as slog  # noqa: N813


def setup_function():
    """set the Default to no log file, since only interested in console output"""
    slog.initialize(file_logging=False)

def test_info_console_output(capsys, msg="This is a console test"):
    """Simple test for console output

    Given:Using slogpy
    When: Using info() with a String
    Then: Contents of String shows up in stdout AND nothing in stderr
    """
    slog.info(msg)
    expected_content = f"{msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

def test_debug_console_output(capsys, msg=""):
    """Given:Using slogpy

    When: Using debug() with a String

    Then: Contents of String shows up in stdout AND nothing in stderr

    """
    slog.debug(msg)
    expected_content = ""
    # not sure this line of code is necessary or not. since this won't be any content in the console.
    out, _ = capsys.readouterr()
    assert expected_content == ""
