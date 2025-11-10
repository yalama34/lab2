from pathlib import Path
import typer
from ..utils import logger
from .constants import TRASH_DIR
import shutil

class Executor():
    def __init__(self, arguments, recursive):
        self.arguments = arguments
        self.recursive = recursive
    @logger.catch("rm")
    def handle_rm(self):
        path = Path(self.arguments).expanduser().resolve()
        if path.is_dir():
            if typer.confirm("You are trying to delete a directory. Continue?"):
                shutil.move(path, TRASH_DIR)
            else:
                typer.echo("Cancelling command")
        else:
            shutil.move(path, TRASH_DIR)