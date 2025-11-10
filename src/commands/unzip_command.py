from pathlib import Path
from ..utils import logger
import zipfile
from ..utils.errors import NotAZipError

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments

    @logger.catch("unzip")
    def handle_unzip(self):
        source = Path(self.arguments).expanduser().resolve()
        if not str(source).endswith(".zip"):
            raise NotAZipError(f"Filename must end with .zip")
        with zipfile.ZipFile(source, "r") as zip:
            zip.extractall(source.parent)
