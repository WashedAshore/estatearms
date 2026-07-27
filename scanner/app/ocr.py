"""
Serial-number and proof-mark OCR via Google Cloud Vision.

Cloud Vision is called via REST with an API key set in GOOGLE_CLOUD_VISION_API_KEY.
If the key is not set we skip OCR and return an empty result — the vision model's
own reading of markings still populates the identification.
"""

from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import httpx


# Rough regex heuristics for serial-like tokens and proof-mark-like tokens.
SERIAL_RE = re.compile(r"\b[A-Z]{0,3}[- ]?\d{2,8}[A-Z]{0,3}\b")
PROOF_RE = re.compile(r"\b(?:BATF|BATFE|CAI|SAMCO|CENTURY ARMS|U\.?S\.?|USGI|SA|WRA|RIA|SPRINGFIELD|COLT|WINCHESTER|REMINGTON|MAUSER|WALTHER|H&K|HK|KWK|WaA\d+|EIG|CN|MI|SI|EF)\b", re.I)


@dataclass
class OCRResult:
    full_text: str
    candidate_serials: List[str]
    candidate_proof_marks: List[str]
    provider: str


def _b64(path: Path) -> str:
    return base64.standard_b64encode(path.read_bytes()).decode("ascii")


def ocr_google(image_path: Path) -> OCRResult:
    key = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY")
    if not key:
        return OCRResult(full_text="", candidate_serials=[], candidate_proof_marks=[], provider="none")

    resp = httpx.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={key}",
        json={
            "requests": [
                {
                    "image": {"content": _b64(image_path)},
                    "features": [{"type": "TEXT_DETECTION"}],
                }
            ]
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    data = resp.json()
    anns = data.get("responses", [{}])[0].get("textAnnotations", [])
    full_text = anns[0].get("description", "") if anns else ""

    serials = list({m.group(0) for m in SERIAL_RE.finditer(full_text)})
    proofs = list({m.group(0) for m in PROOF_RE.finditer(full_text)})

    return OCRResult(
        full_text=full_text,
        candidate_serials=serials,
        candidate_proof_marks=proofs,
        provider="google_cloud_vision",
    )
