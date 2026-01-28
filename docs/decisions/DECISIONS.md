# AMPAY - Technical Decisions

*Session: 2026-01-21*

---

## Scoring Algorithm

**CONFIRMED: +1 / 0 / -1 system**

```
Per CATEGORY, per PARTY:

Count all SI votes in category
Count all NO votes in category

IF SI > NO  →  +1 (favor)
IF NO > SI  →  -1 (against)
IF SI = NO  →   0 (divided/neutral)
IF no votes →  null (no data)
```

**Rationale:** Simple, binary positions. User sees clear stance per party per issue.

---

## Data Filtering

### Abstentions
**Decision:** IGNORE

- Only count SI and NO votes
- Abstentions = no recorded position
- Score = SI / (SI + NO)

### Declarative Votes
**Decision:** FILTER OUT

- "Declarar Día del X" = zero policy impact
- Only count substantive votes (budget, policy, law changes)
- LLM will classify each asunto as: `substantive` or `declarative`

### Category Overlap
**Decision:** ONE MAIN CATEGORY

- Each vote assigned to ONE primary category
- No double-counting across categories
- LLM prompt: "Pick the MAIN category, only one"

### Vote Context Limitation
**Decision:** ACCEPT + AGGREGATE

- We cannot know WHY someone voted NO (clause vs concept)
- Acknowledge in methodology page
- Use party aggregate (majority vote = party position)

---

## Categories

**CONFIRMED: 15 categories**

```
seguridad, economia, fiscal, social, empleo, educacion, salud,
agua, vivienda, transporte, energia, mineria, ambiente, agricultura, justicia
```

### Future Exploration: Subcategories
- Manifesto Project uses 56 subcategories
- Could map our 15 to their system for precision
- Example: educacion → education_expansion, education_quality, education_spending
- **Status:** Explore post-MVP

---

## Contradiction Detection (AMPAY! Feature)

**Decision:** ADD TO PIPELINE

**How it works:**
```
Input A: Promise text ("Aumentaremos presupuesto educación")
Input B: Vote asunto ("Ley que reduce presupuesto educación")
         ↓
Claude Haiku (reasoning + Spanish context)
         ↓
Output: ALIGNED / NEUTRAL / CONTRADICTION
         ↓
IF Contradiction → Flag as AMPAY! candidate
```

**Why Claude Opus:**
- Best reasoning available
- Understands Spanish + Peru context deeply
- Can explain WHY it's a contradiction
- Outputs must withstand public scrutiny
- Accuracy > cost for political transparency

**Status:** Implement in pipeline

---

## ManifestoBERTa

**Status:** DROPPED

**Reason:**
- Fine-tuned on European political text (UK, Germany, etc.)
- Training data is mostly English/European languages
- Zero Peru-specific political terminology
- Won't understand "canon minero", Peruvian context, local slang
- Gemini/Haiku are better for Spanish + Peru context

---

## Centrality Weighting

**What:** Weight promises by voter importance

| Promise | Weight |
|---------|--------|
| "Fix economy" | HIGH (voters care) |
| "Rename street" | LOW (nobody cares) |

**Implementation options:**
| Approach | Effort | Accuracy |
|----------|--------|----------|
| Copy existing weights (Mellon 2023) | Low | Medium (not Peru-specific) |
| Survey Peruvian voters | High | High |
| Media mention proxy | Medium | Medium |
| Equal weight (skip) | Zero | Low |

**Decision:** Skip for MVP. All promises weighted equally.

**Status:** Explore post-MVP if app gains traction

---

## Quiz Logic

**CONFIRMED: Quiz v2.0 - Calibration + 8 statements (UPDATED 2026-01-21)**

```
USER FLOW:
1. [CALIBRATION] 2 ideology self-ID questions (FILTER, not in distance calc)
   - C1: "En temas economicos, te consideras izquierda/centro/derecha?"
   - C2: "En temas sociales, te consideras conservador/moderado/progresista?"
   - Purpose: FILTERS which parties appear in primary results
2. [SCORED] 8 policy statements (one at a time)
3. User rates each: De acuerdo (+1) / Neutral (0) / En desacuerdo (-1)
4. System calculates match using Manhattan distance
5. Show TOP 3 matches with percentages
6. "Ver detalle" shows WHY (which questions drove match)
7. Warning if results contradict self-ID
```

