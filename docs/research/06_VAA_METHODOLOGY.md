# VAA Methodology Research

*Research date: 2026-01-21*

## How VAAs Derive Party Positions

| VAA | Method | Process |
|-----|--------|---------|
| **Wahl-O-Mat** | Party Self-Placement | Parties respond agree/disagree/neutral to 30-40 theses |
| **Vote Compass** | Expert Coding + Party Review | Academics code manifestos, send to parties for calibration |
| **Kieskompas** | Triangulation | Expert surveys + manifesto analysis + party self-placement |
| **iSideWith** | Proprietary | Voting records + speeches + "conviction score" |

## How VAAs Collect User Input

| VAA | User Input Method |
|-----|-------------------|
| **Wahl-O-Mat** | 38 theses, user picks: agree / neutral / disagree |
| **Vote Compass** | 30 statements, 5-point Likert scale (strongly agree to strongly disagree) |
| **Smartvote** | 75 questions, agree/disagree + optional "important" flag (2x weight) |
| **iSideWith** | Variable questions, yes/no + importance weighting |

## Standard VAA User Scales

```
Most common: 3-point or 5-point

3-POINT (Wahl-O-Mat style):
  +1 = Agree
   0 = Neutral
  -1 = Disagree

5-POINT (Vote Compass style):
  +2 = Strongly agree
  +1 = Agree
   0 = Neutral
  -1 = Disagree
  -2 = Strongly disagree

WEIGHTING (optional):
  User marks issue as "important" → 2x multiplier
```

## MARPOR Manifesto Coding (Academic Standard)

**Process:**
1. Break manifesto into quasi-sentences (one policy idea each)
2. Assign each to ONE of 56 categories
3. Count frequency per category as % of total
4. Calculate scores (e.g., RILE for left-right)

**Key distinction:** MARPOR measures SALIENCE (emphasis), not POSITION (stance).

## Converting Promises to Stances

**For positional coding (+2 to -2):**

| Score | Meaning | Indicators |
|-------|---------|------------|
| +2 | Strongly supports | Explicit commitment, repeated, "WILL do X" |
| +1 | Supports | Mentioned favorably, implies approval |
| 0 | Neutral | Not mentioned or ambiguous |
| -1 | Opposes | Mentioned negatively, implies disapproval |
| -2 | Strongly opposes | Explicit rejection, repeated opposition |

**Decision rules:**
- Explicit verb = stronger score ("We WILL" = +2 vs "We support" = +1)
- Frequency: 5+ mentions = stronger score
- Conditionality weakens: "If budget allows" = lower intensity

## Recommended Approach for AMPAY

**For party positions (from promises):**
```
1. Each promise has: category + action_verb
2. Code direction:
   - aumentar/expandir/crear/fortalecer → +1
   - reducir/eliminar/recortar → -1
3. Aggregate per category:
   stance = (sum of directions) / (count in category)
4. Normalize to -1 to +1 range
```

**For user input:**
```
Standard VAA approach:
- 20-40 specific STATEMENTS (not categories)
- User rates: agree/neutral/disagree
- Optional importance weighting (2x)
```

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Saved for audit trail*
