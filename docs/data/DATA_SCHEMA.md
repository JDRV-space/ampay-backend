# JSON Data Schema

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

This document defines the structure of the JSON files used in AMPAY, following open data standards where applicable.

---

## 1. Adopted Standards

### 1.1 References

| Standard | Usage | URL |
|----------|-------|-----|
| Popolo | Party/organization structure | https://www.popoloproject.com/specs/ |
| Open Civic Data | IDs and relationships | https://open-civic-data.readthedocs.io/ |
| Schema.org ClaimReview | AMPAYs | https://schema.org/ClaimReview |

### 1.2 Conventions

| Convention | Example |
|------------|---------|
| snake_case for fields | `party_slug`, `vote_date` |
| ISO 8601 for dates | `2026-01-21` |
| Slugs for IDs | `fuerza_popular`, `peru_libre` |
| Percentages as float | `93.1` (not "93.1%") |

---

## 2. quiz_statements.json

### 2.1 Purpose

Contains quiz questions, party positions, and calibration configuration.

### 2.2 Location

```
data/02_output/quiz_statements.json
```

### 2.3 Schema

```json
{
  "version": "string",
  "created": "date",
  "updated": "date",
  "methodology": "string",
  "methodology_reference": "string",

  "party_display_names": {
    "[party_slug]": "string"
  },

  "calibration_questions": {
    "description": "string",
    "purpose": "string",
    "input_method": "string",
    "questions": [
      {
        "id": "string",
        "text": "string",
        "options": ["string"],
        "maps_to_parties": {
          "[option]": ["party_slug"]
        },
        "filter_logic": {
          "rank_1": "string",
          "rank_2": "string",
          "rank_3": "string"
        }
      }
    ]
  },

  "statements": [
    {
      "id": "string",
      "category": "string",
      "axis": "economic|social|governance",
      "text": "string",
      "simple_text": "string",
      "source_promises": ["string"],
      "positions": {
        "[party_slug]": -1|0|1
      },
      "note": "string (optional)"
    }
  ],

  "scale": {
    "user_input": {
      "1": "string",
      "0": "string",
      "-1": "string"
    },
    "party_position": {
      "1": "string",
      "0": "string",
      "-1": "string"
    }
  },

  "algorithm": {
    "method": "string",
    "formula": "string",
    "interpretation": "string",
    "percentage_formula": "string"
  }
}
```

### 2.4 Example

```json
{
  "version": "2.1",
  "statements": [
    {
      "id": "Q01",
      "category": "fiscal",
      "axis": "economic",
      "text": "Las grandes empresas deben pagar mas impuestos",
      "simple_text": "Mas impuestos a grandes empresas",
      "source_promises": ["JP-2026-002"],
      "positions": {
        "fuerza_popular": -1,
        "peru_libre": 1,
        "renovacion_popular": -1
      }
    }
  ]
}
```

---

## 3. ampays.json

### 3.1 Purpose

Contains confirmed AMPAYs with detailed evidence.

### 3.2 Location

```
data/02_output/ampays.json
```

### 3.3 Schema

```json
{
  "version": "string",
  "generated_at": "datetime",
  "source": "string",
  "total": "integer",

  "by_party": {
    "[party_slug]": "integer"
  },

  "ampays": [
    {
      "id": "string",
      "party_slug": "string",
      "party_name": "string",
      "promise": "string",
      "category": "string",
      "vote_position": "SI|NO",
      "expected_position": "SI|NO",
      "evidence": "string",
      "key_laws": ["string"],
      "vote_references": [
        {
          "vote_id": "string",
          "label": "string",
          "vote_type": "sustantivo|declarativo|procedural",
          "party_position": "SI|NO|DIVIDED|NO_DATA",
          "expected_position": "SI|NO"
        }
      ],
      "reasoning": "string",
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],

  "data_disclaimer": {
    "coverage": "string",
    "missing": "string",
    "note": "string"
  }
}
```

### 3.4 Example

```json
{
  "total": 5,
  "ampays": [
    {
      "id": "AMPAY-001",
      "party_slug": "fuerza_popular",
      "party_name": "Fuerza Popular",
      "promise": "Implementar reforma tributaria con principio de universalidad",
      "category": "fiscal",
      "vote_position": "SI",
      "expected_position": "NO",
      "evidence": "Voto SI en 6 leyes que extienden regimenes especiales",
      "key_laws": [
        "PL 3740 - Prorrogar apendices IGV",
        "PL 3195 - Devolucion IGV mineras/hidrocarburos"
      ],
      "vote_references": [
        {
          "vote_id": "2022-12-21T18-06",
          "label": "PL 3740 - Prorrogar apendices IGV",
          "vote_type": "sustantivo",
          "party_position": "SI",
          "expected_position": "NO"
        }
      ],
      "reasoning": "Prometio universalidad pero voto SI en leyes de regimenes especiales",
      "confidence": "HIGH"
    }
  ]
}
```

---

## 4. votes_categorized.json

### 4.1 Purpose

Contains all substantive votes with assigned categories.

### 4.2 Location

```
data/02_output/votes_categorized.json
```

### 4.3 Schema

