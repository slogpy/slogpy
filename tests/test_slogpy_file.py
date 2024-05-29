"""The purpose of the code is to give debug and info methods a unit test to make sure that they are working properly"""
import tempfile

from slogpy.slog import Slog as slog  # noqa: N813


def test_info_file(msg="This is a file test"):
    """Given:Using slogpy

    When: Using info() with a String

    Then: Contents of String shows up in a temp file.

    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.info(msg)
    expected_content = f"- INFO - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()

    assert expected_content in content

def test_debug_file(msg="This is a file test"):
    """Given:Using slogpy

    When: Using debug() with a String

    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr

    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.debug(msg)
    expected_content = f"- DEBUG - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content
