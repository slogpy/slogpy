"""Demo of some of the slogpy functionality"""

import time

from slogpy.slog import Slog as slog
from slogpy.section import Section

slog.initialize(module='slogpy-demo', log_level=slog.DEBUG)
s = Section('slogpy demo')
slog.info('this message is from slog.info()')
slog.warn('this message is from slog.warn()')
slog.info('Setting a user theme...')
user_theme = {'warn': 'black on yellow'}
slog.set_user_theme(user_theme)
slog.warn('this message is from slog.warn() after setting theme')
slog.info('...now back to default theme')
slog.set_default_theme()
slog.warn('warning after restoring theme')
with Section('Inner Section', style='red', level=slog.ERROR) as inner_section:
    inner_section.slog('this inner section called with style="red" and level="slog.ERROR"')
    for feed in ['images', 'manifest', 'component', 'tests']:
        inner_section.slog(f'FAKE create of feed x1-11-release-r2299-{feed}')
        time.sleep(0.2)
        inner_section.slog(f'...elapsed {inner_section.elapsed()}')

slog.set_all_fake()
slog.info('All the messages will be marked as fake until we clear')
slog.info('more fake stuff')
slog.info("doing some operation that no longer has to worry about if it's fake or not")
slog.clear_all_fake()
slog.info('...slog.clear_all_fake() has been called...back to normal')

# When updating the "demo", leave these at the bottom so the "core" is displayed last
# (i.e. a user doesn't have to search up to see what "normal" output looks like)
slog.annoy('message from slog.annoy()')
# duplicate annoy, should not show up
slog.annoy('message from slog.annoy()')
slog.debug('message from slog.debug()')
slog.info('message from slog.info()')
slog.warn('message from slog.warn()')
slog.error('message from slog.error()')
slog.fatal('message from slog.fatal()')
slog.fake('message from slog.fake()')
slog.fake('message from slog.fake()', log_level=slog.WARN)
s.end()
with Section('slogpy instructions'):
    slog.info('To have your logs go somewhere else use:')
    slog.info('    [yellow]export SLOGPY_LOGPATH=/my/other/dir[/]')
    slog.info('')
    slog.info('To use slog in a script:')
    slog.info('    [yellow]from slogpy.slog import Slog as slog')
    slog.info("    [yellow]slog.initialize(module='my_cool_module')")
    slog.info("    [yellow]slog.warn('Oh no! I need to warn you')")
slog.show_logging_path()
