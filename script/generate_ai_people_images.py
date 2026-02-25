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

MODEL_CANDIDATES = [
    "mai-image-1",
    "gpt-image-1"
]

PROMPTS = [
    {
        "file": "stress-real.jpg",
        "prompt": "Ultra realistic photo of a real person under intense work stress, office setting, tense posture, natural light, documentary photography look, no text, no illustration"
    },
    {
        "file": "ansiedade-real.jpg",
        "prompt": "Ultra realistic portrait photo of a real person with anxiety, worried expression, shallow breathing body language, city background softly blurred, no text, no drawing"
    },
    {
        "file": "burnout-real.jpg",
        "prompt": "Ultra realistic photo of a real professional with burnout, late night desk, exhausted expression, laptop light, cinematic but natural, no text, no illustration"
    },
    {
        "file": "depressao-real.jpg",
        "prompt": "Ultra realistic photo of a real person with depressive mood, seated by window, low energy posture, soft natural light, respectful framing, no text, no drawing"
    },
    {
        "file": "panico-real.jpg",
        "prompt": "Ultra realistic photo of a real person during panic moment, hand on chest, short breath expression, indoor setting, respectful non-sensational look, no text"
    },
    {
        "file": "toc-real.jpg",
        "prompt": "Ultra realistic photo of a real person with OCD traits, carefully aligning objects on a table, repeated checking behavior implied, clean indoor light, no text"
    },
    {
        "file": "esquizofrenia-real.jpg",
        "prompt": "Ultra realistic photo of a real person in schizophrenia-related distress, covering ears as if overwhelmed by voices, empathetic and respectful framing, no text"
    }
]


def generate_image(prompt: str) -> bytes:
    last_error = None
    for model in MODEL_CANDIDATES:
        payload = {
            "model": model,
            "prompt": prompt,
            "size": "1024x1024",
            "output_format": "jpeg"
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

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
            b64 = data["data"][0].get("b64_json")
            if not b64:
                raise RuntimeError("No b64_json returned by API")
            print(f"Generated using model: {model}")
            return base64.b64decode(b64)
        except Exception as exc:
            last_error = exc
            print(f"Model failed: {model} -> {exc}")

    raise RuntimeError(f"All models failed. Last error: {last_error}")


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
