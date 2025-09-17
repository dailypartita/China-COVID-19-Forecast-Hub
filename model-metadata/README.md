# 模型元数据

本文件夹包含向**中国新冠预测中心**提交的模型元数据文件。这些文件的规范已调整为与[hubverse文档中的模型元数据指南](https://docs.hubverse.io/en/latest/user-guide/model-metadata.html)保持一致。

每个模型都需要有[yaml格式](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)的元数据。

本说明提供了有关[数据格式](#数据格式)以及在提交元数据文件的pull request之前可以进行的[验证](#数据验证)的详细信息。

# 数据格式

## 必需变量

本节描述yaml文档中的每个变量（键）。
请按此顺序排列变量。

### team_name
团队名称，少于50个字符。

### team_abbr
团队名称缩写，少于16个字符。

### model_name
模型名称，少于50个字符。

### model_abbr
模型缩写名称，少于16个字母数字字符。

### model_contributors

参与预测工作的所有个人列表。
每位贡献者都需要姓名、所属单位和电子邮件地址。个人还可以包含可选的orcid标识符。
提供的所有电子邮件地址将被添加到模型贡献者的邮件分发列表中。

此字段的语法应为：
```
model_contributors: [
  {
    "name": "建模者姓名 1",
    "affiliation": "机构名称 1",
    "email": "modeler1@example.com",
    "orcid": "1234-1234-1234-1234"
  },
  {
    "name": "建模者姓名 2",
    "affiliation": "机构名称 2",
    "email": "modeler2@example.com",
    "orcid": "1234-1234-1234-1234"
  }
]
```

### license

[接受的许可证](https://github.com/cdcepi/FluSight-forecast-hub/blob/673e983fee54f3a21448071ac46a9f78d27dd164/hub-config/model-metadata-schema.json#L69-L75)之一。

我们鼓励团队提交"cc-by-4.0"许可证，以允许最广泛的使用，
包括私人疫苗生产（这将被"cc-by-nc-4.0"许可证排除）。

### designated_model 

团队指定的布尔指示器（`true`或`false`），表示模型是否应被考虑纳入Hub集成和公共可视化。团队最多可以指定两个模型作为designated_model纳入。designated_model值为'False'的模型仍将包含在内部预测中心评估中。

### data_inputs

用于为模型提供信息的数据源列表或描述。特别是那些超出哨点医院SARS-CoV-2阳性率目标数据的数据源。例如：
- 中国CDC周监测报告
- [cn_cdc_crawl](https://github.com/dailypartita/cn_cdc_crawl)的历史ILI监测数据
- 天气数据、流动性数据、疫苗接种覆盖率等

**数据使用说明**：本中心支持使用所有时间段的数据，包括过去、当前和未来几周的数据进行模型训练和评估。团队可以充分利用可用数据进行回顾性分析和前瞻性预测。

### methods

对预测方法的简要描述，少于200个字符。

### methods_long

对此模型所用方法的完整描述。除其他细节外，这应该包括是否考虑空间相关性以及模型如何考虑不确定性。如果模型被修改，此字段还可用于提供修改日期和变更描述。

### ensemble_of_models

布尔值（`true`或`false`），指示模型是否为任何独立组件模型的集成。

### ensemble_of_hub_models

布尔值（`true`或`false`），指示模型是否特别是提交给预测中心的其他模型的集成。

## 可选

### model_version
模型版本的标识符

### website_url

包含有关模型的其他数据的网站网址。
我们鼓励团队提交最用户友好的模型版本，
例如显示模型预测的仪表板或类似内容。

### repo_url

包含模型代码的github（或类似）存储库网址。

### citation

一个或多个有关模型详细信息的手稿或预印本引用。例如，"Gibson GC , Reich NG , Sheldon D. Real-time mechanistic bayesian forecasts of Covid-19 mortality. medRxiv. 2020. https://doi.org/10.1101/2020.12.22.20248736"。

### team_funding 

有关团队或团队成员的资助来源信息，这些信息在任何相关出版物中自然包含。例如，"National Institutes of General Medical Sciences (R01GM123456). The content is solely the responsibility of the authors and does not necessarily represent the official views of NIGMS."

# 数据验证

您可以选择在向中心提交pull request之前本地验证模型元数据文件。请注意，这不是必需的，因为验证也会在pull request上运行。要本地运行验证，请按照以下步骤操作：

1. 创建`China_COVID-19_Forecast_Hub`存储库的fork，然后将fork克隆到您的计算机。
2. 为您的模型创建模型元数据文件草稿，并将其放在此克隆的`model-metadata`文件夹中。
3. 通过在R会话中运行以下命令来安装hubValidations包：
``` r
remotes::install_github("hubverse-org/hubValidations")
```
4. 通过在R会话中运行以下命令来验证您的元数据文件草稿：
``` r
hubValidations::validate_model_metadata(
    hub_path="<您的hub存储库克隆路径>",
    file_path="<您的元数据文件名称>")
```

例如，如果您的工作目录是hub存储库的根目录，您可以使用类似以下的命令：
``` r
hubValidations::validate_model_metadata(hub_path=".", file_path="GZNL-test_001.yml")
```

如果一切正常，您应该看到类似以下的输出：
```
✔ model-metadata-schema.json: File exists at path hub-config/model-metadata-schema.json.
✔ GZNL-test_001.yml: File exists at path model-metadata/GZNL-test_001.yml.
✔ GZNL-test_001.yml: Metadata file extension is "yml" or "yaml".
✔ GZNL-test_001.yml: Metadata file directory name matches "model-metadata".
✔ GZNL-test_001.yml: Metadata file contents are consistent with schema specifications.
✔ GZNL-test_001.yml: Metadata file name matches the `model_id` specified within the metadata file.
```

如果有任何错误，您会看到描述问题的消息。

## 模型元数据文件示例

以下是GZNL测试模型的元数据文件示例：

```yaml
team_name: "广州国家实验室"
team_abbr: "GZNL"
model_name: "GZNL测试模型001"
model_abbr: "test_001"
model_contributors: [
  {
    "name": "杨凯鑫",
    "affiliation": "广州国家实验室",
    "email": "yang_kaixin@gzlab.ac.cn"
  }
]
license: "cc-by-4.0"
designated_model: true
data_inputs: "中国CDC周监测报告，历史ILI数据，多时间窗口的监测数据用于模型训练和评估"
methods: "基于统计建模的时间序列预测，支持多时间窗口分析"
methods_long: "该模型使用时间序列分析来预测SARS-CoV-2阳性率，基于中国CDC哨点医院的全时间段监测数据。模型结合了季节性模式和趋势分析，利用过去、当前和预测未来的数据进行训练和验证，以提供更准确的预测和性能评估。"
ensemble_of_models: false
ensemble_of_hub_models: false
```

## 模型注册所需步骤

1. **Fork存储库**: 创建此存储库的fork
2. **创建元数据文件**: 将您的`team-model.yml`文件添加到`model-metadata/`文件夹
3. **本地验证**（可选）: 使用hubValidations包运行验证检查
4. **提交pull request**: 创建pull request以添加您的元数据文件
5. **等待批准**: Hub管理员将审查并合并您的元数据

一旦您的模型注册成功，您就可以开始向`model-output/`文件夹提交每周预测。
