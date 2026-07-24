# Aggregation of Individual Legislator Votes to Party Level

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Individual legislator votes are aggregated to the party level using the majority position. This document describes the rules for determining each party's position on each vote.

---

## 1. Data Source

### 1.1 Original Dataset

```
Source: openpolitica/congreso-pleno-asistencia-votacion
URL: https://github.com/openpolitica/congreso-pleno-asistencia-votacion
Format: CSV
Period: 2021-07-26 to 2024-07-26
Records: ~289,000 individual votes
Voting sessions: 2,226
```

### 1.2 Relevant Fields

| Field | Description | Example |
|-------|-------------|---------|
| `fecha` | Date of vote | 2023-06-22 |
| `asunto` | Subject voted on | "PL 3456 sobre SIS" |
| `congresista` | Legislator name | "PEREZ GARCIA, JUAN" |
| `grupo_parlamentario` | Party at time of vote | "Fuerza Popular" |
| `votacion` | Vote cast | SI / NO / ABSTENCION / AUSENTE |

---

## 2. Aggregation Rules

### 2.1 Determining Majority Position

For each vote and each party:

```python
def calculate_party_position(individual_votes):
    """
    individual_votes: list of the party's votes in that session
    Returns: party's majority position
    """
    si_votes = count(v == "SI" for v in individual_votes)
    no_votes = count(v == "NO" for v in individual_votes)
    total_present = si_votes + no_votes  # excludes abstentions and absences

    if total_present == 0:
        return "AUSENTE"

    if si_votes > no_votes:
        return "SI"
    elif no_votes > si_votes:
        return "NO"
    else:
        return "DIVIDIDO"
```

### 2.2 Decision Matrix

| YES Votes | NO Votes | Party Position |
|-----------|----------|----------------|
| > 50% | < 50% | **YES** |
| < 50% | > 50% | **NO** |
| = 50% | = 50% | **DIVIDED** |
| 0 | 0 | **ABSENT** |

### 2.3 Treatment of Abstentions

**Decision:** Abstentions do NOT count toward the majority position calculation.

**Justification:**
- An abstention is neither a vote in favor nor against
- Including abstentions would distort the actual YES/NO ratio
- This is consistent with how Congress reports results

**Formula:**
```
Position = YES_votes / (YES_votes + NO_votes)
```

---

## 3. Special Cases

### 3.1 Party Switching (Defectors)

**Problem:** A legislator may switch parliamentary blocs during the legislative term.

**Solution:** The original dataset records `grupo_parlamentario` AT THE TIME OF THE VOTE.

```
Legislator X:
- Vote 2022-03-15: grupo_parlamentario = "Peru Libre" -> counts for PL
- Vote 2022-06-20: grupo_parlamentario = "No Agrupados" -> does not count for PL
- Vote 2022-09-10: grupo_parlamentario = "Fuerza Popular" -> counts for FP
```

**No special handling required:** The field already reflects the correct party.

### 3.2 Small / New Parties

Parties with few legislators may exhibit greater variability.

| Party | Legislators (2021) | Note |
|-------|-------------------|------|
| Partido Morado | 3 | High potential variability |
| Podemos Peru | 5 | Moderate variability |
| Peru Libre | 37 | Low variability (large caucus) |

### 3.3 Divided Votes

When YES = NO exactly:

```
Party X on vote Y:
- YES: 12 legislators
- NO: 12 legislators
- Position: DIVIDED
```

**Interpretation for AMPAY:** A DIVIDED vote counts as 0.5 YES and 0.5 NO in percentage calculations.

### 3.4 Mass Absence

If all legislators of a party are absent:

```
Position: ABSENT
Interpretation: No data for this party on this vote
```

**For pattern analysis:** Absence >= 50% may indicate strategic evasion.

---

## 4. Aggregated Data Structure

### 4.1 Output Format

```json
{
  "vote_id": "2023-06-22T19-24",
  "date": "2023-06-22",
  "asunto": "PL 3456 - Modificacion Ley SIS",
  "result": "APROBADO",
  "party_positions": {
    "fuerza_popular": {
      "position": "SI",
      "votes_favor": 22,
      "votes_contra": 2,
      "abstenciones": 1,
      "ausentes": 3
    },
    "peru_libre": {
      "position": "NO",
      "votes_favor": 5,
      "votes_contra": 28,
      "abstenciones": 0,
      "ausentes": 4
    }
  }
}
```

### 4.2 Output File

```
data/02_output/votes_by_party.json
```

---

## 5. Validation

### 5.1 Internal Consistency

Verify for each vote:

```python
for vote in votes:
    total_reported = vote.total_favor + vote.total_contra + vote.total_abstencion
    sum_parties = sum(p.votes for p in vote.party_positions)
    assert total_reported == sum_parties, "Inconsistency in totals"
```

### 5.2 Comparison with Official Sources

A sample of votes verified against:
- Official Congressional minutes
- OpenPolitica reports

**Result:** 99.7% match (0.3% minor discrepancies due to update timing).

---

## 6. Party Cohesion Metrics

### 6.1 Cohesion Index

Measures how uniformly a party votes:

```
Cohesion = |YES - NO| / (YES + NO)
```

| Cohesion | Interpretation |
|----------|----------------|
| 1.0 | Total unanimity |
| 0.8-0.99 | High cohesion |
| 0.5-0.79 | Moderate cohesion |
| < 0.5 | Divided party |

### 6.2 Cohesion by Party (2021-2024 Average)

| Party | Average Cohesion |
|-------|-----------------|
| Renovacion Popular | 0.94 |
| Peru Libre | 0.91 |
| Fuerza Popular | 0.89 |
| Alianza para el Progreso | 0.87 |
| Avanza Pais | 0.85 |
| Podemos Peru | 0.82 |
| Somos Peru | 0.78 |
| Juntos por el Peru | 0.76 |
| Partido Morado | 0.71 |

---

## 7. Limitations

1. **Parliamentary bloc vs. party:** `grupo_parlamentario` may differ from the legislator's original party
2. **Roll-call vs. secret ballot:** Only roll-call votes are recorded
3. **Quorum:** Some votes have low participation
4. **Leaves of absence:** Legislators on official leave do not vote; this is not "absence"
5. **Rectified votes:** The dataset may not reflect subsequent rectifications

---

## 8. Related Files

| File | Content |
|------|---------|
| `data/02_output/votes_by_party.json` | Aggregated positions |
| `data/02_output/votes_categorized.json` | Votes with assigned category |
| `data/02_output/party_patterns.json` | Patterns by party |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
