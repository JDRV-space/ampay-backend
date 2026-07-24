# Ideological Calibration Mappings

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

This document details how political parties are mapped to calibration axes (economic and social) used in the AMPAY quiz to filter results based on the user's self-identification.

---

## 1. Purpose of the Calibration System

### 1.1 Objective

The calibration system allows users to first see parties within their ideological "comfort zone," preventing negative reactions when the mathematical match suggests unexpected parties.

### 1.2 Does Not Affect the Calculation

**IMPORTANT:** The calibration questions do NOT affect the Manhattan distance calculation. They only filter the PRESENTATION of results.

```
Calculation: 100% based on questions Q01-Q08
Calibration: Only affects display order and grouping
```

---

## 2. Calibration Axes

### 2.1 Economic Axis (C1)

**Question:**
> "On economic issues, rank from most to least identified with:"

**Options:**
1. Izquierda (Left)
2. Centro (Center)
3. Derecha (Right)

**Input method:** The user RANKS the 3 options (1 = most identified with, 3 = least identified with)

### 2.2 Social Axis (C2)

**Question:**
> "On social and cultural issues, rank from most to least identified with:"

**Options:**
1. Conservador (Conservative)
2. Moderado (Moderate)
3. Progresista (Progressive)

**Input method:** The user RANKS the 3 options (1 = most identified with, 3 = least identified with)

---

## 3. Party Mapping by Axis

### 3.1 Economic Axis

| Position | Parties | Justification |
|----------|---------|---------------|
| **Izquierda (Left)** | Peru Libre, Juntos por el Peru | Statism, nationalization, price controls |
| **Centro (Center)** | Partido Morado, Somos Peru, Alianza para el Progreso | Mixed economy, pragmatism, no extreme position |
| **Derecha (Right)** | Fuerza Popular, Renovacion Popular, Avanza Pais, Podemos Peru | Free market, reduction of the state, privatization |

### 3.2 Social Axis

| Position | Parties | Justification |
|----------|---------|---------------|
| **Conservador (Conservative)** | Renovacion Popular, Peru Libre | Pro-traditional family, opposition to gender approach |
| **Moderado (Moderate)** | Fuerza Popular, Podemos Peru, Alianza para el Progreso, Avanza Pais, Somos Peru | No strong social agenda, pragmatic positions |
| **Progresista (Progressive)** | Partido Morado, Juntos por el Peru | LGBTQ+ rights, gender approach, civil rights |

---

## 4. Complete Mapping Matrix

| Party | Economic Axis | Social Axis |
|-------|---------------|-------------|
| Peru Libre | Izquierda (Left) | Conservador (Conservative) |
| Juntos por el Peru | Izquierda (Left) | Progresista (Progressive) |
| Partido Morado | Centro (Center) | Progresista (Progressive) |
| Somos Peru | Centro (Center) | Moderado (Moderate) |
| Alianza para el Progreso | Centro (Center) | Moderado (Moderate) |
| Fuerza Popular | Derecha (Right) | Moderado (Moderate) |
| Renovacion Popular | Derecha (Right) | Conservador (Conservative) |
| Avanza Pais | Derecha (Right) | Moderado (Moderate) |
| Podemos Peru | Derecha (Right) | Moderado (Moderate) |

---

## 5. Filtering Logic

### 5.1 Rules

```
Rank 1 → Parties in this group: INCLUDED as "Within your profile"
Rank 2 → Parties in this group: INCLUDED as "Within your profile"
Rank 3 → Parties in this group: EXCLUDED from "Within your profile"
```

### 5.2 Axis Combination

A party is EXCLUDED if it falls in Rank 3 of ANY axis.

**Example:**
```
User:
  C1 (economic): Derecha (1), Centro (2), Izquierda (3)
  C2 (social): Moderado (1), Conservador (2), Progresista (3)

Excluded:
  - Economic left: Peru Libre, Juntos Peru
  - Social progressive: Partido Morado, Juntos Peru

Partido Morado: Excluded (progressive)
Peru Libre: Excluded (left + conservative, but left excludes it)
Juntos Peru: Excluded (left + progressive, both rank 3)
```

