# Model outputs folder

This folder contains a set of subdirectories, one for each model, that contains submitted model output files for that model. The structure of these directories and their contents follows [the model output guidelines in our documentation](https://docs.hubverse.io/en/latest/user-guide/model-output.html). Documentation for China COVID-19 Forecast Hub submissions specifically is provided below. 

# Data submission instructions

All forecasts should be submitted directly to the [model-output/](./)
folder. Data in this directory should be added to the repository through
a pull request so that automatic data validation checks are run.

These instructions provide detail about the [data
format](#data-formatting) as well as [validation](#Forecast-validation) that
you can do prior to this pull request. In addition, we describe
[metadata](https://github.com/hubverse-org/hubTemplate/blob/master/model-metadata/README.md)
that each model should provide in the model-metadata folder.

*Table of Contents*

-   [What is a forecast](#What-is-a-forecast)
-   [Target data](#Target-data)
-   [Data formatting](#data-formatting)
-   [Forecast file format](#Forecast-file-format)
-   [Forecast data validation](#Forecast-validation)
-   [Weekly ensemble build](#Weekly-ensemble-build)
-   [Policy on late submissions](#policy-on-late-or-updated-submissions)

## What is a forecast 

Models are asked to make specific quantitative forecasts about data that
will be observed in the future. These forecasts are interpreted as
"unconditional" predictions about the future. That is, they are not
predictions only for a limited set of possible future scenarios in which
a certain set of conditions (e.g. vaccination uptake is strong, or new
social-distancing mandates are put in place) hold about the future --
rather, they should characterize uncertainty across all reasonable
future scenarios. In practice, all forecasting models make some
assumptions about how current trends in data may change and impact the
forecasted outcome; some teams select a "most likely" scenario or
combine predictions across multiple scenarios that may occur. Forecasts
submitted to this repository will be evaluated against observed data.

We note that other modeling efforts, such as the [Influenza Scenario
Modeling Hub](https://fluscenariomodelinghub.org/), have been
launched to collect and aggregate model outputs from "scenario
projection" models. These models create longer-term projections under a
specific set of assumptions about how the main drivers of the pandemic
(such as non-pharmaceutical intervention compliance, or vaccination
uptake) may change over time.

## Target Data 

The target data for this hub is the **weekly SARS-CoV-2 positivity rate among influenza-like illness (ILI) cases** from China's sentinel hospital surveillance network. This data is collected and reported by the China CDC through their weekly acute respiratory syndrome surveillance reports. Historical target data can be obtained using the [China CDC Crawl Repository](https://github.com/dailypartita/cn_cdc_crawl), which provides automated tools for downloading and processing China CDC surveillance reports. 


## Data formatting 

The automatic checks in place for forecast files submitted to this
repository validates both the filename and file contents to ensure the
file can be used in the visualization and ensemble forecasting.

### Subdirectory

Each model that submits forecasts for this project will have a unique subdirectory within the [model-output/](model-output/) directory in this GitHub repository where forecasts will be submitted. Each subdirectory must be named

    team-model

where

-   `team` is the team name and
-   `model` is the name of your model.

Both team and model should be less than 15 characters and not include
hyphens or other special characters, with the exception of "\_".

The combination of `team` and `model` should be unique from any other model in the project.


### Metadata

The metadata file will be saved within the model-metdata directory in the Hub's GitHub repository, and should have the following naming convention:


      team-model.yml

Details on the content and formatting of metadata files are provided in the [model-metadata README](https://github.com/hubverse-org/hubTemplate/blob/master/model-metadata/README.md).




### Forecasts

Each forecast file should have the following
format

    YYYY-MM-DD-team-model.csv

where

-   `YYYY` is the 4 digit year,
-   `MM` is the 2 digit month,
-   `DD` is the 2 digit day,
-   `team` is the team name, and
-   `model` is the name of your model.

The date YYYY-MM-DD is the [`reference_date`](#reference_date). This should be the Saturday following the submission date.

The `team` and `model` in this file must match the `team` and `model` in
the directory this file is in. Both `team` and `model` should be less
than 15 characters, alpha-numeric and underscores only, with no spaces
or hyphens. 

## Forecast file format 

The file must be a comma-separated value (csv) file with the following
columns (in any order):

-   `reference_date`
-   `target`
-   `horizon`
-   `target_end_date`
-   `location`
-   `output_type`
-   `output_type_id`
-   `value`

No additional columns are allowed.

The value in each row of the file is a quantile for a particular combination of location, date, and horizon. 

### `reference_date` 

Values in the `reference_date` column must be a date in the ISO format

    YYYY-MM-DD

This is the date from which all forecasts should be considered. This date is the Saturday following the submission Due Date, corresponding to the last day of the epiweek when submissions are made. The `reference_date` should be the same as the date in the filename but is included here to facilitate validation and analysis. 

### `target`

Values in the `target` column must be a character (string) and be the following specific target:

-   **`wk inc covid prop ili`** - Weekly incident COVID-19 proportion in influenza-like illness


### `horizon`
Values in the `horizon` column indicate the number of **weeks** between the `reference_date` and the `target_end_date`. This should be a number between **-3 and 6**, where for example a `horizon` of 0 indicates that the prediction is a nowcast for the **week** of submission, a `horizon` of 1 indicates a forecast for the **week** after submission, and a `horizon` of -1 indicates a nowcast for the **week** before submission (retrospective analysis). 

### `target_end_date`

Values in the `target_end_date` column must be a date in the format

    YYYY-MM-DD
    
This is the last date of the forecast target's **epidemiological week**. This will be the date of the Saturday at the end of the forecasted **week**. Within each row of the submission file, the `target_end_date` should be equal to the `reference_date` + `horizon` * (**7** days).


### `location`

Values in the `location` column must be **"CN"**, representing China as a whole. This hub focuses on national-level forecasting for China's overall SARS-CoV-2 positivity rates from the sentinel hospital network. 

### `output_type`

Values in the `output_type` column must be **"quantile"**.

This hub exclusively collects quantile forecasts for the SARS-CoV-2 positivity rate target, which allows for proper evaluation of prediction intervals and forecast uncertainty. 

### `output_type_id`
Values in the `output_type_id` column specify identifying information for the output type.

#### quantile output

When the predictions are quantiles, values in the `output_type_id` column are a quantile probability level in the format

    0.###

This value indicates the quantile probability level for the `value` in this row.

Teams must provide the following **23 quantiles**:

**Required quantiles**: 0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99

**R code for defining quantiles:**
```r
quantiles <- c(0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99)
```

**Python code for defining quantiles:**
```python
quantiles = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99]
```


### `value`

Values in the `value` column are non-negative numbers indicating the **quantile** prediction for this row. For a "quantile" prediction, `value` is the inverse of the cumulative distribution function (CDF) for the target, location, and quantile associated with that row. For example, the 2.5% and 97.5% quantiles for a given target and location should capture 95% of the predicted values and correspond to the central 95% Prediction Interval.

**Important**: Values represent **percentages** (0-100), not proportions (0-1). For example, a value of 15.3 represents 15.3% SARS-CoV-2 positivity rate. 

### Example tables

Here's an example of a forecast submission for the 2025-08-21 reference date:

| reference_date | target | horizon | target_end_date | location | output_type | output_type_id | value |
|----------------|--------|---------|----------------|----------|-------------|----------------|-------|
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.01 | 8.2 |
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.025 | 8.5 |
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.05 | 9.1 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.5 | 13.5 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.975 | 18.7 |
| 2025-08-21 | wk inc covid prop ili | -3 | 2025-07-31 | CN | quantile | 0.99 | 19.3 |
| 2025-08-21 | wk inc covid prop ili | 0 | 2025-08-21 | CN | quantile | 0.01 | 7.8 |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Key points:**
- Each horizon (-3 to 6) requires all 23 quantiles
- Total rows per submission: 10 horizons × 23 quantiles = 230 rows
- Values represent percentage points (e.g., 13.5 = 13.5%)

## Forecast validation 

To ensure proper data formatting, pull requests for new data in
`model-output/` will be automatically run. Optionally, you may also run these validations locally.

### Pull request forecast validation

When a pull request is submitted, the data are validated through [Github Actions](https://docs.github.com/en/actions) which runs the tests present in [the hubValidations package](https://github.com/hubverse-org/hubValidations). The intent for these tests are to validate the requirements above. Please [let us know](https://github.com/dailypartita/China_COVID-19_Forecast_Hub/issues) if you are facing issues while running the tests.

### Local forecast validation

Optionally, you may validate a forecast file locally before submitting it to the hub in a pull request. Note that this is not required, since the validations will also run on the pull request. To run the validations locally, follow these steps:

1. Create a fork of the `China_COVID-19_Forecast_Hub` repository and then clone the fork to your computer.
2. Create a draft of the forecast file for your model and place it in the appropriate `model-output/team-model/` folder.
3. Install the hubValidations package for R by running the following command from within an R session:
``` r
remotes::install_github("hubverse-org/hubValidations")
```
4. Validate your draft forecast file by running the following command in an R session:
``` r
hubValidations::validate_submission(
    hub_path="<path to your clone of the hub repository>",
    file_path="<relative path to your submission file>")
```

For example, if your working directory is the root of the hub repository:
``` r
hubValidations::validate_submission(
    hub_path=".", 
    file_path="model-output/GZNL-test_001/2025-08-21-GZNL-test_001.csv")
```


## Weekly ensemble build 

Every **Thursday at 09:00 Beijing Time**, we will generate a **China COVID-19 Forecast Hub** ensemble for **weekly SARS-CoV-2 positivity rate** using valid forecast submissions in the current week by the **Wednesday 23:59 Beijing Time** deadline. Some or all participant forecasts may be combined into an ensemble forecast to be published in real-time along with the participant forecasts. In addition, some or all forecasts may be displayed alongside the output of a baseline model for comparison.


## Policy on late or updated submissions 

In order to ensure that forecasting is done in real-time, all forecasts are required to be submitted to this repository by **Wednesday 23:59 Beijing Time** each week. We do not accept late forecasts.

**Weekly submission timeline:**
- **Monday-Wednesday**: Forecast development period
- **Wednesday 23:59 Beijing Time**: Submission deadline
- **Thursday 09:00 Beijing Time**: Ensemble generation and evaluation
- **Saturday**: Reference date (end of epidemiological week)

**Updated submissions:** If you need to update a forecast after submission but before the deadline, you may submit a new pull request with the corrected file. Only the most recent valid submission before the deadline will be used.

## Evaluation criteria

Forecasts will be evaluated using a variety of metrics, including:

### Primary Metrics
- **WIS (Weighted Interval Score)**: Comprehensive measure of probabilistic forecast accuracy
- **MAE (Mean Absolute Error)**: Accuracy of point forecasts (using median/0.5 quantile)
- **Interval Coverage**: Percentage of observations falling within prediction intervals (50%, 95%)

### Relative Metrics
- **Relative WIS**: WIS relative to a baseline model (GZNL-test_001)
- **Relative MAE**: MAE relative to a baseline model

### Evaluation Schedule
- **Real-time evaluation**: Conducted when new surveillance data becomes available
- **Retrospective analysis**: Periodic evaluation of historical forecast performance
- **Dashboard updates**: Results published on the [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)

### Evaluation Data Source
Evaluation will be conducted using official surveillance data from China CDC's sentinel hospital network, obtained through the automated data collection system at [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl).

## Data Sources for Model Development

Teams are encouraged to use the following data sources for model development:

1. **Historical surveillance data**: Available through [China CDC Crawl Repository](https://github.com/dailypartita/cn_cdc_crawl)
2. **Weather data**: Available from Chinese meteorological services
3. **Mobility data**: Available from various sources (with appropriate permissions)
4. **Vaccination data**: Available from official health authorities
5. **Social media indicators**: Available through appropriate APIs and permissions

**Important**: Please ensure compliance with all relevant data use agreements and privacy regulations when using external data sources.

## Support and Contact

- **Technical questions**: Create an issue on [GitHub Issues](https://github.com/dailypartita/China_COVID-19_Forecast_Hub/issues)
- **General inquiries**: Contact Yang Kaixin (yang_kaixin@gzlab.ac.cn)
- **Dashboard access**: [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)
