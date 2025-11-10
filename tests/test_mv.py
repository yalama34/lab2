from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app
from src.utils.errors import SameFileError, InvalidMoveError

runner = CliRunner()

def test_mv_success(fs: FakeFilesystem):
    fs.create_dir("data")
    fs.create_file("source.txt")
    result = runner.invoke(app, ["mv", "source.txt", "data"])
    assert result.exit_code == 0

def test_mv_source_not_found(fs: FakeFilesystem):
    fs.create_dir("data")
    result = runner.invoke(app, ["mv", "data/missing.txt", "data/target.txt"])
    if result.exception is None:
        assert "No such file or directory" in result.stdout or "not found" in result.stdout
    else:
        assert isinstance(result.exception, FileNotFoundError)

def test_mv_target_directory_missing(fs: FakeFilesystem):
    fs.create_file("source.txt", contents="data")
    result = runner.invoke(app, ["mv", "source.txt", "missing_dir/target.txt"])
    if result.exception is None:
        assert "No such file or directory" in result.stdout or "not found" in result.stdout
    else:
        assert isinstance(result.exception, FileNotFoundError)

def test_mv_source_is_directory_over_file_invalid(fs: FakeFilesystem):
    fs.create_dir("dir_to_move")
    fs.create_file("file.txt", contents="x")
    result = runner.invoke(app, ["mv", "dir_to_move", "file.txt"])
    if result.exception is None:
        assert "cannot overwrite non-directory" in result.stdout or "Not a directory" in result.stdout
    else:
        assert isinstance(result.exception, InvalidMoveError)

def test_mv_same_file(fs: FakeFilesystem):
    fs.create_file("file.txt", contents="x")
    result = runner.invoke(app, ["mv", "file.txt", "file.txt"])
    if result.exception is None:
        assert "same file" in result.stdout or "are the same file" in result.stdout
    else:
        assert isinstance(result.exception, SameFileError)

def test_mv_overwrite_file(fs: FakeFilesystem):
    fs.create_file("source.txt", contents="new")
    fs.create_file("target.txt", contents="old")
    result = runner.invoke(app, ["mv", "source.txt", "target.txt"])
    assert result.exit_code == 0
    with open("target.txt", "r") as f:
        assert f.read() == "new"
    assert not fs.exists("source.txt")

def test_mv_dir_into_dir(fs: FakeFilesystem):
    fs.create_dir("srcdir")
    fs.create_file("srcdir/a.txt", contents="a")
    fs.create_dir("destdir")
    # переместим srcdir внутрь destdir
    result = runner.invoke(app, ["mv", "srcdir", "destdir"])
    assert result.exit_code == 0
    assert fs.exists("destdir/srcdir/a.txt")