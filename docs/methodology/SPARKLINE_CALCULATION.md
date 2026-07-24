# Sparkline Calculation: Voting Patterns

**Version:** 1.0
**Date:** 2026-01-21
**Status:** ACTIVE

---

## Executive Summary

Sparklines display the percentage of "YES" votes for each party by category and by month. They are used in party profiles to visualize voting trends.

---

## 1. Sparkline Definition

### 1.1 What Is a Sparkline

A sparkline is a miniature chart that shows trends in a compact space. In AMPAY:

```
Fuerza Popular - economia (economy): ▁▂▃▅▇▆▅▄▃▂ (94.2%)
```

Each bar represents a period (month or category).

### 1.2 Calculated Metrics

| Metric | Formula | Use |
|--------|---------|-----|
| % YES by category | YES_votes / (YES_votes + NO_votes) * 100 | Compare thematic positions |
| % YES by month | YES_votes_month / Total_votes_month * 100 | Track temporal evolution |

---

## 2. Calculation by Category

### 2.1 Formula

```python
def calculate_pct_category(party, category, votes):
    """
    Calculates YES percentage for a party in a category
    """
    party_category_votes = filter(
        votes,
        where party == party_input AND category == category_input
    )

    total_yes = sum(v.votes_favor for v in party_category_votes)
    total_no = sum(v.votes_contra for v in party_category_votes)

    if total_yes + total_no == 0:
        return None  # No data

    return round(total_yes / (total_yes + total_no) * 100, 1)
```

### 2.2 Exclusions

**Votes excluded from calculation:**

| Vote Type | Reason for Exclusion |
|-----------|---------------------|
| `declarativo` (declarative) | No real political impact |
| `procedural` | Legislative mechanics, not a position |
| `justicia` (justice) category | Highly contextual, causes distortion |

### 2.3 Calculation Example

```
Party: Fuerza Popular
Category: salud (health)

Votes found: 258
- YES: 1,581 individual votes
- NO: 118 individual votes
- Total: 1,699

Calculation:
% YES = 1,581 / 1,699 * 100 = 93.1%
```

---

## 3. Calculation by Month

### 3.1 Formula

```python
def calculate_pct_month(party, month, votes):
    """
    Calculates YES percentage for a party in a specific month
    """
    party_month_votes = filter(
        votes,
        where party == party_input
        AND extract_month(date) == month_input
    )

    total_yes = sum(v.votes_favor for v in party_month_votes)
    total_no = sum(v.votes_contra for v in party_month_votes)

    if total_yes + total_no == 0:
        return None  # No data for that month

    return round(total_yes / (total_yes + total_no) * 100, 1)
```

### 3.2 Temporal Normalization

**Problem:** Some months have more votes than others.

**Solution:** The percentage already normalizes (ratio, not absolute count).

**Period:** 2021-08 to 2024-07 (36 months)

### 3.3 Months with Few Votes

If a month has fewer than 5 votes:
- Calculate the percentage normally
- Display with a "low data" indicator
- Do not exclude from the sparkline

---

## 4. Data Structure

### 4.1 JSON Format

```json
{
  "fuerza_popular": {
    "by_category": {
      "salud": {
        "si": 1581,
        "total": 1699,
        "pct": 93.1
      },
      "economia": {
        "si": 2547,
        "total": 2705,
        "pct": 94.2
      }
    },
    "by_month": {
      "2021-08": {
        "si": 1,
        "total": 21,
        "pct": 4.8
      },
      "2021-09": {
        "si": 70,
        "total": 70,
        "pct": 100.0
      }
    }
  }
}
```

### 4.2 Output File

```
data/02_output/party_patterns.json
```

---

## 5. Visualization

### 5.1 Percentage-to-Bar Mapping

| % YES | Bar | Meaning |
|-------|-----|---------|
| 0-12.5% | ▁ | Very low |
| 12.5-25% | ▂ | Low |
| 25-37.5% | ▃ | Medium-low |
| 37.5-50% | ▄ | Medium |
| 50-62.5% | ▅ | Medium-high |
| 62.5-75% | ▆ | High |
| 75-87.5% | ▇ | Very high |
| 87.5-100% | █ | Maximum |

### 5.2 Color Coding

```css
/* CSS Variables for sparklines */
--sparkline-low: #ff6b6b;      /* < 40% - Opposition */
--sparkline-mid: #ffd93d;      /* 40-60% - Divided */
--sparkline-high: #6bff6b;     /* > 60% - Support */
```

### 5.3 Visual Example

```
FUERZA POPULAR - Voting by Category

salud      ████████▇ 93%
economia   █████████ 94%
seguridad  █████████ 96%
educacion  ████████▇ 91%
empleo     ████████▆ 89%
```

---

## 6. Interpretation

### 6.1 Typical Patterns

| Pattern | Meaning |
|---------|---------|
| All high (>80%) | Ruling party or highly cohesive party |
| All low (<40%) | Systematic opposition |
| Variable by category | Differentiated positions by topic |
| Temporal decline | Position shift or internal crisis |

### 6.2 Alerts

**Coherence alert:** If a party has >80% YES in a category but promises the opposite, it may indicate a potential AMPAY.

---

## 7. Limitations

1. **Voting bias:** Not all topics reach a vote
2. **Excessive aggregation:** 15 categories may obscure nuances
3. **Equal weighting:** Major and minor votes carry the same weight
4. **No context:** The number does not explain WHY they voted that way
5. **Fixed period:** 2021-2024, does not include the current legislative session

---

## 8. Validation

### 8.1 Total Verification

```python
# For each party, verify:
total_by_category = sum(cat.total for cat in party.by_category)
total_by_month = sum(month.total for month in party.by_month)

assert total_by_category == total_by_month, "Inconsistency in totals"
```

### 8.2 Comparison with Sources

- Cross-reference with Congressional transparency reports
- Verify months with anomalies (0% or 100%)
- Review categories with sparse data

---

## 9. Generation Script

```python
# scripts/compute_patterns.py

import json
from collections import defaultdict

def compute_party_patterns(votes_categorized):
    patterns = defaultdict(lambda: {
        'by_category': defaultdict(lambda: {'si': 0, 'total': 0}),
        'by_month': defaultdict(lambda: {'si': 0, 'total': 0})
    })

    for vote in votes_categorized:
        category = vote['category']
        month = vote['date'][:7]  # YYYY-MM

        for party, position in vote['party_positions'].items():
            if position['position'] in ['SI', 'NO']:
                patterns[party]['by_category'][category]['total'] += 1
                patterns[party]['by_month'][month]['total'] += 1

                if position['position'] == 'SI':
                    patterns[party]['by_category'][category]['si'] += 1
                    patterns[party]['by_month'][month]['si'] += 1

    # Calculate percentages
    for party in patterns:
        for cat in patterns[party]['by_category']:
            data = patterns[party]['by_category'][cat]
            data['pct'] = round(data['si'] / data['total'] * 100, 1) if data['total'] > 0 else None

        for month in patterns[party]['by_month']:
            data = patterns[party]['by_month'][month]
            data['pct'] = round(data['si'] / data['total'] * 100, 1) if data['total'] > 0 else None

    return patterns
```

---

## 10. Related Files

| File | Content |
|------|---------|
| `data/02_output/party_patterns.json` | Sparkline data |
| `data/02_output/votes_categorized.json` | Source votes |
| `scripts/compute_patterns.py` | Generation script |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-21*
