"""The purpose of the code is to give debug and info methods a unit test to make sure that they are working properly"""
from slogpy.slog import Slog as slog  # noqa: N813


def setup_function():
    """Set the Default to no log file, since only interested in console output"""
    slog.initialize(file_logging=False)

def test_info_console_output(capsys, msg="This is a console test"):
    """Given: Using the slogpy library

    When: log an information message

    Then: the message shows in the stdout stream
    And the message does not show in the stderr stream

    """
    slog.info(msg)
    expected_content = f"{msg}\n"
    expected_error_content = ""
    out, error = capsys.readouterr()

    assert expected_content == out
    assert expected_error_content == error

def test_debug_console_output(capsys, msg="This is a test message"):
    """Given:I am using the slogpy library

    When: Passing an message to debug()

    Then: the message shows in the file
    And the message does not show in the stderr and stdout stream
    """
    slog.debug(msg)
    expected_content = ""
    expected_error_content = ""
    out, error = capsys.readouterr()
    assert expected_error_content == error
    assert expected_content == out

