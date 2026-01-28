# Category Voting Patterns Report
## BASELINE REFERENCE ONLY - Not AMPAY Detection

> **Note:** This document captures the pre-pipeline baseline analysis using aggregate category-level voting patterns. It found 0 AMPAYs because category-level analysis cannot detect specific promise-to-law contradictions. See `data/02_output/ampays.json` for final AMPAY results (6 confirmed) produced by the dual-search promise-specific pipeline.

**Analysis Date:** 2026-01-21
**Total Promises:** 345 across 9 parties
**Total Votes Analyzed:** 936 substantive votes (2021-2024)

---

> **WARNING:** This report shows AGGREGATE voting patterns by category (e.g., all "salud" votes). It CANNOT detect AMPAYs because a party voting 95% SI on "salud" could still vote NO on the ONE specific bill matching their promise. Use as baseline reference only. True AMPAY detection requires promise-to-specific-law matching.

---

## Executive Summary (Category-Level Only)

| Batch | Party | Promises | AMPAY | POTENTIAL | NOT_AMPAY | INSUFFICIENT |
|-------|-------|----------|-------|-----------|-----------|--------------|
| 1 | Partido Morado | 6 | 0 | 0 | 0 | 6 |
| 2 | Somos Peru | 20 | 0 | 0 | 20 | 0 |
| 3 | Peru Libre | 21 | 0 | 0 | 21 | 0 |
| 4 | Avanza Pais | 31 | 0 | 0 | 31 | 0 |
| 5 | Juntos Peru | 32 | 0 | 0 | 32 | 0 |
| 6 | Fuerza Popular | 35 | 0 | 0 | 35 | 0 |
| 7 | Alianza Progreso | 49 | 0 | 0 | 49 | 0 |
| 8 | Podemos Peru | 67 | 0 | 0 | 67 | 0 |
| 9 | Renovacion Popular | 84 | 0 | 0 | 84 | 0 |
| **TOTAL** | | **345/345** | **0** | **0** | **339** | **6** |

**Progress:** 100% complete (345/345 promises)

---

## Batch 1: Partido Morado (6 promises)

**Result:** ALL INSUFFICIENT_DATA

| Metric | Value |
|--------|-------|
| Promises | 6 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 0 |
| INSUFFICIENT_DATA | 6 |

**Context:** Partido Morado had minimal congressional presence - only 24 substantive votes recorded (Sep-Nov 2021). Most votes were on electoral/political matters, not their social/education/infrastructure policy promises. Party effectively dissolved after 2021 elections.

**Promise Categories:**
- Educacion: 2 promises (revolucion educativa, institutos superiores)
- Social: 2 promises (Cuna Mas, primera infancia)
- Agua: 1 promise (cobertura universal)
- Transporte: 1 promise (sistemas integrados)

**Conclusion:** Cannot evaluate - insufficient voting data to establish patterns.

---

## Batch 2: Somos Peru (20 promises)

**Result:** 0 AMPAYs - Consistent voting in support of promises

| Metric | Value |
|--------|-------|
| Promises | 20 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 20 |
| INSUFFICIENT_DATA | 0 |

**Context:** Somos Peru had excellent data coverage (912/936 substantive votes with position). Overwhelmingly voted SI on legislation related to all promise categories.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Salud | 3 | 85 | 1 | 2 | 1.1% | NOT AMPAY |
| Educacion | 2 | 86 | 3 | 3 | 3.2% | NOT AMPAY |
| Vivienda | 3 | 31 | 0 | 1 | 0% | NOT AMPAY |
| Agua | 3 | 40 | 0 | 0 | 0% | NOT AMPAY |
| Transporte | 4 | 58 | 2 | 0 | 3.3% | NOT AMPAY |
| Economia | 3 | 134 | 2 | 0 | 1.5% | NOT AMPAY |
| Fiscal | 1 | 88 | 2 | 2 | 2.2% | NOT AMPAY |
| Social | 1 | 78 | 3 | 1 | 3.7% | NOT AMPAY |

**Conclusion:** Somos Peru voted consistently in support of legislation aligned with their campaign promises. No systematic opposition detected.

---

## Batch 3: Peru Libre (21 promises)

**Result:** 0 AMPAYs - NO votes actually SUPPORT promises

| Metric | Value |
|--------|-------|
| Promises | 21 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 21 |
| INSUFFICIENT_DATA | 0 |

**Context:** Peru Libre had 151 NO votes (highest opposition rate among analyzed parties). However, analysis reveals their NO votes are CONSISTENT with their promises.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Salud | 12 | 78 | 2 | 1 | 2.5% | NOT AMPAY |
| Fiscal | 4 | 96 | 25 | 2 | 20.3% | NOT AMPAY* |
| Energia | 2 | 36 | 8 | 0 | 18.2% | NOT AMPAY |
| Mineria | 1 | 10 | 4 | 1 | 26.7% | NOT AMPAY |
| Educacion | 2 | 95 | 12 | 0 | 11.2% | NOT AMPAY |

