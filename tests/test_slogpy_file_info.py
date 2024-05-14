"""Import slogpy from slog"""
import re
import tempfile

import pytest

from slogpy.slog import Slog as slog  # noqa: N813

"""This is a setup function"""
def setupfunction():
    """Initialize the logger with file logging enabled"""
    # Create a temporary log file for testing
    log_file = tempfile.mktemp(suffix=".log")
    slog.initialize(file_logging=True, log_file=log_file)


"""Unit test for logging"""
@pytest.mark.parametrize("msg", [
    # happy cases
    ("This is a test for the file "),
    ("try 2"),
    # Testing with colors
    ("try [red] 3"),
    # testing nulls
    (None),
    # testing array of strings
    (["String 1", "String 2", "String 3"])
])
def test_info_file_output(msg):
    """Passing a message to the info method and then read the message from the log file"""
    slog.info(msg)
     # Accessing the log file attribute directly
    log_file = slog._log_file
    # Read logged messages from the log file
    with open(log_file, "r") as file:
        content = file.read()
    # Remove ANSI color codes from the expected content
    expected_content = re.sub(r"\[\w+\]", "", f"{msg}\n")
    # Check if any of the logged messages contain the expected content
    assert expected_content in content

def test_file_timestamp():
    """Test the timestamp format in the log file"""
    # Log a message
    slog.info("testing")
    # Access the log file attribute directly
    log_file = slog._log_file
    # Read the content of the log file
    with open(log_file, "r") as file:
        content = file.read()
    # Extract the timestamp from the log file content
    timestamp_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}", content)
    # Validate if the timestamp matches the expected format
    assert timestamp_match is not None, "Timestamp not found in log file"
