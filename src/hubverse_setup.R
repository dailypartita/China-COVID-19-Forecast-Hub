# install.packages("remotes")
# remotes::install_github("hubverse-org/hubAdmin")
# remotes::install_github("hubverse-org/hubCI")
# remotes::install_github("hubverse-org/hubValidations")
# remotes::install_github("hubverse-org/hubVis")
# remotes::install_github("hubverse-org/hubExamples")

setwd("/Users/ykx-gznl/Desktop/预防预警算法集成/hubverse_cn/China_COVID-19_Forecast_Hub/")

# library(hubAdmin)
# validate_config(
#   hub_path = ".",
#   config = c("tasks", "admin"),
#   config_path = NULL,
#   schema_version = "from_config",
#   branch = getOption("hubAdmin.branch", default = "main")
# )
# 
# library(hubCI)
# use_hub_github_action(name = "validate-submission")
# 
# library(hubValidations)
# v <- hubValidations::validate_pr(
#   gh_repo = Sys.getenv("GITHUB_REPOSITORY"),
#   pr_number = Sys.getenv("PR_NUMBER"),
#   skip_submit_window_check = FALSE
# )
# hubValidations::check_for_errors(v, verbose = TRUE)

# library(hubData)
# library(dplyr)
# hub_path <- "./"
# hub_con <- hubData::connect_hub(hub_path)
# hub_con %>%
#   dplyr::filter(output_type == "quantile", location == "CN") %>%
#   dplyr::collect()

library(hubVis)
library(hubExamples)
head(scenario_outputs)
head(scenario_target_ts)
projection_data <- dplyr::mutate(scenario_outputs,
                                 target_date = as.Date(origin_date) + (horizon * 7) - 1)

target_data_us <- dplyr::filter(scenario_target_ts, location == "US",
                                date < min(projection_data$target_date) + 21,
                                date > "2020-10-01")
projection_data_us <- dplyr::filter(projection_data,
                                    scenario_id == "A-2021-03-05",
                                    location == "US")
plot_step_ahead_model_output(projection_data_us, target_data_us)





