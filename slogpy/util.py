"""The utility bucket"""

from rich.console import Console


def strip_style_markup(message: str, console=None) -> str:
    """Remove the 'rich' markup from a string"""
    if console is None:
        console = Console()
    t = console.render_str(str(message))
    return t.plain
