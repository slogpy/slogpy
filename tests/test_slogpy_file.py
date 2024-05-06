from slogpy import slog
from slogpy import __version__
from slogpy.slog import Slog as slog
import tempfile


def setup_function(function):
    slog.initialize(file_logging=True)


#INFO
def test_info_file(msg="This is a test"):
    """The test for the info function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.info(msg)
    expected_content = f"- INFO - {msg}\n"
    with open(temp.name, 'r') as f:
        content = f.read()

    assert expected_content in content
#ANNOY
def test_annoy_file(msg="This is a test"):
    """The test for the annoy function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.annoy(msg)
    expected_content = f"- INFO - ANNOYING YOU: {msg}\n"
    with open(temp.name, 'r') as f:
        content = f.read()

    assert expected_content in content
#DEBUG
def test_debug_file(msg="This is a test"):
    """The test for the debug function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.debug(msg)
    expected_content = f"- DEBUG - {msg}\n"
    with open(temp.name, 'r') as f:
        content = f.read()

    assert expected_content in content

#WARN
def test_warn_file(msg="This is a test"):
    """The test for the debug function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.warn(msg)
    expected_content = f"- WARNING - {msg}\n"
    with open(temp.name, 'r') as f:
        content = f.read()

    assert expected_content in content

#FATAL
def test_fatal_file(msg="This is a test"):
    """The test for the debug function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name)
    slog.fatal(msg)
    expected_content = f"- CRITICAL - {msg}\n"
    with open(temp.name, 'r') as f:
        content = f.read()

    assert expected_content in content

