from pathlib import Path
from ..utils import logger
import tarfile
from ..utils.errors import NotATarError

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments

    @logger.catch("untar")
    def handle_untar(self):
        source = Path(self.arguments).expanduser().resolve()
        if not str(source).endswith(".tar.gz"):
            raise NotATarError(f"Filename must end with .zip")
        with tarfile.TarFile(source, "r") as tar:
            tar.extractall(source.parent)