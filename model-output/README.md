# Model Output

This directory contains forecast submissions for the **China COVID-19 Forecast Hub**. Each model has its own subdirectory containing CSV forecast files. The directory structure and file format follow the [hubverse model output standards](https://hubverse.io/en/latest/user-guide/model-output.html).

## Table of Contents

- [How to Submit](#how-to-submit)
- [Directory Structure](#directory-structure)
- [File Naming Convention](#file-naming-convention)
- [File Format](#file-format)
- [Column Specification](#column-specification)
- [Quantile Levels](#quantile-levels)
- [Complete Example](#complete-example)
- [Validation](#validation)
- [Weekly Schedule](#weekly-schedule)
- [Late Submission Policy](#late-submission-policy)

## How to Submit

1. Place your forecast CSV file in the appropriate `model-output/<team_abbr>-<model_abbr>/` subdirectory.
2. Open a **pull request** to the `main` branch of this repository.
3. Automated validation checks will run via [GitHub Actions](https://docs.github.com/en/actions) using the [hubValidations](https://github.com/hubverse-org/hubValidations) R package.
4. If all checks pass, the pull request will be reviewed and merged.

## Directory Structure

Each participating model must have a unique subdirectory:

```
model-output/
├── GZNL-ExponentialSmoothing/
│   ├── 2025-11-17-GZNL-ExponentialSmoothing.csv
│   └── 2026-03-16-GZNL-ExponentialSmoothing.csv
├── XMU_CTModelling-LSTM/
│   ├── 2025-10-06-XMU_CTModelling-LSTM.csv
│   └── 2026-03-23-XMU_CTModelling-LSTM.csv
├── MUST-SEIRS/
│   └── 2026-01-19-MUST-SEIRS.csv
└── ...
```

The subdirectory name must exactly match the `model_id` (i.e., `<team_abbr>-<model_abbr>`) used in the forecast file name and the model metadata file.

- `team_abbr`: Team abbreviation, ≤15 alphanumeric characters and underscores only
- `model_abbr`: Model abbreviation, ≤15 alphanumeric characters and underscores only

## File Naming Convention

Each forecast file must follow this naming pattern:

```
<reference_date>-<team_abbr>-<model_abbr>.csv
```

Where:
- `reference_date` is in `YYYY-MM-DD` format — the Saturday ending the epidemiological week of the submission
- `team_abbr` and `model_abbr` must match the subdirectory name

**Examples:**
- `2026-03-16-GZNL-SimpleTrend.csv`
- `2026-01-19-MUST-SEIRS.csv`
- `2025-10-06-XMU_CTModelling-LSTM.csv`

## File Format

Files must be comma-separated values (CSV) with the following **8 columns** (in any order). No additional columns are allowed.

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `reference_date` | Date (`YYYY-MM-DD`) | Saturday ending the epidemiological week; must match the date in the file name |
| 2 | `target` | String | Forecast target identifier |
| 3 | `horizon` | Integer | Number of weeks between `reference_date` and `target_end_date` |
| 4 | `target_end_date` | Date (`YYYY-MM-DD`) | Saturday ending the target epidemiological week |
| 5 | `location` | String | Geographic identifier |
| 6 | `output_type` | String | Type of model output representation |
| 7 | `output_type_id` | Numeric | Identifier for the output type (e.g., quantile level) |
| 8 | `value` | Numeric | The forecast value (non-negative) |

## Column Specification

### `reference_date`

The date from which all forecasts in the file are referenced. This is the **Saturday** at the end of the epidemiological week (Sunday–Saturday) containing the submission deadline. The `reference_date` must match the date in the file name.

Format: `YYYY-MM-DD`

### `target`

The forecast target. Currently, the only accepted value is:

| Value | Description |
|-------|-------------|
| `wk inc covid prop ili` | Weekly SARS-CoV-2 positivity rate among ILI cases from sentinel hospital surveillance |

### `horizon`

The number of **weeks** between the `reference_date` and the `target_end_date`. Valid values are integers from **-1 to 6**:

| Horizon | Meaning |
|---------|---------|
| -1 | Nowcast: the week before the reference week |
| 0 | Nowcast: the reference week itself |
| 1 | 1-week-ahead forecast |
| 2 | 2-week-ahead forecast |
| ... | ... |
| 6 | 6-week-ahead forecast |

Teams may submit any subset of these horizons.

### `target_end_date`

The **Saturday** ending the epidemiological week being forecast. Must satisfy:

```
target_end_date = reference_date + horizon × 7 days
```

Format: `YYYY-MM-DD`

Standard packages can convert between dates and epidemiological weeks:
- **R**: [MMWRweek](https://cran.r-project.org/web/packages/MMWRweek/), [lubridate](https://lubridate.tidyverse.org/reference/week.html)
- **Python**: [pymmwr](https://pypi.org/project/pymmwr/), [epiweeks](https://pypi.org/project/epiweeks/)

### `location`

The geographic unit of the forecast. Currently, only national-level forecasts are accepted:

| Value | Description |
|-------|-------------|
| `CN` | People's Republic of China (national level) |

### `output_type`

The type of model output representation. Currently accepted:

| Value | Description |
|-------|-------------|
| `quantile` | Quantile forecast — the inverse of the cumulative distribution function (CDF) at a given probability level |

### `output_type_id`

For quantile forecasts, this is the **probability level** of the quantile, expressed as a decimal between 0 and 1.

See [Quantile Levels](#quantile-levels) for the full list of required values.

### `value`

The forecast value — a **non-negative number** representing the predicted SARS-CoV-2 positivity rate.

**Important**: Values are in **percentage points** (0–100 scale), **not** proportions (0–1).

| Value | Interpretation |
|-------|---------------|
| `13.5` | 13.5% positivity rate |
| `2.3` | 2.3% positivity rate |

## Quantile Levels

Teams must provide all **23 required quantile levels** for each combination of `reference_date`, `horizon`, `target`, and `location`:

```
0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99
```

These quantile levels define the following prediction intervals:

| Interval | Lower Quantile | Upper Quantile |
|----------|---------------|----------------|
| 50% PI | 0.25 | 0.75 |
| 80% PI | 0.1 | 0.9 |
| 90% PI | 0.05 | 0.95 |
| 95% PI | 0.025 | 0.975 |
| 98% PI | 0.01 | 0.99 |

**Code references:**

```r
# R
quantiles <- c(0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35,
               0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
               0.85, 0.9, 0.95, 0.975, 0.99)
```

```python
# Python
quantiles = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35,
             0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
             0.85, 0.9, 0.95, 0.975, 0.99]
```

## Complete Example

Below is an example submission for reference date 2026-03-16 with horizons -1 and 0 (truncated for brevity; a real submission would include all 23 quantiles per horizon for all submitted horizons):

```csv
reference_date,target,horizon,target_end_date,location,output_type,output_type_id,value
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.01,1.8
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.025,1.9
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.05,2.0
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.1,2.1
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.15,2.2
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.2,2.3
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.25,2.4
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.3,2.4
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.35,2.5
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.4,2.5
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.45,2.6
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.5,2.6
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.55,2.7
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.6,2.7
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.65,2.8
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.7,2.8
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.75,2.9
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.8,3.0
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.85,3.1
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.9,3.2
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.95,3.4
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.975,3.6
2026-03-16,wk inc covid prop ili,-1,2026-03-09,CN,quantile,0.99,3.8
2026-03-16,wk inc covid prop ili,0,2026-03-16,CN,quantile,0.01,1.5
...
```

**Key points:**
- Each horizon requires all 23 quantile levels
- With all 8 horizons (-1 through 6): 8 × 23 = **184 rows** per submission
- All `value` entries are in percentage points (e.g., `2.6` = 2.6%)
- `target_end_date` must equal `reference_date + horizon × 7`

## Validation

### Automated Pull Request Validation

When a pull request is submitted, data is validated via [GitHub Actions](https://docs.github.com/en/actions) using the [hubValidations](https://github.com/hubverse-org/hubValidations) R package. The checks verify:

- File exists and is in an accepted format (CSV or Parquet)
- File name follows the naming convention
- File directory name matches the `model_id` in the file name
- `round_id` (reference date) is valid
- Submission is within the accepted time window
- All required task ID / output type / output type ID combinations are present
- Values are valid (non-negative, correct types)

### Local Validation (Optional)

You can validate your forecast locally before submitting a pull request:

1. Fork and clone the repository.
2. Place your forecast file in the appropriate `model-output/<model_id>/` directory.
3. Install the hubValidations R package:

```r
remotes::install_github("hubverse-org/hubValidations")
```

4. Run validation:

```r
hubValidations::validate_submission(
    hub_path = ".",
    file_path = "model-output/GZNL-SimpleTrend/2026-03-16-GZNL-SimpleTrend.csv"
)
```

If everything is correct, you should see output like:

```
✔ [file_exists]: File exists at path model-output/GZNL-SimpleTrend/2026-03-16-GZNL-SimpleTrend.csv.
✔ [file_name]: File name "2026-03-16-GZNL-SimpleTrend.csv" is valid.
✔ [file_location]: File directory name matches model_id metadata in file name.
✔ [round_id_valid]: round_id is valid.
✔ [file_format]: File is accepted hub format.
✔ [file_read]: File can be read successfully.
✔ [valid_vals]: value column values are valid.
✔ [req_vals]: Required task ID/output type/output type ID combinations are present.
```

## Weekly Schedule

| Day | Event |
|-----|-------|
| Monday – Wednesday | Forecast development period |
| **Wednesday 23:59 CST** | **Submission deadline** |
| Thursday 09:00 CST | Ensemble generation and evaluation |
| Saturday | Reference date (end of the epidemiological week) |

## Late Submission Policy

All forecasts must be submitted before **Wednesday 23:59 Beijing Time** each week. Late submissions are not accepted.

If you need to update a forecast after submission but before the deadline, submit a new pull request with the corrected file. Only the most recent valid submission before the deadline will be used.

## Support

- **Technical issues**: [GitHub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- **General inquiries**: yang_kaixin@gzlab.ac.cn
- **Dashboard**: [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)
