# ruff: noqa
import os
from collections.abc import Sequence
from pathlib import Path
import argparse

BASE_DIR = Path(__file__).parent.resolve()

DEFAULT_PRODUCTION_DOTENVS_DIR = BASE_DIR / ".envs" / ".production"
DEFAULT_PRODUCTION_DOTENV_FILES = [
    DEFAULT_PRODUCTION_DOTENVS_DIR / ".django",
    DEFAULT_PRODUCTION_DOTENVS_DIR / ".postgres",
]
DEFAULT_LOCAL_DOTENVS_DIR = BASE_DIR / ".envs" / ".local"
DEFAULT_LOCAL_DOTENV_FILES = [
    DEFAULT_LOCAL_DOTENVS_DIR / ".django",
    DEFAULT_LOCAL_DOTENVS_DIR / ".postgres",
]
DEFAULT_OUTPUT_FILE = BASE_DIR / ".env"


def merge(
    output_file: Path,
    files_to_merge: Sequence[Path],
) -> None:
    merged_content = ""
    for merge_file in files_to_merge:
        if merge_file.exists():
            merged_content += merge_file.read_text()
            merged_content += os.linesep
        else:
            print(f"Warning: {merge_file} does not exist and will be skipped.")
    output_file.write_text(merged_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge dotenv files into a single .env file."
    )
    parser.add_argument(
        "--env",
        choices=["production", "local"],
        default="production",
        help="Specify whether to merge files from .envs/.production or .envs/.local. Default is 'production'.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help="Output .env file. Default is '.env' in the current directory.",
    )

    args = parser.parse_args()

    if args.env == "production":
        dotenv_files = DEFAULT_PRODUCTION_DOTENV_FILES
    elif args.env == "local":
        dotenv_files = DEFAULT_LOCAL_DOTENV_FILES
    else:
        raise ValueError("Invalid --env option. Must be 'production' or 'local'.")

    merge(args.output, dotenv_files)
