#!/usr/bin/env python3
"""
PHASE 1.2: Promise Extraction - Prepare batches for LLM processing
This script prepares page batches and tracks progress.
LLM calls will be made externally.
"""

import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
import glob

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
PAGES_DIR = DATA_DIR / "pdfs" / "pages"
PROMISES_DIR = DATA_DIR / "promises"
PROCESSING_DIR = DATA_DIR / "processing"

# Party definitions
PARTIES = [
    {"name": "Peru Libre", "slug": "peru_libre", "code": "PL"},
    {"name": "Fuerza Popular", "slug": "fuerza_popular", "code": "FP"},
    {"name": "Alianza para el Progreso", "slug": "alianza_progreso", "code": "APP"},
    {"name": "Renovacion Popular", "slug": "renovacion_popular", "code": "RP"},
    {"name": "Avanza Pais", "slug": "avanza_pais", "code": "APAIS"},
    {"name": "Podemos Peru", "slug": "podemos_peru", "code": "PP"},
    {"name": "Juntos por el Peru", "slug": "juntos_peru", "code": "JP"},
    {"name": "Somos Peru", "slug": "somos_peru", "code": "SP"},
    {"name": "Partido Morado", "slug": "partido_morado", "code": "PM"}
]

VALID_CATEGORIES = [
    "seguridad", "economia", "fiscal", "social", "empleo",
    "educacion", "salud", "agua", "vivienda", "transporte",
    "energia", "mineria", "ambiente", "agricultura", "justicia"
]

def get_timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_progress():
    progress_path = PROCESSING_DIR / "extraction_progress.json"
    if progress_path.exists():
        with open(progress_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"batches_completed": [], "party_year_complete": []}

def save_progress(progress):
    progress_path = PROCESSING_DIR / "extraction_progress.json"
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def get_pages_for_party_year(party_slug, year):
    """Get all page files for a party/year combination."""
    pages_dir = PAGES_DIR / f"{party_slug}_{year}"
    if not pages_dir.exists():
        return []

    page_files = sorted(pages_dir.glob("page_*.txt"))
    return page_files

def prepare_batch(page_files, batch_start, batch_size=5):
    """Prepare a batch of pages for LLM processing."""
    batch_end = min(batch_start + batch_size, len(page_files))
    batch_pages = page_files[batch_start:batch_end]

    combined_text = ""
    for i, page_path in enumerate(batch_pages):
        page_num = batch_start + i + 1
        with open(page_path, 'r', encoding='utf-8') as f:
            page_text = f.read()
        combined_text += f"\n\n=== PAGE {page_num} ===\n\n{page_text}"

    return combined_text, batch_end - batch_start

def get_next_batch_to_process(progress):
    """Find the next unprocessed batch."""
    for party in PARTIES:
        for year in [2021, 2026]:
            party_year_key = f"{party['slug']}_{year}"

            # Skip if party/year is fully complete
            if party_year_key in progress.get("party_year_complete", []):
                continue

            page_files = get_pages_for_party_year(party["slug"], year)
            if not page_files:
                continue

            total_pages = len(page_files)

            # Find next unprocessed batch
            for batch_start in range(0, total_pages, 5):
                batch_key = f"{party_year_key}_{batch_start}"
                if batch_key not in progress.get("batches_completed", []):
                    return {
                        "party": party,
                        "year": year,
                        "party_year_key": party_year_key,
                        "batch_start": batch_start,
                        "batch_key": batch_key,
                        "page_files": page_files,
                        "total_pages": total_pages
                    }

    return None

def validate_promise(promise):
    """Validate a single promise object."""
    errors = []

    if not promise.get("text"):
        errors.append("Empty text")

    if promise.get("category") not in VALID_CATEGORIES:
        errors.append(f"Invalid category: {promise.get('category')}")

    if promise.get("secondary_category") and promise["secondary_category"] not in VALID_CATEGORIES:
        errors.append(f"Invalid secondary_category: {promise['secondary_category']}")

    if not promise.get("action_verb"):
        errors.append("Empty action_verb")

    if promise.get("extraction_quality") not in ["clear", "ambiguous"]:
        errors.append(f"Invalid extraction_quality: {promise.get('extraction_quality')}")

    if promise.get("extraction_quality") == "ambiguous" and not promise.get("source_quote"):
        errors.append("Ambiguous extraction missing source_quote")

    return errors

def validate_llm_response(response):
    """Validate the full LLM response."""
    try:
        if isinstance(response, str):
            response = json.loads(response)

        if "promises" not in response:
            return False, "Missing 'promises' key", None

        if not isinstance(response["promises"], list):
            return False, "'promises' is not an array", None

        if "page_summary" not in response:
            return False, "Missing 'page_summary' key", None

        # Validate each promise
        all_errors = []
        for i, promise in enumerate(response["promises"]):
            errors = validate_promise(promise)
            if errors:
                all_errors.append(f"Promise {i}: {', '.join(errors)}")

        if all_errors:
            return False, "\n".join(all_errors), response

        return True, None, response

    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}", None

