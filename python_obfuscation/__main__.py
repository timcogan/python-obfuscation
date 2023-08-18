import argparse

from .obfuscation import compile_and_replace


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile Python (.py) files and replace them with bytecode (.pyc) files."
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=".",
        help="Directory to start the compilation and replacement. Default is the current directory.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    compile_and_replace(args.directory)


if __name__ == "__main__":
    main()
