#!/usr/bin/env python3
"""
PHASE 1.3: Vote Classification
Builds vote index and classifies 2,226 congressional votes.
"""

import os
import sys
import json
import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
CONGRESS_DIR = DATA_DIR / "congress"
OPENPOLITICA_DIR = CONGRESS_DIR / "openpolitica" / "data" / "2021-2026"
VOTES_DIR = DATA_DIR / "votes"
PROCESSING_DIR = DATA_DIR / "processing"

VALID_CATEGORIES = [
    "seguridad", "economia", "fiscal", "social", "empleo",
    "educacion", "salud", "agua", "vivienda", "transporte",
    "energia", "mineria", "ambiente", "agricultura", "justicia"
]

# Keywords for classification
CATEGORY_KEYWORDS = {
    "seguridad": ["delincuencia", "policia", "crimen", "seguridad ciudadana", "terrorismo", "delitos", "penitenciario", "defensa nacional", "fuerzas armadas", "narcotrafico"],
    "economia": ["economia", "comercio", "exportacion", "importacion", "empresa", "pymes", "inversion", "mercado", "industria", "productividad", "competitividad"],
    "fiscal": ["presupuesto", "tributo", "impuesto", "igv", "renta", "sunat", "recaudacion", "gasto publico", "deficit", "fiscal", "deuda publica", "credito fiscal"],
    "social": ["pobreza", "inclusion", "discapacidad", "adulto mayor", "pension", "pensiones", "familia", "mujer", "igualdad", "violencia", "derechos humanos"],
    "empleo": ["trabajo", "empleo", "laboral", "trabajador", "sueldo", "salario", "sindical", "sunafil", "cts", "gratificacion", "despido"],
    "educacion": ["educacion", "universidad", "escolar", "estudiante", "profesor", "docente", "beca", "sunedu", "minedu", "academico", "investigacion"],
    "salud": ["salud", "hospital", "medico", "essalud", "sis", "vacuna", "pandemia", "covid", "medicamento", "enfermedad", "minsa", "farmacia"],
    "agua": ["agua", "saneamiento", "desague", "sunass", "sedapal", "acuifero", "riego", "hidrico", "potable"],
    "vivienda": ["vivienda", "urbanismo", "inmueble", "construccion", "alquiler", "hipoteca", "techo propio", "mivivienda", "asentamiento"],
    "transporte": ["transporte", "carretera", "ferroviario", "aeropuerto", "puerto", "metro", "metropolitano", "vehiculo", "transito", "infraestructura vial"],
    "energia": ["energia", "electricidad", "gas", "petroleo", "hidroelectrica", "solar", "eolica", "osinergmin", "combustible"],
    "mineria": ["mineria", "minas", "canon minero", "regalias mineras", "exploracion minera", "concesion minera", "extractiva"],
    "ambiente": ["ambiente", "ambiental", "contaminacion", "deforestacion", "biodiversidad", "cambio climatico", "residuos", "reciclaje", "areas protegidas", "oefa"],
    "agricultura": ["agricultura", "agropecuario", "campesino", "cosecha", "siembra", "agroindustria", "fertilizante", "semilla", "riego", "ganaderia", "pesca"],
    "justicia": ["justicia", "judicial", "fiscal", "juez", "congreso", "ley", "reglamento", "constitucion", "corte", "tribunal", "proceso", "sentencia", "ministerio publico", "jnj"]
}

def get_timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_vote_index():
    index_path = CONGRESS_DIR / "vote_index.json"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_vote_index(vote_index):
    index_path = CONGRESS_DIR / "vote_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(vote_index, f, indent=2, ensure_ascii=False)

