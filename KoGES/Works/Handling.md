
적당한 규모의 KoGES data를 handling할 기회를 얻었다.  
1. 3개의 cohort를 다루고 있는 KoGES data를 merge하기  
2. 각 cohort의 follow-up 기간이 다르므로 indexing으로 구분하기  

SAS dataset이 문제다. sasdata로 불러온 것을 csv로 내보내면 파일이 깨져버린다.  
아마 encoding문제인 것 같은데 두 개의 타입으로 encoding된 dataset이 있는 게 가능한가?

기타 제외하기로 결정  
도시 농촌은 끝냈고 지역이 문제  
Cox 추가할 것  

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

#### Comment about dataset ####
# 이 dataset은 urban_raw를 이용, baseline과 F/U 단계에서 암 발병 정보를 알아보기 위해 만들어졌다. 
# urban_raw의 암 진단명에 있어서 '기타' 수준이 ('중복응답', '판단불가', '암종아님')등을 포함하고 있기 때문에 
# '기타'수준을 갖는 obs를 '암 과거력 없음'으로 정제할 필요가 있었고
# 진단명 1, 2, 3 등으로 복수 진단을 허용하고 있음을 이용, 진단명 1에서는 '기타'이나 진단명 2,3에서 1-9 수준의 값을 갖는다면
# 진단명 1을 진단명 2, 3의 1-9 수준으로 대체하였다. 
# 이 방법은 진단명 1에서 기타인 obs를 최대한 살릴 수 있다는 장점을,
# 복수 진단을 갖고 있는 obs에 대한 정보 손실을 불러온다는 단점을 갖는다. 
# '기타'수준 갖는 obs를 '암 과거력 없음'처리 하게 됐을 때에 오는 손실을 최대한 방지하기 위해 이 방법을 선택하였다. 
#### Comment about dataset ####
#### Urban data set에서 '기타' 수준을 갖는 obs 살리기 ####

