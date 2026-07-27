"""
Vision provider abstraction for the EstateArms scanner.

Two backends are supported:
  1. Anthropic Claude (claude-sonnet family) - primary firearm ID + variant reasoning
  2. OpenAI GPT-4o / GPT-5 - fallback and consensus check

Provider is chosen by the VISION_PROVIDER env var. Keys pulled from env:
  ANTHROPIC_API_KEY  - required for provider=anthropic
  OPENAI_API_KEY     - required for provider=openai

If neither key is set, the scanner returns a structured stub so the rest of the
pipeline (OCR, valuation prompt, inventory row) can still be exercised.
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


@dataclass
class IdentifyResult:
    raw: str
    parsed: dict
    provider: str
    model: str


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _b64_image(path: Path) -> tuple[str, str]:
    """Return (base64_data, mime_type) for the given image path."""
    ext = path.suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime = mime_map.get(ext, "image/jpeg")
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return data, mime


def _extract_json(text: str) -> dict:
    """Extract the first JSON object from a model response, tolerant of fences."""
    t = text.strip()
    if t.startswith("```"):
        # strip fenced block
        t = t.split("```", 2)[1]
        if t.startswith("json"):
            t = t[4:]
        t = t.strip().rstrip("`").strip()
    # find first { and matching }
    start = t.find("{")
    if start == -1:
        raise ValueError("No JSON object found in model response")
    depth = 0
    for i in range(start, len(t)):
        if t[i] == "{":
            depth += 1
        elif t[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(t[start : i + 1])
    raise ValueError("Unterminated JSON object in model response")


def identify_anthropic(image_path: Path, user_notes: str = "") -> IdentifyResult:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    sys_prompt = _load_prompt("identify.md")
    b64, mime = _b64_image(image_path)

    user_content = [
        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
        {"type": "text", "text": f"User notes: {user_notes or '(none)'}\n\nReturn the JSON identification now."},
    ]

    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 2000,
            "system": sys_prompt,
            "messages": [{"role": "user", "content": user_content}],
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()
    text = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
    parsed = _extract_json(text)
    return IdentifyResult(raw=text, parsed=parsed, provider="anthropic", model=model)


def identify_openai(image_path: Path, user_notes: str = "") -> IdentifyResult:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-2024-11-20")
    sys_prompt = _load_prompt("identify.md")
    b64, mime = _b64_image(image_path)

    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "content-type": "application/json"},
        json={
            "model": model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": sys_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"User notes: {user_notes or '(none)'}\n\nReturn the JSON identification now."},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    ],
                },
            ],
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    parsed = _extract_json(text)
    return IdentifyResult(raw=text, parsed=parsed, provider="openai", model=model)


def identify_stub(image_path: Path, user_notes: str = "") -> IdentifyResult:
    """No-key fallback so the rest of the pipeline can be exercised."""
    stub = {
        "type": "other",
        "make": None,
        "model": None,
        "variant": None,
        "caliber": None,
        "barrel_length_in": None,
        "action": None,
        "era": None,
        "finish": None,
        "grips_stock": None,
        "visible_markings": [],
        "serial_number_visible": None,
        "condition": {"nra_grade": None, "finish_pct_estimate": None, "notes": "stub — no vision key configured"},
        "rarity": {"level": "Common", "factors": [], "production_notes": "stub"},
        "nfa": {"applies": False, "class": None, "pre_86_mg_possible": False, "required_transfer_form": None, "estate_notes": "stub"},
        "candidates": [],
        "id_confidence": "low",
        "what_would_raise_confidence": ["Set ANTHROPIC_API_KEY or OPENAI_API_KEY to enable real vision ID"],
        "reasoning_brief": f"Stub response for {image_path.name}. Notes: {user_notes or '(none)'}",
    }
    return IdentifyResult(raw=json.dumps(stub), parsed=stub, provider="stub", model="none")


def identify(image_path: Path, user_notes: str = "") -> IdentifyResult:
    provider = os.environ.get("VISION_PROVIDER", "auto").lower()
    if provider == "anthropic":
        return identify_anthropic(image_path, user_notes)
    if provider == "openai":
        return identify_openai(image_path, user_notes)
    # auto: prefer anthropic, fall back to openai, then stub
    if os.environ.get("ANTHROPIC_API_KEY"):
        return identify_anthropic(image_path, user_notes)
    if os.environ.get("OPENAI_API_KEY"):
        return identify_openai(image_path, user_notes)
    return identify_stub(image_path, user_notes)
