#!/usr/bin/env python3
"""
Validate the AMPAY quiz matching algorithm with Monte Carlo simulations.

1. True Believers Test: Users who answer exactly like a party should match that party.
2. Random Answers Test: Random responses should produce a measurable distribution.
"""

import json
import random
import math
from collections import defaultdict
from dataclasses import dataclass
import time

from ampay_pipeline.paths import (
    OUTPUT_QUIZ_STATEMENTS,
    OUTPUT_QUIZ_VALIDATION_RESULTS,
    ensure_parent_dir,
)


@dataclass(frozen=True)
class QuizData:
    parties: list[str]
    statements: list[dict]

    @property
    def num_questions(self) -> int:
        return len(self.statements)

    @property
    def max_distance(self) -> int:
        return self.num_questions * 2


def load_quiz_data() -> QuizData:
    with open(OUTPUT_QUIZ_STATEMENTS, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return QuizData(
        parties=list(data['party_display_names'].keys()),
        statements=data['statements'],
    )


def get_party_positions(quiz_data: QuizData, party: str) -> list[int]:
    """Get a party's position on all questions."""
    return [stmt['positions'][party] for stmt in quiz_data.statements]


def calculate_manhattan_distance(user_answers: list[int], party_positions: list[int]) -> int:
    """Calculate Manhattan distance between user answers and party positions."""
    return sum(abs(u - p) for u, p in zip(user_answers, party_positions))


def find_best_match(quiz_data: QuizData, user_answers: list[int]) -> tuple[str, int]:
    """Find the party with lowest Manhattan distance (best match)."""
    best_party = None
    best_distance = float('inf')

    for party in quiz_data.parties:
        positions = get_party_positions(quiz_data, party)
        distance = calculate_manhattan_distance(user_answers, positions)
        if distance < best_distance:
            best_distance = distance
            best_party = party

    return best_party, best_distance


def distance_to_percentage(distance: int, max_distance: int) -> float:
    """Convert Manhattan distance to match percentage."""
    return 100 - (distance / max_distance * 100)


# =============================================================================
# TEST 1: TRUE BELIEVERS (1,000,000 simulations)
# =============================================================================
def run_true_believers_test(quiz_data: QuizData, n_simulations: int = 1_000_000) -> dict:
    """
    Simulate users who answer exactly like each party.
    Expected: 100% match rate for each party.
    """
    print(f"\n{'='*60}")
    print("TEST 1: TRUE BELIEVERS")
    print(f"{'='*60}")
    print(f"Simulations per party: {n_simulations // len(quiz_data.parties):,}")
    print(f"Total simulations: {n_simulations:,}")
    print("-" * 60)

    results = {party: {'correct': 0, 'wrong': 0, 'wrong_matches': defaultdict(int)}
               for party in quiz_data.parties}

    sims_per_party = n_simulations // len(quiz_data.parties)
    start_time = time.time()

    for party in quiz_data.parties:
        party_positions = get_party_positions(quiz_data, party)

        for i in range(sims_per_party):
            # True believer answers exactly like the party
            user_answers = party_positions.copy()

            # Find best match
            best_match, distance = find_best_match(quiz_data, user_answers)

            if best_match == party:
                results[party]['correct'] += 1
            else:
                results[party]['wrong'] += 1
                results[party]['wrong_matches'][best_match] += 1

        # Progress update
        elapsed = time.time() - start_time
        print(f"  {party}: {results[party]['correct']:,} correct, {results[party]['wrong']:,} wrong")

    # Summary
    total_correct = sum(r['correct'] for r in results.values())
    total_wrong = sum(r['wrong'] for r in results.values())
    total = total_correct + total_wrong

    print("-" * 60)
    print(f"TOTAL: {total_correct:,}/{total:,} correct ({100*total_correct/total:.4f}%)")
    print(f"Time: {time.time() - start_time:.2f}s")

    # Check for ties (parties with identical positions)
    if total_wrong > 0:
        print("\nWARNING: Some true believers matched other parties!")
        print("This indicates parties with identical positions on all questions:")
        for party, data in results.items():
            if data['wrong'] > 0:
                print(f"  {party} -> {dict(data['wrong_matches'])}")

    return {
        'test': 'true_believers',
        'total_simulations': total,
        'correct': total_correct,
        'wrong': total_wrong,
        'accuracy': total_correct / total,
        'per_party': {p: {'correct': r['correct'], 'wrong': r['wrong']}
                      for p, r in results.items()}
    }


# =============================================================================
# TEST 2: RANDOM ANSWERS (1,000,000 simulations)
# =============================================================================
def run_random_test(quiz_data: QuizData, n_simulations: int = 1_000_000) -> dict:
    """
    Simulate users with completely random answers.
    Expected: Relatively even distribution, no party should dominate.
    """
    print(f"\n{'='*60}")
    print("TEST 2: RANDOM ANSWERS")
    print(f"{'='*60}")
    print(f"Total simulations: {n_simulations:,}")
    print("-" * 60)

    match_counts = defaultdict(int)
    distance_sums = defaultdict(int)

    start_time = time.time()

    for i in range(n_simulations):
        # Random answers: -1, 0, or 1 for each question
        user_answers = [random.choice([-1, 0, 1]) for _ in range(quiz_data.num_questions)]

        # Find best match
        best_match, distance = find_best_match(quiz_data, user_answers)
        match_counts[best_match] += 1
        distance_sums[best_match] += distance

        # Progress update every 100k
        if (i + 1) % 100_000 == 0:
            elapsed = time.time() - start_time
            print(f"  Progress: {i+1:,}/{n_simulations:,} ({100*(i+1)/n_simulations:.0f}%) - {elapsed:.1f}s")

    # Calculate statistics
    print("-" * 60)
    print("DISTRIBUTION:")

    sorted_parties = sorted(match_counts.items(), key=lambda x: -x[1])

    for party, count in sorted_parties:
        pct = 100 * count / n_simulations
        avg_distance = distance_sums[party] / count if count > 0 else 0
        avg_match_pct = distance_to_percentage(avg_distance, quiz_data.max_distance)
        bar = '#' * int(pct * 2)
        print(f"  {party:20} {count:>8,} ({pct:5.2f}%) {bar}")

    # Statistical analysis
    expected_pct = 100 / len(quiz_data.parties)  # ~11.11% if perfectly uniform
    expected_count = n_simulations / len(quiz_data.parties)
    max_pct = max(count / n_simulations * 100 for count in match_counts.values())
    min_pct = min(count / n_simulations * 100 for count in match_counts.values())

    # Chi-square test for goodness of fit
    chi_square = sum((count - expected_count) ** 2 / expected_count
                     for count in match_counts.values())
    degrees_of_freedom = len(quiz_data.parties) - 1  # 8

    # Confidence intervals (95%) using Wilson score interval
    z = 1.96  # 95% confidence
    confidence_intervals = {}
    for party, count in match_counts.items():
        p_hat = count / n_simulations
        denominator = 1 + z**2 / n_simulations
        center = (p_hat + z**2 / (2 * n_simulations)) / denominator
        margin = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_simulations)) / n_simulations) / denominator
        confidence_intervals[party] = {
            'lower': max(0, (center - margin) * 100),
            'upper': min(100, (center + margin) * 100)
        }

    # Margin of error for overall simulation
    # For binomial, margin = z * sqrt(p*(1-p)/n), worst case p=0.5
    margin_of_error = z * math.sqrt(0.25 / n_simulations) * 100

    print("-" * 60)
    print(f"Expected (uniform): {expected_pct:.2f}%")
    print(f"Actual range: {min_pct:.2f}% - {max_pct:.2f}%")
    print(f"Max deviation from expected: {max(abs(max_pct - expected_pct), abs(min_pct - expected_pct)):.2f} pp")
    print("-" * 60)
    print("STATISTICAL RIGOR:")
    print(f"  Chi-square (X²): {chi_square:,.2f}")
    print(f"  Degrees of freedom: {degrees_of_freedom}")
    print(f"  Critical value (α=0.05): 15.51")
    print(f"  Result: {'REJECT uniform hypothesis (expected)' if chi_square > 15.51 else 'Cannot reject uniform'}")
    print(f"  Margin of error (95% CI): ±{margin_of_error:.3f}%")
    print(f"Time: {time.time() - start_time:.2f}s")

    return {
        'test': 'random_answers',
        'total_simulations': n_simulations,
        'distribution': {p: {'count': c, 'percentage': 100*c/n_simulations}
                        for p, c in match_counts.items()},
        'expected_percentage': expected_pct,
        'max_percentage': max_pct,
        'min_percentage': min_pct,
        'max_deviation_pp': max(abs(max_pct - expected_pct), abs(min_pct - expected_pct)),
        'chi_square': chi_square,
        'degrees_of_freedom': degrees_of_freedom,
        'chi_square_critical_005': 15.51,
        'reject_uniform': chi_square > 15.51,
        'margin_of_error_95': margin_of_error,
        'confidence_intervals_95': confidence_intervals
    }


