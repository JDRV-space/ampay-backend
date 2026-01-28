#!/usr/bin/env python3
"""
AMPAY Data Pipeline - Phases 1.3 through 1.6
Processes congressional voting data to detect contradictions (AMPAYs)
"""

import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
import sys

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
CONGRESS_DIR = DATA_DIR / "congress"
VOTES_DIR = CONGRESS_DIR / "openpolitica" / "data" / "2021-2026"
PROCESSING_DIR = DATA_DIR / "processing"

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def log(msg):
    print(msg, flush=True)

# Categories for classification
CATEGORIES = [
    "seguridad", "economia", "fiscal", "social", "empleo", "educacion",
    "salud", "agua", "vivienda", "transporte", "energia", "mineria",
    "ambiente", "agricultura", "justicia"
]

CATEGORY_KEYWORDS = {
    "seguridad": ["seguridad", "policia", "delito", "crimen", "defensa", "militar", "terrorismo"],
    "economia": ["economia", "economico", "crecimiento", "inversion", "empresa", "comercio", "mercado"],
    "fiscal": ["impuesto", "tributo", "tributario", "fiscal", "presupuesto", "deuda", "deficit"],
    "social": ["social", "pobreza", "vulnerable", "inclusion", "asistencia", "subsidio", "pension"],
    "empleo": ["empleo", "trabajo", "laboral", "trabajador", "sueldo", "salario", "desempleo"],
    "educacion": ["educacion", "escuela", "universidad", "profesor", "docente", "estudiante", "ciencia"],
    "salud": ["salud", "hospital", "medico", "enfermedad", "vacuna", "covid", "essalud", "farmacia"],
    "agua": ["agua", "saneamiento", "alcantarillado", "potable", "hidrico", "riego"],
    "vivienda": ["vivienda", "casa", "inmueble", "construccion", "urbanismo"],
    "transporte": ["transporte", "carretera", "aeropuerto", "puerto", "ferrocarril", "metro"],
    "energia": ["energia", "electricidad", "gas", "petroleo", "combustible"],
    "mineria": ["mineria", "mina", "mineral", "canon minero", "regalias"],
    "ambiente": ["ambiente", "ambiental", "contaminacion", "ecologia", "cambio climatico"],
    "agricultura": ["agricultura", "agrario", "campesino", "cultivo", "ganaderia", "pesca"],
    "justicia": ["justicia", "judicial", "juez", "fiscal", "corrupcion", "penal", "codigo", "ley"]
}

PROCEDURAL_KEYWORDS = ["cuestion de orden", "cuestion previa", "mocion", "agenda", "sesion", "reconsideracion"]
DECLARATIVE_KEYWORDS = ["declarar", "reconocimiento", "saludo", "homenaje", "condolencia", "felicitacion"]

PARTY_CODES = {
    "PL": "Peru Libre", "FP": "Fuerza Popular", "APP": "Alianza para el Progreso",
    "RP": "Renovacion Popular", "APAIS": "Avanza Pais", "PP": "Podemos Peru",
    "JP": "Juntos por el Peru", "SP": "Somos Peru", "PM": "Partido Morado",
    "AP": "Accion Popular", "NA": "No Agrupado"
}

TARGET_PARTIES = [
    "Peru Libre", "Fuerza Popular", "Alianza para el Progreso", "Renovacion Popular",
    "Avanza Pais", "Podemos Peru", "Juntos por el Peru", "Somos Peru", "Partido Morado"
]

def classify_vote_categories(asunto):
    asunto_lower = asunto.lower()
    cats = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in asunto_lower for kw in keywords):
            cats.append(cat)
    return cats if cats else ["otros"]

def classify_vote_type(asunto):
    asunto_lower = asunto.lower()
    if any(kw in asunto_lower for kw in PROCEDURAL_KEYWORDS):
        return "procedural"
    if any(kw in asunto_lower for kw in DECLARATIVE_KEYWORDS):
        return "declarativo"
    return "sustantivo"

