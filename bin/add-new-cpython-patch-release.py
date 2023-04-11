#!/usr/bin/env python3

import hashlib
import sys
from urllib.request import urlopen
from pathlib import Path

PYTHON_BUILD_PATH = Path(__file__).parent / "../plugins/python-build/share/python-build"


def generate_new_line(line, major, minor, patch, ext):
    line_components = line.lstrip().split(" ")
    python_url = f"https://www.python.org/ftp/python/{major}.{minor}.{patch}/Python-{major}.{minor}.{patch}.{ext}"
    with urlopen(python_url) as f:
        checksum = hashlib.file_digest(f, "sha256")

    line_components[1] = f'"Python-{major}.{minor}.{patch}"'
    line_components[2] = f'"{python_url}#{checksum.hexdigest()}"'

    new_line = " ".join(line_components)

    indent_len = len(line) - len(line.lstrip())
    indent = " " * indent_len

    return f"{indent}{new_line}"


def main():
    python_version = sys.argv[1]
    major, minor, patch = python_version.split('.')
    previous_version = f"{major}.{minor}.{int(patch) - 1}"
    with open(PYTHON_BUILD_PATH / previous_version) as fh:
        template = fh.readlines()

    for idx, line in enumerate(template):
        if f"Python-{major}.{minor}" not in line:
            continue
        for ext in ("tar.xz", "tgz"):
            if ext in line:
                new_line = generate_new_line(line, major, minor, patch, ext)
                template[idx] = new_line

    with open(PYTHON_BUILD_PATH / python_version, 'w') as fh:
        fh.writelines(template)


if __name__ == '__main__':
    main()
