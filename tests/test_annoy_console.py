"""module contains tests for the Slog class, specifically the annoying method, which is responsible for slog annoying"""

from slogpy.slog import Slog as slog  # noqa: N813,


def test_annoy_unique_message(capsys, msg="This is a annoy test"):  # noqa: D103
    """Given: a single line annoy message

    When: passed into slog.annoy
    Then: method will check for annoy message only once and display it.
    """
    # Arrange

    # Act
    slog.annoy(msg)


    expected_content = f"ANNOYING YOU: {msg}\n"
    expected_error_content = ""
    out, error = capsys.readouterr()

    assert expected_content == out
    assert expected_error_content == error
