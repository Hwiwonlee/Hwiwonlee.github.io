
적당한 규모의 KoGES data를 handling할 기회를 얻었다.  
1. 3개의 cohort를 다루고 있는 KoGES data를 merge하기  
2. 각 cohort의 follow-up 기간이 다르므로 indexing으로 구분하기  

```r
dir <- "path"

urban_raw <- read.csv("path/file name", stringsAsFactors=F)
rural_raw <- read.csv("path/file name", stringsAsFactors=F)
local_raw <- read.csv("path/file name", stringsAsFactors=F)

# pre. Library
library(reshape2)

# 1. Preprocessing

urban_raw %>%
  select(RID, matches("DS1_CA[[:digit:]]")) %>%
  # as_tibble() %>%

  # dplyr::filter(DS1_CA1 == 2) %>% # 5274
  # group_by(DS1_CA1CU) %>%
  # count()

  # dplyr::filter(DS1_CA2 == 2) %>%  # 162
  # group_by(DS1_CA2CU) %>%
  # count()

  # dplyr::filter(DS1_CA3 == 2) %>% # 11
  # group_by(DS1_CA3CU) %>%
  # count()

  # dplyr::filter(DS1_CA1 == 2 & DS1_CA2 == 2 ) # 162
  # dplyr::filter(DS1_CA1 == 2 & DS1_CA3 == 2 ) # 11
  # dplyr::filter(DS1_CA2 == 2 & DS1_CA3 == 2 ) # 11


  # Baseline에서 전체 암환자 수는 5274명이며
  # 한 개의 다른 암이 있는 경우는 162명, 두 개의 다른 암이 있는 경우는 11명이다.
  # 치료 경과에 따라 Grouping을 하고 합을 구해보기도 했다.


  # CA1 & CA1SP 과거력은 있지만 암종이 기록되지 않은 경우, 240
  # dplyr::filter(DS1_CA1 == 2 & DS1_CA1SP == ".") %>%

  # CA2 & CA2SP 과거력은 있지만 암종이 기록되지 않은 경우, 10
  # dplyr::filter(DS1_CA1 == 2 & DS1_CA2 == 2 & DS1_CA2SP == ".") %>%

  # CA3 & CA3SP 과거력은 있지만 암종이 기록되지 않은 경우, 7
  # dplyr::filter(DS1_CA3 == 2 & DS1_CA3SP == ".")

  # 위의 모든 경우가 CA1 & CA1SP의 240개의 obs와 중복되므로 과거력은 있으나 암종이 기록되지 않은 경우는 총 240개


  # DS1_CA1를 기준으로 filtering한 후 암 유무로 group 후 암종과 치료경과를 기준하여 count
  # 즉, 암 유무 -> 암종 -> 치료경과의 경우의 수를 모두 볼 수 있음
  # https://dplyr.tidyverse.org/reference/tally.html
  dplyr::filter(is.na(DS1_CA1) != T ) %>%
  group_by(DS1_CA1) %>% count(DS1_CA1SP, DS1_CA1CU)

urban_raw %>%
  select(RID, matches("DS[[:digit:]]_CA[[:digit:]]")) %>%
  dplyr::filter(is.na(DS1_CA1) != T ) %>%
  group_by(DS1_CA1) %>% count(DS1_CA1SP, DS1_CA1CU, DS1_CA1CU1, DS2_CA1, DS2_CA1SP, DS2_CA1CU) %>%
  openxlsx::write.xlsx(., file = "test.xlsx")




urban_raw %>%
  select(RID, matches("DS2_CA[[:digit:]]")) %>%
  # dplyr::filter(DS2_CA1 == 2) # 1759
  # dplyr::filter(DS2_CA2 == 2) # 40
  # dplyr::filter(DS2_CA1 == 2 & DS2_CA2 == 2) # 40

  # Follow-up에서 전체 암환자 수는 1759명이며
  # 한 개의 다른 암이 있는 경우는 40명이다.

  # dplyr::filter(DS2_CA1SP == ".") %>% # DS2에서는 모든 암종이 기록되어 있음
  # dplyr::filter(DS2_CA2 == 2 & DS2_CA2SP == ".") # DS2에서는 모든 암종이 기록되어 있음


  group_by(DS2_CA1SP) %>%
  dplyr::filter(DS2_CA1 == 2) %>%
  count() %>% arrange(as.numeric(DS2_CA1SP))



rural_raw %>%
  select(RID, matches("NCB_CA[[:digit:]]|NCF1_CA")) %>%
  dplyr::filter(is.na(NCB_CA1) != T ) %>%
  group_by(NCB_CA1) %>% count(NCB_CA1NA, NCB_CA1CU, NCF1_CA, NCF1_CA_NA1_1, NCF1_CA_NA2_1, NCF1_CACU) %>%
  openxlsx::write.xlsx(., file = "test_rural.xlsx")

```
