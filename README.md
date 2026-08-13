# INFO 511 — Arizona Air Challenge

Student workspace for **When Does Desert Air Become Unhealthy?**, a semester-spanning INFO 511 data project with a private Kaggle classification component.

Your competition task is to estimate the probability that an Arizona ozone-monitoring site-day had a daily maximum 8-hour ozone concentration strictly greater than 70 parts per billion. The target is called `high_ozone`. This is a retrospective classification task using same-day weather—not a forecast of a future day.

An individual `high_ozone = 1` row must not be described as an EPA regulatory violation. Formal regulatory determinations use multi-year design values rather than a single daily reading.

## Where work happens

- **Kaggle is authoritative for competition data, computing, and submissions.** Join the private competition, attach its data to a Kaggle notebook, and submit probability files there.
- **GitHub is your versioned project workspace.** Keep your notebook, code, written analysis, environment notes, and reproducibility record here.

Do not commit Kaggle CSVs or submission files. The `.gitignore` excludes them by default.

## Fastest start: Kaggle

1. Join the private INFO 511 competition and accept its rules.
2. Open the competition's **Code** tab and create or import a notebook.
3. Upload `notebooks/01_starter_baseline.ipynb` or import it from this GitHub repository.
4. In the notebook, choose **Add Input** and attach the Arizona Air Challenge competition data.
5. Select a standard **CPU** session. A GPU is unnecessary.
6. Leave internet access off; the starter uses packages already available in Kaggle.
7. Choose **Run All**.
8. Download `/kaggle/working/submission.csv` from the notebook output and submit it to the competition.
9. Record the notebook version, validation score, Kaggle score, model, and changes in your project log.

The starter automatically finds the attached competition files under `/kaggle/input`. It performs a future-time validation using 2021–2022 for fitting and 2023 for validation, then refits on all 2021–2023 training rows and predicts the 2024–2025 test rows.

## Local alternative

Requires Python 3.11 or later:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Download `train.csv`, `test.csv`, and `sample_submission.csv` from Kaggle into `data/`, then open the starter notebook. Generated submissions belong in `submissions/`.

The public row counts and SHA-256 hashes in `data/release_manifest.json` can be used to confirm that local downloads match the frozen Kaggle release.

Validate a submission before uploading:

```bash
python scripts/validate_submission.py submissions/submission.csv
```

## Required submission format

Your CSV must contain all 30,728 test rows in exactly two columns:

```text
row_id,high_ozone
row_0123456789abcdef,0.031
row_fedcba9876543210,0.742
```

`high_ozone` must contain finite probabilities from 0 through 1. Do not alter `row_id`.

## Evaluation

The Kaggle leaderboard uses ROC-AUC. A constant prediction scores 0.5. Because the positive class is rare, accuracy can be misleading and is not the leaderboard metric.

Your course analysis must go beyond ROC-AUC. Report and interpret average precision, balanced accuracy, precision, recall, F1, a confusion matrix at a justified threshold, and calibration where appropriate. Explain how model errors and threshold choices affect interpretation.

## Repository contents

```text
arizona-air-challenge-student/
├── README.md
├── data/                         # local Kaggle downloads; CSVs ignored
├── docs/
│   ├── competition_rules.md
│   ├── data_dictionary.md
│   └── project_checklist.md
├── notebooks/
│   └── 01_starter_baseline.ipynb
├── scripts/
│   └── validate_submission.py
├── submissions/                  # generated predictions; CSVs ignored
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Academic integrity and data limitations

Do not retrieve labels from EPA/AQS or another external source, reverse pseudonymous identifiers, or use instructor-only files. External data are prohibited unless the instructor announces an exception for the entire class.

The monitor network is geographically uneven and does not measure personal exposure. Weather may come from another AQS monitor within 50 km. Results describe monitored site-days in this dataset, not every person or location in Arizona. Read [the competition rules](docs/competition_rules.md) and [data dictionary](docs/data_dictionary.md) before modeling.
