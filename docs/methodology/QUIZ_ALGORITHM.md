# Quiz Algorithm: Voter-Party Compatibility

**Version:** 3.3
**Date:** 2026-01-22
**Status:** ACTIVE

---

## Disclaimer

> **This quiz is an informational tool based on published government plans. It does not constitute a voting recommendation. Results show the similarity between your answers and the declared positions of parties, not an assessment of their performance or integrity.**

---

## Executive Summary

The AMPAY quiz uses a **blended scoring** algorithm based on Manhattan distance with a coverage adjustment. This approach combines the standard VAA (Voting Advice Application) methodology with a penalty for parties with few defined positions.

**Version 3.3:** 15 questions with a balanced 5:4 left-right ratio on the economic axis, plus social and cross-ideological questions. Interleaved ordering to prevent response bias. Algorithm validated with 2 million simulations.

**Validation:** 1 million true believer tests (100% accuracy in party identification) + 1 million random tests (balance ratio 2.72:1).

---

## 1. Theoretical Foundation

### 1.1 Voting Advice Applications (VAAs)

VAAs are tools that help voters identify which political parties best align with their preferences. They work by:

1. Collecting party positions on political issues
2. Asking the user their position on the same issues
3. Calculating the "distance" between user and parties
4. Displaying the closest parties

**Academic references:**