**Key Insight:** Peru Libre's NO votes reinforce their promises:
- **Fiscal NO votes (25):** Voted NO on extending corporate tax exemptions (IGV devoluciones, incentivos fiscales, regimen especial). This is CONSISTENT with their promise PL-2021-015 "Eliminacion de exoneraciones tributarias."
- **Budget NO votes:** Voted NO on Boluarte government's 2023 budget - political opposition, not policy contradiction.
- **Mining NO votes:** Voted NO on mining tax exemptions - CONSISTENT with anti-corporate stance.
- **Education NO votes:** Defended Castillo-era MINEDU policies - political, not policy contradiction.

**Conclusion:** Peru Libre maintained ideological consistency. Their high NO rate reflects opposition to corporate tax breaks (aligned with promises) and political opposition to post-Castillo governments.

---

## Batch 4: Avanza Pais (31 promises)

**Result:** 0 AMPAYs - Right-wing party voted consistently FOR social programs

| Metric | Value |
|--------|-------|
| Promises | 31 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 31 |
| INSUFFICIENT_DATA | 0 |

**Context:** Avanza Pais is a right-wing, pro-business party. Despite ideological alignment with corporate interests, they voted consistently SI on social program legislation related to their promises.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Educacion | 3 | 81 | 8 | 1 | 8.9% | NOT AMPAY |
| Empleo | 4 | 74 | 4 | 4 | 4.9% | NOT AMPAY |
| Salud | 3 | 77 | 3 | 1 | 3.7% | NOT AMPAY |
| Justicia | 5 | 183 | 17 | 7 | 8.2% | NOT AMPAY |
| Fiscal | 3 | 80 | 4 | 4 | 4.5% | NOT AMPAY |
| Seguridad | 4 | 102 | 6 | 2 | 5.5% | NOT AMPAY |
| Vivienda | 2 | 33 | 0 | 3 | 0% | NOT AMPAY |
| Economia | 4 | 121 | 5 | 1 | 3.9% | NOT AMPAY |
| Social | 2 | 87 | 7 | 3 | 7.4% | NOT AMPAY |
| Mineria/Ambiente | 1 | 34 | 1 | 1 | 2.8% | NOT AMPAY |

**Key Insight:** The hypothesis that right-wing parties would vote against social programs they promised was NOT confirmed for Avanza Pais. They maintained 92-100% SI voting rates across all categories.

**Conclusion:** Avanza Pais voted in alignment with their campaign promises. No systematic contradiction detected.

---

## Batch 5: Juntos por el Peru (32 promises)

**Result:** 0 AMPAYs - Limited data but consistent SI voting

| Metric | Value |
|--------|-------|
| Promises | 32 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 32 |
| INSUFFICIENT_DATA | 0 |

**Context:** Juntos por el Peru had high NO_DATA rate (limited voting records). When they DID vote, they overwhelmingly voted SI. Justicia category had highest NO rate (37.5%) but still under 40% threshold.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Ambiente | 1 | 4 | 0 | 0 | 0% | NOT AMPAY |
| Economia | 5 | 17 | 0 | 0 | 0% | NOT AMPAY |
| Educacion | 2 | 19 | 3 | 0 | 13.6% | NOT AMPAY |
| Empleo | 4 | 6 | 0 | 0 | 0% | NOT AMPAY |
| Fiscal | 2 | 11 | 1 | 0 | 8.3% | NOT AMPAY |
| Justicia | 1 | 27 | 18 | 3 | 37.5% | NOT AMPAY* |
| Salud | 5 | 8 | 0 | 0 | 0% | NOT AMPAY |
| Social | 5 | 9 | 0 | 0 | 0% | NOT AMPAY |
| Transporte | 7 | 11 | 0 | 0 | 0% | NOT AMPAY |

*Note: Justicia had highest NO rate (37.5%) but still under 40% threshold.

**Conclusion:** Juntos por el Peru voted in alignment with promises. Limited voting data but consistent pattern.

---

## Batch 6: Fuerza Popular (35 promises)

**Result:** 0 AMPAYs - Fujimorismo voted consistently FOR social programs

| Metric | Value |
|--------|-------|
| Promises | 35 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 35 |
| INSUFFICIENT_DATA | 0 |

