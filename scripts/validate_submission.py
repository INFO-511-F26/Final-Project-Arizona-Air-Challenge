#!/usr/bin/env python3
"""Validate submission shape and probabilities without access to hidden labels."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ID_COLUMN = "row_id"
TARGET = "high_ozone"


def validate_submission(submission: pd.DataFrame, sample: pd.DataFrame) -> None:
    if list(submission.columns) != [ID_COLUMN, TARGET]:
        raise ValueError(f"Columns must be exactly: {ID_COLUMN}, {TARGET}")
    if len(submission) != len(sample):
        raise ValueError(f"Submission must contain {len(sample):,} rows")
    if submission[ID_COLUMN].duplicated().any():
        raise ValueError("row_id values must be unique")
    if set(submission[ID_COLUMN]) != set(sample[ID_COLUMN]):
        raise ValueError("row_id values must exactly match sample_submission.csv")
    prediction = pd.to_numeric(submission[TARGET], errors="coerce")
    if prediction.isna().any() or not np.isfinite(prediction).all():
        raise ValueError("high_ozone predictions must all be finite numbers")
    if not prediction.between(0, 1).all():
        raise ValueError("high_ozone predictions must be between 0 and 1")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    parser.add_argument("--sample", type=Path, default=Path("data/sample_submission.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_submission(pd.read_csv(args.submission), pd.read_csv(args.sample))
    print(f"Valid submission: {args.submission} ({sum(1 for _ in open(args.submission)) - 1:,} rows)")


if __name__ == "__main__":
    main()