**Why calibration questions (HYBRID approach):**
- Prevents user rage when results contradict self-identity
- HYBRID: Show matches within self-ID first, suggest others second

```
RESULTS DISPLAY:

"Dentro de tu perfil:" (filtered by self-ID)
  Fuerza Popular (78%)
  Renovacion Popular (71%)
  Avanza Pais (65%)

"Tambien podrias considerar:" (if policy match outside self-ID)
  Segun tus respuestas, tambien tienes coincidencias con
  Juntos por el Peru (72%)
```

- User sees "safe" results first (within their stated ideology)
- Still surfaces true policy matches as suggestion
- No rage, no echo chamber

**8 Statements (3 axes):**
```
ECONOMIC (4):
Q01: Impuesto sobreganancias mineras
Q02: Revisar TLCs
Q03: PetroPeru operar lotes
Q04: Fortalecer sindicatos

SOCIAL (2):
Q05: AFP vs pensiones estatales
Q06: Control inmigracion venezolana

GOVERNANCE (2):
Q07: Asamblea Constituyente
Q08: Descentralizacion (mas poder a regiones)
```

**Removed consensus questions (zero discriminatory power):**
- Intangibilidad Amazonia (all parties +1)
- Cobertura universal agua (all parties +1)
- Eliminar burocracia MYPEs (all parties +1)

**Party Positions Source:**
```
DECISION: Use 2026 PROMISES only (not voting records)

Rationale:
- Quiz is for 2026 election → use 2026 proposals
- Voting records are 2021-2024 (old data)
- AMPAY feature already covers promise vs vote gaps
- Simpler, faster to ship for 2-person team

Data file: data/02_output/quiz_statements.json
```

**Results display:**
```
Tu mejor coincidencia:
  Fuerza Popular (78%)

Tambien similar:
  Renovacion Popular (71%)
  Avanza Pais (65%)

[Ver detalle] → Shows breakdown by question
```

**Algorithm (based on Wahl-O-Mat, Smartvote):**
```
For each party:
  distance = sum(|user_position - party_position|)
  match% = 100 - (distance / max_possible_distance * 100)
```

**Sources:**
- Wahl-O-Mat: https://www.wahl-o-mat.de/
- Smartvote: https://www.smartvote.ch/
- Vote Compass: https://votecompass.com/

**Research file:** See docs/research/06_VAA_METHODOLOGY.md

**Decision history:**
- v1.0: 15 categories with +1/-1 selection (critic: 6/20 - FATAL)
- v1.1: 12 statements with Agree/Neutral/Disagree (critic: 7/20 - major issues)
- v2.0: 2 calibration + 8 statements + top 3 results + breakdown (CURRENT)
- Key fix: Added ideology calibration to prevent user rage
- Reviewed: @critic agent 2026-01-21

---

## Tools & Models

**PRIMARY: Claude Opus ONLY**

| Task | Model |
|------|-------|
| Categorize asuntos | Opus |
| Categorize promises | Opus |
| Contradiction detection | Opus |
| Declarative vs Substantive | Opus |
| Promise-vote matching | Opus |

**Rationale:**
- Political transparency = high stakes
- Every output will be audited/scrutinized
- Must justify using smartest LLM available
- Accuracy > cost for this use case
- No room for errors in public-facing political data

**Dropped:**
- Haiku (not smart enough for auditable outputs)
- Sonnet (not smart enough for auditable outputs)
- Gemini Flash (keep Claude-only stack)
- ManifestoBERTa (English-trained, no Peru context)

---

## Open Items (Explore Later)

- [ ] Subcategories (56 vs 15)
- [ ] Centrality weighting (Peru-specific voter surveys)
- [ ] Spanish-specific NLI model for contradiction detection

---

## Summary Table

| Decision | Choice | Status |
|----------|--------|--------|
| Scoring | +1 / 0 / -1 | CONFIRMED |
| Abstentions | Ignore | CONFIRMED |
| Declarative votes | Filter out | CONFIRMED |
| Category overlap | One main | CONFIRMED |
| Vote context | Accept limitation | CONFIRMED |
| Categories | 15 | CONFIRMED |
| Subcategories | Explore later | DEFERRED |
| Contradiction detection | Claude Opus | IMPLEMENTED |
| Centrality weighting | Skip MVP | CONFIRMED |
| Quiz | v2.0: calibration + 8 statements | CONFIRMED |
| LLM stack | Opus only | CONFIRMED |
| ManifestoBERTa | DROPPED | N/A |
| Gemini Flash | DROPPED | N/A |

