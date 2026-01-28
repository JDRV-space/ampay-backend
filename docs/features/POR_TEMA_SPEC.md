# Feature Spec: Por Tema

*Created: 2026-01-21*

## Overview

Browse congressional votes (2021-2024) filtered by topic. User selects a category, sees all relevant votes and how each party voted.

## User Value

**Question answered:** "¿Cómo votaron los partidos en temas de [salud/economía/seguridad]?"

**Use case:** User wants to see actual voting behavior, not just promises. Complements the quiz (promises) with real data (votes).

---

## Data Source

```
/data/01_input/votes/votes_categorized.json
├── 2226 votes total
├── 15 categories
└── Links to voting CSVs per vote
```

---

## UI Flow

### Screen 1: Category Selection

```
┌─────────────────────────────────────┐
│  VOTACIONES POR TEMA                │
│                                     │
│  Selecciona un tema:                │
│                                     │
│  [Salud]        164 votaciones      │
│  [Economía]     226 votaciones      │
│  [Seguridad]    161 votaciones      │
│  [Educación]    180 votaciones      │
│  [Empleo]       116 votaciones      │
│  [Agricultura]  106 votaciones      │
│  [Transporte]    97 votaciones      │
│  [Ambiente]      77 votaciones      │
│  [Fiscal]        78 votaciones      │
│  [Agua]          57 votaciones      │
│  [Energía]       48 votaciones      │
│  [Vivienda]      42 votaciones      │
│  [Minería]       19 votaciones      │
│                                     │
│  [Justicia - 776 votaciones]        │
│  ⚠️ Incluye procedimientos internos │
└─────────────────────────────────────┘
```

### Screen 2: Vote List (filtered by category)

```
┌─────────────────────────────────────┐
│  ← SALUD (164 votaciones)           │
│                                     │
│  Filtrar: [Sustantivo ▼] [2023 ▼]   │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Ley de Fortalecimiento del SIS ││
│  │ 15 Mar 2023 · Aprobado          ││
│  │ Votación sustantiva             ││
│  │                        [Ver →]  ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Reforma del Sistema de Salud   ││
│  │ 08 Nov 2022 · Rechazado         ││
│  │ Votación sustantiva             ││
│  │                        [Ver →]  ││
│  └─────────────────────────────────┘│
│                                     │
│  [Cargar más...]                    │
└─────────────────────────────────────┘
```

### Screen 3: Vote Detail

```
┌─────────────────────────────────────┐
│  ← SALUD                            │
│                                     │
│  LEY DE FORTALECIMIENTO DEL SIS    │
│  15 de marzo de 2023                │
│  Resultado: APROBADO (78-42-10)     │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ PARTIDO          │ VOTO         ││
│  │──────────────────│──────────────││
│  │ Fuerza Popular   │ ✗ En contra  ││
│  │ Perú Libre       │ ✓ A favor    ││
│  │ Renovación Pop.  │ ✓ A favor    ││
│  │ Avanza País      │ ✗ En contra  ││
│  │ Alianza Progreso │ ✓ A favor    ││
│  │ Somos Perú       │ ○ Abstención ││
│  │ Podemos Perú     │ — Ausente    ││
│  │ Juntos por Perú  │ ✓ A favor    ││
│  │ Partido Morado   │ ✓ A favor    ││
│  └─────────────────────────────────┘│
│                                     │
│  [Ver detalle completo en Congreso] │
│                                     │
│  ───────────────────────────────────│
│  Esto es información pública del    │
│  Congreso de la República.          │
└─────────────────────────────────────┘
```

---

## Filters

| Filter | Options |
|--------|---------|
| **vote_type** | Sustantivo (leyes reales), Declarativo, Procedural, Todos |
| **year** | 2021, 2022, 2023, 2024, Todos |
| **result** | Aprobado, Rechazado, Todos |

**Default:** Sustantivo only (hide procedural noise)

---

## Data Processing

### Step 1: Load votes by category
```javascript
const votesByCategory = votes.filter(v => v.category === selectedCategory);
```

### Step 2: Load party votes from CSV
```
Each vote has: votaciones_path → CSV with columns:
- congresista
- grupo_parlamentario
- voto (A FAVOR, EN CONTRA, ABSTENCIÓN, SIN RESPONDER)
```

### Step 3: Aggregate by party
```javascript
// Group votes by partido, count A FAVOR / EN CONTRA / etc.
const partyVotes = aggregateByParty(votacionesCSV);
```

---

## Party Mapping

Congressional groups → Our party slugs:

| Grupo Parlamentario | party_slug |
|---------------------|------------|
| FUERZA POPULAR | fuerza_popular |
| PERÚ LIBRE | peru_libre |
| RENOVACIÓN POPULAR | renovacion_popular |
| AVANZA PAÍS | avanza_pais |
| ALIANZA PARA EL PROGRESO | alianza_progreso |
| SOMOS PERÚ | somos_peru |
| PODEMOS PERÚ | podemos_peru |
| JUNTOS POR EL PERÚ | juntos_peru |
| PARTIDO MORADO | partido_morado |

**Note:** Some congresspeople changed parties mid-term. Use grupo_parlamentario at time of vote.

---

## Edge Cases

1. **Party didn't exist yet** - Show "N/A" or hide row
2. **Party had no members present** - Show "— Ausentes"
3. **Mixed votes within party** - Show majority + "(dividido)"
4. **Low confidence categorization** - Flag with "⚠️ Categorización aproximada"

---

## Integration with Quiz

After quiz results, show:

```
┌─────────────────────────────────────┐
│  Tus respuestas se alinean con:     │
│  JUNTOS POR EL PERÚ (82%)           │
│                                     │
│  [Ver cómo votaron en el Congreso →]│
└─────────────────────────────────────┘
```

Links to "Por Tema" filtered by quiz topics (salud, economía, etc.)

---

## Technical Notes

- **Data size:** 2226 votes × ~130 congresspeople = ~290K vote records
- **Caching:** Pre-aggregate party votes per vote_id, store in JSON
- **Performance:** Lazy load vote details on click

---

## MVP Scope

**Include:**
- Category selection
- Vote list with filters
- Party vote breakdown per vote

**Exclude (v2):**
- Individual congressperson lookup
- Vote comparison across time
- Export functionality

---

## Disclaimer (required)

```
Los datos provienen del portal del Congreso de la República.
AMPAY presenta esta información sin modificaciones.
Esto no es una recomendación de voto.
```
