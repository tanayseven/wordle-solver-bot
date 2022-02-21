import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

_screen_shot_location: Optional[str] = None


@contextmanager
def new_working_directory_location(directory_location: Optional[str] = None):
    global _screen_shot_location
    if directory_location is None:
        directory_location = str(tempfile.TemporaryDirectory().name)
    _screen_shot_location = str(Path(directory_location).absolute() / "screen_shot.png")
    if Path(directory_location).exists():
        shutil.rmtree(str(Path(directory_location)))
    Path(directory_location).mkdir()
    yield
    if Path(directory_location).exists():
        shutil.rmtree(str(Path(directory_location)))


def screen_shot_location():
    return _screen_shot_location
