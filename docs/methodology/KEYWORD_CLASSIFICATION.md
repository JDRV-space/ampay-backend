# Vote Categorization Provenance

**Status:** ACTIVE WITH PROVENANCE LIMITATION

`data/02_output/votes_categorized.json` contains 2,226 plenary vote records assigned to 15 thematic categories and one of three vote types. Its committed summary reports:

- 936 substantive records;
- 1,149 procedural records;
- 141 declarative records;
- 40 low-confidence records, all marked as fallbacks.

## Current Contract

Each record contains a primary category, optional secondary category, vote type, confidence, reasoning, detected keywords, date, subject, and stable vote ID. `python3 scripts/validate_current_outputs.py` recomputes the record count and vote-type distribution from the committed records.

## Provenance Limitation

The repository retains more than one historical classification path:

- `scripts/legacy/phase_1_3_vote_classification.py` contains deterministic keyword rules.
- `scripts/legacy/classify_votes.py` contains a language-model workflow with fallback classification.
- The committed output includes fallback records and free-form reasoning.

Repository evidence does not establish one reproducible command that generated the exact committed file. The output must therefore not be described as fully deterministic or as containing no language-model assistance.

The current JSON is the authority for published classifications. Rebuilding it requires a separately reviewed pipeline and a diff against the committed output.