```json
{
  "metadata": {
    "generated_at": "datetime",
    "total_votes": "integer",
    "period": {
      "start": "date",
      "end": "date"
    },
    "source": "string"
  },

  "votes": [
    {
      "id": "string",
      "date": "date",
      "asunto": "string",
      "category": "string",
      "vote_type": "sustantivo|declarativo|procedural",
      "result": "aprobado|rechazado",
      "totals": {
        "favor": "integer",
        "contra": "integer",
        "abstencion": "integer",
        "ausente": "integer"
      },
      "party_positions": {
        "[party_slug]": {
          "position": "SI|NO|DIVIDIDO|AUSENTE",
          "votes_favor": "integer",
          "votes_contra": "integer",
          "abstenciones": "integer",
          "ausentes": "integer"
        }
      }
    }
  ]
}
```

---

## 5. votes_by_party.json

### 5.1 Purpose

Provides quick access to party positions indexed by vote_id.

### 5.2 Location

```
data/02_output/votes_by_party.json
```

### 5.3 Schema

```json
{
  "[vote_id]": {
    "[party_slug]": {
      "favor": "integer",
      "contra": "integer",
      "abstencion": "integer",
      "ausente": "integer",
      "position": "SI|NO|DIVIDIDO|AUSENTE"
    }
  }
}
```

### 5.4 Example

```json
{
  "2023-06-22T19-24": {
    "fuerza_popular": {
      "favor": 22,
      "contra": 2,
      "abstencion": 1,
      "ausente": 3,
      "position": "SI"
    },
    "peru_libre": {
      "favor": 5,
      "contra": 28,
      "abstencion": 0,
      "ausente": 4,
      "position": "NO"
    }
  }
}
```

---

## 6. party_patterns.json

### 6.1 Purpose

Voting patterns for sparklines and visualizations.

### 6.2 Location

```
data/02_output/party_patterns.json
```

### 6.3 Schema

```json
{
  "generated_at": "datetime",
  "categories": ["string"],

  "parties": {
    "[party_slug]": {
      "by_category": {
        "[category]": {
          "si": "integer",
          "total": "integer",
          "pct": "float"
        }
      },
      "by_month": {
        "[YYYY-MM]": {
          "si": "integer",
          "total": "integer",
          "pct": "float"
        }
      }
    }
  }
}
```

---

## 7. Schema Validation

### 7.1 JSON Schema (Example for ampays)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AMPAY",
  "type": "object",
  "required": ["id", "party_slug", "promise", "confidence"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^AMPAY-[0-9]{3}$"
    },
    "party_slug": {
      "type": "string",
      "enum": ["fuerza_popular", "peru_libre", "renovacion_popular", "avanza_pais", "alianza_progreso", "somos_peru", "podemos_peru", "juntos_peru", "partido_morado"]
    },
    "confidence": {
      "type": "string",
      "enum": ["HIGH", "MEDIUM", "LOW"]
    }
  }
}
```

### 7.2 Validation Script

```python
# scripts/validate_schema.py
import json
import jsonschema

def validate_ampays(data, schema):
    for ampay in data['ampays']:
        jsonschema.validate(ampay, schema)
    print(f"Validated {len(data['ampays'])} AMPAYs")
```

---

## 8. Relationships Between Files

```
┌─────────────────────────────────────────────────────────┐
│                    QUIZ FLOW                            │
│                                                         │
│  quiz_statements.json                                   │
│    ├── statements[].positions → party_slug             │
│    └── calibration → party_slug                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    AMPAY FLOW                           │
│                                                         │
│  ampays.json                                            │
│    ├── ampays[].party_slug → party_slug                │
│    └── ampays[].key_laws → votes_categorized.votes[]   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    VOTES FLOW                           │
│                                                         │
│  votes_categorized.json                                 │
│    ├── votes[].party_positions → party_slug            │
│    └── votes[].category → party_patterns.categories    │
│                                                         │
│  votes_by_party.json (optimized index)                  │
│                                                         │
│  party_patterns.json (aggregations)                     │
└─────────────────────────────────────────────────────────┘
```

---

## 9. TypeScript Types

```typescript
// types/index.ts

export type PartySlug =
  | 'fuerza_popular'
  | 'peru_libre'
  | 'renovacion_popular'
  | 'avanza_pais'
  | 'alianza_progreso'
  | 'somos_peru'
  | 'podemos_peru'
  | 'juntos_peru'
  | 'partido_morado';

export type Position = -1 | 0 | 1;
export type VotePosition = 'SI' | 'NO' | 'DIVIDIDO' | 'AUSENTE';
export type Confidence = 'HIGH' | 'MEDIUM' | 'LOW';
export type Category =
  | 'seguridad' | 'economia' | 'fiscal' | 'social'
  | 'empleo' | 'educacion' | 'salud' | 'agua'
  | 'vivienda' | 'transporte' | 'energia' | 'mineria'
  | 'ambiente' | 'agricultura' | 'justicia';

export interface QuizStatement {
  id: string;
  category: Category;
  axis: 'economic' | 'social' | 'governance';
  text: string;
  simple_text: string;
  positions: Record<PartySlug, Position>;
}

export interface Ampay {
  id: string;
  party_slug: PartySlug;
  party_name: string;
  promise: string;
  category: Category;
  vote_position: 'SI' | 'NO';
  expected_position: 'SI' | 'NO';
  evidence: string;
  key_laws: string[];
  reasoning: string;
  confidence: Confidence;
}
```

---

## 10. Generated Files

| File | Generated By | Frequency |
|------|-------------|-----------|
| `quiz_statements.json` | Manual | Once |
| `ampays.json` | Manual + Script | Once |
| `votes_categorized.json` | Script | Once |
| `votes_by_party.json` | Script | Once |
| `party_patterns.json` | Script | Once |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
