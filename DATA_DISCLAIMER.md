# Data Disclaimer

## Voting Data Is Incomplete

### What This Repo Has

| Data | Coverage | Source |
|------|----------|--------|
| Congressional votes | 2021-07-26 to 2024-03-07 | [OpenPolitica](https://github.com/openpolitica/congreso-pleno-asistencia-votacion) |
| Party promises | 2021 election | Official JNE plans de gobierno |

### What Is Missing

| Data | Period | Impact |
|------|--------|--------|
| Congressional votes | 2024-03-08 onward | Not analyzed here |

### What This Means

1. The 5 committed AMPAY records are based on about 52% of the congressional term by calendar duration.
2. Additional contradictions may exist in 2024-2026 votes.
3. Parties marked with 0 AMPAYs may have contradictions in the unanalyzed period.
4. LLM-assisted extraction, classification, and contradiction detection need human audit.
5. Public claims based on this repo should state the coverage limit.
6. This data should not be treated as final election advice.

### If You Use This Data Publicly

- State that congressional vote coverage stops on 2024-03-07.
- Do not imply the AMPAY list is complete.
- Audit LLM-generated records before making claims about a party or candidate.
- Update the analysis when complete 2021-2026 voting data is available.

### Source Verification

```
Repository: https://github.com/openpolitica/congreso-pleno-asistencia-votacion
Upstream snapshot: not pinned in this repository
Upstream data structure: /data/2021-2026/YYYY/MM/DD/
Earliest vote: 2021-07-26
Latest committed vote: 2024-03-07
```

Any public-facing use of this data should show this limitation near the claim it supports.

### Source Privacy

Extracted plan text preserves policy content but redacts national identity
numbers found in digital-signature blocks. Run
`python3 scripts/validate_source_privacy.py` before publishing refreshed source
text.
