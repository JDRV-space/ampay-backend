#!/usr/bin/env python3
"""
AMPAY Contradiction Filtering Script
Phases 1-3: Extract, filter, and validate contradictions from party voting data.

Handles multiple JSON structures from different party files.

Author: JDRV-space
Date: 2026-01-21
"""

import json
import csv
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
OUTPUT_JSON = DATA_DIR / "ampay_FILTERED_FOR_REVIEW.json"
OUTPUT_CSV = DATA_DIR / "ampay_FILTERED_FOR_REVIEW.csv"

# Phase 1: Procedural keywords to filter out
PROCEDURAL_KEYWORDS = [
    "EXONERACION DE LA SEGUNDA VOTACION",
    "EXONERACIÓN DE LA SEGUNDA VOTACIÓN",
    "CUESTION PREVIA",
    "CUESTIÓN PREVIA",
    "CUESTION DE ORDEN",
    "CUESTIÓN DE ORDEN",
    "RECONSIDERACION",
    "RECONSIDERACIÓN",
    "ADMISION A DEBATE",
    "ADMISIÓN A DEBATE",
    "INSISTENCIA EN LA AUTOGRAFA",
    "INSISTENCIA EN LA AUTÓGRAFA",
]


@dataclass
class Contradiction:
    """Represents a single contradiction found in voting data."""
    party: str
    promise_id: str
    promise_text: str
    promise_category: str
    law_date: str
    law_asunto: str
    vote_id: str
    party_vote: str
    expected_vote: str
    contradiction_type: str  # A = NO on supporting, B = SI on contradicting
    keywords_used: List[str] = field(default_factory=list)
    # Phase 2 fields
    relevance_score: int = 0
    reasoning: str = ""
    is_valid: bool = True
    filter_reason: str = ""


def is_procedural(asunto: str) -> Tuple[bool, str]:
    """Check if law asunto contains procedural keywords (Phase 1 filter)."""
    asunto_upper = asunto.upper()
    for keyword in PROCEDURAL_KEYWORDS:
        if keyword.upper() in asunto_upper:
            return True, keyword
    return False, ""


def get_party_position(law: dict, party_code: str) -> Optional[str]:
    """Extract party position from law record, handling different naming conventions."""
    # Try various position key formats
    possible_keys = [
        f"{party_code.lower()}_position",
        f"{party_code.upper()}_position",
        "position",
        f"{party_code.lower()}_pos",
    ]

    for key in possible_keys:
        if key in law:
            return law[key]

    # Also check for si/no counts to infer position
    si_key = f"{party_code.lower()}_si"
    no_key = f"{party_code.lower()}_no"

    if si_key in law and no_key in law:
        si = law.get(si_key, 0)
        no = law.get(no_key, 0)
        if si > 0 and no == 0:
            return "SI"
        elif no > 0 and si == 0:
            return "NO"
        elif si > 0 and no > 0:
            return "DIVIDED"

    return None


