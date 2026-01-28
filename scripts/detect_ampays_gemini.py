#!/usr/bin/env python3
"""
Phase 1.5: Detect Contradictions (AMPAYs) - Gemini Version
Compares 2021 promises against actual votes to find contradictions.
Uses Gemini CLI instead of Claude CLI.

Usage:
  python detect_ampays_gemini.py --sample            # Test with 10 promises
  python detect_ampays_gemini.py --all               # Run all promises
  python detect_ampays_gemini.py --party peru_libre  # Run for specific party
"""

import sys
sys.stdout.reconfigure(line_buffering=True)

import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import time
import re

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

Return ONLY valid JSON (no markdown, no code blocks, no explanation before or after):
{{
  "rating": "KEPT|BROKEN|PARTIAL|NO_DATA",
  "is_ampay": true|false,
  "confidence": 0.0-1.0,
  "reasoning": "2-3 sentences explaining the analysis",
  "vote_summary": {{
    "aligned": 0,
    "contradictory": 0,
    "neutral_or_unclear": 0
  }},
  "key_votes": []
}}"""


def load_promises():
    """Load 2021 campaign promises."""
    with open(PROMISES_PATH) as f:
        data = json.load(f)

    # Flatten all 2021 promises from all parties
    all_promises = []
    for party_slug, party_data in data.get("parties", {}).items():
        if "2021" in party_data and "promises" in party_data["2021"]:
            for p in party_data["2021"]["promises"]:
                promise = {
                    "promise_id": p.get("id", f"{party_slug}-{len(all_promises)}"),
                    "party": party_slug,
                    "promise_text": p.get("text", ""),
                    "category": p.get("category", "").lower(),
                    "secondary_category": p.get("secondary_category"),
                    "source_quote": p.get("source_quote", "")
                }
                all_promises.append(promise)

    return all_promises


def load_party_positions():
    """Load party position data."""
    with open(PARTY_POSITIONS_PATH) as f:
        data = json.load(f)
    return data.get("votes", [])


def get_relevant_votes(party_positions, party_name, category, limit=20):
    """Get votes for a specific party and category."""
    relevant = []

    for vote in party_positions:
        if vote.get("category") != category:
            continue
        if vote.get("vote_type") != "sustantivo":
            continue

        party_data = vote.get("party_positions", {}).get(party_name, {})
        if party_data.get("position") in ["NO_DATA", "AUSENTE"]:
            continue

        relevant.append({
            "vote_id": vote["vote_id"],
            "date": vote["date"],
            "asunto": vote["asunto"][:200],
            "party_position": party_data.get("position"),
            "si_percentage": party_data.get("si_percentage", 0)
        })

    # Sort by date descending, take most recent
    relevant.sort(key=lambda x: x["date"], reverse=True)
    return relevant[:limit]


def call_gemini(prompt, max_retries=3):
    """Call Gemini CLI to analyze promise vs votes."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["gemini", "-m", "gemini-2.5-pro", prompt],
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout.strip()
            if not output:
                output = result.stderr.strip()

            if not output:
                print(f"    Attempt {attempt + 1} failed: Empty response", flush=True)
                time.sleep(2)
                continue

            # Try to extract JSON from response
            # Remove markdown code blocks if present
            output = re.sub(r'^```json\s*', '', output)
            output = re.sub(r'^```\s*', '', output)
            output = re.sub(r'\s*```$', '', output)

            # Find JSON object in output
            json_match = re.search(r'\{[\s\S]*\}', output)
            if json_match:
                json_str = json_match.group()
                parsed = json.loads(json_str)
                return parsed
            else:
                print(f"    Attempt {attempt + 1} failed: No JSON found in response", flush=True)
                time.sleep(2)
                continue

        except subprocess.TimeoutExpired:
            print(f"    Attempt {attempt + 1} failed: Timeout", flush=True)
            time.sleep(2)
        except json.JSONDecodeError as e:
            print(f"    Attempt {attempt + 1} failed: Invalid JSON: {e}", flush=True)
            time.sleep(2)
        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {e}", flush=True)
            time.sleep(2)

    return None


