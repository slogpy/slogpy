"""The purpose of the code is to give all methods a unit test to make sure that they are working properly"""
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

    Then: Contents of String shows up in a file AND nothing in stdout and stderr

    """
    slog.debug(msg)
    expected_content = ""
    out, _ = capsys.readouterr()
    assert expected_content == out

def test_annoy_console_output(capsys, msg="This is a console test"):
    """Simple test for console output

    Given:Using slogpy
    When: Using annoy() with a String
    Then: Contents of String shows up in stdout AND nothing in stderr
    """
    slog.annoy(msg)
    expected_content = f"ANNOYING YOU: {msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

def test_warn_console_output(capsys, msg="This is a console test"):
    """Simple test for console output

    Given:Using slogpy
    When: Using warn() with a String
    Then: Contents of String shows up in stdout AND nothing in stderr
    """
    slog.warn(msg)
    expected_content = f"WARNING: {msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

def test_error_console_output(capsys, msg="This is a console test"):
    """Simple test for console output

    Given:Using slogpy
    When: Using error() with a String
    Then: Contents of String shows up in stdout AND nothing in stderr
    """
    slog.error(msg)
    expected_content = f"ERROR: {msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

def test_fatal_console_output(capsys, msg="This is a console test"):
    """Simple test for console output

    Given:Using slogpy
    When: Using info() with a String
    Then: Contents of String shows up in stdout AND nothing in stderr
    """
    slog.fatal(msg)
    expected_content = f"FATAL: {msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out
