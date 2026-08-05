# Quiz Matching Algorithm

**Status:** ACTIVE CONTRACT

The quiz compares 15 user responses with coded positions for nine tracked parties. Two calibration questions are a separate filtering step. A result is a similarity calculation, not an endorsement or voting recommendation.

## Data Owner

`data/02_output/quiz_statements.json` owns the Spanish statements and party positions. The consuming frontend may add translations and presentation metadata, but it must not change statement identity or party positions independently.

## Scoring

For answers and party positions in `{-1, 0, 1}`, raw Manhattan distance is:

```text
D = sum(abs(user_answer - party_position))
```

The current consumer ranks parties with a coverage-adjusted score:

```text
P = number of non-zero party positions
score = 0.9 * D + 0.1 * (D / max(P, 4)) * 15
```

Lower scores rank first. The displayed percentage remains based on raw distance:

```text
percentage = round(100 - D / 30 * 100)
```

The ranking order is blended score, then raw distance, then party slug for an explicit deterministic tie display order. This final ordering rule is arbitrary and does not establish a meaningful preference between exactly tied parties.

## Calibration

The two calibration questions can exclude parties assigned to a user's lowest-ranked economic or social grouping from the displayed profile matches. The unfiltered best match is retained separately. Calibration mappings are interpretive metadata and must not be described as objective party identity.

## Validation

`scripts/quiz_simulation.py 42` is the reproducible backend check for this contract. It should:

- test each distinct party response vector once;
- run the seeded random-response distribution stated in its output;
- report exact ties and winner distribution;
- write `data/02_output/quiz_validation_results.json`.

Repeatedly evaluating the same nine party vectors does not constitute additional independent simulations. No claim of ten million distinct simulations is supported.

## Limitations

- Party positions are coded interpretations of plan material and require source review.
- Neutral positions reduce recorded disagreement and can affect rankings.
- Question selection, calibration mappings, and coverage adjustment affect outcomes.
- Match percentages are not probabilities, approval ratings, or forecasts.
- The deployed frontend implementation must be compared with this contract before public validation results are cited.
