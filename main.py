#!/usr/bin/env python3
"""By The Numbers - news-image-20261119 entry for wallet w6.

The artwork is a dashboard of oversized figures from 19 November 2026.
This program validates the bundled PNG and publishes it to /output.
"""
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1 * 1024 * 1024

FIGURES = [
    ("13", "years waited for the global launch of GTA VI"),
    ("$190.4M", "record price paid for a Van Gogh at auction"),
    ("EUR 45B", "EU loan proposed for Ukraine, tied to Russian reparations"),
    ("1", "light-day from Earth, the distance Voyager 1 has now reached"),
    ("11,000+", "Ebola cases confirmed in DR Congo"),
    ("$1.4T", "expected market debut valuation for Anthropic"),
]


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def check_image(path: Path) -> int:
    if not path.is_file():
        raise FileNotFoundError(f"missing image: {path}")
    size = path.stat().st_size
    if size == 0:
        raise ValueError("entry.png is empty")
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, limit is {MAX_BYTES}")
    with path.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        raise ValueError("entry.png does not start with a PNG signature")
    return size


def main() -> int:
    try:
        size = check_image(SOURCE)
    except (FileNotFoundError, ValueError) as exc:
        return fail(str(exc))

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)

    print("By The Numbers - 19 November 2026")
    print(f"validated entry.png ({size} bytes) -> {DEST}")
    for value, caption in FIGURES:
        print(f"  {value:>9}  {caption}")
    print("One dashboard, six numbers, a whole day of world news.")
    if DEST.read_bytes()[: len(PNG_MAGIC)] != PNG_MAGIC:
        return fail("copied file failed the PNG signature re-check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
