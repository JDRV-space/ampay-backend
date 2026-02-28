# Party Position Determination

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

How AMPAY determines a political party's position (SI/NO/DIVIDED/AUSENTE) from individual congress member votes. Simple majority algorithm on openpolitica data.

---

## 1. Input Data

Voting data comes from the resultados_grupo.csv files published by openpolitica. Each row represents the vote count of a parliamentary group for a specific vote.

### 1.1 CSV Structure

Each row contains the fields: grupo_parlamentario, si, no, abstenciones. Values are counts of congress members from that party who voted in each direction.

```
# resultados_grupo.csv
grupo_parlamentario,si,no,abstenciones
PL,8,2,1
FP,0,12,0
APP,6,3,2
RP,1,9,0
...
```

### 1.2 Party Codes

openpolitica uses abbreviated codes to identify each parliamentary group. The system maps these codes to full names for user-facing display.

| Code | Party |
|---|---|
| `PL` | Peru Libre |
| `FP` | Fuerza Popular |
| `APP` | Alianza para el Progreso |
| `RP` | Renovacion Popular |
| `AP` | Avanza Pais |
| `PP` | Podemos Peru |
| `JP` | Juntos por el Peru |
| `SP` | Somos Peru |
| `PM` | Partido Morado |
| `ACP` | Accion Popular |

---

## 2. Simple Majority Rule

A party's position is determined by simple majority of congress members present (who voted YES, NO, or abstained). More than 50% of those present must have voted in the same direction to assign a definite position.

### 2.1 Present Count Calculation

SI, NO, and abstention votes are summed to obtain the total present count. Absent members are not counted in the denominator.

```
total_present = si + no + abstenciones
```

### 2.2 Majority Threshold

A strict >50% threshold (simple majority) is applied. >= 50% is not used to avoid ambiguity in exact 50% ties.

> **Strict threshold:** Uses > 0.5 (strict greater than), not >= 0.5. An exact 50% tie is classified as DIVIDED, not SI or NO.

### 2.3 Percentage Calculation

In addition to the position, the percentage of SI votes over present members is calculated, rounded to one decimal:

```
si_percentage = round(si / max(total_present, 1) * 100, 1)
```

Using max(total_present, 1) prevents division by zero when total_present == 0 (AUSENTE case). In that case, si_percentage will be 0.0.

---

## 3. Decision Table

The algorithm produces exactly 4 possible outcomes. Each vote for each party is classified into one of these categories:

| Condition | Result | Description |
|---|---|---|
| `total_present == 0` | **AUSENTE** | No congress member from the party voted or abstained |
| `si / total_present > 0.5` | **SI** | More than half of those present voted in favor |
| `no / total_present > 0.5` | **NO** | More than half of those present voted against |
| `None of the above` | **DIVIDED** | Neither SI nor NO exceed 50% of those present |

### 3.1 Full Algorithm

The source code in aggregate_positions.py implements the logic as follows:

```python
# aggregate_positions.py

total_present = si + no + abstenciones

if total_present == 0:
    position = "AUSENTE"
elif si / total_present > 0.5:
    position = "SI"
elif no / total_present > 0.5:
    position = "NO"
else:
    position = "DIVIDED"

si_percentage = round(si / max(total_present, 1) * 100, 1)
```

### 3.2 Evaluation Order

The order of conditions matters: AUSENTE is checked first (total_present == 0), then SI (majority in favor), then NO (majority against), and finally DIVIDED as the residual case. If a party has exactly 50% SI and 50% NO, it is classified as DIVIDED.

```
total_present = si + no + abstenciones
        |
        v
  total_present == 0?
   /          \
  YES          NO
  |             |
  v             v
AUSENTE    si/total > 0.5?
            /          \
           YES          NO
           |             |
           v             v
         "SI"      no/total > 0.5?
                    /          \
                   YES          NO
                   |             |
                   v             v
                 "NO"       "DIVIDED"
```

---

## 4. Party Mapping

AMPAY tracks 10 main parties from the Peruvian Congress 2021-2026. Codes come from openpolitica and are mapped to full names for the user interface.

### 4.1 Tracked Parties

