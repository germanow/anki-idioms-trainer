# Idiom images: findings and plan

Goal: add a cartoon image to each card in the "Idioms and Phrases" deck (~4,800 notes).

## Setup

- Laptop `192.168.0.31` (RTX 4080 Laptop, 12 GB VRAM, 32 GB RAM).
- Ollama `:11434`, models: gemma4:12b/26b/31b, qwen3:14b, qwen3.5:9b. Default context is 4K on 12 GB;
  set `OLLAMA_CONTEXT_LENGTH=16384` for Open WebUI (its built-in tool definitions alone exceed 4K).
- ComfyUI `:8188`, FLUX.2 Klein 4B fp8, 4 steps, CFG 1, euler, 1024x1024, ~3 s/image.
- Note fields: `Phrase/Idiom`, `Definition`, `Example`.

## Findings

1. Idiom or definition in the image prompt → garbled text and speech bubbles in ~90% of images.
   An LLM must first write a concrete scene (who, doing what, where) with no text or idiom words.
2. Scene writers, same 10 idioms, thinking off, with example sentence:

   | Model | Time per idiom | Fit |
   |---|---|---|
   | gemma4:12b | ~2 s | ~8/10 |
   | **gemma4:26b** | ~2–5 s | **~9/10** |
   | gemma4:31b | ~12 s | ~9/10 |
   | qwen3:14b | ~2 s | ~7/10 |
   | qwen3.5:9b | ~2 s | ~5/10, surreal, stray non-English words |

3. Thinking on: 5–35x slower, no better, some empty answers. Keep `think: false`.
4. Example sentence: helps abstract idioms but pulls in letters/notices. The prompt forbids
   papers, letters, documents and screens.
5. 50-idiom run (gemma4:26b + Klein 4B): ~1.7 min prompts + ~3 min images. Nearly no text in images;
   ~30–35 of 50 clearly show the meaning. Weak ones are abstract idioms (bend the truth, go nuts,
   hold good, speaking with one voice). See `gallery.html`.

## Scene prompt (system)

> You write prompts for an image model. Given an English idiom and its meaning, describe ONE concrete,
> single-panel cartoon scene that shows the MEANING (not a literal picture of the words unless that
> literal picture clearly conveys the meaning). Say who is there, what they are doing, their facial
> expressions, and the setting. Do not include any text, letters, signs, labels, speech bubbles,
> papers, letters, documents, screens, or the idiom's words. End with: 'Colorful flat cartoon
> illustration, no text.' You may get an example sentence; use it as inspiration for the situation,
> not a script. Reply with the prompt only, 40-70 words.

User message: `Idiom: …\nMeaning: …\nExample: …`

## Plan

The 50-idiom check is done; no manual review. Three steps, each interruptible and resumable:
it skips work already saved, so rerunning continues where it stopped.

Order: not-yet-learned (new) cards first, then learned. Suspended cards are skipped.

0. **Export**: `./export_idioms.py` writes `idioms.json` (note_id, phrase, definition, example,
   learned) in that order, so steps 1–2 run without Anki. 3,706 idioms: 1,313 new, 2,393 learned.
1. **Prompts** (gemma4:26b): write each idiom's scene to the prompts file in this repo, saving
   after every idiom. Unload the model at the end (`keep_alive: 0`).
2. **Images** (ComfyUI, Klein 4B): go idiom by idiom through the saved prompts and save each
   image in this repo, skipping ones that already exist. Free ComfyUI at the end (`POST /free`).
3. **Attach**: upload each image to Anki with AnkiConnect `storeMediaFile` and set an `Image`
   field (`<img src="…">`) on the note, skipping notes that already have one. Add the field to
   the note type and card template first, and back up the collection.

Each saved record is keyed by note ID, so the steps line up even if the deck changes.
