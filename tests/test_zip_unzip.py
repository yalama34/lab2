from pathlib import Path
import zipfile
from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def _patch_resolve(monkeypatch):
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: self)

def test_zip_creates_archive(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    fs.create_dir("data")
    fs.create_file("data/a.txt", contents="A")
    fs.create_file("data/b.txt", contents="B")

    result = runner.invoke(app, ["zip", "data", "archive.zip"])
    assert result.exit_code == 0
    assert fs.exists("archive.zip")

    with zipfile.ZipFile("archive.zip", "r") as z:
        names = z.namelist()
    assert any(name.endswith("a.txt") for name in names)
    assert any(name.endswith("b.txt") for name in names)

def test_unzip_extracts_files(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    with zipfile.ZipFile("archive.zip", "w") as z:
        z.writestr("x.txt", "X")
        z.writestr("y.txt", "Y")

    result = runner.invoke(app, ["unzip", "archive.zip"])
    assert result.exit_code == 0
    with open("x.txt", "r") as f:
        assert f.read() == "X"
    with open("y.txt", "r") as f:
        assert f.read() == "Y"

def test_zip_nonexistent_source(fs: FakeFilesystem, monkeypatch):
    _patch_resolve(monkeypatch)
    result = runner.invoke(app, ["zip", "no_such_folder", "archive.zip"])
    assert isinstance(result.exception, FileNotFoundError)