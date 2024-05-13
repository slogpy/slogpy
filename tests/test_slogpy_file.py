"""Import slogpy from slog"""
from slogpy.slog import Slog as slog # noqa: N813 I001
import tempfile

"""This is a setup function"""
def setup_function():
    """create a file for output"""
    slog.initialize(file_logging=True)

"""debug method unit test"""
def test_debug_file(msg="This is a file test"):
    """The test for the debug function."""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.debug(msg)
    expected_content = f"- DEBUG - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()

    assert expected_content in content
