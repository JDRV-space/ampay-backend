# Calibration Filtering

**Version:** 1.0
**Date:** 2026-02-27
**Status:** ACTIVE

---

## Executive Summary

Before showing quiz results, the system excludes parties the user fundamentally disagrees with. This document describes the pre-filtering algorithm based on calibration questions.

---

## 1. Purpose

AMPAY's quiz calculates a compatibility score for each political party based on Manhattan distance. However, numerical scoring alone can produce counterintuitive results: a party with high compatibility on secondary issues could appear in the top 3 even though the user fundamentally rejects its economic or social stance.

Calibration solves this. Before sorting and displaying results, the system asks the user to rank their preferences on two fundamental axes. The party associated with the least preferred option is excluded from the final ranking.

**Why it is necessary:**

- **Compatibility vs. affinity:** A high score does not guarantee the user feels represented
- **Fundamental axes:** Economic and social stances are the deepest divisions between parties
- **User experience:** Prevents the final result from seeming disconnected from stated priorities

---

## 2. Calibration Questions

The system presents two calibration questions, one for each axis of the political spectrum. The user orders three options from most to least preferred (ranking 1-2-3).

### 2.1 C1 - Economic Axis

Question about preferred economic model. The three options represent distinct stances on the economic spectrum:

- Option A: Free market economy with minimal regulation
- Option B: Mixed economy with moderate state participation
- Option C: Economy with strong state intervention

*Each option maps to specific parties via maps_to_parties in the quiz configuration.*

### 2.2 C2 - Social Axis

Question about preferred social stance. The three options represent distinct stances on the social spectrum:

- Option A: Social conservatism and traditional values
- Option B: Moderate stance with gradual openness
- Option C: Social progressivism and expanded rights

*Same mechanism as C1: each option maps to a subset of parties.*

### 2.3 Data Structure

The user ranking is stored as an ordered array per question:

```json
calibration: {
  C1: ["B", "A", "C"],  // rank 1, rank 2, rank 3
  C2: ["C", "B", "A"],  // rank 1, rank 2, rank 3
}
```

---

## 3. Exclusion Mechanism

The filtering algorithm is deliberately simple: only the last position (rank 3) triggers exclusion.

### 3.1 Exclusion Rule

1. Take the option at position 3 (last) from C1
2. Look up the parties mapped to that option in maps_to_parties
3. Add those parties to the exclusion set
4. Repeat for C2
5. Filter results: exclude all parties in the set

### 3.2 Implementation

*The filterByCalibration function in quiz.ts:*

```typescript
function filterByCalibration(
  results: PartyMatchResult[],
  calibration: QuizAnswers['calibration'],
  quizData: QuizData
): PartyMatchResult[] {
  const c1 = quizData.calibration_questions.questions[0]; // Economic
  const c2 = quizData.calibration_questions.questions[1]; // Social

  const excludedParties = new Set<PartySlug>();

  // C1 - Economic: last position (rank 3) gets excluded
  const c1Rank3 = calibration.C1[2];
  if (c1Rank3 && c1.maps_to_parties[c1Rank3]) {
    c1.maps_to_parties[c1Rank3]?.forEach(
      (p) => excludedParties.add(p as PartySlug)
    );
  }

  // C2 - Social: last position (rank 3) gets excluded
  const c2Rank3 = calibration.C2[2];
  if (c2Rank3 && c2.maps_to_parties[c2Rank3]) {
    c2.maps_to_parties[c2Rank3]?.forEach(
      (p) => excludedParties.add(p as PartySlug)
    );
  }

  return results.filter(
    (r) => !excludedParties.has(r.partySlug)
  );
}
```

### 3.3 Practical Example

Suppose the user ranks:

- **C1 (Economic): [B, A, C] - Prefers mixed, then market, rejects intervention**
- **C2 (Social): [C, B, A] - Prefers progressivism, then moderate, rejects conservatism**

Result: Parties mapped to C1-option-C and C2-option-A are excluded from the ranking.

---

## 4. Complete Flow

Calibration is applied as the last step before showing results:

1. User answers quiz questions (positions by topic)
2. Manhattan distance is calculated per party (blended score)
3. Parties are sorted by score from highest to lowest compatibility
4. **filterByCalibration is applied: exclude rank 3 parties**
5. Top 3 remaining parties are shown to the user

**Calibration does NOT modify scores. It only removes parties from the final ranking.**

### 4.1 Flow Diagram

```
Quiz Answers
      |
      v
Calculate Manhattan distance (blended score)
      |
      v
Sort by compatibility (highest to lowest)
      |
      v
Apply filterByCalibration  <-- rank 3 = exclude
      |
      v
Show top 3 remaining parties
```

---

## 5. Compass Relationship

The calibration questions are designed to align with the axes of AMPAY's political compass:

- **C1 = Economic axis:** From free market to state intervention. Corresponds to the horizontal axis of the compass.
- **C2 = Social axis:** From conservatism to progressivism. Corresponds to the vertical axis of the compass.

This alignment allows calibration to function as a coherent filter: a user located in one compass quadrant will naturally exclude parties from the opposite quadrant.

```
                Progressivism (C2-C)
                     |
                     |
Intervention   ------+------   Free market
  (C1-C)             |            (C1-A)
                     |
              Conservatism (C2-A)
```

---

## 6. Transparency

Calibration is a presentation filter, not a calculation filter. The system maintains transparency as follows:

- **Complete scores accessible:** The compatibility score for ALL parties (including excluded ones) is calculated and stored
- **True top match:** If the highest compatibility party was excluded by calibration, the user can access this information
- **Reversible filter:** The user can view results without calibration if desired
- **No data manipulation:** Scores are not altered, only the display is filtered

---

## 7. Limitations

- **Binary exclusion:** There is no partial penalty. A party is completely excluded or untouched. There is no middle ground.
- **Coarse filter:** Ranking 3 options is a rough approximation of the political spectrum. Nuances within each option are lost.
- **Only rank 3:** Only the last position triggers exclusion. Rank 2 (second least preferred) has no effect.
- **Mapping dependency:** Filtering quality depends entirely on maps_to_parties being correctly configured.
- **No feedback:** The user does not see which parties were excluded or why, unless they explore the full results.

---

## 8. Related Files

| File | Content |
|---|---|
| `src/lib/quiz.ts` | filterByCalibration function and quiz logic |
| `public/data/quiz_posiciones_partidos.json` | Calibration question configuration and party mapping |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-02-27*
