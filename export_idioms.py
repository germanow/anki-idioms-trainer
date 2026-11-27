#!/usr/bin/env python3
"""Export the "Idioms and Phrases" deck to idioms.json so later steps don't need Anki open.

Order: new cards first, in Anki's new-queue order, then learned cards. Suspended cards are skipped.
Each record is {note_id, phrase, definition, example, learned}.
"""

import json

from random_idiom import DECK, anki, plain


def export(learned):
    query = f'deck:"{DECK}" -is:suspended ' + ("-is:new" if learned else "is:new")
    cards = sorted(anki("cardsInfo", cards=anki("findCards", query=query)),
                   key=lambda c: (c["due"], c["note"]))
    for card in cards:
        fields = {name: plain(field["value"]) for name, field in card["fields"].items()}
        yield {"note_id": card["note"], "phrase": fields.get("Phrase/Idiom", ""),
               "definition": fields.get("Definition", ""), "example": fields.get("Example", ""),
               "learned": learned}


def main():
    idioms, seen = [], set()
    for idiom in [*export(False), *export(True)]:
        if idiom["note_id"] not in seen:
            seen.add(idiom["note_id"])
            idioms.append(idiom)
    with open("idioms.json", "w") as f:
        json.dump(idioms, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(idioms)} idioms ({sum(i['learned'] for i in idioms)} learned) to idioms.json")


if __name__ == "__main__":
    main()
