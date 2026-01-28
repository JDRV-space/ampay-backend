#!/usr/bin/env python3
"""
Phase 1.3: Vote Classification
Classifies congressional votes into categories using LLM.

Usage:
  python classify_votes.py --batch-start 0 --batch-end 5  # Run batches 0-4 (100 votes)
  python classify_votes.py --all                          # Run all 112 batches
  python classify_votes.py --sample                       # Run 3 batches as test
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import time

# Configuration
BATCH_SIZE = 20
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
VOTE_INDEX_PATH = DATA_DIR / "congress" / "vote_index.json"
OUTPUT_PATH = DATA_DIR / "votes_categorized.json"
CHECKPOINT_DIR = DATA_DIR / "votes"
PROCESSING_DIR = DATA_DIR / "processing"

VALID_CATEGORIES = [
    "seguridad", "economia", "fiscal", "social", "empleo",
    "educacion", "salud", "agua", "vivienda", "transporte",
    "energia", "mineria", "ambiente", "agricultura", "justicia"
]

CLASSIFICATION_PROMPT = """You are classifying Peruvian congressional votes into categories.

CATEGORIES (choose exactly ONE primary category):
- seguridad: Police, crime, terrorism, military, national defense, public safety
- economia: Economic policy, trade, commerce, business regulation, competition
- fiscal: Taxes, budget, public spending, debt, Treasury matters
- social: Social programs, welfare, poverty, inequality, social protection
- empleo: Labor laws, employment, workers rights, unions, pensions
- educacion: Schools, universities, teachers, educational policy
- salud: Healthcare, hospitals, medicines, public health, epidemics (COVID)
- agua: Water supply, sanitation, water resources, irrigation
- vivienda: Housing, urban development, construction
- transporte: Roads, airports, ports, public transit, traffic
- energia: Electricity, oil, gas, renewable energy
- mineria: Mining, extraction industries
- ambiente: Environment, pollution, climate, natural resources, disasters (El Nino)
- agricultura: Farming, rural development, food security
- justicia: Courts, legal system, constitutional matters, Congress procedures, elections, human rights, political investigations, anti-corruption (PROCEDURAL votes about Congress itself go here)

VOTE TYPES:
- sustantivo: Creates/modifies actual laws with real-world impact
- declarativo: Symbolic declarations, recognitions, commemorations
- procedural: Internal Congress procedures, committee formation, reconsiderations

IMPORTANT RULES:
1. Votes about forming congressional commissions/committees → justicia + procedural
2. Votes about investigating corruption → justicia (unless the corruption is sector-specific like ESSALUD → salud)
3. Votes about COVID-19 → salud
4. Votes about elections/electoral fraud → justicia
5. Votes about specific ministries → map to their sector (Educacion ministry → educacion)
6. "Reconsideracion" votes inherit the category of the original vote
7. "Admision a debate" votes inherit the category of the underlying motion

Classify each vote. Return ONLY valid JSON array with no markdown formatting.

INPUT VOTES:
{votes_json}

