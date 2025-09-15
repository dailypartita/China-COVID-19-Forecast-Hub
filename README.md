# 中国新冠病毒预测中心

这个协作预测平台收集和评估来自中国哨点医院的流感样病例中SARS-CoV-2阳性率的实时预测。该平台为比较预测模型、为公共卫生决策提供循证见解。任何有兴趣将这些数据用于其他研究或发表的人员，请联系 yang_kaixin@gzlab.ac.cn 获取关于数据源归属的信息。

## 每周SARS-CoV-2阳性率预测

本中心专注于预测来自中国哨点医院监测网络的每周流感样病例中SARS-CoV-2阳性率。预测提供用于回顾性分析（现报告）和未来预测的概率性预测。

**提交时间：** 预测提交期从2025年8月21日开始，将无限期持续。要求参与者每周**北京时间周三23:59**之前提交预测（以下称为预测提交截止日期）。如果数据可用性时间表发生变化，中国新冠病毒预测中心可能会更改预测提交的截止日期。在这种情况下，参与者将至少提前一周收到通知。每周提交（包括文件名）将以参考日期为准，参考日期是预测提交截止日期之后的周六。参考日期是包含预测提交截止日期的流行病学周（EW）（周日至周六）的最后一天。

**预测目标：**
参与团队需要提供全国范围内以下目标的预测：
**"wk inc covid prop ili"** （每周流感样病例中新冠病毒发生率比例）。

团队需要提交截至参考日期的流行病学周（EW）以及**-3至+6周**范围内各时间跨度的概率性预测。团队可以但不是必须提交所有周时间跨度的预测。预测的评估数据将来自中国疾控中心哨点医院监测系统的SARS-CoV-2阳性率周汇总数据。我们将使用[CDC](https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf)定义的流行病学周规范，即周日至周六。预测的目标结束日期是感兴趣的流行病学周结束的周六，可以使用以下表达式计算：
**目标结束日期 = 参考日期 + 时间跨度 * (7天)**。

