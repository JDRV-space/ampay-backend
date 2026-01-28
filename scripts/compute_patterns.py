#!/usr/bin/env python3
"""
compute_patterns.py

Computes party voting patterns by category and month for sparkline graphics.
Used by: Sparklines graphic (Partidos - Party Profile)

Input:  data/01_input/votes/party_positions.json (9MB)
Output: data/02_output/party_patterns.json
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_FILE = PROJECT_ROOT / "data/01_input/votes/party_positions.json"
OUTPUT_FILE = PROJECT_ROOT / "data/02_output/party_patterns.json"

# Party slug mapping
PARTY_SLUG_MAP = {
    "Fuerza Popular": "fuerza_popular",
    "Peru Libre": "peru_libre",
    "Renovacion Popular": "renovacion_popular",
    "Avanza Pais": "avanza_pais",
    "APAIS": "avanza_pais",
    "AP-PIS": "avanza_pais",
    "Alianza para el Progreso": "alianza_progreso",
    "Somos Peru": "somos_peru",
    "Podemos Peru": "podemos_peru",
    "Juntos por el Peru": "juntos_peru",
    "Partido Morado": "partido_morado",
    "SP-PM": "partido_morado",
}

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

# Categories we care about (exclude justicia - mostly procedural)
TARGET_CATEGORIES = [
    "salud",
    "economia",
    "seguridad",
    "educacion",
    "empleo",
    "agricultura",
    "transporte",
    "ambiente",
    "fiscal",
    "agua",
    "energia",
    "vivienda",
    "mineria",
]


def normalize_party_name(name: str) -> str | None:
    slug = PARTY_SLUG_MAP.get(name)
    if slug and slug in TARGET_PARTIES:
        return slug
    return None


def main():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Processing {len(data['votes'])} votes...")

    # Data structures for aggregation
    # by_category[party][category] = {"si": count, "total": count}
    by_category = defaultdict(lambda: defaultdict(lambda: {"si": 0, "total": 0}))

    # by_month[party][YYYY-MM] = {"si": count, "total": count}
    by_month = defaultdict(lambda: defaultdict(lambda: {"si": 0, "total": 0}))

    # Process each vote
    for vote in data["votes"]:
        category = vote.get("category", "").lower()
        vote_type = vote.get("vote_type", "")
        date = vote.get("date", "")

        # Skip procedural votes and justicia (noisy)
        if vote_type == "procedural":
            continue
        if category == "justicia":
            continue
        if category not in TARGET_CATEGORIES:
            continue

        # Extract month
        month = date[:7] if len(date) >= 7 else None

        # Process party positions
        for party_name, party_data in vote.get("party_positions", {}).items():
            slug = normalize_party_name(party_name)
            if not slug:
                continue

            total_present = party_data.get("total_present", 0)
            si_count = party_data.get("si", 0)

            if total_present > 0:
                # By category
                by_category[slug][category]["si"] += si_count
                by_category[slug][category]["total"] += total_present

                # By month
                if month:
                    by_month[slug][month]["si"] += si_count
                    by_month[slug][month]["total"] += total_present

    # Build output
    output = {
        "generated_at": datetime.now().isoformat(),
        "categories": TARGET_CATEGORIES,
        "parties": {}
    }

    for party in TARGET_PARTIES:
        party_data = {
            "by_category": {},
            "by_month": {},
            "category_averages": {}
        }

        # Category percentages
        for cat in TARGET_CATEGORIES:
            cat_data = by_category[party][cat]
            if cat_data["total"] > 0:
                pct = round(cat_data["si"] / cat_data["total"] * 100, 1)
            else:
                pct = None
            party_data["by_category"][cat] = {
                "si": cat_data["si"],
                "total": cat_data["total"],
                "pct": pct
            }
            party_data["category_averages"][cat] = pct

        # Monthly percentages (sorted)
        months_sorted = sorted(by_month[party].keys())
        for month in months_sorted:
            month_data = by_month[party][month]
            if month_data["total"] > 0:
                pct = round(month_data["si"] / month_data["total"] * 100, 1)
            else:
                pct = None
            party_data["by_month"][month] = {
                "si": month_data["si"],
                "total": month_data["total"],
                "pct": pct
            }

        # Sparkline data (list of monthly percentages for easy charting)
        party_data["sparkline"] = [
            party_data["by_month"].get(m, {}).get("pct", 0) or 0
            for m in months_sorted
        ]
        party_data["sparkline_months"] = months_sorted

        output["parties"][party] = party_data

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"Writing {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Stats
    file_size = OUTPUT_FILE.stat().st_size / 1024
    print(f"Done! Output: {file_size:.1f} KB")

    # Sample output
    print("\nSample - Fuerza Popular by category:")
    for cat, data in list(output["parties"]["fuerza_popular"]["category_averages"].items())[:5]:
        print(f"  {cat}: {data}%")


if __name__ == "__main__":
    main()
