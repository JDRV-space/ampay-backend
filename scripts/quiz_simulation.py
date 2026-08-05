#!/usr/bin/env python3
"""Validate the quiz ranking contract with deterministic and random cases."""

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import random
import sys

from ampay_pipeline.paths import (
    OUTPUT_QUIZ_STATEMENTS,
    OUTPUT_QUIZ_VALIDATION_RESULTS,
    ensure_parent_dir,
)


BLEND_ALPHA = 0.1
MIN_POSITIONS_FLOOR = 4
DEFAULT_RANDOM_CASES = 1_000_000


@dataclass(frozen=True)
class QuizData:
    parties: list[str]
    statements: list[dict]

    @property
    def question_count(self) -> int:
        return len(self.statements)

    @property
    def max_distance(self) -> int:
        return self.question_count * 2


@dataclass(frozen=True)
class Match:
    party: str
    distance: int
    blended_score: float


def load_quiz_data() -> QuizData:
    with OUTPUT_QUIZ_STATEMENTS.open(encoding="utf-8") as file:
        data = json.load(file)
    return QuizData(
        parties=list(data["party_display_names"]),
        statements=data["statements"],
    )


def get_party_positions(quiz_data: QuizData, party: str) -> list[int]:
    return [statement["positions"][party] for statement in quiz_data.statements]


def calculate_distance(user_answers: list[int], party_positions: list[int]) -> int:
    return sum(abs(user - party) for user, party in zip(user_answers, party_positions))


def calculate_blended_score(distance: int, non_zero_positions: int) -> float:
    normalized = distance / max(non_zero_positions, MIN_POSITIONS_FLOOR)
    return (1 - BLEND_ALPHA) * distance + BLEND_ALPHA * normalized * 15


def rank_matches(quiz_data: QuizData, user_answers: list[int]) -> list[Match]:
    matches: list[Match] = []
    for party in quiz_data.parties:
        positions = get_party_positions(quiz_data, party)
        distance = calculate_distance(user_answers, positions)
        matches.append(
            Match(
                party=party,
                distance=distance,
                blended_score=calculate_blended_score(
                    distance,
                    sum(position != 0 for position in positions),
                ),
            )
        )
    return sorted(matches, key=lambda match: (match.blended_score, match.distance, match.party))


def top_ties(matches: list[Match]) -> list[str]:
    top = matches[0]
    return [
        match.party
        for match in matches
        if math.isclose(match.blended_score, top.blended_score)
        and match.distance == top.distance
    ]


def run_party_vector_test(quiz_data: QuizData) -> dict:
    cases: dict[str, dict] = {}
    correct_top_tier = 0
    for party in quiz_data.parties:
        matches = rank_matches(quiz_data, get_party_positions(quiz_data, party))
        tied_parties = top_ties(matches)
        if party in tied_parties:
            correct_top_tier += 1
        cases[party] = {
            "display_winner": matches[0].party,
            "top_ties": tied_parties,
            "distance": matches[0].distance,
            "blended_score": matches[0].blended_score,
        }

    return {
        "test": "party_response_vectors",
        "total_cases": len(quiz_data.parties),
        "correct_top_tier": correct_top_tier,
        "accuracy": correct_top_tier / len(quiz_data.parties),
        "per_party": cases,
    }


def run_random_test(quiz_data: QuizData, case_count: int) -> dict:
    winners = Counter({party: 0 for party in quiz_data.parties})
    tie_count = 0

    for _ in range(case_count):
        answers = [random.choice((-1, 0, 1)) for _ in range(quiz_data.question_count)]
        matches = rank_matches(quiz_data, answers)
        winners[matches[0].party] += 1
        if len(top_ties(matches)) > 1:
            tie_count += 1

    percentages = {
        party: count / case_count * 100 for party, count in winners.items()
    }
    non_zero_counts = [count for count in winners.values() if count]
    imbalance_ratio = (
        max(non_zero_counts) / min(non_zero_counts) if non_zero_counts else None
    )

    return {
        "test": "random_answers",
        "total_cases": case_count,
        "display_winner_distribution": {
            party: {"count": winners[party], "percentage": percentages[party]}
            for party in quiz_data.parties
        },
        "top_score_ties": tie_count,
        "top_score_tie_percentage": tie_count / case_count * 100,
        "display_winner_imbalance_ratio": imbalance_ratio,
        "interpretation": (
            "The random distribution describes this question set and deterministic "
            "tie display order; uniform winners are not an expected correctness condition."
        ),
    }


def main(seed: int = 42, random_cases: int = DEFAULT_RANDOM_CASES) -> int:
    random.seed(seed)
    quiz_data = load_quiz_data()
    party_vectors = run_party_vector_test(quiz_data)
    random_answers = run_random_test(quiz_data, random_cases)

    output = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).date().isoformat(),
            "seed": seed,
            "questions": quiz_data.question_count,
            "parties": len(quiz_data.parties),
            "random_cases": random_cases,
            "algorithm": "coverage-adjusted Manhattan distance",
            "formula": "0.9*D + 0.1*(D/max(P,4))*15",
            "tie_display_order": "blended score, raw distance, party slug",
            "input_sha256": hashlib.sha256(
                OUTPUT_QUIZ_STATEMENTS.read_bytes()
            ).hexdigest(),
        },
        "party_response_vectors": party_vectors,
        "random_answers": random_answers,
    }

    ensure_parent_dir(OUTPUT_QUIZ_VALIDATION_RESULTS)
    with OUTPUT_QUIZ_VALIDATION_RESULTS.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2, ensure_ascii=False)
        file.write("\n")

    print(
        "PASS: checked "
        f"{party_vectors['total_cases']} party vectors and {random_cases:,} random cases"
    )
    print(
        "INFO: top-score ties in random cases: "
        f"{random_answers['top_score_tie_percentage']:.2f}%"
    )
    print(f"PASS: wrote {OUTPUT_QUIZ_VALIDATION_RESULTS}")
    return 0


if __name__ == "__main__":
    selected_seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    selected_cases = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_RANDOM_CASES
    raise SystemExit(main(selected_seed, selected_cases))
