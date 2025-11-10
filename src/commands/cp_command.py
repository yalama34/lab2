import typer
import os
from pathlib import Path
import shutil
from ..utils import logger
import errno
from ..utils.errors import MissingFlagError, OverwriteNonDirectoryError

class Executor():
    def __init__(self, recursive, arguments):
        self.arguments = arguments
        self.recursive = recursive
    @logger.catch("cp")
    def handle_cp(self):
        copy_what, copy_to = self.arguments
        copy_what = Path(copy_what).expanduser().resolve()
        if not copy_what.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(copy_what))
        copy_to = Path(copy_to).expanduser().resolve()
        if copy_what.is_file():
            shutil.copy2(str(copy_what), str(copy_to))
        elif copy_what.is_dir():
            if not self.recursive:
                raise MissingFlagError(f"-r not specified; omitting directory '{copy_what}'", str(copy_what))
            if not copy_to.is_dir():
                raise OverwriteNonDirectoryError(f"cannot overwrite non-directory '{copy_to}' with directory '{copy_what}'")
            shutil.copytree(copy_what, copy_to, dirs_exist_ok=True)





