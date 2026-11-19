"""19 NOV 2026 By The Numbers — a counted view of the day.

Six big figures carry Thursday, 19 November 2026: 13 years of
waiting for a game, 45 billion euros for Ukraine, one light-day
for a probe, $190.4m for a painting, 11,000 Ebola cases and a
$1.4tn would-be debut. The dashboard is entry.png; this program
is its publisher.
"""

import shutil
from pathlib import Path

FIGURES = [
    ("13", "YEARS OF WAITING", "ended as GTA VI finally launches worldwide"),
    ("EUR 45bn", "FOR UKRAINE", "EU loan proposal, repaid from reparations"),
    ("1", "LIGHT-DAY", "Voyager 1's distance from Earth, a NASA first"),
    ("$190.4m", "FOR A VAN GOGH", "record auction price after a history dispute"),
    ("11,000", "EBOLA CASES", "DR Congo outbreak more than doubles"),
    ("$1.4tn", "ANTHROPIC DEBUT", "the Claude maker eyes a giant listing"),
]
ALSO = "Trump-Xi-Putin in Shenzhen · Cyclone Akvan · Crimean Bridge struck · Fed hints at hikes"
METHOD = "Every figure was reported on 19 November 2026; nothing older is counted."


def entry_file() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def png_chunks_ok(blob: bytes) -> bool:
    """Walk the PNG chunk table: every chunk must be complete."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    pos = 8
    while pos + 8 <= len(blob):
        length = int.from_bytes(blob[pos:pos + 4], "big")
        pos += 8 + length + 4
        if pos > len(blob):
            return False
    return pos == len(blob)


def main() -> None:
    src = entry_file()
    blob = src.read_bytes()
    if not png_chunks_ok(blob):
        raise SystemExit("entry.png has a broken chunk table")
    if len(blob) > 1_048_576:
        raise SystemExit("entry.png breaks the 1 MiB cap")
    out = Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)
    print("19 NOV 2026 BY THE NUMBERS")
    for num, label, note in FIGURES:
        print(f"  {num} — {label}: {note}")
    print(f"  also: {ALSO}")
    print(f"dashboard delivered to {out}")


if __name__ == "__main__":
    main()
