#!/usr/bin/env python3
"""
aggregate_votes.py

Transforms party_positions.json into votes_by_party.json for the frontend.
Used by: Parliament Semicircle graphic (Por Tema - Vote Detail)

Input:  data/01_input/votes/party_positions.json (9MB)
Output: data/02_output/votes_by_party.json
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_FILE = PROJECT_ROOT / "data/01_input/votes/party_positions.json"
OUTPUT_FILE = PROJECT_ROOT / "data/02_output/votes_by_party.json"

# Party slug mapping (display name -> slug for frontend)
PARTY_SLUG_MAP = {
    "Fuerza Popular": "fuerza_popular",
    "Peru Libre": "peru_libre",
    "Renovacion Popular": "renovacion_popular",
    "Avanza Pais": "avanza_pais",
    "APAIS": "avanza_pais",  # Alternative name
    "AP-PIS": "avanza_pais",  # Code
    "Alianza para el Progreso": "alianza_progreso",
    "Somos Peru": "somos_peru",
    "Podemos Peru": "podemos_peru",
    "Juntos por el Peru": "juntos_peru",
    "Partido Morado": "partido_morado",
    "SP-PM": "partido_morado",  # Code
}

# Parties we care about (the 9 with 2026 candidates)
TARGET_PARTIES = [
    "fuerza_popular",
    "peru_libre",
    "renovacion_popular",
    "avanza_pais",
    "alianza_progreso",
    "somos_peru",
    "podemos_peru",
    "juntos_peru",
    "partido_morado",
]


def normalize_party_name(name: str) -> str | None:
    """Convert party display name to slug, return None if not in our 9 parties."""
    slug = PARTY_SLUG_MAP.get(name)
    if slug and slug in TARGET_PARTIES:
        return slug
    return None


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
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Processing {len(data['votes'])} votes...")

    output = {
        "generated_at": datetime.now().isoformat(),
        "total_votes": len(data["votes"]),
        "parties": TARGET_PARTIES,
        "votes": {}
    }

    for vote in data["votes"]:
        processed = process_vote(vote)
        output["votes"][vote["vote_id"]] = processed

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Stats
    file_size = OUTPUT_FILE.stat().st_size / 1024 / 1024
    print(f"Done! Output: {file_size:.2f} MB")
    print(f"Votes processed: {len(output['votes'])}")


if __name__ == "__main__":
    main()
