#!/usr/bin/env python3
"""Validate cross-file contracts for the committed AMPAY outputs."""

from collections import Counter
import hashlib
import json
import sys

from ampay_pipeline.parties import PARTY_NAME_TO_SLUG, TARGET_PARTY_SLUGS
from ampay_pipeline.paths import (
    OUTPUT_AMPAYS,
    OUTPUT_CONFIRMED_AMPAYS,
    OUTPUT_PARTY_PATTERNS,
    OUTPUT_QUIZ_STATEMENTS,
    OUTPUT_QUIZ_VALIDATION_RESULTS,
    OUTPUT_VOTES_BY_PARTY,
    OUTPUT_VOTES_CATEGORIZED,
)

from validate_ampay_traceability import main as validate_traceability


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def collect_contract_errors() -> list[str]:
    errors: list[str] = []
    confirmed_data = load_json(OUTPUT_CONFIRMED_AMPAYS)
    public_data = load_json(OUTPUT_AMPAYS)
    votes_data = load_json(OUTPUT_VOTES_CATEGORIZED)
    votes_by_party = load_json(OUTPUT_VOTES_BY_PARTY)
    party_patterns = load_json(OUTPUT_PARTY_PATTERNS)
    quiz_statements = load_json(OUTPUT_QUIZ_STATEMENTS)
    quiz_validation = load_json(OUTPUT_QUIZ_VALIDATION_RESULTS)

    votes = votes_data.get("votes", [])
    dates = [vote["date"] for vote in votes]
    vote_types = Counter(vote["vote_type"] for vote in votes)
    coverage = f"{min(dates)} to {max(dates)}" if dates else ""

    if votes_data.get("total_votes") != len(votes):
        errors.append("votes_categorized total_votes does not match its vote records")
    if votes_data.get("classification_stats", {}).get("by_vote_type") != dict(vote_types):
        errors.append("votes_categorized by_vote_type does not match its vote records")
    if votes_by_party.get("total_votes") != len(votes_by_party.get("votes", {})):
        errors.append("votes_by_party total_votes does not match its vote records")
    if votes_by_party.get("total_votes") != len(votes):
        errors.append("votes_by_party and votes_categorized have different vote counts")

    confirmed = confirmed_data.get("ampays", [])
    public = public_data.get("ampays", [])
    confirmed_by_id = {ampay["id"]: ampay for ampay in confirmed}
    public_by_id = {ampay["id"]: ampay for ampay in public}

    if public_data.get("total") != len(public):
        errors.append("ampays.json total does not match len(ampays)")
    if set(public_by_id) != set(confirmed_by_id):
        errors.append("ampays.json IDs do not match AMPAY_CONFIRMED_2021.json")
    if public_data.get("data_disclaimer", {}).get("coverage") != coverage:
        errors.append(
            "ampays.json coverage does not match votes_categorized date range: "
            f"{public_data.get('data_disclaimer', {}).get('coverage')} != {coverage}"
        )

    expected_by_party = dict.fromkeys(TARGET_PARTY_SLUGS, 0)
    for ampay in confirmed:
        slug = PARTY_NAME_TO_SLUG.get(ampay.get("party"))
        if slug in expected_by_party:
            expected_by_party[slug] += 1
    if public_data.get("by_party") != expected_by_party:
        errors.append("ampays.json by_party does not match confirmed AMPAY records")

    votes_index = {vote["vote_id"]: vote for vote in votes}
    party_votes = votes_by_party.get("votes", {})
    for ampay_id, confirmed_ampay in confirmed_by_id.items():
        public_ampay = public_by_id.get(ampay_id)
        if not public_ampay:
            continue

        party_slug = PARTY_NAME_TO_SLUG.get(confirmed_ampay.get("party"))
        evidence = confirmed_ampay.get("evidence", {})
        expected_fields = {
            "party_slug": party_slug,
            "party_name": confirmed_ampay.get("party"),
            "promise": confirmed_ampay.get("promise_text"),
            "category": confirmed_ampay.get("promise_category"),
            "vote_position": evidence.get("vote"),
            "expected_position": evidence.get("expected_vote"),
            "confidence": confirmed_ampay.get("confidence"),
        }
        for field, expected in expected_fields.items():
            if public_ampay.get(field) != expected:
                errors.append(f"{ampay_id} public {field} disagrees with confirmed evidence")

        confirmed_vote_ids = {
            reference.get("vote_id") for reference in evidence.get("vote_references", [])
        }
        public_vote_ids = {
            reference.get("vote_id")
            for reference in public_ampay.get("vote_references", [])
        }
        if public_vote_ids != confirmed_vote_ids:
            errors.append(f"{ampay_id} public vote references disagree with confirmed evidence")

        for reference in public_ampay.get("vote_references", []):
            vote_id = reference.get("vote_id")
            vote = votes_index.get(vote_id)
            party_vote = party_votes.get(vote_id)
            if not vote or not party_vote or not party_slug:
                continue
            expected_reference = {
                "date": vote.get("date"),
                "category": vote.get("category"),
                "vote_type": vote.get("vote_type"),
                "party_position": party_vote["parties"][party_slug]["position"],
            }
            for field, expected in expected_reference.items():
                if reference.get(field) != expected:
                    errors.append(f"{ampay_id} public {field} is stale for vote {vote_id}")

    expected_parties = set(TARGET_PARTY_SLUGS)
    if set(votes_by_party.get("parties", [])) != expected_parties:
        errors.append("votes_by_party does not contain the nine tracked parties")
    if set(party_patterns.get("parties", {})) != expected_parties:
        errors.append("party_patterns does not contain the nine tracked parties")
    if len(quiz_statements.get("statements", [])) != 15:
        errors.append("quiz_statements does not contain 15 statements")

    quiz_metadata = quiz_validation.get("metadata", {})
    quiz_hash = hashlib.sha256(OUTPUT_QUIZ_STATEMENTS.read_bytes()).hexdigest()
    if quiz_metadata.get("input_sha256") != quiz_hash:
        errors.append("quiz validation results do not match the current quiz statements")
    if quiz_metadata.get("questions") != len(quiz_statements.get("statements", [])):
        errors.append("quiz validation question count is stale")
    if quiz_metadata.get("algorithm") != "coverage-adjusted Manhattan distance":
        errors.append("quiz validation algorithm does not match the current contract")

    return errors


def main() -> int:
    if validate_traceability() != 0:
        return 1

    errors = collect_contract_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("PASS: committed output counts, coverage, and projections are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
