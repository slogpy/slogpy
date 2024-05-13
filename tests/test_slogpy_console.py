"""Import slogpy from slog"""
from slogpy.slog import Slog as slog # noqa: N813 I001

"""This is a setup function"""
def setup_function():
    """Not to create a file for output"""
    slog.initialize(file_logging=False)

"""First unit test"""
def test_info_console_output(capsys, msg="This is a console test"):
    """Passing a message to the info method and then capture the message from the console"""
    slog.info(msg)
    expected_content = f"{msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out

"""Second unit test (Debug Method)"""
def test_debug_console_output(capsys, msg="This is a console test"):
    """Set the log level to 1, so the output can be captured from the consol"""
    slog.set_log_level(1)
    """Passing a message to the Debug method and then capture the message from the console"""
    slog.debug(msg)
    expected_content = f"DEBUG: {msg}\n"
    out, _ = capsys.readouterr()
    assert expected_content == out
