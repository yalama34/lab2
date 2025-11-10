import errno
from pathlib import Path
import typer
from ..utils import logger
from .constants import TRASH_DIR, HOME_DIR, ROOT_DIR
import shutil
import os

class Executor():
    def __init__(self, arguments, recursive):
        self.arguments = arguments
        self.recursive = recursive
    @logger.catch("rm")
    def handle_rm(self):
        path = Path(self.arguments).expanduser().resolve()
        if path in (ROOT_DIR, HOME_DIR) or path == HOME_DIR.parent:
            raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), str(self.arguments))

        if path.is_dir():
            if not self.recursive:
                raise NotADirectoryError(errno.EACCES, os.strerror(errno.EACCES), str(path))
            if typer.confirm("You are trying to delete a directory. Continue?"):
                shutil.move(path, TRASH_DIR)
            else:
                typer.echo("Cancelling command")
        else:
            shutil.move(path, TRASH_DIR)