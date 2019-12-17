```r
# install.packages("xlsx")
library(xlsx)
# Merging data set

## 1. exploring raw dataset 
hw <- as.tbl(read.xlsx2('...HW_DATA.xlsx', sheetIndex=1, header=TRUE, stringsAsFactors = FALSE))
pc <- as.tbl(read.xlsx2('...PC_DATA.xlsx', sheetIndex=1, header=TRUE, stringsAsFactors = FALSE))
pc
dim(hw) # (227, 949)
dim(pc) # (137, 391)

### 1.1 중복 검사 
duplicated(rbind(hw[, 1], pc[, 1])) 
sum(duplicated(rbind(hw[, 1], pc[, 1]))) # 0
rbind(hw[, 1], pc[, 1])[which(duplicated(rbind(hw[, 1], pc[, 1])) | duplicated(rbind(hw[, 1], pc[, 1]), fromLast=T) ),] # 0

unique(rbind(hw[, 1], pc[, 1])) # 364

### index 상에는 중복이 없는 것으로 보임. 


## 2. digging column-wise 
### 2.1 columns 1:3
hw[, 1:3] # No : observation number, 종양은행번호 : kind of index, 건강기록지.버전 : kind of index
pc[, 1:3]  # No : observation number, label : kind of index, 설문지버전 : kind of index

### 2.1 columns 4:89
sum(colnames(hw[, 4:89]) != colnames(pc[, 4:89])) # 순서와 이름이 같은 것을 확인
colnames(hw[, 4:89]) # 수기 확인 완료

# 4:89까지 part 1로 정의 
hw1 <- hw[, 4:89] %>% type_convert(cols(HEIGHT = col_double()))
pc1 <- pc[, 4:89] %>% type_convert(cols(HEIGHT = col_double()))

#### NOTE. tyoe_convert ####
# 딱 한 번만, 하나의 열의 data type을 바꿔도 나머지 columns의 data type이 바뀐다. 
hw1 <- hw[, 4:89]
hw1 # all column type is chr
hw1 <- hw[, 4:89] %>% type_convert(cols(HEIGHT = col_integer()))
hw1 # change the column type 
#### ####

#### 2.1.1 data type 비교 
which(sapply(hw1, class) == sapply(pc1, class))
which(sapply(hw1, class) != sapply(pc1, class))
sum(sapply(hw1, class) != sapply(pc1, class)) # 17개의 col이 다른 dtype을 갖음 

hw1[, which(sapply(hw1,class) != sapply(pc1,class))]
pc1[, which(sapply(hw1,class) != sapply(pc1,class))]
# '문자' 때문에 chr로 설정되어 있는 것을 확인
# example : hw1$CEA vs pc1$CEA, pc1$CEA가 '>0.5' 때문에 chr로 설정되어 있음. 

which(sapply(hw1, class) == "character" | sapply(pc1, class) == "character")

which(sapply(hw1, class) == "character")
length(which(sapply(hw1, class) == "character"))
which(sapply(pc1, class) == "character")
length(which(sapply(pc1, class) == "character"))

options(max.print=100000)
print(as.data.frame(rbind(hw1[, which(sapply(hw1, class) == "character")], pc1[, which(sapply(hw1, class) == "character")])), width = getOption("max.print"))

# U_cotinine
# >2500 때문에 chr로 되어 있음. 
# 1) 구간으로 나눠 categorical
# 2) >2500를 2500로 변환

# NMP22
# <2.1 때문에 chr로 되어 있음. 
# 1) 구간으로 나눠 categorical, 근데 2.1 미만의 값도 존재하는데?
# 2) <2.1를 2.1로 변환 

# CA19_9, CA125
# <5, chr
# 1) 구간으로 나눠 categorical
# 2) <5를 대체

# VDRL : 실제로 chr, integer로 대체
# HBs_Ag : 실제로 chr, integer로 대체

# Anti_HBs
# < 10, > 290, > 1000
# 1) 구간으로 나눠 categorical
# 2) < 10, > 290, > 1000를 대체

# Anti_HIV : 실제로 chr, integer로 대체

# Anti_HCV : chr

# U_Alb, U_Glucos, U_ket, U_BIL, U_BLD, U_Uro : ?
# -, n+, +/-로 나옴. -가 negative인지 null인지? 

# U_NIT : chr
# - : null? negative?

# U_RBC, U_WBC, U_SQE : 구간으로 정의됨
# hw와 pc의 구간이 조금 다름 : (1,4) vs (1,2), (3,4)
# < 1, (1,4), (5,9), (10. 19), (20, 29), (30, 39), 100 이상


print(as.data.frame(rbind(hw1[, which(sapply(pc1, class) == "character")], pc1[, which(sapply(pc1, class) == "character")]))[, 1:13], width = getOption("max.print"))

# SBP, DBP, LDL : '.' = null value 때문
# U_cotinine : 위에서 처리

# CEA 
# <0.5 때문에 chr로 되어 있음. 
# 1) 구간으로 나눠 categorical
# 2) <0.5를 0.5로 변환 

# NMP22, CA19_9, CA125 : 위에서 처리

# VDRL, HBs_Ag : 위에서 처리
# Anti_HBs, Anti_HCV : 위에서 처리

# Anti_HIV : negative or null


print(as.data.frame(rbind(hw1[, which(sapply(pc1, class) == "character")], pc1[, which(sapply(pc1, class) == "character")]))[, 14:26], width = getOption("max.print"))

# Anti_HAVIgG, U_color, U_Turbidity : chr 
# U_Alb, U_Glucose, U_Ket, U_BIL, U_BLD, U_Uro,
# U_NIT, U_RBC, U_WBC, U_SQE : 위에서 처리 


# CONCLUSION df1, hw1 bind with pc1 
df1 <- rbind(hw1, pc1)



### 2.2 columns with alcohole
col_hw2 <- c("ALC", "ALCDU", "CALC",
             "BEER", "BEER_A",
             "SOJU", "SOJU_A",
             "WSKY", "WSKY_A",
             "TKJU", "TKJU_A",
             "WINE", "WINE_A",
             "ALC_A", "ALC_T",
             "ALC_DA")

# 알콜 관련한 column의 base line
hw2 <- hw[, col_hw2] %>% type_convert(cols(ALC = col_double()))

col_pc2 <- c("ALCOHOL", "ALCOHYR", "DrQYr","DrQMo",
             "AUDIT7", "AUDIT8",
             "BEERN", "BEERAM",
             "SOJUN", "SOJUAM",
             "GINN", "GINAM",
             "RICEN", "RICEAM",
             "WINEN", "WINEAM",
             "FRUITN", "FRUITAM", 
             "ETNAME", "ETALN", "ETALAM", "ETALCUP")
pc2 <- pc[, col_pc2] %>% type_convert(cols(ALCOHOL = col_double()))

#### PROBLEM 2.2.1 건강기록지와 건강검진의 '음주횟수' 수준이 다르다. 
# coding book 기준, 각각 1~8, 0~7 이므로 reference를 0에 맞추면 해결 가능.

# 새로운 문제 : 첫번째 건강기록지의 음주횟수 수준이 6개로 차이가 있다.
## 가설 1. 1st 건강기록지의 음주횟수 수준에는 '안 마신다'가 포함되어 있지 않다. 
##         따라서, 1st 건강기록지의 음주횟수 수준이 첫번째 수준을 갖지만 '음주량'에 value가 들어가 있으면 음주횟수를 조정한다. 
##         => 1st 건강기록지를 제외한 나머지 질문지의 음주횟수 첫번째 수준은 '안 마신다'이므로 '안 마시는 사람'이 '음주량'을 갖고 있을 수 없다고 가정한다. 

# 소주를 예로 들어 시도해보자. 
hw2[which(hw2[(hw2[, "SOJU"]) == 1, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 2, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 3, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 4, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 5, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 6, ]$SOJU_A < 99), "SOJU_A"]
hw2[which(hw2[(hw2[, "SOJU"]) == 7, ]$SOJU_A < 99), "SOJU_A"] # null

pc2[which(pc2[(pc2[, "SOJUN"]) == 0, ]$SOJUAM < 9999), "SOJUAM"]
pc2[which(pc2[(pc2[, "SOJUN"]) == 1, ]$SOJUAM < 9999), "SOJUAM"]
pc2[which(pc2[(pc2[, "SOJUN"]) == 2, ]$SOJUAM < 9999), "SOJUAM"]
pc2[which(pc2[(pc2[, "SOJUN"]) == 3, ]$SOJUAM < 9999), "SOJUAM"]



#### pc2[which(pc2[(pc2[, "SOJUN"]) == 3, ]$SOJUAM < 9999), "SOJUAM"]에서 9999가 나옴. ####
pc2[(pc2[, "SOJUN"]) == 3, ]$SOJUAM # non '9999'
sum(pc2[(pc2[, "SOJUN"]) == 3, ]$SOJUAM == 9999, na.rm=T) # non '9999'

which(pc2[(pc2[, "SOJUN"]) == 3, ]$SOJUAM < 9999)
# 애초에 위 결과가 SOJUN column == 3의 결과를 return해주지도 않는다. 
# 문제가 뭘까?

pc2[(pc2[, "SOJUN"]) == 3, ] # 1)
pc2[which((pc2[, "SOJUN"]) == 3), ] # 2) 

# 2)가 맞다. 
# 1)로는 제대로된 filtering이 되지 않는다. 
# filtering? 좀 더 간단하게 할 수 있지 않을까? 

pc2 %>% dplyr::filter(SOJUN == 3 & SOJUAM < 9999) %>% select(SOJUAM)
# Done

# which를 이용해서 할 수는 없을까?, 사실 index column 하나 만들어서 하면 해결 되긴 함. 
# Step 1. SOJUN에서 level 3 뽑아내기 
pc2 %>% dplyr::filter(SOJUN == 3)
pc2[which((pc2[, "SOJUN"]) == 3), ]

# Step 2. SOJUN == 3 & SOJUAM < 9999 뽑아내기 
pc2 %>% dplyr::filter(SOJUN == 3 & SOJUAM < 9999) %>% select(SOJUAM)
pc2[which((pc2[, "SOJUN"]) == 3), "SOJUAM"][which(pc2[which((pc2[, "SOJUN"]) == 3), "SOJUAM"] < 9999), ]

# Step 3. SOJUN == 3 & SOJUAM < 9999의 index? 
# which로 뽑으면 조건에 따라 범위가 바뀌기 때문에 위에서 사용한 방법으로 하기 어려움. 
pc2_index <- pc2 %>% mutate(index = seq(1, nrow(pc2), 1))
pc2_index %>% dplyr::filter(SOJUN == 3 & SOJUAM < 9999) %>% select(SOJUAM, index) # 1)
pc2_index[which((pc2_index[, "SOJUN"]) == 3), c("SOJUAM", "index")][which(pc2_index[which((pc2_index[, "SOJUN"]) == 3), "SOJUAM"] < 9999), ] # 2)

# dplyr와 which를 이용한 방법으로 같은 결과를 만들어냈다.
# 보면 알겠지만 dplyr, pipe를 사용하면 훨씬 직관적인 code로 결과를 만들어낼 수 있다. 
# 그러니 dplyr를 사용해서 위의 code를 바꿔주자.
#### ####

# 편의성을 위해 index column 추가 
hw2 <- hw2 %>% mutate(index = seq(1, nrow(hw2), 1))
pc2 <- pc2 %>% mutate(index = seq(1, nrow(pc2), 1))

## 사실 지금까지 이 과정을 했던 건, "가설 1 : 음주횟수의 수준 1 = 안마신다로 변경할 수 있다"를 
## 해보려고 한건데, dataset 자체에 설문지 버전을 의미하는 column이 있었다. 
## 그러니까, 설문지 버전 column을 가지고 오면 쉽게 알아볼 수 있었다는 것.

# 설문지 버전 column 추가 
hw2 <- hw2 %>% mutate(Q_ver = as.double(hw$건강기록지.버전)) %>% select(Q_ver, everything())
pc2 <- pc2 %>% mutate(Q_ver = as.double(str_replace_all(pc$설문지버전, "개인_", ""))) %>% select(Q_ver, everything())

hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 3) %>% select(-contains("_A"))
hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 3) %>% select(contains("_A"))

hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 2) %>% select(-contains("_A"))
hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 2) %>% select(contains("_A"))

hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 1) %>% select(-contains("_A"))
hw2 %>% dplyr::filter(Q_ver == 1 & ALC == 1) %>% select(contains("_A"))

# CAUTION. 건강기록지 첫번째 버전에서 술을 마시는 사람들이 '몇 번' 마시는지 모두 null value
# 일단 두고, 나중에 처리할 것. 


#### PROBLEM. 2.2.2 개인검진의 과실주를 기타술로 포함
## 해도 될까? 거-의 없는 수준 일까? 
pc2 %>% dplyr::filter(FRUITN != 0) %>% select(FRUITN, FRUITAM)
pc2 %>% dplyr::filter(ETALN != 0) %>% select(ETALN, ETNAME, ETALAM, ETALCUP)

hw2 %>% dplyr::filter(ALC_T != 0) %>% select(ALC_T, ALC_DA, ALC_A)

# 기타 술 항목 자체가 전체 obs에서 미미한 수준이다.
# NOTE. 따라서 개인검진의 과실주 항목을 기타술로 포함시켜도 될 듯.

#### PROBLEM. 2.2.3 변수 균일화
# 1. 금주 기간
## pc는 연, 개월로 나눠져 있고 hw는 연 단위임. 
## 연을 기준으로 하자. 
summary(hw2$CALC, na.rm=T)
summary(pc2$DrQYr, na.rm=T)
summary(pc2$DrQMo, na.rm=T) # 애초에 금주기간의 NA가 너무 많다. 

# CACL 생성 후 체크
pc2 %>% 
  mutate_at(vars(contains("DrQ")), ~replace(., is.na(.), 0)) %>%
  mutate(CALC = DrQYr + (DrQMo/12)) %>% 
  filter(CALC != 0) %>% 
  select(CALC, DrQYr, DrQMo)

# CACL로 DrQYr과 DrQMo를 대체 
pc2 <- pc2 %>% 
  mutate_at(vars(contains("DrQ")), ~replace(., is.na(.), 0)) %>%
  mutate(CALC = DrQYr + (DrQMo/12)) %>% 
  select(1:3, CALC, everything(), -c(DrQYr, DrQMo))

#### PROBLEM 2.2.4 중복 안되는 변수 
summary(pc2[5:6], na.rm=T)

nrow(pc2) - sum(is.na(pc2[5])) # 0 : AUDIT7은 모두 NA
nrow(pc2) - sum(is.na(pc2[6])) # 1 : AUDIT8은 하나 빼고 모두 NA

# TRY : AUDIT7, AUDIT8 삭제
pc2 <- pc2 %>% 
  select(-c(AUDIT7, AUDIT8))


#### TRY 2.2.5 rbind(hw2, pc2)
# pc2의 과실주 관련 변수를 기타에 포함시키기
## Step 1. pc2를 기준, ALC_T, ALC_A, ALC_DA 만들고 확인 
pc2 %>% 
  dplyr::filter(FRUITN != 0 | ETALN != 0) %>% 
  select(FRUITN, FRUITAM, ETALN, ETNAME, ETALAM, ETALCUP, index) %>% 
  mutate_all(~replace(., is.na(.), 0)) %>% 
  mutate(ALC_T = FRUITN + ETALN, ALC_A = ETNAME) %>% 
  mutate(ALC_DA = ifelse(ETALCUP != 0, FRUITAM + ETALAM*(ETALCUP/50), FRUITAM + ETALAM))

## Step 2. FRUIT- 변수 제거 
pc2 %>% 
  mutate_at(vars(FRUITN, FRUITAM, ETALN, ETNAME, ETALAM, ETALCUP), ~replace(., is.na(.), 0)) %>% 
  mutate(ALC_T = FRUITN + ETALN, ALC_A = ETNAME) %>% 
  mutate(ALC_DA = ifelse(ETALCUP != 0, FRUITAM + ETALAM*(ETALCUP/50), FRUITAM + ETALAM)) %>%
  select(everything(), -matches("FRUIT"), -matches("ET")) %>%
  dplyr::filter(ALC_T != 0) %>% 
  select(matches("ALC")) # 제거 후 확인함

## Step 3. pc2 대체
pc2_c <- pc2 %>% 
  mutate_at(vars(FRUITN, FRUITAM, ETALN, ETNAME, ETALAM, ETALCUP), ~replace(., is.na(.), 0)) %>% 
  mutate(ALC_T = FRUITN + ETALN, ALC_A = ETNAME) %>% 
  mutate(ALC_DA = ifelse(ETALCUP != 0, FRUITAM + ETALAM*(ETALCUP/50), FRUITAM + ETALAM)) %>%
  select(everything(), -matches("FRUIT"), -matches("ET"))

pc2_c %>% dplyr::filter(ALC_T != 0) %>% 
  select(matches("ALC")) 

pc2 %>% 
  mutate_at(vars(FRUITN, FRUITAM, ETALN, ETNAME, ETALAM, ETALCUP), ~replace(., is.na(.), 0)) %>% 
  mutate(ALC_T = FRUITN + ETALN, ALC_A = ETNAME) %>% 
  mutate(ALC_DA = ifelse(ETALCUP != 0, FRUITAM + ETALAM*(ETALCUP/50), FRUITAM + ETALAM)) %>%
  select(everything(), -matches("FRUIT"), -matches("ET")) %>%
  dplyr::filter(ALC_T != 0) %>% 
  select(matches("ALC"))

# 위의 결과가 같은 것을 확인
pc2 <- pc2_c
  

## Step 4. 변수 이름과 순서 통합 
# select하고 rename으로 바꿔줌
hw2_colnames <- colnames(hw2)

pc2_c <- pc2 %>% select(-15, 15) %>% 
  rename_all(funs(c(hw2_colnames)))

sum(pc2_c != pc2 %>% select(-15, 15), na.rm = T) # 같은 것 확인


## Step 5. TRY rbind
pc2 <- pc2_c

# CONCLUSION
df2 <- rbind(hw2, pc2)

# To DO index와 Q_ver 정리할 것. 근데 어차피 나중에 한번에 정리해야할 것 같음.

### 2.3 columns with smoking
hw3 <- hw %>% mutate(Q_ver = as.double(hw$건강기록지.버전)) %>%
  mutate(index = seq(1, nrow(hw), 1)) %>% 
  select(Q_ver, index, matches("SM")) %>% 
  type_convert(cols(SMOKST = col_double()))


pc3 <- pc %>% mutate(Q_ver = as.double(str_replace_all(pc$설문지버전, "개인_", ""))) %>% 
  mutate(index = seq(1, nrow(pc), 1)) %>% 
  select(Q_ver, index, matches("SMOK"), PTSMK, matches("SECSM")) %>% 
  type_convert(cols(SMOKST = col_double()))
