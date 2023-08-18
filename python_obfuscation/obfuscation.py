import compileall
import os
import shutil
from pathlib import Path


def compile_and_replace(dir_path: Path):
    compileall.compile_dir(dir_path, force=True)

    # Move .pyc files from __pycache__ to the parent directory
    for root, dirs, files in os.walk(dir_path):
        if "__pycache__" in root:
            for file in files:
                if file.endswith(".pyc"):
                    pyc_path = os.path.join(root, file)
                    new_path = os.path.join(os.path.dirname(root), file)
                    shutil.move(pyc_path, new_path)

    # Delete .py files
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                os.remove(os.path.join(root, file))

    # Delete empty __pycache__ directories
    for root, dirs, _ in os.walk(dir_path):
        if "__pycache__" in dirs:
            cache_dir = os.path.join(root, "__pycache__")
            if not os.listdir(cache_dir):
                os.rmdir(cache_dir)
