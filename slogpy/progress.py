"""Progress bars for slog"""

from typing import Optional, Union
import rich.progress
from rich.progress import ProgressColumn, GetTimeCallable

from slogpy.slog import Slog as slog


class SlogProgress(rich.progress.Progress):
    """A slog friendly progress"""

    # pylint: disable=useless-super-delegation
    def __init__(self,
                 *columns: Union[str, ProgressColumn],
                 auto_refresh: bool = True,
                 refresh_per_second: float = 10,
                 speed_estimate_period: float = 30,
                 transient: bool = False,
                 redirect_stdout: bool = True,
                 redirect_stderr: bool = True,
                 get_time: Optional[GetTimeCallable] = None,
                 disable: bool = False,
                 expand: bool = False) -> None:
        super().__init__(*columns,
                         console=slog._rich_console,
                         auto_refresh=auto_refresh,
                         refresh_per_second=refresh_per_second,
                         speed_estimate_period=speed_estimate_period,
                         transient=transient,
                         redirect_stdout=redirect_stdout,
                         redirect_stderr=redirect_stderr,
                         get_time=get_time,
                         disable=disable,
                         expand=expand)


# ============================================================
# Factory functions for common progress bars.
# ============================================================
def get_progress() -> SlogProgress:
    """Get the rich default style progress bar"""
    return SlogProgress()


def get_progress_counting() -> SlogProgress:
    """Get the simple counting progress bar"""
    return SlogProgress("[progress.description]{task.description}", rich.progress.BarColumn(),
                        rich.progress.MofNCompleteColumn())


def get_progress_counting_with_time() -> SlogProgress:
    """Get the counting progress with estimated time bar"""
    return SlogProgress(
        "[progress.description]{task.description}",
        rich.progress.BarColumn(),
        "{task.completed}/{task.total:.0f}",
        rich.progress.TimeRemainingColumn(),
        rich.progress.TimeElapsedColumn(),
    )
