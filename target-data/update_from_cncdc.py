#!/usr/bin/env python3
"""Update Hub target data from cn_cdc_dashboard surveillance CSVs.

Targets:
- wk inc covid prop ili  (weekly, from cncdc_surveillance_covid19.csv)
- wk inc flu prop ili    (weekly, from cncdc_surveillance_all.csv)
- mo inc dengue cases    (monthly, from notifiable_all.csv)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

CNCDC_BASE = (
    "https://raw.githubusercontent.com/dailypartita/cn_cdc_dashboard/main/data/"
)
COVID_URL = CNCDC_BASE + "cncdc_surveillance_covid19.csv"
SURV_ALL_URL = CNCDC_BASE + "cncdc_surveillance_all.csv"
NOTIFIABLE_URL = CNCDC_BASE + "notifiable_all.csv"
LOCAL_DATA_DIR = Path("/data/ykx/hubverse_proj/00-cn_cdc_dashboard/data")

TARGET_COVID = "wk inc covid prop ili"
TARGET_FLU = "wk inc flu prop ili"
TARGET_DENGUE = "mo inc dengue cases"
LOCATION = "CN"
MIN_DATE_COVID = "2022-12-05"
MAX_ORACLE_LOOKBACK = 6
QUANTILE_LEVELS = [
    0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
    0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99,
]

DENGUE_HORIZONS = [-1, 0, 1, 2, 3]
DENGUE_FIRST_REFERENCE = "2024-01-01"
DENGUE_LAST_REFERENCE = "2027-10-01"

ROOT = Path(__file__).resolve().parent
TIME_SERIES_PATH = ROOT / "time-series.csv"
ORACLE_PATH = ROOT / "oracle-output.csv"
TASKS_PATH = ROOT.parent / "hub-config" / "tasks.json"


def load_csv_rows(url: str, csv_path: Path | None) -> list[dict[str, str]]:
    """Load rows from a local CSV, or fall back to GitHub raw."""
    if csv_path is not None:
        path = csv_path.expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {path}")
        text = path.read_text(encoding="utf-8-sig")
        return list(csv.DictReader(text.splitlines()))

    with urllib.request.urlopen(url, timeout=60) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(text.splitlines()))


def local_or_github(filename: str, url: str, explicit: Path | None,
                    from_github: bool) -> tuple[list[dict[str, str]], str]:
    if not from_github:
        candidate = explicit or (LOCAL_DATA_DIR / filename)
        if candidate.exists():
            return load_csv_rows(url, candidate), str(candidate)
    return load_csv_rows(url, None), url


def build_weekly_series(rows: list[dict[str, str]], pathogen: str,
                        target: str, min_date: str | None) -> list[dict[str, str]]:
    series: dict[str, float] = {}
    for row in rows:
        if row.get("pathogen") != pathogen:
            continue
        date = row["reference_date"]
        if min_date and date < min_date:
            continue
        value = row.get("ili_percent", "").strip()
        if not value:
            continue
        series[date] = float(value)

    return [
        {
            "date": date,
            "location": LOCATION,
            "target": target,
            "value": f"{series[date]:g}",
        }
        for date in sorted(series.keys(), reverse=True)
    ]


def build_dengue_series(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    series: dict[str, int] = {}
    for row in rows:
        if row.get("disease") != "登革热" or row.get("row_kind") != "disease":
            continue
        cases = row.get("cases", "").strip()
        if not cases:
            continue
        # reference_date is the first day of the reported month
        series[row["reference_date"]] = int(float(cases))

    return [
        {
            "date": date,
            "location": LOCATION,
            "target": TARGET_DENGUE,
            "value": str(series[date]),
        }
        for date in sorted(series.keys(), reverse=True)
    ]


def month_diff(later: str, earlier: str) -> int:
    a = datetime.strptime(later, "%Y-%m-%d")
    b = datetime.strptime(earlier, "%Y-%m-%d")
    return (a.year - b.year) * 12 + (a.month - b.month)


def add_months(date: str, n: int) -> str:
    dt = datetime.strptime(date, "%Y-%m-%d")
    month = dt.month - 1 + n
    year = dt.year + month // 12
    month = month % 12 + 1
    return f"{year:04d}-{month:02d}-01"


def month_starts(first: str, last: str) -> list[str]:
    dates = []
    current = first
    while current <= last:
        dates.append(current)
        current = add_months(current, 1)
    return dates


def build_oracle(time_series: list[dict[str, str]], target: str,
                 monthly: bool) -> list[dict[str, str]]:
    rows = [row for row in time_series if row["target"] == target]
    dates = sorted({row["date"] for row in rows})
    values = {row["date"]: row["value"] for row in rows}
    oracle_rows: list[dict[str, str]] = []

    for ref in dates:
        available = [date for date in dates if date <= ref][-MAX_ORACLE_LOOKBACK:]
        for target_date in available:
            if monthly:
                horizon = month_diff(target_date, ref)
            else:
                ref_dt = datetime.strptime(ref, "%Y-%m-%d")
                target_dt = datetime.strptime(target_date, "%Y-%m-%d")
                horizon = (target_dt - ref_dt).days // 7
            oracle_rows.append(
                {
                    "reference_date": ref,
                    "target": target,
                    "horizon": str(horizon),
                    "target_end_date": target_date,
                    "location": LOCATION,
                    "output_type": "quantile",
                    "output_type_id": "0.5",
                    "oracle_value": values[target_date],
                }
            )

    return oracle_rows


def flu_target_metadata() -> dict[str, object]:
    return {
        "target_id": TARGET_FLU,
        "target_name": "Influenza virus positivity rate among department "
                       "influenza-like illness (ILI) cases",
        "target_units": "proportion",
        "target_keys": {"target": TARGET_FLU},
        "description": "This target represents the influenza virus positivity "
                       "rate among department influenza-like illness (ILI) "
                       "cases, as reported in China CDCs weekly National "
                       "Sentinel Surveillance of Acute Respiratory Infectious "
                       "Diseases, in the week ending on the target_end_date "
                       "(i.e., [horizon] weeks after the reference_date).",
        "target_type": "continuous",
        "is_step_ahead": True,
        "time_unit": "week",
    }


def dengue_target_metadata() -> dict[str, object]:
    return {
        "target_id": TARGET_DENGUE,
        "target_name": "Monthly reported dengue cases",
        "target_units": "count",
        "target_keys": {"target": TARGET_DENGUE},
        "description": "This target represents the number of reported dengue "
                       "cases in China, as published in China CDCs monthly "
                       "notifiable infectious disease surveillance report, in "
                       "the calendar month starting on the target_end_date "
                       "(i.e., [horizon] months after the reference_date).",
        "target_type": "discrete",
        "is_step_ahead": True,
        "time_unit": "month",
    }


def make_quantile_output_type(value_type: str) -> dict[str, object]:
    return {
        "quantile": {
            "output_type_id": {"required": QUANTILE_LEVELS},
            "is_required": False,
            "value": {"type": value_type, "minimum": 0},
        },
        "sample": {
            "output_type_id_params": {
                "type": "character",
                "max_length": 15,
                "min_samples_per_task": 200,
                "max_samples_per_task": 200,
                "compound_taskid_set": ["location"],
            },
            "is_required": False,
            "value": {"type": value_type, "minimum": 0},
        },
    }


def make_dengue_round() -> dict[str, object]:
    reference_dates = month_starts(DENGUE_FIRST_REFERENCE, DENGUE_LAST_REFERENCE)
    first_end = add_months(DENGUE_FIRST_REFERENCE, min(DENGUE_HORIZONS))
    last_end = add_months(DENGUE_LAST_REFERENCE, max(DENGUE_HORIZONS))
    return {
        "round_id_from_variable": True,
        "round_id": "reference_date",
        "model_tasks": [
            {
                "task_ids": {
                    "reference_date": {"required": None, "optional": reference_dates},
                    "location": {"required": None, "optional": [LOCATION]},
                    "horizon": {"required": None, "optional": DENGUE_HORIZONS},
                    "target_end_date": {
                        "required": None,
                        "optional": month_starts(first_end, last_end),
                    },
                    "target": {"required": None, "optional": [TARGET_DENGUE]},
                },
                "output_type": make_quantile_output_type("integer"),
                "target_metadata": [dengue_target_metadata()],
            }
        ],
        "submissions_due": {
            "relative_to": "reference_date",
            "start": -360,
            "end": 360,
        },
    }


def merge_dates(task_ids: dict[str, object], dates: list[str]) -> bool:
    changed = False
    for key in ("reference_date", "target_end_date"):
        current = task_ids[key]["optional"]
        merged = sorted(set(current) | set(dates))
        if merged != current:
            task_ids[key]["optional"] = merged
            changed = True
    return changed


def update_tasks_json(weekly_dates: list[str],
                      monthly_dates: list[str]) -> bool:
    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    rounds = tasks["rounds"]
    changed = False

    # Round 1 (weekly): covid + flu share task ids.
    weekly_task = rounds[0]["model_tasks"][0]
    if merge_dates(weekly_task["task_ids"], weekly_dates):
        changed = True
    targets = weekly_task["task_ids"]["target"]["optional"]
    if TARGET_FLU not in targets:
        targets.append(TARGET_FLU)
        changed = True
    metadata_ids = {m["target_id"] for m in weekly_task["target_metadata"]}
    if TARGET_FLU not in metadata_ids:
        weekly_task["target_metadata"].append(flu_target_metadata())
        changed = True

    # Round 2 (monthly): dengue.
    dengue_round = None
    for rnd in rounds[1:]:
        rnd_targets = rnd["model_tasks"][0]["task_ids"]["target"]["optional"]
        if TARGET_DENGUE in rnd_targets:
            dengue_round = rnd
            break
    if dengue_round is None:
        dengue_round = make_dengue_round()
        rounds.append(dengue_round)
        changed = True
    if merge_dates(dengue_round["model_tasks"][0]["task_ids"], monthly_dates):
        changed = True

    if changed:
        TASKS_PATH.write_text(
            json.dumps(tasks, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return changed


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_hub_target_data(args: argparse.Namespace) -> dict[str, object]:
    """Regenerate Hub target-data (+ tasks.json dates) from cncdc CSVs."""
    covid_rows, covid_src = local_or_github(
        "cncdc_surveillance_covid19.csv", COVID_URL, args.csv, args.from_github)
    surv_rows, surv_src = local_or_github(
        "cncdc_surveillance_all.csv", SURV_ALL_URL, args.surv_csv, args.from_github)
    notifiable_rows, notifiable_src = local_or_github(
        "notifiable_all.csv", NOTIFIABLE_URL, args.notifiable_csv, args.from_github)

    covid_series = build_weekly_series(
        covid_rows, "新型冠状病毒", TARGET_COVID, MIN_DATE_COVID)
    flu_series = build_weekly_series(
        surv_rows, "流感病毒", TARGET_FLU, None)
    dengue_series = build_dengue_series(notifiable_rows)
    if not covid_series or not flu_series or not dengue_series:
        raise RuntimeError("No time-series rows generated from cncdc CSVs")

    time_series = covid_series + flu_series + dengue_series
    oracle = (
        build_oracle(time_series, TARGET_COVID, monthly=False)
        + build_oracle(time_series, TARGET_FLU, monthly=False)
        + build_oracle(time_series, TARGET_DENGUE, monthly=True)
    )
    write_csv(
        TIME_SERIES_PATH,
        time_series,
        ["date", "location", "target", "value"],
    )
    write_csv(
        ORACLE_PATH,
        oracle,
        [
            "reference_date",
            "target",
            "horizon",
            "target_end_date",
            "location",
            "output_type",
            "output_type_id",
            "oracle_value",
        ],
    )
    weekly_dates = sorted(
        {row["date"] for row in covid_series + flu_series})
    monthly_dates = sorted({row["date"] for row in dengue_series})
    tasks_changed = update_tasks_json(weekly_dates, monthly_dates)

    def span(series: list[dict[str, str]]) -> str:
        return f"{series[-1]['date']} .. {series[0]['date']} ({len(series)} rows)"

    return {
        "covid": span(covid_series),
        "flu": span(flu_series),
        "dengue": span(dengue_series),
        "oracle_rows": len(oracle),
        "tasks_changed": tasks_changed,
        "sources": [covid_src, surv_src, notifiable_src],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Local cncdc_surveillance_covid19.csv (default: local path if present, else GitHub)",
    )
    parser.add_argument(
        "--surv-csv",
        type=Path,
        default=None,
        help="Local cncdc_surveillance_all.csv (default: local path if present, else GitHub)",
    )
    parser.add_argument(
        "--notifiable-csv",
        type=Path,
        default=None,
        help="Local notifiable_all.csv (default: local path if present, else GitHub)",
    )
    parser.add_argument(
        "--from-github",
        action="store_true",
        help="Force fetch from GitHub raw instead of local CSVs",
    )
    args = parser.parse_args()

    stats = update_hub_target_data(args)
    print(f"Updated {TIME_SERIES_PATH.name}:")
    print(f"  covid:  {stats['covid']}")
    print(f"  flu:    {stats['flu']}")
    print(f"  dengue: {stats['dengue']}")
    print(f"Updated {ORACLE_PATH.name}: {stats['oracle_rows']} rows")
    print(f"Updated tasks.json: {'yes' if stats['tasks_changed'] else 'no'}")
    for src in stats["sources"]:
        print(f"Source: {src}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
