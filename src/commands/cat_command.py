from pathlib import Path
import typer
from ..utils import logger


class Executor():
    def __init__(self, arguments):
        self.arguments = arguments
    @logger.catch("cat")
    def handle_cat(self):
        path = Path(self.arguments).expanduser().resolve()
        with open(str(path), "r") as file:
            for line in file:
                typer.echo(line, nl=False)
            file.close()