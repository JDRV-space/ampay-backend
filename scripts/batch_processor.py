#!/usr/bin/env python3
"""
Batch processor for promise extraction.
Processes pages and generates promise extraction JSON output for manual review.
"""

import os
import sys
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Points to repo root
DATA_DIR = BASE_DIR / "data"
PAGES_DIR = DATA_DIR / "pdfs" / "pages"
PROCESSING_DIR = DATA_DIR / "processing"
PROMISES_DIR = DATA_DIR / "promises"

PARTIES = [
    {"name": "Peru Libre", "slug": "peru_libre", "code": "PL"},
    {"name": "Fuerza Popular", "slug": "fuerza_popular", "code": "FP"},
    {"name": "Alianza para el Progreso", "slug": "alianza_progreso", "code": "APP"},
    {"name": "Renovacion Popular", "slug": "renovacion_popular", "code": "RP"},
    {"name": "Avanza Pais", "slug": "avanza_pais", "code": "APAIS"},
    {"name": "Podemos Peru", "slug": "podemos_peru", "code": "PP"},
    {"name": "Juntos por el Peru", "slug": "juntos_peru", "code": "JP"},
    {"name": "Somos Peru", "slug": "somos_peru", "code": "SP"},
    {"name": "Partido Morado", "slug": "partido_morado", "code": "PM"}
]

VALID_CATEGORIES = [
    "seguridad", "economia", "fiscal", "social", "empleo",
    "educacion", "salud", "agua", "vivienda", "transporte",
    "energia", "mineria", "ambiente", "agricultura", "justicia"
]

def get_party_info(party_slug):
    for p in PARTIES:
        if p["slug"] == party_slug:
            return p
    return None

def process_all_pages_for_party_year(party_slug, year):
    """Read all pages for a party/year and return combined content."""
    pages_dir = PAGES_DIR / f"{party_slug}_{year}"
    if not pages_dir.exists():
        return None, 0

    page_files = sorted(pages_dir.glob("page_*.txt"))
    all_text = ""

    for page_file in page_files:
        page_num = int(page_file.stem.split("_")[1])
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        all_text += f"\n\n=== PAGE {page_num} ===\n\n{content}"

    return all_text, len(page_files)

def extract_promises_keywords(text):
    """Extract potential promises using keyword patterns - for pre-filtering."""
    action_patterns = [
        r"(?:vamos a|se va a|proponemos|prometemos|nos comprometemos a|implementaremos|crearemos|construiremos|eliminaremos|aumentaremos|reduciremos|fortaleceremos|impulsaremos|garantizaremos|promoveremos|estableceremos)",
        r"(?:crear|eliminar|aumentar|reducir|construir|implementar|modificar|fortalecer|impulsar|garantizar|promover|establecer|reformar|mejorar|desarrollar)\s+",
    ]

    sentences = re.split(r'[.;]', text)
    potential_promises = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue
        for pattern in action_patterns:
            if re.search(pattern, sentence.lower()):
                potential_promises.append(sentence[:500])
                break

    return potential_promises

def get_text_summary(text, max_chars=2000):
    """Get a summary portion of text."""
    # Get first portion
    if len(text) <= max_chars:
        return text

    # Get beginning, middle, and end samples
    third = max_chars // 3
    beginning = text[:third]
    middle_start = len(text) // 2 - third // 2
    middle = text[middle_start:middle_start + third]
    end = text[-third:]

    return f"{beginning}\n\n[...MIDDLE SECTION...]\n\n{middle}\n\n[...END SECTION...]\n\n{end}"

def print_party_year_overview(party_slug, year):
    """Print an overview of a party/year for analysis."""
    party = get_party_info(party_slug)
    if not party:
        print(f"Unknown party: {party_slug}")
        return

    text, page_count = process_all_pages_for_party_year(party_slug, year)
    if not text:
        print(f"No pages found for {party_slug}_{year}")
        return

    # Get potential promises through keyword extraction
    potential = extract_promises_keywords(text)

    print(f"Party: {party['name']}")
    print(f"Year: {year}")
    print(f"Code: {party['code']}")
    print(f"Total pages: {page_count}")
    print(f"Total characters: {len(text)}")
    print(f"Potential promise sentences: {len(potential)}")
    print("\n" + "="*60)
    print("TEXT SAMPLE:")
    print("="*60)
    print(get_text_summary(text, 6000))

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python batch_processor.py overview <party_slug> <year>")
        print("  python batch_processor.py full <party_slug> <year>")
        print("  python batch_processor.py list")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        for party in PARTIES:
            for year in [2021, 2026]:
                pages_dir = PAGES_DIR / f"{party['slug']}_{year}"
                if pages_dir.exists():
                    page_count = len(list(pages_dir.glob("page_*.txt")))
                    promises_file = PROMISES_DIR / f"{party['slug']}_{year}.json"
                    status = "DONE" if promises_file.exists() else "PENDING"
                    print(f"{party['slug']}_{year}: {page_count} pages [{status}]")

    elif cmd == "overview" and len(sys.argv) >= 4:
        party_slug = sys.argv[2]
        year = int(sys.argv[3])
        print_party_year_overview(party_slug, year)

    elif cmd == "full" and len(sys.argv) >= 4:
        party_slug = sys.argv[2]
        year = int(sys.argv[3])
        text, page_count = process_all_pages_for_party_year(party_slug, year)
        if text:
            print(text)

if __name__ == "__main__":
    main()
