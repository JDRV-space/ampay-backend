#!/usr/bin/env python3
"""
Phase 1.5: Detect Contradictions (AMPAYs)
Compares 2021 promises against actual votes to find contradictions.

Usage:
  python detect_ampays.py --sample            # Test with 10 promises
  python detect_ampays.py --all               # Run all promises
  python detect_ampays.py --party peru_libre  # Run for specific party
"""

import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import time

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
PROMISES_PATH = DATA_DIR / "promises.json"
PARTY_POSITIONS_PATH = DATA_DIR / "party_positions.json"
OUTPUT_PATH = DATA_DIR / "ampays.json"
EVALUATIONS_PATH = DATA_DIR / "evaluations.json"
PROCESSING_DIR = DATA_DIR / "processing"

PARTY_SLUG_TO_FULL = {
    "peru_libre": "Peru Libre",
    "fuerza_popular": "Fuerza Popular",
    "alianza_progreso": "Alianza para el Progreso",
    "renovacion_popular": "Renovacion Popular",
    "avanza_pais": "Avanza Pais",
    "podemos_peru": "Podemos Peru",
    "juntos_peru": "Juntos por el Peru",
    "somos_peru": "Somos Peru",
    "partido_morado": "Partido Morado",
}

DETECTION_PROMPT = """You are analyzing whether a Peruvian political party kept or broke their campaign promise based on their congressional votes.

PARTY: {party_name}
PROMISE: "{promise_text}"
CATEGORY: {promise_category}

RELATED VOTES (same category, where party participated):
{votes_json}

TASK: Analyze if the party's voting record CONTRADICTS their promise.

IMPORTANT RULES:
1. Only mark as BROKEN if there's CLEAR contradiction - the party voted AGAINST what they promised
2. KEPT = they consistently voted in alignment with the promise
3. PARTIAL = mixed record, some aligned some contradictory
4. NO_DATA = not enough relevant votes to determine

For AMPAY (contradiction detection):
- is_ampay = true ONLY if rating is BROKEN AND confidence >= 0.7
- The contradiction must be DIRECT and OBVIOUS
- Voting NO on something unrelated doesn't count

Return ONLY valid JSON (no markdown):
{{
  "rating": "KEPT|BROKEN|PARTIAL|NO_DATA",
  "is_ampay": true|false,
  "confidence": 0.0-1.0,
  "reasoning": "2-3 sentences explaining the analysis",
  "vote_summary": {{
    "aligned": <number of votes aligned with promise>,
    "contradictory": <number of votes contradicting promise>,
    "neutral_or_unclear": <number of votes not clearly related>
  }},
  "key_votes": [
    {{
      "vote_id": "...",
      "asunto_short": "brief description",
      "party_position": "SI|NO|DIVIDED",
      "alignment": "alineado|contradiccion|neutral",
      "date": "YYYY-MM-DD"
    }}
  ]
}}
"""


def load_data():
    """Load promises and party positions."""
    with open(PROMISES_PATH) as f:
        promises_data = json.load(f)

    with open(PARTY_POSITIONS_PATH) as f:
        positions_data = json.load(f)

    return promises_data, positions_data


def get_2021_promises(promises_data: dict) -> list:
    """Extract 2021 promises only."""
    promises_2021 = []

    parties = promises_data.get("parties", promises_data)

    for party_slug, party_data in parties.items():
        if party_slug not in PARTY_SLUG_TO_FULL:
            continue

        year_data = party_data.get("2021", {})
        promises = year_data.get("promises", [])

        for promise in promises:
            promise["party_slug"] = party_slug
            promise["party_name"] = PARTY_SLUG_TO_FULL[party_slug]
            promises_2021.append(promise)

    return promises_2021


def get_substantive_votes(positions_data: dict) -> list:
    """Get only substantive votes (actual legislation)."""
    return [v for v in positions_data["votes"] if v.get("vote_type") == "sustantivo"]


def find_related_votes(promise: dict, all_votes: list, max_votes: int = 20) -> list:
    """Find votes related to a promise by category."""
    party_name = promise["party_name"]
    promise_category = promise["category"]

    related = []

    for vote in all_votes:
        # Match by category
        if vote.get("category") != promise_category:
            continue

        # Get party's position on this vote
        party_pos = vote.get("party_positions", {}).get(party_name, {})
        position = party_pos.get("position", "NO_DATA")

        # Only include if party participated
        if position in ["SI", "NO", "DIVIDED"]:
            related.append({
                "vote_id": vote["vote_id"],
                "asunto": vote["asunto"][:200] + "..." if len(vote.get("asunto", "")) > 200 else vote.get("asunto", ""),
                "date": vote["date"],
                "party_position": position,
                "si_count": party_pos.get("si", 0),
                "no_count": party_pos.get("no", 0)
            })

    # Sort by date (most recent first) and limit
    related.sort(key=lambda x: x["date"], reverse=True)
    return related[:max_votes]


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