def list_pending_batches():
    """List all pending batches that need to be processed."""
    progress = load_progress()
    pending = []

    for party in PARTIES:
        for year in [2021, 2026]:
            party_year_key = f"{party['slug']}_{year}"

            if party_year_key in progress.get("party_year_complete", []):
                continue

            page_files = get_pages_for_party_year(party["slug"], year)
            if not page_files:
                continue

            total_pages = len(page_files)

            for batch_start in range(0, total_pages, 5):
                batch_key = f"{party_year_key}_{batch_start}"
                if batch_key not in progress.get("batches_completed", []):
                    batch_end = min(batch_start + 5, total_pages)
                    pending.append({
                        "party": party["name"],
                        "slug": party["slug"],
                        "year": year,
                        "batch_key": batch_key,
                        "pages": f"{batch_start+1}-{batch_end}",
                        "total_pages": total_pages
                    })

    return pending

def get_batch_info(batch_key):
    """Get detailed info for a specific batch."""
    progress = load_progress()

    # Parse batch_key: party_slug_year_batchstart
    parts = batch_key.rsplit("_", 1)
    if len(parts) != 2:
        return None

    party_year_key = parts[0]
    batch_start = int(parts[1])

    # Parse party_year_key
    for party in PARTIES:
        for year in [2021, 2026]:
            if f"{party['slug']}_{year}" == party_year_key:
                page_files = get_pages_for_party_year(party["slug"], year)
                combined_text, batch_size = prepare_batch(page_files, batch_start)

                return {
                    "party_name": party["name"],
                    "party_slug": party["slug"],
                    "party_code": party["code"],
                    "year": year,
                    "batch_start": batch_start,
                    "batch_size": batch_size,
                    "total_pages": len(page_files),
                    "combined_text": combined_text,
                    "batch_key": batch_key
                }

    return None

def save_batch_result(batch_key, llm_response, promises_with_ids):
    """Save the result of a processed batch."""
    progress = load_progress()

    # Mark batch as completed
    if batch_key not in progress["batches_completed"]:
        progress["batches_completed"].append(batch_key)

    save_progress(progress)

    # Save individual batch result for recovery
    batch_results_dir = PROCESSING_DIR / "batch_results"
    batch_results_dir.mkdir(exist_ok=True)

    result_file = batch_results_dir / f"{batch_key}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "batch_key": batch_key,
            "timestamp": get_timestamp(),
            "promises_count": len(promises_with_ids),
            "promises": promises_with_ids
        }, f, indent=2, ensure_ascii=False)

def finalize_party_year(party_slug, year, all_promises):
    """Finalize and save promises for a party/year."""
    progress = load_progress()
    party_year_key = f"{party_slug}_{year}"

    # Get party info
    party_info = next((p for p in PARTIES if p["slug"] == party_slug), None)
    if not party_info:
        return False

    # Deduplicate promises
    seen_texts = set()
    unique_promises = []
    for p in all_promises:
        normalized = p["text"].lower().strip()
        if normalized not in seen_texts:
            seen_texts.add(normalized)
            unique_promises.append(p)

    # Calculate stats
    stats = {
        "total_extracted": len(unique_promises),
        "clear": len([p for p in unique_promises if p["extraction_quality"] == "clear"]),
        "ambiguous": len([p for p in unique_promises if p["extraction_quality"] == "ambiguous"]),
        "by_category": {}
    }

    for cat in VALID_CATEGORIES:
        stats["by_category"][cat] = len([p for p in unique_promises if p["category"] == cat])

    # Get page count
    page_files = get_pages_for_party_year(party_slug, year)

    # Build output
    output = {
        "party": party_info["name"],
        "party_slug": party_slug,
        "year": year,
        "extraction_date": get_timestamp(),
        "total_pages_processed": len(page_files),
        "promises": unique_promises,
        "extraction_stats": stats
    }

    # Save party/year file
    PROMISES_DIR.mkdir(exist_ok=True)
    output_file = PROMISES_DIR / f"{party_slug}_{year}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Mark party/year as complete
    if party_year_key not in progress.get("party_year_complete", []):
        if "party_year_complete" not in progress:
            progress["party_year_complete"] = []
        progress["party_year_complete"].append(party_year_key)

    save_progress(progress)

    print(f"Saved {len(unique_promises)} promises for {party_info['name']} {year}")
    return True

