---
name: score-idiom
description: Summarize an idiom drill — count right/wrong/passed answers and list the idioms the user could not recall, with glosses to review. Use at the end of a /practice-idiom session, when the user says stop, or when they ask for a score, results, recap, or summary of how the drill went.
---

# Idiom drill summary

Closes out a `practice-idiom` session: a score, and the list of idioms worth reviewing.

## Where the numbers come from

The drill runs with no tool calls between rounds, so nothing is written to disk — every round is
in this conversation, and that is the source. Walk back through the session and tally the rounds
you have actually judged.

Two things this means in practice:

- Count only rounds the user answered in this session. Never estimate, round, or infer a count
  from how long the session felt.
- If earlier rounds have been summarized out of context, say so in one line ("the first stretch of
  this session is no longer in context, so this covers the last N rounds") and summarize what is
  left. A partial summary that is labelled partial is fine; an invented total is not.

If the session has no drill in it at all, say that and offer to start one — do not produce an
empty scoreboard.

## Buckets

Each answered round goes in exactly one:

- **Right** — their idiom fit the situation. This includes an answer that was not the drawn
  target, one you confirmed but flagged for register or strength, and a real idiom whose form you
  corrected. The drill scores fit, not card-matching, so all of those are hits.
- **Wrong** — their idiom did not fit: wrong meaning, wrong polarity, wrong context.
- **Passed** — they passed, drew a blank, or asked to be told.

## The summary

Keep it to one compact message, in this order:

1. One line of score: total rounds, then right / wrong / passed.
2. **Could not recall** — every wrong and passed round, one line each: the target idiom, a short
   gloss, and for a wrong answer what they said instead. These are the review list.
3. **Shaky form** — only if there were any: idioms they reached for correctly but garbled, with
   the right form. One line each.
4. One closing line: what the pattern says, if there is one worth saying — a meaning they keep
   reaching past, a register they lean on. Skip it rather than manufacture a pattern from two
   rounds.

Example shape:

```
14 rounds — 9 right, 3 wrong, 2 passed.

Could not recall
  cut to the chase — get to the point, skipping the preamble (you said "spill the beans")
  a blessing in disguise — something bad that turns out well
  up in the arms — passed

Shaky form
  "a hot potato" — the idiom is just "hot potato"

The misses are all about timing and sequence — worth a pass through those cards.
```

No praise, no grading scale, no encouragement padding. The counts and the list are the whole
point.

End on that closing line. Do not offer to re-drill the misses, ask whether they want to keep
going, or close with a question of any kind — the summary is the last word. If the user wants
another round they will say so.
