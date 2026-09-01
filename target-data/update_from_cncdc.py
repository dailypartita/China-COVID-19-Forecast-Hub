#!/usr/bin/env python3
"""Update Hub target data from cn_cdc_crawl surveillance CSV."""

from __future__ import annotations

import csv
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

CNCDC_URL = (
    "https://raw.githubusercontent.com/dailypartita/cn_cdc_crawl/main/"
    "data/cncdc_surveillance_covid19.csv"
)
TARGET = "wk inc covid prop ili"
LOCATION = "CN"
MIN_DATE = "2022-12-05"
MAX_ORACLE_LOOKBACK = 6

ROOT = Path(__file__).resolve().parent
TIME_SERIES_PATH = ROOT / "time-series.csv"
ORACLE_PATH = ROOT / "oracle-output.csv"
TASKS_PATH = ROOT.parent / "hub-config" / "tasks.json"


def fetch_cncdc_rows() -> list[dict[str, str]]:
    with urllib.request.urlopen(CNCDC_URL, timeout=60) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(text.splitlines()))


def build_time_series(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    series: dict[str, float] = {}
    for row in rows:
        date = row["reference_date"]
        if date < MIN_DATE:
            continue
        series[date] = float(row["ili_percent"])

    return [
        {
            "date": date,
            "location": LOCATION,
            "target": TARGET,
            "value": f"{series[date]:g}",
        }
        for date in sorted(series.keys(), reverse=True)
    ]


def build_oracle(time_series: list[dict[str, str]]) -> list[dict[str, str]]:
    dates = sorted({row["date"] for row in time_series})
    values = {row["date"]: float(row["value"]) for row in time_series}
    oracle_rows: list[dict[str, str]] = []

    for ref in dates:
        available = [date for date in dates if date <= ref][-MAX_ORACLE_LOOKBACK:]
        ref_dt = datetime.strptime(ref, "%Y-%m-%d")
        for target in available:
            target_dt = datetime.strptime(target, "%Y-%m-%d")
            horizon = (target_dt - ref_dt).days // 7
            oracle_rows.append(
                {
                    "reference_date": ref,
                    "target": TARGET,
                    "horizon": str(horizon),
                    "target_end_date": target,
                    "location": LOCATION,
                    "output_type": "quantile",
                    "output_type_id": "0.5",
                    "oracle_value": f"{values[target]:g}",
                }
            )

    return oracle_rows


def update_tasks_json(time_series: list[dict[str, str]]) -> bool:
    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    dates = sorted({row["date"] for row in time_series})
    task_ids = tasks["rounds"][0]["model_tasks"][0]["task_ids"]
    changed = False

    for key in ("reference_date", "target_end_date"):
        current = task_ids[key]["optional"]
        merged = sorted(set(current) | set(dates))
        if merged != current:
            task_ids[key]["optional"] = merged
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


def main() -> int:
    rows = fetch_cncdc_rows()
    time_series = build_time_series(rows)
    oracle = build_oracle(time_series)

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
    tasks_changed = update_tasks_json(time_series)

    latest = time_series[0]["date"]
    earliest = time_series[-1]["date"]
    print(f"Updated {TIME_SERIES_PATH.name}: {len(time_series)} rows ({earliest} .. {latest})")
    print(f"Updated {ORACLE_PATH.name}: {len(oracle)} rows")
    print(f"Updated tasks.json: {'yes' if tasks_changed else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
