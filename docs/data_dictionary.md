# Data dictionary

Each row represents one Arizona ozone-monitoring **site-day**. Exact dates, coordinates, AQS identifiers, ozone measurements, AQI, and weather-source identifiers are withheld from the student release.

## Files

- `train.csv`: 46,737 rows from 2021–2023, including `high_ozone`.
- `test.csv`: 30,728 future rows from 2024–2025, excluding the target.
- `sample_submission.csv`: required test identifiers and an example probability column.

## Columns

| Column | Description |
|---|---|
| `row_id` | Unique pseudonymous submission key; do not use it as a numeric predictor |
| `site_code` | Pseudonymous monitoring-site category |
| `year_index` | 0 for 2021 through 4 for 2025 |
| `month` | Month number, 1–12 |
| `season` | Winter, spring, summer, or fall |
| `region` | Broad Arizona teaching region |
| `county_name` | County containing the ozone-monitoring site |
| `temperature_mean`, `temperature_max` | Daily temperature in degrees Fahrenheit from the nearest eligible AQS monitor within 50 km |
| `wind_speed_mean`, `wind_speed_max` | Daily resultant wind speed in knots within 50 km |
| `relative_humidity_mean`, `relative_humidity_max` | Daily relative humidity in percent within 50 km |
| `temperature_missing`, `wind_speed_missing`, `relative_humidity_missing` | 1 when that weather family is unavailable; otherwise 0 |
| `high_ozone` | Training target: 1 when daily maximum 8-hour ozone is strictly greater than 70 ppb |

Missing numeric weather values are intentional. Choose and document an imputation or missing-value strategy. Do not delete every incomplete row without evaluating the consequences.

## Interpretation limits

- The label is a course threshold, not a regulatory-violation determination.
- Site-days repeat within monitoring sites and across time; rows are not independent people.
- Monitor coverage is geographically uneven.
- Weather can come from a nearby rather than co-located AQS monitor.
- Same-day weather supports retrospective explanation, not operational forecasting.
