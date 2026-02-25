import base64
import json
import os
import pathlib
import sys
import urllib.request

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Missing OPENAI_API_KEY environment variable.")
    sys.exit(1)

OUT_DIR = pathlib.Path("assets/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-image-1"

PROMPTS = [
    {
        "file": "stress-ai.png",
        "prompt": "Photorealistic image of a real person under intense stress at work: young adult in an office/call-center setting, visibly overwhelmed, shouting into a pillow to release tension, cinematic but respectful, natural lighting, no text"
    },
    {
        "file": "ansiedade-ai.png",
        "prompt": "Photorealistic image of a real person with anxiety: young adult looking repeatedly at a wristwatch in a busy public place, tense body posture, worried expression, realistic skin detail, empathetic framing, no text"
    },
    {
        "file": "burnout-ai.png",
        "prompt": "Photorealistic image of a real person with burnout: exhausted professional at desk late at night, head down near laptop, tired posture, empty coffee cups, realistic office environment, empathetic tone, no text"
    },
    {
        "file": "depressao-ai.png",
        "prompt": "Photorealistic image of a real person with depressive symptoms: adult seated near a window in soft natural light, low energy and distant gaze, intimate and respectful composition, no text"
    },
    {
        "file": "panico-ai.png",
        "prompt": "Photorealistic image of a young woman experiencing panic, holding her chest on the heart side, visible shortness of breath and fear, background slightly blurred, respectful and non-sensational, no text"
    },
    {
        "file": "toc-ai.png",
        "prompt": "Photorealistic image of a real person with OCD traits, meticulously organizing a desk with precise alignment of objects, repeated checking behavior implied, clear indoor lighting, respectful framing, no text"
    },
    {
        "file": "esquizofrenia-ai.png",
        "prompt": "Photorealistic image of a real person with schizophrenia-related distress, covering ears in desperation as if trying to block voices, emotional but respectful framing, realistic interior scene, no text"
    }
]


def generate_image(prompt: str) -> bytes:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "size": "1024x1024"
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))

    b64 = data["data"][0].get("b64_json")
    if not b64:
        raise RuntimeError("No b64_json returned by API")
    return base64.b64decode(b64)


def main() -> None:
    for item in PROMPTS:
        filename = item["file"]
        prompt = item["prompt"]
        print(f"Generating {filename}...")
        try:
            image_bytes = generate_image(prompt)
            output_path = OUT_DIR / filename
            output_path.write_bytes(image_bytes)
            print(f"Saved {output_path}")
        except Exception as exc:
            print(f"Failed {filename}: {exc}")


if __name__ == "__main__":
    main()
