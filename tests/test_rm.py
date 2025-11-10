from pathlib import Path
import typer
from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app
from src.commands.constants import TRASH_DIR

runner = CliRunner()

def _patch_resolve(monkeypatch):
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: self)

def test_rm_file_moves_to_trash(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    fs.create_dir(str(TRASH_DIR))
    fs.create_file("file.txt", contents="hello")

    result = runner.invoke(app, ["rm", "file.txt"])

    assert result.exit_code == 0
    assert not fs.exists("file.txt")
    with open(str(Path(TRASH_DIR) / "file.txt"), "r") as f:
        assert f.read() == "hello"

def test_rm_directory_confirm_yes(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    monkeypatch.setattr(typer, "confirm", lambda prompt: True)

    fs.create_dir("dir_to_remove")
    fs.create_file("dir_to_remove/a.txt", contents="a")
    fs.create_dir(str(TRASH_DIR))

    result = runner.invoke(app, ["rm", "dir_to_remove", "-r"])

    assert result.exit_code == 0
    assert not fs.exists("dir_to_remove")
    assert fs.exists(str(Path(TRASH_DIR) / "dir_to_remove" / "a.txt"))

def test_rm_directory_confirm_no(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    monkeypatch.setattr(typer, "confirm", lambda prompt: False)

    fs.create_dir("dir_keep")
    fs.create_file("dir_keep/a.txt", contents="a")

    result = runner.invoke(app, ["rm", "dir_keep", "-r"])

    assert result.exit_code == 0
    assert "Cancelling command" in result.stdout
    assert fs.exists("dir_keep")