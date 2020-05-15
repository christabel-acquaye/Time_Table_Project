#!/usr/bin/env python
# encoding: utf-8
import logging
import platform
import time

from gunicorn import glogging

# now we patch Python code to add color support to logging.StreamHandler


def add_coloring_to_emit_windows(fn):
    # add methods we need to the class
    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

    def _set_color(self, code):
        import ctypes
        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    # noinspection PyProtectedMember,PyProtectedMember
    def new(*args):
        FOREGROUND_BLUE = 0x0001  # text color contains blue.
        FOREGROUND_GREEN = 0x0002  # text color contains green.
        FOREGROUND_RED = 0x0004  # text color contains red.
        FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
        # winbase.h

        # wincon.h
        FOREGROUND_GREEN = 0x0002
        FOREGROUND_RED = 0x0004
        FOREGROUND_MAGENTA = 0x0005
        FOREGROUND_YELLOW = 0x0006
        FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.

        BACKGROUND_YELLOW = 0x0060
        BACKGROUND_INTENSITY = 0x0080  # background color is intensified.

        levelno = args[1].levelno
        if levelno >= 50:
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY
        elif levelno >= 40:
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif levelno >= 30:
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif levelno >= 20:
            color = FOREGROUND_GREEN
        elif levelno >= 10:
            color = FOREGROUND_MAGENTA
        else:
            color = FOREGROUND_WHITE
        # noinspection PyProtectedMember
        args[0]._set_color(color)

        ret = fn(*args)
        # noinspection PyProtectedMember
        args[0]._set_color(FOREGROUND_WHITE)
        # print "after"
        return ret

    return new


def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = '\x1b[31m'  # red
        elif levelno >= 40:
            color = '\x1b[31m'  # red
        elif levelno >= 30:
            color = '\x1b[33m'  # yellow
        elif levelno >= 20:
            color = '\x1b[32m'  # green
        elif levelno >= 10:
            color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'  # normal

        ts = time.ctime(args[1].created)
        # normal
        args[1].msg = f'{color}[{ts}] [{args[1].filename}] [{args[1].levelname}] {args[1].msg} \x1b[0m'
        # print "after"
        return fn(*args)

    return new


class AppLogger(glogging.Logger):
    """Custom logger for Gunicorn log messages."""

    def setup(self, cfg):
        """Configure Gunicorn application logging configuration."""
        super().setup(cfg)

        # Override Gunicorn's `error_log` configuration.
        self._set_handler(
            self.error_log,
            cfg.errorlog,
            logging.Formatter(fmt='')
        )


logging.basicConfig(format='', level=logging.DEBUG)
if platform.system() == 'Windows':
    # Windows does not support ANSI escapes and
    # we are using API calls to set the console color
    logging.StreamHandler.emit = add_coloring_to_emit_windows(
        logging.StreamHandler.emit)
else:
    # all non-Windows platforms are supporting ANSI
    # escapes so we use them
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(
        logging.StreamHandler.emit
    )