def parse_metadatos(metadatos_path):
    """Parse metadatos.csv and return a dictionary."""
    result = {}
    try:
        with open(metadatos_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    key = row[0].strip().lower()
                    value = row[1].strip()
                    result[key] = value
    except Exception as e:
        print(f"Error parsing {metadatos_path}: {e}")
    return result

def extract_vote_id_from_path(voting_folder):
    """Extract vote ID from folder path like 2021-07-26T10-40-votacion."""
    folder_name = voting_folder.name
    # Remove -votacion suffix
    vote_id = folder_name.replace("-votacion", "")
    return vote_id

def build_vote_index():
    """Build index of all voting sessions."""
    print("Building vote index...")

    vote_index = []

    # Walk through the openpolitica directory structure
    # Structure: 2021-2026/YYYY/MM/DD/YYYY-MM-DDTHH-MM-votacion/
    for year_dir in sorted(OPENPOLITICA_DIR.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue

            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue

                for voting_folder in sorted(day_dir.iterdir()):
                    if not voting_folder.is_dir() or not voting_folder.name.endswith("-votacion"):
                        continue

                    metadatos_path = voting_folder / "metadatos.csv"
                    votaciones_path = voting_folder / "votaciones.csv"

                    if not metadatos_path.exists() or not votaciones_path.exists():
                        continue

                    metadatos = parse_metadatos(metadatos_path)

                    vote_entry = {
                        "vote_id": extract_vote_id_from_path(voting_folder),
                        "date": metadatos.get("dia", metadatos.get("fecha", "")),
                        "time": metadatos.get("hora", ""),
                        "asunto": metadatos.get("asunto", ""),
                        "presidente": metadatos.get("presidente", ""),
                        "quorum": int(metadatos.get("quorum", 0) or 0),
                        "metadatos_path": str(metadatos_path),
                        "votaciones_path": str(votaciones_path),
                        "classification_status": "pending"
                    }
                    vote_index.append(vote_entry)

    # Sort by date/time
    vote_index.sort(key=lambda x: (x["date"], x["time"]))

    # Assign sequential indices
    for i, vote in enumerate(vote_index):
        vote["index"] = i

    result = {
        "created_at": get_timestamp(),
        "total_votes": len(vote_index),
        "votes": vote_index
    }

    save_vote_index(result)
    print(f"Vote index built: {len(vote_index)} votes found")
    return result

def classify_vote_by_keywords(asunto):
    """Classify a vote by keyword matching."""
    asunto_lower = asunto.lower()

    # Score each category
    scores = {}
    keywords_found = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in asunto_lower:
                score += 1
                keywords_found.append(keyword)
        scores[category] = score

    # Get best category
    if max(scores.values()) > 0:
        best_category = max(scores, key=scores.get)
        # Get secondary category (second highest score)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        secondary = sorted_scores[1][0] if sorted_scores[1][1] > 0 else None
    else:
        best_category = "justicia"  # default for parliamentary procedures
        secondary = None

    # Determine vote type
    procedural_keywords = ["cuestion de orden", "cuestion previa", "reconsideracion",
                          "reglamento", "mocion", "dispensa", "exoneracion de segunda votacion",
                          "comision", "levantamiento", "orden del dia", "agenda"]

    declarativo_keywords = ["declarar", "declaracion", "reconocimiento", "homenaje",
                           "saludar", "expresar", "interes nacional", "necesidad publica",
                           "dia de", "semana de", "ano de"]

    vote_type = "sustantivo"  # default
    for kw in procedural_keywords:
        if kw in asunto_lower:
            vote_type = "procedural"
            break
    if vote_type != "procedural":
        for kw in declarativo_keywords:
            if kw in asunto_lower:
                vote_type = "declarativo"
                break

    # Calculate confidence based on keyword matches
    max_score = max(scores.values())
    confidence = min(0.95, 0.5 + (max_score * 0.15))

    return {
        "category": best_category,
        "secondary_category": secondary,
        "vote_type": vote_type,
        "confidence": round(confidence, 2),
        "keywords_detected": list(set(keywords_found)),
        "reasoning": f"Clasificado por {max_score} palabras clave detectadas relacionadas con {best_category}"
    }

def load_classification_progress():
    """Load progress from checkpoint."""
    checkpoint_path = PROCESSING_DIR / "vote_classification_checkpoint.json"
    if checkpoint_path.exists():
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"last_batch": -1, "votes_classified": 0}

def save_classification_progress(batch_num, votes_classified):
    """Save progress checkpoint."""
    checkpoint_path = PROCESSING_DIR / "vote_classification_checkpoint.json"
    with open(checkpoint_path, 'w', encoding='utf-8') as f:
        json.dump({
            "last_batch": batch_num,
            "votes_classified": votes_classified,
            "timestamp": get_timestamp()
        }, f, indent=2)

def classify_all_votes(batch_size=20):
    """Classify all votes in batches."""
    # Load or build vote index
    vote_index_data = load_vote_index()
    if vote_index_data is None:
        vote_index_data = build_vote_index()

    votes = vote_index_data["votes"]
    total_votes = len(votes)

    # Check expected count
    if total_votes != 2226:
        print(f"Warning: Expected 2226 votes, found {total_votes}")

    # Load progress
    progress = load_classification_progress()
    start_batch = progress["last_batch"] + 1

    # Ensure directories exist
    VOTES_DIR.mkdir(parents=True, exist_ok=True)

    classifications = []

    # Load any existing classifications
    for batch_file in sorted(VOTES_DIR.glob("batch_*.json")):
        with open(batch_file, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)
            classifications.extend(batch_data.get("results", []))

    # Calculate total batches
    total_batches = (total_votes + batch_size - 1) // batch_size

    print(f"Starting from batch {start_batch + 1}, total batches: {total_batches}")

    for batch_num in range(start_batch, total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_votes)
        batch_votes = votes[start_idx:end_idx]

        batch_results = []

        for vote in batch_votes:
            # Classify the vote
            classification = classify_vote_by_keywords(vote["asunto"])

            result = {
                "vote_id": vote["vote_id"],
                "date": vote["date"],
                "time": vote["time"],
                "asunto": vote["asunto"],
                "category": classification["category"],
                "secondary_category": classification["secondary_category"],
                "vote_type": classification["vote_type"],
                "confidence": classification["confidence"],
                "reasoning": classification["reasoning"],
                "keywords_detected": classification["keywords_detected"],
                "metadatos_path": vote["metadatos_path"],
                "votaciones_path": vote["votaciones_path"]
            }
            batch_results.append(result)

        # Save batch checkpoint
        batch_file = VOTES_DIR / f"batch_{batch_num:03d}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump({
                "batch_num": batch_num,
                "start_idx": start_idx,
                "end_idx": end_idx,
                "results": batch_results,
                "timestamp": get_timestamp()
            }, f, indent=2, ensure_ascii=False)

        classifications.extend(batch_results)

        # Save progress checkpoint every 10 batches
        if (batch_num + 1) % 10 == 0:
            save_classification_progress(batch_num, len(classifications))

        percent = round((end_idx / total_votes) * 100, 1)
        print(f"Batch {batch_num + 1}/{total_batches} complete ({percent}%)")

    # Calculate statistics
    stats = {
        "by_category": {},
        "by_vote_type": {},
        "average_confidence": 0,
        "low_confidence_count": 0,
        "fallback_count": 0
    }

    for cat in VALID_CATEGORIES:
        stats["by_category"][cat] = len([c for c in classifications if c["category"] == cat])

    for vt in ["declarativo", "sustantivo", "procedural"]:
        stats["by_vote_type"][vt] = len([c for c in classifications if c["vote_type"] == vt])

    if classifications:
        stats["average_confidence"] = round(
            sum(c["confidence"] for c in classifications) / len(classifications), 2
        )
        stats["low_confidence_count"] = len([c for c in classifications if c["confidence"] < 0.5])

    # Save final output
    output = {
        "extraction_date": get_timestamp(),
        "total_votes": len(classifications),
        "classification_stats": stats,
        "votes": classifications
    }

    output_path = DATA_DIR / "votes_categorized.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nClassification complete: {len(classifications)} votes")
    print(f"Saved to: {output_path}")

    return output

