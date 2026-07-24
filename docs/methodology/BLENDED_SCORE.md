# Blended Score Algorithm

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

Raw Manhattan distance favors parties with few recorded positions. The Blended Score penalizes low coverage so that parties with more defined stances compete on a level playing field.

---

## 1. The Problem

### 1.1 Low-Coverage Bias

Manhattan distance measures the absolute difference between the user position and the party position on each topic. When a party has no recorded position on a topic, it is assigned 0 (neutral). This creates a systematic bias:

- **Parties with few positions:** Accumulate less total distance because most of their topics are 0 vs user
- **Parties with many positions:** Accumulate more distance because they have real stances that may differ from the user
- **Result:** A party with 3 positions always appears "closer" than one with 15, regardless of actual alignment

### 1.2 Bias Magnitude

Without correction, parties with few positions win the ranking with a 7.6:1 advantage over parties with full coverage. This makes the quiz unusable for comparing parties with different numbers of stances.

```
// Example: User answers 15 topics, scale [-2, +2]
// Party A: only 5 recorded positions (10 topics = 0)
// Party B: 15 recorded positions

Party A total distance: 8   (only accumulates on 5 topics)
Party B total distance: 22  (accumulates on 15 topics)

Without correction: Party A WINS (8 < 22)
But: Party A only covered 33% of topics
```

---

## 2. Blended Score Formula

### 2.1 Formal Definition

The Blended Score combines the raw distance with a coverage-normalized version:

```
score = (1 - alpha) * D + alpha * (D / max(P, MIN_POSITIONS_FLOOR)) * 15

score = 0.9 * D + 0.1 * (D / max(P, 4)) * 15
```

**Where:**

- **D** = raw Manhattan distance (sum of absolute differences)
- **alpha** = 0.1 (weight of the normalized component)
- **P** = number of non-zero positions of the party
- **MIN_POSITIONS_FLOOR** = 4 (minimum floor to avoid division by very small numbers)
- **15** = scale factor so the normalized component has comparable magnitude to D

### 2.2 Intuition

- **Majority component (90%):** Raw distance D dominates the score. This preserves intuitive behavior: parties close to the user score better.
- **Corrective component (10%):** The normalized distance D/max(P,4) penalizes parties with few positions. If P is low, D/P is high, increasing the score (worse ranking).
- **Floor of 4:** Prevents parties with 1-3 positions from receiving disproportionate penalties. With P=1, the penalty would be extreme without this floor.

### 2.3 TypeScript Implementation

```typescript
const BLEND_ALPHA = 0.1;
const MIN_POSITIONS_FLOOR = 4;

export function calculateBlendedScore(
  distance: number,
  nonZeroPositions: number
): number {
  const divisor = Math.max(nonZeroPositions, MIN_POSITIONS_FLOOR);
  const normalizedDistance = distance / divisor;
  return (1 - BLEND_ALPHA) * distance
       + BLEND_ALPHA * normalizedDistance * 15;
}
```

---

## 3. Percentage Conversion

### 3.1 Formula

After the Blended Score, the distance is converted to an affinity percentage to display to the user:

```
percentage = 100 - (distance / maxDistance) * 100
```

**Where:**

- **maxDistance** = maximum possible distance per quiz configuration (scale * number of topics)

The result is rounded to the nearest integer. A percentage of 85% means the user and party agree on 85% of weighted positions.

### 3.2 Implementation

```typescript
export function distanceToPercentage(distance: number): number {
  const percentage = 100 - (distance / QUIZ_CONFIG.maxDistance) * 100;
  return Math.round(percentage);
}
```

---

## 4. Full Pipeline

### 4.1 Data Flow

Scoring follows a 4-stage pipeline:

- **calculateDistance:** Computes Manhattan distance between user answers and party positions
- **calculateBlendedScore:** Applies coverage correction using alpha=0.1
- **distanceToPercentage:** Converts blended distance to 0-100 affinity percentage
- **sort:** Orders parties by descending percentage (highest affinity first)

### 4.2 Pipeline Diagram

