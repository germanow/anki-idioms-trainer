#!/usr/bin/env python3
"""Pull random learned idioms from the Anki "Idioms and Phrases" deck via AnkiConnect.

"Learned" means the card has left the new queue and is not suspended.
"Young" narrows that to cards still in learning or with an interval under 21 days,
Anki's own cutoff between young and mature.
"Today" narrows it to cards first studied today or answered Again today.
Anki must be running with the AnkiConnect add-on installed.

Prints a JSON list of {phrase, definition}.

Examples:
    ./random_idiom.py           # one random learned idiom
    ./random_idiom.py -n 10     # ten of them
    ./random_idiom.py --young   # only young cards
    ./random_idiom.py --today   # only cards learned or failed today
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


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--count", type=int, default=1, help="how many idioms to pull")
    parser.add_argument("--young", action="store_true",
                        help="only young cards (learning, or interval under 21 days)")
    parser.add_argument("--today", action="store_true",
                        help="only cards first studied today or answered Again today")
    return parser.parse_args()


def build_query(young, today):
    query = f'deck:"{DECK}" -is:new -is:suspended'
    if young:
        query += " prop:ivl<21"
    if today:
        query += " (introduced:1 OR rated:1:1)"
    return query


def random_idioms(query, count):
    card_ids = anki("findCards", query=query)
    if not card_ids:
        sys.exit(f"No cards matched: {query}")
    picked = random.sample(card_ids, min(count, len(card_ids)))

    idioms = []
    for card in anki("cardsInfo", cards=picked):
        fields = {name: plain(field["value"]) for name, field in card["fields"].items()}
        idioms.append({
            "phrase": fields.get("Phrase/Idiom", ""),
            "definition": fields.get("Definition", ""),
        })
    return idioms


def main():
    args = parse_args()
    idioms = random_idioms(build_query(args.young, args.today), args.count)
    print(json.dumps(idioms, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
