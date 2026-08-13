# Project checklist

Use this checklist throughout the project rather than only during the leaderboard week.

## Data and provenance

- [ ] I can state the observational unit and target definition precisely.
- [ ] I inspected column types, ranges, missingness, duplicates, and class prevalence.
- [ ] I documented the EPA/AQS origin and the limits of monitor-based measurements.
- [ ] I did not use external labels, reverse identifiers, or access instructor-only data.

## Validation

- [ ] My main validation respects time order.
- [ ] Preprocessing is fitted only on each training fold, using a pipeline where appropriate.
- [ ] I recorded random seeds and did not tune solely against the Kaggle public leaderboard.
- [ ] I compared my model with a constant or simple interpretable baseline.

## Modeling and evaluation

- [ ] I submit probabilities rather than hard labels.
- [ ] I report ROC-AUC and average precision.
- [ ] I justify any classification threshold and report precision, recall, F1, balanced accuracy, and a confusion matrix.
- [ ] I examine calibration and meaningful error subgroups.
- [ ] I distinguish association from causation and retrospective classification from forecasting.

## Communication and reproducibility

- [ ] A new reader can reproduce my final result from this repository and the Kaggle data.
- [ ] I recorded package versions, notebook version, and the final submission filename.
- [ ] I explain geographic coverage, missing weather, class imbalance, and public-data leakage risk.
- [ ] I do not describe a single high-ozone row as an EPA regulatory violation.
- [ ] My conclusions are supported by evidence and do not overgeneralize beyond monitored site-days.