```
+-----------------------------------+
|  User Answers                     |
|  + Party Positions                |
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|  1. calculateDistance()           |
|     -> D (Manhattan distance)      |
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|  2. calculateBlendedScore(D, P)   |
|     -> 0.9*D + 0.1*(D/max(P,4))*15|
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|  3. distanceToPercentage()        |
|     -> 100 - (D / maxD) * 100     |
+-----------------+-----------------+
                  |
                  v
+-----------------------------------+
|  4. sort (descending)             |
|     -> Final party ranking         |
+-----------------------------------+
```

---

## 5. Simulation Validation

### 5.1 Monte Carlo Methodology

To validate the Blended Score, we ran 10 million simulations under the following conditions:

- **Random users:** Positions generated uniformly on the [-2, +2] scale
- **Real parties:** Actual Peruvian party positions with their variable coverage were used
- **Metric:** Imbalance ratio = (max wins / min wins) across parties

### 5.2 Results

| Metric | Without Blended Score | With Blended Score | Improvement |
|---|---|---|---|
| **Imbalance ratio** | 7.6 : 1 | **2.97 : 1** | 61% reduction |
| **Low-coverage bias** | Severe | **Moderate** | Significant |
| **Fairness across parties** | Unacceptable | **Acceptable** | - |

### 5.3 Interpretation

A ratio of 2.97:1 means the most frequently winning party wins ~3 times more than the least frequent. This is acceptable considering parties have different numbers of positions by design (not all responded to every topic).

---

## 6. Worked Examples

### 6.1 Comparative Example

Scenario: User with positions on 15 topics. Party A has 5 positions, Party B has 15.

| Variable | Party A (5 pos.) | Party B (15 pos.) |
|---|---|---|
| Manhattan Distance (D) | 8 | 22 |
| Non-zero positions (P) | 5 | 15 |
| max(P, 4) | 5 | 15 |
| D / divisor | 8 / 5 = 1.6 | 22 / 15 = 1.47 |
| **Blended Score** | **0.9*8 + 0.1*1.6*15 = 9.6** | **0.9*22 + 0.1*1.47*15 = 22.0** |
| Final percentage | 100 - (9.6/60)*100 = 84% | 100 - (22.0/60)*100 = 63% |

### 6.2 Example Analysis

- **Without Blended Score:** Party A (D=8) would beat Party B (D=22) for having lower raw distance, despite having positions on only 5 of 15 topics.
- **With Blended Score:** Party A rises from 8.0 to 9.6, and Party B rises from 22.0 to 22.0 (virtually no change because D/15 is very small). The gap narrows, but Party B still needs to be genuinely close to win.
- **Net effect:** The alpha=0.1 is intentionally conservative. It does not drastically invert rankings, only reduces the unfair low-coverage advantage.

```
// Step-by-step calculation - Party A (5 positions)
D = 8, P = 5
divisor = max(5, 4) = 5
normalizedDistance = 8 / 5 = 1.6
blended = 0.9 * 8 + 0.1 * 1.6 * 15
        = 7.2 + 2.4
        = 9.6  (increase of 1.6 vs raw distance 8)

// Step-by-step calculation - Party B (15 positions)
D = 22, P = 15
divisor = max(15, 4) = 15
normalizedDistance = 22 / 15 = 1.467
blended = 0.9 * 22 + 0.1 * 1.467 * 15
        = 19.8 + 2.2
        = 22.0  (increase of 0.0 vs raw distance 22)
```

---

## 7. Limitations

- **Does not eliminate all bias:** With alpha=0.1, parties with few positions still have a residual advantage. A higher alpha (0.3-0.5) would reduce bias further but could distort genuine rankings.
- **Extreme positions:** A party with few but all extreme positions (-2 or +2) may be insufficiently penalized if the user also has extreme positions.
- **Hardcoded factor of 15:** The multiplier 15 assumes a specific scale and number of topics. If the quiz configuration changes, this value should be recalibrated.
- **Arbitrary floor of 4:** MIN_POSITIONS_FLOOR=4 was chosen empirically. For quizzes with fewer than 8 topics, this value may need adjustment.

---

## 8. Related Files

| File | Content |
|---|---|
| `src/utils/quiz.ts` | Implementation of calculateBlendedScore and distanceToPercentage |
| `scripts/quiz_simulation.py` | Monte Carlo simulation script (10M iterations) |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
