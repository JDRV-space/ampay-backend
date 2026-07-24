# Filtering of Parliamentary Votes

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Not all congressional votes carry equal relevance for political analysis. This document describes the criteria for filtering substantive votes from procedural and declarative ones.

---

## 1. Vote Types

### 1.1 Tripartite Classification

| Type | Definition | Included in Analysis |
|------|-----------|---------------------|
| **Substantive** | Votes on legislation with real political impact | **YES** |
| **Procedural** | Votes on legislative mechanics | NO |
| **Declarative** | Symbolic votes with no legal effect | NO |

### 1.2 Examples by Type

**SUBSTANTIVE (include):**
```
- "Law amending the Penal Code"
- "Public Sector Budget 2024"
- "Pension system reform law"
- "Supplementary credit for the health sector"
```

**PROCEDURAL (exclude):**
```
- "Order of the day motion"
- "Approval of previous session minutes"
- "Preliminary question"
- "Point of order"
- "Waiver of second vote"
- "Agenda expansion"
```

**DECLARATIVE (exclude):**
```
- "Declare the Festival of X to be of national interest"
- "Declare Y a national hero"
- "Greeting on the day of Z"
- "Recognition of the work of..."
```

---

## 2. Filtering Criteria

### 2.1 Automatic Exclusion Rules

**By keywords in subject:**

```python
EXCLUDE_IF_CONTAINS = [
    # Procedural
    "orden del dia",
    "acta de sesion",
    "cuestion previa",
    "cuestion de orden",
    "dispensa de",
    "ampliacion de agenda",
    "reconsideracion",
    "votacion en bloque",

    # Declarative
    "declarar de interes nacional",
    "declarar heroe",
    "declarar patrimonio",
    "saludo por",
    "reconocimiento a",
    "dia nacional de",
    "dia del",
    "semana de",
    "mes de",
    "año de"
]
```

### 2.2 Forced Inclusion Rules

Even if exclusion keywords are present, INCLUDE if:

```python
INCLUDE_IF_CONTAINS = [
    "ley",
    "proyecto de ley",
    "presupuesto",
    "credito suplementario",
    "decreto",
    "reforma",
    "modificacion",
    "deroga"
]
```

### 2.3 Decision Matrix

| Contains Exclusion | Contains Inclusion | Result |
|--------------------|--------------------|--------|
| NO | YES | **INCLUDE** |
| NO | NO | **INCLUDE** (default) |
| YES | NO | **EXCLUDE** |
| YES | YES | **MANUAL REVIEW** |

---

## 3. Classification Process

### 3.1 Automated Pipeline

```
┌─────────────────────────────────────────┐
│         VOTE SUBJECT                    │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  EXCLUSION RULES      │
         │  (keywords)           │
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   No match     Excl match   Both match
        │            │            │
        ▼            │            ▼
   ┌─────────┐       │      ┌───────────┐
   │ INCLUDE │       │      │ MANUAL    │
   │ as      │       │      │ REVIEW    │
   │substantive│     │      └───────────┘
   └─────────┘       │
                     ▼
         ┌───────────────────────┐
         │  INCLUSION RULES      │
         │  (keywords)           │
         └───────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   Incl match               No match
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌─────────┐
   │ INCLUDE │              │ EXCLUDE │
   │ as      │              │ as      │
   │substantive│            │ declarative/
   └─────────┘              │ procedural │
                            └─────────┘
```

### 3.2 Assisted Review

For ambiguous cases, use assisted review and manual validation:

```
Prompt:
"Classify this Peruvian Congress vote subject:

SUBJECT: [text]

Classification (choose ONE):
1. SUBSTANTIVE - Law or decision with real political impact
2. PROCEDURAL - Legislative mechanics with no political content
3. DECLARATIVE - Symbolic recognition with no legal effect

Respond ONLY with: SUBSTANTIVE, PROCEDURAL, or DECLARATIVE"
```

---

## 4. Filtering Statistics

### 4.1 Filtering Results (2021-2024)

| Type | Count | % of Total |
|------|-------|------------|
| **Substantive** | 2,226 | 62.4% |
| Procedural | 847 | 23.8% |
| Declarative | 497 | 13.9% |
| **TOTAL** | 3,570 | 100% |

### 4.2 Declarative Votes by Year

| Year | Declarative | % of Year | Notes |
|------|-------------|-----------|-------|
| 2021 | 89 | 11.2% | Start of legislature |
| 2022 | 142 | 14.8% | Normal |
| 2023 | 178 | 15.6% | Pre-electoral increase |
| 2024 | 88 | 12.1% | Partial (through July) |

**Source:** Ojo Publico analysis on declarative bills: [URL](https://ojo-publico.com/4925/congresistas-impulsaron-497-proyectos-ley-declarativos-el-2023)

---

## 5. Justification for Exclusions

### 5.1 Why Exclude Declarative Votes

1. **No legal force:** They do not create obligations or rights
2. **No budget impact:** They do not allocate resources
3. **Pattern distortion:** They artificially inflate the "YES" percentage
4. **Universally approved:** Almost always pass by unanimity

**Example of distortion:**
```
Unfiltered: FP 96% YES (includes 200 declarative votes)
Filtered:   FP 89% YES (substantive only)
```

### 5.2 Why Exclude Procedural Votes

1. **Do not reflect political position:** They are session mechanics
2. **Lost context:** A "preliminary question" can be a tactic
3. **High frequency:** They artificially inflate the vote count
4. **Irrelevant to promises:** Cannot be linked to campaign commitments

---

## 6. Special Cases

### 6.1 Censure/Vacancy Motions

**Classification:** SUBSTANTIVE

**Reason:** High political impact, even though they are technically "motions."

```
INCLUDE:
- "Censure motion against Minister X"
- "Presidential vacancy motion"
- "Interpellation motion"
```

### 6.2 Investigative Commissions

**Classification:** SUBSTANTIVE

**Reason:** They reflect a position on oversight.

```
INCLUDE:
- "Creation of investigative commission on X"
- "Final report of investigative commission"
```

### 6.3 Appointments

**Classification:** SUBSTANTIVE (if a position of power)

```
INCLUDE:
- "Appointment of Constitutional Tribunal members"
- "Appointment of Ombudsman"
- "Appointment of Comptroller General"

EXCLUDE:
- "Appointment of ceremonial representative"
```

---

## 7. Filtering Validation

### 7.1 Verification Sample

Manually review 5% of filtered votes:

| Category | Sample | Correct | Accuracy |
|----------|--------|---------|----------|
| Substantive | 111 | 108 | 97.3% |
| Procedural | 42 | 40 | 95.2% |
| Declarative | 25 | 24 | 96.0% |

### 7.2 Common Errors

| Error | Frequency | Solution |
|-------|-----------|----------|
| Declarative classified as substantive | 2.1% | Add keywords |
| Substantive excluded by false positive keyword | 0.8% | Inclusion rules |
| Ambiguous procedural | 3.2% | Assisted review for disambiguation |

---

## 8. Limitations

1. **Availability bias:** Only analyzes what reaches a vote
2. **Lost context:** We do not know if an exclusion was strategic
3. **Granularity:** Some substantive votes contain declarative sections
4. **Evolution:** New vote types may not be covered

---

## 9. Related Files

| File | Content |
|------|---------|
| `data/02_output/votes_categorized.json` | Filtered votes with category |
| `scripts/filter_votes.py` | Filtering script |
| `data/02_output/votes_categorized.json` | Categorized votes (audit) |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
