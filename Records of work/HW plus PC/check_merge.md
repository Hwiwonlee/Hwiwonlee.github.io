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

#### 2.2.1 건강기록지와 건강검진의 '음주횟수' 수준이 다르다. 
# coding book 기준, 각각 1~8, 0~7 이므로 reference를 0에 맞추면 해결 가능.

# 새로운 문제 : 첫번째 건강기록지의 음주횟수 수준이 6개로 차이가 있다.
## 가설 1. 1st 건강기록지의 음주횟수 수준에는 '안 마신다'가 포함되어 있지 않다. 
##         따라서, 첫번째 수준을 갖지만 '음주량'에 value가 들어가 있으면 음주횟수를 조정한다. 
##         => 1st 건강기록지를 제외한 나머지 질문지의 음주횟수 첫번째 수준은 '안 마신다'이므로 '안 마시는 사람'이 '음주량'을 갖고 있을 수 없다고 가정한다. 

# 소주를 예로 들어 시도해보자. 
hw2[na.omit(hw2[, "SOJU"]) == 1, "SOJU_A"]
hw2[(hw2[, "SOJU"]) == 1, ]$SOJU_A
hw2[(hw2[, "SOJU"]) == 2, ]$SOJU_A
hw2[(hw2[, "SOJU"]) == 3, ]$SOJU_A

pc2[(pc2[, "SOJUN"]) == 0, ]$SOJUAM
pc2[(pc2[, "SOJUN"]) == 1, ]$SOJUAM


# 12.17, 음주횟수 및 음주량이 중복응답 가능해서 table 전체를 봐야 할 것 같음. 


# 모르는 경우, 건강기록지는 99, 개인검진은 9999
sum(hw2 == 99, na.rm = T) # 31
sum(pc2 == 9999, na.rm = T) # 4 

pc2 %>% dplyr::filter(SOJUAM == 9999 | BEERAM == 9999 | GINAM == 9999 | RICEAM == 9999 | WINEAM == 9999)  
# 음주량을 모르는 경우 3개
hw2 %>% dplyr::filter(SOJU_A == 99)
hw2[, 4:16] %>% dplyr::filter(SOJU_A == 99 | BEER_A == 99 | WSKY_A == 99 | TKJU_A == 99 | WINE_A == 99) 
# 음주량을 모르는 경우 14개 



# 개인검진의 과실주를 기타술로 포함
## 해도 될까? 거-의 없는 수준 일까? 
na.omit(pc2[(pc2[, "FRUITN"]) != 0, "FRUITN"])
na.omit(pc2[(pc2[, "ETALN"]) != 0, "ETALN"])
na.omit(pc2[, "ETNAME"])

na.omit(hw2[(hw2[, "ALC_T"]) != 0, "ALC_T"])
na.omit(hw2[(hw2[, "ALC_T"]) != 0, "ALC_DA"])
na.omit(hw2[, "ALC_A"])

# 기타 술 항목 자체가 전체 obs에서 미미한 수준이다.
# 따라서 개인검진의 과실주 항목을 기타술로 포함. 
```