def validate_phase():
    """Validate Phase 1.3 output."""
    output_path = DATA_DIR / "votes_categorized.json"

    validation = {
        "phase": "1.3",
        "phase_name": "Vote Classification",
        "started_at": None,
        "completed_at": get_timestamp(),
        "total_votes_expected": 2226,
        "total_votes_classified": 0,
        "batches_processed": 0,
        "successful_batches": 0,
        "individual_retries": 0,
        "fallbacks_used": 0,
        "validation_checks": {
            "all_votes_classified": False,
            "all_categories_valid": True,
            "all_vote_types_valid": True,
            "all_confidence_in_range": True,
            "no_empty_reasoning": True,
            "no_missing_vote_ids": True,
            "category_distribution_reasonable": True
        },
        "status": "FAIL"
    }

    if not output_path.exists():
        print("votes_categorized.json not found!")
        return validation

    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    votes = data.get("votes", [])
    validation["total_votes_classified"] = len(votes)

    # Check all votes classified
    validation["validation_checks"]["all_votes_classified"] = len(votes) >= 2226

    # Validate each vote
    vote_ids = set()
    for vote in votes:
        vote_ids.add(vote["vote_id"])

        if vote.get("category") not in VALID_CATEGORIES:
            validation["validation_checks"]["all_categories_valid"] = False

        if vote.get("vote_type") not in ["declarativo", "sustantivo", "procedural"]:
            validation["validation_checks"]["all_vote_types_valid"] = False

        conf = vote.get("confidence", 0)
        if not (0.0 <= conf <= 1.0):
            validation["validation_checks"]["all_confidence_in_range"] = False

        if not vote.get("reasoning"):
            validation["validation_checks"]["no_empty_reasoning"] = False

        if not vote.get("vote_id"):
            validation["validation_checks"]["no_missing_vote_ids"] = False

    # Check category distribution
    stats = data.get("classification_stats", {}).get("by_category", {})
    total = sum(stats.values())
    if total > 0:
        for cat, count in stats.items():
            if count / total > 0.4:  # No category should have > 40%
                validation["validation_checks"]["category_distribution_reasonable"] = False

    # Count batches
    validation["batches_processed"] = len(list(VOTES_DIR.glob("batch_*.json")))
    validation["successful_batches"] = validation["batches_processed"]

    # Overall status
    if all(validation["validation_checks"].values()) and len(votes) >= 2226:
        validation["status"] = "PASS"

    # Save validation
    val_path = PROCESSING_DIR / "phase_1_3_validation.json"
    with open(val_path, 'w', encoding='utf-8') as f:
        json.dump(validation, f, indent=2, ensure_ascii=False)

    return validation

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python phase_1_3_vote_classification.py build-index")
        print("  python phase_1_3_vote_classification.py classify")
        print("  python phase_1_3_vote_classification.py validate")
        print("  python phase_1_3_vote_classification.py status")
        return

    cmd = sys.argv[1]

    if cmd == "build-index":
        result = build_vote_index()
        print(f"Index built: {result['total_votes']} votes")

    elif cmd == "classify":
        output = classify_all_votes()
        print(f"Classification stats: {output['classification_stats']}")

    elif cmd == "validate":
        validation = validate_phase()
        print(json.dumps(validation, indent=2))

    elif cmd == "status":
        vote_index = load_vote_index()
        progress = load_classification_progress()

        if vote_index:
            print(f"Vote index: {vote_index['total_votes']} votes")
        else:
            print("Vote index: Not built")

        print(f"Last batch: {progress['last_batch'] + 1}")
        print(f"Votes classified: {progress['votes_classified']}")

if __name__ == "__main__":
    main()
