# Data Limitations

**Status:** ACTIVE

This document owns stable limitations for the committed AMPAY datasets. Counts and dates below are derived from the committed files and are checked by `python3 scripts/validate_current_outputs.py`.

## Congressional Votes

- Coverage: 2021-07-26 through 2024-03-07.
- Records: 2,226 plenary vote records.
- Types: 936 substantive, 1,149 procedural, and 141 declarative.
- Votes from 2024-03-08 onward are not present.
- Committee votes, secret votes, negotiations, motives, and vote justifications are not represented by these records.
- A historical source-build step produced party positions. The current `scripts/aggregate_votes.py` transforms committed party-position input but does not reconstruct the upstream source snapshot.

Voting patterns in `party_patterns.json` exclude procedural votes and the `justicia` category, but they include declarative votes. They must not be described as statistics over substantive votes only.

## Promise Evidence

- The repository contains 345 extracted 2021 promises and 246 extracted 2026 proposals across nine tracked parties.
- Extraction and review included language-model assistance and human judgment.
- Source-page values are approximate extraction-batch locations, not verified exact citations.
- 590 of 591 promise records do not contain a usable source quotation.
- `data/03_evidence/promise_extraction_audit.md` records a dated audit that removed 37 potential hallucinations from the 2026 set.

Until exact page and quotation evidence is added, public claims must not describe every promise as fully traceable to an exact passage.

## AMPAY Evidence

- Five contradiction records are currently confirmed.
- Confirmed records cite substantive vote IDs and are validated against committed vote and party-position files.
- The list is evidence from the available period, not a complete assessment of any party.
- Missing legislation, incomplete vote coverage, ambiguous promise language, or unmatched terminology can produce false negatives.
- Vote records do not establish political motive or the full legislative context.

## Quiz Data

- The committed quiz dataset contains 15 statements and two calibration questions.
- Party positions are manually coded interpretations of plan material and require continuing source review.
- A quiz match measures similarity to coded positions. It is not an endorsement, forecast, or assessment of integrity.
- The scoring runtime is owned by the consuming frontend. This repository's simulation must be kept aligned with that runtime before its results are cited.

## Privacy and Reuse

- Extracted plan text must not publish identity numbers from digital-signature blocks. Run `python3 scripts/validate_source_privacy.py` before publication.
- Public availability of a source does not by itself establish a reuse license. See `docs/data/DATA_SOURCES.md` and retain primary-source attribution.
- Completeness and accuracy percentages are not claimed without a reproducible measurement and dated evidence.
