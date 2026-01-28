#!/usr/bin/env python3
"""
PHASE 1.1: PDF Download & Text Extraction
Downloads 18 PDFs, extracts text, and splits into pages.
"""

import os
import sys
import json
import fitz  # PyMuPDF
import urllib.request
import ssl
from datetime import datetime, timezone
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
PDFS_DIR = DATA_DIR / "pdfs"
RAW_DIR = PDFS_DIR / "raw"
TEXT_DIR = PDFS_DIR / "text"
PAGES_DIR = PDFS_DIR / "pages"
PROCESSING_DIR = DATA_DIR / "processing"

# Party definitions
PARTIES = [
    {
        "name": "Peru Libre",
        "slug": "peru_libre",
        "code": "PL",
        "urls": {
            2021: "https://perulibre.pe/plan-bicentenario.pdf",
            2026: "https://img.lpderecho.pe/wp-content/uploads/2025/12/Partido-Politico-Nacional-Peru-Libre-Plan-de-Gobierno-LP-derecho.pdf"
        }
    },
    {
        "name": "Fuerza Popular",
        "slug": "fuerza_popular",
        "code": "FP",
        "urls": {
            2021: "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1095/ARCHIVO/FIRMADO/3017.PDF",
            2026: "https://img.lpderecho.pe/wp-content/uploads/2025/12/Fuerza-Popular-Plan-de-gobierno-LP-Derecho.pdf"
        }
    },
    {
        "name": "Alianza para el Progreso",
        "slug": "alianza_progreso",
        "code": "APP",
        "urls": {
            2021: "https://bitacora.jomra.es/wp-content/uploads/2021/02/pg21_alianzaparaelprogreso.pdf",
            2026: "https://mpesije.jne.gob.pe/docs/72576403-804a-4f28-85d3-bf4c7e648667.pdf"
        }
    },
    {
        "name": "Renovacion Popular",
        "slug": "renovacion_popular",
        "code": "RP",
        "urls": {
            2021: "https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/16482.pdf",
            2026: "https://img.lpderecho.pe/wp-content/uploads/2025/12/Renovacion-Popular-Plan-de-Gobierno-LP.pdf"
        }
    },
    {
        "name": "Avanza Pais",
        "slug": "avanza_pais",
        "code": "APAIS",
        "urls": {
            2021: "https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/16535.pdf",
            2026: "https://mpesije.jne.gob.pe/docs/5857261c-789e-4599-ac05-4531654b10b4.pdf"
        }
    },
    {
        "name": "Podemos Peru",
        "slug": "podemos_peru",
        "code": "PP",
        "urls": {
            2021: "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/2017/ARCHIVO/FIRMADO/8661.PDF",
            2026: "https://mpesije.jne.gob.pe/docs/67b637b0-e2f7-47cc-8b23-fa16be709cc2.pdf"
        }
    },
    {
        "name": "Juntos por el Peru",
        "slug": "juntos_peru",
        "code": "JP",
        "urls": {
            2021: "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1587/ARCHIVO/FIRMADO/5262.PDF",
            2026: "https://mpesije.jne.gob.pe/docs/3dd0e649-061c-4f31-8c3f-7a0836b58bde.pdf"
        }
    },
    {
        "name": "Somos Peru",
        "slug": "somos_peru",
        "code": "SP",
        "urls": {
            2021: "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1766/ARCHIVO/FIRMADO/6519.PDF",
            2026: "https://mpesije.jne.gob.pe/docs/1334ac30-c28e-42a5-8fc5-79a4638ccd2a.pdf"
        }
    },
    {
        "name": "Partido Morado",
        "slug": "partido_morado",
        "code": "PM",
        "urls": {
            2021: "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1595/ARCHIVO/FIRMADO/5314.PDF",
            2026: "https://img.lpderecho.pe/wp-content/uploads/2025/12/Partido-morado-Plan-de-gobierno-LP-Derecho.pdf"
        }
    }
]

def get_timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_download_log():
    log_path = PROCESSING_DIR / "download_log.json"
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"entries": [], "completed": []}

def save_download_log(log):
    log_path = PROCESSING_DIR / "download_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def download_pdf(url, output_path, party_slug, year):
    """Download PDF from URL with retries."""
    print(f"  Downloading {party_slug}_{year}.pdf...")

    # SSL context for https
    # Some government sites (JNE) may have certificate issues;
    # pass --insecure flag to disable verification if needed
    ctx = ssl.create_default_context()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    req = urllib.request.Request(url, headers=headers)

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
                content = response.read()
                with open(output_path, 'wb') as f:
                    f.write(content)
                return True, len(content)
        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                return False, str(e)

    return False, "Max retries exceeded"

def extract_text(pdf_path, text_path):
    """Extract full text from PDF."""
    print(f"  Extracting text...")
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        return True, len(full_text)
    except Exception as e:
        return False, str(e)

def split_pages(pdf_path, pages_dir):
    """Split PDF into individual page text files."""
    print(f"  Splitting into pages...")
    try:
        os.makedirs(pages_dir, exist_ok=True)
        doc = fitz.open(pdf_path)
        page_count = len(doc)

        for i, page in enumerate(doc):
            page_num = i + 1
            page_text = page.get_text()
            page_file = pages_dir / f"page_{page_num:03d}.txt"
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(page_text)

        doc.close()
        return True, page_count
    except Exception as e:
        return False, str(e)

