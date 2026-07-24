#!/usr/bin/env python3
"""
aggregate_votes.py

Transforms party_positions.json into votes_by_party.json for the frontend.
Used by: Parliament Semicircle graphic (Por Tema - Vote Detail)

Input:  data/01_input/votes/party_positions.json (9MB)
Output: data/02_output/votes_by_party.json
"""

import json
from datetime import datetime

from ampay_pipeline.parties import TARGET_PARTY_SLUGS, normalize_party_name
from ampay_pipeline.paths import (
    INPUT_PARTY_POSITIONS,
    OUTPUT_VOTES_BY_PARTY,
    ensure_parent_dir,
)


def process_vote(vote: dict) -> dict:
    """Extract party positions from a single vote."""
    result = {
        "vote_id": vote["vote_id"],
        "date": vote["date"],
        "category": vote["category"],
        "vote_type": vote["vote_type"],
        "asunto": vote["asunto"][:200],  # Truncate for size
        "parties": {}
    }

    for party_name, data in vote.get("party_positions", {}).items():
        slug = normalize_party_name(party_name)
        if slug:
            result["parties"][slug] = {
                "position": data["position"],  # SI, NO, DIVIDED, AUSENTE
                "si": data["si"],
                "no": data["no"],
                "abstencion": data["abstencion"],
                "ausente": data["ausente"],
                "total": data["total_present"],
                "si_pct": round(data["si_percentage"], 1)
            }

    return result


def main():
    print(f"Reading {INPUT_PARTY_POSITIONS}...")
    with open(INPUT_PARTY_POSITIONS, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Processing {len(data['votes'])} votes...")

    output = {
        "generated_at": datetime.now().isoformat(),
        "total_votes": len(data["votes"]),
        "parties": TARGET_PARTY_SLUGS,
        "votes": {}
    }

    for vote in data["votes"]:
        processed = process_vote(vote)
        output["votes"][vote["vote_id"]] = processed

    ensure_parent_dir(OUTPUT_VOTES_BY_PARTY)

    print(f"Writing {OUTPUT_VOTES_BY_PARTY}...")
    with open(OUTPUT_VOTES_BY_PARTY, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Stats
    file_size = OUTPUT_VOTES_BY_PARTY.stat().st_size / 1024 / 1024
    print(f"Done! Output: {file_size:.2f} MB")
    print(f"Votes processed: {len(output['votes'])}")


if __name__ == "__main__":
    main()
