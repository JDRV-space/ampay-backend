# Keyword-Based Vote Classification

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

Algorithm that categorizes 2,226 congressional votes into 15 thematic categories using keyword matching on the vote subject text.

---

## 1. Overview

The keyword classification algorithm assigns each of the 2,226 substantive votes to one of 15 thematic categories. It works by comparing the "asunto" (subject) text of each vote against predefined keyword dictionaries.

The process is fully deterministic: it uses no language models or complex heuristics. Each vote receives a primary category, an optional secondary category, a vote type, and a confidence score.

**Key data:**
- 2,226 votes classified
- 15 thematic categories
- Substring matching on lowercase text
- Confidence between 0.50 and 0.95

---

## 2. The 15 Categories

Each category has a keyword dictionary. The system searches for exact matches (substring) in the vote subject converted to lowercase.

| Category | Keywords (examples) | Description |
|---|---|---|
| **seguridad** | `delincuencia, policia, crimen, seguridad ciudadana, terrorismo` | Public order, police, terrorism |
| **economia** | `economia, comercio, exportacion, importacion, empresa` | Commerce, businesses, exports |
| **fiscal** | `presupuesto, tributo, impuesto, igv, renta, sunat` | Budget, taxes, tributes |
| **social** | `pobreza, inclusion, discapacidad, adulto mayor, pension` | Inclusion, disability, pensions |
| **empleo** | `trabajo, empleo, laboral, trabajador, sueldo` | Labor, wages, workers rights |
| **educacion** | `educacion, universidad, escolar, estudiante` | Universities, schools, students |
| **salud** | `salud, hospital, medico, essalud, sis` | Hospitals, doctors, health insurance |
| **agua** | `agua, saneamiento, desague, sunass` | Sanitation, drainage, water resources |
| **vivienda** | `vivienda, urbanismo, inmueble, construccion` | Urban planning, real estate, construction |
| **transporte** | `transporte, carretera, ferroviario, aeropuerto` | Highways, railways, airports |
| **energia** | `energia, electricidad, gas, petroleo` | Electricity, gas, petroleum |
| **mineria** | `mineria, minas, canon minero, regalias mineras` | Mining, mining canon, royalties |
| **ambiente** | `ambiente, ambiental, contaminacion, deforestacion` | Pollution, deforestation, ecology |
| **agricultura** | `agricultura, agropecuario, campesino` | Agriculture, farmers, irrigation |
| **justicia** | `justicia, judicial, fiscal, juez, congreso` | Judiciary, judges, prosecutors |

---

## 3. Scoring Algorithm

For each vote, the algorithm iterates over all 15 categories and counts how many keywords from each appear in the subject text. The category with the highest score wins.

### 3.1 Pseudocode

```python
def classify_vote_by_keywords(asunto):
    asunto_lower = asunto.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in asunto_lower)
        scores[category] = score

    sorted_scores = sorted(
        scores.items(), key=lambda x: x[1], reverse=True
    )

    best_category = sorted_scores[0][0] \
        if sorted_scores[0][1] > 0 else "justicia"

    secondary = sorted_scores[1][0] \
        if sorted_scores[1][1] > 0 else None

    max_score = sorted_scores[0][1]
    confidence = min(0.95, 0.5 + (max_score * 0.15))

    return {
        "category": best_category,
        "secondary_category": secondary,
        "confidence": confidence,
        "scores": scores
    }
```

### 3.2 Practical Example

For a vote with subject: "Law modifying the public safety and national police budget"

| Category | Keywords | Score | Result |
|---|---|---|---|
| **seguridad** | `seguridad ciudadana, policia` | **2** | **PRIMARY** |
| **fiscal** | `presupuesto` | **1** | **SECONDARY** |
| economia | - | 0 | - |
| social | - | 0 | - |
| *(11 more)* | - | 0 | - |

**Result:** category = "seguridad", secondary = "fiscal", confidence = min(0.95, 0.5 + 2*0.15) = 0.80

---

## 4. Secondary Category

In addition to the primary category (highest score), the algorithm saves the second-highest scoring category as "secondary category". This enables analysis of votes that span multiple topics.

