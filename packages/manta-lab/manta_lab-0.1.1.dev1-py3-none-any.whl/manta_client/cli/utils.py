import os
import sys
import traceback
from functools import wraps

import click
from click.exceptions import ClickException

from manta_lab.errors import Error


def cli_unsupported(argument):
    print("Unsupported argument `{}`".format(argument))
    sys.exit(1)


class ClickMantaException(ClickException):
    def format_message(self):
        # TODO: change logfile
        orig_type = "{}.{}".format(self.orig_type.__module__, self.orig_type.__name__)
        if issubclass(self.orig_type, Error):
            return click.style(str(self.message), fg="red")
        else:
            return "An Exception was raised, see %s for full traceback.\n" "%s: %s" % (
                "log_file",
                orig_type,
                self.message,
            )


def display_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Error as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(lines)
            click_exc = ClickMantaException(e)
            click_exc.orig_type = exc_type
            raise click_exc(sys.exc_info()[2])

    return wrapper
