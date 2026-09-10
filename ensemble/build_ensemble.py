#!/usr/bin/env python3
"""Build the hub ensemble as a weighted mean of member model quantiles.

The ensemble value at each quantile level is the weighted mean of the member
models' values at that same level (a weighted Vincent average). Weights come
from ensemble/weights.json and are renormalised over the models that actually
contributed to each task, so a missing submission does not shrink the ensemble.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import yaml

HUB_ROOT = Path(__file__).resolve().parent.parent
ENSEMBLE_DIR = Path(__file__).resolve().parent
TASKS_PATH = HUB_ROOT / "hub-config" / "tasks.json"
METADATA_DIR = HUB_ROOT / "model-metadata"
MODEL_OUTPUT_DIR = HUB_ROOT / "model-output"
WEIGHTS_PATH = ENSEMBLE_DIR / "weights.json"

ENSEMBLE_ID = "CNCovidHub-ensemble"
OUTPUT_TYPE = "quantile"
COLUMNS = [
    "reference_date",
    "target",
    "horizon",
    "target_end_date",
    "location",
    "output_type",
    "output_type_id",
    "value",
]

# (target, location, horizon) identifies one predictive distribution.
TaskKey = Tuple[str, str, int]
# Quantile levels are matched numerically so that "0.01" and "0.010" agree.
QLevel = float


def qkey(value: str | float) -> QLevel:
    return round(float(value), 6)


class RoundConfig:
    """The parts of hub-config/tasks.json the ensemble needs."""

    def __init__(self, tasks: dict) -> None:
        model_task = tasks["rounds"][0]["model_tasks"][0]
        task_ids = model_task["task_ids"]
        quantile = model_task["output_type"]["quantile"]["output_type_id"]

        self.reference_dates: List[str] = sorted(self._values(task_ids["reference_date"]))
        self.target_end_dates = set(self._values(task_ids["target_end_date"]))
        self.required_quantiles: List[QLevel] = [qkey(q) for q in quantile["required"]]
        # Preserve the config's own textual form so output matches other models.
        self.quantile_labels: Dict[QLevel, str] = {
            qkey(q): repr(q) if isinstance(q, float) else str(q) for q in quantile["required"]
        }

    @staticmethod
    def _values(task_id: dict) -> List:
        return list(task_id.get("required") or []) + list(task_id.get("optional") or [])

    @classmethod
    def load(cls) -> "RoundConfig":
        return cls(json.loads(TASKS_PATH.read_text(encoding="utf-8")))


def load_weight_config(path: Path = WEIGHTS_PATH) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    method = cfg.get("method", "weighted_mean")
    if method != "weighted_mean":
        raise SystemExit(f"Unsupported ensemble method: {method!r}")
    return cfg


def load_members(weight_cfg: dict) -> Dict[str, float]:
    """Return eligible member model_id -> weight."""
    default_weight = float(weight_cfg.get("default_weight", 1.0))
    overrides = {k: float(v) for k, v in (weight_cfg.get("weights") or {}).items()}

    members: Dict[str, float] = {}
    registered: set[str] = set()
    excluded: List[str] = []
    for path in sorted(METADATA_DIR.glob("*.yaml")):
        meta = yaml.safe_load(path.read_text(encoding="utf-8"))
        model_id = f"{meta['team_abbr']}-{meta['model_abbr']}"
        registered.add(model_id)
        if model_id == ENSEMBLE_ID:
            continue
        # Never feed one hub ensemble into another.
        if meta.get("ensemble_of_hub_models"):
            continue
        if not meta.get("designated_model"):
            continue
        weight = overrides.get(model_id, default_weight)
        if weight > 0:
            members[model_id] = weight
        else:
            excluded.append(model_id)

    if excluded:
        print(f"权重为 0，已排除: {', '.join(sorted(excluded))}")

    unknown = sorted(set(overrides) - registered)
    if unknown:
        print(f"警告: weights.json 中以下 model_id 未在 model-metadata 注册: {', '.join(unknown)}")

    return members


def read_member_round(
    model_id: str, reference_date: str, cfg: RoundConfig
) -> Dict[TaskKey, Dict[QLevel, float]]:
    """Read one model's submission, keyed by task and quantile level.

    Returns an empty mapping when the model did not submit for this round.
    """
    path = MODEL_OUTPUT_DIR / model_id / f"{reference_date}-{model_id}.csv"
    if not path.exists():
        return {}

    forecasts: Dict[TaskKey, Dict[QLevel, float]] = defaultdict(dict)
    # utf-8-sig tolerates submissions saved with a byte order mark.
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("output_type") != OUTPUT_TYPE:
                continue
            if row.get("reference_date") != reference_date:
                continue
            key: TaskKey = (row["target"], row["location"], int(row["horizon"]))
            forecasts[key][qkey(row["output_type_id"])] = float(row["value"])

    return dict(forecasts)


def weighted_quantiles(
    contributions: List[Tuple[float, Dict[QLevel, float]]], cfg: RoundConfig
) -> List[float]:
    """Weighted mean per quantile level, kept non-decreasing."""
    total = sum(weight for weight, _ in contributions)
    values = [
        sum(weight * quantiles[level] for weight, quantiles in contributions) / total
        for level in cfg.required_quantiles
    ]
    for i in range(1, len(values)):
        if values[i] < values[i - 1]:
            values[i] = values[i - 1]
    return values


def build_round(
    reference_date: str, members: Dict[str, float], cfg: RoundConfig, min_models: int
) -> Tuple[List[dict], List[str]]:
    """Return (rows, log lines) for one reference date."""
    submissions = {
        model_id: read_member_round(model_id, reference_date, cfg)
        for model_id in members
    }

    log: List[str] = []
    missing = sorted(m for m, f in submissions.items() if not f)
    if missing:
        log.append(f"未提交: {', '.join(missing)}")

    # Collect the models that supplied a complete quantile set for each task.
    by_task: Dict[TaskKey, List[Tuple[float, Dict[QLevel, float]]]] = defaultdict(list)
    incomplete: Dict[str, int] = defaultdict(int)
    for model_id, forecasts in submissions.items():
        for key, quantiles in forecasts.items():
            if all(level in quantiles for level in cfg.required_quantiles):
                by_task[key].append((members[model_id], quantiles))
            else:
                incomplete[model_id] += 1

    for model_id, count in sorted(incomplete.items()):
        log.append(f"分位点不全，已排除 {count} 个 horizon: {model_id}")

    reference = datetime.strptime(reference_date, "%Y-%m-%d")
    rows: List[dict] = []
    skipped: List[str] = []
    for key in sorted(by_task, key=lambda k: (k[0], k[1], k[2])):
        target, location, horizon = key
        contributions = by_task[key]
        if len(contributions) < min_models:
            skipped.append(f"horizon {horizon} (仅 {len(contributions)} 个模型)")
            continue

        target_end_date = (reference + timedelta(weeks=horizon)).strftime("%Y-%m-%d")
        if target_end_date not in cfg.target_end_dates:
            skipped.append(f"horizon {horizon} (target_end_date {target_end_date} 不在配置内)")
            continue

        values = weighted_quantiles(contributions, cfg)
        for level, value in zip(cfg.required_quantiles, values):
            rows.append(
                {
                    "reference_date": reference_date,
                    "target": target,
                    "horizon": horizon,
                    "target_end_date": target_end_date,
                    "location": location,
                    "output_type": OUTPUT_TYPE,
                    "output_type_id": cfg.quantile_labels[level],
                    "value": round(value, 4),
                }
            )

    if skipped:
        log.append(f"跳过: {'; '.join(skipped)}")

    contributors = sorted({m for m, f in submissions.items() if f} - set(incomplete))
    if rows:
        log.append(f"成员 {len(contributors)} 个: {', '.join(contributors)}")

    return rows, log


def write_round(reference_date: str, rows: List[dict]) -> Path:
    out_dir = MODEL_OUTPUT_DIR / ENSEMBLE_ID
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{reference_date}-{ENSEMBLE_ID}.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def resolve_reference_dates(args: argparse.Namespace, cfg: RoundConfig) -> List[str]:
    if args.all_rounds:
        return cfg.reference_dates
    if args.reference_date:
        unknown = [d for d in args.reference_date if d not in cfg.reference_dates]
        if unknown:
            raise SystemExit(
                f"参考日期不在 hub-config/tasks.json 的轮次中: {', '.join(unknown)}"
            )
        return list(args.reference_date)
    return [cfg.reference_dates[-1]]


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reference-date",
        action="append",
        metavar="YYYY-MM-DD",
        help="Round to build; repeatable. Defaults to the latest configured round.",
    )
    parser.add_argument(
        "--all-rounds",
        action="store_true",
        help="Rebuild every configured round that has enough member submissions.",
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=WEIGHTS_PATH,
        help="Alternative weights file, for trying a scheme before adopting it.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be built without writing any file.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    cfg = RoundConfig.load()
    weight_cfg = load_weight_config(args.weights)
    members = load_members(weight_cfg)
    if not members:
        raise SystemExit("没有合格的成员模型，无法构建集成")

    min_models = int(weight_cfg.get("min_models", 2))
    weight_summary = ", ".join(f"{m}={w:g}" for m, w in members.items())
    print(f"{ENSEMBLE_ID}: 权重 {weight_summary}")
    print(f"每个 horizon 至少需要 {min_models} 个模型\n")

    written = 0
    for reference_date in resolve_reference_dates(args, cfg):
        rows, log = build_round(reference_date, members, cfg, min_models)
        if not rows:
            if not args.all_rounds:
                print(f"{reference_date}: 无可用成员预测，未生成")
                for line in log:
                    print(f"  {line}")
            continue

        for line in log:
            print(f"  {line}")
        if args.dry_run:
            print(f"{reference_date}: 将生成 {len(rows)} 行 (dry-run)")
        else:
            path = write_round(reference_date, rows)
            print(f"{reference_date}: 已生成 {len(rows)} 行 -> {path.relative_to(HUB_ROOT)}")
        written += 1

    print(f"\n完成 {written} 轮")
    return 0


if __name__ == "__main__":
    sys.exit(main())
