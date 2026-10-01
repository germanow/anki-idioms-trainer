# anki-idioms-trainer

A Claude Code skill that drills your Anki idioms in reverse: it describes a situation, you reply
with an idiom that fits. It only uses idioms from cards you have already learned.

## Usage

1. Open Anki with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed,
   and leave it running. Python 3 is the only other requirement.
2. Run `claude` in this directory and type `/practice-idiom`.
3. Reply to each situation with an idiom, "hint" for one clue, or "pass".
4. Say "stop" for a summary: right, hinted, wrong and passed counts, plus the idioms you could
   not recall. `/score-idiom` gives the same summary mid-session.

```
Take the pay cut or lose the job: your boss wants an answer by Friday.

> between a rock and a hard place

Fits.

between a rock and a hard place — forced to choose between two bad options.
"With the rent going up and no cheaper flat around, we're between a rock and a hard place."
Also works: caught between the devil and the deep blue sea · on the horns of a dilemma

Your friend has talked up a business plan for months but never started...
```

Any idiom that fits the situation counts.

`/practice-idiom young` limits the drill to young cards.

The skill gets its idioms from `random_idiom.py`; the deck and field names it expects are set at
the top of that script.

## Limitations

- A long session can repeat an idiom; nothing tracks what you have been asked.
- The summary covers the current session only; there is no history across sessions.
