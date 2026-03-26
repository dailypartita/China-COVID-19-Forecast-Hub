# Model Metadata

This directory contains model metadata files for the **China COVID-19 Forecast Hub**. Each participating model must have a metadata file in [YAML format](https://yaml.org/) that describes the model, team, and methods. The metadata specification is aligned with the [hubverse model metadata guide](https://hubverse.io/en/latest/user-guide/model-metadata.html).

## Table of Contents

- [File Naming](#file-naming)
- [Required Fields](#required-fields)
- [Optional Fields](#optional-fields)
- [Example Metadata File](#example-metadata-file)
- [Validation](#validation)
- [Registration Steps](#registration-steps)

## File Naming

Each metadata file must be named:

```
<team_abbr>-<model_abbr>.yml
```

Where `<team_abbr>-<model_abbr>` is the `model_id`, matching the subdirectory name in `model-output/`. For example, the metadata file for the model submitting to `model-output/GZNL-SimpleTrend/` would be named `GZNL-SimpleTrend.yml`.

## Required Fields

All metadata files must include the following fields, in this order:

### `team_name`

Full name of the team. Must be fewer than 50 characters.

### `team_abbr`

Abbreviated team name. Must be fewer than 16 characters, containing only alphanumeric characters and underscores.

### `model_name`

Full name of the model. Must be fewer than 50 characters.

### `model_abbr`

Abbreviated model name. Must be fewer than 16 characters, containing only alphanumeric characters and underscores.

### `model_contributors`

A list of all individuals involved in the forecasting effort. Each contributor requires a `name`, `affiliation`, and `email`. An optional `orcid` identifier may also be provided. All listed email addresses will be added to the model contributor mailing list.

```yaml
model_contributors: [
  {
    "name": "Contributor Name",
    "affiliation": "Institution Name",
    "email": "contributor@example.com",
    "orcid": "1234-1234-1234-1234"
  }
]
```

### `license`

One of the following accepted licenses:

| License | Description |
|---------|-------------|
| `CC0-1.0` | Creative Commons Zero (public domain) |
| `CC-BY-4.0` | Creative Commons Attribution 4.0 |
| `CC-BY_SA-4.0` | Creative Commons Attribution-ShareAlike 4.0 |
| `PPDL` | Public Domain Dedication and License |
| `ODC-by` | Open Data Commons Attribution |
| `ODbL` | Open Database License |
| `OGL-3.0` | Open Government Licence 3.0 |

We encourage teams to use `CC-BY-4.0` to allow the broadest use of model outputs.

### `designated_model`

Boolean (`true` or `false`) indicating whether this model should be considered for inclusion in hub ensembles and public visualizations. Each team may designate up to two models. Models with `designated_model: false` will still be included in internal evaluation.

### `data_inputs`

A description of the data sources used to inform the model, especially sources beyond the sentinel hospital SARS-CoV-2 positivity target data. Examples:

- China CDC weekly surveillance reports
- Historical ILI surveillance data from [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl)
- Weather data, mobility data, vaccination coverage, etc.

### `methods`

A brief description of the forecasting methods. Must be fewer than 200 characters.

### `methods_long`

A full description of the methods used by the model. This should include whether spatial correlations are considered, how the model accounts for uncertainty, and any modifications made over time (with dates).

### `ensemble_of_models`

Boolean (`true` or `false`) indicating whether the model is an ensemble of any independent component models.

### `ensemble_of_hub_models`

Boolean (`true` or `false`) indicating whether the model is specifically an ensemble of other models submitted to this hub.

## Optional Fields

### `model_version`

An identifier for the version of the model.

### `website_url`

URL of a public-facing website with additional information about the model (e.g., a dashboard showing model forecasts).

### `repo_url`

URL of a GitHub (or similar) repository containing the model code.

### `citation`

One or more citations for manuscripts or preprints describing the model in detail.

### `team_funding`

Information about funding sources for the team or team members.

## Example Metadata File

Below is a complete example metadata file:

```yaml
team_name: "Guangzhou National Laboratory"
team_abbr: "GZNL"
model_name: "Simple Trend Model"
model_abbr: "SimpleTrend"
model_contributors: [
  {
    "name": "Yang Kaixin",
    "affiliation": "Guangzhou National Laboratory",
    "email": "yang_kaixin@gzlab.ac.cn"
  }
]
license: "CC-BY-4.0"
designated_model: true
data_inputs: "China CDC weekly surveillance reports, historical ILI data from cn_cdc_crawl"
methods: "Statistical time series forecasting using simple trend extrapolation"
methods_long: "This model uses time series analysis to predict SARS-CoV-2 positivity rates based on sentinel hospital surveillance data from China CDC. It combines recent trend analysis with historical seasonal patterns to generate probabilistic forecasts at multiple horizons."
ensemble_of_models: false
ensemble_of_hub_models: false
repo_url: "https://github.com/dailypartita/China-COVID-19-Forecast-Hub"
```

## Validation

You can optionally validate your metadata file locally before submitting a pull request. Validation will also run automatically on the pull request.

### Local Validation

1. Fork and clone the repository.
2. Create your metadata file and place it in the `model-metadata/` directory.
3. Install the hubValidations R package:

```r
remotes::install_github("hubverse-org/hubValidations")
```

4. Validate your metadata file:

```r
hubValidations::validate_model_metadata(
    hub_path = ".",
    file_path = "GZNL-SimpleTrend.yml"
)
```

If everything is correct, you should see output like:

```
✔ model-metadata-schema.json: File exists at path hub-config/model-metadata-schema.json.
✔ GZNL-SimpleTrend.yml: File exists at path model-metadata/GZNL-SimpleTrend.yml.
✔ GZNL-SimpleTrend.yml: Metadata file extension is "yml" or "yaml".
✔ GZNL-SimpleTrend.yml: Metadata file directory name matches "model-metadata".
✔ GZNL-SimpleTrend.yml: Metadata file contents are consistent with schema specifications.
✔ GZNL-SimpleTrend.yml: Metadata file name matches the model_id specified within the metadata file.
```

## Registration Steps

1. **Fork the repository**: Create a fork of this repository on GitHub.
2. **Create your metadata file**: Add your `<team_abbr>-<model_abbr>.yml` file to the `model-metadata/` directory following the format above.
3. **Validate locally** (optional): Use the hubValidations package to check your file.
4. **Submit a pull request**: Create a pull request to add your metadata file.
5. **Await review**: A hub administrator will review and merge your metadata.

Once your model is registered, you can begin submitting weekly forecasts to the [`model-output/`](../model-output/) directory. See the [model output guide](../model-output/README.md) for submission format details.
