"""Script Logger"""

import copy
import datetime
import inspect
import logging
import os
from typing import List, Optional

from rich.table import Table
import rich.box
from rich.console import Console
import rich.console
from rich.theme import Theme

from slogpy.util import strip_style_markup

# Type alias to keep my lines a bit shorter
OptListStr = Optional[List[str]]

SLOG_THEME_DATA = {
    # Log Levels
    'debug': 'bright_black',
    'info': 'white',
    'warn': 'bright_yellow',
    'error': 'bright_red',
    'fatal': 'white on red',
    'annoy': 'red on bright_yellow',
    'fake': 'black on green',
    'debug_label': 'magenta',
    # Section
    'section_rule': 'bright_blue',
    'section_start': 'yellow',
    'section_end': 'cyan',
    'section_timestamp': 'bright_black',
    # Misc
    'filepath': 'green',
}

SLOG_THEME = Theme(SLOG_THEME_DATA)
SLOG_NO_THEME = Theme({k: '' for k in SLOG_THEME_DATA})
CONSOLE = Console(theme=SLOG_THEME)


def _get_depth_str(depth):
    """Create pad for insertion at beginning of a log output"""
    if depth == 0:
        return ''
    return '-' * (depth * 2) + ' '


def _get_logging_root_path():
    """What directory should we log into"""
    root = os.getenv('SLOGPY_LOGPATH')
    if root and not os.path.isdir(root):
        print(f'** WARNING ** SLOGPY_LOGPATH set to {root} but that is not a directory; using {os.getcwd()}')
        root = None
    if not root:
        root = os.getcwd()
    return root


def _get_logging_name(module, tag):
    """Get the datetime thingy"""
    now = datetime.datetime.now()
    base_part = now.strftime('%Y%m%d_%H%M%S')
    tag_part = f'.{tag}' if tag else ''
    if module:
        return f'{module}.{base_part}{tag_part}'
    return base_part


