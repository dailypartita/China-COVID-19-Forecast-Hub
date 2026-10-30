<div align="center">

# China Infectious Disease Forecast Hub

**English** | [中文](README.zh.md)

</div>

Collaborative forecasting hub built on the [Hubverse](https://hubverse.io/) framework. Collects, validates, and archives probabilistic forecasts of SARS-CoV-2 and influenza positivity rates among influenza-like illness (ILI) cases from China's national sentinel surveillance network, plus monthly reported dengue cases from national notifiable disease surveillance.

**Dashboard:** [dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard](https://dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard/)

**Target data:** [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard) · **Observed coverage:** COVID-19 weekly 2022-12-05 – 2026-10-12 · Flu weekly 2024-11-11 – 2026-10-12 · Dengue monthly 2024-01 – 2026-08 · **Configured submission rounds:** Mondays through 2027-10-25

## Features

### Forecast Targets

**Round 1 — weekly respiratory targets**

- **Targets:** `wk inc covid prop ili`, `wk inc flu prop ili` — weekly SARS-CoV-2 / influenza virus positivity rates among ILI cases
- **Location:** `CN` (national)
- **Output:** 23-quantile probabilistic forecasts (horizons -1 to 6; teams may submit any subset — full -1..6 is recommended for comparability, but not all are required for validation)
- **Units:** Percentage points (e.g., `13.5` = 13.5%), not proportions

**Round 2 — monthly dengue target**

- **Target:** `mo inc dengue cases` — monthly reported dengue cases from notifiable disease surveillance
- **Location:** `CN` (national)
- **Output:** 23-quantile probabilistic forecasts (horizons -1 to 3 months; reference dates are the 1st of each month)
- **Units:** Case counts (integers)

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

See the [Dashboard Evaluation page](https://dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard/eval.html) for latest rankings.

## Data Updates

| Step | Schedule |
|------|----------|
| CDC sentinel report | Weekly (typically Wednesday) |
| Target data sync | From [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard) via `target-data/update_from_cncdc.py` (automated: `sync-target-data.yaml`) |
| Forecast submission deadline | Wednesday 23:59 Beijing time |
| Dashboard data refresh | Thursday 17:33 UTC (automated) |

Target data from [China CDC sentinel surveillance](https://www.chinacdc.cn/jksj/jksj04_14275/) (weekly respiratory pathogens) and [China CDC notifiable disease reports](https://www.chinacdc.cn/jksj/jksj01/) (monthly dengue). Structured data source: [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard).

## Repository Structure

```
China-Infectious-Disease-Forecast-Hub/
├── hub-config/          # Hub configuration (admin, tasks, schemas)
├── model-metadata/      # Model registration (one YAML per model)
├── model-output/        # Forecast submissions (one folder per model)
├── ensemble/            # Weights and build script for the hub ensemble
├── target-data/         # Ground truth and oracle data
│   ├── time-series.csv
│   ├── oracle-output.csv
│   └── update_from_cncdc.py
└── .github/workflows/   # Automated PR validation + target-data sync
```

## Architecture

| Component | Description |
|-----------|-------------|
| Framework | [Hubverse](https://hubverse.io/) |
| Schema | Hubverse v6.0.0 |
| Validation | hubValidations + GitHub Actions |
| Target data | [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard) |
| Dashboard | [China Infectious Disease Forecast Dashboard](https://dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard/) |

### Configuration

- [`hub-config/admin.json`](hub-config/admin.json) — hub settings
- [`hub-config/tasks.json`](hub-config/tasks.json) — modeling tasks and quantile requirements
- [`hub-config/model-metadata-schema.json`](hub-config/model-metadata-schema.json) — metadata schema

### Workflows

- **Hub Submission Validation (R)** (`validate-submission.yaml`) — validate forecast PRs on merge
- **Sync target data from cn_cdc_dashboard** (`sync-target-data.yaml`) — scheduled/manual refresh of `target-data/` and `tasks.json` dates; commits only when something changes

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

Automated on a schedule (Fri/Sun 08:00 UTC) and via Actions → **Sync target data from cn_cdc_dashboard**. Manual local run:

```bash
python3 target-data/update_from_cncdc.py --from-github
```

This refreshes `time-series.csv`, `oracle-output.csv`, and `hub-config/tasks.json` from the latest [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard) release.

## Data Access

| Dataset | Path | Description |
|---------|------|-------------|
| Target time series | `target-data/time-series.csv` | Weekly observed positivity rates + monthly dengue cases |
| Oracle output | `target-data/oracle-output.csv` | Ground truth for evaluation and dashboard |
| Model forecasts | `model-output/<model_id>/` | Submitted probabilistic forecasts |
| Hub config | `hub-config/` | Task definitions and admin settings |

Browse data interactively on the [Dashboard data page](https://dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard/data.html).

## Links

- [Forecast Dashboard](https://dailypartita.github.io/China-Infectious-Disease-Forecast-Dashboard/)
- [cn_cdc_dashboard](https://github.com/dailypartita/cn_cdc_dashboard)
- [Hub Issues](https://github.com/dailypartita/China-Infectious-Disease-Forecast-Hub/issues)
- [Hubverse docs](https://docs.hubverse.io/)

## Contact

- **Technical issues:** [GitHub Issues](https://github.com/dailypartita/China-Infectious-Disease-Forecast-Hub/issues)
- **General inquiries:** yang_kaixin@gzlab.ac.cn

## License

See [LICENSE](LICENSE).
