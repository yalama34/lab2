from pyfakefs.fake_filesystem import FakeFilesystem, FakeFileOpen
from typer.testing import CliRunner
from src.main import app
from src.utils.errors import MissingFlagError, OverwriteNonDirectoryError

runner = CliRunner()

def test_cp_source_not_found(fs: FakeFilesystem):
    fs.create_dir("data")

    result = runner.invoke(app, ["cp", "data/missing.txt", "data/target.txt"])

    assert isinstance(result.exception, FileNotFoundError)

def test_cp_target_directory_missing(fs: FakeFilesystem):
    fs.create_file("source.txt", contents="data")

    result = runner.invoke(app, ["cp", "source.txt", "missing_dir/target.txt"])

    assert isinstance(result.exception, FileNotFoundError)

def test_cp_source_is_directory(fs: FakeFilesystem):
    fs.create_dir("data")

    result = runner.invoke(app, ["cp", "data", "copy.txt"])

    assert isinstance(result.exception, MissingFlagError)

def test_cp_cant_overwrite(fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file("data/1.txt")
    fs.create_file("data/2.txt")
    fs.create_file("data/3.txt")
    fs.create_file("source")
    result = runner.invoke(app, ["cp", "-r", "data", "source"])
    assert isinstance(result.exception, OverwriteNonDirectoryError)