urban_raw %>%
  
  # # 암 과거력이 NA이지만 진단명이 있는 사람 : 0
  # # 즉, 암 과거력이 없는 사람 중 진단명이 있는 사람은 없다. 
  # dplyr::filter(DS1_CA1 == "." & DS1_CA1SP != ".")
  
  # # 2개의 암 과거력을 갖는 사람 : 162명
  # dplyr::filter(DS1_CA1 == "2" & DS1_CA2 == "2")
  # dplyr::filter(DS1_CA2 == "2") # 와 결과가 같다.

  # # 3개의 암 과거력을 갖는 사람 : 11명
  # dplyr::filter(DS1_CA1 == "2" & DS1_CA2 == "2" & DS1_CA3 == "2") 
  # dplyr::filter(DS1_CA3 == "2") # 와 결과가 같다.
  
  # # 혹시 몰라서 CA1에서 과거력이 없지만 CA2, CA3에서 과거력을 갖는 사람도 찾아봄
  # # 없음

  # 암 과거력 유무에 대한 column : cancer_BL
  mutate(cancer_BL = 
           case_when(
             # 암 과거력 여부 파악 : CA1, CA2, CA3 
             DS1_CA1 == 1 ~ 0,
             
             # 과거력이 결측치인 경우, 암 과거력이 없다고 정의
             DS1_CA1 == "." ~ 0,
             # 암 진단이 '기타'이거나 결측치인 경우 암 과거력이 없다고 정의
             ## 이것만 주석처리하면 기타와 결측치를 제외하지 않은 결과를 볼 수 있음
             # DS1_CA1SP == 10 | DS1_CA1SP == "." ~ 0,
             
             DS1_CA1 == 2 ~ 1
           )
  ) %>% 
  # 암 진단명에 대한 column : cancer_BL_type
  
  mutate(cancer_BL_type = 
           case_when (
             ## 1) 암과거력이 존재하나 '기타'나 NA를 갖는 관측치인 경우 
             (cancer_BL == 1) & (DS1_CA1SP == "10"| DS1_CA1SP == ".") ~ "10",
             ## 2) 암 과거력이 있으면서 기타나 NA를 갖지 않는 경우
             cancer_BL == 1 & is.na(DS1_CA1SP) != TRUE ~ DS1_CA1SP
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count(cancer_BL_type)
  
  mutate(cancer_BL_type = 
           case_when (
             ## 3) (cancer_BL_type == 10 & DS1_CA2 == 2)일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             (cancer_BL_type == 10 & DS1_CA2 == 2) & (DS1_CA2SP == "10"| DS1_CA2SP == ".") ~ "10",
             ## 4) (cancer_BL_type == 10 & DS1_CA2 == 2)일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             (cancer_BL_type == 10 & DS1_CA2 == 2) & is.na(DS1_CA2SP) != TRUE ~ DS1_CA2SP,
             cancer_BL_type == 10 ~ cancer_BL_type,
             cancer_BL_type != 10 ~ cancer_BL_type
             
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count(cancer_BL_type)
  
  mutate(cancer_BL_type = 
           case_when (
             ## 5) (cancer_BL_type == 10 & DS1_CA3 == 2)일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             (cancer_BL_type == 10 & DS1_CA3 == 2) & (DS1_CA3SP == "10"| DS1_CA3SP == ".") ~ "10",
             ## 6) (cancer_BL_type == 10 & DS1_CA3 == 2)일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             (cancer_BL_type == 10 & DS1_CA3 == 2) & is.na(DS1_CA3SP) != TRUE ~ DS1_CA3SP,
             cancer_BL_type == 10 ~ cancer_BL_type,
             cancer_BL_type != 10 ~ cancer_BL_type
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count(cancer_BL_type)
  
  # cancer_BL_type을 기준으로 cancer_BL 다시 정의
  mutate(cancer_BL = 
           case_when(
             # 암 과거력 여부 파악 : CA1, CA2, CA3 
             cancer_BL_type == 10 | is.na(cancer_BL_type) == TRUE ~ 0,
             
             # 과거력이 결측치인 경우, 암 과거력이 없다고 정의
             is.na(cancer_BL_type) != TRUE ~ 1
           )
  ) %>% 
  # count(cancer_BL)

  # F/U의 암 발생 현황 정리
  ## F/U의 total sample : baseline에서 암 과거력이 없는 사람들
  # dplyr::filter(cancer_BL == 0) %>% 
  
  mutate(cancer_FU1 = 
           case_when(
             cancer_BL == 0 & (DS2_CA1 == 1 | DS2_CA1 == "." | DS2_CA1 == "") ~ "0",
             cancer_BL == 0 & (DS2_CA1 == 2) ~ "1",
             cancer_BL == 1 ~ ""
           )
  ) %>% 
  # group_by(cancer_FU1) %>% count()
  
  mutate(cancer_FU1_type = 
           case_when (
             ## 1) 암 과거력이 존재하나 '기타'나 NA를 갖는 관측치인 경우 
             (cancer_FU1 == 1) & (DS2_CA1SP == "10") ~ "10", 
             (cancer_FU1 == 1) & (DS2_CA1SP == "." | DS2_CA1SP == "") ~ "11",
             ## 2) 암 과거력이 있으면서 기타나 NA를 갖지 않는 경우
             cancer_FU1 == 1 & is.na(DS2_CA1SP) != TRUE ~ DS2_CA1SP
           )
  ) %>% 
  # group_by(cancer_FU1_type) %>% count(cancer_FU1_type)
  
  mutate(cancer_FU1_type = 
           case_when (
             ## 3) (cancer_FU1_type == 10 & DS2_CA2 == 2)일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             (cancer_FU1_type == 10 & DS2_CA2 == 2) & (DS2_CA2SP == "10"| DS2_CA2SP == ".") ~ "10",
             ## 4) (cancer_FU1_type == 10 & DS2_CA2 == 2)일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             (cancer_FU1_type == 10 & DS2_CA2 == 2) & is.na(DS2_CA2SP) != TRUE ~ DS2_CA2SP,
             ## 5) 이미 10으로 정의되었고 위의 경우에서 걸러지지 않았다면 그냥 10이 맞음
             cancer_FU1_type == 10 ~ cancer_FU1_type,
             ## 6) 10이 아닌 모든 진단명은 그대로 내려오기
             cancer_FU1_type != 10 ~ cancer_FU1_type
           )
  ) %>% 
  group_by(cancer_FU1_type) %>% count(cancer_FU1_type)
  # # dataset으로 export
  # write.csv("city_cancer_dataset.csv")

  #### NOTE ####
  # mutate(cancer_BL = 
  #          case_when(
  #            # 암 과거력 여부 파악 : CA1, CA2, CA3 
  #            DS1_CA1 == 1 ~ 0,
  #            DS1_CA1 == 2 ~ 1, 
  #            DS1_CA1 == "." ~ 0,
  #            DS1_CA1SP == 10 | DS1_CA1SP == "." ~ 0,
  #          )
  # ) %>% group_by(cancer_BL) %>% count()
  # 이렇게 선언하면 DS1_CA1SP 구문이 실행되지 않은 결과값으로 나온다.
  # 왜냐면 이미 DS1_CA1 == 2 ~ 1이 실행됐기 때문에 CA1 == 2를 갖는 값 중 CA1SP == 10를 갖는 값이 있다 하더라도 바뀌지 않는다.
  # case_when의 특징인가? 주의해야할 부분인 것 같다. 



#### Urban data set에서 '기타' 수준을 갖는 obs 살리기 ####


#### Comment about dataset ####
# 이 dataset은 urban_raw를 이용, baseline과 F/U 단계에서 암 발병 정보를 알아보기 위해 만들어졌다. 
# 이전의 방법으로 dataset을 만들면 중복 진단의 정보가 모두 사라진다는 단점 떄문에
# 특정 암종을 target으로 하는 경우라면 발생된 정보 손실로 인해 분석의 정확도가 떨어질 수 있다. 
# 따라서 모든 진단명과 횟수를 나타낼 필요가 있어 이 dataset을 만들었다. 
# 또한 '기타'를 갖는 obs의 경우, 위의 방법처럼 진단명 2, 3을 기준으로 1-9 수준의 진단명을 갖는다면 
# 암 과거력을 갖는 사람으로, 기타나 결측치를 갖는다면 과거력을 가지지 않는 사람으로 정의하였다. 
# 이 dataset은 중복 진단을 갖는 obs의 정보를 모두 유지한다는 장점을 가지나
# 중복 진단을 나타내는 변수들로 인해 dataset이 복잡해진다는 단점 또한 가지고 있다. 
#### Comment about dataset ####

#### Urban data set에서 모든 진단 횟수와 암종 나타내기 ####
urban_raw %>%

  mutate(cancer_BL_1 = 
           case_when(
             DS1_CA1 == 2 & DS1_CA1SP == 10 ~ DS1_CA1SP,
             DS1_CA1 == 2 & (DS1_CA1SP == "." |  DS1_CA1SP == "") ~ "11",
             DS1_CA1 == 2 & is.na(DS1_CA1SP) != TRUE ~ DS1_CA1SP, 
             DS1_CA1 != 2 ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_1) %>% count()
  
  mutate(cancer_BL_2 = 
           case_when(
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (DS1_CA2 == 2) & (DS1_CA2SP == 10) ~ DS1_CA2SP,
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (DS1_CA2 == 2) & (DS1_CA2SP == "." |  DS1_CA2SP == "") ~ "11",
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (DS1_CA2 == 2) & is.na(DS1_CA2SP) != TRUE ~ DS1_CA2SP, 
             DS1_CA2 == 2 ~ DS1_CA2SP,
             DS1_CA2 != 2 ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_2) %>% count()
  mutate(cancer_BL_3 = 
           case_when(
             (cancer_BL_2 == 10 | cancer_BL_2 == 11) & (DS1_CA3 == 2) & (DS1_CA3SP == 10) ~ DS1_CA3SP,
             (cancer_BL_2 == 10 | cancer_BL_2 == 11) & (DS1_CA3 == 2) & (DS1_CA3SP == "." |  DS1_CA3SP == "") ~ "11",
             (cancer_BL_2 == 10 | cancer_BL_2 == 11) & (DS1_CA3 == 2) & is.na(DS1_CA3SP) != TRUE ~ DS1_CA3SP, 
             DS1_CA3 == 2 ~ DS1_CA3SP,
             DS1_CA3 != 2 ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_3) %>% count()
  
  # 3개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖는 obs를 빼려면 어떻게 해야 할까? 
  # 무식하게 했다. 
  mutate(cancer_BL = 
           case_when(
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (cancer_BL_2 != 10 & cancer_BL_2 != "Non-case" & cancer_BL_2 != "11") ~ 1, 
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (cancer_BL_3 != 10 & cancer_BL_3 != "Non-case" & cancer_BL_3 != "11") ~ 1, 
             (cancer_BL_2 == 10 | cancer_BL_2 == 11) & (cancer_BL_3 != 10 & cancer_BL_3 != "Non-case" & cancer_BL_3 != "11") ~ 1, 
             
             cancer_BL_1 == "Non-case" ~ 0,
             
             cancer_BL_1 != 10 & cancer_BL_1 != 11~ 1,
             TRUE ~ 0
           )
  ) %>% 
  # group_by(cancer_BL) %>% count()
  
  
  
  mutate(cancer_FU_1 = 
           case_when(
             cancer_BL == 0 & DS2_CA1 == 2 & DS2_CA1SP == 10 ~ DS2_CA1SP,
             cancer_BL == 0 & DS2_CA1 == 2 & (DS2_CA1SP == "." |  DS2_CA1SP == "") ~ "11",
             cancer_BL == 0 & DS2_CA1 == 2 & is.na(DS2_CA1SP) != TRUE ~ DS2_CA1SP, 
             cancer_BL == 0 & DS2_CA1 != 2 ~ "Non-case",
             TRUE ~ "Baseline case"
           )
  ) %>% 
  # group_by(cancer_FU_1) %>% count()
  
  mutate(cancer_FU_2 = 
           case_when(
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (DS2_CA2 == 2) & (DS2_CA2SP == 10) ~ DS2_CA2SP,
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (DS2_CA2 == 2) & (DS2_CA2SP == "." |  DS2_CA2SP == "") ~ "11",
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (DS2_CA2 == 2) & is.na(DS2_CA2SP) != TRUE ~ DS2_CA2SP, 
             DS2_CA2 == 2 ~ DS2_CA2SP,
             DS2_CA2 != 2 ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_FU_2) %>% count()
  
  mutate(cancer_FU = 
           case_when(
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1", 
             
             cancer_FU_1 == "Non-case" ~ "0",
             cancer_FU_1 == "Baseline case" ~ cancer_FU_1,
             
             cancer_FU_1 != 10 & cancer_FU_1 != 11~ "1",
             TRUE ~ "0"
           )
  ) %>% 
  # group_by(cancer_FU) %>% count()
#### Urban data set에서 모든 진단 횟수와 암종 나타내기 ####



#### Rural data set에서 모든 진단 횟수와 암종 나타내기 ####
rural_raw %>% 
  mutate(cancer_BL_1= 
           case_when(
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # grepl("암", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("암", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1, # 단순 결과로 40개의 암종 발견
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             grepl("위암|위장암", NCB_CA1NA) == TRUE | grepl("위암|위장암", NCB_CA_NA1) == TRUE  ~ "1",
             NCB_CA1NA == "간암" | NCB_CA_NA1 == "간암" ~ "2",
             # "대장에 용정제거 후 암세포 발견" 때문에 grepl으로 변경함
             grepl("대장", NCB_CA1NA) == TRUE | grepl("대장", NCB_CA_NA1) == TRUE  ~ "3",
             NCB_CA1NA == "유방암" | NCB_CA_NA1 == "유방암" ~ "4",
             
             # 자궁경부암의 경우가 좀 복잡함 : 총 43명
             ## 자궁경부암 : 33명, 경부암 : 5명
             ## 경부상피암 : 1, 자궁경부상피내암 : 2, 자궁경부이행암 : 1, 자궁상피내암 : 1
             NCB_CA1NA == "자궁경부암"|NCB_CA1NA == "경부암" | NCB_CA_NA1 == "자궁경부암"|NCB_CA_NA1 == "경부암" ~ "5",
             # grepl("경부|상피", NCB_CA1NA) == TRUE | grepl("경부|상피", NCB_CA_NA1) == TRUE  ~ "5",
             NCB_CA1NA == "자궁경부상피내암" | NCB_CA_NA1 == "자궁경부상피내암" ~ "5",
             NCB_CA1NA == "경부상피암" | NCB_CA_NA1 == "경부상피암" ~ "5",
             
             NCB_CA1NA == "자궁경부이행암" | NCB_CA_NA1 == "자궁경부이행암" ~ "5",
             NCB_CA1NA == "자궁상피내암" | NCB_CA_NA1 == "자궁상피내암" ~ "5",
             # Q. 왜 아래의 코드를 이용하면 +2가 아니라 +4가 되는 걸까?
             # grepl("자궁경부|자궁상피", NCB_CA1NA) == TRUE | grepl("자궁경부|자궁상피", NCB_CA_NA1) == TRUE  ~ "5",
             
             NCB_CA1NA == "폐암" | NCB_CA_NA1 == "폐암" ~ "6",
             
             # NCB_CA1NA == "갑상선암" | NCB_CA_NA1 == "갑상선암"~ "7", # 27개
             # grepl("갑상선", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("갑상선", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1, # 16개
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA1NA == "갑상선암"|NCB_CA1NA == "갑상선" | NCB_CA_NA1 == "갑상선암"|NCB_CA_NA1 == "갑상선"~ "7",
             
             # 전립선암 : 8명, 전립선 : 1명. 마찬가지로 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA1NA) == TRUE | grepl("전립선암|전립선", NCB_CA_NA1) == TRUE  ~ "8",
             
             # 방광암 : 7명, 방광 : 3명. 마찬가지로 방광도 방광암으로 간주하고 진행함.
             NCB_CA1NA == "방광암"|NCB_CA1NA =="방광" | NCB_CA_NA1 == "방광암"|NCB_CA_NA1 =="방광" ~ "9",
             
             # grepl("자궁암|자궁내막암", NCB_CA1NA) == TRUE | grepl("자궁암|자궁내막암", NCB_CA_NA1) == TRUE  ~ "10",
             # NCB_CA1NA != "." | NCB_CA_NA1 != "." ~ "10",
             
             # 암종 구분
             # grepl("암", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("암", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1,
             
             
             grepl("암", NCB_CA1NA) == TRUE ~ "10",
             grepl("암", NCB_CA_NA1) == TRUE ~ "10",
             
             NCB_CA1 == "2" & NCB_CA1NA != "." ~ "11",
             NCB_CA == "2" & NCB_CA_NA1 != "." ~ "11",
             
             # NCB_CA1 == "2" & NCB_CA1NA != "." ~ NCB_CA1NA,
             # NCB_CA == "2" & NCB_CA_NA1 != "." ~ NCB_CA_NA1,
             
             NCB_CA1 == "2" & NCB_CA1NA == "." ~ "11",
             NCB_CA == "2" & NCB_CA_NA1 == "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>%
  # group_by(cancer_BL_1) %>% count() %>% as.data.frame()

  mutate(cancer_BL_2= 
           case_when(

             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             grepl("위암|위", NCB_CA2NA) == TRUE | grepl("위암|위", NCB_CA_NA2) == TRUE  ~ "1",
             NCB_CA2NA == "간암" | NCB_CA_NA2 == "간암" ~ "2",
             
             grepl("대장", NCB_CA2NA) == TRUE | grepl("대장", NCB_CA_NA2) == TRUE  ~ "3",
             grepl("유방|유방암", NCB_CA2NA) == TRUE | grepl("유방|유방암", NCB_CA_NA2) == TRUE  ~ "4",
             
             grepl("경부|자궁경부암", NCB_CA2NA) == TRUE | grepl("경부|자궁경부암", NCB_CA_NA2) == TRUE  ~ "5",
             
             NCB_CA2NA == "폐암" | NCB_CA_NA2 == "폐암" ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA2NA == "갑상선암"|NCB_CA2NA == "갑상선" | NCB_CA_NA2 == "갑상선암"|NCB_CA_NA2 == "갑상선"~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA2NA) == TRUE | grepl("전립선암|전립선", NCB_CA_NA2) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA2NA == "방광암"|NCB_CA2NA =="방광" | NCB_CA_NA2 == "방광암"|NCB_CA_NA2 =="방광" ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA2NA) == TRUE ~ NCB_CA2NA,
             # grepl("암", NCB_CA_NA2) == TRUE ~ NCB_CA_NA2,
             
             NCB_CA2 == "2" & NCB_CA2NA != "." ~ "10",
             NCB_CA == "2" & NCB_CA_NA2 != "." ~ "10",
             NCB_CA2 == "2" & NCB_CA2NA == "." ~ "11",
             # NCB_CA == "2" & NCB_CA_NA2 == "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_2) %>% count() %>% as.data.frame()

  mutate(cancer_BL_3= 
           case_when(
             
             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             ## NCB_CA_NA3은 존재하지 않으므로 제외함 
             
             grepl("위암", NCB_CA3NA) == TRUE  ~ "1",
             NCB_CA3NA == "간암" ~ "2",
             
             grepl("대장|대장암", NCB_CA3NA) == TRUE  ~ "3",
             grepl("유방|유방암", NCB_CA3NA) ~ "4",
             
             NCB_CA3NA == "자궁경부암"|NCB_CA3NA == "경부암" ~ "5",
             
             NCB_CA3NA == "자궁경부상피내암" ~ "5",
             NCB_CA3NA == "경부상피암" ~ "5",
             
             NCB_CA3NA == "자궁경부이행암" ~ "5",
             NCB_CA3NA == "자궁상피내암"  ~ "5",
             
             NCB_CA3NA == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA3NA == "갑상선암"|NCB_CA3NA == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA3NA) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA3NA == "방광암"|NCB_CA3NA =="방광"  ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA3NA) == TRUE ~ NCB_CA3NA,
             
             NCB_CA3 == "2" & NCB_CA3NA != "." ~ "10",
             NCB_CA3 == "2" & NCB_CA3NA == "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_3) %>% count() %>% as.data.frame()
  
  mutate(cancer_BL = 
           case_when(
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (cancer_BL_2 != 10 & cancer_BL_2 != "Non-case" & cancer_BL_2 != "11") ~ 1, 
             (cancer_BL_1 == 10 | cancer_BL_1 == 11) & (cancer_BL_3 != 10 & cancer_BL_3 != "Non-case" & cancer_BL_3 != "11") ~ 1, 
             (cancer_BL_2 == 10 | cancer_BL_2 == 11) & (cancer_BL_3 != 10 & cancer_BL_3 != "Non-case" & cancer_BL_3 != "11") ~ 1, 
             
             cancer_BL_1 == "Non-case" ~ 0,
             
             cancer_BL_1 != 10 & cancer_BL_1 != 11~ 1,
             TRUE ~ 0
           )
  ) %>% 
  # group_by(cancer_BL) %>% count()
  
  # 1차 F/U
  mutate(cancer_FU_1 = 
           case_when(
             # 암종 확인
             # cancer_BL == 0 & NCF1_CA_NA1_1 != "." ~ NCF1_CA_NA1_1,
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 == "." ~ "11",
             
             
             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_BL == 0 & grepl("위암", NCF1_CA_NA1_1) == TRUE  ~ "1",
             cancer_BL == 0 & NCF1_CA_NA1_1 == "간암" ~ "2",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA1_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("유방$|유방암", NCF1_CA_NA1_1) ~ "4",
             
             cancer_BL == 0 & grepl("자궁경부$|경부암", NCF1_CA_NA1_1) ~ "5",
             
             cancer_BL == 0 & NCF1_CA_NA1_1 == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_BL == 0 & NCF1_CA_NA1_1 == "갑상선암"|NCF1_CA_NA1_1 == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA1_1) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             cancer_BL == 0 & NCF1_CA_NA1_1 == "방광암"|NCF1_CA_NA1_1 =="방광"  ~ "9",
             
             cancer_BL == 0 & NCF1_CA == "2" & grepl("암", NCF1_CA_NA1_1) ~ "10",
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             cancer_BL == 1 ~ "Baseline case"
           )
  ) %>% 
  # group_by(cancer_FU_1) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU_2 = 
           case_when(
             # 암종 확인 : 단 두 개
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ NCF1_CA_NA2_1, 
             # cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA2_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA2_1) == TRUE  ~ "8",
             
             cancer_BL == 0 & NCF1_CA_NA2_1 == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             
             cancer_BL == 1 ~ "Baseline case"
             
           )
  ) %>% 
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU = 
           case_when(
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1", 
             
             cancer_FU_1 == "Non-case" ~ "0",
             cancer_FU_1 == "Baseline case" ~ cancer_FU_1,
             
             cancer_FU_1 != 10 & cancer_FU_1 != 11 ~ "1",
             TRUE ~ "0"
           )
  ) %>% 
  group_by(cancer_FU) %>% count()
#### Rural data set에서 모든 진단 횟수와 암종 나타내기 ####  
  
#### Rural data set에서 '기타' 수준을 갖는 obs 살리기 ####
rural_raw %>% 
  mutate(cancer_BL_1= 
           case_when(
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # grepl("암", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("암", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1, # 단순 결과로 40개의 암종 발견
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             grepl("위암|위장암", NCB_CA1NA) == TRUE | grepl("위암|위장암", NCB_CA_NA1) == TRUE  ~ "1",
             NCB_CA1NA == "간암" | NCB_CA_NA1 == "간암" ~ "2",
             # "대장에 용정제거 후 암세포 발견" 때문에 grepl으로 변경함
             grepl("대장", NCB_CA1NA) == TRUE | grepl("대장", NCB_CA_NA1) == TRUE  ~ "3",
             NCB_CA1NA == "유방암" | NCB_CA_NA1 == "유방암" ~ "4",
             
             # 자궁경부암의 경우가 좀 복잡함 : 총 43명
             ## 자궁경부암 : 33명, 경부암 : 5명
             ## 경부상피암 : 1, 자궁경부상피내암 : 2, 자궁경부이행암 : 1, 자궁상피내암 : 1
             NCB_CA1NA == "자궁경부암"|NCB_CA1NA == "경부암" | NCB_CA_NA1 == "자궁경부암"|NCB_CA_NA1 == "경부암" ~ "5",
             # grepl("경부|상피", NCB_CA1NA) == TRUE | grepl("경부|상피", NCB_CA_NA1) == TRUE  ~ "5",
             NCB_CA1NA == "자궁경부상피내암" | NCB_CA_NA1 == "자궁경부상피내암" ~ "5",
             NCB_CA1NA == "경부상피암" | NCB_CA_NA1 == "경부상피암" ~ "5",
             
             NCB_CA1NA == "자궁경부이행암" | NCB_CA_NA1 == "자궁경부이행암" ~ "5",
             NCB_CA1NA == "자궁상피내암" | NCB_CA_NA1 == "자궁상피내암" ~ "5",
             # Q. 왜 아래의 코드를 이용하면 +2가 아니라 +4가 되는 걸까?
             # grepl("자궁경부|자궁상피", NCB_CA1NA) == TRUE | grepl("자궁경부|자궁상피", NCB_CA_NA1) == TRUE  ~ "5",
             
             NCB_CA1NA == "폐암" | NCB_CA_NA1 == "폐암" ~ "6",
             
             # NCB_CA1NA == "갑상선암" | NCB_CA_NA1 == "갑상선암"~ "7", # 27개
             # grepl("갑상선", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("갑상선", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1, # 16개
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA1NA == "갑상선암"|NCB_CA1NA == "갑상선" | NCB_CA_NA1 == "갑상선암"|NCB_CA_NA1 == "갑상선"~ "7",
             
             # 전립선암 : 8명, 전립선 : 1명. 마찬가지로 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA1NA) == TRUE | grepl("전립선암|전립선", NCB_CA_NA1) == TRUE  ~ "8",
             
             # 방광암 : 7명, 방광 : 3명. 마찬가지로 방광도 방광암으로 간주하고 진행함.
             NCB_CA1NA == "방광암"|NCB_CA1NA =="방광" | NCB_CA_NA1 == "방광암"|NCB_CA_NA1 =="방광" ~ "9",
             
             # grepl("자궁암|자궁내막암", NCB_CA1NA) == TRUE | grepl("자궁암|자궁내막암", NCB_CA_NA1) == TRUE  ~ "10",
             # NCB_CA1NA != "." | NCB_CA_NA1 != "." ~ "10",
             
             # 암종 구분
             # grepl("암", NCB_CA1NA) == TRUE ~ NCB_CA1NA,
             # grepl("암", NCB_CA_NA1) == TRUE ~ NCB_CA_NA1,
             
             # NCB_CA1 == "2" & NCB_CA1NA != "." ~ "10",
             # NCB_CA == "2" & NCB_CA_NA1 != "." ~ "10",
             
             grepl("암", NCB_CA1NA) == TRUE ~ "10",
             grepl("암", NCB_CA_NA1) == TRUE ~ "10",
             
             NCB_CA1 == "2" & NCB_CA1NA == "." ~ "11",
             NCB_CA == "2" & NCB_CA_NA1 == "." ~ "11",
             NCB_CA1 == "2" & NCB_CA1NA != "." ~ "11",
             NCB_CA == "2" & NCB_CA_NA1 != "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>%
  # group_by(cancer_BL_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_BL_2= 
           case_when(
             
             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             grepl("위암|위", NCB_CA2NA) == TRUE | grepl("위암|위", NCB_CA_NA2) == TRUE  ~ "1",
             NCB_CA2NA == "간암" | NCB_CA_NA2 == "간암" ~ "2",
             
             grepl("대장", NCB_CA2NA) == TRUE | grepl("대장", NCB_CA_NA2) == TRUE  ~ "3",
             grepl("유방|유방암", NCB_CA2NA) == TRUE | grepl("유방|유방암", NCB_CA_NA2) == TRUE  ~ "4",
             
             grepl("경부|자궁경부암", NCB_CA2NA) == TRUE | grepl("경부|자궁경부암", NCB_CA_NA2) == TRUE  ~ "5",
             
             NCB_CA2NA == "폐암" | NCB_CA_NA2 == "폐암" ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA2NA == "갑상선암"|NCB_CA2NA == "갑상선" | NCB_CA_NA2 == "갑상선암"|NCB_CA_NA2 == "갑상선"~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA2NA) == TRUE | grepl("전립선암|전립선", NCB_CA_NA2) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA2NA == "방광암"|NCB_CA2NA =="방광" | NCB_CA_NA2 == "방광암"|NCB_CA_NA2 =="방광" ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA2NA) == TRUE ~ NCB_CA2NA,
             # grepl("암", NCB_CA_NA2) == TRUE ~ NCB_CA_NA2,
             
             NCB_CA2 == "2" & NCB_CA2NA != "." ~ "10",
             NCB_CA == "2" & NCB_CA_NA2 != "." ~ "10",
             NCB_CA2 == "2" & NCB_CA2NA == "." ~ "11",
             # NCB_CA == "2" & NCB_CA_NA2 == "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_2) %>% count() %>% as.data.frame()
  
  mutate(cancer_BL_3= 
           case_when(
             
             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             ## NCB_CA_NA3은 존재하지 않으므로 제외함 
             
             grepl("위암", NCB_CA3NA) == TRUE  ~ "1",
             NCB_CA3NA == "간암" ~ "2",
             
             grepl("대장|대장암", NCB_CA3NA) == TRUE  ~ "3",
             grepl("유방|유방암", NCB_CA3NA) ~ "4",
             
             NCB_CA3NA == "자궁경부암"|NCB_CA3NA == "경부암" ~ "5",
             
             NCB_CA3NA == "자궁경부상피내암" ~ "5",
             NCB_CA3NA == "경부상피암" ~ "5",
             
             NCB_CA3NA == "자궁경부이행암" ~ "5",
             NCB_CA3NA == "자궁상피내암"  ~ "5",
             
             NCB_CA3NA == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA3NA == "갑상선암"|NCB_CA3NA == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA3NA) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA3NA == "방광암"|NCB_CA3NA =="방광"  ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA3NA) == TRUE ~ NCB_CA3NA,
             
             NCB_CA3 == "2" & NCB_CA3NA != "." ~ "11",
             NCB_CA3 == "2" & NCB_CA3NA == "." ~ "11",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_3) %>% count() %>% as.data.frame()
    
  mutate(cancer_BL_type = 
           case_when (
             ## 1) 암과거력이 존재하나 '기타'나 NA를 갖는 관측치인 경우 
             (NCB_CA1 == "2" | NCB_CA == "2") & (cancer_BL_1 == "10"| cancer_BL_1 == "11") ~ "10",
             ## 2) 암 과거력이 있으면서 기타나 NA를 갖지 않는 경우
             (NCB_CA1 == "2" | NCB_CA == "2") & is.na(cancer_BL_1) != TRUE ~ cancer_BL_1
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count()
  
  mutate(cancer_BL_type = 
           case_when (
             ## 3) (cancer_BL_type == 10 & (NCB_CA2 == "2" | NCB_CA == "2"))일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             (cancer_BL_type == 10 & (NCB_CA2 == "2" | NCB_CA == "2")) & (cancer_BL_2 == "10"| cancer_BL_2 == "11") ~ "10",
             ## 4) (cancer_BL_type == 10 & (NCB_CA2 == "2" | NCB_CA == "2"))일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             ## Non-case는 NCB_CA == "2"지만 2차 진단명을 갖지 않는 경우임.
             ## 발생하는 이유는 NCB_CA와 NCB_CA[1-3]의 중복 진단명 수준이 다르기 때문
             ## NCB_CA : 진단 여부 + NA1, NA2로 진단명 물음
             ## NCB_CA[1:3] : 각 진단 여부 + NA[1:3] 각 진단명 물음
             (cancer_BL_type == 10 & (NCB_CA2 == "2" | NCB_CA == "2")) & is.na(cancer_BL_2) != TRUE ~ cancer_BL_2,
             
             # 아래 두 코드를 제외한다면 이 단계에서 추가되는 obs만 볼 수 있음
             cancer_BL_type == 10 ~ cancer_BL_type,
             cancer_BL_type != 10 ~ cancer_BL_type
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count(cancer_BL_type)
  
  mutate(cancer_BL_type = 
           case_when (
             ## 5) cancer_BL_type == 10 & NCB_CA3 == "2"일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             cancer_BL_type == 10 & NCB_CA3 == "2" & (cancer_BL_3 == "10"| cancer_BL_3 == "11") ~ "10",
             ## 6) (cancer_BL_type == 10 & DS1_CA3 == 2)일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             cancer_BL_type == 10 & NCB_CA3 == "2" & is.na(cancer_BL_3) != TRUE ~ cancer_BL_3,
             
             # 아래 두 코드를 제외한다면 이 단계에서 추가되는 obs만 볼 수 있음
             cancer_BL_type == 10 ~ cancer_BL_type,
             cancer_BL_type != 10 ~ cancer_BL_type
           )
  ) %>% 
  # group_by(cancer_BL_type) %>% count(cancer_BL_type)
  
  # cancer_BL_type을 기준으로 cancer_BL 다시 정의
  mutate(cancer_BL = 
           case_when(
             # 암 과거력 여부 파악 : BL_type이 '기타'이거나 '결측치'인 경우나 암 과거력이 없는 경우는 모두 0  
             cancer_BL_type == 10 | cancer_BL_type == "Non-case" | is.na(cancer_BL_type) == TRUE ~ 0,
             
             # 위의 경우를 제외한 모든 경우 : 암 과거력이 존재하며 암 유형이 1-9 수준으로 정의될 때 1
             is.na(cancer_BL_type) != TRUE ~ 1
           )
  ) %>% 
  # count(cancer_BL)

  # 1차 F/U
  mutate(cancer_FU_1 = 
           case_when(
             # 암종 확인
             # cancer_BL == 0 & NCF1_CA_NA1_1 != "." ~ NCF1_CA_NA1_1,
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 == "." ~ "11",
             
             
             # 1) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_BL == 0 & grepl("위암", NCF1_CA_NA1_1) == TRUE  ~ "1",
             cancer_BL == 0 & NCF1_CA_NA1_1 == "간암" ~ "2",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA1_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("유방$|유방암", NCF1_CA_NA1_1) ~ "4",
             
             cancer_BL == 0 & grepl("자궁경부$|경부암", NCF1_CA_NA1_1) ~ "5",
             
             cancer_BL == 0 & NCF1_CA_NA1_1 == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_BL == 0 & NCF1_CA_NA1_1 == "갑상선암"|NCF1_CA_NA1_1 == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA1_1) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             cancer_BL == 0 & NCF1_CA_NA1_1 == "방광암"|NCF1_CA_NA1_1 =="방광"  ~ "9",
             
             cancer_BL == 0 & NCF1_CA == "2" & grepl("암", NCF1_CA_NA1_1) ~ "10",
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             cancer_BL == 1 ~ "Baseline case"
           )
  ) %>% 
  # group_by(cancer_FU_1) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU_2 = 
           case_when(
             # 암종 확인 : 단 두 개
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ NCF1_CA_NA2_1, 
             # cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA2_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA2_1) == TRUE  ~ "8",
             
             cancer_BL == 0 & NCF1_CA_NA2_1 == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             
             cancer_BL == 1 ~ "Baseline case"
             
           )
  ) %>% 
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU_type = 
           case_when (
             ## 1) 암과거력이 존재하나 '기타'나 NA를 갖는 관측치인 경우 
             NCF1_CA == "2" & (cancer_FU_1 == "10"| cancer_FU_1 == "11") ~ "10",
             ## 2) 암 과거력이 있으면서 기타나 NA를 갖지 않는 경우
             NCF1_CA == "2" & is.na(cancer_FU_1) != TRUE ~ cancer_FU_1,
             TRUE ~ cancer_FU_1
           )
  ) %>% 
  # group_by(cancer_FU_type) %>% count()
  
  mutate(cancer_FU_type = 
           case_when (
             ## 3) (cancer_FU_type == 10 & NCF1_CA == "2")일 때, 기타나 NA를 갖는 관측치인 경우, type을 10으로 고정
             (cancer_FU_type == 10 & NCF1_CA == "2") & (cancer_FU_2 == "10"| cancer_FU_2 == "11") ~ "10",
             ## 4) (cancer_FU_type == 10 & NCF1_CA == "2")일 때, 1~9의 관측치를 갖는 경우, 1~9의 값으로 type을 변경 
             (cancer_FU_type == 10 & NCF1_CA == "2") & is.na(cancer_FU_2) != TRUE ~ cancer_FU_2, 
             
             ## 모두 Non-case
             ## 이 경우는 FU_1에서 '10'을 갖는 obs 중 FU_2 = [1:10]를 갖지 않는 경우임
             
             # 아래 두 코드를 제외한다면 이 단계에서 추가되는 obs만 볼 수 있음
             cancer_FU_type == 10 ~ cancer_FU_type,
             cancer_FU_type != 10 ~ cancer_FU_type
           )
  ) %>% 
  # group_by(cancer_FU_type) %>% count(cancer_FU_type)
  
  mutate(cancer_FU = 
           case_when(
             (cancer_FU_1 == 10 | cancer_FU_1 == 11) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1", 
             
             cancer_FU_1 == "Non-case" ~ "0",
             cancer_FU_1 == "Baseline case" ~ cancer_FU_1,
             
             cancer_FU_1 != 10 & cancer_FU_1 != 11 ~ "1",
             TRUE ~ "0"
           )
  ) %>% 
  group_by(cancer_FU) %>% count()

#### Rural data set에서 '기타' 수준을 갖는 obs 살리기 ####
```

```r
FQ_scoring <- function(x, na.rm = FALSE) {
  ifelse(x == ".", NA, 
         ifelse( x == "1", 0, 
                 ifelse( x == "2", 1*7/30, 
                         ifelse ( x == "3", 2.5*7/30, 
                                  ifelse(x == "4", 1.5, 
                                         ifelse(x == "5", 3.5, 
                                                ifelse(x == "6", 5.5, 
                                                       ifelse(x == "7", 7, 
                                                              ifelse(x == "8", 14, 
                                                                     ifelse(x == "9", 21, NA)
                                                              )
                                                       )
                                                )
                                         )
                                  )
                         )
                 )
         )
  )
}
AM_scoring <- function(x, na.rm = FALSE) {
  ifelse(x == ".", NA, 
         ifelse( x == "1", 0.5, 
                 ifelse( x == "2", 1, 
                         ifelse ( x == "3", 1.5, NA)
                 )
         )
  )
}

freq_barplot <- function(data, target) {
  apply(data[, target], 2, table) %>% 
    as.data.frame() %>% 
    rowid_to_column() %>% 
    mutate(rowid = c("NA", paste0(seq(1, 9, 1)))) %>% 
    gather("key", "value", -rowid) %>% 
    ggplot(aes(x = factor(rowid), y = value, fill = factor(rowid))) +
    geom_bar(stat = "identity") + 
    scale_fill_viridis_d() + 
    geom_text(aes(label = sprintf("%d", value), y= value), vjust = 0.25, hjust = -0.05) + 
    coord_flip() +
    facet_wrap(. ~ key, ncol = 1) -> result
  
  return(result)
}


target <- c("DS1_F084_FQ", "DS1_F085_FQ", "DS1_F086_FQ", "DS1_F087_FQ")
freq_barplot(urban_raw, target)


target <- c("NCB_F084_FQ", "NCB_F085_FQ", "NCB_F086_FQ", "NCB_F087_FQ")
freq_barplot(rural_raw, target)


```

```r 
#### meat ####
scoring <- function(x, na.rm = FALSE) {
  ifelse(x == ".", NA, 
         ifelse( x == "1", 0, 
                 ifelse( x == "2", 1/30, 
                         ifelse ( x == "3", 2.5/30, 
                                  ifelse(x == "4", 1.5/7, 
                                         ifelse(x == "5", 3.5/7, 
                                                ifelse(x == "6", 5.5/7, 
                                                       ifelse(x == "7", 1, 
                                                              ifelse(x == "8", 2, 
                                                                     ifelse(x == "9", 3, 1000)
                                                                     )
                                                              )
                                                       )
                                                )
                                  )
                         )
                 )
         )
  )
}

red_meat <- paste0("DS1_F0", c(57, 58, 59, 61, 62, 63), "_FQ")
processed_meat <- "DS1_F060_FQ"
white_meat <- "DS1_F064_FQ"
fish_white <- c("DS1_F067_FQ", "DS1_F069_FQ", "DS1_F071_FQ", "DS1_F072_FQ", "DS1_F081_FQ")
fish_red <- c("DS1_F068_FQ", "DS1_F070_FQ", "DS1_F074_FQ", "DS1_F075_FQ")

urban_raw %>% 
  mutate_at(red_meat, scoring) %>% 
  mutate_at(processed_meat, scoring) %>% 
  mutate_at(white_meat, scoring) %>% 
  mutate_at(fish_white, scoring) %>%
  mutate_at(fish_red, scoring) %>% 
  
  as_tibble() %>% replace(is.na(.), 0) %>% 
  
  mutate(RED_meat =  rowSums(.[red_meat])/length(red_meat)) %>%
  mutate(PROCESSED_meat =  rowSums(.[processed_meat])/length(processed_meat)) %>% 
  mutate(WHITE_meat =  rowSums(.[white_meat])/length(white_meat)) %>% 
  mutate(FISH_white =  rowSums(.[fish_white])/length(fish_white)) %>% 
  mutate(FISH_red =  rowSums(.[fish_red])/length(fish_red)) %>% 
  
  # select(RID, red_meat, RED_meat, processed_meat, PROCESSED_meat, white_meat, WHITE_meat,
  #        fish_white, FISH_white, fish_red, FISH_red)
  
  select(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red) %>% 
  
  # summarise_all(list(min = min, max = max, mean = mean, sd = sd, 
  #                    Q1 = ~ quantile(x = ., prob = 0.25), 
  #                    Q2 = ~ quantile(x = ., prob = 0.50), 
  #                    Q3 = ~ quantile(x = ., prob = 0.75))) %>% 
  # t() %>% 
  # write.xlsx("food_distribution.xlsx")
  pivot_longer(., cols = c(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red), 
               names_to = "Var", values_to = "Val") %>% 
  ggplot(aes(x = Var, y = log(Val+0.0001), fill = Var)) + 
  geom_boxplot() + labs(x="Food categoires", y="log(score mean)") 
ggsave("city_food_box.jpg", dpi = 300)





red_meat <- paste0("NCB_F0", c(57, 58, 59, 61, 62, 63), "_FQ")
processed_meat <- "NCB_F060_FQ"
white_meat <- "NCB_F064_FQ"
fish_white <- c("NCB_F067_FQ", "NCB_F069_FQ", "NCB_F071_FQ", "NCB_F072_FQ", "NCB_F081_FQ")
fish_red <- c("NCB_F068_FQ", "NCB_F070_FQ", "NCB_F074_FQ", "NCB_F075_FQ")

rural_raw %>% 
  mutate_at(red_meat, scoring) %>% 
  mutate_at(processed_meat, scoring) %>% 
  mutate_at(white_meat, scoring) %>% 
  mutate_at(fish_white, scoring) %>%
  mutate_at(fish_red, scoring) %>% 
  
  as_tibble() %>% replace(is.na(.), 0) %>% 
  
  mutate(RED_meat =  rowSums(.[red_meat])/length(red_meat)) %>%
  mutate(PROCESSED_meat =  rowSums(.[processed_meat])/length(processed_meat)) %>% 
  mutate(WHITE_meat =  rowSums(.[white_meat])/length(white_meat)) %>% 
  mutate(FISH_white =  rowSums(.[fish_white])/length(fish_white)) %>% 
  mutate(FISH_red =  rowSums(.[fish_red])/length(fish_red)) %>% 
  
  # select(RID, red_meat, RED_meat, processed_meat, PROCESSED_meat, white_meat, WHITE_meat,
  #        fish_white, FISH_white, fish_red, FISH_red)
  
  select(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red) %>% 
  
  # summarise_all(list(min = min, max = max, mean = mean, sd = sd, 
  #                    Q1 = ~ quantile(x = ., prob = 0.25), 
  #                    Q2 = ~ quantile(x = ., prob = 0.50), 
  #                    Q3 = ~ quantile(x = ., prob = 0.75))) %>% 
  # t() %>% 
  # write.xlsx("food_distribution.xlsx")
  pivot_longer(., cols = c(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red), 
               names_to = "Var", values_to = "Val") %>% 
  ggplot(aes(x = Var, y = log(Val+0.0001), fill = Var)) + 
  geom_boxplot() + labs(x="Food categoires", y="log(score mean)")
ggsave("rural_food_box.jpg", dpi = 300)



red_meat <- c("AS1_DOG_1", "AS1_PORK_1", "AS1_POK3_1", "AS1_BUPO_1", "AS1_BEEF_1", "AS1_SPBF_1", "AS1_NEJA_1")
processed_meat <- "AS1_HAM_1"
white_meat <- "AS1_CHIC_1"
fish_white <- c("AS1_FRFH_1", "AS1_GALF_1", "AS1_JOGI_1", "AS1_TAEF_1", "AS1_UMUK_1")
fish_red <- c("AS1_JANF_1", "AS1_BLFH_1", "AS1_ANCH_1", "AS1_CHAF_1")

local_raw %>% 
  mutate_at(red_meat, scoring) %>% 
  mutate_at(processed_meat, scoring) %>% 
  mutate_at(white_meat, scoring) %>% 
  mutate_at(fish_white, scoring) %>%
  mutate_at(fish_red, scoring) %>% 
  
  as_tibble() %>% replace(is.na(.), 0) %>% 
  
  mutate(RED_meat =  rowSums(.[red_meat])/length(red_meat)) %>%
  mutate(PROCESSED_meat =  rowSums(.[processed_meat])/length(processed_meat)) %>% 
  mutate(WHITE_meat =  rowSums(.[white_meat])/length(white_meat)) %>% 
  mutate(FISH_white =  rowSums(.[fish_white])/length(fish_white)) %>% 
  mutate(FISH_red =  rowSums(.[fish_red])/length(fish_red)) %>% 
  
  # select(RID, red_meat, RED_meat, processed_meat, PROCESSED_meat, white_meat, WHITE_meat,
  #        fish_white, FISH_white, fish_red, FISH_red)
  
  select(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red) %>% 
  
  # summarise_all(list(min = min, max = max, mean = mean, sd = sd, 
  #                    Q1 = ~ quantile(x = ., prob = 0.25), 
  #                    Q2 = ~ quantile(x = ., prob = 0.50), 
  #                    Q3 = ~ quantile(x = ., prob = 0.75))) %>% 
  # t() %>% 
  # write.xlsx("food_distribution.xlsx")
  # select(RED_meat) %>% # table()
  # ggplot(aes(x = "RED_meat", y = log(RED_meat))) + geom_boxplot()
  
  
  pivot_longer(., cols = c(RED_meat, PROCESSED_meat, WHITE_meat, FISH_white, FISH_red), 
               names_to = "Var", values_to = "Val") %>% 
  ggplot(aes(x = Var, y = log(Val+0.0001), fill = Var)) + 
  geom_boxplot() + labs(x="Food categoires", y="log(score mean)")
ggsave("local_food_box.jpg", dpi = 300)

```





