"""UnitTesting for slog.info to file"""
import os
import re
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
def test_info_file_output(temp_log_file, msg):
    """Passing a message to the info method and then read the message from the log file

    Given: users input
    When: log users input with slog.info
    Then: check if output is the same as input
    """
    slog.info(msg)
    content = read_log_file(temp_log_file)
    expected_content = f"{msg}\n"
    assert expected_content in content

def test_file_timestamp(temp_log_file):
    """Timestamp checking method

    Given: a single line log message
    When: passed into slog.info
    Then: method will check start of output for timestamp
    """
    slog.info("testing")
    content = read_log_file(temp_log_file)
    lines = content.splitlines()
    iso8601_format = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"
    for line in lines:
        assert re.match(iso8601_format, line), f"Line does not start with a valid timestamp: {line}"
