# slogpy
An opinionated and simple to use logger for Python scripts and tools

## Using `slogpy.slog` in your code

### Prep
If you are writing a tool, you should be using `poetry`!
```bash
poetry add slogpy
```
If you are adding slog to an existing script and need to get slogpy in the "old-fashioned way" you can:
```bash
pip3 install --user --upgrade slogpy
```
### In your code
```python
# maybe a bit weird looking, but it gets us the usage style we want
from slogpy.slog import Slog as slog

slog.initialize(module='widget') # optional, but highly recommended

slog.info('Log something at the info level')
slog.debug('log some debugging...this will only go to file unless you set the logging level')
slog.annoy('You need to add handling for this!')
slog.warn('hey, this is a warning')
slog.error('Something bad happened')
slog.fatal('Oh no, Mr. Bill! Something REALLY bad happened')

# if you want to tell the user where the log is (after any logging!)
print(f'Log written to: {slog.get_logging_path()}')
```

## Using a progress bar with slog
If you try to just use rich.progress you will likely not get the desired
result. This is due to a separate console being used. We have wrappers to
solve this.

Here's how to use them:

```python
import time

from slogpy.slog import Slog as slog
from slogpy.progress import (SlogProgress, get_progress,
    get_progress_counting, get_progress_counting_with_time)

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


if __name__ == '__main__':
    test_progress()
```

## Dumping local vars
There are two slog functions to help you emit your local variables:

### `slog.show_locals()`
This is primarily meant for when you want to show some/all of your locals on
the console (they will also be logged).
### `slog.log_locals()`
This is primarily meant for when you want to log some/all of your locals, you
can pass a value to `level` if you also want on the console (for instance, 
during development).

### Example of both
```python
from slogpy.slog import Slog as slog


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
```

## Where the heck are my logs?
Generally, they will be in the same directory from which you ran the python script (CWD). The log file will be named using `YYYYmmDD_HHMMSS.log`

If you called `slog.initialize()` with a module name (recommended), the filename will be `<module>.YYYYmmDD_HHMMSS.log`.
You can also call `slog.initialize(path=my_path)` in which case `my_path` is used as the filename to log to. There are cases where this is better,
but it should not be the norm.

If the log file already exists, `slog` will append to that file.

You can also set a root directory to log to with the environment variable `SLOGPY_LOGPATH` in which case the logs will go to
`<SLOGPY_LOGPATH>/<module>.YYYYmmDD_HHMMSS.log` or `<SLOGPY_LOGPATH>/YYYYmmDD_HHMMSS.log`

Passing a `tag` to `slog.initialize()` will also affect the name of the generated log file. Passing a tag is handy when you have a tool that implements sub-commands and the like.

* `slog.initialize()` -> 20240320_072842.log
* `slog.initialize(module='widget')` -> widget.20240320_072842.log
* `slog.initialize(module='widget', tag='init')` -> widget.20240320_072842.init.log
* `slog.initialize(tag='init')` -> 20240320_072842.init.log

## Using tags with slog and click

```python
@click.group()
# other options and variables here
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.pass_context
def widget_cmd_group(ctx, verbose):
    """does stuff"""
    ctx.ensure_object(dict)
    ctx.obj['log_level'] = slog.DEBUG if verbose else slog.INFO
    # other code goes here


@widget_cmd_group.command('<command>')
@click.pass_context
def widget_<command>(ctx):
    """widget <command>"""
    slog.initialize(module='widget', tag='<command>', log_level=ctx.obj['log_level'])
    # other code goes here
```
