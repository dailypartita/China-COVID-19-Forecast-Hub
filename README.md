<div align="center">

# China COVID-19 Forecast Hub

**English** | [中文](README.zh.md)

</div>

Collaborative forecasting hub built on the [Hubverse](https://hubverse.io/) framework. Collects, validates, and archives weekly probabilistic forecasts of SARS-CoV-2 positivity rate among influenza-like illness (ILI) cases from China's national sentinel surveillance network.

**Dashboard:** [dailypartita.github.io/China-COVID-19-Forecast-Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)

**Target data:** [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) · **Coverage:** 2022-12-05 – 2026-08-17

## Features

### Forecast Target

- **Target:** `wk inc covid prop ili` — weekly SARS-CoV-2 positivity rate among ILI cases
- **Location:** `CN` (national)
- **Output:** 23-quantile probabilistic forecasts (horizons -1 to 6)
- **Units:** Percentage points (e.g., `13.5` = 13.5%), not proportions

### Submission

- Register model metadata in `model-metadata/`
- Submit weekly forecast CSV files via pull request to `model-output/`
- File naming: `<reference_date>-<team_abbr>-<model_abbr>.csv`

### Validation

All pull requests are validated automatically via [GitHub Actions](.github/workflows/validate-submission.yaml) using [hubValidations](https://github.com/hubverse-org/hubValidations).

## Active Models

| Team | Models |
|------|--------|
| GZNL | NextWave |
| XMU_CTModelling | FNN, LSTM, XGBoost, GRU, TCN |
| MUST | SEIRS |

See the [Dashboard Evaluation page](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/eval.html) for latest rankings.

## Data Updates

| Step | Schedule |
|------|----------|
| CDC sentinel report | Weekly (typically Wednesday) |
| Target data sync | From [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) via `target-data/update_from_cncdc.py` |
| Forecast submission deadline | Wednesday 23:59 Beijing time |
| Dashboard data refresh | Thursday 17:33 UTC (automated) |

Target data from [China CDC sentinel surveillance](https://www.chinacdc.cn/jksj/jksj04_14275/). Extraction tool: [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl).

## Repository Structure

```
China-COVID-19-Forecast-Hub/
├── hub-config/          # Hub configuration (admin, tasks, schemas)
├── model-metadata/      # Model registration (one YAML per model)
├── model-output/        # Forecast submissions (one folder per model)
├── target-data/         # Ground truth and oracle data
│   ├── time-series.csv
│   ├── oracle-output.csv
│   └── update_from_cncdc.py
└── .github/workflows/   # Automated PR validation
```

## Architecture

| Component | Description |
|-----------|-------------|
| Framework | [Hubverse](https://hubverse.io/) |
| Schema | Hubverse v6.0.0 |
| Validation | hubValidations + GitHub Actions |
| Target data | [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) |
| Dashboard | [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/) |

### Configuration

- [`hub-config/admin.json`](hub-config/admin.json) — hub settings
- [`hub-config/tasks.json`](hub-config/tasks.json) — modeling tasks and quantile requirements
- [`hub-config/model-metadata-schema.json`](hub-config/model-metadata-schema.json) — metadata schema

### Workflows

- **Hub Submission Validation (R)** (`validate-submission.yaml`) — validate forecast PRs on merge

## Contributing

### Register a model

1. Create a YAML metadata file in [`model-metadata/`](model-metadata/)
2. Open a pull request following the [model metadata guide](model-metadata/README.md)

### Submit forecasts

1. Place CSV files in `model-output/<team_abbr>-<model_abbr>/`
2. Follow the [model output guide](model-output/README.md) for format and quantile requirements
3. Submit a pull request before **Wednesday 23:59 Beijing time**
4. Ensure the PR branch is up to date with `main` before validation runs

### Update target data

```bash
python3 target-data/update_from_cncdc.py
```

This refreshes `time-series.csv`, `oracle-output.csv`, and `hub-config/tasks.json` from the latest [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) release.

## Data Access

| Dataset | Path | Description |
|---------|------|-------------|
| Target time series | `target-data/time-series.csv` | Weekly observed positivity rates |
| Oracle output | `target-data/oracle-output.csv` | Ground truth for evaluation and dashboard |
| Model forecasts | `model-output/<model_id>/` | Submitted probabilistic forecasts |
| Hub config | `hub-config/` | Task definitions and admin settings |

Browse data interactively on the [Dashboard data page](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/data.html).

## Links

- [Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)
- [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl)
- [Hub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- [Hubverse docs](https://docs.hubverse.io/)

## Contact

- **Technical issues:** [GitHub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- **General inquiries:** yang_kaixin@gzlab.ac.cn

## License

See [LICENSE](LICENSE).
