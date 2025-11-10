from pathlib import Path
from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def patch_resolve(monkeypatch):
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: self)

def test_grep_simple_match(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    fs.create_dir("data")
    fs.create_file("data/a.txt", contents="Hello\nworld")
    fs.create_file("data/b.txt", contents="no match")

    result = runner.invoke(app, ["grep", "world", "data"])

    assert result.exit_code == 0
    assert "a.txt: 2 world" in result.stdout

def test_grep_recursive_case_insensitive(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    fs.create_dir("data")
    fs.create_file("data/a.txt", contents="ALPHA")
    fs.create_file("data/b.txt", contents="alpha")

    result = runner.invoke(app, ["grep","-i", "alpha", "data"])

    assert result.exit_code == 0
    assert "\\a.txt: 1 ALPHA" in result.stdout
    assert "\\b.txt: 1 alpha" in result.stdout

def test_grep_no_matches(fs: FakeFilesystem, monkeypatch):
    patch_resolve(monkeypatch)
    fs.create_dir("data")
    fs.create_file("data/a.txt", contents="one\ntwo")

    result = runner.invoke(app, ["grep", "missing", "data"])

    assert result.exit_code == 0
    assert result.stdout.strip() == ""