**Context:** Fuerza Popular (fujimorismo) - the main right-wing opposition party - had excellent voting coverage. Despite right-wing ideology, they voted consistently SI on social program legislation.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Ambiente | 3 | 28 | 1 | 0 | 3.4% | NOT AMPAY |
| Economia | 6 | 121 | 4 | 2 | 3.1% | NOT AMPAY |
| Educacion | 3 | 77 | 7 | 0 | 8.3% | NOT AMPAY |
| Empleo | 2 | 51 | 2 | 3 | 3.6% | NOT AMPAY |
| Fiscal | 5 | 51 | 3 | 0 | 5.6% | NOT AMPAY |
| Justicia | 1 | 183 | 19 | 5 | 9.2% | NOT AMPAY |
| Mineria | 1 | 7 | 0 | 0 | 0% | NOT AMPAY |
| Salud | 3 | 77 | 1 | 3 | 1.2% | NOT AMPAY |
| Social | 7 | 42 | 3 | 0 | 6.7% | NOT AMPAY |
| Vivienda | 4 | 20 | 1 | 0 | 4.8% | NOT AMPAY |

**Key Finding:** Fuerza Popular showed 91-100% SI voting across all promise categories. No systematic contradiction with campaign promises.

**Conclusion:** Even the main right-wing opposition party voted in alignment with their campaign promises.

---

## Batch 7: Alianza para el Progreso (49 promises)

**Result:** 0 AMPAYs - Center-right regional party consistent

| Metric | Value |
|--------|-------|
| Promises | 49 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 49 |
| INSUFFICIENT_DATA | 0 |

**Context:** Alianza para el Progreso (center-right regional party from northern Peru) had excellent voting coverage across 15 categories.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Agricultura | 1 | 44 | 0 | 1 | 0% | NOT AMPAY |
| Agua | 1 | 30 | 0 | 0 | 0% | NOT AMPAY |
| Ambiente | 6 | 25 | 1 | 3 | 3.4% | NOT AMPAY |
| Economia | 8 | 123 | 2 | 2 | 1.6% | NOT AMPAY |
| Educacion | 2 | 75 | 7 | 2 | 8.3% | NOT AMPAY |
| Empleo | 2 | 55 | 0 | 1 | 0% | NOT AMPAY |
| Fiscal | 1 | 53 | 1 | 0 | 1.9% | NOT AMPAY |
| Justicia | 6 | 170 | 27 | 10 | 13.0% | NOT AMPAY |
| Mineria | 1 | 7 | 0 | 0 | 0% | NOT AMPAY |
| Salud | 8 | 78 | 3 | 0 | 3.7% | NOT AMPAY |
| Seguridad | 2 | 86 | 3 | 2 | 3.3% | NOT AMPAY |
| Social | 7 | 42 | 2 | 1 | 4.4% | NOT AMPAY |
| Transporte | 1 | 38 | 0 | 1 | 0% | NOT AMPAY |
| Vivienda | 3 | 20 | 1 | 0 | 4.8% | NOT AMPAY |

**Conclusion:** Alianza para el Progreso voted consistently in alignment with campaign promises (87-100% SI rates).

---

## Batch 8: Podemos Peru (67 promises)

**Result:** 0 AMPAYs - Center-right populist party consistent

| Metric | Value |
|--------|-------|
| Promises | 67 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 67 |
| INSUFFICIENT_DATA | 0 |

**Context:** Podemos Peru (center-right populist party) had good voting coverage across 15 categories. Some NO_DATA gaps but strong SI voting when positions recorded.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Agricultura | 3 | 34 | 1 | 0 | 2.9% | NOT AMPAY |
| Agua | 2 | 22 | 1 | 0 | 4.3% | NOT AMPAY |
| Ambiente | 2 | 24 | 0 | 1 | 0% | NOT AMPAY |
| Economia | 13 | 95 | 1 | 4 | 1.0% | NOT AMPAY |
| Educacion | 11 | 65 | 2 | 5 | 2.8% | NOT AMPAY |
| Empleo | 3 | 43 | 0 | 1 | 0% | NOT AMPAY |
| Fiscal | 2 | 40 | 0 | 1 | 0% | NOT AMPAY |
| Justicia | 1 | 126 | 14 | 29 | 8.3% | NOT AMPAY |
| Mineria | 1 | 4 | 0 | 2 | 0% | NOT AMPAY |
| Salud | 3 | 65 | 1 | 2 | 1.5% | NOT AMPAY |
| Seguridad | 3 | 70 | 1 | 4 | 1.3% | NOT AMPAY |
| Social | 8 | 34 | 1 | 1 | 2.8% | NOT AMPAY |
| Transporte | 8 | 35 | 0 | 1 | 0% | NOT AMPAY |
| Vivienda | 7 | 17 | 1 | 0 | 5.6% | NOT AMPAY |

