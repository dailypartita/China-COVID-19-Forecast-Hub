# install.packages("remotes")
# remotes::install_github("hubverse-org/hubAdmin")
# remotes::install_github("hubverse-org/hubCI")
# remotes::install_github("hubverse-org/hubValidations")

setwd("/Users/ykx-gznl/Desktop/预防预警算法集成/hubverse_cn/China_COVID-19_Forecast_Hub/")

library(hubAdmin)
validate_config(
  hub_path = ".",
  config = c("tasks", "admin"),
  config_path = NULL,
  schema_version = "from_config",
  branch = getOption("hubAdmin.branch", default = "main")
)

library(hubCI)
use_hub_github_action(name = "validate-submission")

library(hubValidations)
v <- hubValidations::validate_pr(
  gh_repo = Sys.getenv("GITHUB_REPOSITORY"),
  pr_number = Sys.getenv("PR_NUMBER"),
  skip_submit_window_check = FALSE
)
hubValidations::check_for_errors(v, verbose = TRUE)

