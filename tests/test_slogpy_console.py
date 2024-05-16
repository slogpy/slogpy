"""The purpose of the code is to give two methods a unit test to make sure that they are working properly"""
from slogpy.slog import Slog as slog  # noqa: N813

"This is a setup function"
def setup_function():
    """set the Default to no log file, since only interested in console output"""
    slog.initialize(file_logging=False)

"First unit test"
def test_info_console_output(capsys, msg="This is a console test"):
    """Using slog info to capture log info in stdout"""
    slog.info(msg)
    expected_content = f"{msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

"Second unit test (debug method)"
def test_debug_console_output(capsys, msg=""):
    """Using slog debug to capture log info in stdout"""
    slog.debug(msg)
    expected_content = ""
    # not sure this line of code is necessary or not. since this won't be any content in the console.
    out, _ = capsys.readouterr()
    assert expected_content == ""
