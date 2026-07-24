"""Canonical filesystem paths for committed AMPAY data inputs and outputs."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
INPUT_DIR = DATA_DIR / "01_input"
OUTPUT_DIR = DATA_DIR / "02_output"

PDF_INPUT_DIR = INPUT_DIR / "pdfs"
PDF_TEXT_INPUT_DIR = PDF_INPUT_DIR / "text"
PROMISE_INPUT_DIR = INPUT_DIR / "promises"
VOTE_INPUT_DIR = INPUT_DIR / "votes"
ANALYSIS_BY_PARTY_OUTPUT_DIR = OUTPUT_DIR / "analysis_by_party"

INPUT_PARTY_POSITIONS = VOTE_INPUT_DIR / "party_positions.json"
INPUT_VOTES_CATEGORIZED = VOTE_INPUT_DIR / "votes_categorized.json"

OUTPUT_AMPAYS = OUTPUT_DIR / "ampays.json"
OUTPUT_CONFIRMED_AMPAYS = OUTPUT_DIR / "AMPAY_CONFIRMED_2021.json"
OUTPUT_PARTY_PATTERNS = OUTPUT_DIR / "party_patterns.json"
OUTPUT_QUIZ_STATEMENTS = OUTPUT_DIR / "quiz_statements.json"
OUTPUT_QUIZ_VALIDATION_RESULTS = OUTPUT_DIR / "quiz_validation_results.json"
OUTPUT_VOTES_BY_PARTY = OUTPUT_DIR / "votes_by_party.json"
OUTPUT_VOTES_CATEGORIZED = OUTPUT_DIR / "votes_categorized.json"


def ensure_parent_dir(path: Path) -> None:
    """Create the parent directory for a file output path."""
    path.parent.mkdir(parents=True, exist_ok=True)
