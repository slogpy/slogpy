"""The test for the slogpy package."""
import pytest
import re
from slogpy import slog
from slogpy import __version__
from slogpy.slog import Slog as slog
from unittest.mock import patch
import unittest
def test_version():
    """The most basic of tests."""
    assert __version__ == "0.1.0"

def test_Slog_info(capsys, string):
    """Test function to check if slog.info correctly logs the provided string."""
    slog.info(string)
    captured = capsys.readouterr()
    # Remove ANSI escape codes using regex
    cleaned_output = re.sub(r'\x1b[[0-9;]*m', '', captured.out)
    return cleaned_output.strip() == string

# Method to test slog.info to console when using nulls
def test_logging_info_None(capsys):
    """Test slog.info when passed None."""
    assert test_Slog_info(capsys, None)

# Method to test slog.info to console when using a string
def test_logging_info_String(capsys):
    """Test slog.info when passed a string."""
    assert test_Slog_info(capsys, 'Log something at the info level')

# Method to test slog.info to console when using an empty string
def test_logging_info_Empty(capsys):
    """Test slog.info when passed an empty string."""
    assert test_Slog_info(capsys, '')







# def test_logging_info(capsys):

#     slog.info("Log something at the info level")
#     captured = capsys.readouterr()
#      # Remove ANSI escape codes using regex
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "Log something at the info level\n"

# def test_logging_debug(capsys):
#     # Set logging level to DEBUG (or appropriate level for debug messages)
#     original_level = slog._console_log_level  # Store original level (optional)
#     slog.set_log_level(slog.DEBUG)

#     slog.debug('log some debugging...this will only go to file unless you set the logging level')
#     captured = capsys.readouterr()
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "DEBUG: log some debugging...this will only go to file unless you set the logging level\n"

#     # Reset logging level (optional)
#     slog.set_log_level(original_level)

# def test_logging_annoy(capsys):

#     slog.annoy('You need to add handling for this!')
#     captured = capsys.readouterr()
#      # Remove ANSI escape codes using regex
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "ANNOYING YOU: You need to add handling for this!\n"

# def test_logging_warn(capsys):

#     slog.warn("hey, this is a warning")
#     captured = capsys.readouterr()
#      # Remove ANSI escape codes using regex
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "WARNING: hey, this is a warning\n"

# def test_logging_error(capsys):

#     slog.error('Something bad happened')
#     captured = capsys.readouterr()
#      # Remove ANSI escape codes using regex
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "ERROR: Something bad happened\n"

# def test_logging_fatal(capsys):

#     slog.fatal('Oh no, Mr. Bill! Something REALLY bad happened')
#     captured = capsys.readouterr()
#      # Remove ANSI escape codes using regex
#     cleaned_output = re.sub(r'\x1b\[[0-9;]*m', '', captured.out)
#     assert cleaned_output == "FATAL: Oh no, Mr. Bill! Something REALLY bad happened\n"


# def test_get_logging_path_with_log_file(tmp_path):
#     """Test get_logging_path with a temporary log file"""
#     log_file_path = tmp_path / "test.log"
#     slog.initialize(path=str(log_file_path))
#     assert slog.get_logging_path() == str(log_file_path)


