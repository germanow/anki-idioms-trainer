# anki-idioms-trainer

Your Anki cards show you an idiom and ask what it means. This goes the other way: it describes a
situation and asks you for the idiom. Recognising *hot potato* on a card is easy; reaching for it
while you talk is the part that needs practice.

`/idiom-training` is a Claude Code skill that runs that drill, using only idioms from cards you
have already learned.

## Getting started

1. Open Anki with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed,
   and leave it running. Python 3 is all the script needs.
2. Run `claude` in this directory and type `/idiom-training`.
3. Read the situation you are given. Reply with an idiom that fits — just the idiom, no
   explanation needed. Say "pass" if nothing comes to mind.
4. You get back, in one message: a verdict on your answer, the idiom that was drawn, one or two
   others that would also have worked, and the next situation. Answer again straight away.
5. Say "stop" when you are done. You get a short recap of what to review.

```
Your colleague dumps a politically messy budget decision on your desk
an hour before he goes on leave. What do you call what he just handed you?

> a hot potato

Fits. Slight form note: usually "a hot potato" is what it is, and you'd
say he "passed the buck" for what he did.
Drawn: hot potato — an issue nobody wants responsibility for.
Also works: pass the buck · leave someone holding the baby

Next: your friend has been talking up a business plan for months but
has still not registered the company or spoken to a single customer...
```

Your answer does not have to match the idiom that was drawn. If it fits the situation it
counts — the goal is range, not guessing a specific card. Wrong-fit answers get a one-line
reason; a garbled form of a real idiom is accepted and corrected.

Idioms are fetched ten at a time, so there is no pause between your answer and the next
situation. The batch does pass through the terminal on the way in — don't go expanding that tool
output and you will not spoil yourself. Prompt suggestions are switched off for this project in
`.claude/settings.json`, because the suggestion box will otherwise offer you the answer
before you have typed anything.

## random_idiom.py

The skill's source of idioms, also usable on its own:

```bash
./random_idiom.py                        # one random learned idiom
./random_idiom.py -n 5 --full            # five, with definition and stats
./random_idiom.py --mature               # only cards with interval >= 21 days
./random_idiom.py --deck 'Idioms and Phrases::Tier 1' --json
```

"Learned" means the card has left the new queue and is not suspended, regardless of due date.
It expects notes with `Phrase/Idiom`, `Definition` and `Example` fields in the
`Idioms and Phrases` deck; `--deck` overrides that. `--help` lists the rest.

## Rough edges

A long session can repeat an idiom — nothing tracks what you have been asked. Nothing is saved
between sessions, so there is no score or history.
