from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def test_ls_existing_directory(fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file("data/file1.txt")
    fs.create_file("data/file2.txt")
    result = runner.invoke(app, ["ls", "data"])
    assert result.exit_code == 0

def test_ls_is_file(fs: FakeFilesystem):
    fs.create_file("file.txt")
    result = runner.invoke(app, ["ls", "file.txt"])
    assert isinstance(result.exception, NotADirectoryError)

def test_ls_not_existing_directory(fs: FakeFilesystem):
    fs.create_dir("exists")
    result = runner.invoke(app, ["ls", "nonexists"])
    assert isinstance(result.exception, FileNotFoundError)

def test_ls_detailed(fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file("data/file1.txt")
    fs.create_file("data/file2.txt")
    result = runner.invoke(app, ["ls", "-l", "data"])
    assert result.exit_code == 0






