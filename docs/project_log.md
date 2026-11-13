# Arizona Air Challenge — Project Log

This document tracks the development of the Arizona Air Challenge classification model, including exploratory data analysis, preprocessing decisions, model experiments, validation results, and changes made throughout the project.

The goal is to maintain a record of what was changed, why the change was made, how it affected model performance, and what was learned from the results.

---

## 1. Initial Baseline

**Code:** 01_starter_baseline.ipynb 
**Submission:** submission.csv 

The initial submission established a baseline model and provided a starting point for evaluating future improvements.

### Initial results

| Metric | Result |
|---|---:|
| Kaggle score | 0.87281 |
| Validation ROC-AUC | 0.9109 |
| Average precision | 0.1727 |
| Balanced accuracy (threshold = 0.5) | 0.8471 |
| Precision (threshold = 0.5) | 0.1191 |
| Recall (threshold = 0.5) | 0.8768 |
| F1-score (threshold = 0.5) | 0.2098 |
| Validation prevalence | 0.0274 |

### Initial observations

- The validation ROC-AUC was 0.9109, providing a baseline for comparing future models.
- The validation prevalence was 2.74%, indicating that high-ozone observations were relatively uncommon.
- Recall was relatively high (0.8768), while precision was low (0.1191) at the 0.5 classification threshold.
- The difference between precision and recall suggests that the model identifies many high-ozone observations but also produces a substantial number of false positives.

### Initial decisions

- Use the initial submission as the baseline for future model comparisons.
- Complete EDA before making additional preprocessing or modeling changes.
- Investigate missingness, class imbalance, and relationships between predictors and high-ozone observations.

---

## 2. Exploratory Data Analysis (EDA))

**Code:** 02_EDA.py
**Submission:** N/A

**Dataset Overview**
- Training dataset contains **46,737 rows and 17 columns**.
- Missing values were found in six weather measurement columns:
  - `temperature_mean`, `temperature_max`
  - `wind_speed_mean`, `wind_speed_max`
  - `relative_humidity_mean`, `relative_humidity_max`
- Three binary missingness indicators are provided:
  - `temperature_missing`
  - `wind_speed_missing`
  - `relative_humidity_missing`
- Correlations between the weather-family missingness indicators were approximately 0.30, suggesting a weak-to-moderate tendency for weather measurements to be unavailable together.

**High-Ozone Distribution**
- Overall high-ozone prevalence is approximately **3.00%**, indicating a significant class imbalance.
- High-ozone prevalence by month follows an approximately bell-shaped distribution, with the highest prevalence around July.
- Summer has substantially higher high-ozone prevalence than the other seasons.
- The Central region has the highest prevalence, followed by the Eastern region, with the remaining regions considerably lower.
- Weather measurements show different relationships with high-ozone prevalence:
  - Temperature and wind speed show more noticeable changes across high- and low-ozone observations.
  - Relative humidity shows a weaker relationship.

**High-Ozone Patterns Over Time**
- Annual high-ozone prevalence was highest in 2021 and lowest in 2022.
- Monthly trends show a clear seasonal pattern, with high-ozone prevalence peaking during summer.
- A smaller increase was also observed around December 2021 and January 2022.
- When comparing weather measurements with high-ozone prevalence over time:
  - Temperature and high-ozone prevalence appear to increase together.
  - Wind speed may increase slightly before some months with higher high-ozone prevalence.
  - Relative humidity may increase following months with higher high-ozone prevalence.
- These patterns are exploratory observations and do not establish causal relationships.

**Geographical Variables: Site, Region, and County**
- Examined three geographical variables: `site_code`, `region`, and `county_name`.
- No missing values were found in these columns.
- The dataset contains:
  - **46 unique monitoring sites**
  - **5 geographic regions**
  - **10 counties**
- Most monitoring sites had relatively consistent record counts, although a handful had substantially fewer observations.
- `site_66e710a6` had the highest high-ozone prevalence by far, but had a relatively low record count of 688. This should be interpreted cautiously because a smaller sample can produce less stable prevalence estimates.
- Maricopa County had both the highest record count and the highest high-ozone prevalence among counties.
- Geographic variables may provide useful predictive information, particularly at the county and monitoring-site levels.

**Combined Seasonal and Regional Patterns**
- The Central region during summer has the highest observed high-ozone prevalence.
- This suggests that interactions between geographic region and season may be useful features to investigate during feature engineering and model development.

**Correlations and Multicollinearity**
- Temperature has the strongest correlation with `high_ozone`, approximately 0.19. This is a relatively weak positive relationship.
- Some correlations exist between weather measurements and month, including relative humidity and month (approximately 0.26) and temperature and month (approximately -0.39).
- The strongest correlations overall occur between average and maximum measurements within the same weather family (e.g., `temperature_mean` and `temperature_max`).
- The multicollinearity analysis did not reveal any unexpected relationships or major concerns beyond the expected correlations between related weather measurements.

**Initial EDA Takeaways**
- **Class imbalance**: High-ozone observations account for only approximately 3% of the training dataset, making class imbalance an important consideration during model evaluation and development.
- **Seasonality**: Month and season appear to be important predictors, with high-ozone prevalence peaking during summer.
- **Geographic variation**: Region, county, and monitoring site show differences in high-ozone prevalence and may capture meaningful geographic patterns.
- **Weather relationships**: Temperature shows the strongest relationship with high-ozone observations, although the overall correlation is relatively weak. Other weather measurements may also contribute useful information.
- **Nonlinear patterns**: Relationships between weather measurements and high-ozone prevalence may not be entirely linear, suggesting that nonlinear effects and feature transformations may be worth exploring.
- **Feature interactions**: Seasonal and geographic interactions, particularly observations from the Central region during summer, are worth investigating.
- **Site-level variability**: Differences in prevalence across monitoring sites should be evaluated carefully, particularly for sites with relatively few observations.