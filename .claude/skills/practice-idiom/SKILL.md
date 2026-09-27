---
name: practice-idiom
description: Drill the user's learned Anki idioms by presenting situations they must respond to with a fitting idiom. Use when the user wants to practice, train, or be quizzed on idioms, or invokes /practice-idiom. Judges whether their idiom fits the situation rather than whether it matches the hidden target.
---

# Idiom training

Active-recall drill: the user is given a situation and must produce an idiom that fits it.
Idioms come from their own learned Anki cards, so the drill stays inside what they have
actually studied.

## Setting up a batch

Fetch ten at a time, so the drill itself runs with zero tool calls between an answer and the
next situation:

```bash
./random_idiom.py -n 10
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

Then show the target idiom with a short gloss and one example sentence using it — a natural
utterance someone would actually say in a situation like this, not a dictionary line. Follow it
with one or two other idioms that would also have worked, each with a short gloss (no example
sentence needed for those). Alternatives may come from your own knowledge; they need not be in
the deck.

The example sentence should put the idiom in a concrete situation of its own rather than restate
the one just drilled, so the user sees the idiom's typical use, not only this one fit.

## Formatting

The terminal renders your replies as markdown, and that is the only colour you get — raw ANSI
escapes are printed literally, so never emit them. The point of the markup is that the user's eye
lands on the idioms without reading the prose around them:

- **Every idiom goes in backticks**, wherever it appears — the target, the alternatives, a form
  you are correcting, the user's own answer when you quote it back. Backticked text renders in
  its own colour, so the idioms become the scannable layer of the reply.
- *Italicise the example sentence*, and only the example sentence. It is the one line that is
  someone speaking rather than you explaining.
- Open the verdict with a **bolded** word or short phrase — **Fits.**, **Doesn't fit.**,
  **Close.** — then the rest of the verdict in plain prose.
- Glosses stay plain, after an em dash. Alternatives go on one line, separated by ` · `.
- The situation itself is plain prose with no markup at all. Nothing in it should be coloured,
  partly for contrast with the feedback above it and partly because marking a phrase inside the
  situation hints at the wording you are asking the user to produce.

So a round is written as:

````
**Fits.** Slightly stronger than the situation calls for, but it works.

`hot potato` — an issue nobody wants responsibility for.
*"The parking policy has been a hot potato since the new building opened."*
Also works: `pass the buck` · `leave someone holding the baby`

Your friend has been talking up a business plan for months but still has not registered the
company or spoken to a single customer.
````

## Keeping it quick

Every reply after an answer has the same shape, in this order, marked up as described above:

1. One or two lines of verdict on their idiom.
2. The target with its gloss and example sentence, then the alternatives, compact.
3. The next situation, immediately, in the same message.

No preamble, no "ready for the next one?", no separators beyond what readability needs. The user
should be able to answer, read, and answer again without a round trip in between. When the batch
runs out, fetch the next one in the same turn as the previous round's feedback.

Stop when the user says stop, and close with the `score-idiom` skill, which counts the rounds
and lists what to review. Keeping the tally is its job, not yours — do not interrupt
the drill to score anything.
