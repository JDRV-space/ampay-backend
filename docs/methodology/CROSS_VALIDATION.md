# Cross-Validation of AMPAYs

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Every AMPAY detected automatically undergoes a cross-validation process before publication. This document describes the verification process, acceptance criteria, and examples of rejected false positives.

---

## 1. Validation Process

### 1.1 Validation Pipeline

```
┌─────────────────────────────────────────┐
│      AUTOMATICALLY DETECTED AMPAY       │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  SOURCE VERIFICATION  │
         │  (promise + votes)    │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  SEMANTIC ANALYSIS    │
         │  (logical connection) │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  CONTEXT SEARCH       │
         │  (explanations)       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  FINAL DECISION       │
         │  (approve/reject)     │
         └───────────────────────┘
```

### 1.2 Validation Criteria

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Verifiable source** | Does the promise exist in the JNE PDF? | Mandatory |
| **Verifiable vote** | Is the voting data correct? | Mandatory |
| **Semantic connection** | Is the law related to the promise? | High |
| **Consistent pattern** | Are there multiple votes, not just one? | Medium |
| **No exculpatory context** | Is there no reasonable explanation? | Medium |

---

## 2. Source Verification

### 2.1 Verify Promise

**Steps:**
1. Obtain the original PDF from JNE
2. Locate the cited page
3. Confirm exact text
4. Verify it is a promise (not context)

**Checklist:**
- [ ] PDF accessible at cited URL
- [ ] Correct page
- [ ] Text matches
- [ ] It is a commitment, not a description

### 2.2 Verify Votes

**Steps:**
1. Query the OpenPolitica dataset
2. Search by date + subject
3. Confirm party position
4. Verify it is a substantive vote

**Checklist:**
- [ ] Vote exists in dataset
- [ ] Correct date
- [ ] Subject matches
- [ ] Party position is correct
- [ ] It is not a procedural vote

---

## 3. Semantic Analysis

### 3.1 Promise-Law Connection

**Key question:** Does voting YES/NO on this law directly affect fulfillment of the promise?

**Connection Matrix:**

| Promise | Law | Vote | Connection | Verdict |
|---------|-----|------|----------|-----------|
| "Eliminate exemptions" | Law eliminating exemption X | NO | DIRECT | AMPAY |
| "Eliminate exemptions" | Law extending exemption X | YES | DIRECT (inverse) | AMPAY |
| "Eliminate exemptions" | General budget law | NO | INDIRECT | Not AMPAY |

### 3.2 Common Semantic Errors

| Error | Example | Why It Is an Error |
|-------|---------|-------------------|
| **False homonym** | Promise "citizen security" vs. Law "food security" | Different concepts |
| **Category without specificity** | Promise "improve healthcare" vs. Any health law | Promise too vague |
| **Tactical opposition** | Voting NO due to a specific amendment, not the concept | Context lost |

---

## 4. Context Search

### 4.1 Context Sources

| Source | What to Look For | Where |
|--------|-----------------|-------|
| Press | Party statements about the vote | Google News |
| Minutes | Vote justification in session | Congreso.gob.pe |
| Communiques | Official party position | Social media |

### 4.2 Valid Exculpatory Context

| Context | Example | Result |
|---------|---------|--------|
| **Opposition on form, not substance** | "We voted NO because the law had technical errors" | Evaluate case |
| **Changed circumstances** | Promise made in 2021, very different reality in 2023 | Evaluate case |
| **Mixed legislation** | Law has both aligned and contradictory provisions | Not an automatic AMPAY |

### 4.3 Non-Exculpatory Context

| Invalid Excuse | Why It Is Invalid |
|----------------|-------------------|
| "Ideological coherence" | If it contradicts the ideology, it should not have been promised |
| "Political convenience" | This is precisely what AMPAY detects |
| "Resources were unavailable" | Promises should be realistic |
| "The opposition proposed it" | The origin does not invalidate the content |

---

## 5. Examples of Rejected False Positives

### 5.1 Case: FP-MYPE-NO

```
DETECTED AMPAY:
- Promise: "Formalize one million MSMEs"
- Law: "MSME invoice payment law"
- FP vote: NO

INVESTIGATION:
- FP voted NO on this specific law
- BUT voted YES on 25 other MSME laws
- This NO was due to opposition to a penalty clause

DECISION: REJECTED
REASON: Overall pattern is supportive (25 YES vs 1 NO)
```

