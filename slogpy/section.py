"""Nice output for sections with time and elapsed"""

import datetime
from slogpy.slog import Slog as slog


class Section:
    """Log a section header/footer"""

    def __init__(self, name, style='section_rule', level=slog.INFO) -> None:
        """initialize the instance and display the header"""
        self.start = datetime.datetime.now()
        self.name = name
        self.style = style
        self.level = level
        # the [:-3] removes the last three digits so we don't have unnecessary precision that is distracting.
        slog.section(self.name,
                     self.start.strftime('%a %H:%M:%S.%f')[:-3],
                     start=True,
                     style=self.style,
                     level=self.level)

    def elapsed(self):
        """time elapsed since creating instance"""
        now = datetime.datetime.now()
        return now - self.start

    def end(self):
        """Done with the section, emit the footer"""
        # the [:-3] removes the last three digits so we don't have unnecessary precision that is distracting.
        slog.section(self.name, str(self.elapsed())[:-3], start=False, style=self.style, level=self.level)

    def slog(self, message, depth=0, op_start=False):
        """Logs a message in the section"""
        slog.slog(message=message, level=self.level, depth=depth, op_start=op_start)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()