The secondary category is only assigned if its score is greater than 0. If only one category has matches, there is no secondary.

### 4.1 Use in Analysis

The secondary category allows:

- Identifying votes that cross topics (e.g., "security" + "fiscal")
- Detecting multi-sector legislation
- Enriching the thematic analysis on the By Topic page

```python
sorted_scores = sorted(
    scores.items(), key=lambda x: x[1], reverse=True
)

secondary = sorted_scores[1][0] \
    if sorted_scores[1][1] > 0 else None
```

---

## 5. Vote Type Detection

In addition to the thematic category, the algorithm classifies each vote into one of three types: substantive, procedural, or declarative. This classification uses separate keyword lists.

### 5.1 Procedural Keywords

```python
PROCEDURAL_KEYWORDS = [
    "cuestion de orden",
    "reglamento",
    "mocion de orden",
    "dispensa",
    "reconsideracion",
    "cuestion previa",
    "orden del dia",
    "ampliacion de agenda",
    "votacion en bloque"
]
```

### 5.2 Declarative Keywords

```python
DECLARATIVE_KEYWORDS = [
    "declarar de interes nacional",
    "declarar heroe",
    "declarar patrimonio",
    "homenaje",
    "interes nacional",
    "saludo por",
    "reconocimiento a",
    "dia nacional de",
    "dia del"
]
```

### 5.3 Assignment Logic

If the subject contains any procedural keyword, it is marked as "procedural". If it contains any declarative keyword, it is marked as "declarative". Otherwise, the default type is "substantive".

```python
vote_type = "sustantivo"  # default

if any(kw in asunto_lower for kw in PROCEDURAL_KEYWORDS):
    vote_type = "procedural"
elif any(kw in asunto_lower for kw in DECLARATIVE_KEYWORDS):
    vote_type = "declarativo"
```

---

## 6. Confidence Formula

The confidence score reflects the certainty of the classification. It is calculated from the maximum score obtained:

```
confidence = min(0.95, 0.5 + (max_score * 0.15))
```

### 6.1 Confidence Table

| Max Score | Confidence | Interpretation |
|---|---|---|
| 0 | 0.50 | No matches (default "justicia") |
| 1 | 0.65 | Low - single match |
| 2 | 0.80 | Moderate - two matches |
| 3 | 0.95 | High - three matches |
| 4+ | 0.95 | Very high - four or more matches |

### 6.2 Maximum Cap

Confidence never exceeds 0.95 because the keyword method has inherent limitations. Even with many matches, 100% accuracy cannot be guaranteed without semantic understanding.

> **Note:** A score of 3 already reaches the 0.95 cap. Scores of 4, 5 or more do not increase confidence.

---

## 7. Default Category

When no dictionary has matches (max score = 0), the vote is assigned to the "justicia" category as a default value.

```python
best_category = max(scores, key=scores.get) \
    if max(scores.values()) > 0 else "justicia"

# confidence = 0.50 (score 0 -> 0.5 + 0*0.15 = 0.50)
```

### 7.1 Justification

- **Parliamentary context:** Votes without matches tend to be about legislative procedures that naturally fall under "justicia" (state organs, congressional functions)
- **Frequency:** Approximately 12% of votes receive the default category
- **Manual review:** Votes with the default category can be easily identified by their 0.50 confidence score

---

## 8. Limitations

- **No semantic understanding:** Substring matching does not understand context. "police" in "police law" and "history of police" score equally
- **Ambiguous votes:** Multi-topic votes may be incorrectly classified if the secondary category was the correct one
- **Fixed dictionaries:** Keywords are not automatically updated. New legislative topics might not be covered
- **Unresolved ties:** If two categories have the same score, Python max() picks the first by dictionary order, not by relevance
- **Synonym sensitivity:** If Congress uses terminology different from the dictionary, classification fails silently

---

## 9. Related Files

| File | Content |
|---|---|
| `scripts/phase_1_3_vote_classification.py` | Keyword classification script |
| `data/02_output/votes_categorized.json` | Categorized votes with metadata |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