OUTPUT FORMAT (exactly {count} items):
[
  {{
    "vote_id": "2021-07-26T10-40",
    "category": "justicia",
    "secondary_category": null,
    "vote_type": "procedural",
    "confidence": 0.95,
    "reasoning": "Brief 1-sentence explanation",
    "keywords_detected": ["reglamento", "congreso", "mesa directiva"]
  }}
]
"""


def load_vote_index():
    """Load the vote index."""
    with open(VOTE_INDEX_PATH) as f:
        data = json.load(f)
    return data["votes"]


def call_llm(prompt: str) -> str:
    """Call Claude via CLI."""
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True,
        text=True,
        timeout=120
    )
    if result.returncode != 0:
        raise Exception(f"LLM call failed: {result.stderr}")
    return result.stdout.strip()


def parse_llm_response(response: str, expected_count: int) -> list:
    """Parse and validate LLM response."""
    # Clean up response - remove markdown code blocks if present
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        response = "\n".join(lines[1:-1])

    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    if not isinstance(data, list):
        raise ValueError("Response is not a list")

    if len(data) != expected_count:
        raise ValueError(f"Expected {expected_count} items, got {len(data)}")

    # Validate each item
    validated = []
    for item in data:
        if item.get("category") not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category: {item.get('category')}")
        if item.get("vote_type") not in ["sustantivo", "declarativo", "procedural"]:
            raise ValueError(f"Invalid vote_type: {item.get('vote_type')}")
        if not isinstance(item.get("confidence"), (int, float)):
            raise ValueError("Confidence must be a number")
        if not 0 <= item["confidence"] <= 1:
            raise ValueError(f"Confidence out of range: {item['confidence']}")
        if not item.get("reasoning"):
            raise ValueError("Empty reasoning")

        validated.append({
            "vote_id": item["vote_id"],
            "category": item["category"],
            "secondary_category": item.get("secondary_category"),
            "vote_type": item["vote_type"],
            "confidence": item["confidence"],
            "reasoning": item["reasoning"],
            "keywords_detected": item.get("keywords_detected", [])
        })

    return validated


def classify_batch(votes: list, batch_num: int, max_retries: int = 3) -> list:
    """Classify a batch of votes."""
    batch_input = [{"vote_id": v["vote_id"], "asunto": v["subject"]} for v in votes]
    votes_json = json.dumps(batch_input, ensure_ascii=False, indent=2)

    prompt = CLASSIFICATION_PROMPT.format(
        votes_json=votes_json,
        count=len(votes)
    )

    for attempt in range(max_retries):
        try:
            print(f"  Batch {batch_num}: Attempt {attempt + 1}...")
            response = call_llm(prompt)
            results = parse_llm_response(response, len(votes))

            # Merge with original vote data (match spec field names)
            for i, result in enumerate(results):
                result["date"] = votes[i]["date"]
                result["time"] = votes[i]["time"]
                result["asunto"] = votes[i]["subject"]
                folder = votes[i]["folder_path"]
                result["metadatos_path"] = f"{folder}/metadatos.csv"
                result["votaciones_path"] = f"{folder}/votaciones.csv"

            return results

        except Exception as e:
            print(f"  Batch {batch_num}: Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                # Return fallbacks
                print(f"  Batch {batch_num}: Using fallbacks")
                return [{
                    "vote_id": v["vote_id"],
                    "date": v["date"],
                    "time": v["time"],
                    "asunto": v["subject"],
                    "metadatos_path": f"{v['folder_path']}/metadatos.csv",
                    "votaciones_path": f"{v['folder_path']}/votaciones.csv",
                    "category": "justicia",
                    "secondary_category": None,
                    "vote_type": "procedural",
                    "confidence": 0.3,
                    "reasoning": "FALLBACK: Classification failed after retries",
                    "keywords_detected": [],
                    "is_fallback": True
                } for v in votes]
            time.sleep(2)  # Brief delay before retry


def save_checkpoint(batch_num: int, results: list):
    """Save batch checkpoint."""
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    checkpoint_path = CHECKPOINT_DIR / f"batch_{batch_num:03d}.json"
    with open(checkpoint_path, "w") as f:
        json.dump({
            "batch_num": batch_num,
            "count": len(results),
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, ensure_ascii=False, indent=2)


def load_existing_results() -> list:
    """Load results from existing checkpoints."""
    results = []
    if not CHECKPOINT_DIR.exists():
        return results

    for checkpoint_file in sorted(CHECKPOINT_DIR.glob("batch_*.json")):
        with open(checkpoint_file) as f:
            data = json.load(f)
            results.extend(data["results"])

    return results


def calculate_stats(results: list) -> dict:
    """Calculate classification statistics."""
    stats = {
        "by_category": {},
        "by_vote_type": {},
        "average_confidence": 0,
        "low_confidence_count": 0,
        "fallback_count": 0
    }

    for cat in VALID_CATEGORIES:
        stats["by_category"][cat] = 0
    for vt in ["sustantivo", "declarativo", "procedural"]:
        stats["by_vote_type"][vt] = 0

    total_conf = 0
    for r in results:
        stats["by_category"][r["category"]] = stats["by_category"].get(r["category"], 0) + 1
        stats["by_vote_type"][r["vote_type"]] = stats["by_vote_type"].get(r["vote_type"], 0) + 1
        total_conf += r["confidence"]
        if r["confidence"] < 0.5:
            stats["low_confidence_count"] += 1
        if r.get("is_fallback"):
            stats["fallback_count"] += 1

    stats["average_confidence"] = round(total_conf / len(results), 3) if results else 0

    return stats


def main():
    parser = argparse.ArgumentParser(description="Classify congressional votes")
    parser.add_argument("--batch-start", type=int, default=0, help="Start batch number")
    parser.add_argument("--batch-end", type=int, default=None, help="End batch number (exclusive)")
    parser.add_argument("--all", action="store_true", help="Run all batches")
    parser.add_argument("--sample", action="store_true", help="Run 3 sample batches")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoints")
    args = parser.parse_args()

    # Load votes
    print("Loading vote index...")
    all_votes = load_vote_index()
    total_votes = len(all_votes)
    total_batches = (total_votes + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"Total votes: {total_votes}")
    print(f"Total batches: {total_batches}")

    # Determine batch range
    if args.sample:
        batch_start = 0
        batch_end = 3
    elif args.all:
        batch_start = 0
        batch_end = total_batches
    else:
        batch_start = args.batch_start
        batch_end = args.batch_end or (batch_start + 1)

    print(f"Running batches {batch_start} to {batch_end - 1}")

    # Load existing results if resuming
    all_results = []
    if args.resume:
        all_results = load_existing_results()
        print(f"Loaded {len(all_results)} existing results")
        # Find which batches are already done
        done_vote_ids = {r["vote_id"] for r in all_results}
    else:
        done_vote_ids = set()

    # Process batches
    for batch_num in range(batch_start, batch_end):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, total_votes)
        batch_votes = all_votes[start_idx:end_idx]

        # Skip if already done
        if all(v["vote_id"] in done_vote_ids for v in batch_votes):
            print(f"Batch {batch_num}: Already done, skipping")
            continue

        print(f"\nBatch {batch_num}/{total_batches - 1} (votes {start_idx}-{end_idx - 1})...")

        results = classify_batch(batch_votes, batch_num)
        save_checkpoint(batch_num, results)
        all_results.extend(results)

        print(f"  Classified {len(results)} votes")

        # Brief delay between batches
        if batch_num < batch_end - 1:
            time.sleep(1)

    # Save final output if we have results
    if all_results:
        print(f"\nSaving {len(all_results)} total results...")
        stats = calculate_stats(all_results)

        output = {
            "generated_at": datetime.now().isoformat(),
            "total_votes": len(all_results),
            "classification_stats": stats,
            "votes": all_results
        }

        with open(OUTPUT_PATH, "w") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\nCategory distribution:")
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
            pct = count / len(all_results) * 100
            print(f"  {cat}: {count} ({pct:.1f}%)")

        print(f"\nVote type distribution:")
        for vt, count in stats["by_vote_type"].items():
            pct = count / len(all_results) * 100
            print(f"  {vt}: {count} ({pct:.1f}%)")

        print(f"\nAverage confidence: {stats['average_confidence']}")
        print(f"Low confidence (<0.5): {stats['low_confidence_count']}")
        print(f"Fallbacks: {stats['fallback_count']}")

    print("\nDone!")


if __name__ == "__main__":
    main()
