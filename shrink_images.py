#!/usr/bin/env python3
"""Step 3: shrink images/<note_id>.png to small/<note_id>.jpg (512 px, JPEG) for Anki, using macOS sips.

Skips images already converted; rerun to convert new ones.
"""

import argparse
import os
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, help="stop after converting this many images")
    limit = parser.parse_args().count
    os.makedirs("small", exist_ok=True)
    todo = sorted(f[:-4] for f in os.listdir("images")
                  if f.endswith(".png") and f[:-4].isdigit() and not os.path.exists(f"small/{f[:-4]}.jpg"))
    for n, note_id in enumerate(todo[:limit], 1):
        tmp = f"small/{note_id}.tmp.jpg"
        subprocess.run(["sips", "-Z", "512", "-s", "format", "jpeg", "-s", "formatOptions", "80",
                        f"images/{note_id}.png", "--out", tmp], check=True, capture_output=True)
        os.replace(tmp, f"small/{note_id}.jpg")
        print(f"{n}/{len(todo)} small/{note_id}.jpg", flush=True)


if __name__ == "__main__":
    main()