- Garzia, D. (2010). "The Methodological Challenges of Voting Advice Applications". *Representation*, 46(1), 89-102. DOI: [10.1080/00344890903510006](https://doi.org/10.1080/00344890903510006)
- Walgrave, S., Nuytemans, M., & Kriesi, H. (2009). "Who is taught by voters?". *Journal of Information Technology & Politics*, 6(3-4), 194-208. DOI: [10.1080/19331680903048992](https://doi.org/10.1080/19331680903048992)

### 1.2 Manhattan Distance (City-Block Distance)

Manhattan distance measures the absolute difference between two points in a multidimensional space. It is the preferred method used by VAAs such as Wahl-O-Mat (Germany) and Smartvote (Switzerland).

**Mathematical formula:**

```
D(user, party) = Σ |user_position_i - party_position_i|
```

Where:
- `D` = total distance
- `i` = each quiz question
- `position` = numerical value (-1, 0, or +1)

**Why Manhattan and not Euclidean:**

| Metric | Formula | Usage |
|--------|---------|-------|
| Manhattan | Σ\|x-y\| | Traditional VAAs, intuitive interpretation |
| Euclidean | √Σ(x-y)² | Penalizes large differences more heavily |

Manhattan distance treats all differences equally, which is fairer for political comparisons where there is no consensus on which difference is "worse."

---

## 2. Implementation in AMPAY

### 2.1 Position Scale

**User input:**
```
+1 = Agree
 0 = Neutral / Don't know
-1 = Disagree
```

**Party positions:**
```
+1 = Supports (explicit promise in favor)
 0 = No clear position (silence or ambiguity)
-1 = Opposes (explicit promise against)
```

### 2.2 Distance Calculation

**Example with 15 questions:**

| Question | User | Fuerza Popular | Peru Libre |
|----------|------|----------------|------------|
| Q01 (Mining taxes) | +1 | -1 | +1 |
| Q02 (Security) | -1 | +1 | 0 |
| Q03 (FTAs) | +1 | -1 | +1 |
| Q04 (Labor flexibility) | -1 | +1 | -1 |
| Q05 (State role in energy) | +1 | -1 | +1 |
| ... | ... | ... | ... |
| Q15 (Decentralization) | +1 | 0 | +1 |

**Distance:** Sum of |user_position - party_position| for each question.

### 2.3 Blended Score

The current algorithm uses a blended score that considers two factors:

1. **Manhattan distance (90%):** How close the user's answers are to the party's positions
2. **Coverage adjustment (10%):** Penalty for parties with few defined positions

**Why the coverage adjustment:**

A party with position 0 (no clear position) on many questions would achieve an artificially low distance, as it would be "close to everyone." The adjustment penalizes this ambiguity so that parties with clear positions are not disadvantaged.

```
Maximum possible distance = 2 * number_of_questions = 2 * 15 = 30

Blended score = 0.9 * distance + 0.1 * coverage_penalty

Percentage = 100 - (score / maximum * 100)

Example:
Party A: distance=8, 12 defined positions -> low score -> high affinity
Party B: distance=6, 4 defined positions -> high penalty -> adjusted affinity
```

**Interpretation:** Lower blended score = greater true compatibility.

### 2.4 Algorithm Validation

The algorithm was validated with 2 million simulations:

| Test Type | Count | Result |
|-----------|-------|--------|
| True believer tests | 1,000,000 | 100% accuracy (9/9 parties correct) |
| Random tests | 1,000,000 | Balance ratio 2.72:1 |

**True believer tests:** Simulated users who answer exactly as a party would. The algorithm must identify that party as the top match.

**Random tests:** Randomly generated answers to verify that no party is systematically favored. The balance ratio measures the relationship between the most and least selected party (ideal: 1:1, acceptable: <3:1).

The blended score is used to reduce the effect of parties with sparse positions while keeping the result interpretable.

---

## 3. Calibration System (Ideological Filter)

### 3.1 Purpose

Calibration questions do NOT affect the distance calculation. They serve to:
1. Filter out parties the user considers outside their spectrum
2. Avoid results that contradict the user's self-identification
3. Present results in two sections: "within your profile" and "others"

### 3.2 Calibration Questions

**C1: Economic Axis**
```
"On economic issues, rank from most to least identified with:"
Options: Left, Center, Right
Method: User RANKS 1-2-3
```

**C2: Social Axis**
```
"On social and cultural issues, rank from most to least identified with:"
Options: Conservative, Moderate, Progressive
Method: User RANKS 1-2-3
```

### 3.3 Calibration-to-Party Mapping

| Calibration | Mapped Parties |
|-------------|----------------|
| Left (economic) | Peru Libre, Juntos por el Peru |
| Center (economic) | Partido Morado, Somos Peru, Alianza para el Progreso |
| Right (economic) | Fuerza Popular, Renovacion Popular, Avanza Pais, Podemos Peru |
| Conservative (social) | Renovacion Popular, Peru Libre |
| Moderate (social) | FP, Podemos Peru, APP, Avanza Pais, Somos Peru |
| Progressive (social) | Partido Morado, Juntos por el Peru |

### 3.4 Filtering Logic

```
Rank 1 -> Primary filter (best matches)
Rank 2 -> Secondary filter (also shown)
Rank 3 -> EXCLUDED from "Within your profile"
```

**Example:**
- User ranks: Right (1), Center (2), Left (3)
- Mathematical result: Peru Libre 80%, Fuerza Popular 65%
- Display: FP appears under "Within your profile," PL appears under "You might also consider"

---

## 4. Question Selection

### 4.1 Inclusion Criteria

1. **Discriminatory power:** The question must generate variation among parties
2. **Based on promises:** Each party position must have documentary backing
3. **Electoral relevance:** The topic must be important to Peruvian voters
4. **Clarity:** Unambiguous wording

### 4.2 Exclusion Criteria

1. **Total consensus:** If all parties share the same position, the question does not discriminate
2. **Insufficient data:** If fewer than 5 parties have a clear position
3. **Secondary topics:** Questions about marginal issues in the Peruvian debate

### 4.3 Questions Removed Due to Consensus

The following questions were discarded because all parties had position +1:

- "Protect the intangibility of the Amazon"
- "Guarantee universal drinking water coverage"
- "Eliminate bureaucratic barriers for MSMEs"

**Reference:** See `quiz_statements.json` field `removed_consensus_questions`

---

## 5. Results Presentation

### 5.1 Display Structure

```
╔═══════════════════════════════════════════════════════╗
║ WITHIN YOUR PROFILE:                                  ║
║   1. Fuerza Popular         78%                       ║
║   2. Avanza Pais            71%                       ║
║   3. Renovacion Popular     65%                       ║
╠═══════════════════════════════════════════════════════╣
║ YOUR ANSWERS ALIGN WITH:                              ║
║   Peru Libre                82%                       ║
║   (This party is outside your declared profile)       ║
╠═══════════════════════════════════════════════════════╣
║ This is NOT a voting recommendation.                  ║
║ Compare the government plans before deciding.         ║
╚═══════════════════════════════════════════════════════╝
```

### 5.2 "View Details" Logic

When clicking on a party, display:
- Which questions brought the user closer to that party
- Which questions moved the user away from that party
- Source of the party's position (promise ID)

---

## 6. Academic Validation

### 6.1 Comparison with Established VAAs

| VAA | Algorithm | Scale | Weighting |
|-----|-----------|-------|-----------|
| Wahl-O-Mat | Manhattan | 3 points | Optional (2x) |
| Smartvote | Manhattan/Euclidean | 5 points | Optional |
| Vote Compass | Likert | 5 points | Automatic |
| **AMPAY** | Manhattan | 3 points | No weighting |

### 6.2 Justification of Design Decisions

**3-point scale (vs. 5):**
- Simplifies the user experience
- Reduces completion time
- Appropriate for 15 questions (medium-length quiz)

**No weighting:**
- All questions carry equal weight
- Avoids bias in the selection of "important topics"
- Consistent with basic Wahl-O-Mat approach

**Ideological balance:**
- 5 economic-left coded questions
- 4 economic-right coded questions
- 3 social axis questions
- 3 cross-ideological questions
- Interleaved order: Left-Right-Left-Right to prevent acquiescence bias

---

## 7. Limitations

1. **Simplification:** 15 questions do not capture the full complexity of politics
2. **Trinary positions:** -1/0/+1 does not allow for fine-grained nuance
3. **Availability bias:** Only parties with documented promises are included
4. **Temporal:** Positions based on 2021/2026 government plans
5. **Self-report:** Relies on user honesty in calibration
6. **Context:** Positions reflect promises, not necessarily actions

---

## 8. Related Files

| File | Content |
|------|---------|
| `data/02_output/quiz_statements.json` | Questions and party positions |
| `docs/research/03_QUIZ_ALGORITHM.md` | Detailed VAA research |
| `docs/research/06_VAA_METHODOLOGY.md` | Comparison of VAA methodologies |

---

## References

For all academic references and sources used in AMPAY, see the centralized document:
[Bibliography and Sources](../reference/SOURCES_BIBLIOGRAPHY.md)

---

*Last updated: 2026-01-22 (15 balanced questions, blended algorithm with coverage adjustment)*