def check_party_year_complete(party_slug, year):
    """Check if all batches for a party/year are complete."""
    progress = load_progress()
    party_year_key = f"{party_slug}_{year}"

    page_files = get_pages_for_party_year(party_slug, year)
    if not page_files:
        return True  # No pages = complete

    total_pages = len(page_files)

    for batch_start in range(0, total_pages, 5):
        batch_key = f"{party_year_key}_{batch_start}"
        if batch_key not in progress.get("batches_completed", []):
            return False

    return True

def collect_party_year_promises(party_slug, year):
    """Collect all promises from batch results for a party/year."""
    party_year_key = f"{party_slug}_{year}"
    batch_results_dir = PROCESSING_DIR / "batch_results"

    all_promises = []

    page_files = get_pages_for_party_year(party_slug, year)
    total_pages = len(page_files)

    for batch_start in range(0, total_pages, 5):
        batch_key = f"{party_year_key}_{batch_start}"
        result_file = batch_results_dir / f"{batch_key}.json"

        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
                all_promises.extend(batch_data.get("promises", []))

    return all_promises

def merge_all_promises():
    """Merge all party/year files into data/promises.json."""
    all_promises = {
        "extraction_date": get_timestamp(),
        "parties": {}
    }

    for party in PARTIES:
        party_data = {}
        for year in [2021, 2026]:
            file_path = PROMISES_DIR / f"{party['slug']}_{year}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    party_data[str(year)] = json.load(f)

        if party_data:
            all_promises["parties"][party["slug"]] = party_data

    output_file = DATA_DIR / "promises.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_promises, f, indent=2, ensure_ascii=False)

    print(f"Merged promises saved to {output_file}")
    return True

