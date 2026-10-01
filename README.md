# anki-idioms-trainer

A Claude Code skill that drills your Anki idioms in reverse: it describes a situation, you reply
with an idiom that fits. It only uses idioms from cards you have already learned.

## Usage

1. Open Anki with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed,
   and leave it running. Python 3 is the only other requirement.
2. Run `claude` in this directory and type `/practice-idiom`.
3. Reply to each situation with an idiom, or "pass".
4. Say "stop" for a summary: right, wrong and passed counts, plus the idioms you could not
   recall. `/score-idiom` gives the same summary mid-session.

```
Your colleague dumps a politically messy budget decision on your desk
an hour before he goes on leave. What do you call what he just handed you?

> a hot potato

Fits. For what he did, you'd say he passed the buck.

hot potato — an issue nobody wants responsibility for.
"The parking policy has been a hot potato since the new building opened."
Also works: pass the buck · leave someone holding the baby

Your friend has been talking up a business plan for months but has still
not registered the company or spoken to a single customer...
```

Any idiom that fits the situation counts, not just the one that was drawn.

`/practice-idiom young` limits the drill to young cards: still in learning, or with an interval
under 21 days.

Idioms are fetched ten at a time and the batch shows up in the tool output, so don't expand it
or you will see the answers.

## random_idiom.py

The skill's source of idioms, also usable on its own:

```bash
./random_idiom.py           # one random learned idiom
./random_idiom.py -n 10     # ten of them
./random_idiom.py --young   # only young cards
```

It prints a JSON list of `{phrase, definition}`. "Learned" means the card has left the new queue
and is not suspended. It expects notes with `Phrase/Idiom` and `Definition` fields in the
`Idioms and Phrases` deck, set as `DECK` at the top of the script.

## Limitations

- A long session can repeat an idiom; nothing tracks what you have been asked.
- The summary covers the current session only; there is no history across sessions.
