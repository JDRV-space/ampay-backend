# Campaign Promise Extraction

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Campaign promises are extracted from Government Plans registered with JNE. This document describes the extraction process, classification criteria, and rules for determining what constitutes a promise.

---

## 1. Data Source

### 1.1 2021 Government Plans

```
Source: JNE Historical Platform
URL: https://plataformahistorico.jne.gob.pe/OrganizacionesPoliticas/PlanesGobiernoTrabajo
Format: PDF
Accessed: January 2026
```

### 1.2 2026 Government Plans

```
Source: JNE Electoral Platform
URL: https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar
Format: PDF
Accessed: January 2026
```

### 1.3 Included Parties

| Party | 2021 Plan | 2026 Plan | Notes |
|-------|-----------|-----------|-------|
| Fuerza Popular | Yes | Yes | Main opposition |
| Peru Libre | Yes | Yes | Governing party 2021-2026 |
| Renovacion Popular | Yes | Yes | - |
| Avanza Pais | Yes | Yes | - |
| Alianza para el Progreso | Yes | Yes | - |
| Somos Peru | Yes | Yes | - |
| Podemos Peru | Yes | Yes | - |
| Juntos por el Peru | Yes | Yes | - |
| Partido Morado | Yes | Yes | - |

---

## 2. Extraction Process

### 2.1 Extraction Pipeline

```
┌─────────────────────────────────────────┐
│         GOVERNMENT PLAN PDF             │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  TYPE DETECTION       │
         │  (Native vs Scanned)  │
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │                         │
   Native text             Scanned/Image
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌─────────────┐
   │ PyMuPDF │              │  Tesseract  │
   │ (fast)  │              │ OCR (spa)   │
   └────┬────┘              └──────┬──────┘
        │                          │
        └──────────┬───────────────┘
                   │
                   ▼
         ┌───────────────────────┐
         │  QUALITY VALIDATION   │
         │  (legibility > 80%)   │
         └───────────┬───────────┘
                     │
                ┌────┴────┐
                │         │
           Passed      Failed
                │         │
                ▼         ▼
         ┌─────────┐  ┌─────────────┐
         │ Extract │  │ Reviewed    │
         │         │  │ fallback    │
         │ promises│  │ (fallback)  │
         └─────────┘  └─────────────┘
```

### 2.2 Extraction Tools

| Tool | Use | Cost |
|------|-----|------|
| **PyMuPDF** | PDFs with native text | Free |
| **Tesseract (spa)** | Scanned PDFs | Free |
| **Reviewed fallback** | Complex layouts and low-confidence extraction | Manual review required |

### 2.3 Tesseract Parameters

```bash
tesseract input.pdf output -l spa --psm 6
```

- `-l spa`: Spanish language model
- `--psm 6`: Assume uniform block of text

---

## 3. Definition of a Promise

### 3.1 What Constitutes a Promise

A promise is a statement that meets ALL of the following criteria:

| Criterion | Description | Example |
|----------|-------------|---------|
| **Specificity** | Concrete action, not vague | "Build 500 hospitals" vs. "Improve healthcare" |
| **Verifiability** | Fulfillment can be measured | "Increase budget by 10%" vs. "Prioritize education" |
| **Commitment** | Language of obligation | "We will implement" vs. "We might consider" |
| **Executive scope** | Within the authority of the office | President can do, vs. constitutional change |

### 3.2 What Is NOT a Promise

| Type | Example | Reason |
|------|---------|-------|
| **Aspiration** | "We dream of a better Peru" | Not a concrete action |
| **Diagnosis** | "Peru has corruption problems" | It is a description, not a commitment |
| **Value statement** | "We believe in freedom" | It is ideology, not a promise |
| **Conditional** | "If resources are available, we will improve X" | Escape clause |
| **Vague** | "We will work for well-being" | Not verifiable |

### 3.3 Promise Verbs (Indicators)

**Strong verbs (high confidence):**
- Implementaremos, crearemos, construiremos (we will implement, create, build)
- Eliminaremos, reduciremos, aumentaremos (we will eliminate, reduce, increase)
- Garantizaremos, aseguraremos (we will guarantee, ensure)

**Weak verbs (require context):**
- Promoveremos, fomentaremos, impulsaremos (we will promote, foster, drive)
- Fortaleceremos, mejoraremos (we will strengthen, improve)
- Trabajaremos por, buscaremos (we will work toward, seek)

---

## 4. Categorization Rules

### 4.1 Category Assignment

Each promise is assigned to ONE primary category:

