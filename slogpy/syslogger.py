"""Helpers to write to syslog - this needs work! Just here as placeholder and example of how to write to
the syslog. This should be properly incorporated into slogpy (soon!)"""

import syslog


def write_to_syslog(message: str) -> None:
    """Write to syslog"""
    # syslog.syslog(syslog.LOG_INFO, message)
    syslog.syslog(syslog.LOG_ERR, message)


def main():
    """Entry point"""
    write_to_syslog('this is a test2')


if __name__ == '__main__':
    main()
