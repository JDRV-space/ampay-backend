#!/usr/bin/env python3
"""Validate confirmed AMPAY records against committed vote IDs."""

import json
import sys
from pathlib import Path

from ampay_pipeline.parties import PARTY_NAME_TO_SLUG
from ampay_pipeline.paths import (
    OUTPUT_CONFIRMED_AMPAYS,
    OUTPUT_VOTES_BY_PARTY,
    OUTPUT_VOTES_CATEGORIZED,
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def build_vote_index(votes_data: dict) -> dict:
    return {vote["vote_id"]: vote for vote in votes_data["votes"]}


def collect_errors(ampays_data: dict, votes_index: dict, votes_by_party: dict) -> list[str]:
    errors: list[str] = []
    confirmed = ampays_data.get("ampays", [])

    if ampays_data.get("total_ampays_confirmed") != len(confirmed):
        errors.append(
            "total_ampays_confirmed does not match len(ampays): "
            f"{ampays_data.get('total_ampays_confirmed')} != {len(confirmed)}"
        )

    for ampay in confirmed:
        evidence = ampay.get("evidence", {})
        references = evidence.get("vote_references", [])
        party_slug = PARTY_NAME_TO_SLUG.get(ampay.get("party", ""))
        expected_vote = evidence.get("vote")

        if not party_slug:
            errors.append(f"{ampay['id']} has unknown party {ampay.get('party')}")
            continue

        if not references:
            errors.append(f"{ampay['id']} has no evidence.vote_references")
            continue

        for reference in references:
            vote_id = reference.get("vote_id")
            categorized_vote = votes_index.get(vote_id)
            party_vote = votes_by_party["votes"].get(vote_id)

            if not categorized_vote:
                errors.append(f"{ampay['id']} references missing categorized vote {vote_id}")
                continue

            if not party_vote:
                errors.append(f"{ampay['id']} references missing party vote {vote_id}")
                continue

            if categorized_vote.get("vote_type") != "sustantivo":
                errors.append(
                    f"{ampay['id']} references non-substantive vote "
                    f"{vote_id}: {categorized_vote.get('vote_type')}"
                )

            if reference.get("vote_type") != categorized_vote.get("vote_type"):
                errors.append(
                    f"{ampay['id']} reference vote_type disagrees for {vote_id}: "
                    f"{reference.get('vote_type')} != {categorized_vote.get('vote_type')}"
                )

            actual_position = party_vote["parties"][party_slug]["position"]
            if actual_position != reference.get("party_position"):
                errors.append(
                    f"{ampay['id']} reference party_position disagrees for {vote_id}: "
                    f"{reference.get('party_position')} != {actual_position}"
                )

            if actual_position != expected_vote:
                errors.append(
                    f"{ampay['id']} evidence vote disagrees for {vote_id}: "
                    f"{expected_vote} != {actual_position}"
                )

    removed = ampays_data.get("removed_ampays", {}).get("removed", [])
    removed_ampay_003 = [
        ampay for ampay in removed if ampay.get("original_id") == "AMPAY-003"
    ]

    if any(ampay.get("id") == "AMPAY-003" for ampay in confirmed):
        errors.append("AMPAY-003 is still present in confirmed ampays")

    if not removed_ampay_003:
        errors.append("AMPAY-003 is missing from removed_ampays")
    else:
        for reference in removed_ampay_003[0].get("vote_references", []):
            vote_id = reference.get("vote_id")
            categorized_vote = votes_index.get(vote_id)

            if not categorized_vote:
                errors.append(f"AMPAY-003 removal references missing vote {vote_id}")
                continue

            if categorized_vote.get("vote_type") == "sustantivo":
                errors.append(
                    f"AMPAY-003 removal references substantive vote {vote_id}; "
                    "expected procedural support for removal"
                )

    return errors


def main() -> int:
    ampays_data = load_json(OUTPUT_CONFIRMED_AMPAYS)
    votes_index = build_vote_index(load_json(OUTPUT_VOTES_CATEGORIZED))
    votes_by_party = load_json(OUTPUT_VOTES_BY_PARTY)

    errors = collect_errors(ampays_data, votes_index, votes_by_party)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "PASS: validated "
        f"{len(ampays_data['ampays'])} confirmed AMPAYs with vote references"
    )
    print("PASS: AMPAY-003 is removed because its referenced votes are procedural")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
