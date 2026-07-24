# Coding of Party Positions

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Political party positions are coded on a +1/0/-1 scale based on their documented campaign promises. Silence is interpreted as a neutral position (0).

---

## 1. Coding System

### 1.1 Position Scale

| Value | Meaning | Criterion |
|-------|---------|----------|
| **+1** | SUPPORTS | Explicit promise in favor of the issue |
| **0** | NEUTRAL | No clear promise or silence on the issue |
| **-1** | OPPOSES | Explicit promise against the issue |

### 1.2 Source of Positions

**Sole source:** 2026 government plans registered with JNE

```
URL: https://plataformaelectoral.jne.gob.pe/candidatos/plan-gobierno-trabajo/buscar
Format: PDF
Accessed: January 2026
```

**Why only 2026 plans (not voting records):**
1. The quiz is for the 2026 elections, so 2026 proposals are used
2. Voting records cover 2021-2024 (historical data)
3. The AMPAY feature already covers promise-vote discrepancies
4. Simplifies development

---

## 2. Coding Rules

### 2.1 Criteria for +1 (SUPPORTS)

A position is coded +1 when the government plan contains:

1. **Explicit commitment:** "We will implement X," "We will create Y"
2. **Repeated favorable mention:** The issue appears 3+ times positively
3. **Positive action verb:** increase, expand, create, strengthen, guarantee
4. **Declared priority:** The issue appears among priorities or main policy pillars

**Examples:**
```
"We will implement the nationalization of Camisea gas" -> +1 on energia (energy)
"We will strengthen labor unions" -> +1 on empleo (employment/labor rights)
"We will expand the public health system" -> +1 on salud (public health)
```

### 2.2 Criteria for -1 (OPPOSES)

A position is coded -1 when the government plan contains:

1. **Explicit opposition:** "We will eliminate X," "We reject Y"
2. **Negative mention:** The issue is presented as a problem to correct
3. **Negative action verb:** reduce, eliminate, cut, privatize (in context)
4. **Counter-proposal:** An alternative incompatible with the +1 position

**Examples:**
```
"We will reduce state intervention in the economy" -> -1 on statist economy
"We will eliminate tax exemptions" -> -1 on fiscal (tax) benefits
"We will privatize inefficient services" -> -1 on public services
```

### 2.3 Criteria for 0 (NEUTRAL)

A position is coded 0 when:

1. **Total silence:** The issue does not appear in the government plan
2. **Ambiguous mention:** Vague language with no clear commitment
3. **Contradictory position:** The plan contains statements in both directions
4. **Excessive conditionality:** "We will study," "If possible," "We will evaluate"

**Examples:**
```
(Issue not mentioned) -> 0
"We will evaluate the possibility of reforming the tax system" -> 0
"We will improve the economy" (without specifying how) -> 0
```

---

## 3. Coding Process

### 3.1 Workflow

```
┌─────────────────────────────────────────┐
│      GOVERNMENT PLAN PDF (JNE)          │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  TEXT EXTRACTION      │
         │  (PyMuPDF/Tesseract)  │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  IDENTIFY PROMISES    │
         │  RELEVANT TO QUIZ     │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  ASSIGN POSITION      │
         │  (+1 / 0 / -1)        │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  DOCUMENT SOURCE      │
         │  (promise ID + page)  │
         └───────────────────────┘
```

### 3.2 Source Documentation

Each coded position must have:

```json
{
  "party": "peru_libre",
  "question": "Q01",
  "position": 1,
  "source_promises": ["PL-2026-024", "PL-2026-049"],
  "evidence": "Plan de gobierno p.47: 'Nacionalizaremos el gas de Camisea'",
  "confidence": "HIGH"
}
```

---

## 4. Treatment of Silence

### 4.1 Logic of Silence = 0

**Academic justification:**

The Manifesto Project (MARPOR) distinguishes between SALIENCE (how much a party emphasizes a topic) and POSITION (what it thinks about the topic). When a party does not mention an issue:

1. We cannot infer its actual position
2. Silence may be strategic or by omission
3. Assigning +1 or -1 would be speculation

