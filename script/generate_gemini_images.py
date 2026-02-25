import base64
import json
import os
import pathlib
import sys
import urllib.request
import urllib.error

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Missing GEMINI_API_KEY environment variable.")
    sys.exit(1)

OUT_DIR = pathlib.Path("assets/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {
        "file": "stress-real.jpg",
        "prompt": "Photorealistic image of a real adult under severe stress at work, tense face, cluttered desk, natural light, documentary style, respectful tone, no text"
    },
    {
        "file": "ansiedade-real.jpg",
        "prompt": "Photorealistic close portrait of a person with anxiety, worried expression, shallow breathing posture, urban background softly blurred, realistic skin texture, no text"
    },
    {
        "file": "burnout-real.jpg",
        "prompt": "Photorealistic person experiencing burnout, exhausted at office desk late night, head supported by hand, laptop light, candid style, no text"
    },
    {
        "file": "depressao-real.jpg",
        "prompt": "Photorealistic image of a person with depressive mood, seated by window, low energy body language, soft natural light, empathetic framing, no text"
    },
    {
        "file": "panico-real.jpg",
        "prompt": "Photorealistic young adult in panic, holding chest and trying to breathe, realistic indoor scene, respectful non-sensational composition, no text"
    },
    {
        "file": "toc-real.jpg",
        "prompt": "Photorealistic person with OCD traits meticulously aligning objects on table, repeated checking behavior implied, clear daylight, no text"
    },
    {
        "file": "esquizofrenia-real.jpg",
        "prompt": "Photorealistic portrait of a person in schizophrenia-related distress, covering ears as if overwhelmed by voices, empathetic framing, muted colors, no text"
    }
]

MODEL_CANDIDATES = [
    os.getenv("GEMINI_MODEL", "gemini-3.0-image-generation"),
    "gemini-2.0-flash-preview-image-generation",
    "gemini-2.0-flash-exp-image-generation",
]


def call_gemini(model: str, prompt: str) -> bytes:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as res:
        data = json.loads(res.read().decode("utf-8"))

    candidates = data.get("candidates", [])
    for cand in candidates:
        content = cand.get("content", {})
        for part in content.get("parts", []):
            inline = part.get("inlineData")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])

    raise RuntimeError("No image bytes found in Gemini response")


def generate_one(item):
    last_err = None
    for model in MODEL_CANDIDATES:
        try:
            print(f"Trying {model} for {item['file']}...")
            img = call_gemini(model, item["prompt"])
            (OUT_DIR / item["file"]).write_bytes(img)
            print(f"Saved {OUT_DIR / item['file']} (model={model})")
            return
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:400]}"
        except Exception as e:
            last_err = str(e)

    raise RuntimeError(f"Failed for {item['file']}: {last_err}")


def main():
    for item in PROMPTS:
        try:
            generate_one(item)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
