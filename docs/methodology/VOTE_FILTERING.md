# Vote-Type Classification

**Status:** ACTIVE

The committed vote dataset retains substantive, procedural, and declarative plenary records. Vote type controls which records may support a confirmed AMPAY.

## Types

| Type | Current records | Meaning |
|---|---:|---|
| Substantive | 936 | A decision with direct legislative or policy effect |
| Procedural | 1,149 | A decision about process, scheduling, admission, reconsideration, or procedure |
| Declarative | 141 | A symbolic declaration or recognition without direct policy implementation |
| Total | 2,226 | All committed categorized plenary records |

These counts are derived from `data/02_output/votes_categorized.json` and checked by `python3 scripts/validate_current_outputs.py`.

## AMPAY Rule

Only records classified as substantive may appear in a confirmed AMPAY's `evidence.vote_references`. `scripts/validate_ampay_traceability.py` enforces that rule and preserves the removal evidence for AMPAY-003, whose cited votes were procedural.

The dataset itself is not filtered down to substantive records. Interfaces may display other vote types, but they must label the type and must not describe all 2,226 records as substantive.

## Provenance Limitation

The exact historical classifier is not fully reproducible from one current command. See `docs/methodology/KEYWORD_CLASSIFICATION.md` for the deterministic and language-model-assisted paths retained in the repository.
