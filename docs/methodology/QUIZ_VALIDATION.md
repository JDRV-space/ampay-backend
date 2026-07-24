# Quiz Algorithm Validation

**AMPAY - Electoral Transparency Peru 2026**

| Field | Value |
|-------|-------|
| Date | January 23, 2026 |
| Author | [@JDRV-space](https://github.com/JDRV-space) |
| Method | Monte Carlo Simulation |
| Review | Open to methodological audits |

---

## Neutrality Statement

AMPAY is an informational tool that does not recommend whom to vote for.

- **Funding:** Self-funded by the founding team (no external sponsors)
- **Party affiliation:** None -- team members have no current or past party membership
- **Privacy:** No accounts, no tracking cookies, no logging of user responses
- **Public methodology:** This document and the validation data are available for audit

---

## Executive Summary

**2,000,000 simulations** were conducted to validate the AMPAY political quiz matching algorithm.

| Test | Simulations | Result |
|------|-------------|--------|
| True Believers | 1,000,000 | **100% accuracy** |
| Random Responses | 1,000,000 | Distribution consistent with party positions |

**Conclusion:** The algorithm functions correctly. The distribution of random matches reflects the position structure of each party.

---

## Related Documents

| Document | Content |
|----------|---------|
| Promise Extraction | How party positions are extracted from JNE government plans |
| VAA Methodology | Academic foundation of the quiz design |
| Replication Dataset | `data/02_output/quiz_validation_dataset.json` -- File to reproduce the validation |

---

## Methodology

### Algorithm Evaluated

The quiz uses **Manhattan distance** to calculate the similarity between the user's responses and each party's positions:

```
distance = Σ |user_response - party_position|
```

| Parameter | Value |
|-----------|-------|
| Questions | 15 |
| Parties | 9 |
| Scale | -1 (Disagree), 0 (Neutral), +1 (Agree) |
| Maximum distance | 30 points |
| Tiebreaker | First party alphabetically |

### Why Manhattan Distance?

- **Treats each question independently** -- sum of absolute differences
- **Does not disproportionately penalize** a single large disagreement
- **With a 3-point scale**, Manhattan and Euclidean produce similar rankings; Manhattan is simpler to interpret
- **Standard in VAA applications** (Wahl-O-Mat, Vote Compass)

### Conversion to Percentage

```
match_percentage = 100 - (distance / 30 * 100)
```

---

## Test 1: True Believers

### Objective

Verify that a user who answers exactly like a party is matched with that party.

### Results

| Party | Simulations | Correct | Accuracy |
|-------|-------------|---------|----------|
| Fuerza Popular | 111,111 | 111,111 | 100% |
| Peru Libre | 111,111 | 111,111 | 100% |
| Renovacion Popular | 111,111 | 111,111 | 100% |
| Avanza Pais | 111,111 | 111,111 | 100% |
| Alianza para el Progreso | 111,111 | 111,111 | 100% |
| Somos Peru | 111,111 | 111,111 | 100% |
| Podemos Peru | 111,111 | 111,111 | 100% |
| Juntos por el Peru | 111,111 | 111,111 | 100% |
| Partido Morado | 111,111 | 111,111 | 100% |
| **TOTAL** | **999,999** | **999,999** | **100%** |

### Interpretation

The algorithm achieves **100% accuracy** for users with defined positions. This result also confirms that each party has a unique position vector.

---

## Test 2: Random Responses

### Objective

Evaluate the distribution of results when users respond randomly.

### Party Position Structure

The key to understanding the results lies in how many **neutral (0)** positions each party holds:

| Party | Neutral Positions (0) | Extreme Positions (-1/+1) |
|-------|-----------------------|---------------------------|
| Somos Peru | 13 | 2 |
| Podemos Peru | 11 | 4 |
| Partido Morado | 11 | 4 |
| Alianza para el Progreso | 10 | 5 |
| Fuerza Popular | 6 | 9 |
| Avanza Pais | 6 | 9 |
| Peru Libre | 3 | 12 |
| Juntos por el Peru | 3 | 12 |
| Renovacion Popular | 1 | 14 |

**Key observation:** Random responses have an expected value of 0 (the average of -1, 0, +1). Therefore, parties with more neutral positions will be mathematically closer to random "noise."

### Results

| Party | Matches | Percentage | Neutral Positions |
|-------|---------|-----------|-------------------|
| Somos Peru | 321,196 | 32.12% | 13 |
| Peru Libre | 131,845 | 13.18% | 3 |
| Alianza para el Progreso | 115,890 | 11.59% | 10 |
| Partido Morado | 113,563 | 11.36% | 11 |
| Podemos Peru | 105,233 | 10.52% | 11 |
| Fuerza Popular | 95,878 | 9.59% | 6 |
| Renovacion Popular | 41,152 | 4.12% | 1 |
| Juntos por el Peru | 40,671 | 4.07% | 3 |
| Avanza Pais | 34,572 | 3.46% | 6 |

### Statistical Verification

The distribution is NOT uniform, as expected mathematically:

| Metric | Value |
|--------|-------|
| Chi-squared (X2) | 545,177.93 |
| Degrees of freedom | 8 |
| Result | Non-uniform distribution (confirmed) |

**Note:** This chi-squared test confirms what we already know from the position structure. It is not a "bias test" but rather a verification that the results are consistent with the mathematics.

### Observed Correlation

The correlation between neutral positions and random match rate is evident:

- **Somos Peru:** 13 neutrals -> 32% random match rate
- **Renovacion Popular:** 1 neutral -> 4% random match rate

This demonstrates that the algorithm **functions correctly**: parties with clear positions require intentional alignment.

---

## Ideological Clarity Metrics

| Party | Random Match Rate | Ideological Clarity |
|-------|-------------------|---------------------|
| Avanza Pais | 3.46% | **High** (defined positions) |
| Juntos por el Peru | 4.07% | **High** |
| Renovacion Popular | 4.12% | **High** |
| Fuerza Popular | 9.59% | Medium |
| Podemos Peru | 10.52% | Medium |
| Partido Morado | 11.36% | Medium |
| Alianza para el Progreso | 11.59% | Medium |
| Peru Libre | 13.18% | Medium-Low |
| Somos Peru | 32.12% | **Low** (mostly neutral) |

**Threshold definitions:**
- High clarity: <5% random match rate
- Medium: 5-15%
- Low: >15%

**Implication:** If the user's top match is a low-clarity party, it is recommended to examine the 2nd and 3rd matches for more specific alignment.

---

## Conclusions

1. **100% accuracy** for users with defined positions
2. **Consistent distribution** with the mathematical structure of party positions
3. **No artificial bias** -- results reflect the actual positions of the parties
4. **Verifiable correlation** between position neutrality and random match rate

---

## Reproducibility

### Requirements

- Python 3.8+
- No external dependencies (standard library only)

### Files

| File | Description |
|------|-------------|
| `scripts/quiz_simulation.py` | Validation script |
| `data/02_output/quiz_statements.json` | Complete quiz data |
| `data/02_output/quiz_validation_dataset.json` | Simplified dataset for replication |

**SHA-256 Hash (quiz_posiciones_partidos.json):** `fdd72e86366ef6c7b77c0dd6d25724556ed7d90193b5439c2ac528241cd012d1`

### Execution

The necessary files are available upon request for methodological audit.

```bash
# Verify data file integrity
shasum -a 256 data/02_output/quiz_statements.json
# Should output: c33f9d55ec53e653...f9db

# Run with fixed seed (exact reproducibility)
python3 scripts/quiz_simulation.py 42

# Run without seed (verify statistical consistency)
python3 scripts/quiz_simulation.py
```

### Specifications

| Parameter | Value |
|-----------|-------|
| Simulations | 2,000,000 |
| Time | ~55 seconds (Apple M1) |
| Official seed | 42 |
| Dependencies | None (standard library) |

---

## Sensitivity Analysis

The algorithm was evaluated under different scenarios to verify its robustness:

| Scenario | Impact on Results |
|----------|-------------------|
| Changing 1 response | May change ranking of parties with differences < 2 points |
| All neutral responses (0) | Somos Peru achieves best match (13 neutrals) |
| All extreme responses (+1/-1) | Renovacion Popular most likely (14 extreme positions) |
| Distance ties | Resolved alphabetically (deterministic behavior) |

**Practical implication:** Users with clear positions obtain stable matches. Undecided users (many neutrals) may see variation in their ranking of nearby parties.

---

## Limitations

1. **Party positions:** This validation assumes that positions were correctly extracted (see [PROMISE_EXTRACTION.md](PROMISE_EXTRACTION.md))
2. **External validation:** Review by academic or electoral observation institutions is invited

---

## Contact

- GitHub: [@JDRV-space](https://github.com/JDRV-space)

---

*Public document, reproducible and open to review.*
