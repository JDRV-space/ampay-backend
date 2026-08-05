# Party Vote Aggregation

**Status:** ACTIVE

This document owns the interpretation of committed party-position inputs and the current `votes_by_party.json` projection.

## Data Flow

1. A historical source-build step produced `data/01_input/votes/party_positions.json` from individual congressional records.
2. `scripts/aggregate_votes.py` maps the tracked party names to nine slugs and writes `data/02_output/votes_by_party.json`.
3. `scripts/compute_patterns.py` calculates category and monthly voting patterns from the same committed input.

The current aggregation script does not recreate individual party positions from the upstream repository.

## Position Rule

The retained source-build logic in `scripts/legacy/aggregate_positions.py` defines:

```text
total_present = SI + NO + ABSTENCION

if total_present == 0:       AUSENTE
elif SI / total_present > .5: SI
elif NO / total_present > .5: NO
else:                         DIVIDED
```

Abstentions are included in the denominator. Absences and licenses are excluded. A party therefore needs more than half of all present members, including abstentions, for a `SI` or `NO` position.

## Pattern Statistics

`scripts/compute_patterns.py` excludes procedural votes, the `justicia` category, and untracked categories. It includes declarative votes. For each retained category or month it reports:

```text
SI percentage = total individual SI votes / total present members
```

These percentages are participation-weighted individual vote shares, not the percentage of sessions in which a party's majority position was `SI`.

## Limitations

- Party switching is represented only to the extent captured in the committed source input.
- `DIVIDED` and `AUSENTE` do not establish motive.
- The current repository does not independently verify every individual-vote count against an official snapshot.
- Public explanations must not claim that abstentions are excluded or that patterns use substantive votes only.
