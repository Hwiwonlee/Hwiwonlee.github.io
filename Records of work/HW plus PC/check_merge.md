```r
# Merging data set

## 1. exploring raw dataset 
hw <- as.tbl(read.xlsx2('...HW_DATA.xlsx', sheetIndex=1, header=TRUE, stringsAsFactors = FALSE))
pc <- as.tbl(read.xlsx2('...PC_DATA.xlsx', sheetIndex=1, header=TRUE, stringsAsFactors = FALSE))

# dataset에  '나이'가 누락되어 있어서 추가로 import 
age <- as.tbl(read.xlsx2('...AGE.xlsx', sheetIndex=1, header=T, stringsAsFactors = FALSE))
age %>% rename(NO = NO.) %>% 
  rename(ymd = THENAME) -> age

#### NOTE. age의 ymd를날짜로 바꿔주기 ####
# import할 때 (char, int) 형태로 들어옴.
# as.Date(age$ymd, format = "%Y-%m-%d")
# 로 안바뀜 

# 차선책으로 origin을 설정해 origin 기준 integer만큼 day가 추가된 형태로 구함.
# origin 찾아서 넣음.
as.Date(as.integer(age$ymd), origin = "1899-12-30")
age$ymd <- as.Date(as.integer(age$ymd), origin = "1899-12-30")
age
# 일단 답은 나오는데, 이게 최선일까? 
####

dim(hw) # (137, 391)
dim(pc) # (227, 949)

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

#### 2.2.1 data type 비교 
which(sapply(hw1, class) == sapply(pc1, class)) # hw1과 pc1이 같은 type인 column의 이름과 자리
which(sapply(hw1, class) != sapply(pc1, class)) # hw1과 pc1이 다른 type인 column의 이름과 자리
sum(sapply(hw1, class) != sapply(pc1, class)) # 17개의 col이 다른 dtype을 갖음 

hw1[, which(sapply(hw1,class) != sapply(pc1,class))]
pc1[, which(sapply(hw1,class) != sapply(pc1,class))]
# '문자' 때문에 chr로 설정되어 있는 것을 확인
# example : hw1$CEA vs pc1$CEA, pc1$CEA가 '>0.5' 때문에 chr로 설정되어 있음. 

which(sapply(hw1, class) == "character" | sapply(pc1, class) == "character") # hw1의 col이 char거나, pc1의 col이 char인 col name과 자리
length(which(sapply(hw1, class) == "character" | sapply(pc1, class) == "character")) # 전체 26개 
 
which(sapply(hw1, class) == "character") # hw1의 col 중 char인 colname과 자리 
length(which(sapply(hw1, class) == "character")) # 19개 
which(sapply(pc1, class) == "character") # pc1의 col 중 char인 colname과 자리 
length(which(sapply(pc1, class) == "character")) # 26개 

# MORE EFFICIENT char인 pc1와 hw1의 col 중에 겹치는 것, 겹치지 않는 것 뽑아내기. 
#### GRAB-BAG ####
a <- c(which(sapply(pc1, class) == "character"), which(sapply(hw1, class) == "character")) 
length(a) # 26 + 19, hw1와 pc1의 char인 colname 합치기 

a[duplicated(a)]; length(a[duplicated(a)]) # 19개의 col이 겹침. 
a[-which(duplicated(a) | duplicated(a, fromLast = T))]; length(a[-which(duplicated(a) | duplicated(a, fromLast = T))]) # 7개의 col이 겹치지 않음. 

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

print(as.data.frame(rbind(hw1[, which(sapply(pc1, class) == "character")], pc1[, which(sapply(pc1, class) == "character")])), width = getOption("max.print"))
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

# Anti_HAVIgG, U_color, U_Turbidity : chr 
# U_Alb, U_Glucose, U_Ket, U_BIL, U_BLD, U_Uro,
# U_NIT, U_RBC, U_WBC, U_SQE : 위에서 처리 


#### ####        


# CONCLUSION df1, hw1 bind with pc1 
df1 <- rbind(hw1, pc1)



### 2.2 columns with alcohole
# 알콜 관련한 column의 base line
col_hw2 <- c("ALC", "ALCDU", "CALC",
             "BEER", "BEER_A",
             "SOJU", "SOJU_A",
             "WSKY", "WSKY_A",
             "TKJU", "TKJU_A",
             "WINE", "WINE_A",
             "ALC_A", "ALC_T",
             "ALC_DA")

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
  mutate(CALC = DrQYr + (DrQMo/12))%>% 
  dplyr::filter(CALC != 0) %>% 
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

# pc2_c와 pc2가 같은지 확인 
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


#### 2.3.1 impute the missing with "Have you ever been smoking?"
hw3 %>% select(SM) %>% drop_na() # 전체 127개에서 68개만 non-null. 나머지는?

hw3 %>% mutate_at(vars(("SM")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(SM == 77) %>% select(-matches("CSM"), -matches("CHSM")) %>%
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) -> extra_NA

extra_NA 
# 흡연여부가 NA인 obs 중 본인 흡연 관련 변수들에서 non-null을 갖는 obs가 하나도 없음.
# NOTE imputation할 근거가 없음. 

pc3 %>% select(SMOKST) %>% drop_na() # 226, 하나 제외하고 모두 non-null
nrow(pc3) # 227


#### 2.3.2 impute the missing with "Have your spouse ever been smoking?"
# Part 1. HW
hw3 %>% select(CSM) %>% drop_na() # 63

hw3 %>% select(CSM) %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) # 74개의 null

# 배우자 흡연과 관련있는 변수를 모아 74개의 null에 imputation 시행 
## 관련있는 변수들만 따로 선택 
hw3 %>% mutate_at(vars(("CSM")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(CSM == 77) %>% 
  select(-c(index, CSM), -matches("^S"), -matches("^H"), -matches("CHSM")) %>%
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) # 10개의 관련 변수 중 null 개수 

# 모두 null인 col 제외하고 관련있는 변수 선택   
hw3 %>% mutate_at(vars(("CSM")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(CSM == 77) %>% 
  select(-c(index, CSM), -matches("^S"), -matches("^H"), -matches("CHSM")) %>%
  select(-(2:6)) 
# 순서에 따라, 가족에 의한 흡연 노출, 가족에 의한 흡연 노출 - 가족
# 흡연에 노출된 시기, 흡연에 노출된 기간, 간접흡연이 이뤄지는 장소
# 결국, 배우자의 흡연 여부를 추측할 수 있는 자료는 아님. 
# NOTE 배우자의 흡연 여부 imputation 불가 

# Part 2. PC
pc3 %>% select(PTSMK) %>% drop_na() # 14

pc3 %>% select(PTSMK) %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) # 213개의 null

# 배우자 흡연과 관련있는 변수를 모아 213개의 null에 imputation 시행 
## 관련있는 변수들만 따로 선택 
pc3 %>% mutate_at(vars(("PTSMK")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(PTSMK == 77) %>% 
  select(-2, -matches("SMOK")) %>%
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) # 10개의 관련 변수 중 null 개수 
# 위의 과정이 의미 없음. 
# pc dataset에는 '배우자 흡연 유무'만 존재해서 
# 흡연량, 기간과 같이 추론할 수 있는 obs가 존재하지 않음. 
# NOTE 배우자의 흡연 여부 imputation 불가 

#### 2.3.3 impute the missing with "Have you ever been second-hand smoking?"
# part 1. HW
hw3 %>% select(matches('CSM_F')) %>%
  mutate_at(vars(("CSM_F")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(CSM_F == 77) %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.))))

# CSM_F가 null이면 다른 관련 변수도 null 
# NOTE imputation 불가. 

# Part 2. PC
pc3 %>% select(matches('SECSM')) %>%
  mutate_at(vars(("SECSM")), ~replace(., is.na(.), 77)) %>%
  dplyr::filter(SECSM == 77) %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.))))
# SECSM이 null이면 다른 관련 변수도 null
# NOTE imputation 불가 


#### 2.3.4 변수 균일화
# 흡연 유무에 대해서 hw3는 3개, pc3는 4개의 level을 가짐. 
# hw3의 level로 맞춰주자. 
## Step 1. pc3의 SMOKST의 3을 2로, 4를 3으로 바꿔줌 
pc3 %>% mutate_at(vars("SMOKST"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("SMOKST"), ~replace(., .==4, 3))

## Step 2. 제대로 바뀌었는지 index를 이용해 확인 
# 1. 바뀐 2와 바뀌기 전 3이 같은지 확인 
pc3 %>% mutate_at(vars("SMOKST"), ~replace(., .==2, 0)) %>%  # test를 위해 원래 2를 0으로 대체 
  mutate_at(vars("SMOKST"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("SMOKST"), ~replace(., .==4, 3)) %>%
  dplyr::filter(SMOKST == 2) %>% 
  select(index) # 1)

pc3 %>% dplyr::filter(SMOKST == 3) %>% 
  select(index) # 2), 1)과 2)가 같음. 

# 2. 바뀐 3와 바뀌기 전 4가 같은지 확인 
pc3 %>% mutate_at(vars("SMOKST"), ~replace(., .==2, 0)) %>%  # test를 위해 원래 2를 0으로 대체 
  mutate_at(vars("SMOKST"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("SMOKST"), ~replace(., .==4, 3)) %>%
  dplyr::filter(SMOKST == 3) %>% 
  select(index) # 1)

pc3 %>% dplyr::filter(SMOKST == 4) %>% 
  select(index) # 2) 1)과 2)가 같음 

## Step 3. 바꿔주기 
pc3 %>% mutate_at(vars("SMOKST"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("SMOKST"), ~replace(., .==4, 3)) -> pc3

sum(pc3$SMOKST == 4, na.rm=T) # 4가 남아있는지 확인, 없음. 


# 배우자의 흡연유무에 대해서는 hw3는 3개, pc3는 4개의 level을 가짐.
# hw3의 level로 맞춰추자.
pc3 %>% select(PTSMK) %>% drop_na() # 227 중 14

## Step 1. pc3의 SMOKST의 3을 2로, 4를 3으로 바꿔줌 
pc3 %>% mutate_at(vars("PTSMK"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("PTSMK"), ~replace(., .==4, 3))

## Step 2. 제대로 바뀌었는지 index를 이용해 확인 
# 1. 바뀐 2와 바뀌기 전 3이 같은지 확인 
pc3 %>% mutate_at(vars("PTSMK"), ~replace(., .==2, 0)) %>%  # test를 위해 원래 2를 0으로 대체 
  mutate_at(vars("PTSMK"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("PTSMK"), ~replace(., .==4, 3)) %>%
  dplyr::filter(PTSMK == 2) %>% 
  select(index) # 1)

pc3 %>% dplyr::filter(PTSMK == 3) %>% 
  select(index) # 2), 1)과 2)가 같음. 

# 2. 바뀐 3와 바뀌기 전 4가 같은지 확인 
pc3 %>% mutate_at(vars("PTSMK"), ~replace(., .==2, 0)) %>%  # test를 위해 원래 2를 0으로 대체 
  mutate_at(vars("PTSMK"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("PTSMK"), ~replace(., .==4, 3)) %>%
  dplyr::filter(PTSMK == 3) %>% 
  select(index) # 1)

pc3 %>% dplyr::filter(PTSMK == 4) %>% 
  select(index) # 2) 1)과 2)가 같음 

## Step 3. 바꿔주기 
pc3 %>% mutate_at(vars("PTSMK"), ~replace(., .==3, 2)) %>% 
  mutate_at(vars("PTSMK"), ~replace(., .==4, 3)) -> pc3

sum(pc3$PTSMK == 4, na.rm=T) # 4가 남아있는지 확인, 없음. 

# hw3의 HSM_Y가 '연월일'의 형태를 가지고 pc3가 금연시작 나이를 가짐.
# hw3의 형태를 pc3로 바꿔보자.

hw3 %>% mutate(NO = hw$NO) %>% 
  mutate(HSM_Y = str_replace(HSM_Y, "(-\\d+)", "")) %>% # str_replace와 rex를 이용해 바꿈. 
  # select(HSM_Y, NO) %>% 
  # drop_na() %>% 
  type_convert(cols(HSM_Y = col_double())) %>% 
  # select(NO) %>% 
  merge(age, by = 'NO') %>%  # NO를 기준으로 age와 merging 
  # select(HSM_Y, a, ymd, NO) %>% # 결과 확인
  mutate(age_Year = str_replace(ymd, "(-\\d+-\\d+)", "")) %>% # ymd에서 year만 추출 
  type_convert(cols(age_Year= col_double())) %>% 
  mutate(SMOKSP = a - (age_Year - HSM_Y)) %>%   # SMOKSP : 금연을 시작한 나이 생성 완료 
  as.tbl() %>% 
  select(c(2:27), SMOKSP) -> hw3 # SMOKSP 추가함. 137 x 27

  
#### 2.3.5 rbind()

# 기존 hw3에서 유의미한 변수들만 뽑아서 정리
# '유의미한 변수'란 pc3와 함께 볼 수 있는 변수들을 의미. 
hw3 %>% 
  select(c(SM, SM_A, SMAM, SMDU, SMOKSP, CSM, CSM_F)) -> hw3_change 

# 기존 pc3에서 유의미한 변수들만 뽑아서 정리
# '유의미한 변수'란 hw3와 함께 볼 수 있는 변수들을 의미. 
pc3 %>%
  select(c(SMOKST , SMOKAGE, SMOKDS, SMOKYR, SMOKSP, PTSMK, SECSM)) %>% 
  rename(SM = SMOKST,
         SM_A = SMOKAGE,
         SMAM = SMOKDS,
         SMDU = SMOKYR,
         CSM = PTSMK,
         CSM_F = SECSM) -> pc3_change

# rbind(hw3_change, pc3_change)
# CONCLUSION
df3 <- rbind(hw3_change, pc3_change)


#### 4. JOB 
# rawdatset의 codebook을 체크해보니 사용할 수 있는 변수가 "JOB" 밖에 없음
# 1) hw와 pc의 JOB column을 추출하고 
# 2) level을 맞춰주고
# 3) 합치기 

# 4.1 extract
hw %>% select(JOB) %>% 
  type_convert(cols(JOB = col_double())) -> hw4

pc %>% select(JOB) %>% 
  type_convert(cols(JOB = col_double())) -> pc4

# 4.2 decrirbe
# imputation 보류 
# 의사 결정 필요 
hw4 %>% group_by(JOB) %>% tally()
pc4 %>% group_by(JOB) %>% tally()


# 4.3 add index
hw4 %>% mutate(JOB_index = JOB + 0.1) -> hw4_change
pc4 %>% mutate(JOB_index = JOB + 0.2) -> pc4_change


# 4.4 rbind
# CONCLUSION
df4 <- rbind(hw4_change, pc4_change)

#### 5. 약 관련 변수

# 5.1 extract 
hw %>% 
  # 아무 영문자로 시작하고 뒤에 OC가 오는 col과 OC로 시작하는 col 선택 
  select(matches("^[A-z]OC|^OC"), index) %>% 
  type_convert(cols(OC=col_double()))-> hw5 

pc %>% 
  # OC로 시작하는 col 선택 
  select(matches("^OC"), index) %>% 
  type_convert(cols(OC=col_double()))-> pc5

# 5.2 describe 
hw5 %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) 
# OC_A와 OCDU는 모두 null, 사용나이와 기간
# HOC_A, HOCDU는 7개 non-null
# OC는 34개 non_null

pc5 %>% 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.))))
# OCYR, OCMO 15개 non_null
# OCAGE 18개 non_null
# OC 56개 non-null

# 5.3 Imputation
# TO DO. OC, HOC_A, HOCDU의 NA row가 모두 일치 하나?
# 일치하지 않는다면 그 자리의 obs를 imputation할 수 있지 않을까?
# 그럼 일치 여부를 쉽게 볼 수 있는 방법은 뭘까? 

# Step 1. hw5
hw5 %>% 
  drop_na(OC) %>% 
  drop_na(HOC_A) # 1)

hw5 %>% 
  drop_na(OC) %>% 
  drop_na(HOCDU) # 2)

# 1)과 2)의 결과가 같음. 
# 따라서 OC가 NA이나 다른 column이 값을 갖는 경우는 없음.
# 즉, imputation 불가 

# Step 2. pc5
pc5 %>% 
  dplyr::filter(is.na(OC)) %>% # OC가 na인 것만 return, 네 개의 col 모두 171개 
  select_if(function(x) any(is.na(x))) %>% 
  summarise_each(funs(sum(is.na(.)))) # 4개의 col의 NA 모두 171개
# 따라서 OC가 NA면 다른 col도 NA다. 
# 즉, imputation 불가 

# 5.4 variable scaling
# hw5.HOCDU : 과거 복용 기간, scale이 년,월인데 한 개의 column으로 표현
# 120과 180으로 추측해본 결과 '개월'이 아닐까 함.

# pc5.OCYR, pc5.OCOM : 복용 기간의 년, 월

# 두 table을 합치기 위해 단위를 '년'으로 통일하기로 함. 
# 단, 120과 180는 수정에 의사결정이 필요하므로 일단 그냥 두기로 함. 

# pc5.OCYR, pc5.OCOM를 연 단위로 바꾸기
pc5 %>% 
  dplyr::filter(!is.na(OC)) %>%
  dplyr::filter(!is.na(OCAGE)) %>% 
  mutate_at(vars(contains("OC")), ~replace(., is.na(.), 0)) %>%
  mutate(HOCDU = ifelse(OCYR != 9999 | OCMO != 9999, OCYR + (OCMO/12), 9999))
# To DO 이 코드의 문제는 mutate_at을 써서 NA를 채워 넣었기 때문에 
# 이 상태로 pc5를 업데이트하면 dataset이 손상된다. 
# merge?

pc5 %>% 
  dplyr::filter(!is.na(OC)) %>%
  dplyr::filter(!is.na(OCAGE)) %>% 
  mutate_at(vars(contains("OC")), ~replace(., is.na(.), 0)) %>%
  mutate(HOCDU = ifelse(OCYR != 9999 | OCMO != 9999, OCYR + (OCMO/12), 9999)) %>% 
  select(HOCDU, index) %>% # merge 대상인 HOCDU와 key, index 선택 
  mutate_at(vars(contains("OC")), ~replace(., . == 0 , NA)) %>% # NA는 NA로 돌려놓고 
  merge(pc5, by = "index", all = T) %>% # Outter join by index 
  as.tbl() %>% 
  select(OC, OCAGE, OCYR, OCMO, HOCDU, index) -> pc5 # 결과 확인, pc5로 대체 
  
# 5.5 rbind 
# hw5에서 의미 없는 col인 OC_A와 OCDU를 지우고
# HOC_A와 HOCDU를 OC_A, OCDU로 바꿔준다. 
# pc5는 hw5의 형식에 맞춰준다. 

hw5 %>% select(OC, HOC_A, HOCDU) %>% 
  rename(OC_A = HOC_A,
         OCDU = HOCDU) -> hw5_change

pc5 %>% rename(OC_A = OCAGE,
               OCDU = HOCDU) %>% 
  select(OC, OC_A, OCDU) -> pc5_change

# CONCLUSION
df5 <- rbind(hw5_change, pc5_change)

#### 6. 개인정보 (1)
# 6.1 extract

# TO DO 아래의 과정을 한 코드로 묶을 수는 없을까? 
# list로 출력하면 가능할 것 같은데 
# hw %>% select(MARRIG, EDULEV, ECOST) %>% 
#   type_convert(cols("MARRIG" = col_double())) %>% 
#   group_by(MARRIG) %>% arrange(MARRIG) %>% summarise(n = n())
# 
# hw %>% select(MARRIG, EDULEV, ECOST) %>% 
#   type_convert(cols(MARRIG = col_double())) %>% 
#   group_by(EDULEV) %>% arrange(EDULEV) %>% summarise(n = n())
# 
# hw %>% select(MARRIG, EDULEV, ECOST) %>% 
#   type_convert(cols(MARRIG = col_double())) %>% 
#   group_by(ECOST) %>% arrange(ECOST) %>% summarise(n = n())

#### TRY LOG ####
hw %>% select(MARRIG, EDULEV, ECOST) %>% 
  type_convert(cols(MARRIG = col_double())) %>% 
  group_by(MARRIG) %>% group_map(~ head(.x, 100L))

pc %>% select(MARRI, SCHOLA, INCOME) %>% 
  type_convert(cols(MARRI = col_double())) %>% 
  group_by(MARRI) %>% group_map(~ head(.x, 100L)) 
#### ####


sum_of_each_category_element(hw, list("MARRIG", "EDULEV", "ECOST"))
sum_of_each_category_element(pc, list("MARRI", "SCHOLA", "INCOME"))


# 6.2 Variable scaling 
# 1) MARRI는 의사결정이 필요해서 동결

# 2) EDULEV은 가능할 것 같아서 시도 : TRY 
pc %>% select(SCHOLA, index) %>% 
  type_convert(cols(MARRI = col_double())) %>% 
  mutate(EDULEV = ifelse(
    SCHOLA == 2, 1, ifelse(
      SCHOLA == 3, 2, ifelse(
        SCHOLA == 4 | SCHOLA == 5 | SCHOLA == 6, 3, ifelse(
          SCHOLA == 7 | SCHOLA == 8, 4, 
          5
            )
        )
      )
    )
    ) %>% 
  # dplyr::filter(EDULEV == 5) # check. 
  select(-SCHOLA) -> pc_6_EDULEV

# 3) ECOST도 가능할 것 같아서 시도 : TRY
## Step 1. hw의 수준이 이상해서 바꿔줌 
## 4 : [400, 700), 5 : 400 이상, 6 : 700 이상.
## 4 : 4 + 5, 5 : 6 으로 
  
hw %>% select(ECOST, index) %>% 
  type_convert(cols(ECOST = col_double())) %>% 
  mutate(ECOST = ifelse(
    ECOST == 4 | ECOST == 5, 4, ifelse(
      ECOST == 6, 5, ifelse(
        ECOST == 7, 6, ECOST
      )
    )
  )
  ) -> hw_6_ECOST
  

sum_of_each_category_element(hw, list("ECOST"))
sum_of_each_category_element(hw_6_ECOST, list("ECOST")) # 체크 완료 

## Step 2. pc의 수준 맞춰주기
## 9 : 기타를 6: 잘모름으로 바꿔줌

pc %>% select(INCOME, index) %>% 
  type_convert(cols(INCOME = col_double())) %>% 
  mutate(ECOST = ifelse(
    INCOME == 9, 6, INCOME
  )) %>%
  select(ECOST, index) -> pc_6_ECOST

sum_of_each_category_element(pc, list("INCOME"))
sum_of_each_category_element(pc_6_ECOST, list("ECOST")) # 체크 완료 


## Step 3. rbind
hw %>% select(MARRIG, EDULEV, index) %>% 
  type_convert(cols(MARRIG = col_double())) %>% 
  merge(hw_6_ECOST, by = "index", all = T) %>% 
  as.tibble() -> hw6

sum_of_each_category_element(hw, list("MARRIG", "EDULEV", "ECOST"))
sum_of_each_category_element(hw6, list("MARRIG", "EDULEV", "ECOST")) # 변경 사항 체크 완료


pc %>% select(MARRI, index) %>% 
  type_convert(cols(MARRI = col_double())) %>% 
  merge(pc_6_EDULEV, by = "index", all = T) %>% 
  merge(pc_6_ECOST, by = "index", all = T) %>%
  rename(MARRIG = MARRI) %>% 
  as.tibble() -> pc6

sum_of_each_category_element(pc, list("MARRI", "SCHOLA", "INCOME"))
sum_of_each_category_element(pc6, list("MARRIG", "EDULEV", "ECOST")) # 변경 사항 체크 완료


# CONCLUSION
df6 <- rbind(hw6, pc6)



#### 7. MENA 관련 정보
# 7.1 extract
hw %>% 
  select(matches("^MENA|^MPER|LMP|MENO|HORMONE|^LAC|^FAIL|FDEL"), 
         -matches("FAILURE$|MENO$|O_A$")) %>% 
  type_convert(cols(MENA = col_double()))-> hw7
# %>% names(.)로 colname 뽑을 수 있음. 

pc %>% 
  select(matches("^MEN|^LMP|^HRT$|^BRFEED$|^BRFEEDN$|^SAB$|^AAB$|^FPR"), 
         -matches("^MENDRE$|MENSDU")) %>% 
  type_convert(cols(MENAGE = col_double()))-> pc7


#### 7.2 decrirbe
dim(hw7); dim(pc7)
names(pc7)
names(hw7)

#### 7.3 variable handling 
sum_of_each_category_element(pc7, list("MENARCH"))
sum_of_each_category_element(hw7, list("MENA"))

hw7 %>%
  select(LMP) %>% drop_na()

# hw7는 LMP, pc7는 LMPM, LMPD로 되어 있기 때문에
# hw7의 형식으로 맞춰줌
pc7 %>%
  # LMPM이 10보다 크면 바로 paste, 작으면 0을 붙여서 paste
  mutate(LMP = ifelse(LMPM >= 10, # TO DO paste 좀 더 깔끔하게 할 수 없을까? 
                      paste(LMPM, LMPD, sep = "-"), 
                      paste(0, paste(LMPM, LMPD, sep = "-"), sep = ""))) %>% 
  
  select(-c(LMPM, LMPD)) -> pc7_change # LMPM과 LMPD 삭제 

# pc7.MENORETC가 null이므로 삭제 
pc7 %>% 
  select(MENORETC) %>% drop_na()

pc7_change %>% select(-MENORETC) -> pc7_change

names(pc7)
names(hw7)

#### 7.4 renaming
pc7_change %>%
  rename(MENA_A = MENAGE, 
         MENA = MENARCH, 
         MPERID1 = MENREG,
         MPERID2 = MENSPE,
         MENO_D = MENOAGE, 
         MENO_RES = MENORE,
         HORMONE = HRT,
         LACTATION = BRFEED, 
         LAC_NO = BRFEEDN,
         FAILURE1_T = SAB,
         FAILURE2_T = AAB,
         FDEL_A= FPRAGE) %>% 
  select(names(hw7)) -> pc7_change

#### 7.5 rbind
df7 <- rbind(hw7, pc7_change)
# CONCLUSION
#### CAUTION ####
# variable scaling을 하지 않음.
# MENA, HORMONE에 대한 의사결정 필요함. 

#### 8. EXFQ
# 8.1 extract
hw %>% 
  select(EXFQ, EXAM, DAY_WALK, SPORT, SPORT_K, SPORT_T, SPORT2_K, index) %>% 
  type_convert(cols(EXFQ = col_double())) -> hw8

pc %>% 
  select(VIGORD, VIGORM, WALKH, PA, PA1_KIND, PA1_HR, PA2_KIND, index) %>% 
  type_convert(cols(VIGORD = col_double())) -> pc8

sum_of_each_category_element(hw8, list("EXFQ", "EXAM"))
sum_of_each_category_element(pc8, list("VIGORD", "VIGORM"))


# 8.2 variable handling

# 1) VIGORM : 0을 60, 11을 70으로 교체 
pc8 %>% 
  mutate(VIGORM = ifelse(VIGORM == 0, 60,
                         ifelse(VIGORM == 11, 70, VIGORM))) -> pc8_change
  


# 2) hw.SPORT_T : categorical, pc.PA1_HR : descrete
# categorical로 맞춰주기 
sum_of_each_category_element(hw8, list("SPORT_T"))
sum_of_each_category_element(pc8_change, list("PA1_HR"))

pc8_change %>% 
  # PA1_HR : 0 or 9999인 obs의 다른 value는 어떻게 되어 있는지 확인 
  dplyr::filter(PA1_HR == 0 | PA1_HR == 9999) 
  # EX는 하지만 얼마나 하는지는 모르는 obs로 보임. 일단 두자. 


# 구간에 맞춰 categorical로 정리 
pc8_change %>% 
  # select(PA1_HR) %>% 
  mutate(SPORT_T = ifelse(PA1_HR < 1, 1,
                          ifelse(PA1_HR < 2, 2,
                                 ifelse(PA1_HR < 3, 3,
                                        ifelse(PA1_HR < 4, 4,
                                               ifelse(PA1_HR < 9999, 5, PA1_HR)))))) %>% 
  # sum_of_each_category_element(., list("PA1_HR", "SPORT_T")) # 체크 완료 
  select(-PA1_HR) -> pc8_change # PA1_HR 삭제 
  


# 3) hw.DAY_WALK : categorical, pc.WALKH : descrete
# descrete를 categorical로 맞춰주기. 

sum_of_each_category_element(hw8, list("DAY_WALK"))
sum_of_each_category_element(pc8_change, list("VIGORM"))

# 0이 있는게 이상해서 찾아보니 WALKM이 있음. 
# WALKM이 true인 경우를 찾아서 mutate해야할 것 같음. 

pc %>% 
  select(WALKH, WALKM, index) %>% 
  type_convert(cols(.=col_double())) %>% 
  dplyr::filter(WALKH != "NA" | WALKM != "NA") %>% 
  mutate_at(vars(("WALKH")), ~replace(., is.na(.), 0)) %>% 
  mutate(DAY_WALK = ifelse(WALKH == 0 & WALKM < 5, 1, 
                           ifelse(WALKH == 0 &WALKM < 15, 2,
                                 ifelse(WALKH == 0  & WALKM < 30, 3,
                                       ifelse(WALKH == 0  & WALKM < 45, 4,
                                             ifelse(WALKH != 0 | WALKH != "NA", 5, WALKH)))))
         ) %>% # %>% dplyr::filter(WALKM < 10) 체크 완료  
  merge(pc8_change, by = "index", all.y=T) %>% 
  as_tibble() %>% 
  select(-matches("H.x$")) %>% # %>% names()
  select(-matches("WALK.")) -> pc8_change


# 8.3 rename
pc8_change %>% 
  rename(EXFQ = VIGORD,
         EXAM = VIGORM,
         SPORT = PA,
         SPORT_K = PA1_KIND,
         SPORT2_K = PA2_KIND) %>% 
  select(names(hw8)) -> pc8_change


# 8.4 rbind
df8 <- rbind(hw8, pc8_change)









#### DEFINING ####

sum_of_each_category_element <- function(df, target) {
  # dataset과 dataset의 column을 받아 
  # column 기준에서 각 column이 몇 개의 category를 갖고 있으며
  # 각 category마다 몇 개의 element를 갖고 있는지 보여주기 위한 function
  
  # 결과 공간 생성
  # 여러 개의 결과를 한번에 보여주려면 list가 좋을 듯
  # ? list에 빈 공간 어떻게 만들더라? 
  l <- list()
  
  # n개의 column을 반복하기 위한 for문
  for(i in 1:length(target)){
    df %>% select(target) %>% # df에서 target column을 선택 
      type_convert(cols(target[i] = col_double())) %>% # 편의를 위해 col type 변경 
      
      # 12.20 error
      # 아마 target[i]로 처리가 안되는 것 같음.
      # character를 받아올 수 없나? 

      # SOLUTION : 하단 참조       
      
      group_by(target[i]) %>% # i번째 col을 기준으로 group_by
      arrange(target[i]) %>% # @ 굳이 arrange할 필요가 있을까? 
      summarise(n = n()) -> l[[length(l)+1]] # element 계산을 위한 summarise 
  }
  return(l)  

}

## SOLUTION ##
hw %>% select(target) %>% 
  type_convert(cols(target = col_double())) -> test_df

target <- list("MARRIG", "EDULEV", "ECOST")

## 단 한 줄의 코드로 원하는 결과를 얻어올 수 있음. 
df_list <- lapply(target, function(i) group_by(test_df, .dots=i) %>%summarise(n = n()))
## SOLUTION ##

#### FUNCTION 1 ####
sum_of_each_category_element <- function(df, target) {
  
  a <- unlist(target)[1]
   
  df %>% select(unlist(target)) %>% 
    type_convert(cols(a = col_double())) -> test_df
  
  df_list <- lapply(target, function(i) group_by(test_df, .dots=i) %>%summarise(n = n()))
  
  return(df_list)
   
}
#### FUNCTION 1 
