
적당한 규모의 KoGES data를 handling할 기회를 얻었다.  
1. 3개의 cohort를 다루고 있는 KoGES data를 merge하기  
2. 각 cohort의 follow-up 기간이 다르므로 indexing으로 구분하기  

SAS dataset이 문제다. sasdata로 불러온 것을 csv로 내보내면 파일이 깨져버린다.  
아마 encoding문제인 것 같은데 두 개의 타입으로 encoding된 dataset이 있는 게 가능한가?

식이 점수는 하루 단위로 계산  
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
  select(RID, matches("DS[[:digit:]]_CA[[:digit:]]")) %>%
  # dplyr::filter(DS2_CA1 == 2) # 1759
  # dplyr::filter(DS2_CA2 == 2) # 40
  # dplyr::filter(DS2_CA1 == 2 & DS2_CA2 == 2) # 40

  # Follow-up에서 전체 암환자 수는 1759명이며
  # 한 개의 다른 암이 있는 경우는 40명이다.

  # dplyr::filter(DS2_CA1SP == ".") %>% # DS2에서는 모든 암종이 기록되어 있음
  # dplyr::filter(DS2_CA2 == 2 & DS2_CA2SP == ".") # DS2에서는 모든 암종이 기록되어 있음
  
  # Baseline에서 암 과거력이 있는 사람들의 암종 파악
  # group_by(DS1_CA1SP) %>%
  # dplyr::filter(DS1_CA1 == 2) %>%
  # count() %>% arrange(as.numeric(DS1_CA1SP))
  
  # Follow-up에서 새로 추가된, 암 과거력이 있는 사람들의 암종 파악
  dplyr::filter(DS1_CA1 != 2)
  group_by(DS2_CA1SP) %>%
  dplyr::filter(DS2_CA1 == 2) %>%
  count() %>% arrange(as.numeric(DS2_CA1SP))



rural_raw %>%
  select(RID, matches("NCB_CA[[:digit:]]|NCF1_CA")) %>%
  dplyr::filter(is.na(NCB_CA1) != T ) %>%
  group_by(NCB_CA1) %>% count(NCB_CA1NA, NCB_CA1CU, NCF1_CA, NCF1_CA_NA1_1, NCF1_CA_NA2_1, NCF1_CACU) %>%
  openxlsx::write.xlsx(., file = "test_rural.xlsx")

rural_raw %>%
  select(RID, matches("NCB_CA[[:digit:]]|NCF1_CA")) %>%
  dplyr::filter(is.na(NCB_CA1) != T ) %>%
  group_by(NCB_CA1) %>% count(NCB_CA1NA, NCF1_CA, NCF1_CA_NA1_1) %>%
  openxlsx::write.xlsx(., file = "rural_cancer.xlsx")


rural_raw %>%
  select(RID, matches("NCB_CA[[:digit:]]|NCF1_CA")) %>%
# 
#   # Baseline에서 암 과거력이 있는 사람들의 암종 파악
#   mutate(NCB_CA1NA =
#            case_when(
#              NCB_CA1NA == "위암" ~ "1",
#              NCB_CA1NA == "간암" ~ "2",
#              NCB_CA1NA == "대장암" ~ "3",
#              NCB_CA1NA == "유방암" ~ "4",
#              NCB_CA1NA == "자궁경부암"|NCB_CA1NA == "경부암" ~ "5",
#              grepl("자궁", NCB_CA1NA) == TRUE  ~ "5",
#              NCB_CA1NA == "폐암" ~ "6",
#              NCB_CA1NA == "갑상선암"|NCB_CA1NA == "갑상선" ~ "7",
#              NCB_CA1NA == "전립선암" ~ "8",
#              NCB_CA1NA == "방광암" ~ "9",
#              grepl("방광", NCB_CA1NA) == TRUE  ~ "9",
#              NCB_CA1NA == "." ~ "11",
#              is.na(NCB_CA1NA) != TRUE ~ "10"
#     )
#   ) %>%
#   group_by(NCB_CA1NA) %>%
#   dplyr::filter(NCB_CA1 == 2) %>%
#   count() %>% arrange(as.numeric(NCB_CA1NA))
  

  # Follow-up에서 새로 추가된, 암 과거력이 있는 사람들의 암종 파악
  dplyr::filter(NCB_CA1 != 2) %>% 
  mutate(NCF1_CA_NA1_1 =
         case_when(
           grepl("위암", NCF1_CA_NA1_1) == TRUE  ~ "1",
           NCF1_CA_NA1_1 == "간암" ~ "2",
           NCF1_CA_NA1_1 == "대장암" ~ "3",
           NCF1_CA_NA1_1 == "유방암" ~ "4",
           NCF1_CA_NA1_1 == "자궁경부암"|NCF1_CA_NA1_1 == "경부암" ~ "5",
           grepl("자궁암|자궁내막암", NCF1_CA_NA1_1) == TRUE  ~ "5",
           NCF1_CA_NA1_1 == "폐암" ~ "6",
           NCF1_CA_NA1_1 == "갑상선암"|NCF1_CA_NA1_1 == "갑상선" ~ "7",
           NCF1_CA_NA1_1 == "전립선암" ~ "8",
           NCF1_CA_NA1_1 == "방광암" ~ "9",
           NCF1_CA_NA1_1 == "." ~ "11",
           is.na(NCF1_CA_NA1_1) != TRUE ~ "10"
         )
  ) %>%
  group_by(NCF1_CA_NA1_1) %>%
  dplyr::filter(NCF1_CA == 2) %>%
  count() %>% arrange(as.numeric(NCF1_CA_NA1_1))
