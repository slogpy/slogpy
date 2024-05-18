"""UnitTesting for slog.info to file"""
import re
import tempfile

import pytest

from slogpy.slog import Slog as slog  # noqa: N813


def setupfunction():
    """Initialize the logger with file logging enabled"""
    log_file = tempfile.mktemp(suffix=".log")
    slog.initialize(file_logging=True, log_file=log_file)

def read_log_file():
    """Read and return the content of the log file"""
    log_file = slog.get_logging_path()
    with open(log_file, "r") as file:
        return file.read()

# Unit test for logging
@pytest.mark.parametrize("msg", [
    ("This is a test for the file "),
    ("try 2"),
    (None),
    (["String 1", "String 2", "String 3"])
])
def test_info_file_output(msg):
    """Passing a message to the info method and then read the message from the log file"""
    slog.info(msg)
    content = read_log_file()
    expected_content = f"{msg}\n"
    assert expected_content in content

def test_file_timestamp():
    """Test the timestamp format in the log file"""
    slog.info("testing")
    content = read_log_file()
    first_line = content.splitlines()[0]
    iso8601_format= r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"
    assert re.match(iso8601_format, first_line), f"First line does not start with a valid timestamp: {first_line}"
