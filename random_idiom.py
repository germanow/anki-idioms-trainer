#!/usr/bin/env python3
"""Pull a random learned idiom from the Anki "Idioms and Phrases" deck via AnkiConnect.

"Learned" means the card has left the new queue and is not suspended.
Anki must be running with the AnkiConnect add-on installed.

By default only the idiom itself is printed; pass --full for the definition,
example and scheduling stats.

Examples:
    ./random_idiom.py                  # one random learned idiom
    ./random_idiom.py -n 5             # five of them
    ./random_idiom.py --full           # with definition, example and stats
    ./random_idiom.py --mature         # only cards with interval >= 21 days
    ./random_idiom.py --deck '...Tier 1' --json
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
DEFAULT_DECK = "Idioms and Phrases"


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


def fetch(deck, count, mature, min_interval, seed):
    query = f'deck:"{deck}" -is:new -is:suspended'
    if mature:
        min_interval = max(min_interval, 21)
    if min_interval:
        query += f" prop:ivl>={min_interval}"

    card_ids = anki("findCards", query=query)
    if not card_ids:
        sys.exit(f"No learned cards matched: {query}")

    rng = random.Random(seed)
    picked = rng.sample(card_ids, min(count, len(card_ids)))
    return anki("cardsInfo", cards=picked)


def as_idiom(card):
    fields = {name: plain(field["value"]) for name, field in card["fields"].items()}
    return {
        "phrase": fields.get("Phrase/Idiom", ""),
        "definition": fields.get("Definition", ""),
        "example": fields.get("Example", ""),
        "interval_days": card["interval"],
        "reps": card["reps"],
        "lapses": card["lapses"],
        "deck": card["deckName"],
        "card_id": card["cardId"],
    }


def show(idiom, full):
    if not full:
        print(idiom["phrase"])
        return
    print(f"\n\033[1m{idiom['phrase']}\033[0m")
    if idiom["definition"]:
        print(f"  {idiom['definition']}")
    if idiom["example"]:
        print(f"  e.g. {idiom['example']}")
    print(f"  \033[2m[{idiom['deck']} · interval {idiom['interval_days']}d · "
          f"{idiom['reps']} reps · {idiom['lapses']} lapses]\033[0m")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--count", type=int, default=1, help="how many idioms to pull")
    parser.add_argument("-d", "--deck", default=DEFAULT_DECK, help="deck to search (subdecks included)")
    parser.add_argument("--mature", action="store_true", help="only cards with interval >= 21 days")
    parser.add_argument("--min-interval", type=int, default=0, metavar="DAYS",
                        help="only cards with at least this interval")
    parser.add_argument("-f", "--full", action="store_true",
                        help="include definition, example and scheduling stats")
    parser.add_argument("--seed", type=int, help="seed the picker for reproducible output")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of formatted text")
    args = parser.parse_args()

    cards = fetch(args.deck, args.count, args.mature, args.min_interval, args.seed)
    idioms = [as_idiom(card) for card in cards]

    if args.json:
        payload = idioms if args.full else [idiom["phrase"] for idiom in idioms]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for idiom in idioms:
            show(idiom, args.full)
        if args.full:
            print()


if __name__ == "__main__":
    main()
