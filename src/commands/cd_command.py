import os
from pathlib import Path
from ..utils import logger

class Executor():
    def __init__(self, arguments):
        self.arguments = arguments

    @logger.catch("cd")
    def handle_cd(self):
        path = Path(self.arguments).expanduser().resolve()
        os.chdir(path)

