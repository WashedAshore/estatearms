"""
Court-ready inventory row generator.

Takes the identification + valuation output and produces a single JSON payload
matching the DR-140 Florida probate inventory schema (adapted) plus a flat CSV row
ready to append to the master estate inventory spreadsheet.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class InventoryRow:
    scan_id: str
    scanned_at_iso: str
    category: str  # Firearm / NFA Firearm / Component / Ammunition
    make: Optional[str]
    model: Optional[str]
    variant: Optional[str]
    caliber: Optional[str]
    barrel_length_in: Optional[float]
    serial_number: Optional[str]
    condition_grade: Optional[str]
    condition_notes: str
    rarity_level: str
    nfa_applies: bool
    nfa_class: Optional[str]
    required_transfer_form: Optional[str]
    probate_fmv_low: Optional[float]
    probate_fmv_mid: Optional[float]
    probate_fmv_high: Optional[float]
    realized_potential: Optional[float]
    best_venue: Optional[str]
    id_confidence: str
    comp_confidence: str
    photo_filename: str
    key_flags: list
    source_urls: list


def _category(ident: dict) -> str:
    if ident.get("nfa", {}).get("applies"):
        return "NFA Firearm"
    t = (ident.get("type") or "").lower()
    if t == "component":
        return "Component"
    if t in {"pistol", "revolver", "rifle", "shotgun", "smg", "mg"}:
        return "Firearm"
    return "Other"


def build_row(
    ident: dict,
    valuation: Optional[dict],
    photo_filename: str,
    scan_id: str,
    source_urls: Optional[list] = None,
) -> InventoryRow:
    val = valuation or {}
    pf = val.get("probate_fmv") or {}
    rp = val.get("realized_potential") or {}
    return InventoryRow(
        scan_id=scan_id,
        scanned_at_iso=datetime.utcnow().isoformat() + "Z",
        category=_category(ident),
        make=ident.get("make"),
        model=ident.get("model"),
        variant=ident.get("variant"),
        caliber=ident.get("caliber"),
        barrel_length_in=ident.get("barrel_length_in"),
        serial_number=ident.get("serial_number_visible"),
        condition_grade=(ident.get("condition") or {}).get("nra_grade"),
        condition_notes=(ident.get("condition") or {}).get("notes", "") or "",
        rarity_level=(ident.get("rarity") or {}).get("level", "Common"),
        nfa_applies=bool((ident.get("nfa") or {}).get("applies")),
        nfa_class=(ident.get("nfa") or {}).get("class"),
        required_transfer_form=(ident.get("nfa") or {}).get("required_transfer_form"),
        probate_fmv_low=pf.get("low"),
        probate_fmv_mid=pf.get("mid"),
        probate_fmv_high=pf.get("high"),
        realized_potential=rp.get("target"),
        best_venue=rp.get("best_venue"),
        id_confidence=ident.get("id_confidence", "low"),
        comp_confidence=val.get("comp_confidence", "low"),
        photo_filename=photo_filename,
        key_flags=val.get("key_flags", []),
        source_urls=source_urls or [],
    )


def row_to_dict(row: InventoryRow) -> dict:
    return asdict(row)


def row_to_csv_line(row: InventoryRow) -> str:
    def esc(v):
        if v is None:
            return ""
        s = str(v).replace('"', '""')
        return f'"{s}"' if ("," in s or '"' in s or "\n" in s) else s

    fields = [
        row.scan_id, row.scanned_at_iso, row.category, row.make, row.model, row.variant,
        row.caliber, row.barrel_length_in, row.serial_number, row.condition_grade,
        row.condition_notes, row.rarity_level, row.nfa_applies, row.nfa_class,
        row.required_transfer_form, row.probate_fmv_low, row.probate_fmv_mid,
        row.probate_fmv_high, row.realized_potential, row.best_venue,
        row.id_confidence, row.comp_confidence, row.photo_filename,
        "; ".join(row.key_flags), "; ".join(row.source_urls),
    ]
    return ",".join(esc(f) for f in fields)


CSV_HEADER = ",".join([
    "scan_id", "scanned_at_iso", "category", "make", "model", "variant",
    "caliber", "barrel_length_in", "serial_number", "condition_grade",
    "condition_notes", "rarity_level", "nfa_applies", "nfa_class",
    "required_transfer_form", "probate_fmv_low", "probate_fmv_mid",
    "probate_fmv_high", "realized_potential", "best_venue",
    "id_confidence", "comp_confidence", "photo_filename",
    "key_flags", "source_urls",
])
