# China COVID-19 Forecast Hub

This collaborative forecast hub collects and evaluates real-time predictions for SARS-CoV-2 positivity rates among influenza-like illness (ILI) cases from sentinel hospitals across China. The hub serves as a platform for comparing forecasting models and providing evidence-based insights for public health decision-making. Anyone interested in using these data for additional research or publications is requested to contact yang_kaixin@gzlab.ac.cn for information regarding attribution of the source forecasts.

## Weekly SARS-CoV-2 Positivity Rate Forecasts

This hub focuses on forecasting the weekly SARS-CoV-2 positivity rate among influenza-like illness cases from China's sentinel hospital surveillance network. Forecasts provide probabilistic predictions for both retrospective analysis (nowcasting) and future projections.

**Dates:** The forecast submission period began August 21, 2025, and will continue indefinitely. Participants are asked to submit weekly forecasts by **Wednesday 23:59 Beijing Time** each week (herein referred to as the Forecast Due Date). In the event that timelines of data availability change, the China COVID-19 Forecast Hub may change the day of week that forecasts are due. In this case, participants would be notified at least one week in advance. Weekly submissions (including file names) will be specified in terms of the reference date, which is the Saturday following the Forecast Due Date. The reference date is the last day of the epidemiological week (EW) (Sunday to Saturday) containing the Forecast Due Date.

**Prediction Targets:**
Participating teams are asked to provide China-wide predictions for the target
**"wk inc covid prop ili"** (weekly incident COVID-19 proportion in influenza-like illness).

Teams will submit probabilistic forecasts for the epidemiological week (EW) ending on the reference date as well as horizons ranging from **-3 to +6 weeks**. Teams can but are not required to submit forecasts for all weekly horizons. The evaluation data for forecasts will be the weekly aggregate of SARS-CoV-2 positivity rates from China CDC's sentinel hospital surveillance system. We will use the specification of EWs defined by the [CDC](https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf), which run Sunday through Saturday. The target end date for a prediction is the Saturday that ends an EW of interest, and can be calculated using the expression:
**target end date = reference date + horizon * (7 days)**.

