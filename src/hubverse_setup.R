
# # You can install the latest version of hubAdmin from the R-universe:
# install.packages("hubAdmin", repos = c("https://hubverse-org.r-universe.dev", "https://cloud.r-project.org"))
# 
# # install.packages("remotes")
# remotes::install_github("hubverse-org/hubAdmin")
# remotes::install_github("hubverse-org/hubCI")

setwd("/Users/ykx-gznl/Desktop/预防预警算法集成/hubverse_cn/China_COVID-19_Forecast_Hub/")

library(hubAdmin)

validate_config(
  hub_path = "."
)

library(hubCI)

use_hub_github_action(name = "validate-submission")



