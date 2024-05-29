"""Conftest File is for all the unit test files that test file logging."""
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


@pytest.fixture(scope="function")
def read_log_file():
    """Fixture to read and return the content of the log file"""
    def _read_log_file(log_file_path):
        with open(log_file_path, "r") as file:
            return file.read()
    return _read_log_file
