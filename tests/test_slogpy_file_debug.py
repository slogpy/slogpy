"""The purpose of the code is to give debug and info methods a unit test to make sure that they are working properly"""
import pytest

from slogpy.slog import Slog as slog  # noqa: N813


# Unit test for logging
@pytest.mark.parametrize("msg", [
    "This is a test for the file ",
    "try 2",
    None,
    ["String 1", "String 2", "String 3"]
])
def test_info_file(temp_log_file,read_log_file,msg):
    """Given:Using slogpy

    When: Using info() with a String

    Then: Contents of String shows up in a temp file.

    """
    slog.info(msg)
    expected_content = f"{msg}\n"
    content = read_log_file(temp_log_file)
    assert expected_content in content


@pytest.mark.parametrize("msg", [
    "This is a test for the file ",
    "try 2",
    None,
    ["String 1", "String 2", "String 3"]
])
def test_debug_file(temp_log_file,read_log_file,msg):
    """Given:Using slogpy

    When: Using debug() with a String

    Then: Contents of String shows up in a temp file

    """
    slog.debug(msg)
    expected_content = f"{msg}\n"
    content = read_log_file(temp_log_file)
    assert expected_content in content
