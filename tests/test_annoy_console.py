"""Unit this for annoy"""
"""Import slogpy from slog"""
from slogpy.slog import Slog as slog  # noqa: N813, E402


def test_annoy_unique_message():  # noqa: D103
    # Arrange
    message = ""

    # Act
    slog.annoy(message)

    # Assert
    # Check if the message is in the _annoyed dictionary
    assert message in slog._annoyed