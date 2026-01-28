# DATA DISCLAIMER

## CRITICAL: INCOMPLETE VOTING DATA

### What We Have

| Data | Coverage | Source |
|------|----------|--------|
| Congressional votes | 2021-07-26 to 2024-07-26 | [openpolitica](https://github.com/openpolitica/congreso-pleno-asistencia-votacion) |
| Party promises | 2021 election | Official JNE plans de gobierno |

### What We're Missing

| Data | Period | Impact |
|------|--------|--------|
| Congressional votes | 2024-07-27 to 2026-07-26 | **2 YEARS NOT ANALYZED** |

### Implications

1. **AMPAYs detected (6) are based on ~60% of the congressional term**
2. **Additional contradictions may exist in 2024-2026 votes**
3. **Some parties marked "0 AMPAYs" may have contradictions in unanalyzed period**
4. **Results are PROVISIONAL until complete 2021-2026 data is available**

### Recommendation

- Clearly communicate this limitation to users
- Update analysis when complete voting data becomes available
- Consider adding "Data coverage: 2021-2024" badge on UI

### Source Verification

```
Repository: https://github.com/openpolitica/congreso-pleno-asistencia-votacion
Last commit checked: 2024-07-26
Data structure: /data/2021-2026/YYYY/MM/DD/
Earliest vote: 2021-07-26
Latest vote: 2024-07-26
```

---

**This disclaimer must be prominently displayed in any public-facing application using this data.**
