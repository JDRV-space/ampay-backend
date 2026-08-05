# Data Sources

**Status:** ACTIVE

This registry identifies the provenance owners for committed AMPAY data. It does not claim that every source is open-licensed or that the repository contains a complete upstream snapshot.

## Congressional Votes

| Field | Value |
|---|---|
| Upstream project | [openpolitica/congreso-pleno-asistencia-votacion](https://github.com/openpolitica/congreso-pleno-asistencia-votacion) |
| Committed coverage | 2021-07-26 through 2024-03-07 |
| Committed records | 2,226 plenary vote records |
| Local categorized input | `data/01_input/votes/votes_categorized.json` |
| Local party-position input | `data/01_input/votes/party_positions.json` |
| Current projections | `data/02_output/votes_categorized.json`, `votes_by_party.json`, and `party_patterns.json` |

The upstream revision is not pinned in this repository. The local records, not the current upstream default branch, own the published coverage date. No upstream license was identified in the committed provenance material, so reuse terms remain unresolved.

## Government Plans

`data/01_input/pdfs/PDF_URLS.md` owns the exact plan URLs recorded by the project. Extracted text is under `data/01_input/pdfs/text/`, and structured promises are under `data/01_input/promises/`.

The registry includes official electoral sources and some third-party mirrors. Each public claim should cite the primary document when available. Availability and HTTP success do not prove document identity, integrity, or reuse permission.

## Derived Data

| Dataset | Immediate owner |
|---|---|
| Categorized votes | `data/02_output/votes_categorized.json` |
| Party vote positions | `data/02_output/votes_by_party.json` |
| Voting patterns | `data/02_output/party_patterns.json` |
| Quiz statements | `data/02_output/quiz_statements.json` |
| Confirmed AMPAY evidence | `data/02_output/AMPAY_CONFIRMED_2021.json` |
| Public AMPAY projection | `data/02_output/ampays.json` |

Derived outputs inherit the source limitations documented in `docs/data/DATA_LIMITATIONS.md`. The Apache-2.0 license covers original repository work; it does not automatically relicense third-party source material.
