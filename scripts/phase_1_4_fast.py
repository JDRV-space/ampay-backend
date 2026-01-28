#!/usr/bin/env python3
"""Phase 1.4 Fast - Aggregate Party Positions"""
import sys
sys.stdout.reconfigure(line_buffering=True)

import json
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
VOTES_CATEGORIZED_PATH = DATA_DIR / "votes_categorized.json"
OUTPUT_PATH = DATA_DIR / "party_positions.json"

PARTY_CODE_MAP = {
    "PL": "Peru Libre", "FP": "Fuerza Popular", "APP": "Alianza para el Progreso",
    "RP": "Renovacion Popular", "AP-PIS": "Avanza Pais", "PP": "Podemos Peru",
    "JP": "Juntos por el Peru", "SP": "Somos Peru", "SP-PM": "Partido Morado",
    "AP": "Accion Popular", "BM": "Bloque Magisterial", "PB": "Peru Bicentenario",
    "PD": "Peru Democratico", "CD-JPP": "Cambio Democratico - JPP",
    "ID": "Integracion Democratica", "NA": "No Agrupados", "CD": "Cambio Democratico"
}

MAIN_PARTIES = ["Peru Libre", "Fuerza Popular", "Alianza para el Progreso",
    "Renovacion Popular", "Avanza Pais", "Podemos Peru", "Juntos por el Peru",
    "Somos Peru", "Partido Morado", "Accion Popular"]

def read_csv(folder_path):
    csv_path = Path(folder_path) / "resultados_grupo.csv"
    if not csv_path.exists():
        return {}
    positions = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row.get("grupo_parlamentario", "").strip()
            party_name = PARTY_CODE_MAP.get(code, code)
            si = int(row.get("si", 0) or 0)
            no = int(row.get("no", 0) or 0)
            ab = int(row.get("abstenciones", 0) or 0)
            aus = int(row.get("ausentes", 0) or 0)
            lic = int(row.get("licencias", 0) or 0)
            tp = si + no + ab
            if tp == 0:
                pos = "AUSENTE"
            elif si / tp > 0.5:
                pos = "SI"
            elif no / tp > 0.5:
                pos = "NO"
            else:
                pos = "DIVIDED"
            positions[party_name] = {
                "code": code, "position": pos, "si": si, "no": no,
                "abstencion": ab, "ausente": aus + lic, "total_present": tp,
                "si_percentage": round(si / max(tp, 1) * 100, 1)
            }
    return positions

def main():
    print("Loading...")
    with open(VOTES_CATEGORIZED_PATH) as f:
        data = json.load(f)
    votes = data["votes"]
    print(f"Processing {len(votes)} votes...")

    results = []
    missing = 0
    for i, vote in enumerate(votes):
        mp = vote.get("metadatos_path", "")
        fp = str(Path(mp).parent) if mp else ""
        if not fp:
            missing += 1
            continue
        pp = read_csv(fp)
        if not pp:
            missing += 1
        for pn in MAIN_PARTIES:
            if pn not in pp:
                pp[pn] = {"code": "N/A", "position": "NO_DATA", "si": 0, "no": 0,
                          "abstencion": 0, "ausente": 0, "total_present": 0, "si_percentage": 0}
        results.append({
            "vote_id": vote["vote_id"], "date": vote["date"], "time": vote["time"],
            "asunto": vote["asunto"], "category": vote["category"],
            "secondary_category": vote.get("secondary_category"),
            "vote_type": vote["vote_type"], "confidence": vote["confidence"],
            "party_positions": pp
        })
        if (i + 1) % 500 == 0:
            print(f"  {i+1}/{len(votes)}")

    print(f"Missing: {missing}")
    print(f"Saving {len(results)} results...")

    stats = {"by_party": {}}
    for pn in MAIN_PARTIES:
        ps = {"total_si": 0, "total_no": 0, "total_divided": 0, "total_ausente": 0, "total_no_data": 0}
        for r in results:
            p = r["party_positions"].get(pn, {}).get("position", "NO_DATA")
            if p == "SI": ps["total_si"] += 1
            elif p == "NO": ps["total_no"] += 1
            elif p == "DIVIDED": ps["total_divided"] += 1
            elif p == "AUSENTE": ps["total_ausente"] += 1
            else: ps["total_no_data"] += 1
        stats["by_party"][pn] = ps

    output = {
        "generated_at": datetime.now().isoformat(),
        "total_votes": len(results),
        "party_code_mapping": PARTY_CODE_MAP,
        "aggregate_stats": stats,
        "votes": results
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n=== Summary ===")
    for pn in MAIN_PARTIES:
        s = stats["by_party"][pn]
        t = s["total_si"] + s["total_no"] + s["total_divided"] + s["total_ausente"]
        if t > 0:
            print(f"{pn}: SI={s['total_si']} ({s['total_si']/t*100:.0f}%), NO={s['total_no']} ({s['total_no']/t*100:.0f}%)")
    print(f"\nSaved: {OUTPUT_PATH}")
    print("Done!")

if __name__ == "__main__":
    main()
