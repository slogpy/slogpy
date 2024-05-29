"""The purpose of the code is to give debug and info methods a unit test to make sure that they are working properly"""
import os
import tempfile

import pytest

from slogpy.slog import Slog as slog  # noqa: N813


@pytest.fixture(scope="function")
def temp_log_file():
    """Fixture to initialize the logger with file logging enabled and cleanup afterwards"""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file_path = os.path.join(temp_dir, "test_log.log")
        slog.initialize(path=log_file_path)
        yield log_file_path
        # Ensure the logger releases the file handler
        for handler in slog._logger.handlers:
            handler.close()
        slog._logger.handlers = []

def read_log_file(log_file_path):
    """Read and return the content of the log file"""
    with open(log_file_path, "r") as file:
        return file.read()

# Unit test for logging
@pytest.mark.parametrize("msg", [
    "This is a test for the file ",
    "try 2",
    None,
    ["String 1", "String 2", "String 3"]
])


def test_info_file(temp_log_file,msg):
    """Given:Using slogpy

    When: Using info() with a String

    Then: Contents of String shows up in a temp file.

    """
    slog.info(msg)
    expected_content = f"{msg}\n"
    content = read_log_file(temp_log_file)
    assert expected_content in content
# another Unit test for logging
@pytest.mark.parametrize("msg", [
    "This is a test for the file ",
    "try 2",
    None,
    ["String 1", "String 2", "String 3"]
])

def test_debug_file(temp_log_file,msg):
    """Given:Using slogpy

    When: Using debug() with a String

    Then: Contents of String shows up in a temp file AND nothing in stdout and stderr

    """
    slog.info(msg)
    expected_content = f"{msg}\n"
    content = read_log_file(temp_log_file)
    assert expected_content in content
