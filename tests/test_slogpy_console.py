"""The test for the slogpy package."""
from slogpy import slog
from slogpy import __version__
from slogpy.slog import Slog as slog
def test_version():
    """The most basic of tests."""
    assert __version__ == "0.1.0"

def setup_function(function):
    slog.initialize(file_logging=False)

#Info
def test_info_console_output(capsys, msg="This is a console test"):
    slog.info(msg)
    expected_content = f"{msg}\n"
    # Capture the output to stdout and stderr
    out, _ = capsys.readouterr()
    assert expected_content == out

#Annoy
def test_annoy_console_output(capsys, msg="This is a console test"):
    slog.annoy(msg)
    expected_content = f"ANNOYING YOU: {msg}\n"
    # Capture the output to stdout and stderr
    out, _ = capsys.readouterr()
    assert expected_content == out

#Debug
def test_debug_console_output(capsys, msg=""):
    slog.debug(msg)
    expected_content = f"{msg}"
    # Capture the output to stdout and stderr
    out, _ = capsys.readouterr()
    assert expected_content == ""

#Warn
def test_warn_console_output(capsys, msg="This is a console test"):
    slog.warn(msg)
    expected_content = f"WARNING: {msg}\n"
    # Capture the output to stdout and stderr
    out, _ = capsys.readouterr()
    assert expected_content == out

#Fatal
def test_warn_console_output(capsys, msg="This is a console test"):
    slog.fatal(msg)
    expected_content = f"FATAL: {msg}\n"
    # Capture the output to stdout and stderr
    out, _ = capsys.readouterr()
    assert expected_content == out