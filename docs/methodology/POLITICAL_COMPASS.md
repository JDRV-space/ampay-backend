# Political Compass Algorithm

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

The political compass algorithm positions parties and users on a two-dimensional plane with an economic axis (left-right) and a social axis (progressive-conservative), using quiz responses weighted by compass_direction.

---

## 1. The Two Axes

The political compass maps positions on a Cartesian plane with two independent axes:

### 1.1 Economic Axis (x)

Measures the economic position of the party or user on a continuous spectrum.

| Value | Meaning |
|---|---|
| **-1** | Economic left (more state intervention, redistribution) |
| **0** | Economic center |
| **+1** | Economic right (free market, less regulation) |

### 1.2 Social Axis (y)

Measures the social position of the party or user on a continuous spectrum.

| Value | Meaning |
|---|---|
| **-1** | Progressive (individual rights, social change) |
| **0** | Social center |
| **+1** | Conservative (tradition, order, established values) |

```
                    CONSERVATIVE (y = +1)
                          |
                          |
     Left         --------+--------    Right
     (x = -1)             |            (x = +1)
                          |
                          |
                    PROGRESSIVE (y = -1)
```

---

## 2. The Role of compass_direction

Each quiz statement has a compass_direction field that determines how an affirmative response translates to movement on the corresponding axis.

### 2.1 Possible Values

| compass_direction | Effect |
|---|---|
| **-1** | Agreeing (+1) moves toward LEFT (economic) or PROGRESSIVE (social) |
| **+1** | Agreeing (+1) moves toward RIGHT (economic) or CONSERVATIVE (social) |
| **0** | Statement not used for compass (governance questions) |

### 2.2 Multiplication Mechanics

The product position * direction determines the net displacement:

| Position | compass_direction | Product | Movement |
|---|---|---|---|
| +1 (agree) | -1 | **-1** | Left / Progressive |
| +1 (agree) | +1 | **+1** | Right / Conservative |
| -1 (disagree) | -1 | **+1** | Right / Conservative |
| -1 (disagree) | +1 | **-1** | Left / Progressive |

This allows the same statement to be phrased in any direction and still map correctly on the compass.

---

## 3. Calculation for Parties

The calculateCompassPosition function computes a party's position on the compass using the party's coded positions:

### 3.1 Formula

For each axis, the weighted average of the party's positions is calculated:

```
x = SUM(position[i] * direction[i]) / count
    where axis[i] === 'economic'
    and position[i] !== 0
    and direction[i] !== 0

y = SUM(position[i] * direction[i]) / count
    where axis[i] === 'social'
    and position[i] !== 0
    and direction[i] !== 0
```

```typescript
function calculateCompassPosition(
  partySlug: PartySlug,
  quizData: QuizData
): { x: number; y: number } {
  let economicSum = 0;
  let economicCount = 0;
  let socialSum = 0;
  let socialCount = 0;

  for (const statement of quizData.statements) {
    const position = statement.positions[partySlug];
    const direction = statement.compass_direction ?? 0;
    if (position === 0 || direction === 0) continue;

    if (statement.axis === 'economic') {
      economicSum += position * direction;
      economicCount++;
    } else if (statement.axis === 'social') {
      socialSum += position * direction;
      socialCount++;
    }
  }

  const x = economicCount > 0
    ? economicSum / economicCount : 0;
  const y = socialCount > 0
    ? socialSum / socialCount : 0;
  return { x, y };
}
```

### 3.2 Step-by-Step Algorithm

- **Filter statements:** Skip where position === 0 or compass_direction === 0
- **Separate by axis:** Group statements by axis (economic or social)
- **Multiply:** For each statement: position * compass_direction
- **Average:** Sum products and divide by the count of statements in the axis
- **Return:** { x: economicAverage, y: socialAverage }

---

## 4. Calculation for the User

The calculateUserCompassPosition function is identical in structure, but uses user answers instead of party positions.

### 4.1 Differences from Parties

| Aspect | Parties | User |
|---|---|---|
| **Data source** | `statement.positions[partySlug]` | User answer to the statement |
| **Input range** | -1 to +1 (coded) | -1 to +1 (direct answer) |
| **Coverage** | May have position 0 (no position) | Always answers (no 0 from UI) |

### 4.2 Code

Both functions share the same internal logic. The only difference is the source of the position:

```typescript
// For parties:
const position = statement.positions[partySlug];

// For user:
const position = userAnswers[statement.id];

// The rest of the logic is identical
```

---

## 5. Normalization and Bounds

The algorithm results always fall within the [-1, +1] range on both axes.

### 5.1 Why the Range is [-1, +1]

- **Bounded inputs:** Both position and direction are in {-1, 0, +1}
- **Bounded product:** position * direction produces values in {-1, 0, +1}
- **Bounded average:** The average of values in [-1, +1] always falls in [-1, +1]

```
position    in {-1, 0, +1}
direction   in {-1, 0, +1}
product     in {-1, 0, +1}  (after filtering 0s)
average     in [-1, +1]     (mean of bounded values)
```

### 5.2 Interpretation of Values

| Range | Interpretation |
|---|---|
| **x near -1** | Strong economic left tendency |
| **x near 0** | Centered or mixed economic position |
| **x near +1** | Strong economic right tendency |
| **y near -1** | Strong progressive tendency |
| **y near 0** | Centered or mixed social position |
| **y near +1** | Strong conservative tendency |

---

## 6. Integration with the Quiz

The political compass is displayed as a complement to compatibility percentages after completing the quiz.

### 6.1 Visualization Flow

- **Quiz completed:** The user answers all questions
- **Parallel calculation:** Compatibility (Manhattan) and compass position are calculated simultaneously
- **Rendering:** A 2D plane is displayed with the user's point and each party's point
- **Context:** The compass complements the percentages, showing the ideological dimension that the numeric match does not capture

### 6.2 Data Displayed

- User position (highlighted point)
- Each party's position (points with party color)
- Axis labels (Left/Right, Progressive/Conservative)
- Plane quadrants with their meanings

```
  CONSERVATIVE
       |
  LC   |   RC        LC = Left conservative
       |              RC = Right conservative
  -----+-----
       |              LP = Left progressive
  LP   |   RP        RP = Right progressive
       |
  PROGRESSIVE
```

---

## 7. Limitations

- **Two-dimensional reduction:** Politics is multidimensional; two axes do not capture the full ideological complexity
- **Dependency on compass_direction:** The classification of statements into axes and directions is an editorial decision that affects results
- **Governance questions excluded:** Statements with compass_direction = 0 do not contribute to the compass, losing information
- **Sensitivity to balance:** If there are more economic than social questions (or vice versa), one axis has more resolution than the other

---

## 8. Related Files

| File | Content |
|---|---|
| `src/lib/quiz.ts` | calculateCompassPosition and calculateUserCompassPosition functions |
| `src/data/quiz_posiciones_partidos.json` | Party positions with axis and compass_direction per statement |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
