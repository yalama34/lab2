import os
from pathlib import Path
import typer
from datetime import datetime
from stat import filemode
from ..utils import logger

class Executor():
    def __init__(self, detailed, arguments):
        self.detailed = detailed
        self.arguments = arguments

    @logger.catch("ls")
    def handle_ls(self):
        cur_path = Path(self.arguments).expanduser().resolve()
        if self.detailed:
            for item in cur_path.iterdir():
                permissions = filemode(item.stat().st_mode)
                m_time = item.stat().st_mtime
                m_time = str(datetime.fromtimestamp(m_time))
                fsize = os.path.getsize(item.absolute())
                info_message = permissions + " " + m_time + " " + str(fsize) + " bytes"
                typer.echo(info_message + " ", nl=False)
                if item.is_dir():
                    typer.secho(item.name, fg=typer.colors.BLUE)
                else:
                    typer.echo(item.name)
        else:
            for item in cur_path.iterdir():
                if item.is_dir():
                    typer.secho(item.name + " ", nl=False, fg=typer.colors.BLUE)
                else:
                    typer.echo(item.name + " ", nl =False)
            typer.echo("\n")




