# Hub Configuration

This directory contains the configuration files for the **China COVID-19 Forecast Hub**, following the [hubverse hub configuration standards](https://hubverse.io/en/latest/user-guide/hub-config.html).

## Files

| File | Description |
|------|-------------|
| [`admin.json`](admin.json) | Administrative settings for the hub (name, maintainer, repository, accepted file formats, timezone) |
| [`tasks.json`](tasks.json) | Modeling task definitions including task IDs, output types, target metadata, and submission windows |
| [`model-metadata-schema.json`](model-metadata-schema.json) | JSON Schema defining the required and optional fields for model metadata YAML files |

## `admin.json`

Defines global hub settings that should remain stable throughout the hub's operation:

- **Hub name**: China COVID-19 Forecast Hub
- **Maintainer**: GZNL Group
- **Accepted file formats**: CSV and Parquet
- **Timezone**: Asia/Shanghai (Beijing Time)
- **Schema version**: [v6.0.0](https://raw.githubusercontent.com/hubverse-org/schemas/main/v6.0.0/admin-schema.json)

## `tasks.json`

Defines the modeling tasks, including:

- **Round ID**: Derived from `reference_date` (dynamic rounds)
- **Task IDs**: `reference_date`, `location`, `horizon`, `target_end_date`, `target`
- **Output types**:
  - `quantile` — 23 required quantile levels from 0.01 to 0.99
  - `sample` — 200 samples per task (optional)
- **Target**: `wk inc covid prop ili` (weekly SARS-CoV-2 positivity rate among ILI cases)
- **Horizons**: -1 to 6 weeks relative to the reference date
- **Submission window**: Broad window (±360 days relative to reference date)

For a detailed explanation of each task ID and output type, see [model-output/README.md](../model-output/README.md).

## `model-metadata-schema.json`

Defines the JSON Schema that all model metadata files in [`model-metadata/`](../model-metadata/) must conform to. Required fields include:

- `team_name`, `team_abbr`, `model_name`, `model_abbr`
- `model_contributors` (name, affiliation, email)
- `license`
- `designated_model`
- `data_inputs`, `methods`, `methods_long`
- `ensemble_of_models`, `ensemble_of_hub_models`

See [model-metadata/README.md](../model-metadata/README.md) for a complete guide on creating metadata files.

## Schema Version

All configuration files reference the [hubverse schema v6.0.0](https://github.com/hubverse-org/schemas/tree/main/v6.0.0). For schema documentation, see the [hubverse schema reference](https://hubverse.io/en/latest/user-guide/tasks.html).