### 5.3 Final Display

```
"Within your profile:"
  [Top 3 non-excluded parties, sorted by % match]

"Your answers align with:"
  [#1 mathematical match, ALWAYS displayed]
  (If it is an excluded party, show explanatory note)
```

---

## 6. Mapping Justification

### 6.1 Peru Libre as Economic Left + Social Conservative

**Evidence:**
- 2021 governance plan: Nationalization of resources, state control
- 2026 governance plan: Planned economy, statism
- Social positions: Opposition to "gender ideology," traditional Andean values

### 6.2 Partido Morado as Economic Center + Social Progressive

**Evidence:**
- Governance plan: Mixed economy, smart regulation
- Social positions: LGBTQ+ rights, equal marriage, gender approach

### 6.3 Renovacion Popular as Economic Right + Social Conservative

**Evidence:**
- Governance plan: Reduction of the state, free market
- Social positions: Pro-life, pro-traditional family, opposition to gender approach

---

## 7. Special Cases

### 7.1 Peru Libre (Left + Conservative)

An unusual combination in the Western context but common in Andean Latin American left-wing politics.

### 7.2 Parties with Ambiguous Positions

| Party | Ambiguity | Resolution |
|-------|-----------|------------|
| Somos Peru | No clear ideology | Centro/Moderado (pragmatic default) |
| Alianza para el Progreso | Business-oriented but regional | Centro/Moderado |
| Podemos Peru | Pro-business but flexible | Derecha/Moderado |

---

## 8. JSON Representation

```json
{
  "calibration_questions": {
    "questions": [
      {
        "id": "C1",
        "text": "En temas economicos, ordena del mas al menos identificado:",
        "options": ["Izquierda", "Centro", "Derecha"],
        "maps_to_parties": {
          "Izquierda": ["peru_libre", "juntos_peru"],
          "Centro": ["partido_morado", "somos_peru", "alianza_progreso"],
          "Derecha": ["fuerza_popular", "renovacion_popular", "avanza_pais", "podemos_peru"]
        }
      },
      {
        "id": "C2",
        "text": "En temas sociales y culturales, ordena del mas al menos identificado:",
        "options": ["Conservador", "Moderado", "Progresista"],
        "maps_to_parties": {
          "Conservador": ["renovacion_popular", "peru_libre"],
          "Moderado": ["fuerza_popular", "podemos_peru", "alianza_progreso", "avanza_pais", "somos_peru"],
          "Progresista": ["partido_morado", "juntos_peru"]
        }
      }
    ]
  }
}
```

---

## 9. Filtering Algorithm

```python
def filtrar_por_calibracion(partidos, c1_ranking, c2_ranking):
    """
    c1_ranking: dict { "Izquierda": 1, "Centro": 2, "Derecha": 3 }
    c2_ranking: dict { "Conservador": 1, "Moderado": 2, "Progresista": 3 }
    """
    excluidos = set()

    # Exclude parties in rank 3 of C1
    for opcion, rank in c1_ranking.items():
        if rank == 3:
            excluidos.update(C1_MAPS[opcion])

    # Exclude parties in rank 3 of C2
    for opcion, rank in c2_ranking.items():
        if rank == 3:
            excluidos.update(C2_MAPS[opcion])

    # Filter
    dentro_perfil = [p for p in partidos if p.slug not in excluidos]
    fuera_perfil = [p for p in partidos if p.slug in excluidos]

    return dentro_perfil, fuera_perfil
```

---

## 10. Validation

### 10.1 Internal Consistency

Verify that:
- Each party appears in exactly 1 option of C1
- Each party appears in exactly 1 option of C2
- No parties remain unmapped

### 10.2 External Validation

Compare mappings with:
- Chapel Hill Expert Survey (CHES) if available for Peru
- Political science classifications
- Self-identification by parties

---

## 11. Limitations

1. **Oversimplification:** 3 options do not capture ideological nuances
2. **Static:** Mappings may change over time
3. **Subjective:** Classification has an interpretive component
4. **No external validation:** There is no CHES for Peru 2026

---

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
