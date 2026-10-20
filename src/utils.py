import json
import re


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")


def extract_json(raw: str):
    """Robustly pull a JSON object/array out of an LLM response that may be wrapped in
    markdown fences or preceded/followed by extra prose."""
    raw = raw.strip()
    raw = re.sub(r"^```(json)?", "", raw.strip())
    raw = re.sub(r"```$", "", raw.strip())
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to find the first {...} or [...] block
    for open_c, close_c in [("[", "]"), ("{", "}")]:
        start = raw.find(open_c)
        end = raw.rfind(close_c)
        if start != -1 and end != -1 and end > start:
            candidate = raw[start:end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue

    raise ValueError(f"Could not extract JSON from LLM output: {raw[:200]}")