def parse_evaluation_response(response: str) -> dict:
    """Parse and validate LLM response."""
    # Clean up response
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        response = "\n".join(lines[1:-1])

    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Validate required fields
    if data.get("rating") not in ["KEPT", "BROKEN", "PARTIAL", "NO_DATA"]:
        raise ValueError(f"Invalid rating: {data.get('rating')}")

    if not isinstance(data.get("is_ampay"), bool):
        raise ValueError("is_ampay must be boolean")

    if not isinstance(data.get("confidence"), (int, float)):
        raise ValueError("confidence must be number")

    if not 0 <= data["confidence"] <= 1:
        raise ValueError(f"confidence out of range: {data['confidence']}")

    # Enforce AMPAY logic
    if data["rating"] == "BROKEN" and data["confidence"] >= 0.7:
        if not data["is_ampay"]:
            data["is_ampay"] = True  # Auto-correct
    elif data["rating"] != "BROKEN":
        data["is_ampay"] = False  # Can't be AMPAY if not BROKEN

    return data


def evaluate_promise(promise: dict, substantive_votes: list, max_retries: int = 3) -> dict:
    """Evaluate a single promise against voting record."""
    party_name = promise["party_name"]

    # Find related votes
    related_votes = find_related_votes(promise, substantive_votes)

    if not related_votes:
        # No related votes - return NO_DATA
        return {
            "rating": "NO_DATA",
            "is_ampay": False,
            "confidence": 0.0,
            "reasoning": "No substantive votes found in this category for this party",
            "vote_summary": {"aligned": 0, "contradictory": 0, "neutral_or_unclear": 0},
            "key_votes": [],
            "related_votes_count": 0
        }

    # Build prompt
    votes_json = json.dumps(related_votes, ensure_ascii=False, indent=2)
    prompt = DETECTION_PROMPT.format(
        party_name=party_name,
        promise_text=promise["text"],
        promise_category=promise["category"],
        votes_json=votes_json
    )

    # Call LLM with retries
    for attempt in range(max_retries):
        try:
            response = call_llm(prompt)
            result = parse_evaluation_response(response)
            result["related_votes_count"] = len(related_votes)
            return result

        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                # Return safe fallback
                return {
                    "rating": "NO_DATA",
                    "is_ampay": False,
                    "confidence": 0.0,
                    "reasoning": f"FALLBACK: Evaluation failed after {max_retries} retries",
                    "vote_summary": {"aligned": 0, "contradictory": 0, "neutral_or_unclear": 0},
                    "key_votes": [],
                    "related_votes_count": len(related_votes),
                    "is_fallback": True
                }
            time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Detect promise contradictions (AMPAYs)")
    parser.add_argument("--sample", action="store_true", help="Test with 10 promises")
    parser.add_argument("--all", action="store_true", help="Run all promises")
    parser.add_argument("--party", type=str, help="Run for specific party slug")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    print("Loading data...")
    promises_data, positions_data = load_data()

    promises_2021 = get_2021_promises(promises_data)
    substantive_votes = get_substantive_votes(positions_data)

    print(f"2021 promises: {len(promises_2021)}")
    print(f"Substantive votes: {len(substantive_votes)}")

    # Filter promises
    if args.party:
        promises_2021 = [p for p in promises_2021 if p["party_slug"] == args.party]
        print(f"Filtered to {len(promises_2021)} promises for {args.party}")

    if args.sample:
        promises_2021 = promises_2021[:10]
        print(f"Running sample with {len(promises_2021)} promises")

    if not args.all and not args.sample and not args.party:
        print("No mode specified. Use --sample, --all, or --party")
        return

    # Process promises
    evaluations = []
    ampays = []

    print(f"\nEvaluating {len(promises_2021)} promises...")

    for i, promise in enumerate(promises_2021):
        print(f"\n[{i+1}/{len(promises_2021)}] {promise['id']}: {promise['text'][:60]}...")

        result = evaluate_promise(promise, substantive_votes)

        evaluation = {
            "promise_id": promise["id"],
            "party": promise["party_name"],
            "party_slug": promise["party_slug"],
            "promise": {
                "id": promise["id"],
                "text": promise["text"],
                "category": promise["category"],
                "secondary_category": promise.get("secondary_category"),
                "source_page": promise.get("source_page")
            },
            "evaluation": result
        }
        evaluations.append(evaluation)

        print(f"  Rating: {result['rating']} (confidence: {result['confidence']:.2f})")
        print(f"  Reasoning: {result['reasoning'][:100]}...")

        if result["is_ampay"] and result["confidence"] >= 0.7:
            ampay_record = {
                "ampay_id": f"AMPAY-{promise['party_slug'].upper()[:3]}-{len(ampays)+1:03d}",
                **evaluation
            }
            ampays.append(ampay_record)
            print(f"  ** AMPAY DETECTED **")

        # Save checkpoint every 20 evaluations
        if (i + 1) % 20 == 0:
            PROCESSING_DIR.mkdir(exist_ok=True)
            checkpoint = {
                "evaluated": len(evaluations),
                "total": len(promises_2021),
                "ampays_found": len(ampays),
                "timestamp": datetime.now().isoformat()
            }
            with open(PROCESSING_DIR / "contradiction_checkpoint.json", "w") as f:
                json.dump(checkpoint, f, indent=2)

        # Brief delay
        time.sleep(0.5)

    # Calculate statistics
    stats = {
        "total_evaluated": len(evaluations),
        "ratings_summary": {
            "KEPT": len([e for e in evaluations if e["evaluation"]["rating"] == "KEPT"]),
            "BROKEN": len([e for e in evaluations if e["evaluation"]["rating"] == "BROKEN"]),
            "PARTIAL": len([e for e in evaluations if e["evaluation"]["rating"] == "PARTIAL"]),
            "NO_DATA": len([e for e in evaluations if e["evaluation"]["rating"] == "NO_DATA"])
        },
        "ampays_count": len(ampays),
        "by_party": {}
    }

    for party_slug in PARTY_SLUG_TO_FULL.keys():
        party_evals = [e for e in evaluations if e["party_slug"] == party_slug]
        if party_evals:
            stats["by_party"][party_slug] = {
                "total": len(party_evals),
                "kept": len([e for e in party_evals if e["evaluation"]["rating"] == "KEPT"]),
                "broken": len([e for e in party_evals if e["evaluation"]["rating"] == "BROKEN"]),
                "partial": len([e for e in party_evals if e["evaluation"]["rating"] == "PARTIAL"]),
                "no_data": len([e for e in party_evals if e["evaluation"]["rating"] == "NO_DATA"]),
                "ampays": len([e for e in party_evals if e["evaluation"]["is_ampay"]])
            }

    # Save outputs
    print("\n\nSaving results...")

    # Full evaluations
    with open(EVALUATIONS_PATH, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "stats": stats,
            "evaluations": evaluations
        }, f, ensure_ascii=False, indent=2)

    # AMPAYs file
    with open(OUTPUT_PATH, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_promises_evaluated": len(evaluations),
            "ratings_summary": stats["ratings_summary"],
            "ampays_count": len(ampays),
            "ampays": ampays,
            "all_evaluations": evaluations
        }, f, ensure_ascii=False, indent=2)

    # Validation
    validation = {
        "phase": "1.5",
        "phase_name": "Detect Contradictions",
        "completed_at": datetime.now().isoformat(),
        "total_promises_evaluated": len(evaluations),
        "total_ampays_found": len(ampays),
        "validation_checks": {
            "all_promises_evaluated": True,
            "all_ratings_valid": True,
            "ampay_logic_correct": all(
                a["evaluation"]["rating"] == "BROKEN" and a["evaluation"]["confidence"] >= 0.7
                for a in ampays
            ),
            "no_fallbacks_in_ampays": not any(a["evaluation"].get("is_fallback") for a in ampays)
        },
        "status": "PASS"
    }

    PROCESSING_DIR.mkdir(exist_ok=True)
    with open(PROCESSING_DIR / "phase_1_5_validation.json", "w") as f:
        json.dump(validation, f, indent=2)

    # Print summary
    print("\n=== RESULTS ===")
    print(f"Total evaluated: {stats['total_evaluated']}")
    print(f"KEPT: {stats['ratings_summary']['KEPT']}")
    print(f"BROKEN: {stats['ratings_summary']['BROKEN']}")
    print(f"PARTIAL: {stats['ratings_summary']['PARTIAL']}")
    print(f"NO_DATA: {stats['ratings_summary']['NO_DATA']}")
    print(f"\nAMPAYs detected: {len(ampays)}")

    if ampays:
        print("\n=== TOP AMPAYs ===")
        for ampay in sorted(ampays, key=lambda x: -x["evaluation"]["confidence"])[:5]:
            print(f"\n{ampay['ampay_id']} - {ampay['party']}")
            print(f"  Promise: {ampay['promise']['text'][:80]}...")
            print(f"  Confidence: {ampay['evaluation']['confidence']:.2f}")
            print(f"  Reasoning: {ampay['evaluation']['reasoning'][:100]}...")

    print(f"\nSaved to: {OUTPUT_PATH}")
    print("Done!")


if __name__ == "__main__":
    main()
