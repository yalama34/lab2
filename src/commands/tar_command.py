from pathlib import Path
from ..utils import logger
import tarfile
from ..utils.errors import NotATarError
import errno
import os

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments

    @logger.catch("tar")
    def handle_tar(self):
        source, tar_name = self.arguments
        source = Path(source).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(source))
        if not tar_name.endswith(".tar.gz"):
            raise NotATarError(f"Filename file must end with .tar.gz")
        with tarfile.TarFile(tar_name, "w") as tar:
            for item in source.rglob("*"):
                tar.add(item, arcname=item.relative_to(source))

