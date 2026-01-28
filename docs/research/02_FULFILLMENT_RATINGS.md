# Political Promise Fulfillment: Calculation Methodologies

**Research Date:** 2026-01-21
**Sources:** PolitiFact, FullFact, Polimeter, CPPG, Academic Papers (2020-2025)

---

**TLDR:** Promise trackers use 3-6 category rating systems (Kept/Broken/Compromise/Stalled). Academic standard (CPPG) uses binary coding: pledges "at least partially fulfilled" [1] vs "not fulfilled" [0]. Partial fulfillment typically counts as 0.5 or collapses into "fulfilled" for analysis. The hard problem of semantic matching promises to votes remains largely manual - no production-ready automated system exists. Fulfillment rates = (Kept + Partial) / (Total - InProgress).

---

## Part 1: Fact-Checker Methodologies

### PolitiFact Promise-O-Meter

**Source:** [PolitiFact Methodology](https://www.politifact.com/article/2018/feb/12/principles-truth-o-meter-politifacts-methodology-i/)

**Rating Categories (6 levels):**

| Rating | Definition |
|--------|------------|
| **Promise Kept** | Original promise mostly or completely fulfilled |
| **Compromise** | Substantially less than original but significant accomplishment consistent with goal |
| **Promise Broken** | Promise not fulfilled or reversed course |
| **In the Works** | Promise has been proposed or is being considered |
| **Stalled** | No movement; limitations on money, opposition, or shift in priorities |
| **Not Yet Rated** | Every promise begins here until evidence of progress |

**Key Rules:**
1. Promises rated on **verifiable outcomes**, not intentions or effort
2. Only **campaign promises** tracked (pre-election statements only)
3. Post-election promises NOT added to database
4. Ratings can change as circumstances change
5. At end of term, all promises sorted into final three: Kept/Compromise/Broken

**Limitations:**
- Tracks single, verifiable promises, not broad goals
- President can get credit on specific pledges while failing larger underlying goal
- Cannot fact-check opinions, predictions, or non-verifiable claims

---

### FullFact Government Tracker (UK)

**Source:** [FullFact Government Tracker](https://fullfact.org/government-tracker/)

**Rating Categories (7 levels):**

| Rating | Definition |
|--------|------------|
| **Achieved** | Promise fully delivered |
| **Appears on track** | Progress being made, likely to be achieved |
| **In progress** | Action taken, too early to tell outcome |
| **Appears off track** | Significant obstacles to fulfillment |
| **Not kept** | Promise broken |
| **Unclear or disputed** | Outcome unclear or debated |
| **Wait and see** | Too early to assess progress |

**Key Process:**
- Uses governing party's **election manifesto** as source
- Interprets pledges as "reasonable, fair-minded voter" would
- Tracks specific actions (legislation) or numerical targets vs data
- Uses AI to help monitor progress (as of 2024-2025)

---

### Polimeter (Canada)

**Source:** [Polimeter Methodology](https://www.poltext.org/en/donnees-et-analyses/les-polimetres/methodology-polimeters)

**Rating Categories (4 levels):**

| Rating | Definition |
|--------|------------|
| **Kept** | Followed by officially sanctioned government action (law, regulation, treaty) or next formal sanction is certain |
| **Kept in part / In the works** | Action officially taken (white paper, bill, budget announcement) but not complete. Also: compromise in relation to platform promise. Also: kept after prescribed deadline but before end of term |
| **Broken** | Blocked by opposition OR government explicitly renounced promise |
| **Not yet rated** | Not yet evaluated |

**Promise Identification Process:**
1. **Double-blind coding** by two independently trained experts
2. Promise must commit party to perform action or reach specific goal
3. Wording must enable **objective assessment** of achievement
4. Statements without objective assessment criteria = NOT promises

**End of Term Rule:**
> Promises coded "still in the works" **automatically become "broken"** as soon as head of government requests dissolution of House.

**Fulfillment Rate Calculation:**
```
Fulfillment Rate = (Kept + Kept in Part) / Total Promises

Example: Trudeau 2015-2019
- Kept: 236
- Partially Kept: 92
- Total: 353
- Rate: (236 + 92) / 353 = 92.2%
```

---

## Part 2: Academic Methodology (CPPG Standard)

### Comparative Party Pledge Group (CPPG)

**Source:** [Comparative Party Pledges Project](https://comparativepledges.net/)

The CPPG is an international consortium of 60+ researchers studying election pledges in 16+ countries with standardized methodology.

**Coding Scheme:**

**Step 1: Promise Identification**
```
Promise Criteria:
1. Commits party to perform ACTION or reach specific GOAL
2. Wording enables OBJECTIVE assessment of achievement
3. Must be TESTABLE

Non-Promises (Excluded):
- Vague statements ("improve economy")
- Opinions
- Predictions
- Non-verifiable claims
```

**Step 2: Fulfillment Classification**

| Category | Definition |
|----------|------------|
| **Fully Fulfilled** | Government undertakes action or achieves outcome expected |
| **Partially Fulfilled** | Government took material steps toward fulfillment but did not reach goal. Also: compromise outcome |
| **Not Fulfilled** | No government action corresponding to promise |

**Step 3: Binary Recoding for Analysis**
```
For statistical analysis, categories collapse:
- "At least fulfilled in part" = 1
- "Not fulfilled" = 0

This enables cross-country comparison and logit modeling.
```

**Status Quo Distinction:**
CPPG distinguishes between pledges to:
- **Maintain** status quo (defensive)
- **Change** status quo (proactive)

This matters because maintaining status quo is easier to "fulfill" by inaction.

---

### Thomson-Royed Methodology

**Key Papers:**
- Thomson et al. (2017) "The Fulfillment of Parties' Election Pledges" - American Journal of Political Science
- Royed (1996) "Testing the Mandate Model in Britain and the United States" - British Journal of Political Science

**Operationalization:**

| Term | Definition |
|------|------------|
| **Fully Fulfilled** | Government undertakes an action or achieves the outcome expected |
| **Partially Fulfilled** | Government made obvious efforts or achieved obvious outcomes, but did not fully succeed |
| **Not Fulfilled** | No corresponding action |

**Evidence Sources:**
- Legislation
- Ministerial decrees
- Budgetary data
- Secondary sources (news, official documents)

**Statistical Findings:**
- Average fulfillment rate across 12 countries: **67%**
- UK strongest: **85%+** at least partially enacted
- US presidents: **60%+** at least partially fulfilled
- Study scope: 20,000+ pledges, 57 election campaigns, 12 countries

---

## Part 3: The Hard Problems

### Problem 1: Semantic Matching (Promise to Votes/Actions)

**Current State: Largely Manual**

No production-ready automated system exists for matching campaign promises to legislative votes. Current approaches:

**Manual Approach (Most Trackers):**
1. Fact-checkers manually review legislation, regulations, budgets
2. Identify which promise each action relates to
3. Assess degree of fulfillment

**NLP Research Progress:**
- LLMs can "systematically assess bills, explain bill impacts" (Stanford legal scholar John Nay)
- ML models (Random Forests, SVM, Logistic Regression) achieve **73-74% accuracy** predicting MEP voting behavior from legislative text "semantic descriptors"
- LLM position estimates correlate **0.90+** with expert coding

**Practical Limitation:**
> "Governments take actions that relate to promises in ways that are not always straightforward. A promise to 'reduce crime' might be fulfilled through 50 different bills, budget items, and executive actions."

---

### Problem 2: Multiple Votes Per Promise

**The Question:** If 10 votes relate to one promise, how do you score?

**Current Practice (No Standardized Algorithm):**

1. **Holistic Assessment** (PolitiFact, CPPG)
   - Expert judgment considering ALL related actions
   - Not a formula; human weighs evidence

2. **Outcome-Based** (Polimeter)
   - Focus on whether GOAL was achieved, not individual votes
   - "Did crime actually decrease?" not "How many crime bills passed?"

3. **Academic Approach**
   - Pledge is unit of analysis, not vote
   - Single fulfillment determination per pledge

**No Clear Formula Exists:**
```
Theoretical options (not implemented in practice):
- Simple majority: >=50% aligned votes = Kept
- Weighted average: Weight by bill importance
- Most recent: Final related action determines rating
- Composite: Score = (aligned_votes / total_related_votes)
```

---

### Problem 3: Conflicting Votes

**The Question:** Politician votes FOR healthcare bill A, AGAINST bill B. Both relate to same promise. How scored?

**Current Practice:**

**Holistic Judgment:**
- Experts assess NET effect on promise goal
- "Did overall healthcare improve despite mixed votes?"

**No Threshold Algorithm:**
- No tracker uses "7/10 votes align = Kept"
- All use qualitative expert assessment

**Compromise Category:**
- Mixed results often coded as "Compromise" or "Partial"
- Captures "did something but not everything"

---

### Problem 4: Untrackable Promises

**The Question:** What about "improve the economy" with no specific target?

**Current Approaches:**

| Tracker | Handling |
|---------|----------|
| **CPPG/Polimeter** | **Exclude** - Must be "testable" and allow "objective assessment" |
| **PolitiFact** | **Include if verifiable** - Some vague promises get "Stalled" or tracked via proxy metrics |
| **FullFact** | **Mark as "Unclear"** - Acknowledge difficulty of assessment |

**Best Practice:**
> Exclude vague promises at coding stage. Only include pledges with specific, verifiable commitments.

**Example of Testable vs Non-Testable:**
- Non-testable: "Make America great again"
- Testable: "Build a wall on the southern border"
- Semi-testable: "Create 1 million jobs" (verifiable but attribution unclear)

---

### Problem 5: Temporal Issues

**The Question:** Promise made in 2020, unfulfilled in 2024. Broken or pending?

**Rules by Tracker:**

| Tracker | Rule |
|---------|------|
| **Polimeter** | Promises "not yet rated" become **automatically broken** when government requests dissolution |
| **PolitiFact** | Uses "Stalled" for inactive promises; becomes "Broken" at end of term if no action |
| **CPPG** | Promises expected to be fulfilled during parliamentary term following election |

**Deadline Handling (Polimeter):**
> "Promises which are kept after the prescribed deadline (but before end of term) are classified as 'kept in part.'"

**Key Principle:**
- Promise expiration = end of electoral mandate
- No indefinite "pending" status

---

## Part 4: Algorithms and Formulas

### Fulfillment Rate Calculation

**Basic Formula (Polimeter/CPPG):**
```
Fulfillment Rate = (Fully Kept + Partially Kept) / Total Promises
```

**Excluding In-Progress (PolitiFact-style):**
```
Final Fulfillment Rate = (Kept + Compromise) / (Total - In Progress)
```

**Weighted Partial (Theoretical):**
```
Weighted Rate = (Kept * 1.0 + Partial * 0.5) / Total
```
Note: Not used in practice; partial typically counts as full in numerator.

---

### Promise Importance Weighting

**Problem:** Not all promises are equal. Should "Leave EU" count same as "review administrative procedure X"?

**Mellon et al. (2023) Solution - Pledge Centrality:**

**Source:** [Which Promises Actually Matter?](https://journals.sagepub.com/doi/full/10.1177/00323217211027419)

**Method:**
1. Conjoint experiment measures public perception of promise importance
2. Construct "centrality weights" for each promise
3. Apply weights to fulfillment calculation

**Findings:**
- Centrality weighting **reduced UK Conservative fulfillment assessment by 21 percentage points**
- "Leave the EU" received **9%** of all weight (single promise)
- "Reduce net migration to under 100,000" received **8%** weight
- Miscellaneous administrative promises reduced by **>50%**

**Implication:**
> "Pledge centrality cannot be ignored when assessing pledge fulfillment."

**Current Practice:**
- Most trackers do NOT weight by importance
- All promises treated equally (acknowledged limitation)

---

### Inter-Coder Reliability

**Standard Metric: Krippendorff's Alpha**

**Source:** [Krippendorff's Alpha Methodology](https://www.k-alpha.org/methodological-notes)

| Alpha Value | Interpretation |
|-------------|----------------|
| **1.00** | Perfect agreement |
| **0.80+** | Krippendorff's standard for reliability |
| **0.67-0.79** | Lower bound for tentative conclusions; moderate agreement |
| **<0.67** | Poor agreement; data unreliable |

**Best Practices:**
- Test on 10%+ of dataset
- Coders must know political system
- Training session required
- Use Krippendorff's Alpha over Cohen's Kappa (handles multiple coders, missing data, any measurement level)

---

## Part 5: Practical Implementation

### Building a Promise Tracker: Step-by-Step

**Step 1: Promise Extraction**
```
1. Obtain party manifesto/platform
2. Two independent coders identify promises
3. Apply testability criteria:
   - Specific action or goal?
   - Objectively verifiable?
   - Clear deadline or end condition?
4. Calculate inter-coder reliability (target: Alpha > 0.80)
5. Resolve disagreements through discussion
```

**Step 2: Database Structure**
```
Promise Record:
- promise_id
- text (verbatim from source)
- source (manifesto page, speech, etc.)
- category (policy area)
- target (specific metric if applicable)
- deadline (if specified)
- status (Kept/Partial/Broken/In Progress/Not Rated)
- evidence_links[]
- last_updated
- coder_notes
```

**Step 3: Monitoring Process**
```
1. Track official government actions:
   - Legislation passed
   - Executive orders
   - Budget allocations
   - Regulatory changes
   - Official announcements

2. For each action, check against promise database:
   - Does it advance any promise?
   - Does it contradict any promise?

3. Update promise status with evidence citation
```

**Step 4: Rating Decision Tree**
```
Has action been taken?
├── No → "Not Yet Rated" or "Stalled"
└── Yes
    ├── Goal fully achieved? → "Kept"
    ├── Partial progress/compromise? → "Partial/Compromise"
    └── Reversed or blocked? → "Broken"

End of term?
├── "In Progress" → "Broken"
└── Keep current rating
```

**Step 5: Quality Control**
```
1. All ratings supported by citations
2. Regular review cycle (monthly/quarterly)
3. Public methodology documentation
4. Appeals/correction process
```

---

### Best Practices from Existing Implementations

**What Works:**
1. **Double-blind coding** reduces bias (Polimeter)
2. **Testability requirement** excludes vague promises (CPPG)
3. **Citation for every rating** enables verification (All)
4. **Regular updates** maintain relevance (PolitiFact)
5. **Clear methodology docs** build trust (FullFact)

**Common Pitfalls:**
1. Including vague/untestable promises
2. Allowing "In Progress" indefinitely (use end-of-term auto-break)
3. Not weighting by importance (Mellon finding)
4. Single-coder bias (always use multiple coders)
5. Outdated ratings (need active monitoring)

**Lessons Learned:**
1. "Partially fulfilled" often collapses to binary for analysis
2. Promises about maintaining status quo are easier to "keep"
3. Post-election promises should be tracked separately
4. Voters remember broken promises better than kept ones (negativity bias)

---

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

## Confidence Level

**High** - Multiple sources agree on methodology (PolitiFact, Polimeter, CPPG all publish detailed methodology docs). Academic literature well-established (Thomson-Royed framework widely cited). Recent sources (2024-2025) confirm continued use of these approaches.

**Medium** - Semantic matching/automation is emerging area with less consensus. No production NLP system for automated promise-to-vote matching found.

**Low** - Specific formulas for handling multiple conflicting votes (threshold algorithms) not documented anywhere. Appears to be expert judgment, not algorithmic.