def extract_contradictions_from_file(filepath: Path) -> List[Contradiction]:
    """Extract all contradictions from a single party JSON file."""
    contradictions = []

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    party_name = data.get("party", "Unknown")
    party_code = data.get("party_code", "").lower()

    # If no party_code, try to derive from filename
    if not party_code:
        filename = filepath.stem.lower()
        code_map = {
            "fuerza_popular": "fp",
            "peru_libre": "pl",
            "renovacion_popular": "rp",
            "somos_peru": "sp",
            "avanza_pais": "ap",
            "alianza_progreso": "app",
            "podemos_peru": "pp",
            "juntos_peru": "jp",
            "partido_morado": "pm",
        }
        for name, code in code_map.items():
            if name in filename:
                party_code = code
                break

    # Get results array - can be "results" or "detailed_analysis"
    results = data.get("results", data.get("detailed_analysis", []))

    for result in results:
        promise_id = result.get("promise_id", "")
        promise_text = result.get("promise_text", "")
        promise_category = result.get("category", "")

        # Get keywords
        keywords_obj = result.get("keywords_used", result.get("keywords", {}))
        supporting_keywords = keywords_obj.get("supporting", [])
        contradicting_keywords = keywords_obj.get("contradicting", [])

        # STRUCTURE 1: supporting_laws_detail / contradicting_laws_detail (arrays)
        # STRUCTURE 2: supporting_votes / contradicting_votes (arrays)
        # STRUCTURE 3: supporting_laws.laws / contradicting_laws.laws (nested)
        # STRUCTURE 4: supporting_laws.votes / contradicting_laws.votes (nested)

        # Collect all supporting law records
        supporting_laws = []

        # Structure 1
        if "supporting_laws_detail" in result:
            supporting_laws.extend(result["supporting_laws_detail"])

        # Structure 2
        if "supporting_votes" in result:
            supporting_laws.extend(result["supporting_votes"])

        # Structure 3 & 4
        if "supporting_laws" in result and isinstance(result["supporting_laws"], dict):
            if "laws" in result["supporting_laws"]:
                supporting_laws.extend(result["supporting_laws"]["laws"])
            if "votes" in result["supporting_laws"]:
                supporting_laws.extend(result["supporting_laws"]["votes"])

        # Collect all contradicting law records
        contradicting_laws = []

        if "contradicting_laws_detail" in result:
            contradicting_laws.extend(result["contradicting_laws_detail"])

        if "contradicting_votes" in result:
            contradicting_laws.extend(result["contradicting_votes"])

        if "contradicting_laws" in result and isinstance(result["contradicting_laws"], dict):
            if "laws" in result["contradicting_laws"]:
                contradicting_laws.extend(result["contradicting_laws"]["laws"])
            if "votes" in result["contradicting_laws"]:
                contradicting_laws.extend(result["contradicting_laws"]["votes"])

        # Type A: NO on supporting laws (party voted NO when should have voted SI)
        for law in supporting_laws:
            position = get_party_position(law, party_code)
            aligned = law.get("aligned", None)
            expected = law.get("expected_vote", "SI")

            # A contradiction exists if:
            # 1. Position is explicitly "NO", OR
            # 2. aligned is False and expected was SI
            is_contradiction = False

            if position == "NO":
                is_contradiction = True
            elif aligned is False and expected == "SI":
                is_contradiction = True
            elif aligned is None and position and position != "SI" and position != "DIVIDED":
                # Position exists, not SI, not divided - likely NO
                is_contradiction = True

            if is_contradiction:
                contradictions.append(Contradiction(
                    party=party_name,
                    promise_id=promise_id,
                    promise_text=promise_text,
                    promise_category=promise_category,
                    law_date=law.get("date", ""),
                    law_asunto=law.get("asunto", ""),
                    vote_id=law.get("vote_id", ""),
                    party_vote=position or "NO",
                    expected_vote="SI",
                    contradiction_type="A",
                    keywords_used=supporting_keywords,
                ))

        # Type B: SI on contradicting laws (party voted SI when should have voted NO)
        for law in contradicting_laws:
            position = get_party_position(law, party_code)
            aligned = law.get("aligned", None)
            expected = law.get("expected_vote", "NO")

            # A contradiction exists if:
            # 1. Position is "SI", OR
            # 2. aligned is False (they didn't vote as expected, i.e., NO)
            is_contradiction = False

            if position == "SI":
                is_contradiction = True
            elif aligned is False:
                is_contradiction = True

            if is_contradiction:
                contradictions.append(Contradiction(
                    party=party_name,
                    promise_id=promise_id,
                    promise_text=promise_text,
                    promise_category=promise_category,
                    law_date=law.get("date", ""),
                    law_asunto=law.get("asunto", ""),
                    vote_id=law.get("vote_id", ""),
                    party_vote=position or "SI",
                    expected_vote="NO",
                    contradiction_type="B",
                    keywords_used=contradicting_keywords,
                ))

    return contradictions


def phase1_filter_procedural(contradictions: List[Contradiction]) -> Tuple[List[Contradiction], List[Contradiction]]:
    """Phase 1: Remove procedural false positives."""
    valid = []
    filtered = []

    for c in contradictions:
        is_proc, keyword = is_procedural(c.law_asunto)
        if is_proc:
            c.is_valid = False
            c.filter_reason = f"PHASE1_PROCEDURAL: {keyword}"
            filtered.append(c)
        else:
            valid.append(c)

    return valid, filtered


