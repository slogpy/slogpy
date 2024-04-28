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