### 5.2 Case: PL-EXONERACION-SI

```
DETECTED AMPAY:
- Promise: "Eliminate tax exemptions"
- Law: "Extend Amazonia exemption"
- PL vote: YES

INVESTIGATION:
- PL has an electoral base in the Amazon region
- The exemption benefits small producers
- PL distinguishes between "corporate" and "popular" exemptions

DECISION: ACCEPTED with note
REASON: Real contradiction but with nuance (HIGH -> MEDIUM confidence)
```

### 5.3 Case: RP-EXPORTACION-NO

```
DETECTED AMPAY:
- Promise: "Promote exports"
- Law: "Investigative commission on Puerto Chancay"
- RP vote: NO

INVESTIGATION:
- Semantic connection: Port = exports
- However: Investigative commission != promoting exports
- Voting NO on investigating is not voting NO on exporting

DECISION: REJECTED
REASON: Weak semantic connection. Investigating infrastructure is not the same as opposing it.
```

**Note:** This case was subsequently reclassified as a valid AMPAY after additional review.

---

## 6. Validation Metrics

### 6.1 Process Results

| Metric | Value |
|--------|-------|
| Automatically detected AMPAYs | 23 |
| AMPAYs approved after cross-validation | 8 |
| AMPAYs rejected in cross-validation | 15 |
| AMPAYs eliminated in manual audit | 2 |
| AMPAYs retracted in traceability audit | 1 |
| **Final confirmed AMPAYs** | **5** |
| False positive rate (validation) | 65.2% |

> **Audit note:** Of the 8 AMPAYs approved in cross-validation, 2 were subsequently eliminated during the final manual audit (AMPAY-006 and AMPAY-007 from Alianza para el Progreso, original pre-audit numbering) due to incorrect vote interpretation. AMPAY-003 was retracted on 2026-07-09 because its supporting votes are procedural. The final traceability-audited total is 5 AMPAYs.

### 6.2 Rejection Reasons

| Reason | Count | % |
|--------|-------|---|
| Weak semantic connection | 7 | 46.7% |
| Inconsistent pattern (single vote only) | 4 | 26.7% |
| Valid exculpatory context | 2 | 13.3% |
| Error in source data | 2 | 13.3% |

---

## 7. Review Documentation

### 7.1 Record Format

```json
{
  "ampay_candidate_id": "AC-001",
  "detection_date": "2026-01-20",
  "reviewer": "JD",
  "review_date": "2026-01-21",
  "decision": "APPROVED",
  "confidence_adjustment": "HIGH → HIGH",
  "notes": "Verificado en PDF pagina 47. Patron claro con 6 leyes.",
  "sources_checked": [
    "https://plataformahistorico.jne.gob.pe/OrganizacionesPoliticas/PlanesGobiernoTrabajo",
    "https://github.com/openpolitica/congreso-pleno-asistencia-votacion"
  ]
}
```

### 7.2 Audit File

```
data/02_output/ampays.json
```

---

## 8. Appeals Process

### 8.1 How to Appeal an AMPAY

If a party or citizen believes a published AMPAY is incorrect:

1. Open an issue on GitHub: `github.com/ampay/issues`
2. Provide evidence of exculpatory context
3. AMPAY team reviews within 7 days
4. Decision documented publicly

### 8.2 Criteria for a Successful Appeal

| Evidence | Outcome |
|----------|---------|
| Demonstrated factual error | Immediate correction |
| New exculpatory context | Re-evaluation |
| Reasonable alternative interpretation | Add note, maintain AMPAY |
| Opinion without evidence | Reject appeal |

---

## 9. Limitations

1. **Reviewer bias:** Manual validation may be subject to biases
2. **Information asymmetry:** Parties possess more context than reviewers
3. **Limited time:** Exhaustive investigation of every case is not feasible
4. **Incomplete sources:** Some statements are not documented

---

## 10. Related Files

| File | Content |
|------|---------|
| `data/02_output/ampays.json` | Approved AMPAYs |
| `data/02_output/ampays.json` | Approved AMPAYs (includes audit log) |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