---

## Success Rate Display

**CONFIRMED: Per category + Overall**

```
PARTY X:
├── Overall: 65%
├── seguridad: 80%
├── economia: 45%
├── educacion: 70%
├── salud: 60%
├── fiscal: 55%
├── social: 75%
├── empleo: 40%
├── agua: 90%
├── vivienda: 50%
├── transporte: 60%
├── energia: 70%
├── mineria: 30%
├── ambiente: 65%
├── agricultura: 80%
└── justicia: 55%
```

**Rationale:** Users care about specific issues, not just overall score.

---

## Success Rate Algorithm

**CONFIRMED: Based on Polimeter methodology**

**Rating scale:**
```
KEPT      → Party voted in line with promise
BROKEN    → Party voted against promise (= AMPAY!)
PARTIAL   → Mixed votes (some aligned, some not)
NO DATA   → No related votes found
```

**Formula:**
```
Success Rate = (Kept + 0.5*Partial) / (Kept + Partial + Broken)
```

**Example:**
- 8 Kept + 4 Partial + 5 Broken
- Rate = (8 + 2) / (8 + 4 + 5) = 59%

**Process:**
```
For each PROMISE:
  1. Opus finds related VOTES (semantic match)
  2. Check: Did party vote in line with promise?
  3. Assign: KEPT / BROKEN / PARTIAL / NO DATA
  4. Human reviews sample for accuracy
```

**Sources (methodology based on):**
- PolitiFact: https://www.politifact.com/article/2018/feb/12/principles-truth-o-meter-politifacts-methodology-i/
- Polimeter: https://www.poltext.org/en/donnees-et-analyses/les-polimetres/methodology-polimeters
- CPPG (academic): https://comparativepledges.net/
- Thomson et al. 2017: https://onlinelibrary.wiley.com/doi/abs/10.1111/ajps.12313
- Mellon et al. 2023: https://journals.sagepub.com/doi/full/10.1177/00323217211027419

**Research file:** See RESEARCH_PROMISE_FULFILLMENT.md

---

## Auditability

**CONFIRMED: Full transparency**

Every AMPAY shows:
```
┌─────────────────────────────────────────────────┐
│ PROMISE:                                        │
│ "Aumentaremos el presupuesto de educación 10%"  │
│ 📄 Source: Plan de Gobierno 2021, pág. 47       │
│ 🔗 PDF: jne.gob.pe/fp-plan-2021.pdf             │
├─────────────────────────────────────────────────┤
│ VOTE:                                           │
│ "Ley que incrementa presupuesto educación"      │
│ 📅 Date: 2023-05-15                             │
│ ❌ Party voted: NO                              │
│ 🔗 Raw data: github.com/ampay/data/...          │
├─────────────────────────────────────────────────┤
│ WHY CONTRADICTION:                              │
│ "Prometieron aumentar, votaron en contra"       │
│ 🤖 Analyzed by: Claude Haiku, 2026-01-21        │
├─────────────────────────────────────────────────┤
│ ⚠️ ¿Error? github.com/ampay/issues              │
└─────────────────────────────────────────────────┘
```

**Transparencia de datos:**
- Datos gubernamentales de fuentes publicas
- Metodologia completamente documentada
- Fuentes verificables
- Pagina de metodologia explica todo el proceso

---

## Vote URLs

**FINDING: No direct URLs available**

Congress doesn't provide clean URLs to individual voting sessions.

**Solution:**
| Source | Link |
|--------|------|
| Congress archive (general) | congreso.gob.pe/AsistenciasVotacionesPleno/ |
| Our raw data | github.com/ampay/data/openpolitica/YYYY/MM/DD/ |
| openpolitica source | github.com/openpolitica/congreso-pleno-asistencia-votacion |

**Audit method:** User can verify by date + asunto in Congress archive.

---

## Frontend Stack

**CONFIRMED: Next.js 14 + Tailwind + shadcn/ui**

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | Next.js 14 (App Router) | Vercel native, best SEO |
| Styling | Tailwind CSS | Fast, utility-first |
| Components | shadcn/ui | Pro look, accessible |
| Hosting | Vercel | Free tier, fast |
| Export | Static | No server needed |

---

