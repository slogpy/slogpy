# Unit this for annoy
# Import slogpy from slog
from slogpy.slog import Slog as slog  # noqa: N813, E402

"""This module contains tests for the Slog class, specifically the annoying method,
which is responsible for slog annoying messages.
"""

# (note to self) make sure the count is only once......

def test_annoy_unique_message(capsys, msg="This is a annoy test"):  # noqa: D103
    """Timestamp checking method

    Given: a single line annoy message
    When: passed into slog.annoy
    Then: method will check for annoy message
    """
    # Arrange

    # Act
    slog.annoy(msg)

    # Assert (note to self: )
    # Check if the message is in the _annoyed dictionary
    assert msg in slog._annoyed

    expected_content = f"ANNOYING YOU: {msg}\n"
    expected_error_content = ""
    out, error = capsys.readouterr()

    assert expected_content == out
    assert expected_error_content == error

