"""Entry for make.fun's news-image-20261125 bounty.

The picture of 25 November 2026's world news is drawn ahead of time by
build_image.py and stored in this repository as entry.png. This program
only carries that file to the output directory, using the standard
library alone, so both graded runs write the same bytes.
"""

import os
import shutil


def destination():
    """Where the graded run expects the image."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out, "entry.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target = destination()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(source, target)
    # The graded runs must write the same bytes: refuse a short copy
    # rather than leaving a truncated image behind.
    if os.path.getsize(source) != os.path.getsize(target):
        raise SystemExit("entry.png was not copied whole")


if __name__ == "__main__":
    main()