def validate_phase():
    """Run final validation for Phase 1.2."""
    progress = load_progress()

    validation = {
        "phase": "1.2",
        "phase_name": "Promise Extraction",
        "started_at": None,
        "completed_at": get_timestamp(),
        "parties_processed": 0,
        "years_processed": [2021, 2026],
        "total_batches": 0,
        "successful_batches": 0,
        "failed_batches": 0,
        "total_promises_extracted": 0,
        "promises_by_party": {},
        "validation_checks": {
            "all_parties_have_promises": True,
            "all_categories_valid": True,
            "no_empty_texts": True,
            "no_null_action_verbs": True,
            "ambiguous_have_quotes": True,
            "all_ids_unique": True,
            "merged_file_created": False
        },
        "status": "FAIL"
    }

    all_ids = set()

    for party in PARTIES:
        party_promises = {"2021": 0, "2026": 0}

        for year in [2021, 2026]:
            file_path = PROMISES_DIR / f"{party['slug']}_{year}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                promises = data.get("promises", [])
                party_promises[str(year)] = len(promises)
                validation["total_promises_extracted"] += len(promises)

                # Validate promises
                for p in promises:
                    if p.get("id"):
                        if p["id"] in all_ids:
                            validation["validation_checks"]["all_ids_unique"] = False
                        all_ids.add(p["id"])

                    if not p.get("text"):
                        validation["validation_checks"]["no_empty_texts"] = False

                    if not p.get("action_verb"):
                        validation["validation_checks"]["no_null_action_verbs"] = False

                    if p.get("category") not in VALID_CATEGORIES:
                        validation["validation_checks"]["all_categories_valid"] = False

                    if p.get("extraction_quality") == "ambiguous" and not p.get("source_quote"):
                        validation["validation_checks"]["ambiguous_have_quotes"] = False

        validation["promises_by_party"][party["slug"]] = party_promises

        if party_promises["2021"] == 0 or party_promises["2026"] == 0:
            validation["validation_checks"]["all_parties_have_promises"] = False
        else:
            validation["parties_processed"] += 1

    # Check merged file
    merged_path = DATA_DIR / "promises.json"
    validation["validation_checks"]["merged_file_created"] = merged_path.exists()

    # Count batches
    validation["successful_batches"] = len(progress.get("batches_completed", []))

    # Calculate total expected batches
    total_batches = 0
    for party in PARTIES:
        for year in [2021, 2026]:
            page_files = get_pages_for_party_year(party["slug"], year)
            total_batches += (len(page_files) + 4) // 5
    validation["total_batches"] = total_batches

    # Overall status
    if (validation["total_promises_extracted"] >= 300 and
        validation["parties_processed"] == 9 and
        all(validation["validation_checks"].values())):
        validation["status"] = "PASS"

    # Save validation
    val_path = PROCESSING_DIR / "phase_1_2_validation.json"
    with open(val_path, 'w', encoding='utf-8') as f:
        json.dump(validation, f, indent=2, ensure_ascii=False)

    return validation

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python phase_1_2_promise_extraction.py list     - List pending batches")
        print("  python phase_1_2_promise_extraction.py next     - Get next batch to process")
        print("  python phase_1_2_promise_extraction.py get <batch_key>  - Get batch content")
        print("  python phase_1_2_promise_extraction.py save <batch_key> '<json>'  - Save batch result")
        print("  python phase_1_2_promise_extraction.py finalize <party_slug> <year>  - Finalize party/year")
        print("  python phase_1_2_promise_extraction.py merge    - Merge all promises")
        print("  python phase_1_2_promise_extraction.py validate - Run phase validation")
        print("  python phase_1_2_promise_extraction.py status   - Show overall status")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        pending = list_pending_batches()
        print(f"Pending batches: {len(pending)}")
        for b in pending[:20]:  # Show first 20
            print(f"  {b['batch_key']}: {b['party']} {b['year']} pages {b['pages']} (of {b['total_pages']})")
        if len(pending) > 20:
            print(f"  ... and {len(pending) - 20} more")

    elif cmd == "next":
        progress = load_progress()
        batch = get_next_batch_to_process(progress)
        if batch:
            print(json.dumps({
                "batch_key": batch["batch_key"],
                "party": batch["party"]["name"],
                "slug": batch["party"]["slug"],
                "code": batch["party"]["code"],
                "year": batch["year"],
                "batch_start": batch["batch_start"],
                "total_pages": batch["total_pages"]
            }))
        else:
            print("NO_MORE_BATCHES")

    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Usage: python phase_1_2_promise_extraction.py get <batch_key>")
            return

        batch_key = sys.argv[2]
        info = get_batch_info(batch_key)
        if info:
            print(json.dumps({
                "party_name": info["party_name"],
                "party_code": info["party_code"],
                "year": info["year"],
                "batch_start": info["batch_start"],
                "batch_size": info["batch_size"],
                "total_pages": info["total_pages"],
                "page_text": info["combined_text"]
            }, ensure_ascii=False))
        else:
            print("BATCH_NOT_FOUND")

    elif cmd == "save":
        if len(sys.argv) < 4:
            print("Usage: python phase_1_2_promise_extraction.py save <batch_key> '<json>'")
            return

        batch_key = sys.argv[2]
        json_str = sys.argv[3]

        try:
            response = json.loads(json_str)
            valid, error, parsed = validate_llm_response(response)

            if not valid:
                print(f"VALIDATION_ERROR: {error}")
                return

            # Get batch info to assign IDs
            info = get_batch_info(batch_key)
            if not info:
                print("BATCH_NOT_FOUND")
                return

            # Load existing promises count for this party/year
            batch_results_dir = PROCESSING_DIR / "batch_results"
            batch_results_dir.mkdir(exist_ok=True)

            # Count existing promises for ID generation
            existing_count = 0
            party_year_key = f"{info['party_slug']}_{info['year']}"
            for f in batch_results_dir.glob(f"{party_year_key}_*.json"):
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                    existing_count += len(data.get("promises", []))

            # Assign IDs to promises
            promises_with_ids = []
            for i, promise in enumerate(parsed["promises"]):
                promise["id"] = f"{info['party_code']}-{info['year']}-{existing_count + i + 1:03d}"
                promise["source_page"] = info["batch_start"] + 1  # approximate
                promises_with_ids.append(promise)

            save_batch_result(batch_key, parsed, promises_with_ids)
            print(f"SAVED: {len(promises_with_ids)} promises")

        except json.JSONDecodeError as e:
            print(f"JSON_ERROR: {e}")

    elif cmd == "finalize":
        if len(sys.argv) < 4:
            print("Usage: python phase_1_2_promise_extraction.py finalize <party_slug> <year>")
            return

        party_slug = sys.argv[2]
        year = int(sys.argv[3])

        # Check if all batches are complete
        if not check_party_year_complete(party_slug, year):
            print(f"NOT_COMPLETE: Some batches still pending for {party_slug}_{year}")
            return

        # Collect and save
        promises = collect_party_year_promises(party_slug, year)
        success = finalize_party_year(party_slug, year, promises)

        if success:
            print(f"FINALIZED: {party_slug}_{year}")
        else:
            print("FINALIZE_FAILED")

    elif cmd == "merge":
        merge_all_promises()
        print("MERGED")

    elif cmd == "validate":
        validation = validate_phase()
        print(json.dumps(validation, indent=2))

    elif cmd == "status":
        progress = load_progress()
        pending = list_pending_batches()

        print(f"Batches completed: {len(progress.get('batches_completed', []))}")
        print(f"Batches pending: {len(pending)}")
        print(f"Party/years complete: {progress.get('party_year_complete', [])}")

if __name__ == "__main__":
    main()