There are standard software packages to convert from dates to epidemic weeks and vice versa (*e.g.*,
[MMWRweek](https://cran.r-project.org/web/packages/MMWRweek/) and
[lubridate](https://lubridate.tidyverse.org/reference/week.html) for R and [pymmwr](https://pypi.org/project/pymmwr/)
and [epiweeks](https://pypi.org/project/epiweeks/) for Python).

If you have questions about this target, please reach out to Yang Kaixin (yang_kaixin@gzlab.ac.cn).

## Data Sources

### Target Data Collection
The forecast target data comes from **China CDC's weekly acute respiratory syndrome surveillance reports** from sentinel hospitals across China. Historical surveillance data can be obtained from the automated data collection system at:

**🔗 [China CDC Crawl Repository](https://github.com/dailypartita/cn_cdc_crawl)**

This repository provides tools to automatically download, process, and extract structured surveillance data from China CDC's weekly reports, including:
- PDF-to-text conversion of surveillance reports
- Automated extraction of pathogen detection rates
- Time series data for SARS-CoV-2, influenza, and other respiratory pathogens
- Both outpatient ILI and inpatient SARI surveillance data

The extracted data follows the format:
- **report_date**: Report publication date
- **report_week**: Epidemiological week (YYYY-WW format)  
- **pathogen**: Pathogen name (including 新型冠状病毒/SARS-CoV-2)
- **ili_percent**: ILI case positivity rate (%)
- **sari_percent**: SARI case positivity rate (%)

## Getting Started

### For New Teams

1. **Register Your Model**: Create a model metadata file in the `model-metadata/` folder following the [model metadata guidelines](model-metadata/README.md)
2. **Submit Forecasts**: Weekly forecasts should be submitted as CSV files in the `model-output/` folder following the [submission guidelines](model-output/README.md)
3. **Validation**: All submissions are automatically validated through GitHub Actions to ensure format compliance

### Quick Start Checklist

- [ ] Read the [model metadata requirements](model-metadata/README.md)
- [ ] Create your `team-model.yml` metadata file
- [ ] Submit a pull request with your metadata
- [ ] Prepare your first forecast CSV file following the [format specifications](model-output/README.md)
- [ ] Submit weekly forecasts by **Wednesday 23:59 Beijing Time**

## Accessing hub data on the cloud

To ensure greater access to the data created by and submitted to this hub, real-time copies of its model-output,
target, and configuration files are hosted on the Hubverse's Amazon Web Services (AWS) infrastructure,
in a public S3 bucket (coming soon).

**Note**: For efficient storage, all model-output files in S3 are stored in parquet format, even if the original
versions in the GitHub repository are .csv.

GitHub remains the primary interface for operating the hub and collecting forecasts from modelers.
However, the mirrors of hub files on S3 are the most convenient way to access hub data without using git/GitHub or
cloning the entire hub to your local machine.

The sections below provide examples for accessing hub data on the cloud, depending on your goals and
preferred tools. The options include:

| Access Method              | Description                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------- |
| hubData (R)                | Hubverse R client and R code for accessing hub data                                   |
| Polars (Python)            | Python open-source library for data manipulation                                      |
| AWS command line interface | Download hub data to your machine and use hubData or Polars for local access          |

In general, accessing the data directly from S3 (instead of downloading it first) is more convenient. However, if
performance is critical (for example, you're building an interactive visualization), or if you need to work offline,
we recommend downloading the data first.

<!-------------------------------------------------- hubData ------------------------------------------------------->

<details>

<summary>hubData (R)</summary>

[hubData](https://hubverse-org.github.io/hubData), the Hubverse R client, can create an interactive session
for accessing, filtering, and transforming hub model output data stored in S3.

hubData is a good choice if you:

- already use R for data analysis
- want to interactively explore hub data from the cloud without downloading it
- want to save a subset of the hub's data (*e.g.*, forecasts for a specific date or target) to your local machine
- want to save hub data in a different file format (*e.g.*, parquet to .csv)

**Note**: S3 access will be available in future versions.

### Installing hubData

To install hubData and its dependencies (including the dplyr and arrow packages), follow the [instructions in the hubData documentation](https://hubverse-org.github.io/hubData/#installation).

### Using hubData

hubData's [`connect_hub()` function](https://hubverse-org.github.io/hubData/reference/connect_hub.html) returns an [Arrow
multi-file dataset](https://arrow.apache.org/docs/r/reference/Dataset.html) that represents a hub's model output data.
The dataset can be filtered and transformed using dplyr and then materialized into a local data frame
using the [`collect_hub()` function](https://hubverse-org.github.io/hubData/reference/collect_hub.html).


#### Accessing target data

*[hubData will be updated to access target data once the Hubverse target data standards are finalized.]*

#### Accessing model output data

Below is an example of using hubData to connect to a hub on S3 and filter the model output data.

```r
library(dplyr)
library(hubData)

bucket_name <- "hub-bucket-name"
hub_bucket <- s3_bucket(bucket_name)
hub_con <- hubData::connect_hub(hub_bucket, file_format = "parquet", skip_checks = TRUE)
hub_con %>%
  dplyr::filter(location == "MA", output_type == "quantile") %>%
  hubData::collect_hub()

```

- [full hubData documentation](https://hubverse-org.github.io/hubData/)

</details>

<!--------------------------------------------------- Polars ------------------------------------------------------->

<details>

<summary>Polars (Python)</summary>

The Hubverse team is currently developing a Python client (hubDataPy). Until hubDataPy is ready,
the [Polars](https://pola.rs/) library is a good option for working with hub data in S3.
Similar to pandas, Polars is based on dataframes and series. However, Polars has a more straightforward API and is
designed to work with larger-than-memory datasets.

Pandas users can access hub data as described below and then use the `to_pandas()` method to convert a Polars dataframe
to pandas format.

Polars is a good choice if you:

- already use Python for data analysis
- want to interactively explore hub data from the cloud without downloading it
- want to save a subset of the hub's data (*e.g.*, forecasts for a specific date or target) to your local machine
- want to save hub data in a different file format (*e.g.*, parquet to .csv)

### Installing polars

Use pip to install Polars:

```sh
pip install polars
```

### Using Polars

The examples below use the Polars
[`scan_parquet()` function](https://docs.pola.rs/api/python/dev/reference/api/polars.scan_parquet.html), which returns a
[LazyFrame](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html).
LazyFrames do not perform computations until necessary, so any filtering and transforms you apply to the data are
deferred until an explicit
[`collect()` operation](https://docs.pola.rs/api/python/stable/reference/lazyframe/api/polars.LazyFrame.collect.html#polars.LazyFrame.collect).

#### Accessing target data

Get all oracle-output files into a single DataFrame.

```python
import polars as pl

oracle_data = pl.scan_parquet(
    # the structure of the s3 link below will depend on how your hub organizes target data
    "s3://[hub-bucket-name]/target-data/oracle-output/*/*.parquet",
    storage_options={"skip_signature": "true"}
)

# filter and transform as needed and collect into a dataframe, for example:
oracle_dataframe = oracle_data.filter(pl.col("location") == "MA").collect()
```

#### Accessing model output data

Get the model-output files for a specific team (all rounds).
This example uses
[glob patterns to read from data multiple files into a single dataset](https://docs.pola.rs/user-guide/io/multiple/#reading-into-a-single-dataframe).

```python
import polars as pl

lf = pl.scan_parquet(
    "s3://[hub-bucket-name]/model-output/[modeling team name]/*.parquet",
    storage_options={"skip_signature": "true"}
)
```

#### Using partitions (hive-style)

If your data uses hive-style partitioning, Polars can use the partitions to filter the data before reading it.

```python
from datetime import datetime
import polars as pl

oracle_data = pl.scan_parquet(
    "s3://[hub-bucket-name]/target-data/oracle-output/",
    hive_partitioning=True,
    storage_options={"skip_signature": "true"}) \
.filter(pl.col("nowcast_date") == datetime(2025, 2, 5)) \
.collect()
```

- [Full documentation of the Polars Python API](https://docs.pola.rs/api/python/stable/reference/)

</details>

<!--------------------------------------------------- AWS CLI ------------------------------------------------------->

<details>

<summary>AWS CLI</summary>

AWS provides a terminal-based command line interface (CLI) for exploring and downloading S3 files.
This option is ideal if you:

- plan to work with hub data offline but don't want to use git or GitHub
- want to download a subset of the data (instead of the entire hub)
- are using the data for an application that requires local storage or fast response times

### Installing the AWS CLI

- Install the AWS CLI using the
[instructions here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- You can skip the instructions for setting up security credentials, since Hubverse data is public

### Using the AWS CLI

When using the AWS CLI, the `--no-sign-request` option is required, since it tells AWS to bypass a credential check
(*i.e.*, `--no-sign-request` allows anonymous access to public S3 data).

> [!NOTE]
> Files in the bucket's `raw` directory should not be used for analysis (they're for internal use only).

List all directories in the hub's S3 bucket:

```sh
aws s3 ls [hub-bucket-name] --no-sign-request
```

List all files in the hub's bucket:

```sh
aws s3 ls [hub-bucket-name] --recursive --no-sign-request
```

Download all of target-data contents to your current working directory:

```sh
aws s3 cp s3://[hub-bucket-name]/target-data/ . --recursive --no-sign-request
```

Download the model-output files for a specific team:

```sh
aws s3 cp s3://[hub-bucket-name]/[modeling-team-name]/UMass-flusion/ . --recursive --no-sign-request
```

- [Full documentation for `aws s3 ls`](https://docs.aws.amazon.com/cli/latest/reference/s3/ls.html)
- [Full documentation for `aws s3 cp`](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)

</details>

## Acknowledgments

This repository follows the guidelines and standards outlined by [the
[hubverse](https://hubverse.io), which provides a set of data formats and open source tools for modeling hubs.
