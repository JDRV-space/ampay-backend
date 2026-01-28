
# Voting Advice Applications (VAAs): A Research Report

## Introduction

Voting Advice Applications (VAAs) are online tools designed to help voters discover which political parties or candidates best align with their personal preferences. Users answer a series of questions on various political, social, and economic issues, and the VAA then calculates a "match" score with different political entities. This report provides a comprehensive overview of the methodologies, scoring algorithms, and academic critiques of major VAAs.

## Major VAA Platforms and their Methodologies

### iSideWith.com

*   **Methodology:** iSideWith uses a proprietary algorithm that goes beyond simple question-and-answer matching.
*   **Scoring Factors:**
    *   **User Input:** Users answer yes/no questions, can choose nuanced stances, and weight the importance of each issue.
    *   **Candidate Stances:** The platform meticulously researches and documents the official and stated positions of candidates.
    *   **Passion Factors:** The algorithm considers how frequently a candidate discusses an issue.
    *   **Confidence Factors:** This includes the longevity of a candidate's stance and their voting record.
    *   **Conviction Score:** A candidate's score is lowered if they have changed their position on an issue.
*   **URL:** [https://www.isidewith.com/](https://www.isidewith.com/)

### Vote Compass

*   **Methodology:** Developed by Vox Pop Labs, Vote Compass uses a Likert-type scale for user responses.
*   **Scoring Factors:**
    *   **Party Position Coding:** Researchers code party positions based on public records, and parties are consulted for feedback.
    *   **Alignment Scoring:** The algorithm calculates the absolute difference between a user's response and a party's position on each question.
*   **URL:** [https://votecompass.com/](https://votecompass.com/)

### Wahl-O-Mat (Germany)

*   **Methodology:** Wahl-O-Mat, run by the German Federal Agency for Civic Education (bpb), uses the "city block" (Manhattan distance) method.
*   **Scoring Factors:**
    *   **User Input:** Users respond with "agree," "disagree," or "neutral."
    *   **Weighting:** Users can "double weight" important questions.
    *   **Scoring:** A difference between "agree" and "disagree" is 2 points, while a difference to "neutral" is 1 point. The party with the lowest total score is the best match.
*   **URL:** [https://www.wahl-o-mat.de/](https://www.wahl-o-mat.de/)

### EU Vote Match / EUandI

*   **Methodology:** These platforms often use the Manhattan distance or Euclidean distance.
*   **Scoring Factors:**
    *   **Numerical Conversion:** Responses on a 5-point Likert scale are converted to numerical values (e.g., 0, 25, 50, 75, 100).
    *   **Saliency Weighting:** Users can weight the importance of issues.
    *   **Distance Calculation:** The Manhattan or Euclidean distance is calculated between the user's and the party's vector of responses.
*   **URL:** [https://www.votematch.eu/](https://www.votematch.eu/), [https://euandi.eu/](https://euandi.eu/)

### VoteMatch UK

*   **Methodology:** Aims for transparency by avoiding "hidden algorithms."
*   **Scoring Factors:**
    *   **Simple Agreement:** The core of the algorithm is adding up the number of agreements between the user and the party.
    *   **Optional Weighting:** Users can give extra weight to important issues.
*   **URL:** [https://votematch.org.uk/](https://votematch.org.uk/)

### Smartvote (Switzerland)

*   **Methodology:** Primarily uses the "city block" (Manhattan distance) model, but also mentions Euclidean distance.
*   **Scoring Factors:**
    *   **Distance Calculation:** Calculates the political distance between the user and candidates/parties.
    *   **Weighting:** Users can weight questions with a plus (counts double) or minus (counts half).
    *   **Normalization:** The calculated distance is normalized to a 0-100 matching score.
*   **URL:** [https://www.smartvote.ch/](https://www.smartvote.ch/)

## Scoring Algorithms

### Simple Agreement Counting

*   **Formula:** `(Number of Agreements / Total Number of Questions) * 100`
*   **Explanation:** The most basic method. It simply counts the number of times a user's answer matches a party's position. It is easy to understand but lacks nuance.

### Weighted Agreement

*   **Formula:** Varies, but often involves a weighted Kappa or a simple modification of the agreement formula where weighted questions count more (e.g., double).
*   **Explanation:** This method allows users to assign importance to specific issues. An agreement on a weighted issue contributes more to the final score.

### Manhattan Distance (City-Block Distance)

*   **Formula:** `D = Σ|user_i - party_i|`
*   **Explanation:** This formula calculates the "distance" between a user and a party by summing the absolute differences of their positions on each issue `i`. The lower the distance, the closer the match. This is one of the most common methods used by VAAs.

### Euclidean Distance

*   **Formula:** `D = sqrt(Σ(user_i - party_i)^2)`
*   **Explanation:** This formula calculates the straight-line distance between the user and the party in a multi-dimensional space. It gives more weight to large differences on a single issue compared to the Manhattan distance.

### Cosine Similarity

*   **Formula:** `Similarity = (A · B) / (||A|| * ||B||)`
*   **Explanation:** This formula measures the cosine of the angle between two vectors (user and party). It is less about the magnitude of agreement/disagreement and more about the overall orientation of political views. A score of 1 means they are perfectly aligned, while -1 means they are diametrically opposed.

## Technical Implementation Details

### Scale Handling (Likert Scales)

*   VAAs commonly use 3, 5, or 7-point Likert scales to allow for nuanced responses (e.g., "Strongly Agree" to "Strongly Disagree").
*   The number of points on the scale (odd or even) can influence whether a user is forced to take a stance or can remain neutral.

### Score Normalization

*   To compare scores from different scales and questions, VAAs must normalize them, typically to a 0-100% range.
*   **Min-Max Normalization:** `(X - min) / (max - min)` is a common method.
*   **Z-score Normalization:** `(X - mean) / std_dev` is another option.

### Salience Weighting and Double Weighting

*   **Salience Weighting:** This allows users to indicate the importance of issues, which then modifies the calculation. For distance-based algorithms, the distance on a weighted issue is multiplied by a factor (e.g., 2 for "very important").
*   **Double Weighting Controversy:** Some VAAs, like Wahl-O-Mat, use "double weighting," where user-selected important issues have twice the impact. This has been critiqued for potentially distorting the results if not implemented carefully, as it can overshadow the collective importance of many smaller issues.

## Academic Research and Critiques (2020-2025)

### Summary of Findings

*   Recent research emphasizes the need for methodological transparency and robustness in VAAs.
*   There is a growing interest in the effects of VAA design choices (e.g., number of questions, scale type) on user behavior and outcomes.

### Critiques of VAA Algorithms and Methodologies

*   **Accuracy and Validity:** The accuracy of VAAs is a subject of ongoing debate. The way parties' positions are coded (by experts or by the parties themselves) can significantly impact the results.
*   **Algorithmic Bias:** The choice of algorithm (e.g., Manhattan vs. Euclidean distance) is not neutral and can lead to different recommendations.
*   **Oversimplification:** VAAs can oversimplify complex political issues and may not capture the full spectrum of a user's or a party's views.
*   **Data Quality:** The validity of VAA data can be compromised by unrealistic user behavior.

### Research by Diego Garzia

*   Diego Garzia is a prominent scholar in the field of VAAs. His research focuses on the usage and effects of VAAs on voter behavior and political polarization. He is a proponent of using VAAs as tools for civic education.

## Best Practices and Recommendations

### Algorithm Accuracy

*   There is no single "most accurate" algorithm. The choice of algorithm depends on the specific goals of the VAA.
*   Hybrid methods that combine different approaches may provide more robust results.

### Preventing Gaming and Manipulation

*   VAAs should be designed to be robust against "gaming" by users who may try to manipulate the outcome.
*   Clear instructions and transparent methodologies can help mitigate this.

### UX Considerations

*   The user experience is crucial. VAAs should have a clear and intuitive interface.
*   The number of questions should be manageable to avoid user fatigue.

### Transparency Requirements

*   The methodology and algorithms used by VAAs should be transparent and publicly accessible. This allows for academic scrutiny and builds trust with users.

## Referencias

Para ver todas las referencias academicas y fuentes utilizadas en AMPAY, consulta el documento centralizado:
[Bibliografia y Fuentes](/referencia/fuentes)

---

*This report was generated by an AI assistant based on publicly available information.*
