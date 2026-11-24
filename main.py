#!/usr/bin/env python3
"""Ship the entry image to the output directory.

The front page (entry.png, 1024x1024) was drawn at build time with
Pillow; this program only delivers it. It uses the standard library
alone, so it runs in the grader's container: it checks the file is a
PNG of the expected size, copies it to $MAKEFUN_OUTPUT_DIR (or
/output), and verifies the copy byte for byte. The image itself is
committed beside this program in the repository.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = "entry.png"
EXPECTED = (1024, 1024)


def read_header(path):
    """Return the PNG dimensions from the IHDR chunk, or fail."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR first")
    return struct.unpack(">II", head[16:24])


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    try:
        size = read_header(src)
    except (OSError, ValueError) as exc:
        print(f"entry.png failed checks: {exc}", file=sys.stderr)
        sys.exit(1)
    if size != EXPECTED:
        print(f"expected {EXPECTED[0]}x{EXPECTED[1]}, got "
              f"{size[0]}x{size[1]}", file=sys.stderr)
        sys.exit(1)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, ENTRY)
    shutil.copyfile(src, dst)
    if sha256_of(src) != sha256_of(dst):
        print("entry.png copy failed verification", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
