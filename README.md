# anki-idioms-trainer

Your Anki cards show you an idiom and ask what it means. This goes the other way: it describes a
situation and asks you for the idiom. Recognising *hot potato* on a card is easy; reaching for it
while you talk is the part that needs practice.

`/practice-idiom` is a Claude Code skill that runs that drill, using only idioms from cards you
have already learned.

## Getting started

1. Open Anki with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed,
   and leave it running. Python 3 is all the script needs.
2. Run `claude` in this directory and type `/practice-idiom`.
3. Read the situation you are given. Reply with an idiom that fits — just the idiom, no
   explanation needed. Say "pass" if nothing comes to mind.
4. You get back, in one message: a verdict on your answer, the idiom that was drawn, one or two
   others that would also have worked, and the next situation. Answer again straight away.
5. Say "stop" when you are done, and you get a summary: how many you got right, wrong and
   passed, plus the idioms you could not recall. `/score-idiom` gives you the same thing
   mid-session if you want a score before you finish.

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

In the terminal the idioms themselves are colour-highlighted and the example sentence is
italicised, so you can scan a reply for the phrases without reading the prose around them. The
situation is left unmarked on purpose — highlighting a phrase inside it would hint at the wording
you are meant to come up with.

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
./random_idiom.py           # one random learned idiom
./random_idiom.py -n 10     # ten of them
```

It prints a JSON list of `{phrase, definition, example}`. "Learned" means the card has left the
new queue and is not suspended, regardless of due date. It expects notes with `Phrase/Idiom`,
`Definition` and `Example` fields in the `Idioms and Phrases` deck, set as `DECK` at the top of
the script.

## Rough edges

A long session can repeat an idiom — nothing tracks what you have been asked.

The summary is counted from the conversation, not from a saved log, so it covers the current
session only — there is no history across sessions, and a very long session whose early rounds
have scrolled out of Claude's context gets a summary that says so and covers the rest.