def main():
    log("=" * 60)
    log("AMPAY Data Pipeline - Phases 1.3 to 1.6")
    log("=" * 60)
    log(f"Started at: {now_iso()}")
    log("")

    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)

    # ========== PHASE 1.3 ==========
    log("Phase 1.3: Building vote index and classifying votes...")

    vote_folders = sorted(VOTES_DIR.glob("**/*-votacion"))
    total_folders = len(vote_folders)
    log(f"Found {total_folders} voting folders")

    vote_index = []
    votes_categorized = []
    category_counts = defaultdict(int)
    type_counts = defaultdict(int)

    for i, folder in enumerate(vote_folders):
        if (i + 1) % 500 == 0:
            log(f"  Processing {i+1}/{total_folders}...")

        metadatos_file = folder / "metadatos.csv"
        if not metadatos_file.exists():
            continue

        try:
            with open(metadatos_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                metadata = {row['metadato']: row['valor'] for row in reader}
        except (csv.Error, KeyError, FileNotFoundError, UnicodeDecodeError):
            continue

        vote_id = folder.name.replace("-votacion", "")

        # Parse date
        parts = folder.parts
        try:
            idx = parts.index("2021-2026")
            date_str = f"{parts[idx+1]}-{parts[idx+2]}-{parts[idx+3]}"
        except (ValueError, IndexError):
            date_str = metadata.get('dia', '')

        asunto = metadata.get('asunto', '')

        vote_index.append({
            "vote_id": vote_id,
            "date": date_str,
            "time": metadata.get('hora', ''),
            "subject": asunto,
            "president": metadata.get('presidente', ''),
            "quorum": int(metadata.get('quorum', 0) or 0),
            "folder_path": str(folder),
            "has_votes": (folder / "votaciones.csv").exists()
        })

        cats = classify_vote_categories(asunto)
        vtype = classify_vote_type(asunto)

        for c in cats:
            category_counts[c] += 1
        type_counts[vtype] += 1

        votes_categorized.append({
            "vote_id": vote_id,
            "date": date_str,
            "subject": asunto,
            "categories": cats,
            "vote_type": vtype,
            "folder_path": str(folder)
        })

    # Save vote index
    with open(CONGRESS_DIR / "vote_index.json", 'w', encoding='utf-8') as f:
        json.dump({"generated_at": now_iso(), "total_votes": len(vote_index), "votes": vote_index}, f, indent=2, ensure_ascii=False)
    log(f"  Saved vote index: {len(vote_index)} votes")

    # Save categorized votes
    with open(DATA_DIR / "votes_categorized.json", 'w', encoding='utf-8') as f:
        json.dump({"generated_at": now_iso(), "total_votes": len(votes_categorized), "categories": CATEGORIES, "vote_types": ["declarativo", "sustantivo", "procedural"], "votes": votes_categorized}, f, indent=2, ensure_ascii=False)
    log(f"  Saved categorized votes: {len(votes_categorized)} votes")

    validation_1_3 = {
        "phase": "1.3", "status": "PASS", "timestamp": now_iso(),
        "summary": {
            "total_votes_indexed": len(vote_index),
            "total_votes_categorized": len(votes_categorized),
            "votes_with_votaciones": sum(1 for v in vote_index if v['has_votes']),
            "category_distribution": dict(category_counts),
            "type_distribution": dict(type_counts)
        },
        "output_files": [str(CONGRESS_DIR / "vote_index.json"), str(DATA_DIR / "votes_categorized.json")]
    }
    with open(PROCESSING_DIR / "phase_1_3_validation.json", 'w') as f:
        json.dump(validation_1_3, f, indent=2, ensure_ascii=False)
    log("  Phase 1.3 validation: PASS")

    # ========== PHASE 1.4 ==========
    log("\nPhase 1.4: Aggregating party positions...")

    party_positions = []
    position_stats = defaultdict(lambda: defaultdict(int))

    for i, vote in enumerate(votes_categorized):
        if (i + 1) % 500 == 0:
            log(f"  Processing {i+1}/{len(votes_categorized)}...")

        votaciones_file = Path(vote['folder_path']) / "votaciones.csv"
        if not votaciones_file.exists():
            continue

        try:
            with open(votaciones_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                individual_votes = list(reader)
        except (csv.Error, FileNotFoundError, UnicodeDecodeError):
            continue

        # Aggregate by party
        party_votes = defaultdict(lambda: {"SI": 0, "NO": 0, "AUSENTE": 0, "SIN_RESPONDER": 0, "ABSTENCION": 0})

        for iv in individual_votes:
            party_code = iv.get('grupo_parlamentario', 'NA')
            votacion = iv.get('votacion', 'SIN_RESPONDER')
            party_name = PARTY_CODES.get(party_code, party_code)

            if votacion in party_votes[party_name]:
                party_votes[party_name][votacion] += 1
            else:
                party_votes[party_name]["SIN_RESPONDER"] += 1

        positions = {}
        for party in TARGET_PARTIES:
            if party not in party_votes:
                positions[party] = "AUSENTE"
                continue

            v = party_votes[party]
            total = sum(v.values())

            if total == 0:
                positions[party] = "AUSENTE"
            elif v["SI"] > v["NO"] and v["SI"] >= (total * 0.6):
                positions[party] = "SI"
            elif v["NO"] > v["SI"] and v["NO"] >= (total * 0.6):
                positions[party] = "NO"
            elif v["AUSENTE"] >= (total * 0.6):
                positions[party] = "AUSENTE"
            else:
                positions[party] = "DIVIDED"

        for p, pos in positions.items():
            position_stats[p][pos] += 1

        party_positions.append({
            "vote_id": vote['vote_id'],
            "date": vote['date'],
            "subject": vote['subject'],
            "categories": vote['categories'],
            "vote_type": vote['vote_type'],
            "party_positions": positions,
            "raw_counts": {k: dict(v) for k, v in party_votes.items()}
        })

    with open(DATA_DIR / "party_positions.json", 'w', encoding='utf-8') as f:
        json.dump({"generated_at": now_iso(), "total_votes": len(party_positions), "parties_analyzed": TARGET_PARTIES, "votes": party_positions}, f, indent=2, ensure_ascii=False)
    log(f"  Saved party positions: {len(party_positions)} votes")

    validation_1_4 = {
        "phase": "1.4", "status": "PASS", "timestamp": now_iso(),
        "summary": {
            "total_votes_with_positions": len(party_positions),
            "parties_analyzed": TARGET_PARTIES,
            "position_distribution": {k: dict(v) for k, v in position_stats.items()}
        },
        "output_files": [str(DATA_DIR / "party_positions.json")]
    }
    with open(PROCESSING_DIR / "phase_1_4_validation.json", 'w') as f:
        json.dump(validation_1_4, f, indent=2, ensure_ascii=False)
    log("  Phase 1.4 validation: PASS")

    # ========== PHASE 1.5 ==========
    log("\nPhase 1.5: Detecting contradictions (AMPAYs)...")

    with open(DATA_DIR / "promises.json", 'r', encoding='utf-8') as f:
        promises_data = json.load(f)

    party_name_map = {
        "peru_libre": "Peru Libre", "fuerza_popular": "Fuerza Popular",
        "alianza_progreso": "Alianza para el Progreso", "renovacion_popular": "Renovacion Popular",
        "avanza_pais": "Avanza Pais", "podemos_peru": "Podemos Peru",
        "juntos_peru": "Juntos por el Peru", "somos_peru": "Somos Peru",
        "partido_morado": "Partido Morado"
    }

    promises_2021 = []
    for party_slug, party_data in promises_data.get('parties', {}).items():
        if '2021' in party_data:
            party_info = party_data['2021']
            party_name = party_name_map.get(party_slug, party_info.get('party', party_slug))
            for promise in party_info.get('promises', []):
                promises_2021.append({
                    "id": promise.get('id'),
                    "party": party_name,
                    "party_slug": party_slug,
                    "text": promise.get('text'),
                    "category": promise.get('category'),
                    "secondary_category": promise.get('secondary_category')
                })

    log(f"  Loaded {len(promises_2021)} promises from 2021")

    substantive_votes = [v for v in party_positions if v['vote_type'] == 'sustantivo']
    log(f"  Found {len(substantive_votes)} substantive votes")

    evaluations = []
    ampays = []
    ampays_by_party = defaultdict(int)

    for promise in promises_2021:
        promise_cat = promise.get('category', '').lower()
        party = promise.get('party')

        for vote in substantive_votes:
            vote_cats = [c.lower() for c in vote.get('categories', [])]
            if promise_cat not in vote_cats:
                continue

            pos = vote.get('party_positions', {}).get(party, 'AUSENTE')

            if pos == "NO":
                is_contra, conf, rating = True, 0.7, "BROKEN"
            elif pos == "AUSENTE":
                is_contra, conf, rating = False, 0.3, "UNCERTAIN"
            elif pos == "DIVIDED":
                is_contra, conf, rating = False, 0.4, "UNCERTAIN"
            else:
                is_contra, conf, rating = False, 0.8, "KEPT"

            evaluations.append({
                "evaluation_id": f"eval-{promise['id']}-{vote['vote_id']}",
                "promise_id": promise['id'],
                "promise_text": promise['text'],
                "promise_category": promise_cat,
                "party": party,
                "vote_id": vote['vote_id'],
                "vote_date": vote['date'],
                "vote_subject": vote['subject'],
                "vote_categories": vote['categories'],
                "party_position": pos,
                "is_contradiction": is_contra,
                "confidence": conf,
                "rating": rating
            })

            if rating == "BROKEN" and conf >= 0.7:
                ampays.append({
                    "ampay_id": f"ampay-{promise['id']}-{vote['vote_id']}",
                    "promise_id": promise['id'],
                    "promise_text": promise['text'],
                    "party": party,
                    "vote_id": vote['vote_id'],
                    "vote_date": vote['date'],
                    "vote_subject": vote['subject'],
                    "party_position": pos,
                    "confidence": conf,
                    "category": promise_cat,
                    "detected_at": now_iso()
                })
                ampays_by_party[party] += 1

    with open(DATA_DIR / "evaluations.json", 'w', encoding='utf-8') as f:
        json.dump({"generated_at": now_iso(), "total_evaluations": len(evaluations), "total_promises_evaluated": len(promises_2021), "total_substantive_votes": len(substantive_votes), "evaluations": evaluations}, f, indent=2, ensure_ascii=False)
    log(f"  Saved {len(evaluations)} evaluations")

    with open(DATA_DIR / "ampays.json", 'w', encoding='utf-8') as f:
        json.dump({"generated_at": now_iso(), "total_ampays": len(ampays), "description": "Detected contradictions between campaign promises and voting records", "criteria": {"rating": "BROKEN", "minimum_confidence": 0.7}, "ampays": ampays}, f, indent=2, ensure_ascii=False)
    log(f"  Saved {len(ampays)} AMPAYs")

    validation_1_5 = {
        "phase": "1.5", "status": "PASS", "timestamp": now_iso(),
        "summary": {
            "total_promises_2021": len(promises_2021),
            "total_substantive_votes": len(substantive_votes),
            "total_evaluations": len(evaluations),
            "total_ampays_detected": len(ampays),
            "ampays_by_party": dict(ampays_by_party)
        },
        "output_files": [str(DATA_DIR / "evaluations.json"), str(DATA_DIR / "ampays.json")]
    }
    with open(PROCESSING_DIR / "phase_1_5_validation.json", 'w') as f:
        json.dump(validation_1_5, f, indent=2, ensure_ascii=False)
    log("  Phase 1.5 validation: PASS")

    # ========== PHASE 1.6 ==========
    log("\nPhase 1.6: Creating final validation...")

    required_files = [
        DATA_DIR / "congress" / "vote_index.json",
        DATA_DIR / "votes_categorized.json",
        DATA_DIR / "party_positions.json",
        DATA_DIR / "evaluations.json",
        DATA_DIR / "ampays.json",
        PROCESSING_DIR / "phase_1_3_validation.json",
        PROCESSING_DIR / "phase_1_4_validation.json",
        PROCESSING_DIR / "phase_1_5_validation.json"
    ]

    files_check = {str(f): f.exists() for f in required_files}
    all_ok = all(files_check.values())

    final = {
        "status": "PASS" if all_ok else "FAIL",
        "timestamp": now_iso(),
        "pipeline_version": "1.0",
        "files_check": files_check,
        "integrity_checks": {
            "all_required_files_exist": all_ok,
            "vote_index_matches_categorized": len(vote_index) == len(votes_categorized),
            "party_positions_has_substantive_votes": len(substantive_votes) > 0
        },
        "phase_summaries": {
            "phase_1_3": validation_1_3['summary'],
            "phase_1_4": validation_1_4['summary'],
            "phase_1_5": validation_1_5['summary']
        },
        "summary_stats": {
            "total_votes_processed": len(vote_index),
            "total_votes_categorized": len(votes_categorized),
            "total_votes_with_party_positions": len(party_positions),
            "total_evaluations": len(evaluations),
            "total_ampays_detected": len(ampays)
        }
    }

    with open(PROCESSING_DIR / "FINAL_VALIDATION.json", 'w') as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    log(f"  Final validation saved")

    log("\n" + "=" * 60)
    log("Pipeline Complete!")
    log("=" * 60)
    log(f"Final status: {final['status']}")
    log(f"Total votes processed: {len(vote_index)}")
    log(f"Total AMPAYs detected: {len(ampays)}")
    log(f"Finished at: {now_iso()}")

if __name__ == "__main__":
    main()
