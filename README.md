# China COVID-19 Forecast Hub

This collaborative forecasting hub collects and evaluates real-time probabilistic forecasts of the weekly SARS-CoV-2 positivity rate among influenza-like illness (ILI) cases from sentinel hospitals across China. The hub provides a platform for comparing forecasting models and generating evidence-based insights for public health decision-making. It follows the standards and guidelines outlined by the [hubverse](https://hubverse.io), which provides a set of data formats and open-source tools for modeling hubs.

For questions about data sources or attribution, contact yang_kaixin@gzlab.ac.cn.

## Repository Structure

```
China-COVID-19-Forecast-Hub/
├── hub-config/                 # Hub configuration files
│   ├── admin.json              # Administrative settings
│   ├── tasks.json              # Modeling task definitions
│   └── model-metadata-schema.json  # Schema for model metadata
├── model-metadata/             # Model metadata (one YAML per model)
├── model-output/               # Forecast submissions (one folder per model)
├── target-data/                # Ground truth / target data
│   ├── time-series.csv         # Weekly SARS-CoV-2 positivity time series
│   └── oracle-output.csv       # Oracle output for evaluation
└── .github/workflows/          # CI/CD for automated validation
```

## Forecast Target

Participating teams submit forecasts for the following target at the national level (China):

| Target ID | Description | Units |
|-----------|-------------|-------|
| `wk inc covid prop ili` | Weekly SARS-CoV-2 positivity rate among ILI cases from sentinel hospital surveillance | Percentage (0–100) |

Values represent **percentages** (e.g., `13.5` means 13.5%), **not** proportions (0–1).

## Submission Timeline

| Event | Timing |
|-------|--------|
| Forecast development | Monday – Wednesday |
| **Submission deadline** | **Wednesday 23:59 Beijing Time (CST)** |
| Ensemble generation | Thursday 09:00 Beijing Time |
| Reference date | Saturday (end of the epidemiological week containing the deadline) |

Forecasts have been accepted since **August 21, 2025**, and will continue indefinitely. If the data availability schedule changes, participants will be notified at least one week in advance.

## How to Participate

### Step 1: Register Your Model

Create a YAML metadata file for your model in [`model-metadata/`](model-metadata/). See the [model metadata guide](model-metadata/README.md) for required fields and format.

### Step 2: Submit Forecasts

Submit weekly forecast CSV files to [`model-output/`](model-output/) via pull request. See the [model output guide](model-output/README.md) for the complete data format specification.

### Step 3: Automated Validation

All submissions are automatically validated via [GitHub Actions](https://github.com/features/actions) using the [hubValidations](https://github.com/hubverse-org/hubValidations) R package. Your pull request will show validation results before merging.

### Quick Start Checklist

- [ ] Read the [model metadata requirements](model-metadata/README.md)
- [ ] Create your `<team_abbr>-<model_abbr>.yml` metadata file
- [ ] Submit a pull request with your metadata
- [ ] Read the [model output format specification](model-output/README.md)
- [ ] Prepare your forecast CSV following the required format
- [ ] Submit weekly forecasts before **Wednesday 23:59 Beijing Time**

## Data Submission Format (Summary)

Forecast files are submitted as CSV files with the naming convention:

```
<reference_date>-<team_abbr>-<model_abbr>.csv
```

Each file must contain the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `reference_date` | Date (YYYY-MM-DD) | The Saturday ending the epidemiological week of the submission |
| `target` | String | `"wk inc covid prop ili"` |
| `horizon` | Integer | Weeks relative to `reference_date` (valid: -1 to 6) |
| `target_end_date` | Date (YYYY-MM-DD) | `reference_date + horizon × 7 days` |
| `location` | String | `"CN"` (national-level only) |
| `output_type` | String | `"quantile"` |
| `output_type_id` | Numeric | Quantile probability level (e.g., 0.5) |
| `value` | Numeric | Predicted value in percentage points (≥ 0) |

**Required quantile levels (23 total):**
`0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99`

For the complete format specification with examples, see [model-output/README.md](model-output/README.md).

## Data Sources

### Target Data

Forecast target data comes from the **China CDC Weekly Acute Respiratory Infectious Disease Surveillance Report**, covering the national sentinel hospital network. Historical surveillance data is available through an automated data collection system:

**[China CDC Crawl Repository](https://github.com/dailypartita/cn_cdc_crawl)**

This repository provides tools for automatically downloading, processing, and extracting structured surveillance data from China CDC weekly reports, including:
- PDF-to-text conversion of surveillance reports
- Automated extraction of pathogen detection rates
- Time series data for SARS-CoV-2, influenza, and other respiratory pathogens
- Outpatient ILI and inpatient SARI surveillance data

### Target Data Format

The target time series (`target-data/time-series.csv`) uses the following columns:

| Column | Description |
|--------|-------------|
| `date` | End date of the epidemiological week (Saturday) |
| `location` | `"CN"` |
| `target` | `"wk inc covid prop ili"` |
| `value` | SARS-CoV-2 positivity rate (%) |

## Model Development Guidelines

### Data Usage

Teams are encouraged to use all available time periods of surveillance data for model training and evaluation. Negative horizon values (e.g., -1) allow for nowcasting and retrospective model performance assessment.

### Best Practices

- **Cross-validation**: Use rolling-window cross-validation on historical data to assess model stability
- **Feature engineering**: Consider using lagged features and external data sources to improve forecast accuracy
- **Uncertainty quantification**: Ensure model outputs include adequate uncertainty information to support decision-making
- **External data**: Weather data, mobility data, vaccination coverage, and other relevant sources may be used with appropriate attribution

## Evaluation

Forecasts are evaluated against official surveillance data from the China CDC sentinel hospital network, obtained through the [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) automated data collection system.

### Metrics

| Metric | Description |
|--------|-------------|
| **WIS** (Weighted Interval Score) | Primary metric for probabilistic forecast accuracy |
| **MAE** (Mean Absolute Error) | Point forecast accuracy (using the median / 0.5 quantile) |
| **Interval Coverage** | Percentage of observations within predicted intervals (50%, 95%) |

Results are published on the [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/).

## Cloud Data Access

Live copies of model-output, target, and configuration files will be hosted on the Hubverse Amazon Web Services (AWS) infrastructure in a public S3 bucket (coming soon).

> **Note**: For efficient storage, all model-output files in S3 are stored in Parquet format, even if the original versions in the GitHub repository are CSV files.

GitHub remains the operational hub and primary interface for collecting modeler forecasts. The S3 mirror provides the most convenient way to access hub data without using git/GitHub or cloning the entire hub locally.

<details>
<summary>hubData (R)</summary>

[hubData](https://hubverse-org.github.io/hubData), the Hubverse R client, can create interactive sessions to access, filter, and transform hub model output data stored in S3.

### Installation

Follow the [instructions in the hubData documentation](https://hubverse-org.github.io/hubData/#installation).

### Usage

```r
library(dplyr)
library(hubData)

bucket_name <- "hub-bucket-name"
hub_bucket <- s3_bucket(bucket_name)
hub_con <- hubData::connect_hub(hub_bucket, file_format = "parquet", skip_checks = TRUE)
hub_con %>%
  dplyr::filter(location == "CN", output_type == "quantile") %>%
  hubData::collect_hub()
```

- [Full hubData documentation](https://hubverse-org.github.io/hubData/)

</details>

<details>
<summary>Polars (Python)</summary>

[Polars](https://pola.rs/) is a good choice for working with hub data in S3 until the Hubverse Python client (hubDataPy) is ready.

### Installation

```sh
pip install polars
```

### Usage

```python
import polars as pl

lf = pl.scan_parquet(
    "s3://hub-bucket-name/model-output/GZNL-SimpleTrend/*.parquet",
    storage_options={"skip_signature": "true"}
)
```

- [Full Polars documentation](https://docs.pola.rs/api/python/stable/reference/)

</details>

## Contact

- **Technical issues**: Open an issue on [GitHub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- **General inquiries**: Contact Yang Kaixin (yang_kaixin@gzlab.ac.cn)
- **Dashboard**: [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)

## Acknowledgments

China CDC

This repository follows the guidelines and standards outlined by the [hubverse](https://hubverse.io), which provides a set of data formats and open-source tools for modeling hubs.
