"""
EstateArms Scanner — FastAPI service.

Endpoints:
  GET  /            HTML upload UI
  POST /api/scan    multipart form: photo + optional notes -> full scan result JSON
  GET  /api/csv     download master inventory CSV (all scans this session)
  GET  /healthz     health check

Run locally:
  uvicorn app.main:app --host 127.0.0.1 --port 8787 --reload
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

from . import vision, ocr, inventory


ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = ROOT / "uploads"
SCAN_DIR = ROOT / "scans"
UPLOAD_DIR.mkdir(exist_ok=True)
SCAN_DIR.mkdir(exist_ok=True)
CSV_PATH = ROOT / "inventory.csv"

app = FastAPI(title="EstateArms Scanner", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {
        "ok": True,
        "vision_provider": os.environ.get("VISION_PROVIDER", "auto"),
        "has_anthropic_key": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "has_openai_key": bool(os.environ.get("OPENAI_API_KEY")),
        "has_google_vision_key": bool(os.environ.get("GOOGLE_CLOUD_VISION_API_KEY")),
    }


@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.post("/api/scan")
async def scan(
    photo: UploadFile = File(...),
    notes: str = Form(""),
):
    if not photo.filename:
        raise HTTPException(400, "missing photo filename")

    scan_id = uuid.uuid4().hex[:12]
    ext = Path(photo.filename).suffix.lower() or ".jpg"
    saved = UPLOAD_DIR / f"{scan_id}{ext}"
    saved.write_bytes(await photo.read())

    # 1. Vision identification
    try:
        ident_result = vision.identify(saved, user_notes=notes)
        ident = ident_result.parsed
    except Exception as e:
        raise HTTPException(500, f"vision identify failed: {e}")

    # 2. OCR pass for serials / proof marks (augments the vision reading)
    try:
        ocr_result = ocr.ocr_google(saved)
    except Exception as e:
        ocr_result = ocr.OCRResult(full_text=f"OCR error: {e}", candidate_serials=[], candidate_proof_marks=[], provider="error")

    # Merge OCR-found serials into ident if vision missed one
    if not ident.get("serial_number_visible") and ocr_result.candidate_serials:
        ident["serial_number_visible"] = ocr_result.candidate_serials[0]
        ident.setdefault("visible_markings", []).extend(ocr_result.candidate_serials)
    if ocr_result.candidate_proof_marks:
        ident.setdefault("visible_markings", []).extend(ocr_result.candidate_proof_marks)

    # 3. Valuation — deferred: this scaffold does not auto-run comps yet.
    # Comps require web-search integration; that lives in v0.2. For now we
    # return the identification + OCR and an empty valuation slot the operator
    # can fill via the appraisal-pro skill in a chat session.
    valuation = None

    # 4. Build inventory row
    row = inventory.build_row(
        ident=ident,
        valuation=valuation,
        photo_filename=saved.name,
        scan_id=scan_id,
    )

    # 5. Persist scan record + append CSV
    scan_record = {
        "scan_id": scan_id,
        "identification": ident,
        "ocr": {
            "full_text": ocr_result.full_text,
            "candidate_serials": ocr_result.candidate_serials,
            "candidate_proof_marks": ocr_result.candidate_proof_marks,
            "provider": ocr_result.provider,
        },
        "valuation": valuation,
        "inventory_row": inventory.row_to_dict(row),
        "vision_provider": ident_result.provider,
        "vision_model": ident_result.model,
    }
    (SCAN_DIR / f"{scan_id}.json").write_text(json.dumps(scan_record, indent=2), encoding="utf-8")

    if not CSV_PATH.exists():
        CSV_PATH.write_text(inventory.CSV_HEADER + "\n", encoding="utf-8")
    with CSV_PATH.open("a", encoding="utf-8") as f:
        f.write(inventory.row_to_csv_line(row) + "\n")

    return JSONResponse(scan_record)


@app.get("/api/csv")
def download_csv():
    if not CSV_PATH.exists():
        return PlainTextResponse(inventory.CSV_HEADER + "\n", media_type="text/csv")
    return FileResponse(CSV_PATH, media_type="text/csv", filename="estatearms_inventory.csv")


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>EstateArms Scanner</title>
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
  :root { --bg:#0e1116; --card:#161b22; --ink:#e6edf3; --muted:#8b949e; --accent:#f0a04b; --ok:#3fb950; --warn:#d29922; --err:#f85149; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
  header { padding:20px 24px; border-bottom:1px solid #21262d; display:flex; align-items:center; justify-content:space-between; }
  header h1 { margin:0; font-size:18px; letter-spacing:.3px; }
  header .status { font-size:12px; color:var(--muted); }
  main { max-width: 960px; margin: 0 auto; padding: 24px; }
  .card { background:var(--card); border:1px solid #21262d; border-radius:10px; padding:20px; margin-bottom:18px; }
  label { display:block; font-size:12px; color:var(--muted); margin-bottom:6px; text-transform:uppercase; letter-spacing:.5px; }
  input[type=file], textarea { width:100%; background:#0d1117; color:var(--ink); border:1px solid #30363d; border-radius:6px; padding:10px; font:inherit; }
  textarea { min-height:70px; resize:vertical; }
  button { background:var(--accent); color:#1a1a1a; border:0; padding:10px 18px; border-radius:6px; font-weight:600; cursor:pointer; }
  button:disabled { opacity:.5; cursor:not-allowed; }
  .row { display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
  .kv { font-size:14px; }
  .kv b { color:var(--muted); font-weight:500; display:inline-block; min-width:150px; }
  pre { background:#0d1117; border:1px solid #21262d; border-radius:6px; padding:12px; overflow:auto; font-size:12px; }
  .flag { display:inline-block; background:#21262d; color:var(--warn); padding:2px 8px; border-radius:12px; font-size:11px; margin:2px 4px 2px 0; }
  .nfa { color:var(--err); font-weight:700; }
  .ok { color:var(--ok); }
  .muted { color:var(--muted); }
  a { color:var(--accent); }
</style>
</head>
<body>
<header>
  <h1>EstateArms — Photo → Data Scanner</h1>
  <div class="status" id="status">checking backend…</div>
</header>
<main>
  <div class="card">
    <form id="scanForm">
      <label for="photo">Photograph</label>
      <input id="photo" name="photo" type="file" accept="image/*" required />
      <div style="height:12px"></div>
      <label for="notes">Notes (optional — provenance, side of firearm shown, prior identification)</label>
      <textarea id="notes" name="notes" placeholder="e.g. Right side, DLO estate lot #7, previously described as Colt Series 70"></textarea>
      <div style="height:14px"></div>
      <button type="submit" id="submitBtn">Scan</button>
      <a href="/api/csv" style="margin-left:14px" class="muted">Download inventory CSV</a>
    </form>
  </div>

  <div id="result"></div>
</main>

<script>
async function refreshStatus() {
  const r = await fetch('/healthz');
  const j = await r.json();
  const parts = [];
  parts.push(j.has_anthropic_key ? 'anthropic ✓' : 'anthropic ✗');
  parts.push(j.has_openai_key ? 'openai ✓' : 'openai ✗');
  parts.push(j.has_google_vision_key ? 'gcv ✓' : 'gcv ✗');
  document.getElementById('status').textContent = parts.join(' · ');
}
refreshStatus();

function fmt(v) {
  if (v === null || v === undefined || v === '') return '<span class="muted">—</span>';
  if (typeof v === 'boolean') return v ? 'yes' : 'no';
  return String(v);
}

function render(r) {
  const i = r.identification;
  const rw = r.inventory_row;
  const nfa = i.nfa || {};
  const ocr = r.ocr || {};
  const val = r.valuation || {};
  const nfaBadge = nfa.applies ? `<span class="nfa">NFA — ${fmt(nfa.class)} — ${fmt(nfa.required_transfer_form)}</span>` : '<span class="ok">Not NFA-regulated</span>';

  return `
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div><b>Scan</b> <code>${r.scan_id}</code> · via ${r.vision_provider}/${r.vision_model}</div>
        <div>${nfaBadge}</div>
      </div>
      <div class="row">
        <div>
          <div class="kv"><b>Type</b> ${fmt(i.type)}</div>
          <div class="kv"><b>Make</b> ${fmt(i.make)}</div>
          <div class="kv"><b>Model</b> ${fmt(i.model)}</div>
          <div class="kv"><b>Variant</b> ${fmt(i.variant)}</div>
          <div class="kv"><b>Caliber</b> ${fmt(i.caliber)}</div>
          <div class="kv"><b>Barrel (in)</b> ${fmt(i.barrel_length_in)}</div>
          <div class="kv"><b>Era</b> ${fmt(i.era)}</div>
          <div class="kv"><b>Finish</b> ${fmt(i.finish)}</div>
          <div class="kv"><b>Grips/Stock</b> ${fmt(i.grips_stock)}</div>
        </div>
        <div>
          <div class="kv"><b>Serial (visible)</b> ${fmt(i.serial_number_visible)}</div>
          <div class="kv"><b>Condition</b> ${fmt(i.condition?.nra_grade)} (${fmt(i.condition?.finish_pct_estimate)}%)</div>
          <div class="kv"><b>Rarity</b> ${fmt(i.rarity?.level)}</div>
          <div class="kv"><b>ID confidence</b> ${fmt(i.id_confidence)}</div>
          <div class="kv"><b>Category</b> ${fmt(rw.category)}</div>
          <div class="kv"><b>OCR provider</b> ${fmt(ocr.provider)}</div>
          <div class="kv"><b>OCR serial candidates</b> ${(ocr.candidate_serials||[]).map(s=>`<span class="flag">${s}</span>`).join('') || '<span class="muted">—</span>'}</div>
          <div class="kv"><b>OCR proof marks</b> ${(ocr.candidate_proof_marks||[]).map(s=>`<span class="flag">${s}</span>`).join('') || '<span class="muted">—</span>'}</div>
        </div>
      </div>

      <div style="margin-top:14px">
        <div class="muted" style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px">Rarity factors</div>
        ${(i.rarity?.factors||[]).map(f=>`<span class="flag">${f}</span>`).join('') || '<span class="muted">none flagged</span>'}
      </div>

      <div style="margin-top:14px">
        <div class="muted" style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px">Visible markings</div>
        ${(i.visible_markings||[]).map(f=>`<span class="flag">${f}</span>`).join('') || '<span class="muted">none</span>'}
      </div>

      <div style="margin-top:14px">
        <div class="muted" style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px">Reasoning</div>
        <div>${fmt(i.reasoning_brief)}</div>
      </div>

      <div style="margin-top:14px">
        <div class="muted" style="font-size:11px; text-transform:uppercase; letter-spacing:.5px; margin-bottom:6px">Would raise confidence</div>
        ${(i.what_would_raise_confidence||[]).map(f=>`<span class="flag">${f}</span>`).join('') || '<span class="muted">—</span>'}
      </div>

      <details style="margin-top:16px">
        <summary class="muted">Raw JSON scan record</summary>
        <pre>${JSON.stringify(r, null, 2)}</pre>
      </details>
    </div>
  `;
}

document.getElementById('scanForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = document.getElementById('submitBtn');
  const result = document.getElementById('result');
  btn.disabled = true; btn.textContent = 'Scanning…';
  result.innerHTML = '<div class="card muted">Uploading and analyzing…</div>';
  try {
    const fd = new FormData();
    fd.append('photo', document.getElementById('photo').files[0]);
    fd.append('notes', document.getElementById('notes').value);
    const r = await fetch('/api/scan', { method: 'POST', body: fd });
    if (!r.ok) throw new Error(await r.text());
    const j = await r.json();
    result.innerHTML = render(j);
  } catch (err) {
    result.innerHTML = `<div class="card"><span class="nfa">Error:</span> ${err.message}</div>`;
  } finally {
    btn.disabled = false; btn.textContent = 'Scan';
  }
});
</script>
</body>
</html>
"""
