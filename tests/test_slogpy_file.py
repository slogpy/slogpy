"""The purpose of the code is to give all methods a unit test to make sure that they are working properly"""
import tempfile

from slogpy.slog import Slog as slog  # noqa: N813


def test_info_file(msg="This is a test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using info() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.info(msg)
    expected_content = f"- INFO - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()

    assert expected_content in content

def test_debug_file(msg="This is a file test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using debug() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.debug(msg)
    expected_content = f"- DEBUG - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content

def test_annoy_file(msg="This is a file test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using annoy() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.annoy(msg)
    expected_content = f"- INFO - ANNOYING YOU: {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content


def test_warn_file(msg="This is a file test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using warn() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.warn(msg)
    expected_content = f"- WARNING - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content

def test_error_file(msg="This is a file test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using error() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.error(msg)
    expected_content = f"- ERROR - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content


def test_fatal_file(msg="This is a file test"):
    """Simple test for files output

    Given:Using slogpy
    When: Using fatal() with a String
    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr
    """
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.fatal(msg)
    expected_content = f"- CRITICAL - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content
