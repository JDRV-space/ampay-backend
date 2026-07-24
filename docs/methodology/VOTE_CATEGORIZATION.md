# Vote Categorization

AMPAY assigns each substantive congressional vote to one primary thematic category so votes can be compared with party promises and displayed consistently.

## Process

1. Remove non-substantive procedural or declarative votes when they do not express a policy position.
2. Match the remaining vote title and summary against category-specific keywords.
3. Review ambiguous matches manually.
4. Store the final category in `data/02_output/votes_categorized.json`.

## Category Rule

Each vote receives one primary category. When a vote touches multiple topics, the selected category should reflect the main policy effect of the vote, not every secondary topic mentioned in the title.

## Quality Controls

- Borderline cases require manual review.
- Similar votes should receive consistent categories.
- Category limitations should be documented rather than hidden.

## Limitations

- Some votes genuinely cross categories.
- Keyword matching can miss context or over-match common terms.
- Category labels simplify complex legislation.
- The categories are a working analytical layer, not official congressional taxonomy.
