#!/usr/bin/env python3
"""将 XMU 系列模型输出的 value 列乘以 100（从小数转为百分数）"""

import csv
import glob
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
pattern = os.path.join(base_dir, "XMU_CTModelling-*", "*.csv")
files = sorted(glob.glob(pattern))

print(f"找到 {len(files)} 个 XMU 模型输出文件")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    for row in rows:
        try:
            val = float(row["value"])
            row["value"] = round(val * 100, 2)
        except (ValueError, KeyError):
            continue

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    rel = os.path.relpath(filepath, base_dir)
    print(f"  ✓ {rel}")

print(f"\n完成，共处理 {len(files)} 个文件")