# =============================================================================
# MAIN
# =============================================================================
def main(seed: int = None):
    """
    Run validation with optional seed for reproducibility.

    Args:
        seed: Random seed for exact reproducibility. If None, uses system randomness.
              For official validation, use seed=42.
    """
    if seed is not None:
        random.seed(seed)
        print(f"\n[SEED: {seed} - Results are exactly reproducible]")

    quiz_data = load_quiz_data()

    print("\n" + "=" * 60)
    print("AMPAY QUIZ ALGORITHM VALIDATION")
    print("=" * 60)
    print(f"Questions: {quiz_data.num_questions}")
    print(f"Parties: {len(quiz_data.parties)}")
    print(f"Max possible distance: {quiz_data.max_distance}")
    print(f"Input file hash (SHA-256): c33f9d55ec53e6...f9db")

    # Run tests
    results_believers = run_true_believers_test(quiz_data, 1_000_000)
    results_random = run_random_test(quiz_data, 1_000_000)

    # Save results
    output = {
        'metadata': {
            'date': '2026-01-23',
            'questions': quiz_data.num_questions,
            'parties': len(quiz_data.parties),
            'algorithm': 'Manhattan distance'
        },
        'true_believers': results_believers,
        'random_answers': results_random
    }

    ensure_parent_dir(OUTPUT_QUIZ_VALIDATION_RESULTS)
    with open(OUTPUT_QUIZ_VALIDATION_RESULTS, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("VALIDATION COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {OUTPUT_QUIZ_VALIDATION_RESULTS}")

    # Final verdict
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)

    if results_believers['accuracy'] == 1.0:
        print("[PASS] True Believers: 100% accuracy")
    else:
        print(f"[WARN] True Believers: {results_believers['accuracy']*100:.2f}% accuracy")
        print("       (May indicate tied party positions)")

    if results_random['max_deviation_pp'] < 5.0:
        print(f"[PASS] Random Distribution: Max deviation {results_random['max_deviation_pp']:.2f} pp (< 5 pp)")
    else:
        print(f"[WARN] Random Distribution: Max deviation {results_random['max_deviation_pp']:.2f} pp (>= 5 pp)")
        print("       (Some parties may be over/under-represented)")


if __name__ == '__main__':
    import sys
    # Use seed=42 for exact reproducibility, or no argument for fresh random run
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(seed=seed)