## Domain

**CONFIRMED: ampayperu.com**

---

## Confidence Handling

**CONFIRMED: Threshold system**

```
OPUS OUTPUT per match:
{
  "match": "CONTRADICTION",
  "confidence": 0.85,
  "reasoning": "Promise says X, vote was opposite"
}

RULES:
├── confidence >= 0.9  →  Auto-publish
├── confidence 0.7-0.9 →  Flag for human review
├── confidence < 0.7   →  Discard (too uncertain)
```

**UI behavior:**
- Only show high-confidence AMPAYs to users
- No confidence score shown publicly (confusing)
- Internal dashboard shows all for QA

---

## Human Review (QA)

**CONFIRMED: Sample before launch**

```
PROCESS:
1. Run Opus on ALL data
2. Sample 50 random AMPAYs
3. Human verifies each:
   - Promise source correct?
   - Vote data correct?
   - Contradiction logic makes sense?
4. If >90% accurate → launch
5. If <90% → fix prompts, re-run, re-sample
```

**Reviewer:** JD + 1-2 trusted people

---

## Edge Cases

**CONFIRMED: Not an issue**

**Party switches:**
- openpolitica data has `grupo_parlamentario` per vote
- This is the party AT TIME OF VOTE
- If congressman switched, each vote shows correct party
- No special handling needed

**Party splits/merges:**
- Same logic - use party at time of vote
- Historical accuracy preserved

---

## Data Refresh

**CONFIRMED: One-time snapshot**

- Pre-election snapshot only
- No periodic updates for MVP
- Data covers: 2021 promises + 2021-2026 votes + 2026 proposals
- Future: Consider updates if app gains traction

---

## Features (MVP)

**CONFIRMED:**

```
CORE:
✅ Quiz - match user to party
✅ Auditoría - 2021 promises vs votes
✅ Propuestas 2026 - party proposals
✅ AMPAY! - contradictions
✅ Methodology - how we did it
✅ Party profiles - page per party
✅ Search - by topic, party, keyword
✅ Share - social sharing

EXTRAS:
✅ Download data - CSV/JSON for journalists
✅ Stats dashboard - aggregated charts
✅ Embed widget - for other sites
✅ Dark mode
✅ Audit page - full transparency (data trail + methodology)

DROPPED:
❌ API - risk blowing Vercel free tier
```

---

## Audit Page

**CONFIRMED: Both (data trail + methodology)**

```
/audit page includes:

1. DATA AUDIT TRAIL:
   - Raw data sources (links to JNE, Congress)
   - LLM reasoning for each AMPAY
   - Timestamps of analysis
   - Version history

2. METHODOLOGY DEEP-DIVE:
   - How we extracted promises
   - How we categorized votes
   - How we detected contradictions
   - Confidence thresholds
   - Limitations acknowledged
```

---

## Launch Strategy

**CONFIRMED: Soft launch first**

```
PHASE 1: Soft launch
- Share with small trusted group (10-20 people)
- Collect feedback
- Fix critical bugs
- Verify data accuracy

PHASE 2: Public launch
- Social media announcement
- Press outreach (if relevant)
- Full public access
```

---

## Language

**CONFIRMED: Spanish only**

- Quechua is oral, not written standard
- Target audience reads Spanish
- No translation needed for MVP

---

## Page Routes

**CONFIRMED:**

```
/                     → Landing + Quiz start
/quiz                 → Quiz flow
/resultados           → Quiz results
/partidos             → All parties list
/partidos/[slug]      → Party profile (e.g., /partidos/fuerza-popular)
/auditoria            → Auditoría overview (promises vs votes)
/ampays               → All contradictions
/propuestas-2026      → 2026 proposals by party
/metodologia          → Methodology page
/audit                → Data audit trail
/buscar               → Search
/descargar            → Download data
/stats                → Stats dashboard
```

---

## JSON Schema / Data Structure

**CONFIRMED: Popolo/OCD + Custom**

```
/ampay/data/
├── parties.json      → Popolo standard
├── votes.json        → Popolo standard
├── promises.json     → Custom (we create)
├── ampays.json       → Custom (we create)
└── scores.json       → Custom (we create)
```

**Dual purpose:**
- App reads these files to display info
- Anyone can download to verify/audit
- GitHub tracks all changes

**Field definitions:**

