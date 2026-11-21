"""News-image entry for make.fun, competition news-image-20261120.
The image itself is entry.png beside this file, drawn by build_image.py
(a Pillow newspaper front page for Friday 20 November 2026).
This program only copies it to the output directory, so both grader
runs produce the same bytes. Standard library only.
Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
# Copy, never re-encode: the judge must see exactly the bytes we drew.
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
