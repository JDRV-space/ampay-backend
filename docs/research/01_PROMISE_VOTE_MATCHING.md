# Matching Political Promises to Legislative Voting Records
## Comprehensive Research on Algorithms and Methodologies

**Research Date:** January 21, 2026
**Confidence Level:** HIGH - Multiple academic sources agree, recent data (2023-2025)

---

## TLDR

The field combines **political science methodology** (Manifesto Project's 56-category coding scheme) with **NLP approaches** (BERT embeddings, semantic similarity). Key tools: ManifestoBERTa (fine-tuned XLM-RoBERTa on 1.9M political statements), PolitiFact's 6-point rating scale. Critical gap: no end-to-end open-source system exists for promise-to-vote matching; researchers combine multiple tools.

---

## 1. Academic Papers on Pledge Fulfillment Analysis

### Core Methodology Papers

#### **"Which Promises Actually Matter? Election Pledge Centrality and Promissory Representation"**
- **Authors:** Jonathan Mellon, Christopher Prosser, Jordan Urban, Adam Feldman
- **Year:** 2023
- **Journal:** Political Studies
- **URL:** https://journals.sagepub.com/doi/full/10.1177/00323217211027419
- **Key Finding:** Developed conjoint experiment method to measure "promise centrality" - not all promises are equal
- **Methodology:** Centrality weighting reduced Conservative promise-keeping assessment by 21 percentage points
- **Impact:** EU promises weighted 6x higher, immigration 6x higher; miscellaneous admin promises reduced by >50%

#### **"When Is A Pledge A Pledge?"**
- **Journal:** British Journal of Political Science (Cambridge)
- **URL:** https://www.cambridge.org/core/journals/british-journal-of-political-science/article/abs/when-is-a-pledge-a-pledge/1417230DEEA7744E8AB589375D56DB69
- **Key Finding:** Voters define pledges as "sincere and realistic" regardless of who made them or verifiability
- **Method:** Conjoint experiments on ~6,000 respondents (US, UK, Denmark)

#### **"Why All These Promises?"**
- **Authors:** Vestergaard et al.
- **Year:** 2025
- **Journal:** European Journal of Political Research
- **URL:** https://ejpr.onlinelibrary.wiley.com/doi/full/10.1111/1475-6765.70011
- **Focus:** Why parties make hundreds of promises despite risk of penalization for unfulfilled commitments

#### **"Politics and Pledge Fulfillment: A Mixed-Methods Analysis of French Electoral Pledges"**
- **Project:** PARTIPOL (French Research Agency funded)
- **URL:** https://shs.hal.science/halshs-02429431
- **Key Insight:** Understanding pledge implementation requires both institutional capacity AND governmental incentives
- **Innovation:** Combines electoral studies with public policy analysis

#### **"Election Promise Tracking: Extending the Shelf Life of Democracy in Digital Journalism"**
- **Year:** 2025
- **Journal:** Journalism Studies (Taylor & Francis)
- **URL:** https://www.tandfonline.com/doi/full/10.1080/1461670X.2025.2477001
- **Focus:** History and methodology comparison between journalistic vs academic approaches

---

## 2. Existing Projects and Databases

### The Manifesto Project (Gold Standard)

**URL:** https://manifesto-project.wzb.eu/

**Overview:**
- Analyzes parties' election manifestos to study policy preferences
- Funded by German Science Foundation (DFG) 2009-2024 as MARPOR
- Won APSA award for best dataset in comparative politics (2003)
- Documents available in 40+ languages with validated machine translation since 2024

**Coding Scheme:**
- **56 categories** grouped into **7 major policy domains**
- Unit of analysis: "quasi-sentences" (smallest meaningful political statement)
- Each quasi-sentence coded into exactly one category
- Categories designed to be comparable across parties, countries, elections, and time

**The 7 Policy Domains:**
1. External Relations
2. Freedom and Democracy
3. Political System
4. Economy
5. Welfare and Quality of Life
6. Fabric of Society
7. Social Groups

**Coding Process:**
1. Unitization: Split text into quasi-sentences
2. Transform into table (one row per quasi-sentence)
3. Allocate codes from category scheme
4. Policy goals precede political means if both mentioned
5. Use minimal context/personal knowledge

**Quality Control:**
- Coders are political scientists or students, native speakers
- Training on English documents with accuracy threshold
- Intensive communication between coders and MARPOR supervisors

**Key Resources:**
- Manifesto Corpus: https://journals.sagepub.com/doi/pdf/10.1177/2053168016643346
- Codebook: https://manifesto-project.wzb.eu/down/data/2020b/codebooks/codebook_MPDataset_MPDS2020b.pdf
- Coding Handbook: https://manifesto-project.wzb.eu/information/documents?name=handbook_v4

---

### PolitiFact Promise Tracker

**URL:** https://www.politifact.com/truth-o-meter/promises/

**Methodology:**
- Created "Obameter" in 2009 (world's first election promise tracking platform)
- Tracked 533 Obama promises over 8 years
- Active trackers: Biden Promise Tracker, Trump-O-Meter

**Promise Identification Process:**
1. Review speech transcripts, TV appearances, position papers, campaign websites
2. Define promise as "prospective statement of action/outcome that is verifiable"
3. Rate based on verifiable outcomes, NOT intentions or effort

**Six-Point Rating Scale:**
| Rating | Description |
|--------|-------------|
| NOT YET RATED | Starting point for all promises |
| IN THE WORKS | Proposed or being considered |
| STALLED | No movement on promise |
| COMPROMISE | Substantially less accomplished but significant |
| PROMISE KEPT | Mostly or completely fulfilled |
| PROMISE BROKEN | Not fulfilled |

**Citation:** https://www.politifact.com/article/2018/feb/12/principles-truth-o-meter-politifacts-methodology-i/

---

### UK Promise Trackers

#### **Full Fact Government Tracker**
- **URL:** https://fullfact.org/government-tracker/
- Monitors 86 key pledges from Labour's 2024 manifesto
- Tracks subsequent announcements post-election

#### **Vote for Policies Promise Tracker**
- **URL:** https://tracker.voteforpolicies.org.uk/
- Tracks UK government progress on election promises
- Connects users to support for issues they care about

#### **Institute for Government Manifesto Tracker**
- **URL:** https://www.instituteforgovernment.org.uk/our-work/trackers
- Measures which election promises translated into action
- Creates special trackers for key moments

#### **BBC Manifesto Tracker** (Historical)
- Used traffic light system (yellow = some progress, red = little/no progress)
- Criticism: "some progress" vs "little progress" is subjective

---

### Polimeter

**URL:** https://www.polimeter.org/en

- Independent initiative developed by political scientists
- Tracks whether politicians keep promises
- Multi-country coverage

---

### Country-Specific Systems

| Country | System | Notes |
|---------|--------|-------|
| Canada | Trudometer | Nuanced fulfillment categories beyond kept/broken |
| Germany | Various trackers | Focus on financial implications of promises |
| UK | Multiple (above) | 200+ verifiable promises per manifesto |

---

## 3. NLP/Computational Approaches

### ManifestoBERTa (State of the Art)

**URL:** https://manifesto-project.wzb.eu/information/documents/manifestoberta

**Architecture:**
- Based on **XLM-RoBERTa large** models
- Fine-tuned on **1.9 million annotated statements** from Manifesto Corpus
- Classifies into 56 categories from Handbook 4 coding scheme

**Two Model Variants:**
1. **manifestoberta-sentence:** For standalone texts (social media posts)
2. **manifestoberta-context:** Incorporates surrounding sentences; superior performance for documents

**Availability:** Free on Hugging Face model hub

**Citation:** Burst, Lehmann, Franzmann, Al-Gaddooa, Ivanusch, Regel, Riethmuller, Wessels, Zehnter (2023). WZB Berlin.

---

### Semantic Similarity Algorithms

#### **Word2Vec Approach**
- Train word embeddings on corpora of political speeches
- Build party embeddings using aggregated word vectors
- Use **cosine similarity** between party vectors as similarity function
- SemScale: Word embeddings significantly outperform tf-idf vectors

#### **BERT vs Word2Vec** (December 2024 Study)
**URL:** https://arxiv.org/abs/2412.04505
- BERT outperforms Word2Vec in maintaining semantic stability
- BERT still recognizes subtle semantic variations
- **Recommendation:** Use BERT for short-term analysis requiring stability

#### **Multilingual BERT (LaBSE)**
- Transforms sentences into high-dimensional vectors
- Enables cross-language political position comparison
- Validation against DW-NOMINATE voting record scaling

---

### Text Scaling Methods

**Political Text Scaling:**
- Predicts scores (left-to-right ideology, EU integration attitudes)
- Methods: DW-NOMINATE, Wordfish, Wordshoal

**Embedding-Based Methods:**
- Transform legal/political texts into numerical vectors
- Calculate semantic similarity via cosine distance
- Compare against ground truth (voting records, expert surveys)

---

### Topic Modeling

**Applications:**
- Analyze topics in legislative speech, Senate press releases, electoral manifestos
- Reveal policy issues parties discuss
- Track how electoral reforms affect information diversity

**Tools:** Latent Dirichlet Allocation (LDA), BERT topic modeling

---

### Contradiction Detection

**Key Paper:** "Finding Contradictions in Text" - Stanford NLP Group
**URL:** https://nlp.stanford.edu/pubs/contradiction-acl08.pdf

**Contradiction Types:**
1. **Negation:** "I support X" vs "I do not support X"
2. **Antonyms:** Using opposite words
3. **Numerical:** Conflicting numbers
4. **Structural:** Grammatical/logical conflicts

**Deep Learning Results:**
- LSTM + manual features achieved 91.2% accuracy (SemEval dataset)
- BETO (Spanish BERT) achieved F1 of 92.47% for contradiction detection
- Spanish dataset (ES-Contradiction): economics and politics domains

**Natural Language Inference (NLI):**
- Contradiction detection is special case of NLI
- Models classify pairs as: entailment, contradiction, neutral

---

### Challenges in Political NLP

1. **Ambiguity of legal/political language**
2. **Specialized terminology**
3. **Complex sentence structures**
4. **Temporal context:** Algorithms should not be used outside same election/legislative period
5. **Finding topical rather than positional similarities**

---

## 4. Methodology Questions Answered

### How is "Fulfillment" Operationalized?

| Approach | Scale | Used By |
|----------|-------|---------|
| Binary | Kept/Broken | Simple academic studies |
| Partial | Kept/Partially/Broken | UK trackers |
| 6-Point | Not Rated/In Works/Stalled/Compromise/Kept/Broken | PolitiFact |
| Weighted | Centrality-adjusted percentages | Mellon et al. 2023 |

**Key Insight:** Research shows centrality weighting dramatically changes fulfillment assessments.

### What Granularity of Matching?

1. **Quasi-sentence level:** Manifesto Project standard unit
2. **Bill-level:** Match promise to specific legislation
3. **Vote-level:** Match promise to legislator voting record
4. **Policy-area level:** Aggregate by domain (economy, welfare, etc.)

### How Handle Coalition Governments?

- Analyze **coalition agreements** separately from manifestos
- Consider **which party controls relevant ministry**
- Track **senior vs junior partner** promise fulfillment separately
- Account for **compromise positions** in coalition negotiations

### Ground Truth Validation

1. **Expert surveys:** Political scientists rate fulfillment
2. **Inter-coder reliability:** Multiple coders, measure agreement (Krippendorff's alpha)
3. **Voting record data:** DW-NOMINATE, GovTrack data
4. **Temporal validation:** Compare predictions to eventual outcomes

---

## 5. Open Source Tools and Datasets

### GitHub Repositories

#### **PolData (erikgahner/PolData)**
- **URL:** https://github.com/erikgahner/PolData
- Curated collection of political science datasets

#### **Legal Text Analytics (Liquid-Legal-Institute)**
- **URL:** https://github.com/Liquid-Legal-Institute/Legal-Text-Analytics
- Methods and tools for legal text analysis

#### **Awesome Legal Data**
- **URL:** https://github.com/openlegaldata/awesome-legal-data
- Collection of datasets for legal text processing

#### **Political Ideology Classifier**
- **URL:** https://github.com/javiermorenosan/ideology-text-classifier
- Uses Congressional Record speeches (97th-114th Congress)
- Methods: Naive Bayes, Logistic Regression, SVM, LDA

#### **Political Sentiment**
- **URL:** https://github.com/DylanModesitt/political-sentiment
- Uses Cornell vote database (congressional debates 2005)
- Labels: party affiliation + for/against bill

#### **Open Source Legislation**
- **URL:** https://github.com/spartypkp/open-source-legislation
- Goal: Global legislation in SQL format for LLMs
- Status: Ambitious but incomplete/unmaintained

---

### Key Datasets

| Dataset | Description | Languages |
|---------|-------------|-----------|
| Manifesto Project Corpus | 1.9M+ coded political statements | 40+ |
| Pile-of-Law | 256GB legal/admin text | English |
| MultiLegalPile | Legal text for LLM training | 24 |
| LexGLUE | Legal language understanding benchmark | English |
| MultiEURLEX | 65k EU legal acts + EuroVoc labels | 23 |
| Congressional Record | US Congress speeches 97th-114th | English |
| Cornell Vote Database | Congressional debates 2005 | English |

---

### NLP Libraries for Political Text

1. **transformers (Hugging Face):** Access ManifestoBERTa
2. **spaCy:** General NLP, entity recognition
3. **Gensim:** Word2Vec, topic modeling
4. **NLTK:** Basic text processing
5. **manifestoR:** R package for Manifesto Project data

---

## 6. Recommended Pipeline for Promise-to-Vote Matching

Based on research, a system would need:

### Step 1: Promise Extraction
- Use ManifestoBERTa to classify manifesto text into 56 categories
- Extract quasi-sentences that are "promises" (prospective, verifiable)

### Step 2: Legislative Text Processing
- Parse bills/votes from legislative APIs (GovTrack, LegiScan)
- Classify legislative text into same 56 categories

### Step 3: Semantic Matching
- Generate BERT embeddings for promises and legislative text
- Calculate cosine similarity within same policy categories
- Threshold for "match" (empirically determined)

### Step 4: Voting Record Integration
- Link bills to legislator votes
- Aggregate party-level or individual-level fulfillment

### Step 5: Fulfillment Scoring
- Apply 6-point scale (PolitiFact model)
- Optionally weight by centrality (Mellon et al. method)

### Step 6: Contradiction Detection
- Run NLI model on promise-action pairs
- Flag contradictions for manual review

---

## 7. Research Gaps Identified

1. **No end-to-end open-source system** for promise-to-vote matching
2. **Limited multilingual tools** beyond EU languages
3. **Coalition government handling** lacks standardized methodology
4. **Centrality weighting** not widely adopted despite strong evidence
5. **Cross-temporal analysis** challenging due to semantic drift

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*Research compiled January 21, 2026*
