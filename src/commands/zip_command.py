from pathlib import Path
from ..utils import logger
import zipfile
from ..utils.errors import NotAZipError
import errno
import os

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments

    @logger.catch("zip")
    def handle_zip(self):
        source, zip_name = self.arguments
        source = Path(source).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(source))
        if not zip_name.endswith(".zip"):
            raise NotAZipError(f"Filename file must end with .zip")
        with zipfile.ZipFile(zip_name, "w") as zip:
            for item in source.rglob("*"):
                zip.write(item, arcname=item.relative_to(source))