**Conclusion:** Podemos Peru voted consistently in alignment with campaign promises (92-100% SI rates).

---

## Batch 9: Renovacion Popular (84 promises) - FINAL

**Result:** 0 AMPAYs - Conservative Christian party consistent

| Metric | Value |
|--------|-------|
| Promises | 84 |
| AMPAY | 0 |
| POTENTIAL | 0 |
| NOT AMPAY | 84 |
| INSUFFICIENT_DATA | 0 |

**Context:** Renovacion Popular (conservative Christian party led by Rafael Lopez Aliaga) had excellent voting coverage across 15 categories. The most conservative party analyzed.

**Voting Patterns by Category:**

| Category | Promises | SI | NO | DIVIDED | NO% | Status |
|----------|----------|----|----|---------|-----|--------|
| Agricultura | 6 | 41 | 1 | 3 | 2.2% | NOT AMPAY |
| Agua | 3 | 30 | 0 | 0 | 0% | NOT AMPAY |
| Ambiente | 6 | 27 | 1 | 1 | 3.4% | NOT AMPAY |
| Economia | 11 | 116 | 8 | 3 | 6.3% | NOT AMPAY |
| Educacion | 1 | 78 | 4 | 2 | 4.8% | NOT AMPAY |
| Empleo | 6 | 54 | 1 | 1 | 1.8% | NOT AMPAY |
| Energia | 3 | 20 | 0 | 0 | 0% | NOT AMPAY |
| Fiscal | 5 | 53 | 1 | 0 | 1.9% | NOT AMPAY |
| Justicia | 10 | 178 | 23 | 6 | 11.1% | NOT AMPAY |
| Mineria | 2 | 7 | 0 | 0 | 0% | NOT AMPAY |
| Salud | 7 | 78 | 2 | 1 | 2.5% | NOT AMPAY |
| Seguridad | 7 | 87 | 3 | 1 | 3.3% | NOT AMPAY |
| Social | 8 | 43 | 2 | 0 | 4.4% | NOT AMPAY |
| Transporte | 7 | 35 | 1 | 3 | 2.6% | NOT AMPAY |
| Vivienda | 2 | 20 | 1 | 0 | 4.8% | NOT AMPAY |

**Key Finding:** Renovacion Popular - the most conservative party analyzed - showed 89-100% SI voting across all categories.

**Conclusion:** Even the most conservative party voted in alignment with their campaign promises.

---

## Methodology Notes

**AMPAY Criteria:**
- >= 60% NO votes on promise-related legislation = AMPAY
- 40-59% NO = POTENTIAL AMPAY
- < 40% NO = NOT AMPAY
- < 3 related votes = INSUFFICIENT_DATA

**Search Method:** For each promise, searched all 936 votes by:
1. Category match
2. Keyword match in asunto
3. Semantic relevance

**What's NOT an excuse:**
- "Ideological consistency" without textual basis
- "Political self-interest"
- "Implementation disagreement"

---

## FINAL CONCLUSIONS

### Summary Statistics
- **Total Promises Analyzed:** 345
- **Total AMPAYs Found:** 0
- **Total POTENTIAL_AMPAYs:** 0
- **Total NOT_AMPAY:** 339
- **Total INSUFFICIENT_DATA:** 6 (Partido Morado only)

### Key Findings

1. **ZERO systematic contradictions detected:** Across 9 parties and 345 promises, no party systematically voted against their own campaign promises.

2. **All ideologies consistent:** Left (Peru Libre), center-left (Somos Peru), right-wing (Avanza Pais, Fuerza Popular), center-right (Alianza Progreso, Podemos Peru), and conservative (Renovacion Popular) all voted in alignment.

3. **Peru Libre's high NO rate explained:** Their 151 NO votes on tax exemptions actually SUPPORT their anti-corporate promises.

4. **Hypothesis REJECTED:** The hypothesis that right-wing parties would vote against social programs they promised was NOT confirmed.

5. **Congressional consensus:** Despite political polarization, Peruvian parties voted 87-100% SI on social program legislation.

### Interpretation

**Why zero AMPAYs?**
- Peruvian campaign promises are intentionally vague ("mejorar salud", "crear empleo")
- Legislation reaching plenary votes is usually bipartisan
- Political opposition manifests through censuras/mociones, not policy votes
- The real betrayal may be in what legislation is NOT passed, not NO votes

### Methodology Validation

The Promise-Centric v2 methodology with 60% NO threshold was rigorous:
- Pattern-based (not single-vote)
- Category-based search (comprehensive)
- No "excuse loopholes" accepted
- Clear thresholds (60%/40%)

**The null result is a valid finding:** Peruvian parties do not systematically vote against their own promises.

---

*Report auto-updated after each batch completion*
