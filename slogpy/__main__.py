"""Demo of some of the slogpy functionality"""

import time

from slogpy.section import Section
from slogpy.slog import Slog

Slog.initialize(module="slogpy-demo", log_level=Slog.DEBUG)
s = Section("slogpy demo")
Slog.info("this message is from slog.info()")
Slog.warn("this message is from slog.warn()")
Slog.info("Setting a user theme...")
user_theme = {"warn": "black on yellow"}
Slog.set_user_theme(user_theme)
Slog.warn("this message is from slog.warn() after setting theme")
Slog.info("...now back to default theme")
Slog.set_default_theme()
Slog.warn("warning after restoring theme")
with Section("Inner Section", style="red", level=Slog.ERROR) as inner_section:
    inner_section.slog('this inner section called with style="red" and level="slog.ERROR"')
    for feed in ["images", "manifest", "component", "tests"]:
        inner_section.slog(f"FAKE create of feed x1-11-release-r2299-{feed}")
        time.sleep(0.2)
        inner_section.slog(f"...elapsed {inner_section.elapsed()}")

Slog.set_all_fake()
Slog.info("All the messages will be marked as fake until we clear")
Slog.info("more fake stuff")
Slog.info("doing some operation that no longer has to worry about if it's fake or not")
Slog.clear_all_fake()
Slog.info("...slog.clear_all_fake() has been called...back to normal")

# When updating the "demo", leave these at the bottom so the "core" is displayed last
# (i.e. a user doesn't have to search up to see what "normal" output looks like)
Slog.annoy("message from slog.annoy()")
# duplicate annoy, should not show up
Slog.annoy("message from slog.annoy()")
Slog.debug("message from slog.debug()")
Slog.info("message from slog.info()")
Slog.warn("message from slog.warn()")
Slog.error("message from slog.error()")
Slog.fatal("message from slog.fatal()")
Slog.fake("message from slog.fake()")
Slog.fake("message from slog.fake()", log_level=Slog.WARN)
s.end()
with Section("slogpy instructions"):
    Slog.info("To have your logs go somewhere else use:")
    Slog.info("    [yellow]export SLOGPY_LOGPATH=/my/other/dir[/]")
    Slog.info("")
    Slog.info("To use slog in a script:")
    Slog.info("    [yellow]from slogpy.slog import Slog")
    Slog.info("    [yellow]Slog.initialize(module='my_cool_module')")
    Slog.info("    [yellow]Slog.warn('Oh no! I need to warn you')")
Slog.show_logging_path()
