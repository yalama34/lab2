from pyfakefs.fake_filesystem import FakeFilesystem
from typer.testing import CliRunner
from src.main import app

runner = CliRunner()

def test_cd_nonexistent_directory(fs: FakeFilesystem):
    fs.create_dir("exists")

    result = runner.invoke(app, ["cd", "nonexistent"])
    assert isinstance(result.exception, FileNotFoundError)

