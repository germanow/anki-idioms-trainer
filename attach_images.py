#!/usr/bin/env python3
"""Step 4: attach shrunk small/<note_id>.jpg to Anki notes via AnkiConnect.

Attaches whatever images exist now and records each note in attached.json, so rerunning only
attaches new images. Needs an "Image" field on the note type and {{Image}} in the card template.
Back up the collection first.
"""

import argparse
import base64
import json
import os
import sys

from random_idiom import anki


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, help="stop after attaching this many images")
    limit = parser.parse_args().count
    attached = set(json.load(open("attached.json"))) if os.path.exists("attached.json") else set()
    order = [str(i["note_id"]) for i in json.load(open("idioms.json"))]
    todo = [n for n in order if n not in attached and os.path.exists(f"small/{n}.jpg")][:limit]
    if not todo:
        return print("Nothing new to attach.")
    fields = anki("notesInfo", notes=[int(todo[0])])[0]["fields"]
    if "Image" not in fields:
        sys.exit('Add an "Image" field to the idiom note type (and {{Image}} to the card template) first.')
    for n, note_id in enumerate(todo, 1):
        name = f"idiom_{note_id}.jpg"
        with open(f"small/{note_id}.jpg", "rb") as f:
            anki("storeMediaFile", filename=name, data=base64.b64encode(f.read()).decode())
        anki("updateNoteFields", note={"id": int(note_id), "fields": {"Image": f'<img src="{name}">'}})
        attached.add(note_id)
        with open("attached.json", "w") as f:
            json.dump(sorted(attached), f, indent=0)
        print(f"{n}/{len(todo)} {name}", flush=True)


if __name__ == "__main__":
    main()
