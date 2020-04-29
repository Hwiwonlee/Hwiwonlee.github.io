
기타 제외하기로 결정  
cox는 SAS로 돌릴 예정  
돌리는 중  
Baseline의 ffq를 기준으로 시행  
subtype의 frequency로 추가 진행  
Dairy + vita D + Ca  
Compound 선별 작업 중  

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
             
             ## 0406 : 자궁경부암과 상피내암은 구분하는 게 맞다. -> 빼야지 뭐.
             # NCB_CA1NA == "자궁경부상피내암" | NCB_CA_NA1 == "자궁경부상피내암" ~ "5",
             # NCB_CA1NA == "경부상피암" | NCB_CA_NA1 == "경부상피암" ~ "5",
             # 
             # NCB_CA1NA == "자궁경부이행암" | NCB_CA_NA1 == "자궁경부이행암" ~ "5",
             # NCB_CA1NA == "자궁상피내암" | NCB_CA_NA1 == "자궁상피내암" ~ "5",
             
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
             
             NCB_CA1 == "2" & NCB_CA1NA == "." ~ "12",
             NCB_CA == "2" & NCB_CA_NA1 == "." ~ "12",
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
             
             # grepl("암", NCB_CA2NA) == TRUE ~ "10",
             # grepl("암", NCB_CA_NA2) == TRUE ~ "10",
             
             NCB_CA2 == "2" & NCB_CA2NA != "." ~ "10",
             NCB_CA == "2" & NCB_CA_NA2 != "." ~ "10", 
             # 10 : 8이지만 10 : 2, 11 : 6이다. 
             # NCB_CA2NA에서 기타 암종으로 2개를 찾을 수 있고
             # NCB_CA_NA2가 모두 NA라 6개의 결측치를 갖는다. 
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
             
             # NCB_CA3NA == "자궁경부상피내암" ~ "5",
             # NCB_CA3NA == "경부상피암" ~ "5",
             
             # NCB_CA3NA == "자궁경부이행암" ~ "5",
             # NCB_CA3NA == "자궁상피내암"  ~ "5",
             
             NCB_CA3NA == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA3NA == "갑상선암"|NCB_CA3NA == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA3NA) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA3NA == "방광암"|NCB_CA3NA =="방광"  ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA3NA) == TRUE ~ NCB_CA3NA,
             # TRUE ~ NCB_CA3NA # 췌장 1
             
             NCB_CA3 == "2" & NCB_CA3NA != "." ~ "10",
             NCB_CA3 == "2" & NCB_CA3NA == "." ~ "12",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_3) %>% count() %>% as.data.frame()
  
  # select(cancer_BL_1, cancer_BL_2) %>%
  # mutate(cancer_BL_1 = as.numeric(str_replace(cancer_BL_1, "Non-case", "0"))) %>%
  # mutate(cancer_BL_2 = as.numeric(str_replace(cancer_BL_2, "Non-case", "0"))) %>%
  # table() %>% write.csv("rural_table_1_2.csv")

  # select(cancer_BL_1, cancer_BL_3) %>% 
  # mutate(cancer_BL_1 = as.numeric(str_replace(cancer_BL_1, "Non-case", "0"))) %>% 
  # mutate(cancer_BL_3 = as.numeric(str_replace(cancer_BL_3, "Non-case", "0"))) %>% 
  # table() %>% write.csv("rural_table_1_3.csv")
  
    
  mutate(cancer_BL = 
           case_when(
             
             cancer_BL_1 == "Non-case" ~ 0,
             
             # 3개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             (cancer_BL_1 == 10 | cancer_BL_1 == 11 | cancer_BL_1 == 12) & (cancer_BL_2 != 10 & cancer_BL_2 != "11" & cancer_BL_2 != "Non-case") ~ 1, 
             (cancer_BL_1 == 10 | cancer_BL_1 == 11 | cancer_BL_1 == 12) & (cancer_BL_3 != 10 & cancer_BL_3 != "11" & cancer_BL_3 != "Non-case") ~ 1, 
             
             # 3개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 != 11 & cancer_BL_1 != 12 ~ 1,
             cancer_BL_2 != 11 & cancer_BL_2 != 12 ~ 1,
             cancer_BL_3 != 11 & cancer_BL_3 != 12 ~ 1,
             # TRUE ~ 99
           )
  ) %>% 
  # dplyr::filter(cancer_BL == 99) %>% select(cancer_BL_1, cancer_BL_2, cancer_BL_3)
  # group_by(cancer_BL) %>% count()
  
  
  # 1차 F/U
  mutate(cancer_FU_1 = 
           case_when(
             # 암종 확인
             # cancer_BL == 0 & NCF1_CA_NA1_1 != "." ~ NCF1_CA_NA1_1,
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 == "." ~ "12",
             
             
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
             cancer_BL == 1 ~ "Baseline case",
             cancer_BL == 3 ~ "Exclude case"
           )
  ) %>% 
  # group_by(cancer_FU_1) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU_2 = 
           case_when(
             # 암종 확인 : 단 두 개
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ NCF1_CA_NA2_1, 
             # cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 != "." ~ "11",
             
             
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 == "." ~ "12",
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 == "" ~ "12",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA2_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA2_1) == TRUE  ~ "8",
             
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "." ~ "Non-case",
             
             cancer_BL == 0 & NCF1_CA_NA2_1 != "" ~ "11",
             cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             
             cancer_BL == 1 ~ "Baseline case",
             cancer_BL == 3 ~ "Exclude case"
             
           )
  ) %>% 
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  # # F/U에서 교차표 그려보기 (0407)
  # dplyr::filter(cancer_BL == 0 & NCF1_CA == 2) %>%
  # select(cancer_FU_1, cancer_FU_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()
  
  mutate(cancer_FU = 
           case_when(
             cancer_FU_1 == "Non-case" ~ "0",
             cancer_FU_1 == "Baseline case" ~ cancer_FU_1,
             cancer_FU_1 == "Exclude case" ~ cancer_FU_1,
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1", 
             
             # 2개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             cancer_FU_1 == 11 & cancer_FU_2 == 11 ~ "3",
             cancer_FU_1 == 11 & cancer_FU_2 == 12 ~ "3",
             cancer_FU_1 == 11 & cancer_FU_2 == "Non-case" ~ "3",
             
             cancer_FU_1 == 12 & cancer_FU_2 == 11 ~ "3",
             cancer_FU_1 == 12 & cancer_FU_2 == 12 ~ "3",
             cancer_FU_1 == 12 & cancer_FU_2 == "Non-case" ~ "3",
             
             cancer_FU_1 != 11 & cancer_FU_1 != 12 ~ "1",
             cancer_FU_2 != 11 & cancer_FU_2 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # dplyr::filter(cancer_FU == "99") %>% select(cancer_FU_1, cancer_FU_2)
  
  
  # select(RID, cancer_BL, cancer_BL_1, cancer_BL_2, cancer_BL_3, cancer_FU_1, cancer_FU_2, cancer_FU) %>% 
  # write.csv("rural_cancer_data.csv")
  
  # enery 제외
  # dplyr::filter(NCB_SEX == 1 & (NCB_SS01 > 800 & NCB_SS01 < 4200) | 
  #                 NCB_SEX == 2 & (NCB_SS01 > 500 & NCB_SS01 < 3500)) %>% 
  
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  # select(cancer_FU_1, cancer_FU_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

    
  group_by(cancer_FU) %>% count() %>% as.data.frame()

#### Rural data set에서 모든 진단 횟수와 암종 나타내기 #### 


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
             
             ## 0406 : 자궁경부암과 상피내암은 구분하는 게 맞다. -> 빼야지 뭐.
             # NCB_CA1NA == "자궁경부상피내암" | NCB_CA_NA1 == "자궁경부상피내암" ~ "5",
             # NCB_CA1NA == "경부상피암" | NCB_CA_NA1 == "경부상피암" ~ "5",
             # 
             # NCB_CA1NA == "자궁경부이행암" | NCB_CA_NA1 == "자궁경부이행암" ~ "5",
             # NCB_CA1NA == "자궁상피내암" | NCB_CA_NA1 == "자궁상피내암" ~ "5",
             
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
             
             NCB_CA1 == "2" & NCB_CA1NA == "." ~ "12",
             NCB_CA == "2" & NCB_CA_NA1 == "." ~ "12",
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
             
             # grepl("암", NCB_CA2NA) == TRUE ~ "10",
             # grepl("암", NCB_CA_NA2) == TRUE ~ "10",
             
             NCB_CA2 == "2" & NCB_CA2NA != "." ~ "10",
             NCB_CA == "2" & NCB_CA_NA2 != "." ~ "10", 
             # 10 : 8이지만 10 : 2, 11 : 6이다. 
             # NCB_CA2NA에서 기타 암종으로 2개를 찾을 수 있고
             # NCB_CA_NA2가 모두 NA라 6개의 결측치를 갖는다. 
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
             
             # NCB_CA3NA == "자궁경부상피내암" ~ "5",
             # NCB_CA3NA == "경부상피암" ~ "5",
             
             # NCB_CA3NA == "자궁경부이행암" ~ "5",
             # NCB_CA3NA == "자궁상피내암"  ~ "5",
             
             NCB_CA3NA == "폐암"  ~ "6",
             
             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             NCB_CA3NA == "갑상선암"|NCB_CA3NA == "갑상선" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선", NCB_CA3NA) == TRUE  ~ "8",
             
             # 방광도 방광암으로 간주하고 진행함.
             NCB_CA3NA == "방광암"|NCB_CA3NA =="방광"  ~ "9",
             
             # 암종 구분
             # grepl("암", NCB_CA3NA) == TRUE ~ NCB_CA3NA,
             # TRUE ~ NCB_CA3NA # 췌장 1
             
             NCB_CA3 == "2" & NCB_CA3NA != "." ~ "10",
             NCB_CA3 == "2" & NCB_CA3NA == "." ~ "12",
             TRUE ~ "Non-case"
           )
  ) %>% 
  # group_by(cancer_BL_3) %>% count() %>% as.data.frame()
  
  # select(cancer_BL_1, cancer_BL_2) %>%
  # mutate(cancer_BL_1 = as.numeric(str_replace(cancer_BL_1, "Non-case", "0"))) %>%
  # mutate(cancer_BL_2 = as.numeric(str_replace(cancer_BL_2, "Non-case", "0"))) %>%
  # table() %>% write.csv("rural_table_1_2.csv")

  # select(cancer_BL_1, cancer_BL_3) %>% 
  # mutate(cancer_BL_1 = as.numeric(str_replace(cancer_BL_1, "Non-case", "0"))) %>% 
  # mutate(cancer_BL_3 = as.numeric(str_replace(cancer_BL_3, "Non-case", "0"))) %>% 
  # table() %>% write.csv("rural_table_1_3.csv")
  
    
  mutate(cancer_BL = 
           case_when(
             
             cancer_BL_1 == "Non-case" ~ 0,
             
             # 3개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             (cancer_BL_1 == 10 | cancer_BL_1 == 11 | cancer_BL_1 == 12) & (cancer_BL_2 != 10 & cancer_BL_2 != "11" & cancer_BL_2 != "Non-case") ~ 1, 
             (cancer_BL_1 == 10 | cancer_BL_1 == 11 | cancer_BL_1 == 12) & (cancer_BL_3 != 10 & cancer_BL_3 != "11" & cancer_BL_3 != "Non-case") ~ 1, 
             
             # 3개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 11 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == 12 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 11 & cancer_BL_2 == "Non-case" & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 11 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == 12 & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 11  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == 12  ~ 3,
             cancer_BL_1 == 12 & cancer_BL_2 == "Non-case" & cancer_BL_3 == "Non-case"  ~ 3,
             
             cancer_BL_1 != 11 & cancer_BL_1 != 12 ~ 1,
             cancer_BL_2 != 11 & cancer_BL_2 != 12 ~ 1,
             cancer_BL_3 != 11 & cancer_BL_3 != 12 ~ 1,
             # TRUE ~ 99
           )
  ) %>% 
  # dplyr::filter(cancer_BL == 99) %>% select(cancer_BL_1, cancer_BL_2, cancer_BL_3)
  # group_by(cancer_BL) %>% count()
  
  
  # 1차 F/U
  mutate(cancer_FU_1 = 
           case_when(
             # 암종 확인
             # cancer_BL == 0 & NCF1_CA_NA1_1 != "." ~ NCF1_CA_NA1_1,
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA1_1 == "." ~ "12",
             
             
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
             cancer_BL == 1 ~ "Baseline case",
             cancer_BL == 3 ~ "Exclude case"
           )
  ) %>% 
  # group_by(cancer_FU_1) %>% count() %>%  as.data.frame()
  
  mutate(cancer_FU_2 = 
           case_when(
             # 암종 확인 : 단 두 개
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ NCF1_CA_NA2_1, 
             # cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 != "." ~ "11",
             
             
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 == "." ~ "12",
             cancer_BL == 0 & NCF1_CA == "2" & NCF1_CA_NA2_1 == "" ~ "12",
             
             cancer_BL == 0 & grepl("대장|대장암", NCF1_CA_NA2_1) == TRUE  ~ "3",
             cancer_BL == 0 & grepl("전립선암|전립선", NCF1_CA_NA2_1) == TRUE  ~ "8",
             
             # cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA_NA2_1 == "." ~ "Non-case",
             
             cancer_BL == 0 & NCF1_CA_NA2_1 != "" ~ "11",
             cancer_BL == 0 & NCF1_CA_NA2_1 != "." ~ "11",
             
             cancer_BL == 0 & NCF1_CA == "1" ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "." ~ "Non-case",
             cancer_BL == 0 & NCF1_CA == "" ~ "Non-case",
             
             cancer_BL == 1 ~ "Baseline case",
             cancer_BL == 3 ~ "Exclude case"
             
           )
  ) %>% 
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  # # F/U에서 교차표 그려보기 (0407)
  # dplyr::filter(cancer_BL == 0 & NCF1_CA == 2) %>%
  # select(cancer_FU_1, cancer_FU_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()
  
  mutate(cancer_FU = 
           case_when(
             cancer_FU_1 == "Non-case" ~ "0",
             cancer_FU_1 == "Baseline case" ~ cancer_FU_1,
             cancer_FU_1 == "Exclude case" ~ cancer_FU_1,
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "Non-case" & cancer_FU_2 != "11") ~ "1", 
             
             # 2개의 진단명에서 10, 11을 갖는 obs 중 한번이라도 1-9를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             cancer_FU_1 == 11 & cancer_FU_2 == 11 ~ "3",
             cancer_FU_1 == 11 & cancer_FU_2 == 12 ~ "3",
             cancer_FU_1 == 11 & cancer_FU_2 == "Non-case" ~ "3",
             
             cancer_FU_1 == 12 & cancer_FU_2 == 11 ~ "3",
             cancer_FU_1 == 12 & cancer_FU_2 == 12 ~ "3",
             cancer_FU_1 == 12 & cancer_FU_2 == "Non-case" ~ "3",
             
             cancer_FU_1 != 11 & cancer_FU_1 != 12 ~ "1",
             cancer_FU_2 != 11 & cancer_FU_2 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # dplyr::filter(cancer_FU == "99") %>% select(cancer_FU_1, cancer_FU_2)
  
  
  # select(RID, cancer_BL, cancer_BL_1, cancer_BL_2, cancer_BL_3, cancer_FU_1, cancer_FU_2, cancer_FU) %>% 
  # write.csv("rural_cancer_data.csv")
  
  # enery 제외
  # dplyr::filter(NCB_SEX == 1 & (NCB_SS01 > 800 & NCB_SS01 < 4200) | 
  #                 NCB_SEX == 2 & (NCB_SS01 > 500 & NCB_SS01 < 3500)) %>% 
  
  # group_by(cancer_FU_2) %>% count() %>%  as.data.frame()
  
  # select(cancer_FU_1, cancer_FU_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

    
  group_by(cancer_FU) %>% count() %>% as.data.frame()

#### Rural data set에서 모든 진단 횟수와 암종 나타내기 #### 
 

#### local dataset에서 모든 진단 횟수와 암종 나타내기 ####
local_raw %>% 
  mutate_all(
    funs(
      case_when(
        (. == 99999 | . == 66666 | . == 77777 | is.na(.) == TRUE) ~ ".",
        TRUE ~ as.character(.)
      )
    )
  ) %>% 
  ## Base line에서 기타 질환에 암종을 갖고 있는 사람 체크
  # dplyr::filter(grepl("암", AS1_PDOTH1NA) == TRUE) %>%
  # select(RID, AS1_PDTOTCA1NA, AS1_PDOTH1NA)
  
  mutate(AS1_PDTOTCA1NA = 
           case_when(
             # AS1_PDOTH1NA : 기타 질환
             # AS1_PDTOTCA1NA : 각종 종양 1
             
             # 기타 질환에 '암'이 있고 각종 종양에 '암'이 없으면 기타 질환의 암으로 값을 대체
             grepl("암", AS1_PDOTH1NA) == TRUE & grepl("암", AS1_PDTOTCA1NA) != TRUE ~ AS1_PDOTH1NA,
             
             # 기타 질환에 '암'이 있고 각종 종양에 '암'이 있으면 각종 종양의 값으로 유지
             grepl("암", AS1_PDOTH1NA) == TRUE & grepl("암", AS1_PDTOTCA1NA) == TRUE ~ AS1_PDTOTCA1NA,
             
             # 나머지는 각종 종양의 값으로 그대로 유지 
             TRUE ~ AS1_PDTOTCA1NA
           )
  ) %>% 
  # # 바뀐 내용 체크 
  ## 체크 완료
  # dplyr::filter(grepl("암", AS1_PDOTH1NA) == TRUE) %>%
  # select(RID, AS1_PDTOTCA1NA, AS1_PDOTH1NA)
  
  mutate(cancer_BL_1= 
           case_when(
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # grepl("암", AS1_PDTOTCA1NA) == TRUE ~ AS1_PDTOTCA1NA, # 13개 종의 암이 있는 것으로 확인 
             # is.na(AS1_PDTOTCA1NA) != TRUE ~ AS1_PDTOTCA1NA
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암

             grepl("위암|위장암", AS1_PDTOTCA1NA) == TRUE  ~ "1",
             grepl("위$", AS1_PDTOTCA1NA) == TRUE  ~ "1",
             AS1_PDTOTCA1NA == "간암" ~ "2",
             # "대장에 용정제거 후 암세포 발견" 때문에 grepl으로 변경함
             grepl("대장$|대장암", AS1_PDTOTCA1NA) == TRUE ~ "3",
             AS1_PDTOTCA1NA == "유방암" ~ "4",

             grepl("경부암|자궁경부암", AS1_PDTOTCA1NA) == TRUE ~ "5",

             grepl("폐$|폐암", AS1_PDTOTCA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             AS1_PDTOTCA1NA == "갑상선암"| AS1_PDTOTCA1NA == "갑상선" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             grepl("전립선암|전립선$", AS1_PDTOTCA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             grepl("방광암|방광$", AS1_PDTOTCA1NA) == TRUE ~ "9",

             # 암종 구분
             # grepl("암", AS1_PDTOTCA1NA) == TRUE ~ AS1_PDTOTCA1NA
             # TRUE ~ AS1_PDTOTCA1NA

             # 1-9에 포함되지 않지만 '암'이면 10
             grepl("암", AS1_PDTOTCA1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             AS1_PDTOTCA1 == "2" & AS1_PDTOTCA1NA != "." ~ "11",
             
             # 암이 있다고 대답했으나 진단명이 없으면 12 
             AS1_PDTOTCA1 == "2" & AS1_PDTOTCA1NA == "." ~ "12",
             
             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code 
             AS1_PDTOTCA1 == "2" & AS1_PDTOTCA1NA != "." ~ AS1_PDTOTCA1NA,
             TRUE ~ "Non-case"
           )
  ) %>%
  # check를 위한 filter and select : cancer_BL_1 == 11 or 12가 정말 제대로 들어갔나?
  # 제대로 들어감 
  # dplyr::filter(cancer_BL_1 == 11 | cancer_BL_1 == 12) %>%
  # select(RID, cancer_BL_1, AS1_PDTOTCA1NA) %>% as.data.frame()
  
  # group_by(cancer_BL_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_BL = 
           case_when(
             cancer_BL_1 == "Non-case" ~ 0, # 암 환자가 아닌 경우
             cancer_BL_1 == 10 ~ 1, # '기타' 종류의 암 환자인 경우 
             cancer_BL_1 == 11 | cancer_BL_1 == 12 ~ 3, # 암이 아닌 다른 종양의 환자이거나 진단명이 결측치인 경우
             cancer_BL_1 != 11 & cancer_BL_1 != 12 ~ 1 # 암이 아닌 다른 종양의 환자도 아니고 진단명이 결측치가 아닌 경우
             # TRUE ~ 99
           )
  ) %>% 
  # group_by(cancer_BL) %>% count() %>% as.data.frame()
  
  ### 1차 F/U
  # local_raw의 1차 F/U는 모든 악성 종양 진단명이 누락되어 있음
  # AS2_PDTOTCA1NA, AS2_PDTOTCA2NA, AS2_PDTOTCA3NA
  # AS2_PDFTOTCA1NA, AS2_PDFTOTCA2NA, AS2_PDFTOTCA3NA
  
  # select(AS2_PDTOTCA1NA, AS2_PDTOTCA2NA, AS2_PDTOTCA3NA, AS2_PDFTOTCA1NA, AS2_PDFTOTCA2NA, AS2_PDFTOTCA3NA) %>% 
  # table() # 확인 완료 
  
  # 04.16 기준 dataset 다시 만들어서 채워넣음
  
  # 안성의 기타 질환 중 '암'이 존재한다면 종양 진단명에 채워넣기
  # Q. AS2_PDTOTCA3NA인 이유?
  # A. 단 하나의 관측치에서만 암종이 존재하고 이 관측치가 기타 질환을 갖지 않기 때문 (EPI17_009_2_195761, 피부암)
  # 위의 내용을 확인, 확인 함 
  # dplyr::filter(grepl("암", AS2_PDTOTCA3NA) == TRUE) %>% 
  # select(RID, AS2_PDTOTCA3NA, AS2_PDOTH1NA)

  # 기타 질환에서 '암'을 갖는 사람이 각종 종양 1에서는 어떤 값을 갖는지 확인
  # 어? 똑같네? 
  # dplyr::filter(grepl("암", AS2_PDOTH1NA) == TRUE) %>%
  # select(RID, AS2_PDTOTCA1NA, AS2_PDOTH1NA)

  mutate(
    AS2_PDTOTCA3NA = 
           case_when(
             # AS2_PDOTH1NA : 기타 질환
             # AS2_PDTOTCA2NA : 각종 종양 1
             
             # 기타 질환에 '암'이 있고 각종 종양1에 '암'이 없으면 기타 질환의 암으로 각종 종양3의 값을 대체
             grepl("암", AS2_PDOTH1NA) == TRUE & grepl("암", AS2_PDTOTCA1NA) != TRUE ~ AS2_PDOTH1NA,
             
             # 기타 질환에 '암'이 있고 각종 종양1에 '암'이 있으면 각종 종양3의 값으로 유지
             grepl("암", AS2_PDOTH1NA) == TRUE & grepl("암", AS2_PDTOTCA1NA) == TRUE ~ AS2_PDTOTCA3NA,
             
             # 나머지는 각종 종양의 값으로 그대로 유지 
             TRUE ~ AS2_PDTOTCA3NA
           )
  ) %>% 
    
  ## 바뀐 내용 체크 
  ## 체크 완료
  # dplyr::filter(grepl("암", AS2_PDOTH1NA) == TRUE) %>%
  # select(RID, AS2_PDTOTCA1NA, AS2_PDTOTCA2NA, AS2_PDTOTCA3NA, AS2_PDOTH1NA)

  
      
  # 안산의 기타 질환 중 '암'이 존재한다면 종양 진단명에 채워넣기
  # 안산의 AS2_PDFOTH1~3NA는 단 하나의 '암' 관측값도 갖지 않아 채워넣을 필요가 없음
  # dplyr::filter(grepl("암", AS2_PDFOTH1NA) == TRUE) # 없음
  # dplyr::filter(grepl("암", AS2_PDFOTH2NA) == TRUE) # 없음
  # dplyr::filter(grepl("암", AS2_PDFOTH3NA) == TRUE) # 없음
  
  
  # IMPORTANT
  # 2개의 지역 각각 진단 이력과 진단명을 갖는 것을 하나의 column으로 합쳐야 뒤에 코드가 제대로 돌아감
  # AS2_PDTOTCA1~3, AS2_PDTOTCA1~3NA에 합쳐보자. 
  
  # count(AS2_PDTOTCA1)

  # AS2_PDTOTCA1~3가 .이면 AS2_PDFTOTCA1~3로 대체하라. 
  # .이 아니면? 1 혹은 2의 값을 갖고 있는 것이고 이 경우에 AS2_PDFTOTCA는 "."이다. 
  mutate(AS2_PDTOTCA1 = 
           case_when(
             AS2_PDTOTCA1 == "." ~ AS2_PDFTOTCA1,
             AS2_PDTOTCA1 != "." ~ AS2_PDTOTCA1
           )
  ) %>% 
  
  mutate(AS2_PDTOTCA2 = 
           case_when(
             AS2_PDTOTCA2 == "." ~ AS2_PDFTOTCA2,
             AS2_PDTOTCA2 != "." ~ AS2_PDTOTCA2
           )
  ) %>% 
  mutate(AS2_PDTOTCA3 = 
           case_when(
             AS2_PDTOTCA3 == "." ~ AS2_PDFTOTCA3,
             AS2_PDTOTCA3 != "." ~ AS2_PDTOTCA3
           )
  ) %>% 
  
  # AS2_PDTOTCA1~3NA가 .이면 AS2_PDFTOTCA1~3NA로 대체하라. 
  # .이 아니면? 진단명을 갖고 있는 것이고 이 경우에 AS2_PDFTOTCANA는 "."이다. 
  
  mutate(AS2_PDTOTCA1NA = 
           case_when(
             AS2_PDTOTCA1NA == "." ~ AS2_PDFTOTCA1NA,
             AS2_PDTOTCA1NA != "." ~ AS2_PDTOTCA1NA
           )
  ) %>% 
  mutate(AS2_PDTOTCA2NA = 
           case_when(
             AS2_PDTOTCA2NA == "." ~ AS2_PDFTOTCA2NA,
             AS2_PDTOTCA2NA != "." ~ AS2_PDTOTCA2NA
           )
  ) %>% 
  mutate(AS2_PDTOTCA3NA = 
           case_when(
             AS2_PDTOTCA3NA == "." ~ AS2_PDFTOTCA3NA,
             AS2_PDTOTCA3NA != "." ~ AS2_PDTOTCA3NA
           )
  ) %>% 

  mutate(cancer_FU1_1= 
           case_when(
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 13개 종으로 보임
             # cancer_BL == 0 & grepl("암", AS2_PDTOTCA1NA) == TRUE ~ AS2_PDTOTCA1NA,
             # 
             # cancer_BL == 0 & is.na(AS2_PDTOTCA1NA) != TRUE ~ AS2_PDTOTCA1NA,
             # 
             # TRUE ~ as.character(cancer_BL)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암

             cancer_BL == 0 & grepl("위암|위장암", AS2_PDTOTCA1NA) == TRUE  ~ "1",

             cancer_BL == 0 & AS2_PDTOTCA1NA == "간암" ~ "2",

             cancer_BL == 0 & grepl("대장$|대장암", AS2_PDTOTCA1NA) == TRUE ~ "3",

             cancer_BL == 0 & AS2_PDTOTCA1NA == "유방암" ~ "4",

             cancer_BL == 0 & grepl("경부암|자궁경부암", AS2_PDTOTCA1NA) == TRUE ~ "5",

             # 폐암의심 때문에 $ 추가
             cancer_BL == 0 & grepl("폐$|폐암$", AS2_PDTOTCA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_BL == 0 & AS2_PDTOTCA1NA == "갑상선암"| AS2_PDTOTCA1NA == "갑상선" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_BL == 0 & grepl("전립선암|전립선$", AS2_PDTOTCA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_BL == 0 & grepl("방광암|방광$", AS2_PDTOTCA1NA) == TRUE ~ "9",

             # 암종 구분
             # grepl("암", AS2_PDTOTCA1NA) == TRUE ~ AS2_PDTOTCA1NA,
             # 
             # TRUE ~ AS2_PDTOTCA1NA


             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_BL == 0 & grepl("암", AS2_PDTOTCA1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_BL == 0 & AS2_PDTOTCA1 == "2" & AS2_PDTOTCA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_BL == 0 & AS2_PDTOTCA1 == "2" & AS2_PDTOTCA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_BL == 0 & AS2_PDTOTCA1 == "2" & TRUE ~ AS2_PDTOTCA1NA,
             
             # 여전히 암에 걸리지 않은 사람들
             cancer_BL == 0 & AS2_PDTOTCA1 == "1"  ~ "0",
             cancer_BL == 0 & AS2_PDTOTCA1 == "."  ~ "0",
             
             # 기반조사에서 이미 암 과거력이 존재하는 사람들
             cancer_BL == 1 ~ "Baseline case",
             
             # 기반조사에서 암 진단에서 결측값을 갖거나 암이 아닌 다른 종양을 갖고 있다고 응답한 사람들
             cancer_BL == 3 ~ "Exclude case", 
             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU1_1) %>% count() %>% as.data.frame()
  
  
  mutate(cancer_FU1_2= 
           case_when(
             ## 1) 몇 종류의 암종이 있는지 먼저 파악
             ## 1개 종
             # cancer_BL == 0 & grepl("암", AS2_PDTOTCA2NA) == TRUE ~ AS2_PDTOTCA2NA,
             # 
             # cancer_BL == 0 & is.na(AS2_PDTOTCA2NA) != TRUE ~ AS2_PDTOTCA2NA,
             # 
             # TRUE ~ as.character(cancer_BL)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_BL == 0 & grepl("위암|위장암", AS2_PDTOTCA2NA) == TRUE  ~ "1",

             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_BL == 0 & grepl("암", AS2_PDTOTCA2NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_BL == 0 & AS2_PDTOTCA2 == "2" & AS2_PDTOTCA2NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_BL == 0 & AS2_PDTOTCA2 == "2" & AS2_PDTOTCA2NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_BL == 0 & AS2_PDTOTCA2 == "2" & TRUE ~ AS2_PDTOTCA2NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_BL == 0 & AS2_PDTOTCA2 == "1"  ~ "0",
             cancer_BL == 0 & AS2_PDTOTCA2 == "."  ~ "0",

             # 기반조사에서 이미 암 과거력이 존재하는 사람들
             cancer_BL == 1 ~ "Baseline case",

             # 기반조사에서 암 진단에서 결측값을 갖거나 암이 아닌 다른 종양을 갖고 있다고 응답한 사람들
             cancer_BL == 3 ~ "Exclude case",
             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU1_2) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU1_3= 
           case_when(
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 암종 없음 
             # cancer_BL == 0 & grepl("암", AS2_PDTOTCA3NA) == TRUE ~ AS2_PDTOTCA3NA,
             # 
             # cancer_BL == 0 & is.na(AS2_PDTOTCA3NA) != TRUE ~ AS2_PDTOTCA3NA,
             # 
             # TRUE ~ as.character(cancer_BL)
             
             
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_BL == 0 & grepl("암", AS2_PDTOTCA3NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_BL == 0 & AS2_PDTOTCA3 == "2" & AS2_PDTOTCA3NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_BL == 0 & AS2_PDTOTCA3 == "2" & AS2_PDTOTCA3NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_BL == 0 & AS2_PDTOTCA3 == "2" & TRUE ~ AS2_PDTOTCA3NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_BL == 0 & AS2_PDTOTCA3 == "1"  ~ "0",
             cancer_BL == 0 & AS2_PDTOTCA3 == "."  ~ "0",

             # 기반조사에서 이미 암 과거력이 존재하는 사람들
             cancer_BL == 1 ~ "Baseline case",

             # 기반조사에서 암 진단에서 결측값을 갖거나 암이 아닌 다른 종양을 갖고 있다고 응답한 사람들
             cancer_BL == 3 ~ "Exclude case",
             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU1_3) %>% count() %>% as.data.frame()
  
  # cancer_FU1_3을 갖는 관측치는 딱 하나. 이 관측치의 다른 진단명 여부를 알아보자. 
  # 모두 11, 11, 11, 그럼 어차피 cancer_FU1 == "11"이 된다. 
  # dplyr::filter(cancer_FU1_3 == "11") %>% 
  # select(RID, cancer_FU1_1, cancer_FU1_2, cancer_FU1_3)
  
  # # F/U에서 교차표 그려보기 (0416)
  # 아, cancer_FU_2, _3이 Non-case로 되어 있어서 table이 이상하게 뜨는 거임
  # Non-case 아닌 친구들만 table위로 뜸
  # 위의 암에 걸리지 않은 사람들을 "0"으로 수정함 (04.17)
  # dplyr::filter(cancer_BL == 0) %>%
  # select(cancer_FU1_1, cancer_FU1_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()
  
  mutate(cancer_FU1 = 
           case_when(
             # cancer_FU1_1 == "0" ~ "0",
             cancer_FU1_1 == "Baseline case" ~ cancer_FU1_1,
             cancer_FU1_1 == "Exclude case" ~ cancer_FU1_1,
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU1_1 == 11 & cancer_FU1_2 == 11 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == 11 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == 11 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == 11 & cancer_FU1_2 == 12 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == 12 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == 12 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == 11 & cancer_FU1_2 == "0" & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == "0" & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 11 & cancer_FU1_2 == "0" & cancer_FU1_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU1_1 == 12 & cancer_FU1_2 == 11 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == 11 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == 11 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == 12 & cancer_FU1_2 == 12 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == 12 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == 12 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == 12 & cancer_FU1_2 == "0" & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == "0" & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == 12 & cancer_FU1_2 == "0" & cancer_FU1_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU1_1 == "0" & cancer_FU1_2 == 11 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == "0" & cancer_FU1_2 == 11 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == "0" & cancer_FU1_2 == 11 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == "0" & cancer_FU1_2 == 12 & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == "0" & cancer_FU1_2 == 12 & cancer_FU1_3 == 12 ~ "3",
             cancer_FU1_1 == "0" & cancer_FU1_2 == 12 & cancer_FU1_3 == "0" ~ "3",
             
             cancer_FU1_1 == "0" & cancer_FU1_2 == "0" & cancer_FU1_3 == 11 ~ "3",
             cancer_FU1_1 == "0" & cancer_FU1_2 == "0" & cancer_FU1_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU1_1 == "0" & cancer_FU1_2 == "0" & cancer_FU1_3 == "0" ~ "0",
             
             
             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             cancer_FU1_1 != 11 & cancer_FU1_1 != 12 ~ "1",
             cancer_FU1_2 != 11 & cancer_FU1_2 != 12 ~ "1",
             cancer_FU1_3 != 11 & cancer_FU1_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # group_by(cancer_FU1) %>% count() %>% as.data.frame()
  
  
  
  # 2차 F/U 시작
  ## 2차 F/U부터는 위암, 간암, 대장암, 유방암, 폐암, 췌장암, 자궁암이 각각 한 문항씩 갖고 있고 기타종양 1, 기타종양 2의 문항도 존재함. 
  ## 그럼, _1는 위암부터 자궁암까지 값이 있는지, _2는 기타종양 1, _3은 기타종양 2에 대해 정리하면 되지 않을까? 
  
  mutate(cancer_FU2_1= 
           case_when(
             # 이전 내용 정리 
             cancer_FU1 == "Baseline case" ~ cancer_FU1,
             cancer_FU1 == "Exclude case" ~ cancer_FU1, 
             cancer_FU1 == "1" ~ "1st F/U case", 
             cancer_FU1 == "3" ~ "1st F/U Exclude case", 
             
             # 1. 위암
             cancer_FU1 == 0 & AS3_PDFGCA == 2 ~ "1",
             
             # 2. 간암
             cancer_FU1 == 0 & AS3_PDFHCA == 2 ~ "2",
             
             # 3. 대장암
             cancer_FU1 == 0 & AS3_PDFCOLCA == 2 ~ "3",
             
             # 4. 유방암
             cancer_FU1 == 0 & AS3_PDFBRCA == 2 ~ "4",
             
             # 6. 폐암
             cancer_FU1 == 0 & AS3_PDFGCA == 2 ~ "6",
             
             # 10. 췌장암
             cancer_FU1 == 0 & AS3_PDFPACA == 2 ~ "10",
             
             # 10. 자궁암
             cancer_FU1 == 0 & AS3_PDFUTCA == 2 ~ "10",
             
             # FU1에서 넘어온 total N이지만 일단 남은 사람들
             cancer_FU1 == 0 ~ "0"
           )
  ) %>%
  # group_by(cancer_FU2_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU2_2= 
           case_when(
             # 이전 내용 정리 
             cancer_FU1 == "Baseline case" ~ cancer_FU1,
             cancer_FU1 == "Exclude case" ~ cancer_FU1, 
             cancer_FU1 == "1" ~ "1st F/U case", 
             cancer_FU1 == "3" ~ "1st F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 8개 종으로 보임
             # cancer_FU1 == 0 & grepl("암", AS3_PDFCA1NA) == TRUE ~ AS3_PDFCA1NA,
             # 
             # cancer_FU1 == 0 & is.na(AS3_PDFCA1NA) != TRUE ~ AS3_PDFCA1NA,
             # 
             # TRUE ~ as.character(cancer_FU1)


             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암

             cancer_FU1 == 0 & grepl("위암|위장암", AS3_PDFCA1NA) == TRUE  ~ "1",

             cancer_FU1 == 0 & AS3_PDFCA1NA == "간암" ~ "2",

             cancer_FU1 == 0 & grepl("대장$|대장암", AS3_PDFCA1NA) == TRUE ~ "3",

             cancer_FU1 == 0 & AS3_PDFCA1NA == "유방암" ~ "4",

             cancer_FU1 == 0 & grepl("경부암|자궁경부암", AS3_PDFCA1NA) == TRUE ~ "5",

             cancer_FU1 == 0 & grepl("폐암", AS3_PDFCA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_FU1 == 0 & AS3_PDFCA1NA == "갑상선암"| AS3_PDFCA1NA == "갑상선" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_FU1 == 0 & grepl("전립선암|전립선$", AS3_PDFCA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_FU1 == 0 & grepl("방광암|방광$", AS3_PDFCA1NA) == TRUE ~ "9",

             # 암종 구분
             # grepl("암", AS3_PDFCA1NA) == TRUE ~ AS3_PDFCA1NA,
             #
             # TRUE ~ AS3_PDFCA1NA
             #
             #
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU1 == 0 & grepl("암", AS3_PDFCA1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU1 == 0 & AS3_PDFCA1 == "2" & AS3_PDFCA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU1 == 0 & AS3_PDFCA1 == "2" & AS3_PDFCA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU1 == 0 & AS3_PDFCA1 == "2" & TRUE ~ AS3_PDFCA1NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU1 == 0 & AS3_PDFCA1 == "1"  ~ "0",
             cancer_FU1 == 0 & AS3_PDFCA1 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU2_2) %>% count() %>% as.data.frame()

  
  
  mutate(cancer_FU2_3= 
         case_when(
           # 이전 내용 정리 
           cancer_FU1 == "Baseline case" ~ cancer_FU1,
           cancer_FU1 == "Exclude case" ~ cancer_FU1, 
           cancer_FU1 == "1" ~ "1st F/U case", 
           cancer_FU1 == "3" ~ "1st F/U Exclude case", 
           
           
           # 1) 몇 종류의 암종이 있는지 먼저 파악
           # 위 용종 하나
           # 그럼, cancer_FU2_3이 '위용종'인 관측치가 다른 cancer_FU2_는 어떤 값을 갖는지 확인하자.
           # 확인해서 이미 "11"이나 "12"의 값을 갖는다면 굳이 넣지 않아도 됨
           # cancer_FU1 == 0 & grepl("암", AS3_PDFCA2NA) == TRUE ~ AS3_PDFCA2NA,
           # 
           # cancer_FU1 == 0 & is.na(AS3_PDFCA2NA) != TRUE ~ AS3_PDFCA2NA,
           # 
           # TRUE ~ as.character(cancer_FU1)
           
           
           # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
           ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암

           # 1-9에 포함되지 않지만 '암'이면 10
           cancer_FU1 == 0 & grepl("암", AS3_PDFCA2NA) == TRUE ~ "10",

           # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
           cancer_FU1 == 0 & AS3_PDFCA2 == "2" & AS3_PDFCA2NA != "." ~ "11",

           # 암이 있다고 대답했으나 진단명이 없으면 12
           cancer_FU1 == 0 & AS3_PDFCA2 == "2" & AS3_PDFCA2NA == "." ~ "12",

           # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
           cancer_FU1 == 0 & AS3_PDFCA2 == "2" & TRUE ~ AS3_PDFCA2NA,

           # 여전히 암에 걸리지 않은 사람들
           cancer_FU1 == 0 & AS3_PDFCA2 == "1"  ~ "0",
           cancer_FU1 == 0 & AS3_PDFCA2 == "."  ~ "0",

           TRUE ~ "99"
         )
  ) %>%
  # group_by(cancer_FU2_3) %>% count() %>% as.data.frame()
  
  # cancer_FU2_3은 위 용종, 단 하나의 관측값을 갖는다. 
  # 그럼, cancer_FU2_3이 '위용종'인 관측치가 다른 cancer_FU2_는 어떤 값을 갖는지 확인하자.
  # 확인해서 이미 "11"이나 "12"의 값을 갖는다면 굳이 넣지 않아도 됨.
  # dplyr::filter(cancer_FU2_3 == "위용종") %>% 
  # select(RID, cancer_FU2_1, cancer_FU2_2, cancer_FU2_3)
  
  # dplyr::filter(cancer_FU1 == 0) %>%
  # select(cancer_FU2_1, cancer_FU2_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

  mutate(cancer_FU2 = 
           case_when(
             cancer_FU2_1 == "Baseline case" ~ cancer_FU2_1,
             cancer_FU2_1 == "Exclude case" ~ cancer_FU2_1,
             cancer_FU2_1 == "1st F/U case" ~ cancer_FU2_1,
             cancer_FU2_1 == "1st F/U Exclude case" ~ cancer_FU2_1,
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU2_1 == 11 & cancer_FU2_2 == 11 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == 11 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == 11 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == 11 & cancer_FU2_2 == 12 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == 12 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == 12 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == 11 & cancer_FU2_2 == "0" & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == "0" & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 11 & cancer_FU2_2 == "0" & cancer_FU2_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU2_1 == 12 & cancer_FU2_2 == 11 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == 11 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == 11 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == 12 & cancer_FU2_2 == 12 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == 12 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == 12 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == 12 & cancer_FU2_2 == "0" & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == "0" & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == 12 & cancer_FU2_2 == "0" & cancer_FU2_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU2_1 == "0" & cancer_FU2_2 == 11 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == "0" & cancer_FU2_2 == 11 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == "0" & cancer_FU2_2 == 11 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == "0" & cancer_FU2_2 == 12 & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == "0" & cancer_FU2_2 == 12 & cancer_FU2_3 == 12 ~ "3",
             cancer_FU2_1 == "0" & cancer_FU2_2 == 12 & cancer_FU2_3 == "0" ~ "3",
             
             cancer_FU2_1 == "0" & cancer_FU2_2 == "0" & cancer_FU2_3 == 11 ~ "3",
             cancer_FU2_1 == "0" & cancer_FU2_2 == "0" & cancer_FU2_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU2_1 == "0" & cancer_FU2_2 == "0" & cancer_FU2_3 == "0" ~ "0",
             

             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             cancer_FU2_1 != 11 & cancer_FU2_1 != 12 ~ "1",
             cancer_FU2_2 != 11 & cancer_FU2_2 != 12 ~ "1",
             cancer_FU2_3 != 11 & cancer_FU2_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
    # group_by(cancer_FU2) %>% count() %>% as.data.frame()
  
  # 3차 F/U 시작
  # 2차 F/U와 모든 변수가 같...지 않네? 그래도 범주는 똑같으니 이름만 바꿔주자. 
  # 바꿔 줄 것은 2차 F/U에서 업데이트된 암 환자와 제외 인원에 대한 indexing
  # 해당 차수에서 사용할 변수이름들이다. 
  
  mutate(cancer_FU3_1= 
           case_when(
             # 이전 내용 정리 
             cancer_FU2 == "Baseline case" ~ cancer_FU2,
             cancer_FU2 == "Exclude case" ~ cancer_FU2,
             
             cancer_FU2 == "1st F/U case" ~ cancer_FU2,
             cancer_FU2 == "1st F/U Exclude case" ~ cancer_FU2, 
             
             cancer_FU2 == "1" ~ "2nd F/U case", 
             cancer_FU2 == "3" ~ "2nd F/U Exclude case", 
             
             # 1. 위암
             cancer_FU2 == 0 & AS4_GCA == 2 ~ "1",
             
             # 2. 간암
             cancer_FU2 == 0 & AS4_HCC == 2 ~ "2",
             
             # 3. 대장암
             cancer_FU2 == 0 & AS4_COLCA  == 2 ~ "3",
             
             # 4. 유방암
             cancer_FU2 == 0 & AS4_BRCA == 2 ~ "4",
             
             # 6. 폐암
             cancer_FU2 == 0 & AS4_LCA == 2 ~ "6",
             
             # 10. 췌장암
             cancer_FU2 == 0 & AS4_PACA == 2 ~ "10",
             
             # 10. 자궁암
             cancer_FU2 == 0 & AS4_UTCA == 2 ~ "10",
             
             # FU2에서 넘어온 total N이지만 일단 남은 사람들
             cancer_FU2 == 0 ~ "0"
             
           )
  ) %>%
  # group_by(cancer_FU3_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU3_2= 
           case_when(
             # 이전 내용 정리 
             cancer_FU2 == "Baseline case" ~ cancer_FU2,
             cancer_FU2 == "Exclude case" ~ cancer_FU2,
             
             cancer_FU2 == "1st F/U case" ~ cancer_FU2,
             cancer_FU2 == "1st F/U Exclude case" ~ cancer_FU2, 
             
             cancer_FU2 == "1" ~ "2nd F/U case", 
             cancer_FU2 == "3" ~ "2nd F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 3개 종으로 보임
             
             # cancer_FU2 == 0 & grepl("암", AS4_CA1NA) == TRUE ~ AS4_CA1NA,
             # 
             # cancer_FU2 == 0 & is.na(AS4_CA1NA) != TRUE ~ AS4_CA1NA,
             # 
             # TRUE ~ as.character(cancer_FU2)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_FU2 == 0 & grepl("위암|위장암", AS4_CA1NA) == TRUE  ~ "1",

             cancer_FU2 == 0 & AS4_CA1NA == "간암" ~ "2",

             cancer_FU2 == 0 & grepl("대장$|대장암", AS4_CA1NA) == TRUE ~ "3",

             cancer_FU2 == 0 & AS4_CA1NA == "유방암" ~ "4",

             cancer_FU2 == 0 & grepl("경부암|자궁경부암", AS4_CA1NA) == TRUE ~ "5",

             cancer_FU2 == 0 & grepl("폐암", AS4_CA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_FU2 == 0 & AS4_CA1NA == "갑상선암"| AS4_CA1NA == "갑상선" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_FU2 == 0 & grepl("전립선암|전립선$", AS4_CA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_FU2 == 0 & grepl("방광암|방광$", AS4_CA1NA) == TRUE ~ "9",

             # 암종 구분
             # grepl("암", AS4_CA1NA) == TRUE ~ AS4_CA1NA,
             #
             # TRUE ~ AS4_CA1NA
             #
             #
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU2 == 0 & grepl("암", AS4_CA1NA) == TRUE ~ "10",
             cancer_FU2 == 0 & grepl("암", AS4_OTH1NA) == TRUE ~ "10", # 기타 질환에서 피부암, 신장암 케이스 있음. 

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU2 == 0 & AS4_CA1 == "2" & AS4_CA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU2 == 0 & AS4_CA1 == "2" & AS4_CA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU2 == 0 & AS4_CA1 == "2" & TRUE ~ AS4_CA1NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU2 == 0 & AS4_CA1 == "1"  ~ "0",
             cancer_FU2 == 0 & AS4_CA1 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU3_2) %>% count() %>% as.data.frame()
  
  
  
  mutate(cancer_FU3_3= 
           case_when(
             # 이전 내용 정리 
             cancer_FU2 == "Baseline case" ~ cancer_FU2,
             cancer_FU2 == "Exclude case" ~ cancer_FU2,
             
             cancer_FU2 == "1st F/U case" ~ cancer_FU2,
             cancer_FU2 == "1st F/U Exclude case" ~ cancer_FU2, 
             
             cancer_FU2 == "1" ~ "2nd F/U case", 
             cancer_FU2 == "3" ~ "2nd F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 갑상선 암 하나
             # 그럼, cancer_FU3_3이 '갑상선'인 관측치가 다른 cancer_FU2_는 어떤 값을 갖는지 확인하자.
             # cancer_FU2 == 0 & grepl("암", AS4_CA2NA) == TRUE ~ AS4_CA2NA,
             # 
             # cancer_FU2 == 0 & is.na(AS4_CA2NA) != TRUE ~ AS4_CA2NA,
             # 
             # TRUE ~ as.character(cancer_FU2)

             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             cancer_FU2 == 0 & AS4_CA2NA == "갑상선암"| AS4_CA2NA == "갑상선" ~ "7",

             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU2 == 0 & grepl("암", AS4_CA2NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU2 == 0 & AS4_CA2 == "2" & AS4_CA2NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU2 == 0 & AS4_CA2 == "2" & AS4_CA2NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU2 == 0 & AS4_CA2 == "2" & TRUE ~ AS4_CA2NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU2 == 0 & AS4_CA2 == "1"  ~ "0",
             cancer_FU2 == 0 & AS4_CA2 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU3_3) %>% count() %>% as.data.frame()
  
  # cancer_FU3_3은 갑상선암, 단 하나의 관측값을 갖는다. 
  # dplyr::filter(cancer_FU3_3 == "갑상선암") %>%
  # select(RID, cancer_FU3_1, cancer_FU3_2, cancer_FU3_3)
  
  # 다른 종양 진단을 조회해본 결과, 유방종양과 갑상선암 두 개를 갖는다. 
  # 그럼 cancer_FU3_3의 갑상선암과 cancer_FU3_2의 유방종양의 자리를 바꾸면 되지 않을까? 
  mutate(cancer_FU3_2 =
           case_when(
             RID == "EPI17_009_2_162896" ~ "7",
             TRUE ~ cancer_FU3_2
           )
         ) %>%
  mutate(cancer_FU3_3 =
           case_when(
             RID == "EPI17_009_2_162896" ~ "11",
             TRUE ~ cancer_FU3_3
           )
  ) %>%
  
  # 확인, 확인완료 
  # dplyr::filter(AS4_CA2NA == "갑상선암") %>%
  # select(RID, cancer_FU3_1, cancer_FU3_2, cancer_FU3_3)

  # dplyr::filter(cancer_FU2 == 0) %>%
  # select(cancer_FU3_1, cancer_FU3_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

  mutate(cancer_FU3 = 
           case_when(
             cancer_FU2 == "Baseline case" ~ cancer_FU2,
             cancer_FU2 == "Exclude case" ~ cancer_FU2,
             
             cancer_FU2 == "1st F/U case" ~ cancer_FU2,
             cancer_FU2 == "1st F/U Exclude case" ~ cancer_FU2, 
             
             cancer_FU2 == "1" ~ "2nd F/U case", 
             cancer_FU2 == "3" ~ "2nd F/U Exclude case", 
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU3_1 == 11 & cancer_FU3_2 == 11 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == 11 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == 11 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == 11 & cancer_FU3_2 == 12 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == 12 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == 12 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == 11 & cancer_FU3_2 == "0" & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == "0" & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 11 & cancer_FU3_2 == "0" & cancer_FU3_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU3_1 == 12 & cancer_FU3_2 == 11 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == 11 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == 11 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == 12 & cancer_FU3_2 == 12 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == 12 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == 12 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == 12 & cancer_FU3_2 == "0" & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == "0" & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == 12 & cancer_FU3_2 == "0" & cancer_FU3_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU3_1 == "0" & cancer_FU3_2 == 11 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == "0" & cancer_FU3_2 == 11 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == "0" & cancer_FU3_2 == 11 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == "0" & cancer_FU3_2 == 12 & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == "0" & cancer_FU3_2 == 12 & cancer_FU3_3 == 12 ~ "3",
             cancer_FU3_1 == "0" & cancer_FU3_2 == 12 & cancer_FU3_3 == "0" ~ "3",
             
             cancer_FU3_1 == "0" & cancer_FU3_2 == "0" & cancer_FU3_3 == 11 ~ "3",
             cancer_FU3_1 == "0" & cancer_FU3_2 == "0" & cancer_FU3_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU3_1 == "0" & cancer_FU3_2 == "0" & cancer_FU3_3 == "0" ~ "0",
             
             
             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             cancer_FU3_1 != 11 & cancer_FU3_1 != 12 ~ "1",
             cancer_FU3_2 != 11 & cancer_FU3_2 != 12 ~ "1",
             cancer_FU3_3 != 11 & cancer_FU3_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # group_by(cancer_FU3) %>% count() %>% as.data.frame()
  
  # 불현듯 생각난 '기타질환'에 있었던 암종
  # '기타질환'에 암종이 있던 사람은 cancer_FU3에서 암환자로 빠졌을까? 
  # 안빠짐. cancer_FU3_2에 코드 추가하고 옴
  # dplyr::filter(grepl("암", AS4_OTH1NA) == TRUE) %>% 
  # select(RID, AS4_OTH1NA, cancer_FU3)
  
  
  # 4차 F/U 시작
  # 3차 F/U와 모든 변수가 같다. 
  # 바꿔 줄 것은 3차 F/U에서 업데이트된 암 환자와 제외 인원에 대한 indexing
  # 해당 차수에서 사용할 변수이름들이다. 
  
  mutate(cancer_FU4_1= 
           case_when(
             # 이전 내용 정리 
             cancer_FU3 == "Baseline case" ~ cancer_FU3,
             cancer_FU3 == "Exclude case" ~ cancer_FU3,
             
             cancer_FU3 == "1st F/U case" ~ cancer_FU3,
             cancer_FU3 == "1st F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "2nd F/U case" ~ cancer_FU3,  
             cancer_FU3 == "2nd F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "1" ~ "3nd F/U case", 
             cancer_FU3 == "3" ~ "3nd F/U Exclude case", 
             
             # 1. 위암
             cancer_FU3 == 0 & AS5_GCA == 2 ~ "1",
             
             # 2. 간암
             cancer_FU3 == 0 & AS5_HCC == 2 ~ "2",
             
             # 3. 대장암
             cancer_FU3 == 0 & AS5_COLCA  == 2 ~ "3",
             
             # 4. 유방암
             cancer_FU3 == 0 & AS5_BRCA == 2 ~ "4",
             
             # 6. 폐암
             cancer_FU3 == 0 & AS5_LCA == 2 ~ "6",
             
             # 10. 췌장암
             cancer_FU3 == 0 & AS5_PACA == 2 ~ "10",
             
             # 10. 자궁암
             cancer_FU3 == 0 & AS5_UTCA == 2 ~ "10",
             
             # FU3에서 넘어온 total N이지만 일단 남은 사람들
             cancer_FU3 == 0 ~ "0"
             
           )
  ) %>%
  # group_by(cancer_FU4_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU4_2= 
           case_when(
             # 이전 내용 정리 
             cancer_FU3 == "Baseline case" ~ cancer_FU3,
             cancer_FU3 == "Exclude case" ~ cancer_FU3,
             
             cancer_FU3 == "1st F/U case" ~ cancer_FU3,
             cancer_FU3 == "1st F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "2nd F/U case" ~ cancer_FU3,  
             cancer_FU3 == "2nd F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "1" ~ "3nd F/U case", 
             cancer_FU3 == "3" ~ "3nd F/U Exclude case", 
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 10개 종
             # cancer_FU3 == 0 & grepl("암", AS5_CA1NA) == TRUE ~ AS5_CA1NA,
             # 
             # cancer_FU3 == 0 & is.na(AS5_CA1NA) != TRUE ~ AS5_CA1NA,
             # 
             # TRUE ~ as.character(cancer_FU3)

             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_FU3 == 0 & grepl("위암|위장암", AS5_CA1NA) == TRUE  ~ "1",

             cancer_FU3 == 0 & AS5_CA1NA == "간암" ~ "2",

             cancer_FU3 == 0 & grepl("대장$|대장암", AS5_CA1NA) == TRUE ~ "3",

             cancer_FU3 == 0 & AS5_CA1NA == "유방암" ~ "4",

             cancer_FU3 == 0 & grepl("경부암|자궁경부암", AS5_CA1NA) == TRUE ~ "5",

             cancer_FU3 == 0 & grepl("폐암", AS5_CA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_FU3 == 0 & AS5_CA1NA == "갑상선암"| AS5_CA1NA == "갑상선" ~ "7",
             cancer_FU3 == 0 & AS5_OTH1NA == "갑상선암" ~ "7",
             
             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_FU3 == 0 & grepl("전립선암|전립선", AS5_CA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_FU3 == 0 & grepl("방광암|방광$", AS5_CA1NA) == TRUE ~ "9",

             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU3 == 0 & grepl("암", AS5_CA1NA) == TRUE ~ "10",
             cancer_FU3 == 0 & grepl("암", AS5_OTH1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU3 == 0 & AS5_CA1 == "2" & AS5_CA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU3 == 0 & AS5_CA1 == "2" & AS5_CA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU3 == 0 & AS5_CA1 == "2" & TRUE ~ AS5_CA1NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU3 == 0 & AS5_CA1 == "1"  ~ "0",
             cancer_FU3 == 0 & AS5_CA1 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU4_2) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU4_3= 
           case_when(
             # 이전 내용 정리 
             cancer_FU3 == "Baseline case" ~ cancer_FU3,
             cancer_FU3 == "Exclude case" ~ cancer_FU3,
             
             cancer_FU3 == "1st F/U case" ~ cancer_FU3,
             cancer_FU3 == "1st F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "2nd F/U case" ~ cancer_FU3,  
             cancer_FU3 == "2nd F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "1" ~ "3nd F/U case", 
             cancer_FU3 == "3" ~ "3nd F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 자궁상피내암 1, 나머지 기타 종양 3 
             # cancer_FU3 == 0 & grepl("암", AS5_CA2NA) == TRUE ~ AS5_CA2NA,
             # 
             # cancer_FU3 == 0 & is.na(AS5_CA2NA) != TRUE ~ AS5_CA2NA,
             # 
             # TRUE ~ as.character(cancer_FU3)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             # cancer_FU3 == 0 & AS5_CA2NA == "갑상선암"| AS5_CA2NA == "갑상선" ~ "7",
             # 
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU3 == 0 & grepl("암", AS5_CA2NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU3 == 0 & AS5_CA2 == "2" & AS5_CA2NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU3 == 0 & AS5_CA2 == "2" & AS5_CA2NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU3 == 0 & AS5_CA2 == "2" & TRUE ~ AS5_CA2NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU3 == 0 & AS5_CA2 == "1"  ~ "0",
             cancer_FU3 == 0 & AS5_CA2 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU4_3) %>% count() %>% as.data.frame()

  # cancer_FU4_3은 1개의 기타암종과 3개의 기타종양을 갖는다. 
  # 혹시 cancer_FU4_2에 이미 반영이 되어 있지 않을까? 
  # 이미 반영되어 있다! 그럼 cancer_FU4_1과 cancer_FU4_2의 table로만으로도 설명 가능
  # dplyr::filter(grepl("담낭용종|대장종양|유방섬유종|자궁상피내암", cancer_FU4_3) == TRUE) %>%
  # select(RID, cancer_FU4_1, cancer_FU4_2, cancer_FU4_3)
  
  
  
  # 마찬가지로 AS5에서도 '기타질환'에서 암종이 들어간 경우가 있음
  # 제외되었는지 체크하고 제외되어있지 않다면 cancer_FU4_2에 추가하고 오기
  # 제외되어있지 않기 때문에 추가함. 갑상선암 1, 기타암종 2

  # dplyr::filter(grepl("암", AS5_OTH1NA) == TRUE) %>%
  # select(RID, AS5_OTH1NA, cancer_FU4_1, cancer_FU4_2, cancer_FU4_3, cancer_FU3)
  
  # dplyr::filter(cancer_FU3 == 0) %>%
  # select(cancer_FU4_1, cancer_FU4_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

  mutate(cancer_FU4 = 
           case_when(
             cancer_FU3 == "Baseline case" ~ cancer_FU3,
             cancer_FU3 == "Exclude case" ~ cancer_FU3,
             
             cancer_FU3 == "1st F/U case" ~ cancer_FU3,
             cancer_FU3 == "1st F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "2nd F/U case" ~ cancer_FU3,  
             cancer_FU3 == "2nd F/U Exclude case" ~ cancer_FU3, 
             
             cancer_FU3 == "1" ~ "3nd F/U case", 
             cancer_FU3 == "3" ~ "3nd F/U Exclude case", 
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU4_1 == 11 & cancer_FU4_2 == 11 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == 11 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == 11 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == 11 & cancer_FU4_2 == 12 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == 12 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == 12 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == 11 & cancer_FU4_2 == "0" & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == "0" & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 11 & cancer_FU4_2 == "0" & cancer_FU4_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU4_1 == 12 & cancer_FU4_2 == 11 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == 11 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == 11 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == 12 & cancer_FU4_2 == 12 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == 12 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == 12 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == 12 & cancer_FU4_2 == "0" & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == "0" & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == 12 & cancer_FU4_2 == "0" & cancer_FU4_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU4_1 == "0" & cancer_FU4_2 == 11 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == "0" & cancer_FU4_2 == 11 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == "0" & cancer_FU4_2 == 11 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == "0" & cancer_FU4_2 == 12 & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == "0" & cancer_FU4_2 == 12 & cancer_FU4_3 == 12 ~ "3",
             cancer_FU4_1 == "0" & cancer_FU4_2 == 12 & cancer_FU4_3 == "0" ~ "3",
             
             cancer_FU4_1 == "0" & cancer_FU4_2 == "0" & cancer_FU4_3 == 11 ~ "3",
             cancer_FU4_1 == "0" & cancer_FU4_2 == "0" & cancer_FU4_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU4_1 == "0" & cancer_FU4_2 == "0" & cancer_FU4_3 == "0" ~ "0",
             
             
             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             # cancer_FU4_1 != 11 & cancer_FU4_1 != 12 & cancer_FU4_1 != "0" ~ "1_1",
             # cancer_FU4_2 != 11 & cancer_FU4_2 != 12 & cancer_FU4_2 != "0"~ "1_2",
             # cancer_FU4_3 != 11 & cancer_FU4_3 != 12 & cancer_FU4_3 != "0"~ "1_3",
             
             cancer_FU4_1 != 11 & cancer_FU4_1 != 12 ~ "1",
             cancer_FU4_2 != 11 & cancer_FU4_2 != 12 ~ "1",
             cancer_FU4_3 != 11 & cancer_FU4_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # group_by(cancer_FU4) %>% count() %>% as.data.frame()
  
  # 5차 F/U 시작
  # 3차 F/U와 모든 변수가 같다. 
  # 바꿔 줄 것은 3차 F/U에서 업데이트된 암 환자와 제외 인원에 대한 indexing
  # 해당 차수에서 사용할 변수이름들이다. 
  
  mutate(cancer_FU5_1= 
           case_when(
             # 이전 내용 정리 
             cancer_FU4 == "Baseline case" ~ cancer_FU4,
             cancer_FU4 == "Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1st F/U case" ~ cancer_FU4,
             cancer_FU4 == "1st F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "2nd F/U case" ~ cancer_FU4,  
             cancer_FU4 == "2nd F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "3nd F/U case" ~ cancer_FU4, 
             cancer_FU4 == "3nd F/U Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1" ~ "4th F/U case", 
             cancer_FU4 == "3" ~ "4th F/U Exclude case", 
             
             # 1. 위암
             cancer_FU4 == 0 & AS6_GCA == 2 ~ "1",
             
             # 2. 간암
             cancer_FU4 == 0 & AS6_HCC == 2 ~ "2",
             
             # 3. 대장암
             cancer_FU4 == 0 & AS6_COLCA  == 2 ~ "3",
             
             # 4. 유방암
             cancer_FU4 == 0 & AS6_BRCA == 2 ~ "4",
             
             # 6. 폐암
             cancer_FU4 == 0 & AS6_LCA == 2 ~ "6",
             
             # 10. 췌장암
             cancer_FU4 == 0 & AS6_PACA == 2 ~ "10",
             
             # 10. 자궁암
             cancer_FU4 == 0 & AS6_UTCA == 2 ~ "10",
             
             # FU4에서 넘어온 total N이지만 일단 남은 사람들
             cancer_FU4 == 0 ~ "0"
             
           )
  ) %>%
  # group_by(cancer_FU5_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU5_2= 
           case_when(
             # 이전 내용 정리 
             cancer_FU4 == "Baseline case" ~ cancer_FU4,
             cancer_FU4 == "Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1st F/U case" ~ cancer_FU4,
             cancer_FU4 == "1st F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "2nd F/U case" ~ cancer_FU4,  
             cancer_FU4 == "2nd F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "3nd F/U case" ~ cancer_FU4, 
             cancer_FU4 == "3nd F/U Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1" ~ "4th F/U case", 
             cancer_FU4 == "3" ~ "4th F/U Exclude case", 
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 10개 종
             # cancer_FU4 == 0 & grepl("암", AS6_CA1NA) == TRUE ~ AS6_CA1NA,
             # 
             # cancer_FU4 == 0 & is.na(AS6_CA1NA) != TRUE ~ AS6_CA1NA,
             # 
             # TRUE ~ as.character(cancer_FU4)

             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_FU4 == 0 & grepl("위암|위장암", AS6_CA1NA) == TRUE  ~ "1",

             cancer_FU4 == 0 & AS6_CA1NA == "간암" ~ "2",

             cancer_FU4 == 0 & grepl("대장$|대장암", AS6_CA1NA) == TRUE ~ "3",

             cancer_FU4 == 0 & AS6_CA1NA == "유방암" ~ "4",

             cancer_FU4 == 0 & grepl("경부암|자궁경부암", AS6_CA1NA) == TRUE ~ "5",

             cancer_FU4 == 0 & grepl("폐암", AS6_CA1NA) == TRUE ~ "6",

             # 일단, 갑상선도 갑상선암으로 간주하고 진행함.
             cancer_FU4 == 0 & AS6_CA1NA == "갑상선암"| AS6_CA1NA == "갑상선" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_FU4 == 0 & grepl("전립선암|전립선", AS6_CA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_FU4 == 0 & grepl("방광암|방광$", AS6_CA1NA) == TRUE ~ "9",

             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU4 == 0 & grepl("암", AS6_CA1NA) == TRUE ~ "10",
             cancer_FU4 == 0 & grepl("암", AS6_OTH1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU4 == 0 & AS6_CA1 == "2" & AS6_CA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU4 == 0 & AS6_CA1 == "2" & AS6_CA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU4 == 0 & AS6_CA1 == "2" & TRUE ~ AS6_CA1NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU4 == 0 & AS6_CA1 == "1"  ~ "0",
             cancer_FU4 == 0 & AS6_CA1 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU5_2) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU5_3= 
           case_when(
             # 이전 내용 정리 
             cancer_FU4 == "Baseline case" ~ cancer_FU4,
             cancer_FU4 == "Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1st F/U case" ~ cancer_FU4,
             cancer_FU4 == "1st F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "2nd F/U case" ~ cancer_FU4,  
             cancer_FU4 == "2nd F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "3nd F/U case" ~ cancer_FU4, 
             cancer_FU4 == "3nd F/U Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1" ~ "4th F/U case", 
             cancer_FU4 == "3" ~ "4th F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 나머지 기타 종양 4개 종, 6명
             # cancer_FU4 == 0 & grepl("암", AS6_CA2NA) == TRUE ~ AS6_CA2NA,
             # 
             # cancer_FU4 == 0 & is.na(AS6_CA2NA) != TRUE ~ AS6_CA2NA,
             # 
             # TRUE ~ as.character(cancer_FU4)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             # cancer_FU3 == 0 & AS5_CA2NA == "갑상선암"| AS5_CA2NA == "갑상선" ~ "7",
             # 
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU4 == 0 & grepl("암", AS6_CA2NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU4 == 0 & AS6_CA2 == "2" & AS6_CA2NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU4 == 0 & AS6_CA2 == "2" & AS6_CA2NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU4 == 0 & AS6_CA2 == "2" & TRUE ~ AS6_CA2NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU4 == 0 & AS6_CA2 == "1"  ~ "0",
             cancer_FU4 == 0 & AS6_CA2 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU5_3) %>% count() %>% as.data.frame()
  
  # cancer_FU5_3은 4개의 기타종양을 갖는다. 
  # 혹시 cancer_FU5_2에 이미 반영이 되어 있지 않을까? 
  # 이미 반영되어 있다! 그럼 cancer_FU5_1과 cancer_FU5_2의 table로만으로도 설명 가능
  # dplyr::filter(grepl("뇌하수체종양|대장용종|위물혹|유방물혹", cancer_FU5_3) == TRUE) %>%
  # select(RID, cancer_FU4, cancer_FU5_1, cancer_FU5_2, cancer_FU5_3)
  

  # dplyr::filter(cancer_FU4 == 0) %>%
  # select(cancer_FU5_1, cancer_FU5_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

  mutate(cancer_FU5 = 
           case_when(
             # 이전 내용 정리 
             cancer_FU4 == "Baseline case" ~ cancer_FU4,
             cancer_FU4 == "Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1st F/U case" ~ cancer_FU4,
             cancer_FU4 == "1st F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "2nd F/U case" ~ cancer_FU4,  
             cancer_FU4 == "2nd F/U Exclude case" ~ cancer_FU4, 
             
             cancer_FU4 == "3nd F/U case" ~ cancer_FU4, 
             cancer_FU4 == "3nd F/U Exclude case" ~ cancer_FU4,
             
             cancer_FU4 == "1" ~ "4th F/U case", 
             cancer_FU4 == "3" ~ "4th F/U Exclude case", 
             
             # 2개의 진단명에서 10을 갖는 obs 중 한번이라도 1-9를 갖는 obs는 모두 cancer case에 포함
             # (cancer_FU_1 == 10 | cancer_FU_1 == 11 | cancer_FU_1 == 12) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1",
             # (cancer_FU_1 == 10) & (cancer_FU_2 != 10 & cancer_FU_2 != "0" & cancer_FU_2 != "11") ~ "1", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU5_1 == 11 & cancer_FU5_2 == 11 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == 11 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == 11 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == 11 & cancer_FU5_2 == 12 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == 12 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == 12 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == 11 & cancer_FU5_2 == "0" & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == "0" & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 11 & cancer_FU5_2 == "0" & cancer_FU5_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU5_1 == 12 & cancer_FU5_2 == 11 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == 11 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == 11 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == 12 & cancer_FU5_2 == 12 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == 12 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == 12 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == 12 & cancer_FU5_2 == "0" & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == "0" & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == 12 & cancer_FU5_2 == "0" & cancer_FU5_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU5_1 == "0" & cancer_FU5_2 == 11 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == "0" & cancer_FU5_2 == 11 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == "0" & cancer_FU5_2 == 11 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == "0" & cancer_FU5_2 == 12 & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == "0" & cancer_FU5_2 == 12 & cancer_FU5_3 == 12 ~ "3",
             cancer_FU5_1 == "0" & cancer_FU5_2 == 12 & cancer_FU5_3 == "0" ~ "3",
             
             cancer_FU5_1 == "0" & cancer_FU5_2 == "0" & cancer_FU5_3 == 11 ~ "3",
             cancer_FU5_1 == "0" & cancer_FU5_2 == "0" & cancer_FU5_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU5_1 == "0" & cancer_FU5_2 == "0" & cancer_FU5_3 == "0" ~ "0",
             
             
             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             cancer_FU5_1 != 11 & cancer_FU5_1 != 12 ~ "1",
             cancer_FU5_2 != 11 & cancer_FU5_2 != 12 ~ "1",
             cancer_FU5_3 != 11 & cancer_FU5_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
    # group_by(cancer_FU5) %>% count() %>% as.data.frame()
  
  # 6차 F/U 시작
  # 3차 F/U와 모든 변수가 같다. 
  # 바꿔 줄 것은 3차 F/U에서 업데이트된 암 환자와 제외 인원에 대한 indexing
  # 해당 차수에서 사용할 변수이름들이다. 
  
  mutate(cancer_FU6_1= 
           case_when(
             # 이전 내용 정리 
             cancer_FU5 == "Baseline case" ~ cancer_FU5,
             cancer_FU5 == "Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1st F/U case" ~ cancer_FU5,
             cancer_FU5 == "1st F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "2nd F/U case" ~ cancer_FU5,  
             cancer_FU5 == "2nd F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "3nd F/U case" ~ cancer_FU5, 
             cancer_FU5 == "3nd F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "4th F/U case" ~ cancer_FU5, 
             cancer_FU5 == "4th F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1" ~ "5th F/U case", 
             cancer_FU5 == "3" ~ "5th F/U Exclude case", 
             
             # 1. 위암
             cancer_FU5 == 0 & AS7_GCA == 2 ~ "1",
             
             # 2. 간암
             cancer_FU5 == 0 & AS7_HCC == 2 ~ "2",
             
             # 3. 대장암
             cancer_FU5 == 0 & AS7_COLCA  == 2 ~ "3",
             
             # 4. 유방암
             cancer_FU5 == 0 & AS7_BRCA == 2 ~ "4",
             
             # 6. 폐암
             cancer_FU5 == 0 & AS7_LCA == 2 ~ "6",
             
             # 10. 췌장암
             cancer_FU5 == 0 & AS7_PACA == 2 ~ "10",
             
             # 10. 자궁암
             cancer_FU5 == 0 & AS7_UTCA == 2 ~ "10",
             
             # FU5에서 넘어온 total N이지만 일단 남은 사람들
             cancer_FU5 == 0 ~ "0"
             
           )
  ) %>%
  # group_by(cancer_FU6_1) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU6_2= 
           case_when(
             # 이전 내용 정리 
             cancer_FU5 == "Baseline case" ~ cancer_FU5,
             cancer_FU5 == "Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1st F/U case" ~ cancer_FU5,
             cancer_FU5 == "1st F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "2nd F/U case" ~ cancer_FU5,  
             cancer_FU5 == "2nd F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "3nd F/U case" ~ cancer_FU5, 
             cancer_FU5 == "3nd F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "4th F/U case" ~ cancer_FU5, 
             cancer_FU5 == "4th F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1" ~ "5th F/U case", 
             cancer_FU5 == "3" ~ "5th F/U Exclude case", 
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 6개 종
             # cancer_FU5 == 0 & grepl("암", AS7_CA1NA) == TRUE ~ AS7_CA1NA,
             # 
             # cancer_FU5 == 0 & is.na(AS7_CA1NA) != TRUE ~ AS7_CA1NA,
             # 
             # TRUE ~ as.character(cancer_FU5)

             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             
             cancer_FU5 == 0 & grepl("위암|위장암", AS7_CA1NA) == TRUE  ~ "1",

             cancer_FU5 == 0 & AS7_CA1NA == "간암" ~ "2",

             cancer_FU5 == 0 & grepl("대장$|대장암", AS7_CA1NA) == TRUE ~ "3",

             cancer_FU5 == 0 & AS7_CA1NA == "유방암" ~ "4",

             cancer_FU5 == 0 & grepl("경부암|자궁경부암", AS7_CA1NA) == TRUE ~ "5",

             cancer_FU5 == 0 & grepl("폐암", AS7_CA1NA) == TRUE ~ "6",

             cancer_FU5 == 0 & AS7_CA1NA == "갑상선암" ~ "7",

             # 전립선도 전립선암으로 간주하고 진행함.
             cancer_FU5 == 0 & grepl("전립선암|전립선", AS7_CA1NA) == TRUE ~ "8",

             # 방광도 방광암으로 간주하고 진행함.
             cancer_FU5 == 0 & grepl("방광암|방광$", AS7_CA1NA) == TRUE ~ "9",

             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU5 == 0 & grepl("암", AS7_CA1NA) == TRUE ~ "10",
             cancer_FU5 == 0 & grepl("암", AS7_OTH1NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU5 == 0 & AS7_CA1 == "2" & AS7_CA1NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU5 == 0 & AS7_CA1 == "2" & AS7_CA1NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU5 == 0 & AS7_CA1 == "2" & TRUE ~ AS7_CA1NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU5 == 0 & AS7_CA1 == "1"  ~ "0",
             cancer_FU5 == 0 & AS7_CA1 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU6_2) %>% count() %>% as.data.frame()
  
  mutate(cancer_FU6_3= 
           case_when(
             # 이전 내용 정리 
             cancer_FU5 == "Baseline case" ~ cancer_FU5,
             cancer_FU5 == "Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1st F/U case" ~ cancer_FU5,
             cancer_FU5 == "1st F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "2nd F/U case" ~ cancer_FU5,  
             cancer_FU5 == "2nd F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "3nd F/U case" ~ cancer_FU5, 
             cancer_FU5 == "3nd F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "4th F/U case" ~ cancer_FU5, 
             cancer_FU5 == "4th F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1" ~ "5th F/U case", 
             cancer_FU5 == "3" ~ "5th F/U Exclude case", 
             
             
             # 1) 몇 종류의 암종이 있는지 먼저 파악
             # 나머지 기타 종양 3개
             # cancer_FU5 == 0 & grepl("암", AS7_CA2NA) == TRUE ~ AS7_CA2NA,
             # 
             # cancer_FU5 == 0 & is.na(AS7_CA2NA) != TRUE ~ AS7_CA2NA,
             # 
             # TRUE ~ as.character(cancer_FU5)
             
             
             # 2) 도시코호트에서 정리된 것처럼 1-9까지 정의해보기
             ## 순서대로 위암, 간암, 대장암, 유방암, 자궁경부암, 폐암, 갑상선암, 전립선암, 방광암
             # cancer_FU3 == 0 & AS5_CA2NA == "갑상선암"| AS5_CA2NA == "갑상선" ~ "7",
             # 
             # 1-9에 포함되지 않지만 '암'이면 10
             cancer_FU5 == 0 & grepl("암", AS7_CA2NA) == TRUE ~ "10",

             # 암이 있다고 대답했으나 암이 아닌 다른 종양이면 11
             cancer_FU5 == 0 & AS7_CA2 == "2" & AS7_CA2NA != "." ~ "11",

             # 암이 있다고 대답했으나 진단명이 없으면 12
             cancer_FU5 == 0 & AS7_CA2 == "2" & AS7_CA2NA == "." ~ "12",

             # 혹시 누락된 값이 있을 수 있으니 체크하기 위한 code
             cancer_FU5 == 0 & AS7_CA2 == "2" & TRUE ~ AS7_CA2NA,

             # 여전히 암에 걸리지 않은 사람들
             cancer_FU5 == 0 & AS7_CA2 == "1"  ~ "0",
             cancer_FU5 == 0 & AS7_CA2 == "."  ~ "0",

             TRUE ~ "99"
           )
  ) %>%
  # group_by(cancer_FU6_3) %>% count() %>% as.data.frame()
  
  # cancer_FU6_3은 3개의 기타종양을 갖는다. 
  # 혹시 cancer_FU6_2에 이미 반영이 되어 있지 않을까? 
  # 이미 반영되어 있다! 그럼 cancer_FU6_1과 cancer_FU6_2의 table로만으로도 설명 가능
  # dplyr::filter(grepl("갑상선상선종양(관찰)|대장용종|위양성종양", cancer_FU6_3) == TRUE) %>%
  # select(RID, cancer_FU5, cancer_FU6_1, cancer_FU6_2, cancer_FU6_3)
  
  
  # dplyr::filter(cancer_FU5 == 0) %>%
  # select(cancer_FU6_1, cancer_FU6_2) %>%
  # mutate_all(funs(as.numeric)) %>%
  # table()

  mutate(cancer_FU6 = 
           case_when(
             # 이전 내용 정리 
             cancer_FU5 == "Baseline case" ~ cancer_FU5,
             cancer_FU5 == "Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1st F/U case" ~ cancer_FU5,
             cancer_FU5 == "1st F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "2nd F/U case" ~ cancer_FU5,  
             cancer_FU5 == "2nd F/U Exclude case" ~ cancer_FU5, 
             
             cancer_FU5 == "3nd F/U case" ~ cancer_FU5, 
             cancer_FU5 == "3nd F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "4th F/U case" ~ cancer_FU5, 
             cancer_FU5 == "4th F/U Exclude case" ~ cancer_FU5,
             
             cancer_FU5 == "1" ~ "5th F/U case", 
             cancer_FU5 == "3" ~ "5th F/U Exclude case", 
             
             # 3개의 진단명에서 11, 12을 갖는 obs 중 한번이라도 1-10를 갖지 않는 obs는 모두 '기타'에 포함
             # "3"은 F/U N 수에 포함되지 않는 excldue group에 대한 index임
             
             # cancer_FU_1, cancer_FU_2, cancer_FU_3이 하나라도 1-10을 포함할 경우의 수 == 
             # 전체 경우의 수 - (cancer_FU_1, cancer_FU_2, cancer_FU_3이 1-10을 포함하지 않을 경우의 수)
             
             # 경우의 수 1/3개 
             cancer_FU6_1 == 11 & cancer_FU6_2 == 11 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == 11 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == 11 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == 11 & cancer_FU6_2 == 12 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == 12 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == 12 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == 11 & cancer_FU6_2 == "0" & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == "0" & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 11 & cancer_FU6_2 == "0" & cancer_FU6_3 == "0" ~ "3",
             
             # 경우의 수 2/3개 
             cancer_FU6_1 == 12 & cancer_FU6_2 == 11 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == 11 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == 11 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == 12 & cancer_FU6_2 == 12 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == 12 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == 12 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == 12 & cancer_FU6_2 == "0" & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == "0" & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == 12 & cancer_FU6_2 == "0" & cancer_FU6_3 == "0" ~ "3",
             
             # 경우의 수 3/3개 
             cancer_FU6_1 == "0" & cancer_FU6_2 == 11 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == "0" & cancer_FU6_2 == 11 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == "0" & cancer_FU6_2 == 11 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == "0" & cancer_FU6_2 == 12 & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == "0" & cancer_FU6_2 == 12 & cancer_FU6_3 == 12 ~ "3",
             cancer_FU6_1 == "0" & cancer_FU6_2 == 12 & cancer_FU6_3 == "0" ~ "3",
             
             cancer_FU6_1 == "0" & cancer_FU6_2 == "0" & cancer_FU6_3 == 11 ~ "3",
             cancer_FU6_1 == "0" & cancer_FU6_2 == "0" & cancer_FU6_3 == 12 ~ "3",
             
             # 모두 0인 경우는 당연히 0 
             cancer_FU6_1 == "0" & cancer_FU6_2 == "0" & cancer_FU6_3 == "0" ~ "0",
             
             
             # 위의 경우를 제외하고 11이 아니고 12가 아닌 경우는 1 
             cancer_FU6_1 != 11 & cancer_FU6_1 != 12 ~ "1",
             cancer_FU6_2 != 11 & cancer_FU6_2 != 12 ~ "1",
             cancer_FU6_3 != 11 & cancer_FU6_3 != 12 ~ "1",
             
             TRUE ~ "99"
           )
  ) %>% 
  # group_by(cancer_FU6) %>% count() %>% as.data.frame()
  
  # BL부터 6th F/U까지 cancer index를 정리할 수 있는 column 하나 만들자. 
  mutate(cancer_index = 
           case_when(
             # 이전 내용 정리 
             cancer_FU6 == "Baseline case" ~ cancer_FU6,
             cancer_FU6 == "Exclude case" ~ cancer_FU6,
             
             cancer_FU6 == "1st F/U case" ~ cancer_FU6,
             cancer_FU6 == "1st F/U Exclude case" ~ cancer_FU6, 
             
             cancer_FU6 == "2nd F/U case" ~ cancer_FU6,  
             cancer_FU6 == "2nd F/U Exclude case" ~ cancer_FU6, 
             
             cancer_FU6 == "3nd F/U case" ~ cancer_FU6, 
             cancer_FU6 == "3nd F/U Exclude case" ~ cancer_FU6,
             
             cancer_FU6 == "4th F/U case" ~ cancer_FU6, 
             cancer_FU6 == "4th F/U Exclude case" ~ cancer_FU6,
             
             cancer_FU6 == "5th F/U case" ~ cancer_FU6, 
             cancer_FU6 == "5th F/U Exclude case" ~ cancer_FU6,
             
             cancer_FU6 == "1" ~ "6th F/U case", 
             cancer_FU6 == "3" ~ "6th F/U Exclude case",
             
             TRUE ~ "Non-case"
           )
  ) %>% 
  count(cancer_index)

  
#### local dataset에서 모든 진단 횟수와 암종 나타내기 ####
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





