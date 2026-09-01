<div align="center">

# 中国 COVID-19 预测中心 Forecast Hub

[English](README.md) | **中文**

</div>

基于 [Hubverse](https://hubverse.io/) 框架构建的协作式预测中心，用于收集、校验和归档全国哨点监测网络中门急诊 ILI 病例 SARS-CoV-2 阳性率的周度概率预测。

**在线 Dashboard：** [dailypartita.github.io/China-COVID-19-Forecast-Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)

**目标数据：** [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) · **覆盖范围：** 2022-12-05 – 2026-08-17

## 平台功能

### 预测目标

- **指标：** `wk inc covid prop ili` — 门急诊 ILI 病例中 SARS-CoV-2 周度阳性率
- **地区：** `CN`（全国）
- **输出：** 23 分位数概率预测（horizon -1 至 6）
- **单位：** 百分点（如 `13.5` 表示 13.5%），非比例值

### 预测提交

- 在 `model-metadata/` 注册模型元数据
- 通过 Pull Request 向 `model-output/` 提交周度预测 CSV
- 文件命名：`<reference_date>-<team_abbr>-<model_abbr>.csv`

### 自动校验

所有 Pull Request 通过 [GitHub Actions](.github/workflows/validate-submission.yaml) 调用 [hubValidations](https://github.com/hubverse-org/hubValidations) 自动校验。

## 参与模型

| 团队 | 模型 |
|------|------|
| GZNL | ExponentialSmoothing, SeasonalDecomposition, SimpleTrend |
| XMU_CTModelling | FNN, LSTM, XGBoost, GRU, TCN |
| MUST | SEIRS |

最新排名与详细指标请查看 Dashboard [Evaluation 页面](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/eval.html)。

## 数据更新

| 环节 | 时间 |
|------|------|
| CDC 哨点监测报告发布 | 每周（通常周三） |
| 目标数据同步 | 通过 `target-data/update_from_cncdc.py` 从 [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) 更新 |
| 模型预测提交截止 | 每周三 23:59（北京时间） |
| Dashboard 数据更新 | 每周四 17:33 UTC（自动） |

监测数据来源于中国疾控中心[《全国急性呼吸道传染病哨点监测情况》](https://www.chinacdc.cn/jksj/jksj04_14275/)，结构化提取工具：[cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl)。

## 仓库结构

```
China-COVID-19-Forecast-Hub/
├── hub-config/          # Hub 配置（admin、tasks、schema）
├── model-metadata/      # 模型注册（每个模型一个 YAML）
├── model-output/        # 预测提交（每个模型一个目录）
├── target-data/         # 观测真值与 oracle 数据
│   ├── time-series.csv
│   ├── oracle-output.csv
│   └── update_from_cncdc.py
└── .github/workflows/   # PR 自动校验
```

## 技术架构

| 组件 | 说明 |
|------|------|
| 框架 | [Hubverse](https://hubverse.io/) |
| Schema | Hubverse v6.0.0 |
| 校验 | hubValidations + GitHub Actions |
| 目标数据 | [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) |
| Dashboard | [中国 COVID-19 预测中心 Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/) |

### 配置文件

- [`hub-config/admin.json`](hub-config/admin.json) — Hub 基本设置
- [`hub-config/tasks.json`](hub-config/tasks.json) — 建模任务与分位数要求
- [`hub-config/model-metadata-schema.json`](hub-config/model-metadata-schema.json) — 元数据 schema

### 自动化工作流

- **Hub Submission Validation (R)**（`validate-submission.yaml`）— 合并前校验预测 PR

## 参与贡献

### 注册模型

1. 在 [`model-metadata/`](model-metadata/) 创建 YAML 元数据文件
2. 按 [模型元数据指南](model-metadata/README.md) 提交 Pull Request

### 提交预测

1. 将 CSV 文件放入 `model-output/<team_abbr>-<model_abbr>/`
2. 按 [模型输出指南](model-output/README.md) 填写格式与分位数要求
3. 在**每周三 23:59（北京时间）**前提交 Pull Request
4. 校验前请将 PR 分支与 `main` 最新代码同步

### 更新目标数据

```bash
python3 target-data/update_from_cncdc.py
```

该脚本从 [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl) 最新数据刷新 `time-series.csv`、`oracle-output.csv` 和 `hub-config/tasks.json`。

## 数据获取

| 数据集 | 路径 | 说明 |
|--------|------|------|
| 目标时间序列 | `target-data/time-series.csv` | 周度观测阳性率 |
| Oracle 输出 | `target-data/oracle-output.csv` | 评估与 Dashboard 用真值 |
| 模型预测 | `model-output/<model_id>/` | 已提交的概率预测 |
| Hub 配置 | `hub-config/` | 任务定义与管理配置 |

也可通过 [Dashboard 数据页面](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/data.html) 交互式浏览。

## 相关链接

- [Forecast Dashboard](https://dailypartita.github.io/China-COVID-19-Forecast-Dashboard/)
- [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl)
- [Hub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- [Hubverse 文档](https://docs.hubverse.io/)

## 联系方式

- **技术问题：** [GitHub Issues](https://github.com/dailypartita/China-COVID-19-Forecast-Hub/issues)
- **一般咨询：** yang_kaixin@gzlab.ac.cn

## 许可证

详见 [LICENSE](LICENSE) 文件。
