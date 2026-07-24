# Data Limitations

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

This document transparently discloses the known limitations of the data used in AMPAY, including temporal gaps, potential biases, and areas of uncertainty.

---

## 1. Temporal Limitations

### 1.1 Coverage Period

| Dataset | Start | End | Gap |
|---------|-------|-----|-----|
| Votes | 2021-07-26 | 2024-07-26 | 2024-07 to 2026-01 not included |
| 2021 Promises | 2021-04 | 2021-04 | Registered plan only |
| 2026 Promises | 2026-01 | 2026-01 | Registered plan only |

### 1.2 Impact of the 2024-2026 Gap

| Implication | Detail |
|-------------|--------|
| Recent AMPAYs | Contradictions from the last 18 months not detected |
| Position changes | Parties may have changed their behavior |
| Incomplete context | 2021-2024 patterns may not reflect 2024-2026 |

### 1.3 Mitigation

- Explicit disclaimer in the application
- Data cutoff date clearly displayed
- Update planned if data becomes available

---

## 2. Voting Data Limitations

### 2.1 Data Not Captured

| Vote Type | Included | Reason |
|-----------|----------|--------|
| Roll-call vote | YES | Recorded in official minutes |
| Secret vote | NO | No public record exists |
| Committee votes | NO | Only plenary sessions included |
| Bureau decisions | PARTIAL | Some decisions made without a vote |

### 2.2 Lost Context

| Element | Available | Not Available |
|---------|-----------|---------------|
| Vote outcome | YES | - |
| Vote justification | - | NO |
| Prior negotiations | - | NO |
| Political pressure | - | NO |
| Conditional votes | - | NO |

### 2.3 Data Quality

| Metric | Value | Source |
|--------|-------|--------|
| Completeness | 99%+ | openpolitica |
| Accuracy | 99.7% | Sample verification |
| Known errors | < 0.3% | Mostly typos |

---

## 3. Promise Data Limitations

### 3.1 Extraction Issues

| Issue | Frequency | Mitigation |
|-------|-----------|------------|
| Low-quality scanned PDFs | 15% | OCR + manual review |
| Non-standard structure | 100% | Per-document adaptation |
| Vague promises | 30% | Excluded if not verifiable |
| Conditional language | 20% | Coded as 0 |

### 3.2 Documentation Bias

| Party | 2021 Plan Pages | Promises Extracted | Notes |
|-------|-----------------|-------------------|-------|
| Renovacion Popular | 120+ | 84 | Highly detailed plan |
| Peru Libre | 60 | 21 | More general plan |
| Partido Morado | 25 | 6 | Short plan |

**Implication:** Parties with more detailed plans yield a greater number of analyzable promises.

### 3.3 Promises Not Included

| Type | Reason for Exclusion |
|------|---------------------|
| Verbal promises | Not documented in JNE plan |
| Campaign interviews | Outside scope |
| Social media | Questionable verifiability |
| Post-registration promises | Not in official version |

---

## 4. Categorization Limitations

### 4.1 Classification Accuracy

| Method | Estimated Accuracy | Problematic Cases |
|--------|-------------------|-------------------|
| Automatic keywords | 98% | Homonyms |
| Assisted classification | Requires review | Borderline topics |
| Manual review | 99%+ | Residual subjectivity |

### 4.2 Borderline Categories

| Example | Possible Categories | Assignment |
|---------|---------------------|------------|
| "Mining canon for education" | mineria, educacion, fiscal | fiscal |
| "Hospitals in mining zones" | salud, mineria | salud |
| "Employment in agriculture" | empleo, agricultura | agricultura |

### 4.3 Category Evolution

The current 15 categories may not capture:
- Emerging topics (e.g., automation, cryptocurrencies)
- Cross-cutting topics (e.g., gender, digitalization)
- Nuances within categories (e.g., formal vs. informal mining)

---

## 5. Quiz Limitations

### 5.1 Inherent Simplification

| Aspect | Reality | Quiz |
|--------|---------|------|
| Political spectrum | Multidimensional | 2 axes |
| Positions | Nuanced | -1/0/+1 |
| Topics | Thousands | 8 questions |
| Weighting | Variable by voter | Equal for all |

### 5.2 Potential Biases

| Bias | Description | Mitigation |
|------|-------------|------------|
| Question selection | Topics chosen by the team | Diversity of axes |
| Wording | Framing affects responses | Neutral language |
| Order | Early questions anchor | Randomize in future |

### 5.3 Pending Validation

| Test | Status | Priority |
|------|--------|----------|
| Test-retest reliability | Not conducted | Medium |
| Construct validity | Not conducted | High |
| Comparison with surveys | Not conducted | Medium |

---

## 6. AMPAY Limitations

### 6.1 False Negatives

Contradictions we may MISS:

| Type | Reason |
|------|--------|
| No related legislation | Promise without corresponding legislation in the period |
| Undetected keywords | Synonyms not included |
| Subtle contradiction | Weak semantic connection |
| Vote by delegation | Leader votes, caucus absent |

### 6.2 Residual Uncertainty

| AMPAY | Confidence | Source of Uncertainty |
|-------|-----------|----------------------|
| AMPAY-001 | HIGH | Negotiation context unknown |
| AMPAY-005 | MEDIUM | Distinction between "corporate" and "popular" |
| AMPAY-006 | MEDIUM | Only 2 motions found |

### 6.3 Context Not Captured

- Executive branch pressure
- Caucus agreements
- "Strategic" votes
- Changes in bill text between versions

---

## 7. Aggregation Limitations

### 7.1 Legislator vs. Party

| Situation | Treatment | Limitation |
|-----------|-----------|------------|
| Unanimous vote | Position = party position | None |
| Divided vote | Position = majority | Loses nuance |
| Party switcher | Uses party at time of vote | History lost |
| Single-member caucus | Position = individual | Not truly a "party" |

### 7.2 Equal Weights

All votes carry equal weight, yet:
- Some votes are more consequential (e.g., budget)
- Some legislators have more influence (e.g., leaders)
- Some issues matter more to voters

---

## 8. Usage Recommendations

### 8.1 AMPAY Is Designed To

- Inform voters about general patterns
- Identify clear contradictions
- Promote political transparency
- Serve as a starting point for further research

### 8.2 AMPAY Is NOT Designed To

- Predict future behavior with certainty
- Be the sole source for voting decisions
- Replace journalistic analysis
- Assert the intent or motivation of politicians

---

## 9. Confidence Levels by Section

| Section | Confidence | Justification |
|---------|-----------|---------------|
| Voting data | **HIGH** | Official source, verified |
| Vote categorization | **HIGH** | Multi-step process, QA |
| Party positions | **MEDIUM** | Based on promises, not votes |
| Quiz match | **MEDIUM** | Necessary simplification |
| AMPAYs | **VARIABLE** | Depends on specific evidence |

---

## 10. Future Updates

| Improvement | Impact on Limitations |
|-------------|----------------------|
| 2024-2026 data | Eliminates temporal gap |
| External validation | Increases confidence |
| More quiz questions | Reduces simplification |
| Granular categories | Improves accuracy |

---

*Last updated: 2026-01-21*
