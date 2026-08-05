# Party Profile Data Owners

**Status:** ROUTING

This document intentionally does not duplicate candidate names, ideological labels, voting percentages, or AMPAY counts. Those values change independently and previously drifted from the committed datasets.

## Current Owners

| Fact | Authoritative owner |
|---|---|
| Tracked party slugs and display names | `scripts/ampay_pipeline/parties.py` |
| Category and monthly voting patterns | `data/02_output/party_patterns.json` |
| Confirmed contradiction evidence | `data/02_output/AMPAY_CONFIRMED_2021.json` |
| Public AMPAY projection | `data/02_output/ampays.json` |
| Extracted 2021 and 2026 proposals | `data/01_input/promises/` |
| Data coverage and interpretation limits | `docs/data/DATA_LIMITATIONS.md` |

Consumers must calculate current figures from these files rather than copying them into prose. `python3 scripts/validate_current_outputs.py` verifies the current party, vote, and AMPAY output contracts.

## Scope Limitation

The repository tracks nine party slugs. It does not currently document an election-wide inclusion rule proving that these are all eligible or relevant parties for the 2026 election. Candidate identity and current party status are therefore outside this document's authority and require a current electoral source.