class Slog:
    """Script Logger"""
    # pylint: disable=too-many-public-methods
    MINIMAL = 0
    DEBUG = 1
    INFO = 5
    WARN = 9
    ERROR = 10
    FATAL = 99
    _console_log_level = INFO
    _file_log_level = MINIMAL
    # Attack surface for doing user customizable themes,
    # We will want a helper (via either cli or python -m slogpy)
    # That will create a user theme template with all our theme "css classes"
    _rich_console = rich.console.Console(theme=SLOG_THEME)
    _logger = None
    _logger_threw_exception = False
    _log_file = None
    _module_name = None
    _tag = None
    _annoyed = {}
    console_logging_enabled = True
    _it_is_all_fake = False

    SLOG_TO_LOGGING = {
        MINIMAL: logging.NOTSET,
        DEBUG: logging.DEBUG,
        INFO: logging.INFO,
        WARN: logging.WARNING,
        ERROR: logging.ERROR,
        FATAL: logging.CRITICAL,
    }

    @classmethod
    def initialize(cls,
                   path: str = None,
                   module=None,
                   tag=None,
                   file_logging=True,
                   console_logging=True,
                   log_level=INFO):
        """Initialize Slog - optional but recommended"""
        # pylint: disable=too-many-arguments
        cls.set_log_level(log_level)
        cls.console_logging_enabled = console_logging
        if module:
            cls._module_name = module
        if tag:
            cls._tag = tag
        if not file_logging:
            cls._logger = False
            return
        if path:
            cls._log_file = os.path.realpath(path)
        else:
            cls._initialize_log_file(module=module, tag=tag)
        cls._initialize_logger()

    @classmethod
    def _initialize_log_file(cls, module=None, tag=None):
        log_dir = _get_logging_root_path()
        log_name = _get_logging_name(module, tag)
        cls._log_file = os.path.join(log_dir, f'{log_name}.log')

    @classmethod
    def _initialize_logger(cls):
        # ensure this never fails
        cls._logger = False
        # actually initialize cls._logger
        try:
            cls._logger = logging.getLogger('main')
            cls._logger.setLevel(logging.NOTSET + 1)

            file_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            if not cls._log_file:
                cls._initialize_log_file()
            file_handler = logging.FileHandler(cls._log_file)
            file_handler.setLevel(logging.NOTSET + 1)
            file_handler.setFormatter(file_log_formatter)

            cls._logger.addHandler(file_handler)
        except Exception as ex:  # pylint: disable=broad-except
            if not cls._logger_threw_exception:
                cls._logger_threw_exception = True
                # using print here as we may not be printing to console
                print(f'*** Exception creating file logger: {ex}')

    @classmethod
    def set_all_fake(cls):
        """All logging will have fake tag until clear_all_fake() called"""
        cls._it_is_all_fake = True

    @classmethod
    def clear_all_fake(cls):
        """Clears the all fake flag"""
        cls._it_is_all_fake = False

    @classmethod
    def set_default_theme(cls):
        """Set the theme to no theme"""
        cls._rich_console = rich.console.Console(theme=SLOG_THEME)

    @classmethod
    def set_no_theme(cls):
        """Set the theme to no theme"""
        cls._rich_console = rich.console.Console(theme=SLOG_NO_THEME)

    @classmethod
    def set_user_theme(cls, user_theme: dict, update=True):
        """Set the theme as defined by the user"""
        # The caller should not need to know all the keys that we have added, so we start with either the default
        # or the "no theme" dictionary and then apply the passed in dictionary to it.
        if update:
            base = SLOG_THEME_DATA.copy()
        else:
            base = {k: '' for k in SLOG_THEME_DATA}
        base.update(user_theme)
        cls._rich_console = rich.console.Console(theme=Theme(base))

    @classmethod
    def set_log_level(cls, level: int):
        """Explicitly set the logging level"""
        cls._console_log_level = level

    @classmethod
    def _set_file_log_level(cls, level: int):
        """Explicitly set the logging level for file output"""
        cls._file_log_level = level

    # ============================================================
    # The logging worker functions
    # ============================================================
    @classmethod
    def slog(cls, message, level=INFO, depth=0, op_start=False, always=False, fake=False):
        """script log - write some stuff to the console and/or the file"""
        # pylint: disable=too-many-arguments
        fake = fake or cls._it_is_all_fake
        depth_str = _get_depth_str(depth)
        out_message = f'[fake] ══ FAKE ══ [/] {message}' if fake else message
        cls._slog_to_file(out_message, level, depth_str, op_start)
        cls._slog_to_console(out_message, level, depth_str, op_start, always)

    @classmethod
    def section(cls, name, time_part='', start=True, style='section_rule', max_width=118, level=INFO):
        """Section header/footer"""
        # pylint: disable=too-many-arguments
        name_style = '[section_start]' if start else '[section_end]'
        file_tag = 'SECTION START: ' if start else 'SECTION END: '
        styled_title = f'{name_style}{name}[/] [section_timestamp]{time_part}[/]'
        # Need to do strip rather than just cat name and time_part as either may have embedded styles
        stripped_title = strip_style_markup(styled_title)
        # Not too wide and adjust smaller for small consoles
        max_width = min(cls._rich_console.width, max_width)
        the_bar = '━' * max(10, (max_width - 1 - len(stripped_title)))

        # output to console
        if cls.console_logging_enabled and (level >= cls._console_log_level):
            cls._rich_console.print(f'[{style}]{the_bar}[/] {styled_title}')

        # output to file
        cls._slog_to_file('=' * 80, level, '', False)
        cls._slog_to_file(file_tag + stripped_title, level, '', False)
        cls._slog_to_file('=' * 80, level, '', False)

    @classmethod
    def _slog_to_console(cls, message, level, depth_str, op_start, always):
        """Actually log to the console"""
        # pylint: disable=too-many-arguments
        if not cls.console_logging_enabled:
            return

        prepend_map = {
            Slog.WARN: '[warn]WARNING[/]: ',
            Slog.ERROR: '[error]ERROR[/]: ',
            Slog.FATAL: '[fatal]FATAL[/]: ',
            Slog.DEBUG: '[debug_label]DEBUG[/]: '
        }
        # Guard clause - no logging to console needed
        if not always and level < cls._console_log_level:
            return
        # Set up for the colorized prepend for >= WARN
        prepend = ''
        if prepend_map.get(level):
            prepend = prepend_map[level]
        # Most message parts get info, but debug gets debug
        message_theme = '[info]'
        if level == Slog.DEBUG:
            message_theme = '[debug]'
        # No newline if op_start
        ending = '' if op_start else '\n'
        # Send it
        cls._rich_console.print(f'{depth_str}{prepend}{message_theme}{message}', end=ending, soft_wrap=True)

    @classmethod
    def _slog_to_file(cls, message, level, depth_str, op_start):
        """Actually log to file"""
        # if logger not initialized, initialize logger
        if cls._logger is False:
            return
        if cls._logger is None:
            cls._initialize_logger()
        # log the message
        try:
            # Log the message via python logging
            out_message = strip_style_markup(f'{depth_str}{message}', console=cls._rich_console)
            if op_start:
                out_message += '[ --> ]'
            logging_level = cls.SLOG_TO_LOGGING[level]
            cls._logger.log(level=logging_level, msg=out_message)
        except Exception as ex:  # pylint: disable=broad-except
            # if this is the first exception, then we send the exception to the console.
            if not cls._logger_threw_exception:
                cls._logger_threw_exception = True
                # send exception to console
                # ...for now
                print(f'** File logger exception **: {ex}')

    # ============================================================
    # Where's my logfile?
    # ============================================================
    @classmethod
    def get_logging_path(cls):
        """Get a printable string of the logging path"""
        if cls._log_file is None:
            return "NO LOG FILE SET"
        return str(cls._log_file)

    @classmethod
    def show_logging_path(cls):
        """Display the log file path to the console"""
        if cls._log_file is None:
            cls._rich_console.print('[warn]NO LOG FILE[/warn]')
        else:
            cls._rich_console.print(f'Log written to: [filepath]{cls._log_file}[/]')

    # ============================================================
    # Normal logging functions
    # ============================================================
    @classmethod
    def annoy(cls, message):
        """Show an annoy message...only displayed first time unique message passed"""
        if message not in cls._annoyed:
            cls._annoyed[message] = True
            cls.slog(f'[annoy]ANNOYING YOU: {message}[/annoy]', always=True)

    @classmethod
    def always(cls, message, level=INFO, depth=0, op_start=False, fake=False):
        """We want this to go to the console...period."""
        # pylint: disable=too-many-arguments
        cls.slog(message, level, depth, op_start, fake=fake)

    @classmethod
    def debug(cls, message, depth=0, op_start=False, fake=False):
        """log debugging message"""
        cls.slog(message=message, level=cls.DEBUG, depth=depth, op_start=op_start, fake=fake)

    @classmethod
    def info(cls, message, depth=0, op_start=False, fake=False):
        """log an info message"""
        cls.slog(message=message, level=cls.INFO, depth=depth, op_start=op_start, fake=fake)

    @classmethod
    def warn(cls, message, depth=0, op_start=False, fake=False):
        """log an warning message"""
        cls.slog(message=message, level=cls.WARN, depth=depth, op_start=op_start, fake=fake)

    @classmethod
    def error(cls, message, depth=0, op_start=False, fake=False):
        """log an error message"""
        cls.slog(message=message, level=cls.ERROR, depth=depth, op_start=op_start, fake=fake)

    @classmethod
    def fatal(cls, message, depth=0, op_start=False, fake=False):
        """log a fatal message...oh no!"""
        cls.slog(message=message, level=cls.FATAL, depth=depth, op_start=op_start, fake=fake)

    @classmethod
    def fake(cls, message, log_level=INFO, depth=0, op_start=False):
        """specific log of a FAKE operation"""
        cls.slog(message=f'[fake] ══ FAKE ══ [/] {message}', level=log_level, depth=depth, op_start=op_start)

    # ============================================================
    # Specialty logging
    # ============================================================

    @staticmethod
    def _process_locals(caller_locals: dict,
                        var_names: List[str],
                        obfuscate: OptListStr = None,
                        hide: OptListStr = None):
        """Gets the locals ready for display"""
        work = copy.copy(var_names)
        if obfuscate:
            work.extend(obfuscate)
        work = list(set(work))
        work.sort()
        locals_dict = {}
        for name in work:
            if hide and name in hide:
                continue
            value = caller_locals[name]
            if obfuscate and name in obfuscate:
                if isinstance(caller_locals[name], str) and len(caller_locals[name]) > 8:
                    value = caller_locals[name][0:1] + '***' + caller_locals[name][-1:]
                else:
                    value = '*****'
            value = str(value)
            locals_dict[name] = value
        return locals_dict

    @classmethod
    def show_locals(cls,
                    var_names: OptListStr = None,
                    obfuscate: OptListStr = None,
                    hide: OptListStr = None,
                    pretty=True,
                    log_level=INFO):
        """Display locals from the calling function"""
        # pylint: disable=too-many-arguments
        frame = inspect.currentframe()
        caller_locals = frame.f_back.f_locals
        if var_names is None:
            var_names = list(caller_locals.keys())
        locals_dict = cls._process_locals(caller_locals, var_names, obfuscate, hide=hide)
        if pretty:
            table = Table(show_header=False, box=rich.box.SQUARE)
            table.add_column()
            table.add_column()
            for k, v in locals_dict.items():
                table.add_row(k, v)
            cls._rich_console.print(table)

        # If we pretty printed, we only want the file
        if pretty:
            slog_kwargs = {'depth_str': '', 'op_start': False, 'level': log_level}
            _ = [cls._slog_to_file(f'{k}: {v}', **slog_kwargs) for k, v in locals_dict.items()]
        else:
            _ = [cls.slog(f'{k}: {v}', level=log_level) for k, v in locals_dict.items()]

    @classmethod
    def log_locals(cls, obfuscate: OptListStr = None, hide: OptListStr = None, log_level=DEBUG):
        """Log the locals from the calling function"""
        frame = inspect.currentframe()
        caller_locals = frame.f_back.f_locals
        var_names = list(caller_locals.keys())
        locals_dict = cls._process_locals(caller_locals, var_names, obfuscate, hide)
        cls.slog(f'Caller vars: {locals_dict}', level=log_level)
