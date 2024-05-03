import time

from slogpy.slog import Slog as slog
from slogpy.progress import (SlogProgress, get_progress,
    get_progress_counting, get_progress_counting_with_time)
from slogpy.slog import Slog as slog
import click
slog.initialize(module='widget') # optional, but highly recommended

slog.info('Log something at the info level')
slog.debug('log some debugging...this will only go to file unless you set the logging level')
slog.annoy('You need to add handling for this!')
slog.warn('hey, this is a warning')
slog.error('Something bad happened')
slog.fatal('Oh no, Mr. Bill! Something REALLY bad happened')

# if you want to tell the user where the log is (after any logging!)
print(f'Log written to: {slog.get_logging_path()}')

# You can call SlogProgress() just like you would rich.progress.Progress
# or you can use one of the predefined factory methods. If you have a
# progress bar that you use often, add a factory for it in
# slogpy/slogpy/progress.py

def test_progress():
    my_iterable = ['apple', 'pear', 'orange', 'banana', 'kiwi', 'plum', 'durian', 'strawberry', 'grape', 'grapefruit']

    progress = SlogProgress()
    with progress:
        for fruit in progress.track(my_iterable, description='pick fruit'):
            slog.info(f'working on {fruit}')
            time.sleep(0.5)

    progress = get_progress_counting()
    with progress:
        for fruit in progress.track(my_iterable, description='pick fruit'):
            slog.info(f'working on {fruit}')
            time.sleep(0.5)

    progress = get_progress_counting_with_time()
    with progress:
        for tick in progress.track(range(0,10093), description='pick fruit'):
            if tick % 427 == 0:
                slog.info(f'{tick} mod 7 is 0')
            time.sleep(0.0003)


def some_function(name, title, number=27):
    """Demonstrate show_locals and log_locals"""
    x = f'{name}, {title}'
    y = number * 2 - 12
    password = 'p@ssw0rd123'
    other_pass = '123'
    super_secret = 'codename'
    foo = dict(name=name, number=number)

    # demonstrate with pretty set and unset
    for pretty in [True, False]:
        slog.info(f'calling slog.show_locals() with {pretty=}')
        slog.show_locals([
            'name',
            'title',
            'title',
            'y',
            'foo',
            'password',
        ], obfuscate=['password'], pretty=pretty)

    # If you want all the locals, just don't include the list of names
    # ...you may still want to hide/obfuscate
    slog.info('calling slog.show_locals w/o specifying the names')
    slog.show_locals(obfuscate=['password', 'other_pass'], hide=['super_secret'])

    # Logging (usually won't go to screen as it defaults to log_level=slog.DEBUG)
    slog.info('calling slog.log_locals()')
    slog.log_locals(obfuscate=['password', 'other_pass'], hide=['super_secret'])

    # But sometimes we are developing and want to see w/o having to go to the log
    slog.info('calling slog.log_locals() and log_level=slog.INFO')
    slog.log_locals(obfuscate=['password', 'other_pass'], hide=['super_secret'], log_level=slog.INFO)
    slog.show_logging_path()


if __name__ == '__main__':
    some_function('Alice', 'Developer')


@click.group()
# other options and variables here
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.pass_context
def widget_cmd_group(ctx, verbose):
    """does stuff"""
    ctx.ensure_object(dict)
    ctx.obj['log_level'] = slog.DEBUG if verbose else slog.INFO