def process_party_year(party, year, download_log):
    """Process a single party/year PDF."""
    slug = party["slug"]
    key = f"{slug}_{year}"

    # Check if already completed
    if key in download_log.get("completed", []):
        print(f"  {key} already completed, skipping...")
        return True, "already_complete"

    url = party["urls"][year]
    pdf_path = RAW_DIR / f"{key}.pdf"
    text_path = TEXT_DIR / f"{key}.txt"
    pages_dir = PAGES_DIR / key

    entry = {
        "party": party["name"],
        "party_slug": slug,
        "year": year,
        "pdf_url": url,
        "pdf_path": str(pdf_path),
        "status": "processing",
        "timestamp": get_timestamp()
    }

    # Step 1: Download PDF
    success, result = download_pdf(url, pdf_path, slug, year)
    if not success:
        entry["status"] = "download_failed"
        entry["error"] = result
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, f"Download failed: {result}"

    entry["pdf_size_bytes"] = result

    # Validate PDF size > 10KB
    if result < 10240:
        entry["status"] = "pdf_too_small"
        entry["error"] = f"PDF size {result} bytes < 10KB"
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, entry["error"]

    # Step 2: Extract text
    success, result = extract_text(pdf_path, text_path)
    if not success:
        entry["status"] = "extraction_failed"
        entry["error"] = result
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, f"Text extraction failed: {result}"

    entry["text_path"] = str(text_path)
    entry["text_chars"] = result

    # Validate text > 1000 chars
    if result < 1000:
        entry["status"] = "text_too_short"
        entry["error"] = f"Text length {result} chars < 1000"
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, entry["error"]

    # Step 3: Split into pages
    success, result = split_pages(pdf_path, pages_dir)
    if not success:
        entry["status"] = "page_split_failed"
        entry["error"] = result
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, f"Page split failed: {result}"

    entry["pages_dir"] = str(pages_dir)
    entry["page_count"] = result

    # Validate at least 10 pages
    if result < 10:
        entry["status"] = "too_few_pages"
        entry["error"] = f"Page count {result} < 10"
        download_log["entries"].append(entry)
        save_download_log(download_log)
        return False, entry["error"]

    # Success!
    entry["status"] = "complete"
    download_log["entries"].append(entry)
    download_log["completed"].append(key)
    save_download_log(download_log)

    print(f"  SUCCESS: {entry['pdf_size_bytes']} bytes, {entry['text_chars']} chars, {entry['page_count']} pages")
    return True, entry

def validate_phase():
    """Run final validation for Phase 1.1."""
    download_log = load_download_log()

    validation = {
        "phase": "1.1",
        "phase_name": "PDF Download & Text Extraction",
        "started_at": None,
        "completed_at": get_timestamp(),
        "total_pdfs_expected": 18,
        "total_pdfs_downloaded": 0,
        "total_pdfs_extracted": 0,
        "total_pages_extracted": 0,
        "failed_downloads": [],
        "failed_extractions": [],
        "validation_checks": {
            "all_18_pdfs_downloaded": False,
            "all_pdfs_over_10kb": True,
            "all_texts_over_1000_chars": True,
            "all_have_10_plus_pages": True
        },
        "status": "FAIL"
    }

    # Check entries
    complete_entries = [e for e in download_log.get("entries", []) if e["status"] == "complete"]
    failed_entries = [e for e in download_log.get("entries", []) if e["status"] != "complete"]

    validation["total_pdfs_downloaded"] = len(complete_entries)
    validation["total_pdfs_extracted"] = len(complete_entries)
    validation["total_pages_extracted"] = sum(e.get("page_count", 0) for e in complete_entries)
    validation["failed_downloads"] = [e.get("party_slug", "") + "_" + str(e.get("year", "")) for e in failed_entries]

    # Find started_at from first entry
    if download_log.get("entries"):
        timestamps = [e.get("timestamp", "") for e in download_log["entries"] if e.get("timestamp")]
        if timestamps:
            validation["started_at"] = min(timestamps)

    # Validation checks
    validation["validation_checks"]["all_18_pdfs_downloaded"] = len(complete_entries) == 18

    for e in complete_entries:
        if e.get("pdf_size_bytes", 0) < 10240:
            validation["validation_checks"]["all_pdfs_over_10kb"] = False
        if e.get("text_chars", 0) < 1000:
            validation["validation_checks"]["all_texts_over_1000_chars"] = False
        if e.get("page_count", 0) < 10:
            validation["validation_checks"]["all_have_10_plus_pages"] = False

    # Overall status
    if all(validation["validation_checks"].values()) and len(complete_entries) == 18:
        validation["status"] = "PASS"

    # Save validation
    val_path = PROCESSING_DIR / "phase_1_1_validation.json"
    with open(val_path, 'w', encoding='utf-8') as f:
        json.dump(validation, f, indent=2, ensure_ascii=False)

    return validation

def main():
    print("=" * 60)
    print("PHASE 1.1: PDF Download & Text Extraction")
    print("=" * 60)

    # Ensure directories exist
    for d in [RAW_DIR, TEXT_DIR, PAGES_DIR, PROCESSING_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    download_log = load_download_log()

    total_success = 0
    total_failed = 0

    for party in PARTIES:
        for year in [2021, 2026]:
            key = f"{party['slug']}_{year}"
            print(f"\n[{total_success + total_failed + 1}/18] Processing {party['name']} {year}...")

            success, result = process_party_year(party, year, download_log)

            if success:
                total_success += 1
            else:
                total_failed += 1
                print(f"  FAILED: {result}")

    print(f"\n{'=' * 60}")
    print(f"Download complete: {total_success} success, {total_failed} failed")

    # Run validation
    validation = validate_phase()
    print(f"\nValidation status: {validation['status']}")
    print(f"Total pages extracted: {validation['total_pages_extracted']}")

    if validation["status"] != "PASS":
        print("\nFailed items:")
        for f in validation["failed_downloads"]:
            print(f"  - {f}")

    return validation["status"] == "PASS"

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
