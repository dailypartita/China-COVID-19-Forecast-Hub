# 模型输出

[English](README.md) | **中文**

本目录存放 **中国 COVID-19 预测中心** 的预测提交文件。每个模型一个子目录，内含 CSV 预测文件。

本文是提交要点速查。完整说明、Hub 集成模型与本地校验见 [英文 README](README.md)。

## 如何提交

1. 将预测 CSV 放入对应的 `model-output/<team_abbr>-<model_abbr>/` 子目录。
2. 向本仓库的 `main` 分支提交 **Pull Request**。
3. GitHub Actions 会用 [hubValidations](https://github.com/hubverse-org/hubValidations) 自动校验。
4. 校验通过后，管理员审核并合并。

## 文件命名

```
<reference_date>-<team_abbr>-<model_abbr>.csv
```

- `reference_date`：提交所在监测周的**周一**，格式必须为 `YYYY-MM-DD`（不要用 `/`）
- `team_abbr` 与 `model_abbr` 必须与子目录名、元数据中的 `model_id` 一致

**示例：** `2026-08-31-MUST-SEIRS.csv`

## 文件格式

CSV，编码为 **UTF-8 无 BOM**，且**恰好 8 列**（顺序不限），不允许额外列、行尾多余逗号或空数据行。日期一律用 `YYYY-MM-DD`，不要写成 `2026/8/31` 或 `8/31/2026`。

部分电子表格（尤其是 Windows 版 Excel）保存 CSV 时会写入 BOM，表头会变成 `\ufeffreference_date`，导致校验失败。pandas 请使用 `df.to_csv(path, index=False, encoding="utf-8")`，不要用 `utf-8-sig`。

| # | 列名 | 类型 | 说明 |
|---|------|------|------|
| 1 | `reference_date` | 日期 (`YYYY-MM-DD`) | 监测周起始周一；必须与文件名中的日期一致 |
| 2 | `target` | 字符串 | 目前仅接受 `wk inc covid prop ili` |
| 3 | `horizon` | 整数 | `reference_date` 与 `target_end_date` 之间的周数 |
| 4 | `target_end_date` | 日期 (`YYYY-MM-DD`) | 目标监测周的起始周一 |
| 5 | `location` | 字符串 | 目前仅接受 `CN` |
| 6 | `output_type` | 字符串 | 目前仅接受 `quantile` |
| 7 | `output_type_id` | 数值 | 分位数水平（0–1 之间的小数） |
| 8 | `value` | 数值 | 预测值，非负；单位为**百分点**（0–100），不是比例（0–1） |

`target_end_date` 必须满足：`reference_date + horizon × 7 天`。

## Horizon

有效值为 **-1 到 6** 的整数。可提交其中任意子集；建议补齐 -1..6 以便与其他模型可比，但校验并不要求全部 horizon。

| Horizon | 含义 |
|---------|------|
| -1 | Nowcast：参考周的前一周 |
| 0 | Nowcast：参考周本身 |
| 1 | 提前 1 周预测 |
| … | … |
| 6 | 提前 6 周预测 |

对文件中**每一个**已提交的 horizon，都必须给出下面全部 23 个分位数。

## 必填分位数（23 个）

每个 `reference_date`、`horizon`、`target`、`location` 组合都需要这 23 个水平：

```
0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99
```

```python
quantiles = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35,
             0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
             0.85, 0.9, 0.95, 0.975, 0.99]
```

## 常见校验失败原因

| 现象 | 原因 | 处理方法 |
|------|------|----------|
| `[req_vals]` 失败 | 某个已提交 horizon 的分位数不足 23 个 | 文件中每个 horizon 都提供上表全部 23 个水平 |
| 提示缺少 `reference_date` 列 | 文件带 UTF-8 BOM，表头读成 `\ufeffreference_date` | 另存为 UTF-8 无 BOM |
| CSV 日期解析失败 / `CSV conversion error to date32` / 非法值如 `2026/8/31` | 日期写成了斜杠或 Excel 本地格式（`2026/8/31`、`8/31/2026`）而非 ISO | `reference_date`、`target_end_date` 以及文件名中的日期一律用 `YYYY-MM-DD` |
| 出现意外额外列 / 因行尾逗号导致 `file_read` 或 schema 问题 | 末尾空列或空数据行（从电子表格导出时常见） | 恰好 8 列，不要末尾空列或空数据行 |
| `[round_id_valid]` 失败 | `reference_date` 不是周一，或该轮次尚未开放 | 使用监测周起始周一；轮次随目标数据更新而开放 |
| `[valid_vals]` 失败 | 负值，或把阳性率写成了 0–1 的比例 | 使用 0–100 刻度的非负百分点 |

## 更多说明

集成模型（`CNCovidHub-ensemble`）、本地校验步骤、周日程与迟交政策见 [英文 README](README.md)。

## 支持

- **技术问题**：[GitHub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- **一般咨询：** yang_kaixin@gzlab.ac.cn
- **Dashboard：** [China COVID-19 Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)
