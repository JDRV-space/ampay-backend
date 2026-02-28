<div align="center">

# AMPAY

Political transparency platform for Peru 2026 elections. Take a political quiz, discover which party matches your views, and see if they kept their promises or got caught in an AMPAY. Available in Spanish and English.

[![Live App](https://img.shields.io/badge/Live-ampayperu.com-FF4136?style=for-the-badge&logo=vercel&logoColor=white)](https://ampayperu.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Data](https://img.shields.io/badge/Votes-2%2C226-green?style=for-the-badge)](data/02_output/votes_categorized.json)
[![AMPAYs](https://img.shields.io/badge/AMPAYs_Found-6-red?style=for-the-badge)](data/02_output/ampays.json)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/JDRV-space/ampay-data/pulls)

[Live App](https://ampayperu.com) · [Platform Features](#platform-features) · [AMPAYs Found](#ampays-found-6) · [Data Pipeline](#data-pipeline) · [Key Algorithms](#key-algorithms) (11) · [Methodology](#methodology) (20 docs) · [Documentation](#documentation) · [License](#license)

</div>

> **AMPAY**: Porque las promesas se cumplen o se AMPAYan.

## What is AMPAY?

AMPAY is a political transparency platform for Peru's 2026 elections. It combines a **political quiz** that matches voters to parties, a **promise audit system** that tracks whether parties kept their 2021 commitments, and an **AMPAY detection engine** that finds verifiable contradictions where parties voted against their own campaign promises.

**Live at [ampayperu.com](https://ampayperu.com)**

This repository contains the **data pipeline, analysis engine, LLM prompts, output datasets, and 48 methodology documents** that power the platform. The frontend consumes JSON outputs from `data/02_output/`.


## Platform Features

### Political Quiz
`/quiz` · 15 policy questions · 9 parties · Manhattan distance scoring

Users answer 15 policy statements (agree/neutral/disagree) covering taxation, security, labor, energy, social issues, healthcare, and governance. Two calibration questions position the user on economic (left-center-right) and social (conservative-moderate-progressive) axes. Results show percentage compatibility with all 9 parties, split into "within your profile" and full ranking.

**Validated:** 2 million Monte Carlo simulations (seed=42). 100% believer precision: users who answer exactly like a party always get that party as #1.

### AMPAY Contradictions
`/ampays` · 6 confirmed cases · Evidence-backed

Each AMPAY displays the original promise (with JNE PDF page citation), the related congressional votes, the party's actual voting position, and a reasoning chain explaining the contradiction. Confidence levels (HIGH/MEDIUM) based on number of laws and semantic connection strength.

### Party Profiles
`/partidos/[slug]` · 9 parties · Promise fulfillment tracking

Detailed profiles for each party showing ideological positioning, 2026 presidential candidate, congressional seat count, policy positions across 15 categories (+1/0/-1 coding), and promise fulfillment rates (kept/broken/partial/no data).

### Voting Records by Topic
`/por-tema/[category]` · 2,226 votes · 15 categories

Browse all congressional votes (2021-2024) filtered by policy topic. For each vote: date, result (approved/rejected), and a party-by-party breakdown showing who voted yes, no, abstained, or was absent. Filters for vote type (substantive/declarative/procedural) and year.

### Promise Audit
`/auditoria` · 345 promises · 9 parties · 2021 vs actual voting

Side-by-side comparison of what parties promised in their 2021 JNE-registered campaign platforms versus how they actually voted in Congress over 3 years. Links promises to specific laws and votes.

### Statistics Dashboard
`/stats` · Voting patterns · Sparklines · Cohesion indices

Aggregated charts showing party voting patterns by category, monthly trends (36 months of sparkline data), vote categorization distribution, AMPAY frequency by party, and party cohesion indices (0.71-0.94 range).

### 2026 Proposals
`/propuestas-2026` · 9 parties · JNE-registered platforms

All parties' 2026 campaign promises extracted from official JNE platform documents, organized by policy category.

### Data Download
`/descargar` · JSON + CSV · Open data

Download all datasets: quiz statements with party positions, classified congressional votes, AMPAY contradictions, party patterns, and per-party analysis reports.


## AMPAYs Found: 6

| Party | AMPAYs | Categories |
|-------|--------|------------|
| Renovacion Popular | 2 | Fiscal, Economia |
| Fuerza Popular | 1 | Fiscal |
| Peru Libre | 1 | Fiscal |
| Somos Peru | 1 | Fiscal |
| Juntos por el Peru | 1 | Justicia |
| Alianza para el Progreso | 0 |  -  |
| Avanza Pais | 0 |  -  |
| Podemos Peru | 0 |  -  |
| Partido Morado | 0 |  -  |

> **Data coverage:** 2021-07-26 to 2024-07-26 (~60% of term). See [DATA_DISCLAIMER.md](DATA_DISCLAIMER.md).


## Data Pipeline

```
Phase 1.1            Phase 1.2              Phase 1.3               Phase 1.4
PDF Download    →   Promise Extraction  →   Vote Classification  →   AMPAY Detection
(JNE website)       (Claude API)            (Gemini API)             (Claude API)
     ↓                    ↓                       ↓                       ↓
 18 PDFs →          promises/*.json         votes_categorized.json   ampays.json
 text/*.txt                                                               ↓
                                                              Cross-Validation
                                                           (23 candidates → 6)
                              Phase 2: Aggregation
                    ┌────────────┬────────────┬────────────┐
                    ↓            ↓            ↓            ↓
            votes_by_party  patterns   quiz_statements  analysis_by_party/
            (parliament)   (sparklines)  (quiz data)    (9 party reports)
```

### Pipeline Scripts

| Script | Phase | Description |
|--------|-------|-------------|
| `phase_1_1_pdf_download.py` | 1.1 | Download party platform PDFs from JNE |
| `phase_1_2_promise_extraction.py` | 1.2 | Extract measurable promises via Claude API |
| `phase_1_3_vote_classification.py` | 1.3 | Classify 2,226 votes into 15 categories via Gemini |
| `phase_1_4_fast.py` | 1.4 | Detect AMPAYs using dual-search (direct + inverse) |
| `aggregate_votes.py` | 2 | Generate per-vote party breakdown (parliament aggregation) |
| `compute_patterns.py` | 2 | Generate monthly voting patterns per party (sparklines) |
| `aggregate_positions.py` | 2 | Aggregate party positions for quiz (+1/0/-1 coding) |
| `batch_processor.py` | Util | Batch processing with checkpoints and rate limiting |
| `classify_votes.py` | Util | Vote classification utilities |
| `detect_ampays.py` | Util | AMPAY detection core logic |
| `detect_ampays_gemini.py` | Util | AMPAY detection via Gemini API |
| `filter_contradictions.py` | Util | Post-processing contradiction filters |
| `process_pipeline.py` | Orch | End-to-end pipeline orchestrator |
| `quiz_simulation.py` | Val | Quiz algorithm Monte Carlo validation (2M simulations) |

### LLM Prompt Templates

The `prompts/` directory contains the exact prompts used in each LLM-powered phase:

| Prompt | Pipeline Phase | LLM |
|--------|---------------|-----|
| [`extract_promises.md`](prompts/extract_promises.md) | 1.2 Promise Extraction | Claude |
| [`classify_vote.md`](prompts/classify_vote.md) | 1.3 Vote Classification | Gemini |
| [`detect_contradiction.md`](prompts/detect_contradiction.md) | 1.4 AMPAY Detection | Claude |


## Key Algorithms

### 1. AMPAY Detection (Dual Search v5)

Contradictions are detected using two complementary searches per promise:

| Search | Question | AMPAY Condition |
|--------|----------|-----------------|
| **Direct (A)** | Did the party vote NO on laws that would implement its promise? | >= 60% NO votes |
| **Inverse (B)** | Did the party vote YES on laws that contradict its promise? | >= 60% YES votes |

A minimum of 3 relevant laws is required. Both searches run independently; either can trigger an AMPAY.

**Confidence levels:**

| Level | Criteria |
|-------|----------|
| HIGH | >= 60% contradiction + >= 5 laws + clear semantic connection |
| MEDIUM | >= 60% contradiction + 3-4 laws |
| LOW | 40-59% contradiction (rejected) |

**Results:** 23 auto-detected → 8 approved after cross-validation → 6 final after manual audit (2 removed: AMPAY-006/007 from Alianza para el Progreso, original pre-audit numbering, for incorrect vote interpretation). False positive rate: 65.2% before validation.

See: [AMPAY_DETECTION.md](docs/methodology/AMPAY_DETECTION.md), [CROSS_VALIDATION.md](docs/methodology/CROSS_VALIDATION.md)

### 2. Political Quiz Scoring (Manhattan + Coverage v3.3)

Blended score combining Manhattan distance with coverage penalty:

```
distance(user, party) = Σ |user_position_i - party_position_i|
manhattan_score = 1 - distance / (2 × answered_questions)
final_score = 0.9 × manhattan_score + 0.1 × coverage_penalty
percentage = final_score × 100
```

| Parameter | Value |
|-----------|-------|
| Scale | +1 (agree), 0 (neutral), -1 (disagree) |
| Questions | 15 (5 economic-left, 4 economic-right, 3 social, 3 cross-ideological) |
| Parties | 9 |
| Max distance | 30 |

**Ideological filter:** Two additional calibration questions (economic axis, social axis) filter display results into "within your profile" vs "others". This does not affect distance calculation.

**Validation:** 2M Monte Carlo simulations (seed=42). 1M believer tests = 100% precision. 1M random tests = balance ratio 2.72:1.

See: [QUIZ_ALGORITHM.md](docs/methodology/QUIZ_ALGORITHM.md), [QUIZ_VALIDATION.md](docs/methodology/QUIZ_VALIDATION.md)

### 3. Vote Categorization (15-Category System)

Three-tier classification pipeline:

| Tier | Method | Coverage |
|------|--------|----------|
| 1. Keyword matching | Priority-based keyword detection (high/medium/requires-context) | First pass |
| 2. AI classification | Gemini Flash (bulk) + Claude Opus (final) | Multi-match or no-match |
| 3. Human verification | 5% random sample audit | Quality control |

**15 categories:** seguridad, economia, fiscal, social, empleo, educacion, salud, agricultura, agua, vivienda, transporte, energia, mineria, ambiente, justicia.

**Results:** 2,226 substantive votes classified. 94.8% precision overall (98.2% keyword-only, 91.3% AI-only).

See: [VOTE_CATEGORIZATION.md](docs/methodology/VOTE_CATEGORIZATION.md)

### 4. Parliament Aggregation (Individual → Party)

Converts ~289,000 individual congress member votes into party-level positions:

```
Position = majority(SI, NO) excluding abstentions/absences
SI > NO → "SI"  |  NO > SI → "NO"  |  SI = NO → "DIVIDED"  |  0 present → "AUSENTE"
```

**Cohesion index:** `|SI - NO| / (SI + NO)`, ranges from 0.71 (Partido Morado, least cohesive) to 0.94 (Renovacion Popular, most cohesive).

See: [PARLIAMENT_AGGREGATION.md](docs/methodology/PARLIAMENT_AGGREGATION.md)

### 5. Blended Score (α=0.1 Normalization)

Prevents parties with few defined positions from always winning by being "close to everyone":

```
score = (1 - α) × distance + α × (distance / max(positions, 4)) × 15
     = 0.9 × D + 0.1 × (D / max(P, 4)) × 15
```

| Parameter | Value | Purpose |
|-----------|-------|---------|
| α (alpha) | 0.1 | Blending weight for normalization |
| MIN_POSITIONS_FLOOR | 4 | Minimum divisor to avoid over-penalizing |
| 15 | Max distance | Scaling factor |

**Validation:** 10M Monte Carlo simulations. Imbalance reduced from 7.6:1 to 2.97:1 (61% improvement).

See: [BLENDED_SCORE.md](docs/methodology/BLENDED_SCORE.md)

### 6. Political Compass (2D Positioning)

Maps parties and users onto a 2-axis political compass:

```
x (economic) = avg(position_i × compass_direction_i) for economic questions
y (social)   = avg(position_i × compass_direction_i) for social questions
```

| Axis | Range | Poles |
|------|-------|-------|
| Economic (x) | -1 to +1 | Left ↔ Right |
| Social (y) | -1 to +1 | Progressive ↔ Conservative |

`compass_direction` multiplier ensures answers map to the correct quadrant (-1 = left/progressive, +1 = right/conservative, 0 = not used for compass).

See: [POLITICAL_COMPASS.md](docs/methodology/POLITICAL_COMPASS.md)

### 7. Calibration Filtering

Pre-filters quiz results based on 2 calibration questions (economic + social axis):

```
C1 (economic): user ranks 3 options → rank #3 maps to parties → excluded
C2 (social):   user ranks 3 options → rank #3 maps to parties → excluded
```

Applied **after** blended score sorting. True top match (unfiltered) remains accessible for transparency.

See: [CALIBRATION_FILTERING.md](docs/methodology/CALIBRATION_FILTERING.md)

### 8. Position Determination (SI/NO/DIVIDED/AUSENTE)

Determines party position from individual congress member votes using simple majority:

```python
total_present = si + no + abstenciones
if total_present == 0:   → "AUSENTE"
elif si / total_present > 0.5:  → "SI"
elif no / total_present > 0.5:  → "NO"
else:                    → "DIVIDED"
```

Processes `resultados_grupo.csv` from OpenPolitica for each of 2,226 votes across 10 tracked parties.

See: [POSITION_DETERMINATION.md](docs/methodology/POSITION_DETERMINATION.md)

### 9. Keyword Classification (15 Categories)

First-pass classification of votes into 15 categories by keyword matching in the vote's `asunto` text:

```
score[category] = count of keyword matches
best_category = argmax(scores)
confidence = min(0.95, 0.5 + max_score × 0.15)
```

Also detects `vote_type` (sustantivo/procedural/declarativo) using separate keyword lists. Default category when no keywords match: "justicia".

See: [KEYWORD_CLASSIFICATION.md](docs/methodology/KEYWORD_CLASSIFICATION.md)

### 10. Radar Chart (Category Averaging)

Visualizes user-vs-party alignment per category using dual radar overlays:

```
avg = Σ positions / count(statements_in_category)
normalized = ((avg + 1) / 2) × 100    // maps [-1,+1] → [0,100]
```

See: [RADAR_CHART.md](docs/methodology/RADAR_CHART.md)

### 11. Parliament Semicircle (Hemicycle Geometry)

Renders congressional votes as a hemicycle with polar coordinate seating:

```
radius = 60 + row × 25              // 5 rows: 60, 85, 110, 135, 160
angle = π - (i / (N-1)) × π        // distribute seats across semicircle
x = centerX + radius × cos(angle)
y = centerY - radius × sin(angle)
```

Colors: green (SI), red (NO), yellow (abstention), gray (absent). Result: SI > NO → APROBADO.

See: [PARLIAMENT_SEMICIRCLE.md](docs/methodology/PARLIAMENT_SEMICIRCLE.md)


## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS + shadcn/ui |
| Data Pipeline | Python 3.10+ |
| LLM (extraction) | Claude API (Anthropic) |
| LLM (classification) | Gemini API (Google) |
| Validation | 2M Monte Carlo simulations |
| Hosting | Vercel |
| Data Sources | JNE (promises) + OpenPolitica (votes) |


## Architecture

```
ampay/
├── data/
│   ├── 01_input/                        # Raw source data
│   │   ├── promises/
│   │   │   ├── 2021/                   # 9 party promise JSONs (JNE 2021)
│   │   │   └── 2026/                   # 9 party promise JSONs (JNE 2026)
│   │   ├── votes/                       # Congressional voting records
│   │   │   ├── votes_categorized.json   # 2,226 classified votes
│   │   │   └── party_positions.json     # Party positions per question
│   │   └── pdfs/                        # Extracted text from JNE PDFs
│   │       └── text/                   # 18 party platform text files
│   │
│   └── 02_output/                       # Pipeline outputs (frontend reads from here)
│       ├── ampays.json                  # 6 confirmed AMPAYs
│       ├── AMPAY_CONFIRMED_2021.json    # Detailed AMPAY evidence + audit
│       ├── quiz_statements.json         # 15 quiz questions + party positions
│       ├── quiz_position_audit.json     # Party position source audit trail
│       ├── quiz_validation_dataset.json # Quiz validation replication data
│       ├── quiz_validation_results.json # Quiz validation results (2M tests)
│       ├── votes_categorized.json       # 2,226 classified votes
│       ├── votes_by_party.json          # Per-vote party breakdown
│       ├── party_patterns.json          # Voting patterns (sparklines)
│       ├── analysis_by_party/           # Per-party detailed analysis (9 files)
│       └── PROMISE_AUDIT_REPORT.md      # Promise extraction audit report
│
├── scripts/                             # Python data pipeline (14 scripts)
│   ├── phase_1_*.py                     # Pipeline phases 1.1-1.4
│   ├── aggregate_*.py                   # Aggregation scripts
│   ├── compute_patterns.py              # Pattern computation
│   ├── batch_processor.py               # Batch processing utility
│   ├── process_pipeline.py              # Pipeline orchestrator
│   └── quiz_simulation.py               # Quiz validation (2M Monte Carlo)
│
├── prompts/                             # LLM prompt templates
│   ├── extract_promises.md              # Promise extraction prompt (Claude)
│   ├── classify_vote.md                 # Vote classification prompt (Gemini)
│   └── detect_contradiction.md          # AMPAY detection prompt (Claude)
│
├── docs/                                # 48 documentation files
│   ├── methodology/                     # Algorithm documentation (20 docs)
│   ├── data/                            # Data schemas, sources, limitations (7 docs)
│   ├── research/                        # Academic references, VAA research (7 docs)
│   ├── legal/                           # Disclaimers, T&C, privacy policy (6 docs)
│   ├── decisions/                       # Architecture decisions (2 docs)
│   ├── features/                        # Feature specifications (1 doc)
│   └── reference/                       # Glossary, FAQ, bibliography (5 docs)
│
├── DATA_DISCLAIMER.md                   # Critical data coverage limitations
└── LICENSE                              # MIT
```


## By the Numbers

| Metric | Value |
|--------|-------|
| Parties analyzed | 9 |
| Campaign PDFs processed | 18 (2021 + 2026) |
| Promises extracted | 345 (validated) |
| Congressional votes classified | 2,226 (substantive) |
| Individual votes aggregated | ~289,000 |
| AMPAYs confirmed | 6 |
| False positive rejection rate | 65.2% |
| Quiz questions | 15 + 2 calibration |
| Policy categories | 15 |
| Monte Carlo validation tests | 2,000,000 |
| Believer precision | 100% |
| Voting pattern months | 36 (2021-08 to 2024-07) |
| Documentation files | 48 |


## Methodology

Full methodology documentation is in [`docs/methodology/`](docs/methodology/) (20 documents):

#### Algorithms

| Document | Description |
|----------|-------------|
| [BLENDED_SCORE.md](docs/methodology/BLENDED_SCORE.md) | Blended score formula (α=0.1) for balanced quiz matching |
| [QUIZ_ALGORITHM.md](docs/methodology/QUIZ_ALGORITHM.md) | Political quiz scoring (Manhattan distance v3.3) |
| [POLITICAL_COMPASS.md](docs/methodology/POLITICAL_COMPASS.md) | 2D political compass positioning (economic + social axes) |
| [CALIBRATION_FILTERING.md](docs/methodology/CALIBRATION_FILTERING.md) | Quiz calibration questions and party exclusion logic |
| [POSITION_DETERMINATION.md](docs/methodology/POSITION_DETERMINATION.md) | SI/NO/DIVIDED/AUSENTE determination from vote counts |
| [KEYWORD_CLASSIFICATION.md](docs/methodology/KEYWORD_CLASSIFICATION.md) | Keyword-based vote classification into 15 categories |
| [VOTE_CATEGORIZATION.md](docs/methodology/VOTE_CATEGORIZATION.md) | 15-category vote classification system (3-tier pipeline) |
| [VOTE_FILTERING.md](docs/methodology/VOTE_FILTERING.md) | Substantive vs procedural vote filtering |
| [PARLIAMENT_AGGREGATION.md](docs/methodology/PARLIAMENT_AGGREGATION.md) | Individual-to-party vote aggregation + cohesion index |
| [RADAR_CHART.md](docs/methodology/RADAR_CHART.md) | Category radar chart averaging and normalization |
| [SPARKLINE_CALCULATION.md](docs/methodology/SPARKLINE_CALCULATION.md) | Voting pattern sparkline computation |
| [PARLIAMENT_SEMICIRCLE.md](docs/methodology/PARLIAMENT_SEMICIRCLE.md) | Hemicycle geometry for parliamentary vote visualization |

#### Process

| Document | Description |
|----------|-------------|
| [METHODOLOGY_V4_DUAL_SEARCH.md](docs/methodology/METHODOLOGY_V4_DUAL_SEARCH.md) | Master methodology, dual-search AMPAY detection |
| [AMPAY_DETECTION.md](docs/methodology/AMPAY_DETECTION.md) | Contradiction detection algorithm (v5, confidence levels) |
| [CROSS_VALIDATION.md](docs/methodology/CROSS_VALIDATION.md) | Human validation pipeline (23 → 6 AMPAYs) |
| [PROMISE_EXTRACTION.md](docs/methodology/PROMISE_EXTRACTION.md) | LLM-based promise extraction from campaign PDFs |
| [PARTY_POSITION_CODING.md](docs/methodology/PARTY_POSITION_CODING.md) | Party position coding system (+1/0/-1 from PDFs) |
| [DATA_PIPELINE_FLOWS.md](docs/methodology/DATA_PIPELINE_FLOWS.md) | Technical 5-phase pipeline documentation |
| [QUIZ_VALIDATION.md](docs/methodology/QUIZ_VALIDATION.md) | Quiz algorithm Monte Carlo validation (2M simulations) |
| [VERSION_HISTORY.md](docs/methodology/VERSION_HISTORY.md) | Methodology evolution (v1 → v5) |


## Documentation

### Data Documentation

| Document | Description |
|----------|-------------|
| [DATA_SOURCES.md](docs/data/DATA_SOURCES.md) | All data sources with URLs and access dates |
| [DATA_SCHEMA.md](docs/data/DATA_SCHEMA.md) | JSON schema definitions for all output files |
| [DATA_LIMITATIONS.md](docs/data/DATA_LIMITATIONS.md) | Known data gaps and coverage limitations |
| [CATEGORY_DEFINITIONS.md](docs/data/CATEGORY_DEFINITIONS.md) | Full definitions of all 15 vote categories |
| [CATEGORIES.md](docs/data/CATEGORIES.md) | Category overview and keyword mappings |
| [CALIBRATION_MAPPINGS.md](docs/data/CALIBRATION_MAPPINGS.md) | Quiz calibration axis mappings |
| [PARTY_PROFILES.md](docs/data/PARTY_PROFILES.md) | 9 party profiles with ideological positioning |

### Research & References

| Document | Description |
|----------|-------------|
| [00_INITIAL_RESEARCH.md](docs/research/00_INITIAL_RESEARCH.md) | Project research foundations |
| [01_PROMISE_VOTE_MATCHING.md](docs/research/01_PROMISE_VOTE_MATCHING.md) | Promise-to-vote matching methodology |
| [02_FULFILLMENT_RATINGS.md](docs/research/02_FULFILLMENT_RATINGS.md) | Fulfillment rating system design |
| [03_QUIZ_ALGORITHM.md](docs/research/03_QUIZ_ALGORITHM.md) | Quiz algorithm research (VAA literature) |
| [04_JSON_SCHEMA.md](docs/research/04_JSON_SCHEMA.md) | Data schema design decisions |
| [05_PDF_EXTRACTION.md](docs/research/05_PDF_EXTRACTION.md) | PDF extraction methods comparison |
| [06_VAA_METHODOLOGY.md](docs/research/06_VAA_METHODOLOGY.md) | Voting Advice Application methodology |
| [SOURCES_BIBLIOGRAPHY.md](docs/reference/SOURCES_BIBLIOGRAPHY.md) | Academic sources and bibliography |

### Legal

| Document | Description |
|----------|-------------|
| [DISCLAIMER.md](docs/legal/DISCLAIMER.md) | Data and analysis disclaimers |
| [LEGAL_ANALYSIS.md](docs/legal/LEGAL_ANALYSIS.md) | Legal framework analysis |
| [LEGAL_RESEARCH.md](docs/legal/LEGAL_RESEARCH.md) | Legal research and precedents |
| [PRIVACY_POLICY.md](docs/legal/PRIVACY_POLICY.md) | Privacy policy |
| [TERMS_AND_CONDITIONS.md](docs/legal/TERMS_AND_CONDITIONS.md) | Terms and conditions |
| [COPYRIGHT.md](docs/legal/COPYRIGHT.md) | Copyright notice |

### Reference

| Document | Description |
|----------|-------------|
| [GLOSSARY.md](docs/reference/GLOSSARY.md) | Terms and definitions |
| [FAQ.md](docs/reference/FAQ.md) | Frequently asked questions |
| [AUDIT_TRAIL.md](docs/reference/AUDIT_TRAIL.md) | Complete audit trail of data decisions |
| [URL_VERIFICATION_REPORT.md](docs/reference/URL_VERIFICATION_REPORT.md) | URL verification and link audit report |
| [DECISIONS.md](docs/decisions/DECISIONS.md) | Architecture and design decisions |


## Data Sources

| Data | Coverage | Source |
|------|----------|--------|
| Congressional votes | 2021-07 to 2024-07 (3,570 total → 2,226 substantive) | [OpenPolitica](https://github.com/openpolitica/congreso-pleno-asistencia-votacion) |
| Party promises (2021) | 9 parties, 345 validated promises | [JNE Plataforma Historica](https://plataformahistorico.jne.gob.pe/) |
| Party promises (2026) | 9 parties | [JNE Plataforma Electoral](https://plataformaelectoral.jne.gob.pe/) |


## Getting Started

### Prerequisites

- Python 3.10+
- [Anthropic API key](https://console.anthropic.com/) (for promise extraction & AMPAY detection)
- [Google AI API key](https://aistudio.google.com/) (for vote classification)

### Run the Pipeline

```bash
# Clone
git clone https://github.com/JDRV-space/ampay-data.git
cd ampay-data

# Install dependencies
pip install -r requirements.txt

# Set API keys
export ANTHROPIC_API_KEY=your-key-here
export GOOGLE_API_KEY=your-key-here

# Run full pipeline
python scripts/process_pipeline.py

# Or run individual phases
python scripts/phase_1_1_pdf_download.py
python scripts/phase_1_2_promise_extraction.py
python scripts/phase_1_3_vote_classification.py
python scripts/phase_1_4_fast.py
python scripts/aggregate_votes.py
python scripts/compute_patterns.py
```

### Output Files

All pipeline outputs are in `data/02_output/`:

| File | Size | Description |
|------|------|-------------|
| `ampays.json` | 5 KB | 6 confirmed AMPAYs with evidence |
| `AMPAY_CONFIRMED_2021.json` | 10 KB | Detailed AMPAY evidence + audit trail |
| `quiz_statements.json` | 17 KB | 15 quiz questions + 9 party positions |
| `quiz_position_audit.json` | 20 KB | Party position source audit trail |
| `quiz_validation_dataset.json` | 3 KB | Monte Carlo validation replication data |
| `quiz_validation_results.json` | 3 KB | Validation results (2M simulations) |
| `votes_categorized.json` | 2.1 MB | 2,226 classified votes |
| `votes_by_party.json` | 4.7 MB | Per-vote party breakdown (parliament) |
| `party_patterns.json` | 43 KB | Monthly voting patterns (sparklines) |
| `analysis_by_party/` | 1.9 MB | 9 per-party detailed analysis reports |
| `PROMISE_AUDIT_REPORT.md` | 9 KB | Promise extraction audit report |


## License

[MIT](LICENSE)

<div align="center">

**AMPAY**: Porque las promesas se cumplen o se AMPAYan.

A project by [JDRV-space](https://github.com/JDRV-space)

</div>