```json
// parties.json
{
  "id": "fuerza-popular",
  "name": "Fuerza Popular",
  "abbreviation": "FP",
  "candidate_2026": "Keiko Fujimori",
  "seats_2021": 24,
  "logo_url": "/logos/fp.png",
  "color": "#FF6B00",
  "positions": {
    "educacion": 1,
    "salud": -1
  },
  "success_rate": {
    "overall": 59,
    "educacion": 45
  }
}

// promises.json
{
  "id": "fp-edu-001",
  "party_id": "fuerza-popular",
  "text": "Aumentar presupuesto educación 10%",
  "category": "educacion",
  "year": 2021,
  "status": "BROKEN",
  "source": {
    "pdf_url": "jne.gob.pe/fp-2021.pdf",
    "page": 47,
    "extracted_by": "pymupdf"
  }
}

// ampays.json
{
  "id": "ampay-001",
  "promise_id": "fp-edu-001",
  "party_id": "fuerza-popular",
  "vote_date": "2023-05-15",
  "vote_asunto": "Ley presupuesto educación",
  "party_voted": "NO",
  "reasoning": "Prometió aumentar, votó en contra",
  "confidence": 0.92
}
```

**Note:** Page numbers tracked programmatically by PyMuPDF, not by LLM.

**Sources:**
- Popolo Project: https://www.popoloproject.com/specs/
- Open Civic Data: https://open-civic-data.readthedocs.io/
- Schema.org ClaimReview: https://schema.org/ClaimReview

**Research file:** See RESEARCH_JSON_SCHEMA.md, example_schemas.json

---

## PDF Extraction

**CONFIRMED: PyMuPDF + Tesseract + Claude fallback**

```
PDF Input
    |
    v
[Detect Type] --> Native text? --> PyMuPDF (fast)
    |                                  |
    v                                  v
Scanned? --> Tesseract OCR (spa) --> [Validate]
    |                                  |
    v                                  v
Low quality? --> Claude API --> [Output]
```

**Tools:**
| Tool | Use for | Cost |
|------|---------|------|
| PyMuPDF | Native PDFs | Free |
| Tesseract + spa | Scanned pages | Free |
| Claude API | Complex layouts, fallback | ~$0.38/50 pages |

**Chunking:** Page-level (best for government docs)

**Sources:**
- PyMuPDF: https://pymupdf.readthedocs.io/
- Tesseract Spanish: https://github.com/tesseract-ocr/tessdata
- Claude PDF support: https://docs.claude.com/en/docs/build-with-claude/pdf-support

**Research file:** See RESEARCH_PDF_EXTRACTION.md

---

## Updated Summary Table

| Decision | Choice | Status |
|----------|--------|--------|
| Scoring | +1 / 0 / -1 | CONFIRMED |
| Abstentions | Ignore | CONFIRMED |
| Declarative votes | Filter out | CONFIRMED |
| Category overlap | One main | CONFIRMED |
| Vote context | Accept limitation | CONFIRMED |
| Categories | 15 | CONFIRMED |
| Subcategories | Explore later | DEFERRED |
| Contradiction detection | Claude Opus | IMPLEMENTED |
| Centrality weighting | Skip MVP | CONFIRMED |
| Quiz | v2.0: calibration + 8 statements | CONFIRMED |
| LLM stack | Opus only | CONFIRMED |
| ManifestoBERTa | DROPPED | N/A |
| Gemini Flash | DROPPED | N/A |
| Success rate display | Per category + overall | CONFIRMED |
| Success rate algorithm | Research pending | DEFERRED |
| Auditability | Full transparency | CONFIRMED |
| Vote URLs | Link to raw data + archive | CONFIRMED |
| Frontend | Next.js 14 + Tailwind + shadcn | CONFIRMED |
| Language | Spanish only | CONFIRMED |
| Domain | ampayperu.com | CONFIRMED |
| Confidence threshold | 0.9/0.7/discard | CONFIRMED |
| Human review | Sample 50, >90% accuracy | CONFIRMED |
| Data refresh | One-time snapshot | CONFIRMED |
| Launch strategy | Soft launch first | CONFIRMED |
| JSON schema | Popolo/OCD + custom | CONFIRMED |
| PDF extraction | PyMuPDF + Tesseract | CONFIRMED |
| Rating scale | Kept/Broken/Partial/No Data | CONFIRMED |

---

*Last updated: 2026-01-21*