```

```r
urban_raw %>% 
  mutate(BL_cancer = 
           case_when(
             DS1_CA1 == "2" ~ "1",
             DS1_CA1 != "2" ~ "0"
           )
         ) %>% 
  mutate(DS1_milk_FQ = 
           case_when(
             DS1_F084_FQ == "1" ~ 0,
             DS1_F084_FQ == "2" ~ 1/30, # 0.2333/7
             DS1_F084_FQ == "3" ~ 2.5/30, # 0.583333/7
             DS1_F084_FQ == "4" ~ 1.5/7, 
             DS1_F084_FQ == "5" ~ 3.5/7, 
             DS1_F084_FQ == "6" ~ 5.5/7, 
             DS1_F084_FQ == "7" ~ 1, # 7/7
             DS1_F084_FQ == "8" ~ 2, # 14/7
             DS1_F084_FQ == "9" ~ 3 # 21/7
           )
  ) %>%
  mutate(DS1_yo_FQ = 
           case_when(
             DS1_F085_FQ == "1" ~ 0,
             DS1_F085_FQ == "2" ~ 1/30, # 0.2333/7
             DS1_F085_FQ == "3" ~ 2.5/30, # 0.583333/7
             DS1_F085_FQ == "4" ~ 1.5/7, 
             DS1_F085_FQ == "5" ~ 3.5/7, 
             DS1_F085_FQ == "6" ~ 5.5/7, 
             DS1_F085_FQ == "7" ~ 1, # 7/7
             DS1_F085_FQ == "8" ~ 2, # 14/7
             DS1_F085_FQ == "9" ~ 3 # 21/7
           )
  ) %>%
  mutate(DS1_ice_FQ = 
           case_when(
             DS1_F086_FQ == "1" ~ 0,
             DS1_F086_FQ == "2" ~ 1/30, # 0.2333/7
             DS1_F086_FQ == "3" ~ 2.5/30, # 0.583333/7
             DS1_F086_FQ == "4" ~ 1.5/7, 
             DS1_F086_FQ == "5" ~ 3.5/7, 
             DS1_F086_FQ == "6" ~ 5.5/7, 
             DS1_F086_FQ == "7" ~ 1, # 7/7
             DS1_F086_FQ == "8" ~ 2, # 14/7
             DS1_F086_FQ == "9" ~ 3 # 21/7
           )
  ) %>%
  mutate(DS1_cheese_FQ = 
           case_when(
             DS1_F087_FQ == "1" ~ 0,
             DS1_F087_FQ == "2" ~ 1/30, # 0.2333/7
             DS1_F087_FQ == "3" ~ 2.5/30, # 0.583333/7
             DS1_F087_FQ == "4" ~ 1.5/7, 
             DS1_F087_FQ == "5" ~ 3.5/7, 
             DS1_F087_FQ == "6" ~ 5.5/7, 
             DS1_F087_FQ == "7" ~ 1, # 7/7
             DS1_F087_FQ == "8" ~ 2, # 14/7
             DS1_F087_FQ == "9" ~ 3 # 21/7
           )
  ) %>%
  mutate(DS1_soy_FQ = 
           case_when(
             DS1_F088_FQ == "1" ~ 0,
             DS1_F088_FQ == "2" ~ 1/30, # 0.2333/7
             DS1_F088_FQ == "3" ~ 2.5/30, # 0.583333/7
             DS1_F088_FQ == "4" ~ 1.5/7, 
             DS1_F088_FQ == "5" ~ 3.5/7, 
             DS1_F088_FQ == "6" ~ 5.5/7, 
             DS1_F088_FQ == "7" ~ 1, # 7/7
             DS1_F088_FQ == "8" ~ 2, # 14/7
             DS1_F088_FQ == "9" ~ 3 # 21/7
           )
  ) %>%
  mutate(DS1_diary_sum = 
           DS1_milk_FQ + DS1_yo_FQ + DS1_ice_FQ + DS1_cheese_FQ + DS1_soy_FQ) %>% 
  group_by(BL_cancer) %>% 
  select(RID, DS1_diary_sum) %>% 
  summarise(mean = mean(DS1_diary_sum, na.rm=TRUE))
```