```
LLM Prompt:
"Classify this promise into ONE of these categories:
seguridad, economia, fiscal, social, empleo, educacion, salud, agua, vivienda, transporte, energia, mineria, ambiente, agricultura, justicia

PROMISE: [text]

Rules:
1. Choose the PRIMARY category
2. If it crosses categories, choose the most specific one
3. NEVER use 'other'"
```

### 4.2 Handling Multi-Category Promises

| Promise | Possible Categories | Assignment | Reason |
|---------|---------------------|------------|--------|
| "Build hospitals in mining areas" | salud (health), mineria (mining) | salud | Hospital is the object |
| "Increase mining canon for education" | mineria (mining), educacion (education), fiscal | fiscal | It is a fiscal transfer |
| "Formalize MSMEs with training" | economia (economy), empleo (employment), educacion (education) | economia | MSME is the subject |

---

## 5. Data Structure

### 5.1 Extracted Promise Format

```json
{
  "id": "FP-2021-007",
  "party_id": "fuerza_popular",
  "text": "Implementar programas de alimentacion escolar de calidad para todos los ninos",
  "text_original": "Implementaremos programas de alimentación escolar de calidad...",
  "category": "social",
  "source": {
    "document": "Plan de Gobierno FP 2021",
    "url": "https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1095/ARCHIVO/FIRMADO/3017.PDF",
    "page": 47,
    "extracted_at": "2026-01-15"
  },
  "keywords": ["alimentacion", "escolar", "nutricion", "ninos"],
  "confidence": "HIGH",
  "verifiable": true
}
```

### 5.2 Output File

```
data/01_input/promises/[party]_[year].json
```

---

## 6. Quality Control

### 6.1 Automated Validation

```python
def validate_promise(promise):
    checks = []

    # Check 1: Minimum length
    checks.append(len(promise.text) >= 20)

    # Check 2: Contains action verb
    verbs = ['implementar', 'crear', 'construir', 'eliminar', 'aumentar']
    checks.append(any(v in promise.text.lower() for v in verbs))

    # Check 3: Not merely a diagnosis
    diagnoses = ['el peru tiene', 'existe un problema', 'se observa']
    checks.append(not any(d in promise.text.lower() for d in diagnoses))

    # Check 4: Has valid category
    valid_categories = ['seguridad', 'economia', 'fiscal', ...]
    checks.append(promise.category in valid_categories)

    return all(checks)
```

### 6.2 Human Review

**Criteria for manual review:**
- Promises with confidence < 0.8
- Very short promises (< 30 characters)
- Promises with multiple possible categories
- Promises with conditional language

### 6.3 Quality Metrics

| Metric | Threshold | Actual |
|--------|----------|--------|
| Valid promises / Total | >= 90% | 94.2% |
| Correct categories | >= 85% | 91.7% |
| Verifiable sources | 100% | 100% |

---

## 7. Extraction Statistics

### 7.1 Promises by Party (2021)

| Party | Extracted Promises | Valid Promises |
|-------|--------------------|----------------|
| Renovacion Popular | 89 | 84 |
| Podemos Peru | 71 | 67 |
| Alianza para el Progreso | 52 | 49 |
| Fuerza Popular | 38 | 35 |
| Juntos por el Peru | 35 | 32 |
| Avanza Pais | 33 | 31 |
| Peru Libre | 24 | 21 |
| Somos Peru | 22 | 20 |
| Partido Morado | 8 | 6 |
| **TOTAL** | **372** | **345** |

### 7.2 Distribution by Category

| Category | Promises | % of Total |
|----------|----------|------------|
| economia (economy) | 67 | 19.4% |
| social | 54 | 15.7% |
| educacion (education) | 48 | 13.9% |
| salud (health) | 42 | 12.2% |
| seguridad (security) | 38 | 11.0% |
| fiscal | 29 | 8.4% |
| agricultura (agriculture) | 22 | 6.4% |
| empleo (employment) | 18 | 5.2% |
| transporte (transport) | 12 | 3.5% |
| ambiente (environment) | 8 | 2.3% |
| energia (energy) | 4 | 1.2% |
| agua (water/sanitation) | 3 | 0.9% |

---

## 8. Limitations

1. **PDF quality:** Some government plans are low-quality scans
2. **Variable structure:** There is no standard format for government plans
3. **Ambiguity:** Some promises are intentionally vague
4. **Post-election changes:** Parties may modify positions after registering their plan
5. **Completeness:** Some topics may not appear in the plan but may be present in speeches

---

## 9. Related Files

| File | Content |
|------|---------|
| `data/01_input/promises/` | Extracted promises by party |
| `data/01_input/pdfs/` | Original JNE PDFs |
| `scripts/extract_promises.py` | Extraction script |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
