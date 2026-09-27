#!/usr/bin/env python3
"""Pull random learned idioms from the Anki "Idioms and Phrases" deck via AnkiConnect.

"Learned" means the card has left the new queue and is not suspended.
Anki must be running with the AnkiConnect add-on installed.

Prints a JSON list of {phrase, definition}.

Examples:
    ./random_idiom.py           # one random learned idiom
    ./random_idiom.py -n 10     # ten of them
"""

import argparse
import html
import json
import random
import re
import sys
import urllib.error
import urllib.request

ANKI_URL = "http://127.0.0.1:8765"
DECK = "Idioms and Phrases"


def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    request = urllib.request.Request(ANKI_URL, data=payload,
                                    headers={"Content-Type": "application/json"})
    try:
        response = json.load(urllib.request.urlopen(request, timeout=20))
    except urllib.error.URLError as exc:
        sys.exit(f"Cannot reach AnkiConnect at {ANKI_URL}: {exc.reason}\n"
                 "Is Anki running with the AnkiConnect add-on enabled?")
    if response.get("error"):
        sys.exit(f"AnkiConnect error on {action}: {response['error']}")
    return response["result"]


def plain(value):
    """Strip the HTML that Anki stores in fields down to readable text."""
    text = re.sub(r"<br\s*/?>|</(?:div|p|li)>", "\n", value, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\xa0", " ")
    return "\n".join(line.strip() for line in text.split("\n") if line.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--count", type=int, default=1, help="how many idioms to pull")
    args = parser.parse_args()

    query = f'deck:"{DECK}" -is:new -is:suspended'
    card_ids = anki("findCards", query=query)
    if not card_ids:
        sys.exit(f"No learned cards matched: {query}")
    picked = random.sample(card_ids, min(args.count, len(card_ids)))

    idioms = []
    for card in anki("cardsInfo", cards=picked):
        fields = {name: plain(field["value"]) for name, field in card["fields"].items()}
        idioms.append({
            "phrase": fields.get("Phrase/Idiom", ""),
            "definition": fields.get("Definition", ""),
        })
    print(json.dumps(idioms, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
