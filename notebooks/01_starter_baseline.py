# %% [markdown]
# # INFO 511 Arizona Air Challenge — starter baseline
#
# This notebook runs on a standard Kaggle CPU session without internet access or
# additional installations. It also runs locally after the three competition CSVs
# are placed in `data/`.
#
# The goal is to establish a reproducible baseline, not to maximize the leaderboard.
# Improve it only after you understand the data, validation design, and error tradeoffs.

# %%
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 511
TARGET = "high_ozone"
ID_COLUMN = "row_id"

print("pandas", pd.__version__)
print("scikit-learn", sklearn.__version__)

# %% [markdown]
# ## 1. Find and load the competition data
#
# On Kaggle, attach the competition data with **Add Input**. Locally, place the
# files in this repository's `data/` directory. The environment-variable option
# is mainly for automated testing.

# %%
def find_data_directory() -> Path:
    explicit = os.environ.get("ARIZONA_AIR_DATA_DIR")
    search_roots = [Path(explicit)] if explicit else []
    search_roots.extend([Path("/kaggle/input"), Path("data"), Path("../data")])
    expected = {"train.csv", "test.csv", "sample_submission.csv"}
    required_train_columns = {ID_COLUMN, TARGET, "site_code", "year_index", "month"}

    for root in search_roots:
        if not root.exists():
            continue
        candidates = [root] if expected.issubset({path.name for path in root.glob("*.csv")}) else []
        candidates.extend(path.parent for path in root.rglob("train.csv"))
        for candidate in candidates:
            if not all((candidate / name).exists() for name in expected):
                continue
            columns = set(pd.read_csv(candidate / "train.csv", nrows=2).columns)
            if required_train_columns.issubset(columns):
                return candidate
    raise FileNotFoundError(
        "Competition data not found. On Kaggle, use Add Input to attach the Arizona Air "
        "Challenge data. Locally, put train.csv, test.csv, and sample_submission.csv in data/."
    )


DATA_DIRECTORY = find_data_directory()
train = pd.read_csv(DATA_DIRECTORY / "train.csv")
test = pd.read_csv(DATA_DIRECTORY / "test.csv")
sample_submission = pd.read_csv(DATA_DIRECTORY / "sample_submission.csv")

print("Data directory:", DATA_DIRECTORY)
print("Train shape:", train.shape)
print("Test shape:", test.shape)
train.head()

# %% [markdown]
# ## 2. Verify the release before modeling

# %%
assert TARGET in train.columns and TARGET not in test.columns
assert list(train.drop(columns=TARGET).columns) == list(test.columns)
assert train[ID_COLUMN].is_unique and test[ID_COLUMN].is_unique
assert not set(train[ID_COLUMN]).intersection(test[ID_COLUMN])
assert test[ID_COLUMN].tolist() == sample_submission[ID_COLUMN].tolist()
assert set(train[TARGET].unique()).issubset({0, 1})

summary = pd.DataFrame({
    "dtype": train.dtypes.astype(str),
    "missing_count": train.isna().sum(),
    "missing_percent": train.isna().mean().mul(100).round(2),
    "unique_values": train.nunique(),
})
summary

# %%
class_counts = train[TARGET].value_counts().sort_index()
print(class_counts)
print(f"Positive prevalence: {train[TARGET].mean():.3%}")
print("Prevalence by training year index:")
print(train.groupby("year_index")[TARGET].agg(["size", "sum", "mean"]))

# %% [markdown]
# ## 3. Build leak-safe model features
#
# `row_id` is only a submission key. We encode month cyclically so December and
# January are close. All imputation and encoding live inside the pipeline and are
# fitted only on training data.

# %%
def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["month_sin"] = np.sin(2 * np.pi * result["month"] / 12)
    result["month_cos"] = np.cos(2 * np.pi * result["month"] / 12)
    return result


numeric_features = [
    "year_index",
    "month_sin",
    "month_cos",
    "temperature_mean",
    "temperature_max",
    "temperature_missing",
    "wind_speed_mean",
    "wind_speed_max",
    "wind_speed_missing",
    "relative_humidity_mean",
    "relative_humidity_max",
    "relative_humidity_missing",
]
categorical_features = ["site_code", "season", "region", "county_name"]

