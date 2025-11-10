import typer
from .commands import (ls_command, cd_command,
                       cat_command, cp_command,
                       mv_command, rm_command,
                       zip_command, unzip_command,
                       tar_command, untar_command,
                       grep_command)
from typing import List
import shlex
import os
from .utils.logger import logger
from pathlib import Path

home_directory = os.path.expanduser('~')
os.chdir(home_directory)

app = typer.Typer()

@app.command()
def ls(
        path: str = typer.Argument("."),
        detailed: bool = typer.Option(False, "-l")
):
    executor = ls_command.Executor(detailed=detailed, arguments=path)
    executor.handle_ls()

@app.command()
def cd(
        path: str = typer.Argument("."),
):
    executor = cd_command.Executor(arguments=path)
    executor.handle_cd()

@app.command()
def cat(
        path: str = typer.Argument(...),
):
    executor = cat_command.Executor(arguments=path)
    executor.handle_cat()

@app.command()
def cp(
        copy_what: str = typer.Argument(...),
        copy_to: str = typer.Argument(...),
        recursive: bool = typer.Option(False, "-r")
):
    executor = cp_command.Executor(recursive=recursive, arguments=[copy_what, copy_to])
    executor.handle_cp()

@app.command()
def mv(
        move_what: str = typer.Argument(...),
        move_to: str = typer.Argument(...),
):
    executor = mv_command.Executor(arguments=[move_what, move_to])
    executor.handle_mv()

@app.command()
def rm(
        path: str = typer.Argument(...),
        recursive: bool = typer.Option(False, "-r")
):
    executor = rm_command.Executor(arguments=path, recursive=recursive)
    executor.handle_rm()

@app.command()
def zip(
        source: str = typer.Argument(...),
        zip_name: str = typer.Argument(...),
):
    executor = zip_command.Executor(arguments=[source, zip_name])
    executor.handle_zip()

@app.command()
def unzip(
        source: str = typer.Argument(...),
):
    executor = unzip_command.Executor(arguments=source)
    executor.handle_unzip()

@app.command()
def tar(
        source: str = typer.Argument(...),
        tar_name: str = typer.Argument(...),
):
    executor = tar_command.Executor(arguments=[source, tar_name])
    executor.handle_tar()

@app.command()
def untar(
        source: str = typer.Argument(...),
):
    executor = untar_command.Executor(arguments=source)
    executor.handle_untar()

@app.command()
def grep(
        pattern: str = typer.Argument(...),
        path: str = typer.Argument(...),
        recursive: bool = typer.Option(False, "-r"),
        no_register: bool = typer.Option(False, "-i")
):
    executor = grep_command.Executor(arguments=[pattern, path], recursive=recursive, no_register=no_register)
    executor.handle_grep()

"""
@app.command()
def touch(
        path: str = typer.Argument(...),
):
    path = Path(path).expanduser().resolve()
    path.touch(exist_ok=True)

@app.command()
def mkdir(
        path: str = typer.Argument(...),
):
    path = Path(path).expanduser().resolve()
    path.mkdir(exist_ok=True)
"""

def main():
    typer.echo("Оболочка запущена")
    while True:
        command = shlex.split(input(f"{os.getcwd()}>>> "))
        logger.info("%s", ' '.join(command))
        try:
            app(command)
        except SystemExit:
            pass


if __name__ == "__main__":
    main()