def evaluate_semantic_relevance(contradiction: Contradiction) -> Tuple[int, str, bool]:
    """
    Phase 2: Evaluate if the law actually relates to the promise semantically.
    Returns (score 1-5, reasoning, is_valid).

    Score guide:
    5 = Strong direct relationship, clear contradiction
    4 = Good relationship, likely contradiction
    3 = Moderate relationship, possible contradiction
    2 = Weak relationship, probably false positive
    1 = No real relationship, clear false positive
    """
    asunto = contradiction.law_asunto.upper()
    promise = contradiction.promise_text.upper()
    category = contradiction.promise_category.lower()
    keywords = [k.upper() for k in contradiction.keywords_used if isinstance(k, str)]

    # Known false positive patterns
    false_positive_patterns = [
        # CESE in military/police context is not about employment termination promises
        (r"CESE.*MIEMBROS.*FUERO MILITAR", "CESE in military context, not employment"),
        (r"CESE.*MIEMBROS.*POLICIAL", "CESE in police context, not employment"),
        (r"CESE.*TRIBUNAL.*MILITAR", "CESE of military tribunal members"),
        (r"DESIGNACION.*CESE.*FUERO", "Designation/CESE in military forum context"),
        (r"DESIGNACI.N.*CESE.*FUERO", "Designation/CESE in military forum context"),
        (r"LEY DE ORGANIZACI.N.*FUERO MILITAR", "Military organization law"),

        # Procedural votes that slipped through
        (r"NOMINA.*INTEGRANTES.*COMISION", "Nomination of commission members"),
        (r"NÓMINA.*INTEGRANTES.*COMISIÓN", "Nomination of commission members"),
        (r"CUADRO NOMINATIVO", "Nomination table"),
        (r"MESA DIRECTIVA", "Mesa directiva procedural vote"),
        (r"ELECCION.*LISTA", "Election of list/slate"),
        (r"PARTICIPACI.N DE LA LISTA", "List participation procedural"),

        # Budget-related that's too generic
        (r"CUENTA GENERAL.*REPUBLICA.*EJERCICIO FISC", "General fiscal account review"),
        (r"CUENTA GENERAL.*REPÚBLICA.*EJERCICIO FISC", "General fiscal account review"),

        # OIT/International agreements (typically supporting, not contradicting)
        (r"ORGANIZACION INTERNACIONAL DEL TRABAJO", "OIT agreement - likely supporting"),
        (r"ORGANIZACIÓN INTERNACIONAL DEL TRABAJO", "OIT agreement - likely supporting"),

        # International agreements/treaties - typically procedural
        (r"ACUERDO DE TRANSPORTE A.REO", "International transport agreement"),
        (r"PROYECTO DE RESOLUCI.N LEGISLATIVA.*APRUEBA EL ACUERDO", "International agreement approval"),

        # Investigation commissions for other topics mismatched
        (r"COMISION INVESTIGADORA.*IRREGULARIDADES", "Investigation commission - verify relevance"),
        (r"COMISIÓN INVESTIGADORA.*IRREGULARIDADES", "Investigation commission - verify relevance"),

        # Declarative laws (national interest declarations) - weak relevance
        (r"DECLARA DE INTER.S NACIONAL.*D.A", "National interest day declaration"),
        (r"D.A DEL OBRERO", "Worker day declaration"),
        (r"FERIADO NO LABORABLE", "Non-working holiday declaration"),
    ]

    for pattern, reason in false_positive_patterns:
        if re.search(pattern, asunto, re.IGNORECASE):
            return 1, f"FALSE_POSITIVE: {reason}", False

    # Category-specific relevance checks
    category_keywords = {
        "empleo": ["TRABAJO", "EMPLEO", "LABORAL", "TRABAJADOR", "EMPLEADO", "CONTRAT", "SALARIO", "SUELDO", "PENSION", "JUBILA", "MYPE", "CTS", "BENEFICIO LABORAL", "REMUNERAC"],
        "educacion": ["EDUCACION", "EDUCATIVO", "UNIVERSIDAD", "DOCENTE", "MAESTRO", "ESCUELA", "COLEGIO", "ESTUDIANTE", "ACADEMICO", "SUNEDU", "MINEDU", "BECA"],
        "salud": ["SALUD", "HOSPITAL", "MEDICO", "SANITARIO", "ESSALUD", "MINSA", "VACUNA", "FARMACIA", "MEDICAMENTO", "SIS", "EMERGENCIA SANITARIA"],
        "seguridad": ["SEGURIDAD", "POLICIA", "FUERZAS ARMADAS", "MILITAR", "DEFENSA", "DELITO", "CRIMEN", "PENAL", "CIUDADANA"],
        "agricultura": ["AGRAR", "AGRICULT", "CAMPESINO", "RURAL", "COSECHA", "RIEGO", "AGROPECUARIO", "GANAD"],
        "economia": ["ECONOMIA", "FISCAL", "TRIBUTAR", "IMPUESTO", "PRESUPUESTO", "INVERSION", "MYPE", "EMPRESA", "SUNAT", "CREDITO"],
        "transporte": ["TRANSPORTE", "CARRETERA", "FERROCARRIL", "METRO", "BUS", "MTC", "VIA", "INFRAESTRUCTURA"],
        "agua": ["AGUA", "SANEAMIENTO", "DESAGUE", "POTABLE", "ALCANTARILLADO", "SUNASS"],
        "social": ["SOCIAL", "PENSION", "BONO", "SUBSIDIO", "PROGRAMA SOCIAL", "MIDIS", "PENSION 65", "JUNTOS"],
        "justicia": ["JUSTICIA", "JUDICIAL", "JUEZ", "FISCAL", "TRIBUNAL", "CORTE", "PROCESO"],
        "corrupcion": ["CORRUPCION", "TRANSPARENCIA", "FISCALIZACION", "CONTRALORIA", "CONTROL"],
        "ambiente": ["AMBIENTE", "AMBIENTAL", "FORESTAL", "BOSQUE", "CONTAMINACION", "ECOLOG", "CLIMA"],
        "vivienda": ["VIVIENDA", "CONSTRUCCION", "TECHO PROPIO", "URBANIZACION", "MVCS"],
        "mujer": ["MUJER", "GENERO", "VIOLENCIA.*MUJER", "FEMINICIDIO", "IGUALDAD"],
        "ninez": ["NINO", "NINA", "INFANCIA", "MENOR", "ADOLESCENTE"],
        "telecomunicaciones": ["INTERNET", "TELECOMUNICACION", "CONECTIVIDAD", "DIGITAL", "TECNOLOGIA"],
    }

    # Get relevant keywords for this category
    relevant_keywords = category_keywords.get(category, [])

    # Also add keywords from related categories
    related = {
        "empleo": ["economia", "social"],
        "educacion": ["ninez", "social"],
        "salud": ["social"],
        "social": ["empleo", "salud", "vivienda"],
    }
    for related_cat in related.get(category, []):
        relevant_keywords.extend(category_keywords.get(related_cat, []))

    # Count how many category keywords appear in the asunto
    keyword_matches = sum(1 for kw in relevant_keywords if kw in asunto)

    # Check if the matched keywords from the analysis actually appear
    analysis_keyword_matches = sum(1 for kw in keywords if kw and kw in asunto)

    # Scoring logic
    if keyword_matches >= 3 and analysis_keyword_matches >= 2:
        return 5, f"Strong match: {keyword_matches} category keywords, {analysis_keyword_matches} analysis keywords", True
    elif keyword_matches >= 2 and analysis_keyword_matches >= 1:
        return 4, f"Good match: {keyword_matches} category keywords, {analysis_keyword_matches} analysis keywords", True
    elif keyword_matches >= 1 and analysis_keyword_matches >= 1:
        return 3, f"Moderate match: {keyword_matches} category keywords, {analysis_keyword_matches} analysis keywords", True
    elif keyword_matches >= 1 or analysis_keyword_matches >= 1:
        return 2, f"Weak match: {keyword_matches} category keywords, {analysis_keyword_matches} analysis keywords - verify manually", True
    else:
        return 1, f"No keyword match found - likely false positive", False


