from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def test_cat_nonexistent_file(fs: FakeFilesystem):
    fs.create_file("file.txt", contents="")
    result = runner.invoke(app, ["cat", "nonexistent.txt"])
    assert isinstance(result.exception, FileNotFoundError)

def test_cat_dir(fs: FakeFilesystem):
    fs.create_dir("data")
    result = runner.invoke(app, ["cat", "data"])
    assert isinstance(result.exception, PermissionError)

