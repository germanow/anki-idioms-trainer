#!/usr/bin/env python3
"""Step 1: write a cartoon scene prompt for each idiom in idioms.json, using Ollama.

Saves prompts.json ({note_id: scene}) after every idiom; rerun to resume after an interruption.
Env: OLLAMA_URL (default http://192.168.0.31:11434), OLLAMA_MODEL (default gemma4:26b).
"""

import argparse
import json
import os
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://192.168.0.31:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:26b")
SYSTEM = (
    "You write prompts for an image model. Given an English idiom and its meaning, describe ONE "
    "concrete, single-panel cartoon scene that shows the MEANING (not a literal picture of the words "
    "unless that literal picture clearly conveys the meaning). Say who is there, what they are doing, "
    "their facial expressions, and the setting. Do not include any text, letters, signs, labels, "
    "speech bubbles, papers, letters, documents, screens, or the idiom's words. "
    "End with: 'Colorful flat cartoon illustration, no text.' You may get an example sentence; use it "
    "as inspiration for the situation, not a script. Reply with the prompt only, 40-70 words."
)


def ollama(path, body):
    request = urllib.request.Request(f"{OLLAMA_URL}{path}", json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(request, timeout=900))


def scene(idiom):
    user = f"Idiom: {idiom['phrase']}\nMeaning: {idiom['definition']}\nExample: {idiom['example']}"
    reply = ollama("/api/chat", {"model": MODEL, "stream": False, "think": False,
                                 "messages": [{"role": "system", "content": SYSTEM},
                                              {"role": "user", "content": user}]})
    return reply["message"]["content"].strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, help="stop after this many new prompts")
    limit = parser.parse_args().count
    done = 0
    idioms = json.load(open("idioms.json"))
    prompts = json.load(open("prompts.json")) if os.path.exists("prompts.json") else {}
    try:
        for n, idiom in enumerate(idioms, 1):
            key = str(idiom["note_id"])
            if prompts.get(key):
                continue
            prompts[key] = scene(idiom)
            with open("prompts.json.tmp", "w") as f:
                json.dump(prompts, f, ensure_ascii=False, indent=2)
            os.replace("prompts.json.tmp", "prompts.json")
            print(f"{n}/{len(idioms)} {idiom['phrase']}", flush=True)
            done += 1
            if done == limit:
                break
    finally:
        ollama("/api/generate", {"model": MODEL, "keep_alive": 0})


if __name__ == "__main__":
    main()
