# AMPAY Backend

This repo contains the data side of AMPAY: source extracts, LLM prompts, Python scripts, and committed JSON outputs used for a Peruvian political accountability data pipeline.

The scope is the committed data pipeline and public methodology for the current AMPAY records. Reproducibility is limited by source availability, extracted PDF text quality, external model access, and historical source snapshots. The repository does not provide election advice.

## What Is Here

- `data/01_input/`: extracted source material and intermediate inputs.
- `data/01_input/promises/2021/`: 9 party files with 345 extracted 2021 campaign promises.
- `data/01_input/promises/2026/`: 9 party files with 246 extracted 2026 proposals.
- `data/01_input/votes/`: congressional vote inputs used by the aggregation scripts.
- `data/02_output/`: committed JSON and Markdown outputs consumed by downstream work.
- `data/03_evidence/`: dated audits and historical analyses that do not own current outputs.
- `prompts/`: historical prompt templates retained for audit context. No current prompt runner is committed.
- `scripts/`: current Python entrypoints that read from `data/01_input/` or validate `data/02_output/`.
- `scripts/ampay_pipeline/`: shared path and party identity rules used by current scripts.
- `scripts/legacy/`: historical source-build scripts retained for audit context. These are not current public entrypoints.
- `docs/`: public methodology, data, reference, and legal documentation for the committed outputs.

## Committed Outputs

| Path | What it contains |
|---|---|
| `data/02_output/ampays.json` | 5 AMPAY contradiction records with vote ID references. |
| `data/02_output/AMPAY_CONFIRMED_2021.json` | More detailed evidence for the confirmed 2021 AMPAY records. |
| `data/02_output/votes_categorized.json` | 2,226 categorized congressional votes. |
| `data/02_output/votes_by_party.json` | Party-level positions for 2,226 votes across 9 parties. |
| `data/02_output/party_patterns.json` | Monthly/category voting patterns for 9 parties. |
| `data/02_output/quiz_statements.json` | 15 quiz statements with party positions. |

The outputs are committed so they can be inspected without running the pipeline.

Historical v4 candidate analyses and the promise and quiz-position audits are preserved under `data/03_evidence/`. They must not be consumed as current public outputs.

## Data Coverage

| Data | Coverage | Notes |
|---|---|---|
| Congressional votes | 2021-07-26 to 2024-03-07 | From OpenPolitica data present in this repo. Later votes are missing. |
| 2021 party promises | 9 parties, 345 extracted items | Extracted from JNE campaign plan material. |
| 2026 party proposals | 9 parties, 246 extracted items | Extracted from JNE campaign plan material. |

The voting data covers about 52% of the 2021-2026 congressional term by calendar duration. Anything from 2024-03-08 onward is not analyzed here.

## Reproducibility

What is reproducible now:

- You can inspect the committed outputs in `data/02_output/`.
- You can inspect the prompts in `prompts/`.
- You can inspect the extracted source text and promise JSON files under `data/01_input/`.
- `scripts/validate_current_outputs.py` validates traceability for the committed AMPAY records.
- `scripts/aggregate_votes.py` and `scripts/compute_patterns.py` regenerate derived vote outputs from committed vote inputs. They may overwrite committed outputs.
- `scripts/quiz_simulation.py` runs Monte Carlo validation for the quiz matching data. It may overwrite committed validation output.

What is not reproducible out of the box:

- The full source-to-output pipeline is not currently one clean command.
- LLM-dependent stages require external API access and will not be deterministic.
- Historical scripts under `scripts/legacy/` may reference older source-build paths such as `data/promises.json`, `data/congress/`, or `data/pdfs/`.
- The exact committed outputs may depend on source data snapshots, API keys, model behavior, and local paths that are not fully captured here.

## Setup

```bash
git clone https://github.com/JDRV-space/ampay-backend.git
cd ampay-backend
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install --require-hashes -r requirements.lock
```

`requirements.txt` declares direct dependency ranges.
`requirements.lock` pins the reviewed Python 3.12 environment. Regenerate it
with:

```bash
uv pip compile --python-version 3.12 --generate-hashes \
  requirements.txt --output-file requirements.lock
```

Current scripts share path constants through `scripts/ampay_pipeline/paths.py`. Run them from the repo root.

Examples that use committed files:

```bash
python3 scripts/validate_current_outputs.py
python3 scripts/aggregate_votes.py
python3 scripts/compute_patterns.py
python3 scripts/quiz_simulation.py 42
```

Do not run these in a dirty checkout unless you are comfortable reviewing output diffs afterwards.

## Limitations

- LLM-assisted extraction, classification, and contradiction detection need human audit.
- The 5 AMPAY records are evidence packages from a limited dataset, not proof that the list is complete.
- Confirmed AMPAY records must cite stable vote IDs in `vote_references`; free-text law names are labels, not source keys.
- A party with 0 AMPAYs in this repo may still have contradictions in unanalyzed votes.
- Public claims based on this repo should mention the 2021-07-26 to 2024-03-07 vote coverage limit.
- Public claims should not be treated as final election advice.

## Documentation Ownership

Committed datasets and validation scripts own counts, date ranges, and generated outputs. Runtime code owns implemented behavior; methodology documents describe only verified current algorithms. Privacy, legal, and deployment claims require verification against the deployed product and its responsible owner.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Attribution notices are listed in [NOTICE](NOTICE).
