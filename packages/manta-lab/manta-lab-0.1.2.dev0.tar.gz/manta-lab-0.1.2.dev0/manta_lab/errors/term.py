import logging
import sys

import click

DEBUG_STRING = click.style("DEBUG", fg="green")
LOG_STRING = click.style("manta", fg="blue", bold=True)  # same as info
LOG_STRING_NOCOLOR = "manta"
WARN_STRING = click.style("WARNING", fg="yellow")
ERROR_STRING = click.style("ERROR", bg="red", fg="green")
CRITICAL_STRING = click.style("CRITICAL", bg="white", fg="red")
PRINTED_MESSAGES = set()

_silent = False
_show_debugs = True
_show_info = True
_show_warnings = True
_show_errors = True
_show_criticals = True
_logger = None


def termsetup(settings, logger):
    global _silent, _show_debugs, _show_info, _show_warnings, _show_errors, _show_criticals, _logger
    _silent = settings.silent
    _show_debugs = settings._show_debugs
    _show_info = settings._show_info
    _show_warnings = settings._show_warnings
    _show_errors = settings._show_errors
    _show_criticals = settings._show_criticals
    _logger = logger


def termdeug(string, newline=True, repeat=True, prefix=True):
    """Log to standard error with formatting.

    Arguments:
        string (str, optional): The string to print
        newline (bool, optional): Print a newline at the end of the string
        repeat (bool, optional): If set to False only prints the string once per process
        prefix (bool, optional): If set to False only prints the string without prefix
    """
    prefix = DEBUG_STRING if prefix else None
    _log(
        string=string,
        newline=newline,
        repeat=repeat,
        prefix=prefix,
        silent=not _show_debugs,
        level=logging.DEBUG,
    )


def termlog(string="", newline=True, repeat=True, prefix=True):
    prefix = LOG_STRING if prefix else None
    _log(
        string=string,
        newline=newline,
        repeat=repeat,
        prefix=prefix,
        silent=not _show_info,
        level=logging.INFO,
    )


def termwarn(string, newline=True, repeat=True, prefix=True):
    prefix = WARN_STRING if prefix else None
    _log(
        string=string,
        newline=newline,
        repeat=repeat,
        prefix=prefix,
        silent=not _show_warnings,
        level=logging.WARNING,
    )


def termerror(string, newline=True, repeat=True, prefix=True):
    prefix = ERROR_STRING if prefix else None
    _log(
        string=string,
        newline=newline,
        repeat=repeat,
        prefix=prefix,
        silent=not _show_errors,
        level=logging.ERROR,
    )


def termcritical(string, newline=True, repeat=True, prefix=True):
    prefix = CRITICAL_STRING if prefix else None
    _log(
        string=string,
        newline=newline,
        repeat=repeat,
        prefix=prefix,
        silent=not _show_criticals,
        level=logging.CRITICAL,
    )


def _log(string="", newline=True, repeat=True, prefix=None, silent=False, level=logging.INFO):
    if string:
        if prefix:
            line = "\n".join([f"{prefix}: {s}" for s in string.split("\n")])
        else:
            line = string
    else:
        line = ""

    if not repeat and line in PRINTED_MESSAGES:
        return

    # Repeated line tracking limited to 1k messages
    if len(PRINTED_MESSAGES) < 1000:
        PRINTED_MESSAGES.add(line)

    global _logger
    silent = silent or _silent
    if silent:
        if level == logging.DEBUG:
            _logger.debug(line)
        elif level == logging.INFO:
            _logger.info(line)
        elif level == logging.WARNING:
            _logger.warning(line)
        elif level == logging.ERROR:
            _logger.error(line)
        elif level == logging.CRITICAL:
            _logger.critical(line)
        else:
            raise AttributeError()
    else:
        click.echo(line, file=sys.stderr, nl=newline)
