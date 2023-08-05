import logging
import os


def _safe_symlink(base, target, name, delete=False):
    if not hasattr(os, "symlink"):
        return

    symlink_path = os.path.join(base, name)
    logfile_relpath = os.path.relpath(target, base)
    # delete old symlink
    if delete:
        try:
            os.remove(symlink_path)
        except OSError:
            pass
    try:
        os.symlink(logfile_relpath, symlink_path)
    except OSError:
        pass


def create_symlinks(settings):
    if settings.use_symlink:
        _safe_symlink(
            os.path.dirname(settings.log_symlink_user_file),
            settings.log_user_file,
            os.path.basename(settings.log_symlink_user_file),
            delete=True,
        )
        _safe_symlink(
            os.path.dirname(settings.log_symlink_internal_file),
            settings.log_internal_file,
            os.path.basename(settings.log_symlink_internal_file),
            delete=True,
        )


def activate_logging_handler(logger: logging.Logger, log_fname: str):
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(threadName)-10s:%(process)d "
        "[%(filename)s:%(funcName)s():%(lineno)s] %(message)s"
    )

    handler = logging.FileHandler(log_fname)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.propagate = False
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def teardown_logger(logger):
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
