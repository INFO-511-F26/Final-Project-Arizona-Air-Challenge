from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from scripts.validate_submission import validate_submission


ROOT = Path(__file__).resolve().parents[1]


def test_student_release_manifest_contains_only_public_files() -> None:
    manifest = json.loads((ROOT / "data" / "release_manifest.json").read_text())
    assert set(manifest["files"]) == {"train.csv", "test.csv", "sample_submission.csv"}
    serialized = json.dumps(manifest).lower()
    assert all(term not in serialized for term in ["private", "solution", "salt", "mapping"])


def test_valid_submission() -> None:
    sample = pd.DataFrame({"row_id": ["row_a", "row_b"], "high_ozone": [0.1, 0.1]})
    submission = pd.DataFrame({"row_id": ["row_b", "row_a"], "high_ozone": [0.8, 0.2]})
    validate_submission(submission, sample)


@pytest.mark.parametrize(
    "submission",
    [
        pd.DataFrame({"row_id": ["row_a", "row_b"], "high_ozone": [0.2, 1.2]}),
        pd.DataFrame({"row_id": ["row_a", "row_a"], "high_ozone": [0.2, 0.3]}),
        pd.DataFrame({"row_id": ["row_a", "row_c"], "high_ozone": [0.2, 0.3]}),
    ],
)
def test_invalid_submission(submission: pd.DataFrame) -> None:
    sample = pd.DataFrame({"row_id": ["row_a", "row_b"], "high_ozone": [0.1, 0.1]})
    with pytest.raises(ValueError):
        validate_submission(submission, sample)