**Reference:** Werner, A., et al. (2023). "Manifesto Project Codebook v6". DOI: [10.25522/manifesto.v6](https://doi.org/10.25522/manifesto.v6)

### 4.2 Special Cases of Silence

| Situation | Coding | Reason |
|-----------|--------|--------|
| Issue not mentioned | 0 | No data |
| Mention without position | 0 | Ambiguity |
| Promise + counter-promise | 0 | Internal contradiction |
| "We will evaluate" / "We will study" | 0 | Not a commitment |

---

## 5. Party-Ideology Mapping

### 5.1 Economic Axis

| Party | Economic Position | Evidence |
|-------|------------------|----------|
| Peru Libre | Left | Nationalization, state control |
| Juntos por el Peru | Left | Progressive taxation, social spending |
| Partido Morado | Center | Mixed economy, regulation |
| Somos Peru | Center | Pragmatism, no fixed ideology |
| Alianza para el Progreso | Center | Business-oriented but socially conscious |
| Fuerza Popular | Right | Free market, reduced state |
| Renovacion Popular | Right | Fiscal conservative |
| Avanza Pais | Right | Economic liberal |
| Podemos Peru | Right | Pro-business |

### 5.2 Social Axis

| Party | Social Position | Evidence |
|-------|----------------|----------|
| Renovacion Popular | Conservative | Pro-traditional family, anti-gender ideology |
| Peru Libre | Conservative | Andean traditionalism |
| Fuerza Popular | Moderate | No extreme social positions |
| Podemos Peru | Moderate | Pragmatic |
| Alianza para el Progreso | Moderate | No strong social agenda |
| Avanza Pais | Moderate | Economic liberal, socially moderate |
| Somos Peru | Moderate | No defined positions |
| Partido Morado | Progressive | Civil rights, diversity |
| Juntos por el Peru | Progressive | Human rights, gender equality |

---

## 6. Position Validation

### 6.1 Audit Process

For each quiz question:

1. **Review source promise:** Verify that the cited text exists in the PDF
2. **Confirm interpretation:** The coding reflects the content
3. **Cross-check:** Compare with other sources (news, interviews)
4. **Peer review:** A second person reviews doubtful cases

### 6.2 Audit File

```
data/02_output/quiz_position_audit.json
```

Contains:
- Each coded position
- Source promise ID
- Cited text
- PDF page
- Review date
- Reviewer

---

## 7. Removed Questions

### 7.1 Due to Total Consensus

Questions where all parties have +1:

| Original Question | Reason for Removal |
|-------------------|-------------------|
| Amazon intangibility | 9/9 parties +1 |
| Universal water coverage | 9/9 parties +1 |
| Eliminate MSME bureaucracy | 9/9 parties +1 |

**Logic:** Questions without variation do not discriminate between parties.

### 7.2 Due to Insufficient Data

Questions where fewer than 5 parties have a clear position:

| Original Question | Parties with Data |
|-------------------|-------------------|
| (none in the current dataset) | N/A |

---

## 8. Comparison with Other Approaches

### 8.1 AMPAY vs Vote Compass

| Aspect | AMPAY | Vote Compass |
|--------|-------|--------------|
| Position source | Promises only | Promises + experts |
| Scale | 3 points (-1/0/+1) | 5 points |
| Validation | Internal | Parties review |
| Silence | = 0 | May be inferred |

### 8.2 AMPAY vs Wahl-O-Mat

| Aspect | AMPAY | Wahl-O-Mat |
|--------|-------|-----------|
| Who codes | AMPAY team | Parties directly |
| Source | Public PDFs | Questionnaire to parties |
| Scale | 3 points | 3 points |
| Oversight | No external experts | Expert panel |

---

## 9. Limitations

1. **Subjectivity:** Interpretation of vague promises
2. **Strategic silence:** Parties avoid controversial topics
3. **Evolving positions:** 2026 promises may change during the campaign
4. **Promises vs. actual intent:** Government plans may be aspirational

---

## 10. Related Files

| File | Content |
|------|---------|
| `data/02_output/quiz_statements.json` | Coded positions |
| `data/02_output/quiz_position_audit.json` | Source audit |
| `data/01_input/promises/` | Original PDFs |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
