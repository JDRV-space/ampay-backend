# AMPAY - Research & Design Document
## Peru 2026 Election Transparency App

**Date:** 2026-01-20
**Status:** Planning phase
**Status:** Research phase

---

## 1. APP CONCEPT

**Name:** AMPAY
**Tagline:** Infórmate sobre las elecciones 2026
**Meaning:** Peruvian slang for "catching someone in the act"

### Core Features:
1. **Quiz (8 questions)** - Match user to party based on values
2. **Auditoría** - 2021 promises vs actual results
3. **Promesas 2026** - Current promises with specificity scores
4. **AMPAY!** - Contradictions caught (gotchas)
5. **Methodology** - Full transparency on data sources

### Key Differentiator:
> "Coincidencia: 78% | Cumplimiento: 35%"
> "El partido que más coincide contigo tiene el peor track record"

---

## 2. EXISTING OPEN SOURCE REPOS

### Useful for this project:

| Repo | URL | Data | Notes |
|------|-----|------|-------|
| hiperderecho/proyectos_de_ley | https://github.com/hiperderecho/proyectos_de_ley | Congress bills + SQLite | Scrapes congreso.gob.pe |
| congreso/proyectos | https://github.com/congreso/proyectos | Bills since 1990 | Historical data |
| jmcastagnetto/2021-elecciones | https://github.com/jmcastagnetto/2021-elecciones-generales-peru-datos-de-onpe | 2021 election results | ONPE data |
| awesome-datasets-peru | https://github.com/OpenDataCo/awesome-datasets-peru | Dataset links | Reference list |
| PeruData | https://github.com/PeruData | INEI, SENHAMI, MINEM | Research datasets |

### Gap (our moat):
- No one has scraped planes de gobierno
- No one has done promise-to-execution matching
- No one has built a quiz + compliance tracker

---

## 3. DATA SOURCES

### Official Sources:

| Source | URL | Data | Format |
|--------|-----|------|--------|
| JNE Plataforma Electoral | https://plataformaelectoral.jne.gob.pe | Planes de gobierno 2026 | PDF |
| JNE Histórico | https://plataformahistorico.jne.gob.pe | Planes de gobierno 2021 | PDF |
| INEI | https://www.inei.gob.pe | Crime, poverty, health stats | CSV/Excel |
| MEF Transparencia | https://www.mef.gob.pe | Budget execution | API/CSV |
| Congreso | https://www.congreso.gob.pe | Bills, votes | HTML (scrape) |

### 2021 Plan de Gobierno Direct Links Found:
- Juntos por el Perú: https://apisije-e.jne.gob.pe/TRAMITE/ESCRITO/1587/ARCHIVO/FIRMADO/5262.PDF
- Acción Popular: https://declara.jne.gob.pe/ASSETS/PLANGOBIERNO/FILEPLANGOBIERNO/16511.pdf

---

## 4. TOP POLLING CANDIDATES (Jan 2026)

| Rank | Candidato | Partido | % |
|------|-----------|---------|---|
| 1 | Rafael López Aliaga | Renovación Popular | 13.6% |
| 2 | Keiko Fujimori | Fuerza Popular | 7.1% |
| 3 | Mario Vizcarra | Perú Primero | 4.4% |
| 4 | Carlos Álvarez | País para Todos | 3.9% |
| 5 | César Acuña | Alianza para el Progreso | 3.7% |

**MVP Scope:** Top 5 parties only

---

## 5. TECH STACK

```
Frontend:     Next.js or Astro (static export)
Hosting:      Vercel (free tier)
Data:         Pre-computed JSON files
LLM:          Gemini Flash (free tier) for analysis
Embeddings:   sentence-transformers (local, free)
Database:     None (static site)
```

---

## 6. QUIZ - 8 QUESTIONS

| # | Category | Question (Spanish) |
|---|----------|-------------------|
| 1 | Seguridad | ¿El gobierno debería priorizar mano dura contra la delincuencia? |
| 2 | Economía | ¿El Estado debería aumentar impuestos a grandes empresas? |
| 3 | Programas Sociales | ¿Los programas como Pensión 65 deben expandirse? |
| 4 | Minería/Ambiente | ¿Se debe priorizar la inversión minera sobre preocupaciones ambientales? |
| 5 | Educación | ¿El Estado debe controlar el currículo o dar libertad a privados? |
| 6 | Salud | ¿El sistema de salud debería unificarse bajo un sistema público? |
| 7 | Corrupción | ¿Los funcionarios investigados deben ser suspendidos antes de sentencia? |
| 8 | Empleo | ¿Se debe flexibilizar la legislación laboral? |

**Scale:** 5-point Likert (Totalmente de acuerdo → Totalmente en desacuerdo)

