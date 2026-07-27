# EstateArms Scanner

Photo → data scanner for the DLO estate inventory. Upload a photograph of a firearm,
NFA item, or component and get back a structured identification, dual FMV valuation
scaffold, and a court-ready inventory row.

## Status

- v0.1 (this build): identification + OCR + inventory row + web UI, private/local.
- v0.2 (next): weighted-comp valuation via Perplexity comps + auction-house search.
- v0.3: private auth, Railway deploy at `scanner.estatearms.com`.

## Quick start

```bash
cd /home/user/workspace/estatearms/scanner
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env — add ANTHROPIC_API_KEY (or OPENAI_API_KEY) and optionally GOOGLE_CLOUD_VISION_API_KEY
set -a; source .env; set +a
uvicorn app.main:app --host 127.0.0.1 --port 8787 --reload
```

Open http://127.0.0.1:8787 and drag in a photograph.

## What each piece does

- `app/vision.py` — Claude / GPT-4o abstraction. Loads `prompts/identify.md`
  as the system prompt, sends the image, extracts strict JSON. Falls back to
  a stub if no key is set so the rest of the pipeline stays runnable.
- `app/ocr.py` — Google Cloud Vision REST call for serial + proof mark
  extraction. Regex heuristics pull out serial-like and proof-mark-like tokens.
- `app/inventory.py` — Builds a `InventoryRow` from the identification + valuation
  and can emit either dict or CSV line.
- `app/main.py` — FastAPI server. `/` is the upload UI, `/api/scan` is the
  endpoint, `/api/csv` downloads the running master inventory.
- `prompts/identify.md` — the encoded firearm-photo-id skill logic. Everything
  the vision model knows about "assume rare variant first" and NFA triggers is
  in this file. Edit this to tune behavior.
- `prompts/valuation.md` — dual-track valuation prompt for the v0.2 comp pass.

## Master inventory

Every scan appends one row to `inventory.csv` in the project root. Header matches
the schema in `app/inventory.py::CSV_HEADER`. Download it any time from the UI
or from `GET /api/csv`.

Full JSON scan records are written to `scans/<scan_id>.json` for audit / court.

## Environment variables

See `.env.example`. Minimum viable set: nothing — the scanner runs in stub mode
without any keys, so you can exercise the upload flow, OCR, and inventory row
generator. To get real firearm ID, set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`.

## Next steps (v0.2 valuation loop)

1. On identification, kick off a comp search (GunBroker completed sold, Rock Island
   past-results, Morphy's realized, eBay sold).
2. Feed the identification + comp list into `prompts/valuation.md` to compute
   Probate FMV + Realized Potential with source-tier weighting.
3. Attach comp URLs to the inventory row's `source_urls`.
4. Return the completed valuation in the UI.
