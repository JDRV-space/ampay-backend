# Frequently Asked Questions (FAQ)

**Version:** 1.0
**Date:** 2026-01-21
**Language:** English

---

## About AMPAY

### What is AMPAY?

AMPAY is a political transparency tool that enables citizens to:
1. Discover which parties align with their positions through a quiz
2. View contradictions between campaign promises and congressional votes
3. Explore voting patterns by party and category

### Why is it called "AMPAY"?

"Ampay" is a Peruvian colloquial expression meaning to catch someone in the act or to uncover something hidden. We use this term because the tool "catches" parties when they vote contrary to their promises.

### Who created AMPAY?

AMPAY was created by GitHub user [JDRV-space](https://github.com/JDRV-space), an independent Peruvian citizen committed to improving political transparency. We have no affiliation with any political party.

---

## About the Quiz

### How does the quiz work?

The quiz asks you 8 questions about political topics. We compare your answers with the positions of 9 parties using an algorithm called "Manhattan distance" (the same algorithm used by similar tools in Germany and Switzerland). The party with the smallest "distance" is your closest match.

### Do the calibration questions affect my result?

Not directly. The calibration questions (left/right, conservative/progressive) only filter HOW results are presented. Your mathematical match is always calculated the same way, but we display first the parties within your self-identified ideological alignment.

### Why only 8 questions?

We want the quiz to be fast and accessible. More questions would increase accuracy but reduce the completion rate. The 8 questions were selected to cover the most differentiating topics across parties.

### Does the quiz tell me who to vote for?

**NO.** AMPAY is informational, not a voting recommendation. The quiz shows you matches based on positions declared in government plans. You should always conduct further research before deciding your vote.

### What does the match percentage mean?

The percentage indicates how similar your position is to that of the party. 100% would represent a perfect match; 0% would represent total opposition. Most users score between 50-80% with several parties.

---

## About AMPAYs

### What exactly is an AMPAY?

An AMPAY occurs when we find that a party:
- Made a specific promise in its government plan
- Voted contrary to that promise in Congress

For example: promising to "eliminate tax exemptions" but voting YES on laws that extend them.

### How are AMPAYs verified?

Each AMPAY undergoes:
1. Automated detection (pattern matching)
2. Source verification (actual promise, actual vote)
3. Logical connection analysis (does the law relate to the promise?)
4. Manual review before publication

### Why are there so few AMPAYs?

We only publish AMPAYs with high confidence. Many "AMPAY candidates" are discarded because:
- The connection between the promise and the law was weak
- There were only 1-2 votes (insufficient pattern)
- Context existed that explained the vote

### Can parties dispute an AMPAY?

Yes. Any party or citizen may open an issue on our GitHub repository with evidence contradicting our analysis. We will review and correct as appropriate.

### Why do some parties have more AMPAYs than others?

The reasons may vary:
- They made more specific promises (more verifiable)
- They had more opportunities to vote on matters related to their promises
- They actually voted contrary to their promises more frequently

This does not necessarily mean that one party is "worse" than another.

---

## About the Data

### Where do the voting data come from?

We use data from Open Politica, a civil society organization that collects and publishes votes from the Peruvian Congress. You can verify the original data in their GitHub repository.

### Where do the promises come from?

Promises are extracted from the official Government Plans (Planes de Gobierno) registered with the Jurado Nacional de Elecciones (JNE). These are public documents available on the JNE's electoral platform.

### Why do the data only go up to July 2024?

The voting dataset we use was last updated in July 2024. More recent votes are not included. We plan to update the data when new records become available.

### Can I download the data?

Yes. All our data are open and available on GitHub. We want journalists, researchers, and citizens to be able to verify and use our data.

---

## About the Methodology

### What algorithm does the quiz use?

We use Manhattan distance, the same algorithm used by Wahl-O-Mat in Germany and Smartvote in Switzerland. It is a standard in Voting Advice Applications (VAAs) due to its simplicity and interpretability.

### How are party positions assigned?

We read the government plans and assign:
- +1 if there is an explicit promise in favor
- -1 if there is an explicit promise against
- 0 if there is no clear position or the party was silent

### Why do you use only promises and not votes for the quiz?

The quiz is designed for the 2026 elections, so we use the parties' 2026 proposals. The votes are from the 2021-2024 period and reflect historical behavior, not current proposals. Votes are used in the AMPAY section.

### Has the methodology been validated academically?

Our methodology is based on academic literature on VAAs and electoral promise fulfillment. We cite all our sources in the documentation. We have not conducted a formal external validation, but our code and data are open for scrutiny.

---

## About Privacy

### Do you store my quiz answers?

We do not store individual responses or personal data. The calculation is performed in your browser and is not sent to any server.

### Do you use cookies?

Only technical cookies necessary for the site to function. We do not use tracking or advertising cookies.

---

## Issues and Errors

### I found an error in an AMPAY. How do I report it?

Open an issue on our GitHub repository with:
- The AMPAY ID
- What you believe is incorrect
- Evidence supporting your claim

### The quiz does not work in my browser

AMPAY works best in modern browsers (Chrome, Firefox, Safari, and Edge, up to date). If you experience issues, try:
1. Updating your browser
2. Disabling extensions that block JavaScript
3. Clearing your browser cache

### Why does my favorite party not appear?

We only include parties with significant parliamentary representation during the 2021-2026 period. New or very small parties may not be included.

---

## Contact

### How can I contact the creator?

- GitHub: https://github.com/JDRV-space (bug reports, suggestions, contributions)
- X (Twitter): https://x.com/JDRV_space

### Can I contribute to the project?

Yes. AMPAY is open source. You can:
- Report errors
- Suggest improvements
- Contribute code
- Assist with data verification

---

## Disclaimers

### Is AMPAY politically neutral?

AMPAY is an informational tool based on public data. We do not make voting recommendations nor endorse any political party. Our objective is transparency, not political promotion.

### Is the information 100% accurate?

We make our best effort to be accurate, but:
- The data may contain minor errors
- The interpretation of promises has a subjective component
- The political context may be more complex than what we present

We always recommend verifying original sources for important decisions.

---

*Last updated: 2026-01-21*
