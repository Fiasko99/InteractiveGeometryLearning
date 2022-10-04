import os
import sys
from pathlib import Path


def resource_path(*args):
    """Получить абсолютный путь к файлу."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = str(Path(__file__).parent.parent.parent)

    return os.path.join(base_path, *args)
