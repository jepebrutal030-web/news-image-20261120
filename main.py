#!/usr/bin/env python3
"""Write the 20 November 2026 world-news image to the output directory.

The entry image lives in the repository at assets/entry.png (a 1024x1024
infographic summing up the world news of Friday 20 November 2026). This
program copies it to /output/entry.png, creating the output directory when
needed, and verifies the copy with SHA-256 so both grading runs produce
byte-identical output.

Run:  python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")
OUTPUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

MAX_BYTES = 1048576
MAX_SIDE = 1024


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.exists(SOURCE):
        print("missing source image: " + SOURCE, file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print("error: source image is %d bytes, over the 1 MiB cap" % size,
              file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    src = digest(SOURCE)
    out = digest(OUTPUT)
    print("copied " + SOURCE + " -> " + OUTPUT)
    print("sha256: " + out)
    if src != out:
        print("error: output differs from source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
