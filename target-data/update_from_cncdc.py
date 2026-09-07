#!/usr/bin/env python3
"""Update Hub target data from cn_cdc_crawl surveillance CSV."""

from __future__ import annotations

import argparse
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
DEFAULT_LOCAL_CSV = Path(
    "/data/ykx/covid19/get_data/cn_cdc_data/data/cncdc_surveillance_covid19.csv"
)
TARGET = "wk inc covid prop ili"
LOCATION = "CN"
MIN_DATE = "2022-12-05"
MAX_ORACLE_LOOKBACK = 6

ROOT = Path(__file__).resolve().parent
TIME_SERIES_PATH = ROOT / "time-series.csv"
ORACLE_PATH = ROOT / "oracle-output.csv"
TASKS_PATH = ROOT.parent / "hub-config" / "tasks.json"


def load_cncdc_rows(csv_path: Path | None = None) -> list[dict[str, str]]:
    """Load rows from a local CSV, or fall back to GitHub raw."""
    if csv_path is not None:
        path = csv_path.expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"cncdc CSV not found: {path}")
        text = path.read_text(encoding="utf-8-sig")
        return list(csv.DictReader(text.splitlines()))

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


def update_hub_target_data(csv_path: Path | None = None) -> dict[str, object]:
    """Regenerate Hub target-data (+ tasks.json dates) from cncdc COVID CSV."""
    rows = load_cncdc_rows(csv_path)
    time_series = build_time_series(rows)
    if not time_series:
        raise RuntimeError("No time-series rows generated from cncdc CSV")

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
    return {
        "earliest": earliest,
        "latest": latest,
        "time_series_rows": len(time_series),
        "oracle_rows": len(oracle),
        "tasks_changed": tasks_changed,
        "source": str(csv_path) if csv_path else CNCDC_URL,
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
        "--from-github",
        action="store_true",
        help="Force fetch from GitHub raw instead of local CSV",
    )
    args = parser.parse_args()

    csv_path: Path | None
    if args.from_github:
        csv_path = None
    elif args.csv is not None:
        csv_path = args.csv
    elif DEFAULT_LOCAL_CSV.exists():
        csv_path = DEFAULT_LOCAL_CSV
    else:
        csv_path = None

    stats = update_hub_target_data(csv_path)
    print(
        f"Updated {TIME_SERIES_PATH.name}: {stats['time_series_rows']} rows "
        f"({stats['earliest']} .. {stats['latest']})"
    )
    print(f"Updated {ORACLE_PATH.name}: {stats['oracle_rows']} rows")
    print(f"Updated tasks.json: {'yes' if stats['tasks_changed'] else 'no'}")
    print(f"Source: {stats['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
