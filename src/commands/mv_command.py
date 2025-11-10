from pathlib import Path
import typer
from colorama import init, Fore
from datetime import datetime
from ..utils import logger
from ..utils.errors import SameFileError, InvalidMoveError
import shutil
import os

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments
    @logger.catch("mv")
    def handle_mv(self):
        move_what, move_to = self.arguments
        move_what = Path(move_what).expanduser().resolve()
        move_to = Path(move_to).expanduser().resolve()
        if move_what.samefile(move_to):
            raise SameFileError(message=f"'{move_what}' and '{move_to}' are the same file")
        if move_what.is_dir() and move_to.exists() and move_to.is_file():
            raise InvalidMoveError(message=f"'cannot overwrite non-directory '{move_to}' with directory '{move_what}'")
        shutil.move(move_what, move_to)