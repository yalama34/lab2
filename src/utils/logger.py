import logging
import traceback
import functools
import typer
from pathlib import Path
from .errors import ShellError, NotATarError

logger = logging.getLogger("shell")
if not logger.handlers:
    fh = logging.FileHandler("shell.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)

def catch(command_name, re_raise = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                error_source = getattr(exception, "filename", None)
                if error_source:
                    error_source = ": " + error_source
                else:
                    error_source = ""
                logger.error("%s raised exception: %s", command_name, exception)
                if isinstance(exception, FileNotFoundError):
                    typer.secho(f"{command_name}: No such file or directory" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                elif isinstance(exception, PermissionError):
                    typer.secho(f"{command_name}: Permission denied:" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                elif isinstance(exception, IsADirectoryError):
                    typer.secho(f"{command_name}: Is a directory:" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                elif isinstance(exception, NotADirectoryError):
                    typer.secho(f"{command_name}: Not a directory" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                elif isinstance(exception, UnicodeDecodeError):
                    typer.secho(f"{command_name}: Failed to decode file in UTF-8" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                elif isinstance(exception, ShellError):
                    typer.secho(f"{command_name}: {exception.__getattribute__("message")    }" + error_source,
                                fg=typer.colors.BRIGHT_RED)
                else:
                    typer.secho(f"Unknown exception: {exception}", fg=typer.colors.BRIGHT_RED)
                if re_raise:
                    raise
                return None
        return wrapper
    return decorator




