from pathlib import Path
import tarfile
import io
from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def patch_resolve(monkeypatch):
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: self)

def test_tar_creates_archive(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    fs.create_dir("data")
    fs.create_file("data/a.txt", contents="A")
    fs.create_file("data/b.txt", contents="B")

    result = runner.invoke(app, ["tar", "data", "archive.tar.gz"])
    assert result.exit_code == 0
    assert fs.exists("archive.tar.gz")

    with tarfile.open("archive.tar.gz", "r") as t:
        names = t.getnames()
    assert any(name.endswith("a.txt") for name in names)
    assert any(name.endswith("b.txt") for name in names)

def test_untar_extracts_files(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    with tarfile.open("archive.tar.gz", "w") as t:
        info = tarfile.TarInfo("x.txt")
        data = b"X"
        info.size = len(data)
        t.addfile(info, io.BytesIO(data))

        info = tarfile.TarInfo("y.txt")
        data = b"Y"
        info.size = len(data)
        t.addfile(info, io.BytesIO(data))

    result = runner.invoke(app, ["untar", "archive.tar.gz"])
    assert result.exit_code == 0
    with open("x.txt", "r") as f:
        assert f.read() == "X"
    with open("y.txt", "r") as f:
        assert f.read() == "Y"

def test_tar_nonexistent(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    result = runner.invoke(app, ["tar", "no_such_folder", "archive.tar.gz"])
    assert isinstance(result.exception, FileNotFoundError)