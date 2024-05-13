"""Import slogpy from slog"""
from slogpy.slog import Slog as slog  # noqa: N813

"""This is a setup function"""
def setup_function():
    """set "file_logging = False", so it will not create a log file for output."""
    slog.initialize(file_logging=False)

"""First unit test"""
def test_info_console_output(capsys, msg="This is a console test"):
    """Passing a message to the info method and then capture the message from the console"""
    slog.info(msg)
    expected_content = f"{msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

"""Second unit test (debug method)"""
def test_debug_console_output(capsys, msg=""):
    """Passing a message to the Debug method and then capture the message from the console"""
    slog.debug(msg)
    expected_content = f"{msg}"
    # not sure this line of code is necessary or not. since this won't be any content in the console.
    out, _ = capsys.readouterr()
    assert expected_content == ""