def evaluate_promise(promise, party_positions, party_name):
    """Evaluate a single promise against voting record."""
    category = promise.get("category", "").lower()
    promise_text = promise.get("promise_text", "")

    # Get relevant votes
    relevant_votes = get_relevant_votes(party_positions, party_name, category)

    if not relevant_votes:
        return {
            "rating": "NO_DATA",
            "is_ampay": False,
            "confidence": 0.0,
            "reasoning": "No substantive votes found in this category for this party.",
            "vote_summary": {"aligned": 0, "contradictory": 0, "neutral_or_unclear": 0},
            "key_votes": []
        }

    # Build prompt
    prompt = DETECTION_PROMPT.format(
        party_name=party_name,
        promise_text=promise_text,
        promise_category=category,
        votes_json=json.dumps(relevant_votes, indent=2, ensure_ascii=False)
    )

    # Call Gemini
    result = call_gemini(prompt)

    if result is None:
        return {
            "rating": "NO_DATA",
            "is_ampay": False,
            "confidence": 0.0,
            "reasoning": "FALLBACK: Evaluation failed after 3 retries.",
            "vote_summary": {"aligned": 0, "contradictory": 0, "neutral_or_unclear": 0},
            "key_votes": []
        }

    return result


def main():
    parser = argparse.ArgumentParser(description="Detect AMPAYs (contradictions)")
    parser.add_argument("--sample", action="store_true", help="Run with 10 sample promises")
    parser.add_argument("--all", action="store_true", help="Run all promises")
    parser.add_argument("--party", type=str, help="Run for specific party (slug)")
    args = parser.parse_args()

    print("Loading data...", flush=True)
    promises = load_promises()
    party_positions = load_party_positions()

    print(f"2021 promises: {len(promises)}", flush=True)
    print(f"Substantive votes: {len([v for v in party_positions if v.get('vote_type') == 'sustantivo'])}", flush=True)

    # Filter promises if party specified
    if args.party:
        party_full = PARTY_SLUG_TO_FULL.get(args.party)
        if not party_full:
            print(f"Unknown party: {args.party}")
            print(f"Available: {list(PARTY_SLUG_TO_FULL.keys())}")
            return
        promises = [p for p in promises if p.get("party") == args.party]
        print(f"Filtered to {len(promises)} promises for {args.party}", flush=True)

    # Sample mode
    if args.sample:
        promises = promises[:10]
        print(f"Sample mode: {len(promises)} promises", flush=True)

    if not args.sample and not args.all and not args.party:
        print("Specify --sample, --all, or --party <slug>")
        return

    # Evaluate promises
    print(f"\nEvaluating {len(promises)} promises...", flush=True)

    evaluations = []
    ampays = []

    for i, promise in enumerate(promises):
        promise_id = promise.get("promise_id", f"P-{i}")
        party_slug = promise.get("party", "unknown")
        party_name = PARTY_SLUG_TO_FULL.get(party_slug, party_slug)

        print(f"\n[{i+1}/{len(promises)}] {promise_id}: {promise.get('promise_text', '')[:60]}...", flush=True)

        result = evaluate_promise(promise, party_positions, party_name)

        evaluation = {
            "promise_id": promise_id,
            "party": party_slug,
            "party_name": party_name,
            "promise_text": promise.get("promise_text"),
            "category": promise.get("category"),
            "evaluation": result,
            "evaluated_at": datetime.now().isoformat()
        }
        evaluations.append(evaluation)

        print(f"  Rating: {result.get('rating')} (confidence: {result.get('confidence', 0):.2f})", flush=True)
        print(f"  Reasoning: {result.get('reasoning', '')[:80]}...", flush=True)

        if result.get("is_ampay"):
            ampays.append(evaluation)
            print(f"  *** AMPAY DETECTED ***", flush=True)

        # Rate limiting
        time.sleep(1)

    # Save results
    print(f"\n\nSaving results...", flush=True)

    with open(EVALUATIONS_PATH, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_evaluated": len(evaluations),
            "evaluations": evaluations
        }, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_PATH, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_ampays": len(ampays),
            "ampays": ampays
        }, f, ensure_ascii=False, indent=2)

    # Summary
    print(f"\n=== SUMMARY ===", flush=True)
    print(f"Total evaluated: {len(evaluations)}", flush=True)
    print(f"AMPAYs detected: {len(ampays)}", flush=True)

    ratings = {}
    for e in evaluations:
        r = e["evaluation"].get("rating", "UNKNOWN")
        ratings[r] = ratings.get(r, 0) + 1

    print(f"\nRating distribution:", flush=True)
    for r, count in sorted(ratings.items()):
        print(f"  {r}: {count}", flush=True)

    print(f"\nSaved to:", flush=True)
    print(f"  {EVALUATIONS_PATH}", flush=True)
    print(f"  {OUTPUT_PATH}", flush=True)
    print("Done!", flush=True)


if __name__ == "__main__":
    main()
