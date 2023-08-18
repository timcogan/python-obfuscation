from pathlib import Path

from python_obfuscation.obfuscation import compile_and_replace


def test_compile_and_replace(tmpdir):
    tmpdir = Path(tmpdir)
    test_file = tmpdir / "sample.py"
    with open(test_file, "w") as fp:
        fp.write("print('Hello, world!')")

    compile_and_replace(tmpdir)

    assert not test_file.is_file()
    assert len(list(tmpdir.rglob("*.pyc"))) == 1


def test_compile_and_replace_nested(tmpdir):
    tmpdir = Path(tmpdir)
    nested_dir = tmpdir / "nested_dir"
    nested_dir.mkdir()
    test_file = nested_dir / "sample.py"
    with open(test_file, "w") as fp:
        fp.write("print('Hello, world!')")

    compile_and_replace(tmpdir)

    assert not test_file.is_file()
    assert len(list(nested_dir.rglob("*.pyc"))) == 1
