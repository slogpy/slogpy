"""Import slogpy from slog"""
from slogpy import slog

"""This is a setup function"""
def setupfunction():
    """Not to create a file for output"""
    slog.initialize(file_logging=False)

"""First unit test"""
def test_info_console_output(capsys, msg="This is a console test"):
    """Passing a message to the info method and then capture the message from the console"""
    slog.info(msg)
    expected_content = f"{msg}\n"
    out,  = capsys.readouterr()
    assert expected_content == out
