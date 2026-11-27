#!/usr/bin/env python3
"""Step 2: render images/<note_id>.png for each prompt in prompts.json, using ComfyUI (FLUX.2 Klein 4B).

Goes in idioms.json order and skips images that already exist; rerun to resume.
Env: COMFY_URL (default http://192.168.0.31:8188).
"""

import argparse
import json
import os
import time
import urllib.parse
import urllib.request

COMFY_URL = os.environ.get("COMFY_URL", "http://192.168.0.31:8188")


def comfy(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"{COMFY_URL}{path}", data, {"Content-Type": "application/json"})
    return urllib.request.urlopen(request, timeout=300).read()


def workflow(prompt, seed):
    return {
        "1": {"class_type": "UNETLoader",
              "inputs": {"unet_name": "flux-2-klein-4b-fp8.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "flux2"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "full_encoder_small_decoder.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": ""}},
        "6": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "7": {"class_type": "Flux2Scheduler", "inputs": {"steps": 4, "width": 1024, "height": 1024}},
        "8": {"class_type": "CFGGuider",
              "inputs": {"model": ["1", 0], "positive": ["4", 0], "negative": ["5", 0], "cfg": 1.0}},
        "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "11": {"class_type": "SamplerCustomAdvanced",
               "inputs": {"noise": ["10", 0], "guider": ["8", 0], "sampler": ["9", 0],
                          "sigmas": ["7", 0], "latent_image": ["6", 0]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": "idiom"}},
    }


def render(prompt, seed):
    prompt_id = json.loads(comfy("/prompt", {"prompt": workflow(prompt, seed)}))["prompt_id"]
    while not (history := json.loads(comfy(f"/history/{prompt_id}"))).get(prompt_id):
        time.sleep(1)
    entry = history[prompt_id]
    if entry.get("status", {}).get("status_str") == "error":
        raise RuntimeError(f"ComfyUI failed: {entry['status']}")
    image = next(iter(entry["outputs"].values()))["images"][0]
    return comfy("/view?" + urllib.parse.urlencode(image))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, help="stop after this many new images")
    limit = parser.parse_args().count
    done = 0
    prompts = json.load(open("prompts.json"))
    note_ids = [str(i["note_id"]) for i in json.load(open("idioms.json")) if prompts.get(str(i["note_id"]))]
    os.makedirs("images", exist_ok=True)
    try:
        for n, note_id in enumerate(note_ids, 1):
            path = f"images/{note_id}.png"
            if os.path.exists(path):
                continue
            png = render(prompts[note_id], int(note_id) % 2**32)
            with open(path + ".tmp", "wb") as f:
                f.write(png)
            os.replace(path + ".tmp", path)
            print(f"{n}/{len(note_ids)} {path}", flush=True)
            done += 1
            if done == limit:
                break
    finally:
        comfy("/free", {"unload_models": True, "free_memory": True})


if __name__ == "__main__":
    main()
