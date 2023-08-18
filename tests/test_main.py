import runpy
import sys
from pathlib import Path


def test_compile_and_replace(tmpdir):
    tmpdir = Path(tmpdir)
    test_file = tmpdir / "sample.py"
    with open(test_file, "w") as fp:
        fp.write("print('Hello, world!')")

    sys.argv = [sys.argv[0], "--directory", str(tmpdir)]
    runpy.run_module("python_obfuscation", run_name="__main__", alter_sys=True)

    assert not test_file.is_file()
    assert len(list(tmpdir.rglob("*.pyc"))) == 1