| Code | Full Name |
|---|---|
| `PL` | Peru Libre |
| `FP` | Fuerza Popular |
| `APP` | Alianza para el Progreso |
| `RP` | Renovacion Popular |
| `AP` | Avanza Pais |
| `PP` | Podemos Peru |
| `JP` | Juntos por el Peru |
| `SP` | Somos Peru |
| `PM` | Partido Morado |
| `ACP` | Accion Popular |

```python
PARTY_MAP = {
    "PL":  "Peru Libre",
    "FP":  "Fuerza Popular",
    "APP": "Alianza para el Progreso",
    "RP":  "Renovacion Popular",
    "AP":  "Avanza Pais",
    "PP":  "Podemos Peru",
    "JP":  "Juntos por el Peru",
    "SP":  "Somos Peru",
    "PM":  "Partido Morado",
    "ACP": "Accion Popular",
}
```

---

## 5. Aggregate Statistics

Individual per-vote positions are aggregated across 2,226 substantive votes to produce global per-party statistics.

### 5.1 Per-Party Metrics

For each party, the following is calculated:

- **Total SI:** Number of votes where the position was SI
- **Total NO:** Number of votes where the position was NO
- **Total DIVIDED:** Number of votes without a clear majority
- **Total AUSENTE:** Number of votes where no member participated
- **Average SI percentage:** Mean of si_percentage across all votes

### 5.2 Aggregation Example

For a party with 2,226 votes:

```
# Example: Fuerza Popular (FP)
Total votes:          2,226
Position SI:          1,423  (63.9%)
Position NO:            512  (23.0%)
Position DIVIDED:       187  (8.4%)
Position AUSENTE:       104  (4.7%)
Average SI %:          68.2%
```

---

## 6. Special Cases

### 6.1 NO_DATA

When a party does not appear in the resultados_grupo.csv for a specific vote, NO_DATA is assigned. This differs from AUSENTE: NO_DATA means the party did not exist or had no representation at that date, while AUSENTE means it existed but nobody voted.

> **NO_DATA != AUSENTE:** NO_DATA = party did not exist at that date. AUSENTE = party existed but nobody voted.

### 6.2 Leaves and Absences

Congress members on official leave do not appear in the vote count. If all members of a party are on leave, the result is AUSENTE (total_present == 0). Leaves do not generate a separate category.

### 6.3 Single-Member Parties

If a party has a single congress member, the party position is identical to the individual vote: SI if they voted in favor, NO if they voted against, AUSENTE if they did not attend. DIVIDED cannot occur with a single member.

```
# Single-member party
si=1, no=0, abs=0 -> total=1 -> 1/1=1.0 > 0.5 -> "SI"
si=0, no=1, abs=0 -> total=1 -> 0/1=0.0        -> "NO"
si=0, no=0, abs=0 -> total=0                    -> "AUSENTE"
si=0, no=0, abs=1 -> total=1 -> 0/1=0.0         -> "DIVIDED"
```

### 6.4 Abstentions

Abstentions count as "present" for the denominator but do not contribute to SI or NO in the numerator. A party where everyone abstains is classified as DIVIDED (neither SI > 50% nor NO > 50%).

```
# Everyone abstains
si=0, no=0, abs=5 -> total=5
si/total = 0.0 (not > 0.5)
no/total = 0.0 (not > 0.5)
-> "DIVIDED"
```

---

## 7. Limitations

- **Simple majority does not capture intensity:** A party with 51% SI and another with 99% SI have the same "SI" position
- **Abstentions are ambiguous:** An abstention can mean disagreement, indifference, or strategic absence
- **Arbitrary threshold:** The >50% cutoff is a convention, not a mathematical truth. Other thresholds (60%, 67%) would yield different results
- **Does not capture alliances:** The system analyzes parties individually, without detecting joint voting patterns between caucuses
- **Temporal bias:** Party composition changes (party-switching), but the system uses group codes at the time of the vote

---

## 8. Related Files

| File | Content |
|---|---|
| `scripts/aggregate_positions.py` | Position determination algorithm |
| `data/02_output/party_positions.json` | Calculated positions by party and vote |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
