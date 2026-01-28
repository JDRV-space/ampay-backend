# Esquema de Datos JSON

**Version:** 1.0
**Fecha:** 2026-01-21
**Estado:** ACTIVO

---

## Resumen Ejecutivo

Este documento define la estructura de los archivos JSON utilizados en AMPAY, siguiendo estandares de datos abiertos donde es posible.

---

## 1. Estandares Adoptados

### 1.1 Referencias

| Estandar | Uso | URL |
|----------|-----|-----|
| Popolo | Estructura de partidos/organizaciones | https://www.popoloproject.com/specs/ |
| Open Civic Data | IDs y relaciones | https://open-civic-data.readthedocs.io/ |
| Schema.org ClaimReview | AMPAYs | https://schema.org/ClaimReview |

### 1.2 Convenciones

| Convencion | Ejemplo |
|------------|---------|
| snake_case para campos | `party_slug`, `vote_date` |
| ISO 8601 para fechas | `2026-01-21` |
| Slugs para IDs | `fuerza_popular`, `peru_libre` |
| Porcentajes como float | `93.1` (no "93.1%") |

---

## 2. quiz_statements.json

### 2.1 Proposito

Contiene las preguntas del quiz, posiciones de partidos, y configuracion de calibracion.

### 2.2 Ubicacion

```
data/02_output/quiz_statements.json
```

### 2.3 Esquema

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
      "note": "string (opcional)"
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

### 2.4 Ejemplo

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

### 3.1 Proposito

Contiene los AMPAYs confirmados con evidencia detallada.

### 3.2 Ubicacion

```
data/02_output/ampays.json
```

### 3.3 Esquema

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

### 3.4 Ejemplo

```json
{
  "total": 8,
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
      "reasoning": "Prometio universalidad pero voto SI en leyes de regimenes especiales",
      "confidence": "HIGH"
    }
  ]
}
```

---

## 4. votes_categorized.json

### 4.1 Proposito

Contiene todos los votos sustantivos con categoria asignada.

### 4.2 Ubicacion

```
data/02_output/votes_categorized.json
```

### 4.3 Esquema

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

### 5.1 Proposito

Acceso rapido a posiciones de partidos indexado por vote_id.

### 5.2 Ubicacion

```
data/02_output/votes_by_party.json
```

### 5.3 Esquema

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

### 5.4 Ejemplo

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

### 6.1 Proposito

Patrones de votacion para sparklines y visualizaciones.

### 6.2 Ubicacion

```
data/02_output/party_patterns.json
```

### 6.3 Esquema

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

## 7. Validacion de Esquemas

### 7.1 JSON Schema (Ejemplo para ampays)

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

### 7.2 Script de Validacion

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

## 8. Relaciones Entre Archivos

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
│  votes_by_party.json (index optimizado)                 │
│                                                         │
│  party_patterns.json (agregaciones)                     │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Tipos TypeScript

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

## 10. Archivos Generados

| Archivo | Generado Por | Frecuencia |
|---------|--------------|------------|
| `quiz_statements.json` | Manual | Una vez |
| `ampays.json` | Manual + Script | Una vez |
| `votes_categorized.json` | Script | Una vez |
| `votes_by_party.json` | Script | Una vez |
| `party_patterns.json` | Script | Una vez |

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Ultima actualizacion: 2026-01-21*