有标准的软件包可以在日期和流行病学周之间进行转换（*例如*，R语言的[MMWRweek](https://cran.r-project.org/web/packages/MMWRweek/)和[lubridate](https://lubridate.tidyverse.org/reference/week.html)，Python的[pymmwr](https://pypi.org/project/pymmwr/)和[epiweeks](https://pypi.org/project/epiweeks/)）。

如果您对此目标有任何疑问，请联系（yang_kaixin@gzlab.ac.cn）。

## 数据来源

### 目标数据收集
预测目标数据来自**中国疾控中心每周急性呼吸道传染病监测报告**，覆盖全国哨点医院。历史监测数据可从自动化数据收集系统获取：

**🔗 [中国疾控中心爬虫仓库](https://github.com/dailypartita/cn_cdc_crawl)**

该仓库提供自动下载、处理和提取中国疾控中心周报结构化监测数据的工具，包括：
- 监测报告的PDF转文本转换
- 自动提取病原体检测率
- SARS-CoV-2、流感和其他呼吸道病原体的时间序列数据
- 门诊流感样病例和住院严重急性呼吸道感染监测数据

提取的数据遵循以下格式：
- **report_date**: 报告发布日期
- **report_week**: 流行病学周（YYYY-WW格式）
- **pathogen**: 病原体名称（包括新型冠状病毒/SARS-CoV-2）
- **ili_percent**: 流感样病例阳性率（%）
- **sari_percent**: 严重急性呼吸道感染病例阳性率（%）

## 模型开发与评估规范

### 数据使用与模型完整性指导原则

为确保模型评估的科学性和公平性，我们建议参与团队在模型开发过程中遵循以下数据使用准则：

#### **训练数据时间边界**
- **建议做法**：模型训练时请避免使用当前参考日期及其前三周的监测数据（即时间跨度 -3、-2、-1、0 对应的实际观测值）
- **评估设计**：这些时间窗口的数据将作为测试集，用于客观评估各模型的预测性能
- **科学原理**：此设计模拟真实世界预测场景，其中模型需要基于历史数据预测未来和近期趋势

#### **数据完整性监督**
- **质量保证**：我们将定期审查提交的模型预测，以确保遵循最佳建模实践
- **反馈机制**：如发现潜在的数据时间性使用问题，我们将与相关团队沟通并提供改进建议
- **持续改进**：基于透明的评估原则，我们致力于维护一个公平、科学的预测比较环境

#### **最佳实践建议**
- **交叉验证**：推荐在历史数据上使用滚动窗口交叉验证来评估模型稳定性
- **特征工程**：鼓励使用滞后特征和外部数据源来提高预测准确性
- **不确定性量化**：建议模型输出包含充分的不确定性信息以支持决策

> **💡 提示**：这些指导原则旨在建立一个科学、公平的预测评估环境。我们欢迎团队间的技术交流和方法论讨论，共同提升预测模型的质量和实用性。

## 入门指南

### 新团队加入

1. **注册您的模型**：在 `model-metadata/` 文件夹中创建模型元数据文件，遵循[模型元数据指导原则](model-metadata/README.md)
2. **提交预测**：每周预测应作为CSV文件提交到 `model-output/` 文件夹，遵循[提交指导原则](model-output/README.md)
3. **验证**：所有提交都通过GitHub Actions自动验证，以确保格式合规性

### 快速入门检查清单

- [ ] 阅读[模型元数据要求](model-metadata/README.md)
- [ ] 创建您的 `team-model.yml` 元数据文件
- [ ] 提交包含您元数据的拉取请求
- [ ] 根据[格式规范](model-output/README.md)准备您的第一个预测CSV文件
- [ ] 在**北京时间每周三23:59**前提交周预测

## 云端数据访问

为确保对本中心创建和提交的数据有更大的访问权限，model-output、target和配置文件的实时副本托管在Hubverse的亚马逊网络服务（AWS）基础设施上，存储在公共S3存储桶中（即将推出）。

**注意**：为了高效存储，S3中的所有model-output文件都以parquet格式存储，即使GitHub仓库中的原始版本是.csv格式。

GitHub仍然是操作中心和收集建模者预测的主要接口。
但是，S3上中心文件的镜像是在不使用git/GitHub或将整个中心克隆到本地机器的情况下访问中心数据的最便捷方式。

下面的部分根据您的目标和首选工具提供了访问云端中心数据的示例。选项包括：

| 访问方法              | 描述                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------- |
| hubData (R)                | Hubverse R客户端和用于访问中心数据的R代码                                   |
| Polars (Python)            | 用于数据操作的Python开源库                                      |
| AWS命令行接口 | 将中心数据下载到您的机器并使用hubData或Polars进行本地访问          |

一般来说，直接从S3访问数据（而不是先下载）更加便捷。但是，如果性能至关重要（例如，您正在构建交互式可视化），或者您需要离线工作，我们建议先下载数据。

<!-------------------------------------------------- hubData ------------------------------------------------------->

<details>

<summary>hubData (R)</summary>

[hubData](https://hubverse-org.github.io/hubData)，Hubverse R客户端，可以创建交互式会话来访问、过滤和转换存储在S3中的中心模型输出数据。

如果您符合以下条件，hubData是一个好选择：

- 已经使用R进行数据分析
- 想要从云端交互式探索中心数据而无需下载
- 想要将中心数据的子集（*例如*，特定日期或目标的预测）保存到本地机器
- 想要以不同的文件格式保存中心数据（*例如*，parquet转.csv）

**注意**：S3访问将在未来版本中可用。

### 安装hubData

要安装hubData及其依赖项（包括dplyr和arrow包），请遵循[hubData文档中的说明](https://hubverse-org.github.io/hubData/#installation)。

### 使用hubData

hubData的[`connect_hub()`函数](https://hubverse-org.github.io/hubData/reference/connect_hub.html)返回一个[Arrow多文件数据集](https://arrow.apache.org/docs/r/reference/Dataset.html)，代表中心的模型输出数据。
数据集可以使用dplyr进行过滤和转换，然后使用[`collect_hub()`函数](https://hubverse-org.github.io/hubData/reference/collect_hub.html)实现为本地数据框。


#### 访问目标数据

*[一旦Hubverse目标数据标准最终确定，hubData将更新以访问目标数据。]*

#### 访问模型输出数据

以下是使用hubData连接到S3上的中心并过滤模型输出数据的示例。

```r
library(dplyr)
library(hubData)

bucket_name <- "hub-bucket-name"
hub_bucket <- s3_bucket(bucket_name)
hub_con <- hubData::connect_hub(hub_bucket, file_format = "parquet", skip_checks = TRUE)
hub_con %>%
  dplyr::filter(location == "MA", output_type == "quantile") %>%
  hubData::collect_hub()

```

- [完整hubData文档](https://hubverse-org.github.io/hubData/)

</details>

<!--------------------------------------------------- Polars ------------------------------------------------------->

<details>

<summary>Polars (Python)</summary>

Hubverse团队目前正在开发Python客户端（hubDataPy）。在hubDataPy准备就绪之前，[Polars](https://pola.rs/)库是在S3中使用中心数据的好选择。
与pandas类似，Polars基于数据框和序列。但是，Polars具有更直观的API，专为处理大于内存的数据集而设计。

Pandas用户可以如下所述访问中心数据，然后使用`to_pandas()`方法将Polars数据框转换为pandas格式。

如果您符合以下条件，Polars是一个好选择：

- 已经使用Python进行数据分析
- 想要从云端交互式探索中心数据而无需下载
- 想要将中心数据的子集（*例如*，特定日期或目标的预测）保存到本地机器
- 想要以不同的文件格式保存中心数据（*例如*，parquet转.csv）

### 安装polars

使用pip安装Polars：

```sh
pip install polars
```

### 使用Polars

下面的示例使用Polars的[`scan_parquet()`函数](https://docs.pola.rs/api/python/dev/reference/api/polars.scan_parquet.html)，它返回一个[LazyFrame](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)。
LazyFrames在必要时才执行计算，因此您对数据应用的任何过滤和转换都会延迟到显式的[`collect()`操作](https://docs.pola.rs/api/python/stable/reference/lazyframe/api/polars.LazyFrame.collect.html#polars.LazyFrame.collect)。

#### 访问目标数据

将所有oracle-output文件合并到单个DataFrame中。

```python
import polars as pl

oracle_data = pl.scan_parquet(
    # 下面s3链接的结构将取决于您的中心如何组织目标数据
    "s3://[hub-bucket-name]/target-data/oracle-output/*/*.parquet",
    storage_options={"skip_signature": "true"}
)

# 根据需要进行过滤和转换，并收集到数据框中，例如：
oracle_dataframe = oracle_data.filter(pl.col("location") == "MA").collect()
```

#### 访问模型输出数据

获取特定团队的model-output文件（所有轮次）。
此示例使用[全局模式将多个文件读入单个数据集](https://docs.pola.rs/user-guide/io/multiple/#reading-into-a-single-dataframe)。

```python
import polars as pl

lf = pl.scan_parquet(
    "s3://[hub-bucket-name]/model-output/[建模团队名称]/*.parquet",
    storage_options={"skip_signature": "true"}
)
```

#### 使用分区（hive-style）

如果您的数据使用hive-style分区，Polars可以在读取数据之前使用分区来过滤数据。

```python
from datetime import datetime
import polars as pl

oracle_data = pl.scan_parquet(
    "s3://[hub-bucket-name]/target-data/oracle-output/",
    hive_partitioning=True,
    storage_options={"skip_signature": "true"}) \
.filter(pl.col("nowcast_date") == datetime(2025, 2, 5)) \
.collect()
```

- [Polars Python API完整文档](https://docs.pola.rs/api/python/stable/reference/)

</details>

## 致谢

中国疾控中心

本仓库遵循[hubverse](https://hubverse.io)概述的指导原则和标准，hubverse为建模中心提供一套数据格式和开源工具。