def phase2_semantic_filter(contradictions: List[Contradiction]) -> Tuple[List[Contradiction], List[Contradiction]]:
    """Phase 2: Apply semantic relevance filtering."""
    valid = []
    filtered = []

    for c in contradictions:
        score, reasoning, is_valid = evaluate_semantic_relevance(c)
        c.relevance_score = score
        c.reasoning = reasoning

        if not is_valid:
            c.is_valid = False
            c.filter_reason = f"PHASE2_SEMANTIC: {reasoning}"
            filtered.append(c)
        else:
            valid.append(c)

    return valid, filtered


def main():
    """Main execution flow."""
    print("=" * 80)
    print("AMPAY Contradiction Filtering - Phases 1-3")
    print("=" * 80)

    # Find all party files
    party_files = list(DATA_DIR.glob("ampay_v4_*_FULL.json"))
    print(f"\nFound {len(party_files)} party files to process")

    # Extract all contradictions
    all_contradictions: List[Contradiction] = []

    for filepath in party_files:
        print(f"  Processing: {filepath.name}")
        contradictions = extract_contradictions_from_file(filepath)
        all_contradictions.extend(contradictions)
        print(f"    Found {len(contradictions)} contradictions")

    print(f"\nTotal raw contradictions: {len(all_contradictions)}")

    # Phase 1: Filter procedural
    print("\n" + "-" * 40)
    print("PHASE 1: Filtering procedural false positives")
    print("-" * 40)

    after_phase1, phase1_filtered = phase1_filter_procedural(all_contradictions)
    print(f"  Removed: {len(phase1_filtered)} procedural votes")
    print(f"  Remaining: {len(after_phase1)}")

    # Phase 2: Semantic relevance
    print("\n" + "-" * 40)
    print("PHASE 2: Semantic relevance filtering")
    print("-" * 40)

    after_phase2, phase2_filtered = phase2_semantic_filter(after_phase1)
    print(f"  Removed: {len(phase2_filtered)} semantically irrelevant")
    print(f"  Remaining: {len(after_phase2)}")

    # Combine all filtered for reference
    all_filtered = phase1_filtered + phase2_filtered

    # Phase 3: Generate output files
    print("\n" + "-" * 40)
    print("PHASE 3: Generating output files")
    print("-" * 40)

    # Sort by relevance score (highest first) then by party
    after_phase2.sort(key=lambda x: (-x.relevance_score, x.party, x.promise_id))

    # Generate JSON output
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "methodology": "AMPAY v4 Contradiction Filtering",
        "phases": [
            "Phase 1: Removed procedural votes (EXONERACION, CUESTION PREVIA, RECONSIDERACION, ADMISION A DEBATE)",
            "Phase 2: Semantic relevance scoring (1-5 scale, filtered score=1 false positives)",
        ],
        "statistics": {
            "total_raw_contradictions": len(all_contradictions),
            "phase1_removed": len(phase1_filtered),
            "phase2_removed": len(phase2_filtered),
            "total_valid_for_review": len(after_phase2),
        },
        "score_distribution": {
            5: sum(1 for c in after_phase2 if c.relevance_score == 5),
            4: sum(1 for c in after_phase2 if c.relevance_score == 4),
            3: sum(1 for c in after_phase2 if c.relevance_score == 3),
            2: sum(1 for c in after_phase2 if c.relevance_score == 2),
        },
        "by_party": {},
        "contradictions": [asdict(c) for c in after_phase2],
        "filtered_out": [asdict(c) for c in all_filtered],
    }

    # Count by party
    for c in after_phase2:
        if c.party not in output_data["by_party"]:
            output_data["by_party"][c.party] = {"total": 0, "type_A": 0, "type_B": 0}
        output_data["by_party"][c.party]["total"] += 1
        if c.contradiction_type == "A":
            output_data["by_party"][c.party]["type_A"] += 1
        else:
            output_data["by_party"][c.party]["type_B"] += 1

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"  JSON output: {OUTPUT_JSON}")

    # Generate CSV output
    csv_columns = [
        "party", "promise_id", "promise_text", "promise_category",
        "law_date", "law_asunto", "party_vote", "expected_vote",
        "contradiction_type", "relevance_score", "reasoning"
    ]

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for c in after_phase2:
            writer.writerow({
                "party": c.party,
                "promise_id": c.promise_id,
                "promise_text": c.promise_text[:200] + "..." if len(c.promise_text) > 200 else c.promise_text,
                "promise_category": c.promise_category,
                "law_date": c.law_date,
                "law_asunto": c.law_asunto[:300] + "..." if len(c.law_asunto) > 300 else c.law_asunto,
                "party_vote": c.party_vote,
                "expected_vote": c.expected_vote,
                "contradiction_type": c.contradiction_type,
                "relevance_score": c.relevance_score,
                "reasoning": c.reasoning,
            })
    print(f"  CSV output: {OUTPUT_CSV}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total contradictions found: {len(all_contradictions)}")
    print(f"Filtered out (procedural): {len(phase1_filtered)}")
    print(f"Filtered out (semantic): {len(phase2_filtered)}")
    print(f"VALID FOR MANUAL REVIEW: {len(after_phase2)}")
    print("\nBy Party:")
    for party, stats in sorted(output_data["by_party"].items()):
        print(f"  {party}: {stats['total']} (Type A: {stats['type_A']}, Type B: {stats['type_B']})")
    print("\nBy Relevance Score:")
    for score in [5, 4, 3, 2]:
        count = output_data["score_distribution"][score]
        print(f"  Score {score}: {count}")

    print("\n" + "=" * 80)
    print("FILES GENERATED:")
    print(f"  1. {OUTPUT_JSON}")
    print(f"  2. {OUTPUT_CSV}")
    print("=" * 80)


if __name__ == "__main__":
    main()
