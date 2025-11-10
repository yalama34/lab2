import os
from pathlib import Path

IS_UNIX = os.name == "posix"
TRASH_DIR = Path(__file__).parent.parent / ".trash"
TRASH_DIR.mkdir(exist_ok=True)