numeric_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="median", add_indicator=True)),
    ("scale", StandardScaler()),
])
categorical_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])
preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])


def make_model() -> Pipeline:
    return Pipeline([
        ("prepare", preprocessor),
        ("model", LogisticRegression(
            class_weight="balanced",
            max_iter=2_000,
            random_state=SEED,
        )),
    ])


train_features = add_features(train)
test_features = add_features(test)

# %% [markdown]
# ## 4. Use future-time validation
#
# Fit on 2021–2022 (`year_index` 0–1) and validate on 2023 (`year_index` 2).
# This is more realistic than a random row split because the competition test
# rows come from later years. Do not tune against the Kaggle public leaderboard.

# %%
fit_mask = train_features["year_index"] <= 1
validation_mask = train_features["year_index"] == 2

model = make_model()
model.fit(train_features.loc[fit_mask], train.loc[fit_mask, TARGET])
validation_probability = model.predict_proba(train_features.loc[validation_mask])[:, 1]
validation_actual = train.loc[validation_mask, TARGET]

threshold = 0.5
validation_prediction = (validation_probability >= threshold).astype(int)
metrics = pd.Series({
    "roc_auc": roc_auc_score(validation_actual, validation_probability),
    "average_precision": average_precision_score(validation_actual, validation_probability),
    "balanced_accuracy_at_0.5": balanced_accuracy_score(validation_actual, validation_prediction),
    "precision_at_0.5": precision_score(validation_actual, validation_prediction, zero_division=0),
    "recall_at_0.5": recall_score(validation_actual, validation_prediction, zero_division=0),
    "f1_at_0.5": f1_score(validation_actual, validation_prediction, zero_division=0),
    "validation_prevalence": validation_actual.mean(),
})
print(metrics.round(4))
print("Confusion matrix [[TN, FP], [FN, TP]]:")
print(confusion_matrix(validation_actual, validation_prediction, labels=[0, 1]))

# %% [markdown]
# A threshold of 0.5 is shown for illustration; ROC-AUC itself does not use a
# fixed threshold. Choose a threshold based on an explicit purpose and explain
# the precision/recall tradeoff rather than treating 0.5 as automatically correct.

# %% [markdown]
# ## 5. Refit on all training rows and create a Kaggle submission

# %%
final_model = make_model()
final_model.fit(train_features, train[TARGET])
test_probability = final_model.predict_proba(test_features)[:, 1]

submission = sample_submission[[ID_COLUMN]].copy()
submission[TARGET] = test_probability

assert list(submission.columns) == [ID_COLUMN, TARGET]
assert len(submission) == len(test) == 30_728
assert submission[ID_COLUMN].is_unique
assert submission[ID_COLUMN].tolist() == sample_submission[ID_COLUMN].tolist()
assert np.isfinite(submission[TARGET]).all()
assert submission[TARGET].between(0, 1).all()

if Path("/kaggle/working").exists():
    output_path = Path("/kaggle/working/submission.csv")
else:
    working_directory = Path.cwd()
    repository_root = (
        working_directory
        if (working_directory / "README.md").exists()
        else working_directory.parent
        if (working_directory.parent / "README.md").exists()
        else working_directory
    )
    output_directory = repository_root / "submissions"
    output_directory.mkdir(exist_ok=True)
    output_path = output_directory / "submission.csv"

submission.to_csv(output_path, index=False)
print(f"Saved {len(submission):,} predictions to {output_path}")
submission.head()

# %% [markdown]
# ## 6. Before your next model
#
# 1. Record this validation score and submission filename.
# 2. Inspect errors by month, region, county, and available weather—not only one metric.
# 3. Compare at least one other validation design and explain why the result changes.
# 4. Change one modeling decision at a time and keep a log.
# 5. Consider calibration and threshold tradeoffs for the rare positive class.
# 6. Keep the final result reproducible in GitHub.
#
# A small leaderboard improvement is not automatically better science. Your final
# work is evaluated on reasoning, validation, interpretation, ethics, and communication
# as well as predictive performance.
