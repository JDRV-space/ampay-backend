# Contributing

Contributions that improve reproducibility, source traceability, privacy, or factual accuracy are welcome.

## Before Opening a Pull Request

1. Base factual political-data corrections on a primary source and identify the affected record or vote ID.
2. Do not add identity numbers, credentials, private correspondence, or unsupported claims about motive or ideology.
3. Keep generated counts and dates in data files and validators rather than copying them into prose.
4. Run:

```bash
python3 scripts/validate_source_privacy.py
python3 scripts/validate_current_outputs.py
```

If changing quiz behavior, also run `python3 scripts/quiz_simulation.py 42` and explain whether the consuming frontend must be updated.

## Data Corrections

State the current value, proposed value, primary-source URL, and why the source supports the change. An available source is not necessarily licensed for redistribution; note any reuse restriction you identify.

## Scope

AMPAY is an informational project. Contributions must not add party endorsements, voting recommendations, campaign advocacy, or unsupported allegations.
