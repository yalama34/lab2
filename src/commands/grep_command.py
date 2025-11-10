import re
from pathlib import Path
import typer
from datetime import datetime
from stat import filemode
from ..utils import logger

class Executor():
    def __init__(self, arguments, recursive, no_register):
        self.arguments = arguments
        self.recursive = recursive
        self.no_register = no_register
    @logger.catch("grep")
    def handle_grep(self):
        pattern, path = self.arguments
        path = Path(path).expanduser()
        flags = re.IGNORECASE if self.no_register else 0
        regex = re.compile(pattern, flags)
        files = path.rglob("*") if self.recursive else path.glob("*")
        for file in files:
            with file.open("r", encoding="utf-8") as file:
                for lineno, line in enumerate(file, start=1):
                    if regex.search(line):
                        typer.echo(f"{file.name}: {lineno} {line.strip()}")

