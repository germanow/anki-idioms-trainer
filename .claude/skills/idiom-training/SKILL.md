---
name: idiom-training
description: Drill the user's learned Anki idioms by presenting situations they must respond to with a fitting idiom. Use when the user wants to practice, train, or be quizzed on idioms, or invokes /idiom-training. Judges whether their idiom fits the situation rather than whether it matches the hidden target.
---

# Idiom training

Active-recall drill: the user is given a situation and must produce an idiom that fits it.
Idioms come from their own learned Anki cards, so the drill stays inside what they have
actually studied.

## Setting up a batch

Fetch ten at a time, so the drill itself runs with zero tool calls between an answer and the
next situation:

```bash
./random_idiom.py -n 10 --full --json
```

If AnkiConnect is unreachable, tell the user to open Anki and stop. Do not fall back to idioms
from memory — the point is to drill *their* deck.

The batch lands in the conversation, which means it is also in the user's scrollback. That is
fine as long as nothing in your own replies gives an upcoming idiom away — but it does mean the
drill relies on `promptSuggestionEnabled: false` (set in this project's
`.claude/settings.json`). If the user turns suggestions back on, warn them that the
suggestion box can hand them the answer, and offer to go back to keeping the batch on disk.

Work through the batch in order, then fetch the next one.

## Running a round

Present a situation — two or three sentences of concrete scenario that the target idiom would
naturally answer — and stop. Do not state the idiom, its definition, its literal words, or a
transparent near-synonym. The situation should make the *meaning* obvious while leaving the
*wording* to the user.

Never number the rounds as if out of a fixed total, and keep each situation self-contained.

## Judging an answer

The goal is overall idiomatic range, not hitting the exact card. So:

- If their idiom genuinely fits the situation, say so plainly — even when it is not the target.
- If it fits but is off in register, strength, or typical use, confirm it works and name the nuance in one line.
- If it does not fit, say why in one line: wrong meaning, wrong polarity, wrong context.
- If they misremember the form of a real idiom ("a hot potato" vs "hot potato", wrong preposition), accept the answer and correct the form.
- If they are stuck or pass, just reveal it without any scolding.

Then show the target idiom and one or two other idioms that would also have worked, each with a
short gloss. Alternatives may come from your own knowledge; they need not be in the deck.

## Keeping it quick

Every reply after an answer has the same shape, in this order:

1. One or two lines of verdict on their idiom.
2. The target and the alternatives, compact.
3. The next situation, immediately, in the same message.

No preamble, no "ready for the next one?", no separators beyond what readability needs. The user
should be able to answer, read, and answer again without a round trip in between. When the batch
runs out, fetch the next one in the same turn as the previous round's feedback.

Stop when the user says stop, and close with a short recap: what they got, what to review.