---

## 7. ALGORITHMS

### A. Quiz Matching
```
Coincidencia = Σ (match_score × category_weight) / total_weight

match_score:
- Exact match: 100%
- Off by 1: 50%
- Off by 2+: 0%
```

### B. Cumplimiento Score
```
Cumplimiento = (Cumplidas + 0.5 × Parciales) / Total_Promesas

Categories:
- CUMPLIDO: Meta alcanzada, evidencia documental
- PARCIAL: Avance >50% o legislación sin implementar
- INCUMPLIDO: Sin avance significativo
```

### C. Promise Recycling Detection
```
Use sentence-transformers to embed:
- 2021 promises
- 2026 promises

Cosine similarity > 0.8 = "recycled promise"
```

### D. Specificity Scoring
```
Score 0-5 based on:
[ ] Número concreto (+1)
[ ] Meta medible (+1)
[ ] Plazo definido (+1)
[ ] Fuente de financiamiento (+1)
[ ] Mecanismo de implementación (+1)
```

---

## 8. DESIGN SYSTEM

### Colors (Peruvian-inspired, professional):
```
Primary:    #8B2332 (Burgundy/wine)
Secondary:  #D4A84B (Inca gold)
Neutral:    #2C2C2C (Charcoal)
Background: #FAFAF8 (Off-white)
Success:    #2D6A4F (Forest green) - Cumplido
Warning:    #E9C46A (Amber) - Parcial
Error:      #9B2226 (Deep red) - Incumplido
```

### Typography:
- Headlines: Inter Bold or Plus Jakarta Sans
- Body: Inter Regular
- No decorative fonts

### Visual Elements:
- Subtle geometric patterns (textile-inspired)
- Gold accents on CTAs
- Marca Perú energy (modern pride, not tourist kitsch)

### Logo Concept:
```
    ▲
   ╱ ╲
  ╱ ● ╲      AMPAY
 ╱─────╲     Infórmate sobre las elecciones 2026
```
(Eye inside mountain/pyramid - watching the politicians)

---

## 9. WORK BREAKDOWN

### Data Pipeline (Day 1-2):
- [ ] Download 2026 plans (5 parties) from JNE
- [ ] Download 2021 plans (5 parties) from JNE histórico
- [ ] Extract promises using existing script
- [ ] Map party positions to 8 quiz questions
- [ ] Research 15 key outcomes (crime, poverty, hospitals)
- [ ] Use LLM to generate verdicts
- [ ] Use LLM to find AMPAYs

### UI Build (Day 2-3):
- [ ] Landing page
- [ ] Quiz flow (8 questions)
- [ ] Results page
- [ ] Party detail pages
- [ ] AMPAY section
- [ ] Methodology page

### Polish & Deploy (Day 3-4):
- [ ] Mobile responsive
- [ ] OG images for sharing
- [ ] Deploy to Vercel
- [ ] Test all flows

---

## 10. COMPETITOR

**goberlab.org** (7-person team, still on waitlist)
- Building: "Información Electoral Verificada"
- Status: Not launched
- Our advantage: Speed, working extraction pipeline, unique angle (accountability)

---

## 11. LLM PROMPTS (Draft)

### Promise Extraction:
```
Extract all concrete promises from this plan de gobierno PDF.
For each promise, output JSON:
{
  "promise": "text of promise",
  "category": "seguridad|economia|salud|educacion|...",
  "specificity": 0-5,
  "page": number
}
Only extract measurable commitments, not vague statements.
```

### Cumplimiento Verdict:
```
Promise (2021): "{promise}"
Current data: "{stats}"

Determine if this promise was:
- CUMPLIDO: Goal achieved with evidence
- PARCIAL: >50% progress or law passed but not implemented
- INCUMPLIDO: No significant progress

Output JSON:
{
  "verdict": "CUMPLIDO|PARCIAL|INCUMPLIDO",
  "evidence": "brief explanation",
  "source": "data source"
}
```

### AMPAY Detection:
```
Analyze this plan de gobierno for internal contradictions.
Look for:
1. Promises that conflict with each other
2. Promises that conflict with party's voting record
3. Mathematically impossible claims (cut taxes + increase spending)

Output JSON array of contradictions found.
```

---

## 12. SUCCESS METRICS

- All target parties fully analyzed
- Quiz working with accurate matching
- Shareable results
- Transparent methodology documentation

---

## 13. INITIAL FILES CREATED

- Extracted plan de gobierno text files (per party)
- Extracted promises JSON (214 promises from Fuerza Popular as first test)
- Promise extraction script (`scripts/extract_metas_v3.py`)

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Document created: 2026-01-20*
*Project: AMPAY*
