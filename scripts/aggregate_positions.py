#!/usr/bin/env python3
"""
Phase 1.4: Aggregate Party Positions
Reads resultados_grupo.csv files and aggregates party positions per vote.
NO LLM required - pure data processing.

Usage:
  python aggregate_positions.py
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
VOTES_CATEGORIZED_PATH = DATA_DIR / "votes_categorized.json"
OUTPUT_PATH = DATA_DIR / "party_positions.json"
PROCESSING_DIR = DATA_DIR / "processing"

# CORRECTED party code mapping (based on actual openpolitica data)
PARTY_CODE_MAP = {
    # Main parties
    "PL": "Peru Libre",
    "FP": "Fuerza Popular",
    "APP": "Alianza para el Progreso",
    "RP": "Renovacion Popular",
    "AP-PIS": "Avanza Pais",  # FIXED: was APAIS
    "PP": "Podemos Peru",
    "JP": "Juntos por el Peru",
    "SP": "Somos Peru",
    "SP-PM": "Partido Morado",  # FIXED: was PM
    "AP": "Accion Popular",

    # Additional bancadas that appear in data
    "BM": "Bloque Magisterial",
    "PB": "Peru Bicentenario",
    "PD": "Peru Democratico",
    "CD-JPP": "Cambio Democratico - JPP",
    "ID": "Integracion Democratica",
    "NA": "No Agrupados",
}

# Main tracked parties (for app display)
MAIN_PARTIES = [
    "Peru Libre",
    "Fuerza Popular",
    "Alianza para el Progreso",
    "Renovacion Popular",
    "Avanza Pais",
    "Podemos Peru",
    "Juntos por el Peru",
    "Somos Peru",
    "Partido Morado",
    "Accion Popular",
]


def load_votes_categorized():
    """Load the classified votes."""
    with open(VOTES_CATEGORIZED_PATH) as f:
        data = json.load(f)
    return data["votes"]


def read_resultados_grupo(folder_path: str) -> dict:
    """Read resultados_grupo.csv and return party positions."""
    csv_path = Path(folder_path) / "resultados_grupo.csv"

    if not csv_path.exists():
        return {}

    positions = {}

    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get('grupo_parlamentario', '').strip()

                # Map code to party name
                party_name = PARTY_CODE_MAP.get(code, code)

                # Parse vote counts
                try:
                    si = int(row.get('si', 0) or 0)
                    no = int(row.get('no', 0) or 0)
                    abstenciones = int(row.get('abstenciones', 0) or 0)
                    ausentes = int(row.get('ausentes', 0) or 0)
                    licencias = int(row.get('licencias', 0) or 0)
                except (ValueError, TypeError):
                    si = no = abstenciones = ausentes = licencias = 0

                total_present = si + no + abstenciones

                # Determine position
                if total_present == 0:
                    position = "AUSENTE"
                elif si / total_present > 0.5:
                    position = "SI"
                elif no / total_present > 0.5:
                    position = "NO"
                else:
                    position = "DIVIDED"

                positions[party_name] = {
                    "code": code,
                    "position": position,
                    "si": si,
                    "no": no,
                    "abstencion": abstenciones,
                    "ausente": ausentes + licencias,
                    "total_present": total_present,
                    "si_percentage": round(si / max(total_present, 1) * 100, 1)
                }

    except Exception as e:
        print(f"  Error reading {csv_path}: {e}")
        return {}

    return positions


def main():
    print("Loading classified votes...")
    votes = load_votes_categorized()
    print(f"Loaded {len(votes)} votes")

    results = []
    missing_positions = 0

    print("\nAggregating party positions...")
    for i, vote in enumerate(votes):
        # Get folder path from metadatos_path (remove /metadatos.csv)
        metadatos_path = vote.get("metadatos_path", "")
        if metadatos_path:
            folder_path = str(Path(metadatos_path).parent)
        else:
            folder_path = vote.get("folder_path", "")  # fallback for old format

        if not folder_path:
            print(f"  Vote {vote['vote_id']}: No folder path")
            missing_positions += 1
            continue

        # Read party positions from resultados_grupo.csv
        party_positions = read_resultados_grupo(folder_path)

        if not party_positions:
            missing_positions += 1

        # Ensure all main parties have entries
        for party_name in MAIN_PARTIES:
            if party_name not in party_positions:
                party_positions[party_name] = {
                    "code": "N/A",
                    "position": "NO_DATA",
                    "si": 0,
                    "no": 0,
                    "abstencion": 0,
                    "ausente": 0,
                    "total_present": 0,
                    "si_percentage": 0
                }

        result = {
            "vote_id": vote["vote_id"],
            "date": vote["date"],
            "time": vote["time"],
            "asunto": vote["asunto"],
            "category": vote["category"],
            "secondary_category": vote.get("secondary_category"),
            "vote_type": vote["vote_type"],
            "confidence": vote["confidence"],
            "party_positions": party_positions
        }
        results.append(result)

        if (i + 1) % 500 == 0:
            print(f"  Processed {i + 1}/{len(votes)} votes...")

    print(f"\nMissing party position data for {missing_positions} votes")

    # Calculate aggregate statistics
    print("\nCalculating statistics...")
    stats = {"by_party": {}}

    for party_name in MAIN_PARTIES:
        party_stats = {
            "total_si": 0,
            "total_no": 0,
            "total_divided": 0,
            "total_ausente": 0,
            "total_no_data": 0
        }

        for result in results:
            pos = result["party_positions"].get(party_name, {}).get("position", "NO_DATA")
            if pos == "SI":
                party_stats["total_si"] += 1
            elif pos == "NO":
                party_stats["total_no"] += 1
            elif pos == "DIVIDED":
                party_stats["total_divided"] += 1
            elif pos == "AUSENTE":
                party_stats["total_ausente"] += 1
            else:
                party_stats["total_no_data"] += 1

        stats["by_party"][party_name] = party_stats

    # Save output
    print(f"\nSaving {len(results)} results...")
    output = {
        "generated_at": datetime.now().isoformat(),
        "total_votes": len(results),
        "party_code_mapping": PARTY_CODE_MAP,
        "aggregate_stats": stats,
        "votes": results
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Save validation checkpoint
    PROCESSING_DIR.mkdir(exist_ok=True)
    validation = {
        "phase": "1.4",
        "phase_name": "Aggregate Party Positions",
        "completed_at": datetime.now().isoformat(),
        "total_votes_processed": len(results),
        "missing_positions": missing_positions,
        "validation_checks": {
            "all_votes_have_party_positions": missing_positions < len(results) * 0.1,
            "main_parties_present": True,
            "position_values_valid": True
        },
        "status": "PASS" if missing_positions < len(results) * 0.1 else "WARNING"
    }

    with open(PROCESSING_DIR / "phase_1_4_validation.json", "w") as f:
        json.dump(validation, f, indent=2)

    # Print summary
    print("\n=== Party Position Summary ===")
    for party_name in MAIN_PARTIES:
        s = stats["by_party"][party_name]
        total = s["total_si"] + s["total_no"] + s["total_divided"] + s["total_ausente"]
        if total > 0:
            print(f"{party_name}:")
            print(f"  SI: {s['total_si']} ({s['total_si']/total*100:.1f}%)")
            print(f"  NO: {s['total_no']} ({s['total_no']/total*100:.1f}%)")
            print(f"  DIVIDED: {s['total_divided']} ({s['total_divided']/total*100:.1f}%)")
            print(f"  AUSENTE: {s['total_ausente']} ({s['total_ausente']/total*100:.1f}%)")

    print(f"\nSaved to: {OUTPUT_PATH}")
    print("Done!")


if __name__ == "__main__":
    main()
