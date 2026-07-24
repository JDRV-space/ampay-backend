# Radar Chart Algorithm

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

Visualization of user-party alignment by thematic category. This document describes how the scores that feed the radar chart are calculated and normalized.

---

## 1. Purpose

The radar chart provides a visual comparison between the user's positions and those of a political party, broken down by thematic category. Each axis of the chart represents a quiz category, allowing identification of areas of agreement and disagreement.

**Visualization goals:**

- **Area comparison:** Show where user and party agree
- **Gap detection:** Identify categories with the greatest distance
- **Complement to global score:** The compatibility percentage does not show distribution by topic

---

## 2. Category Grouping

The 15 quiz questions are grouped by the category assigned in the positions dataset. Each question belongs to exactly one category.

### 2.1 Category Extraction

Categories are extracted dynamically from the dataset:

```javascript
const categories = [...new Set(
  quizData.statements.map((s) => s.category)
)];
```

### 2.2 Question Mapping

Each category can contain one or more questions. Categories with multiple questions produce more robust averages.

```javascript
const categoryStatements = quizData.statements.filter(
  (s) => s.category === category
);
```

*Note: The number of questions per category depends on the dataset and may vary between quiz versions.*

---

## 3. Average Calculation

For each category, the average position is calculated for both user and party. Individual positions range from -1 (completely against) to +1 (completely in favor).

### 3.1 User Average

The user's answers for all questions in the category are averaged:

```javascript
const userAvg = categoryStatements.reduce(
  (sum, s) => sum + (userAnswers[s.id] ?? 0), 0
) / categoryStatements.length;
```

### 3.2 Party Average

The party's positions (from the dataset) for the same questions are averaged:

```javascript
const partyAvg = categoryStatements.reduce(
  (sum, s) => sum + s.positions[partySlug], 0
) / categoryStatements.length;
```

### 3.3 Numerical Example

For a category with 3 questions:

| Question | User Answer | Party Position |
|---|---|---|
| Q1 | +1.0 | +0.5 |
| Q2 | -0.5 | -1.0 |
| Q3 | +0.5 | +1.0 |
| **Average** | **+0.33** | **+0.17** |

---

## 4. Scale Normalization

The averages in the [-1, +1] range are transformed to the [0, 100] range for radar chart visualization.

### 4.1 Normalization Formula

The linear transformation used:

```javascript
const normalizeScore = (score: number) =>
  ((score + 1) / 2) * 100;

// Equivalent: normalizedValue = 50 * score + 50
```

### 4.2 Mapping Table

Representative values of the transformation:

| Original Value | Normalized Value | Interpretation |
|---|---|---|
| -1.0 | 0 | Completely against |
| -0.5 | 25 | Moderately against |
| 0.0 | 50 | Neutral / No position |
| +0.5 | 75 | Moderately in favor |
| +1.0 | 100 | Completely in favor |

### 4.3 Normalization Properties

- **Linear:** The transformation preserves relative distances between values
- **Bijective:** Each original value maps to exactly one normalized value and vice versa
- **Centered at 50:** The neutral value (0) maps to the center of the scale (50)

---

## 5. Dual Visualization

The radar chart overlays two polygons: one for the user and one for the selected party.

### 5.1 Chart Layers

- **User layer (cyan):** Shows the normalized averages of the user's answers
- **Party layer (green):** Shows the normalized averages of the party's positions

### 5.2 Visual Interpretation

- **High overlap:** Areas where both polygons overlap indicate alignment in that category
- **Visible gaps:** Areas where the polygons diverge show disagreement
- **Symmetric shape:** If both polygons have similar shapes, there is consistency in the position pattern

### 5.3 Technical Implementation

The Recharts library is used with the native RadarChart component:

```jsx
<RadarChart data={data}>
  <PolarGrid />
  <PolarAngleAxis dataKey="category" />
  <PolarRadiusAxis domain={[0, 100]} />
  <Radar
    name="user"
    dataKey="user"
    stroke="#22d3ee"       {/* cyan */}
    fill="#22d3ee"
    fillOpacity={0.3}
  />
  <Radar
    name="party"
    dataKey="party"
    stroke="#4ade80"       {/* green */}
    fill="#4ade80"
    fillOpacity={0.3}
  />
</RadarChart>
```

---

## 6. Limitations

- **Loss of granularity:** Per-category averages can mask disagreements on individual questions. A user and party may have the same average in a category but opposite positions on specific questions.
- **Single-question categories:** When a category contains only one question, the "average" is the single position. These categories are less reliable than those aggregating multiple questions.
- **Cancellation effect:** A +1 and a -1 average to 0, the same as two neutral positions. The radar does not distinguish between neutral consensus and cancelled disagreement.
- **Dataset dependency:** Categories and their distribution depend on the active quiz. Changes in the dataset alter the visualization.

---

## 7. Related Files

| File | Content |
|---|---|
| `RadarChart.tsx` | Radar chart component |
| `quiz_posiciones_partidos.json` | Party positions per question |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
