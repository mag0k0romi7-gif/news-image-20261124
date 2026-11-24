#!/usr/bin/env python3
"""news-image-20261124 rev2 entrypoint (Python 3.13, standard library only).

The entry image is the entry.png beside this file: a 1024x1024 rendering of
50 stories from Tuesday, 24 November 2026, grouped into 9 regions. The
program copies it to the output directory, as the kit's starter does; a copy
is byte-identical every run, so the grader's two runs always agree.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
