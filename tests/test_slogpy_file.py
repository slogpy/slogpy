"""The purpose of this code is to test debug method by using unit test."""
import tempfile

from slogpy.slog import Slog as slog  # noqa: N813

"debug method unit test"
def test_debug_file(msg="This is a file test"):
    """Using slog debug to capture log info in temporary file"""
    # create temp file using tempfile
    temp = tempfile.NamedTemporaryFile(delete=False)
    slog.initialize(path=temp.name,file_logging=True)
    slog.debug(msg)
    expected_content = f"- DEBUG - {msg}\n"
    with open(temp.name, "r") as f:
        content = f.read()
    assert expected_content in content
