# Audit Trail

This document summarizes the public audit status for AMPAY backend datasets.

## Published Coverage

- Congressional votes: 2021-07-26 through 2024-03-07.
- Parties: 9 parties in the current dataset.
- AMPAY records: 5 confirmed records in `data/02_output/ampays.json`.
- Detailed evidence: `data/02_output/AMPAY_CONFIRMED_2021.json`.

## Validations

- JSON outputs are committed for inspection.
- Confirmed AMPAY records include stable `vote_references`.
- Promise, vote, and party-position links are manually reviewed before publication.
- Public documentation records the vote coverage limit.

## Correction Policy

- Factual errors should be corrected in the affected output file and documentation.
- Ambiguous cases should be treated as insufficient evidence until better sources are available.
- Methodology changes that affect public outputs should update the corresponding methodology docs.

## Limitations

- Votes after 2024-03-07 are not analyzed.
- The published AMPAY list is not exhaustive for the full 2021-2026 congressional term.
- Promise matching and vote interpretation include human judgment.
- Claims based on this repository should cite the coverage window and primary sources.
