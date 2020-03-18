
숙원사업 : 코드 정리하기:금토일  
1페이즈 끝 코드 함수화  
 
LOG  

[Function to pass parameter to perform group_by in R](https://stackoverflow.com/questions/55246913/function-to-pass-parameter-to-perform-group-by-in-r)  
[Plot every column in a data frame as a histogram on one page using ggplot](https://stackoverflow.com/questions/13035834/plot-every-column-in-a-data-frame-as-a-histogram-on-one-page-using-ggplot)  
[Outlier detection and treatment with R](https://www.r-bloggers.com/outlier-detection-and-treatment-with-r/)  
[GGPlot Legend Title, Position and Labels](https://www.datanovia.com/en/blog/ggplot-legend-title-position-and-labels/#change-legend-title)  
[Plot multiple boxplot in one graph](https://stackoverflow.com/questions/14604439/plot-multiple-boxplot-in-one-graph)  

[color palette in r](http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf)  

[3. PCA, in mixomics vignett](https://mixomicsteam.github.io/Bookdown/pca.html#principle-of-pca)  
[ggplot2 point shapes](http://www.sthda.com/english/wiki/ggplot2-point-shapes)  
[plsda: Partial Least Squares Discriminant Analysis (PLS-DA)](https://rdrr.io/cran/mixOmics/man/plsda.html)  

[Lasso 1)](https://rpubs.com/baekdata/CVLASSO)   
[Lasso 2)](https://niceguy1575.tistory.com/64)  
[Lasso 3)](https://stats.stackexchange.com/questions/156098/cross-validating-lasso-regression-in-r)  

## 1. preprocessing

## 2. EDA by visualization
### 2.1 Check each variable's distribution using Histogram and boxplot

## 3. Analysis
### 3.1 Conditional Logistic Regression
#### 3.1.1 Simple 
#### 3.1.2 Multiple 


```r
dir = dir

library(xlsx)
data_BN <- read.xlsx(paste(dir, "BN_sheet.xlsx", sep= "/"), sheetIndex = 1, stringsAsFactors=FALSE)
data_MN <- read.xlsx(paste(dir, "MN_sheet.xlsx", sep= "/"), sheetIndex = 1, stringsAsFactors=FALSE)
data_raw <- read.xlsx(paste(dir, "RAW_sheet.xlsx", sep= "/"), sheetIndex = 1, stringsAsFactors=FALSE)


colnames(data_BN)[1:6] <- c("Name", "NO", "Group", "Group_RN", "Batch", "Order")
colnames(data_MN)[1:4] <- c("Name", "NO", "Group", "Group_RN")
colnames(data_raw)[1:4] <- c("Name", "NO", "Group", "Group_RN")

data_BN <- data_BN[-1, ]
data_MN <- data_MN[-1, ]
data_raw <- data_raw[-1, ]


data_BN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>%
  
  # metabolites 결과에서 붙어나온 .Results를 삭제 
  rename_at(vars(matches(".Results$")), funs(str_replace(., ".Result", ""))) %>% 
  
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_BN

data_MN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  
  # metabolites 결과에서 붙어나온 .Results를 삭제 
  rename_at(vars(matches(".Results$")), funs(str_replace(., ".Result", ""))) %>% 
  
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_MN

data_raw %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  
  # metabolites 결과에서 붙어나온 .Results를 삭제 
  rename_at(vars(matches(".Results$")), funs(str_replace(., ".Result", ""))) %>% 
  
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_raw

data_BN %>% 
  group_by(Group) %>%  summarise(n=n())


data_info <- read.xlsx(paste(dir, "info_sheet.xlsx", sep = "/"), header=FALSE, sheetIndex = 1, stringsAsFactors=FALSE)
data_info <- data_info[-1, ]
names(data_info) <- c("NCC_num", "Group_RN", "TB_num", "NO", "sex", "age", "smoking", "alcohol", "주장기", "stage_raw", "stage", "box", "위치")

data_info %>% 
  type_convert(cols(NO = col_double())) -> data_info

data_info %>% 
  group_by(smoking, alcohol) %>% 
  summarise(n = n())

metabolites_list <- read.xlsx(paste(dir, "name_map.xlsx", sep = "/"), sheetIndex = 1, stringsAsFactors=FALSE)

data_stage <- read.xlsx(paste(dir, "OC stage info.xlsx", sep = "/"), header=TRUE, sheetIndex = 1, stringsAsFactors=FALSE)
data_stage %>% 
  mutate(site = replace(site, site == "Buccal혻Mucosa", "Buccal Mucosa")) -> data_stage



# 공백 제거 
metabolites_name <- gsub(" $", "", metabolites_list$Match) 
length(metabolites_name) # 91개  
length(metabolites_name[-which(metabolites_list$Match == "NA")]) # 81개


#### ####

#### <TO do> Oral cancer & metabolites는 1:2 matching이니까 set value를 하나 만들자. ####
#### OLD ####
case_interval = 3
control_interval = 1

set_case = seq(1, 546, case_interval)
set_control = seq(1, 546, control_interval)[-set_case]
set_pre = c()  

n <- 1
m <- 1

for (i in 1:546) {
  j <- 1
  
  if (data_BN$Group[i] == "OC"){
    set_pre[i] <- set_case[n]
    n = n+1
  } else {
    set_pre[i] <- set_control[m]
    m = m+1
  }
}

set = c()
for (i in 1:(546/case_interval)) {
  a = rep(i, case_interval)
  set = c(set, a)
}


data_BN %>% 
  dplyr::filter(Group != "QC") %>% 
  mutate(set_pre = set_pre) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  select(set_pre, Group, everything()) %>% 
  arrange(set_pre) %>% 
  mutate(set = set) %>%
  select(set, everything()) %>% 
  arrange(set) 
#### OLD ####

#### NEW ####
# OC 기준, AGE와 SEX를 이용해 1:2 matching을 함. 
# AGE의 matching 기준은 OC의 AGE +- 2 

data_BN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  select(NO, Group, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_BN

data_MN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  select(NO, Group, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_MN

data_raw %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  select(NO, Group, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_raw


# age merge 결과 체크 
sum(data_BN$age != data_info$age) # 같음 
sum(data_MN$age != data_info$age) # 같음  
sum(data_raw$age != data_info$age) # 같음 

#### age +-2의 match가 가능한 지 판단하자 ####
data_BN %>% 
  dplyr::filter(Group == "OC" & sex == 1) %>% 
  arrange(age)

data_BN %>% 
  dplyr::filter(Group == "C" & sex == 1) %>% 
  arrange(age)

data_BN %>% 
  dplyr::filter(Group == "OC" & sex == 2) %>% 
  arrange(age)

data_BN %>% 
  dplyr::filter(Group == "C" & sex == 2) %>% 
  arrange(age)
# 아무리 봐도 +-2로 matching이 안되는데 

# 시각화를 이용한 확인 
data_BN %>% 
  dplyr::filter(sex == 2) %>% 
  ggplot(., aes(x = age, fill = Group)) +
  geom_histogram(binwidth = 1)

data_BN %>% 
  dplyr::filter(sex == 1) %>% 
  ggplot(., aes(x = age, fill = Group)) +
  geom_histogram(binwidth = 1)
# 역시나 +-2로 딱 떨어지는 matching이 안된다. 

data_BN %>% 
  dplyr::filter(sex == 1 & age < 35) %>% 
  ggplot(., aes(x = age, fill = Group)) +
  geom_histogram(binwidth = 1)

#### age +-2로 딱 떨어지는 match는 불가능하다고 판단 ####

#### 1차 시도, 쉽게 생각하는 matching 방법 ####
# 동일 성별의 OC, C 그룹을 나이순으로 정렬하고 1:2매칭을 하면 되지 않을까? 

# sex == 1의 경우

data_BN %>% 
  dplyr::filter(Group == "OC" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test1.1

data_BN %>% 
  dplyr::filter(Group == "C" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test1.2

data_BN %>% 
  dplyr::filter(Group == "OC" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test2.1

data_BN %>% 
  dplyr::filter(Group == "C" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test2.2

data_MN %>% 
  dplyr::filter(Group == "OC" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test3.1

data_MN %>% 
  dplyr::filter(Group == "C" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test3.2

data_MN %>% 
  dplyr::filter(Group == "OC" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test4.1

data_MN %>% 
  dplyr::filter(Group == "C" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test4.2

data_raw %>% 
  dplyr::filter(Group == "OC" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test5.1

data_raw %>% 
  dplyr::filter(Group == "C" & sex == 1) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test5.2

data_raw %>% 
  dplyr::filter(Group == "OC" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = seq(1, nrow(.), 1)) %>% 
  select(set, everything()) -> test6.1

data_raw %>% 
  dplyr::filter(Group == "C" & sex == 2) %>% 
  arrange(age) %>% 
  mutate(set = rep(1:(nrow(.)/2), each = 2)) %>% 
  select(set, everything()) -> test6.2



test1.1 %>% 
  rbind(test1.2) %>% 
  arrange(set) %>% 
  # select(set, age) %>% 
  ggplot(., aes(x=set, y=age, colour = Group)) + 
  geom_point()
  
test2.1 %>% 
  rbind(test2.2) %>% 
  arrange(set) %>% 
  # select(set, age) %>% 
  ggplot(., aes(x=set, y=age, colour = Group)) + 
  geom_point()


test2.1 %>% 
  rbind(test2.2) %>% 
  mutate(set = set + 121) %>% 
  rbind(test1.1, test1.2) %>% 
  arrange(set) -> data_BN_add_set

test4.1 %>% 
  rbind(test4.2) %>% 
  mutate(set = set + 121) %>% 
  rbind(test3.1, test3.2) %>% 
  arrange(set) -> data_MN_add_set

test6.1 %>% 
  rbind(test6.2) %>% 
  mutate(set = set + 121) %>% 
  rbind(test5.1, test5.2) %>% 
  arrange(set) -> data_raw_add_set

data_BN_add_set %>% 
  ggplot(., aes(x=set, y=age, colour = Group)) + 
  geom_point()

data_MN_add_set %>% 
  ggplot(., aes(x=set, y=age, colour = Group)) + 
  geom_point()

data_raw_add_set %>% 
  ggplot(., aes(x=set, y=age, colour = Group)) + 
  geom_point()

#### 1차 시도, 쉽게 생각하는 matching 방법 ####
data_BN_add_set # 1차 시도 결과 
data_MN_add_set # 1차 시도 결과 
data_raw_add_set # 1차 시도 결과 

#### BN handling ####
data_BN_add_set %>% 
  select(set, Group, NO, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_BN_add_set

names(data_BN_add_set) <- c("set", "Group", "NO", "sex", "age", "smoking", "alcohol",
                            "stage_raw", "stage", "Name", "Group_RN.x",
                            "Batch", "order", metabolites_name, 
                            "NCC_num", "Group_RN.y", "TB_num", "주장기", "box", "위치")

data_BN_add_set <- data_BN_add_set[, -which(names(data_BN_add_set) == 'NA')]


## 1a, 4a, 4b 발견 
data_BN_add_set %>% 
  mutate(stage = gsub("^4[a-z]", "4", stage)) %>% 
  mutate(stage = gsub("^1[a-z]", "1", stage)) %>% 
  
  ## stage 수정 후 stage 별 n개 체크, 수정 완료 
  # group_by(stage) %>% summarise(n = n())
  mutate(stage = gsub("-", "0", stage)) %>% 
  mutate(stage = replace_na(stage, "0")) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  mutate(age = as.numeric(cut_number(.$age, 3)))%>% 
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> data_BN_add_set_ready

data_BN_add_set_ready %>% 
  
  # 쓸모없는 변수 제거 
  select(-c(stage_raw, NO, Name, Group_RN.x,
            Batch, order, NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) %>% 
  
  # formula를 위해 X value names에 공백 제거 
  rename_at(vars(matches(" ")), funs(str_replace(., " ", "_"))) %>% 
  # formula를 위해 X value names에 dash 제거 
  rename_at(vars(matches("-")), funs(str_replace_all(., "-", "_"))) %>% 
  # 숫자가 포함되어있는 metabolites를 HMDB를 참고, 이름 바꿔줌
  rename(beta_Hydroxybutyric_acid = '3_Hydroxybutyric_acid', 
         Methyl_folate = '5_Methyltetrahydrofolic_acid',
         Hydroxy_L_proline = '4_Hydroxyproline') -> BN_info_add_set


# Use logarithm
BN_info_add_set_log <- cbind(BN_info_add_set[, 1:7], log(BN_info_add_set[, 8:88]))
BN_info_add_set_log[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_add_set_log[, -(1:7)])

# Use Standardization
BN_info_add_set_st <- cbind(BN_info_add_set[, 1:7], scale((BN_info_add_set[, 8:88]), T, T))
BN_info_add_set_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_add_set_st[, -(1:7)])

# Use rescaling [0-1], https://gist.github.com/Nicktz/b06e7afcb52db888a10ee28da3d2f589
BN_info_add_set %>% 
  mutate_each_(funs(rescale), vars = names(.)[-(1:7)]) -> BN_info_add_set_re

# Use log + Standardization
BN_info_add_set_log_st <- cbind(BN_info_add_set[, 1:7], log(BN_info_add_set[, 8:88]))
BN_info_add_set_log_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_add_set_log_st[, -(1:7)])
BN_info_add_set_log_st[, -(1:7)] <- scale(BN_info_add_set_log_st[, -(1:7)], T, T)

# 새로 넣은 set을 이용한 CLR 
# simple 
raw_result_add_set <- UsCLR(BN_info_add_set, c(1,2,7))
raw_result_add_set[[1]]

# multiple
summary(clogit(formula = formula_special, data = BN_info_add_set,
               control = coxph.control(iter.max = 1000)))


BN_info_add_set %>% 
  mutate(set = as.factor(set),
         Group = as.factor(Group),
         sex = as.factor(sex),
         smoking = as.factor(smoking),
         alcohol = as.factor(alcohol),
         age = as.factor(age)) -> BN_info_add_set


clogistic(Group ~ age + smoking + alcohol + beta_Hydroxybutyric_acid + 
            Methyl_folate + Acetoacetic_acid + L_Acetylcarnitine + Acetylcholine + 
            Adenine + Adenosine + Asymmetric_dimethylarginine + L_Alanine + 
            Adenosine_monophosphate + L_Arginine + Ascorbic_acid + L_Asparagine + 
            L_Aspartic_acid + Betaine + Butyrylcarnitine + L_Carnitine + 
            Choline + Citrulline + Creatine + Creatinine + L_Cystathionine + 
            L_Cysteine + Decanoylcarnitine + Dimethylglycine + Fumaric_acid + 
            Gamma_Aminobutyric_acid + L_Glutamic_acid + L_Glutamine + 
            Oxidized_glutathione + Glycine + Glycochenodeoxycholic_acid + 
            Glycocholic_acid + Guanine + Hexanoylcarnitine + Hippuric_acid + 
            L_Histidine + Hypoxanthine + Inosine + Isovalerylcarnitine + 
            L_Isoleucine + L_Kynurenine + Lactate + Dodecanoylcarnitine + 
            L_Leucine + L_Lysine + L_Methionine + N_Acetyl_L_aspartic_acid + 
            NAD + Niacinamide + Nicotinic_acid + Nicotinuric_acid + Norepinephrine + 
            L_Octanoylcarnitine + L_Phenylalanine + Propionylcarnitine + 
            L_Proline + Pyridoxamine + Pyridoxine + Pyroglutamic_acid + 
            Riboflavin + S_Adenosylhomocysteine + S_Adenosylmethionine + 
            L_Serine + Glycerophosphocholine + Succinic_acid + Taurine + 
            L_Threonine + Thymine + Trimethylamine_N_oxide + Hydroxy_L_proline + 
            Trigonelline + L_Tryptophan + L_Tyrosine + Uracil + Urea + 
            Uric_acid + Uridine + L_Valine + Xanthine + Xanthosine, strata = set, 
          BN_info_add_set, iter.max = 5000)

# 큰 의미 없음. 

# boxplot 
ggplot(melt(BN_info_add_set_re[, -c(1:7)]), aes(x = variable, y = value)) + 
  geom_boxplot() + theme_minimal()

#### BN handling ####

#### MN handling ####
data_MN_add_set %>% 
  select(set, Group, NO, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_MN_add_set

names(data_MN_add_set) <- c("set", "Group", "NO", "sex", "age", "smoking", "alcohol",
                            "stage_raw", "stage", "Name", "Group_RN.x",
                            metabolites_name, 
                            "NCC_num", "Group_RN.y", "TB_num", "주장기", "box", "위치")

data_MN_add_set <- data_MN_add_set[, -which(names(data_MN_add_set) == 'NA')]


## 1a, 4a, 4b 발견 
data_MN_add_set %>% 
  mutate(stage = gsub("^4[a-z]", "4", stage)) %>% 
  mutate(stage = gsub("^1[a-z]", "1", stage)) %>% 
  
  ## stage 수정 후 stage 별 n개 체크, 수정 완료 
  # group_by(stage) %>% summarise(n = n())
  mutate(stage = gsub("-", "0", stage)) %>% 
  mutate(stage = replace_na(stage, "0")) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  mutate(age = as.numeric(cut_number(.$age, 3)))%>% 
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> data_MN_add_set_ready

data_MN_add_set_ready %>% 
  
  # 쓸모없는 변수 제거 
  select(-c(stage_raw, NO, Name, Group_RN.x,
            NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) %>% 
  
  # formula를 위해 X value names에 공백 제거 
  rename_at(vars(matches(" ")), funs(str_replace(., " ", "_"))) %>% 
  # formula를 위해 X value names에 dash 제거 
  rename_at(vars(matches("-")), funs(str_replace_all(., "-", "_"))) %>% 
  # 숫자가 포함되어있는 metabolites를 HMDB를 참고, 이름 바꿔줌
  rename(beta_Hydroxybutyric_acid = '3_Hydroxybutyric_acid', 
         Methyl_folate = '5_Methyltetrahydrofolic_acid',
         Hydroxy_L_proline = '4_Hydroxyproline') -> MN_info_add_set


# Use logarithm
MN_info_add_set_log <- cbind(MN_info_add_set[, 1:7], log(MN_info_add_set[, 8:88]))
MN_info_add_set_log[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), MN_info_add_set_log[, -(1:7)])

# Use Standardization
MN_info_add_set_st <- cbind(MN_info_add_set[, 1:7], scale((MN_info_add_set[, 8:88]), T, T))
MN_info_add_set_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), MN_info_add_set_st[, -(1:7)])

# Use rescaling [0-1], https://gist.github.com/Nicktz/b06e7afcb52db888a10ee28da3d2f589
MN_info_add_set %>% 
  mutate_each_(funs(rescale), vars = names(.)[-(1:7)]) -> MN_info_add_set_re

# Use log + Standardization
MN_info_add_set_log_st <- cbind(MN_info_add_set[, 1:7], log(MN_info_add_set[, 8:88]))
MN_info_add_set_log_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), MN_info_add_set_log_st[, -(1:7)])
MN_info_add_set_log_st[, -(1:7)] <- scale(MN_info_add_set_log_st[, -(1:7)], T, T)

# 새로 넣은 set을 이용한 CLR 
# simple 
raw_result_add_set <- UsCLR(MN_info_add_set, c(1,2,7))
raw_result_add_set[[1]]

# multiple
summary(clogit(formula = formula_candi, data = MN_info_add_set,
               control = coxph.control(iter.max = 1000)))


MN_info_add_set %>% 
  mutate(set = as.factor(set),
         Group = as.factor(Group),
         sex = as.factor(sex),
         smoking = as.factor(smoking),
         alcohol = as.factor(alcohol),
         age = as.factor(age)) -> MN_info_add_set


clogistic(Group ~ age + smoking + alcohol + beta_Hydroxybutyric_acid + 
            Methyl_folate + Acetoacetic_acid + L_Acetylcarnitine + Acetylcholine + 
            Adenine + Adenosine + Asymmetric_dimethylarginine + L_Alanine + 
            Adenosine_monophosphate + L_Arginine + Ascorbic_acid + L_Asparagine + 
            L_Aspartic_acid + Betaine + Butyrylcarnitine + L_Carnitine + 
            Choline + Citrulline + Creatine + Creatinine + L_Cystathionine + 
            L_Cysteine + Decanoylcarnitine + Dimethylglycine + Fumaric_acid + 
            Gamma_Aminobutyric_acid + L_Glutamic_acid + L_Glutamine + 
            Oxidized_glutathione + Glycine + Glycochenodeoxycholic_acid + 
            Glycocholic_acid + Guanine + Hexanoylcarnitine + Hippuric_acid + 
            L_Histidine + Hypoxanthine + Inosine + Isovalerylcarnitine + 
            L_Isoleucine + L_Kynurenine + Lactate + Dodecanoylcarnitine + 
            L_Leucine + L_Lysine + L_Methionine + N_Acetyl_L_aspartic_acid + 
            NAD + Niacinamide + Nicotinic_acid + Nicotinuric_acid + Norepinephrine + 
            L_Octanoylcarnitine + L_Phenylalanine + Propionylcarnitine + 
            L_Proline + Pyridoxamine + Pyridoxine + Pyroglutamic_acid + 
            Riboflavin + S_Adenosylhomocysteine + S_Adenosylmethionine + 
            L_Serine + Glycerophosphocholine + Succinic_acid + Taurine + 
            L_Threonine + Thymine + Trimethylamine_N_oxide + Hydroxy_L_proline + 
            Trigonelline + L_Tryptophan + L_Tyrosine + Uracil + Urea + 
            Uric_acid + Uridine + L_Valine + Xanthine + Xanthosine, strata = set, 
          MN_info_add_set, iter.max = 5000)

# 큰 의미 없음. 

# boxplot 
ggplot(melt(MN_info_add_set_re[, -c(1:7)]), aes(x = variable, y = value)) + 
  geom_boxplot() + theme_minimal()
#### MN handling ####

#### raw handling ####
data_raw_add_set %>% 
  select(set, Group, NO, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_raw_add_set

names(data_raw_add_set) <- c("set", "Group", "NO", "sex", "age", "smoking", "alcohol",
                            "stage_raw", "stage", "Name", "Group_RN.x",
                            metabolites_name, 
                            "NCC_num", "Group_RN.y", "TB_num", "주장기", "box", "위치")

data_raw_add_set <- data_raw_add_set[, -which(names(data_raw_add_set) == 'NA')]


## 1a, 4a, 4b 발견 
data_raw_add_set %>% 
  mutate(stage = gsub("^4[a-z]", "4", stage)) %>% 
  mutate(stage = gsub("^1[a-z]", "1", stage)) %>% 
  
  ## stage 수정 후 stage 별 n개 체크, 수정 완료 
  # group_by(stage) %>% summarise(n = n())
  mutate(stage = gsub("-", "0", stage)) %>% 
  mutate(stage = replace_na(stage, "0")) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  mutate(age = as.numeric(cut_number(.$age, 3)))%>% 
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> data_raw_add_set_ready

data_raw_add_set_ready %>% 
  
  # 쓸모없는 변수 제거 
  select(-c(stage_raw, NO, Name, Group_RN.x,
            NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) %>% 
  
  # formula를 위해 X value names에 공백 제거 
  rename_at(vars(matches(" ")), funs(str_replace(., " ", "_"))) %>% 
  # formula를 위해 X value names에 dash 제거 
  rename_at(vars(matches("-")), funs(str_replace_all(., "-", "_"))) %>% 
  # 숫자가 포함되어있는 metabolites를 HMDB를 참고, 이름 바꿔줌
  rename(beta_Hydroxybutyric_acid = '3_Hydroxybutyric_acid', 
         Methyl_folate = '5_Methyltetrahydrofolic_acid',
         Hydroxy_L_proline = '4_Hydroxyproline') -> raw_info_add_set


# Use logarithm
raw_info_add_set_log <- cbind(raw_info_add_set[, 1:7], log(raw_info_add_set[, 8:88]))
raw_info_add_set_log[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), raw_info_add_set_log[, -(1:7)])

# Use Standardization
raw_info_add_set_st <- cbind(raw_info_add_set[, 1:7], scale((raw_info_add_set[, 8:88]), T, T))
raw_info_add_set_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), raw_info_add_set_st[, -(1:7)])

# Use rescaling [0-1], https://gist.github.com/Nicktz/b06e7afcb52db888a10ee28da3d2f589
raw_info_add_set %>% 
  mutate_each_(funs(rescale), vars = names(.)[-(1:7)]) -> raw_info_add_set_re

# Use log + Standardization
raw_info_add_set_log_st <- cbind(raw_info_add_set[, 1:7], log(raw_info_add_set[, 8:88]))
raw_info_add_set_log_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), raw_info_add_set_log_st[, -(1:7)])
raw_info_add_set_log_st[, -(1:7)] <- scale(raw_info_add_set_log_st[, -(1:7)], T, T)

# 새로 넣은 set을 이용한 CLR 
# simple 
raw_result_add_set <- UsCLR(raw_info_add_set, c(1,2,7))
raw_result_add_set[[1]]

# multiple
summary(clogit(formula = formula_candi, data = raw_info_add_set,
               control = coxph.control(iter.max = 1000)))


raw_info_add_set %>% 
  mutate(set = as.factor(set),
         Group = as.factor(Group),
         sex = as.factor(sex),
         smoking = as.factor(smoking),
         alcohol = as.factor(alcohol),
         age = as.factor(age)) -> raw_info_add_set


clogistic(Group ~ age + smoking + alcohol + beta_Hydroxybutyric_acid + 
            Methyl_folate + Acetoacetic_acid + L_Acetylcarnitine + Acetylcholine + 
            Adenine + Adenosine + Asymmetric_dimethylarginine + L_Alanine + 
            Adenosine_monophosphate + L_Arginine + Ascorbic_acid + L_Asparagine + 
            L_Aspartic_acid + Betaine + Butyrylcarnitine + L_Carnitine + 
            Choline + Citrulline + Creatine + Creatinine + L_Cystathionine + 
            L_Cysteine + Decanoylcarnitine + Dimethylglycine + Fumaric_acid + 
            Gamma_Aminobutyric_acid + L_Glutamic_acid + L_Glutamine + 
            Oxidized_glutathione + Glycine + Glycochenodeoxycholic_acid + 
            Glycocholic_acid + Guanine + Hexanoylcarnitine + Hippuric_acid + 
            L_Histidine + Hypoxanthine + Inosine + Isovalerylcarnitine + 
            L_Isoleucine + L_Kynurenine + Lactate + Dodecanoylcarnitine + 
            L_Leucine + L_Lysine + L_Methionine + N_Acetyl_L_aspartic_acid + 
            NAD + Niacinamide + Nicotinic_acid + Nicotinuric_acid + Norepinephrine + 
            L_Octanoylcarnitine + L_Phenylalanine + Propionylcarnitine + 
            L_Proline + Pyridoxamine + Pyridoxine + Pyroglutamic_acid + 
            Riboflavin + S_Adenosylhomocysteine + S_Adenosylmethionine + 
            L_Serine + Glycerophosphocholine + Succinic_acid + Taurine + 
            L_Threonine + Thymine + Trimethylamine_N_oxide + Hydroxy_L_proline + 
            Trigonelline + L_Tryptophan + L_Tyrosine + Uracil + Urea + 
            Uric_acid + Uridine + L_Valine + Xanthine + Xanthosine, strata = set, 
          raw_info_add_set, iter.max = 5000)

# 큰 의미 없음. 

# boxplot 
ggplot(melt(raw_info_add_set_re[, -c(1:7)]), aes(x = variable, y = value)) + 
  geom_boxplot() + theme_minimal()
#### raw handling ####

#### In pre-processing, fold change 확인하기 ####
# boxplot으로 살펴본 결과 outliner들이 지나치게 많다. 
# mean으로 계산한 fold-change가 의미가 있을까? median으로 다시 해보자. 

# raw 
raw_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(median)) -> fc_median

raw_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(mean)) -> fc_mean

# BN normalization 
BN_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(median)) -> fc_median

BN_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(mean)) -> fc_mean
  
# Median normalization
MN_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(median)) -> fc_median

MN_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(mean)) -> fc_mean


which(t(as.data.frame(fc_median[2, ] / fc_median[1, ])[-1])[, 1] > 1.50 | 
        t(as.data.frame(fc_median[2, ] / fc_median[1, ])[-1])[, 1] < 0.67)

which(t(as.data.frame(fc_mean[2, ] / fc_mean[1, ])[-1])[, 1] > 1.50 | 
        t(as.data.frame(fc_mean[2, ] / fc_mean[1, ])[-1])[, 1] < 0.67)


#### In pre-processing, fold change 확인하기 ####




#### Find and count outliers ####
# https://www.r-bloggers.com/outlier-detection-and-treatment-with-r/

# 1. (25th - IQR*1.5)보다 작거나 (75th + IQR*1.5)보다 큰 값을 outliner라고 정의하자. 
Find_outliers <- function(data) {
  lowerq = quantile(data)[2]
  upperq = quantile(data)[4]
  iqr = upperq - lowerq
    
  result <- which(data < lowerq -(iqr*1.5) | data > upperq + (iqr*1.5))
  length(result)
}

num_outlier <- apply(BN_info_add_set[, -(1:7)], 2, Find_outliers)

cbind(as.data.frame(num_outlier), 
      index = seq(1, nrow(as.data.frame(num_outlier)), 1)) %>% 
  rownames_to_column() %>% 
  as_tibble() -> num_outlier_index


ggplot(num_outlier_index, aes(y=num_outlier, x = index)) + 
  geom_point() + theme_minimal() + 
  geom_hline(yintercept = 26, color = "red") + 
  geom_text(data = dplyr::filter(num_outlier_index, num_outlier > 26), 
            aes(label = rowname), nudge_x = 2, nudge_y = 1, check_overlap = F)


summary(num_outlier_index) # median : 19, mean : 25.8
num_outlier[which(num_outlier > 26)]
nrow(num_outlier_index[which(num_outlier > 26), ])


# 2. (IQR*3)+75th보다 크고 (IQR*3)+25th보다 작은 값을 outliner라고 정의하자.
Find_extreme_outliers <- function(data) {
  lowerq = quantile(data)[2]
  upperq = quantile(data)[4]
  iqr = upperq - lowerq #Or use IQR(data)
  
  # we identify extreme outliers
  extreme.threshold.upper = (iqr * 3) + upperq
  extreme.threshold.lower = lowerq - (iqr * 3)
  result <- which(data > extreme.threshold.upper | data < extreme.threshold.lower)
  length(result)
}

num_exoutlier <- apply(BN_info_add_set[, -(1:7)], 2, Find_extreme_outliers)

cbind(as.data.frame(num_exoutlier), 
      index = seq(1, nrow(as.data.frame(num_exoutlier)), 1)) %>% 
  rownames_to_column() %>% 
  as_tibble() -> num_exoutlier_index
  

ggplot(num_exoutlier_index, aes(x = index, y = num_exoutlier)) + 
  geom_point() + 
  theme_minimal() + 
  geom_hline(yintercept = 10, color = "red") +
  geom_text(data = dplyr::filter(num_exoutlier_index, num_exoutlier > 10), 
            aes(label = rowname), nudge_x = 2, nudge_y = 1, check_overlap = T)


summary(num_exoutlier_index) # median : 4, mean : 9.7
num_exoutlier[which(num_exoutlier > 10)]
nrow(num_exoutlier_index[which(num_exoutlier > 10), ])

# 3. Group별로 분포보기 
## 3.1 densitiy plot 
BN_info_add_set %>% 
  select(Group, beta_Hydroxybutyric_acid) %>% 
  ggplot(., aes(beta_Hydroxybutyric_acid, fill = as.factor(Group), colour = as.factor(Group))) +
  geom_density(alpha = 0.1)

## 3.2 box plot 
BN_info_add_set %>% 
  select(Group, Guanine) %>% 
  ggplot(., aes(y=Guanine, x = as.factor(Group), fill = as.factor(Group), colour = as.factor(Group))) +
  geom_boxplot(alpha = 0.1)

#### Find and count outliers ####




#### outlier가 일정 기준 이상 존재하는 variable을 제외하고 돌려보자. ####
# 1. outlier를 제외한 full model
no_outlier <- names(BN_info_add_set)[-(which(names(BN_info_add_set) %in% num_outlier_index[which(num_outlier_index$num_outlier > 10), ]$rowname))]

candi_no_outlier <- no_outlier[8:length(no_outlier)][which(no_outlier[8:length(no_outlier)] %in% Change_names(candidate_metabo))]

summary(clogit(formula = as.formula(paste("Group ~", paste(candi_no_outlier, collapse = " + "), "+ strata(set)")),
               data = BN_info_add_set[, c("Group", "set", candi_no_exoutlier)],
               control = coxph.control(iter.max = 100)))

summary(clogit(formula = Group ~ factor(smoking) + factor(alcohol) + 
                 L_Acetylcarnitine + Acetylcholine + L_Alanine + Betaine + L_Carnitine + Creatine + 
                 Creatinine + L_Kynurenine + L_Leucine + L_Methionine + L_Phenylalanine + 
                 S_Adenosylhomocysteine + Urea + L_Valine + strata(set),
               data = BN_info_add_set_st[, no_outlier],
               control = coxph.control(iter.max = 100)))


# 2. extreme outlier를 제외한 full model
no_exoutlier <- names(BN_info_add_set)[-(which(names(BN_info_add_set) %in% 
                                                 num_exoutlier_index[which(num_exoutlier_index$num_exoutlier > 10), ]$rowname))]

candi_no_exoutlier <- no_exoutlier[8:length(no_exoutlier)][which(no_exoutlier[8:length(no_exoutlier)] %in% Change_names(candidate_metabo))]

summary(clogit(formula = as.formula(paste("Group ~", paste(candi_no_exoutlier, collapse = " + "), "+ strata(set)")),
               data = BN_info_add_set[, c("Group", "set", candi_no_exoutlier)],
               control = coxph.control(iter.max = 1000), method='breslow'))

summary(clogit(formula = Group ~ sex + age + smoking + alcohol + Acetoacetic_acid + L_Acetylcarnitine + 
                 Acetylcholine + L_Alanine + L_Arginine + L_Asparagine + L_Aspartic_acid + 
                 Betaine + L_Carnitine + Choline + Citrulline + Creatine + 
                 Creatinine + L_Cysteine + Decanoylcarnitine + Dimethylglycine + 
                 Gamma_Aminobutyric_acid + L_Glutamine + Glycine + Hexanoylcarnitine + 
                 L_Histidine + Isovalerylcarnitine + L_Isoleucine + L_Kynurenine + 
                 Lactate + Dodecanoylcarnitine + L_Leucine + L_Lysine + L_Methionine + 
                 NAD + Niacinamide + Nicotinic_acid + Norepinephrine + L_Octanoylcarnitine + 
                 L_Phenylalanine + Propionylcarnitine + L_Proline + Pyridoxamine + 
                 Pyridoxine + Pyroglutamic_acid + S_Adenosylhomocysteine + 
                 S_Adenosylmethionine + L_Serine + Succinic_acid + L_Threonine + 
                 Thymine + L_Tryptophan + L_Tyrosine + Uracil + Urea + Uric_acid + 
                 Uridine + L_Valine + strata(set),
               data = BN_info_add_set_[, no_exoutlier],
               control = coxph.control(iter.max = 3000), method='breslow'))

candi_no_exoutlier[23]

# error "Loglik converged before variables ; coefficient may be infinite. 
# Q. finite인 var은 뭘까? finite인 var은 계속 유효할까?
# coef_inf의심 variables 
coef_inf <- names(BN_info_add_set[, no_exoutlier][, -c(1,2,7)])[c(2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,40,41,43,47,57)]


no_outlier %in% coef_inf
no_outlier %in% names(BN_info_add_set[, no_exoutlier][, -c(1,2,7)])[-which(names(BN_info_add_set[, no_exoutlier][, -c(1,2,7)]) %in% coef_inf)]
names(BN_info_add_set[, no_exoutlier][, -c(1,2,7)])[-which(names(BN_info_add_set[, no_exoutlier][, -c(1,2,7)]) %in% coef_inf)]

summary(clogit(formula = Group ~ sex + L_Octanoylcarnitine + L_Phenylalanine +
                 Pyridoxamine + Pyroglutamic_acid + S_Adenosylhomocysteine + 
                 S_Adenosylmethionine + Succinic_acid + L_Threonine + 
                 Thymine + L_Tryptophan + L_Tyrosine + Uracil + Urea + 
                 Uric_acid + Uridine + strata(set),
               data = BN_info_add_set[, no_exoutlier],
               control = coxph.control(iter.max = 3000), method='exact'))


#### outlier가 일정 기준 이상 존재하는 variable을 제외하고 돌려보자. ####

#### test 1 : extreme outlier들을 95th, 5th으로 바꾸면? ####
Replace_extreme_outliers <- function(data) {
  lowerq = quantile(data)[2]
  upperq = quantile(data)[4]
  iqr = upperq - lowerq #Or use IQR(data)
  
  # we identify extreme outliers
  extreme.threshold.upper = (iqr * 3) + upperq
  extreme.threshold.lower = lowerq - (iqr * 3)
  
  result1 <- which(data > extreme.threshold.upper)
  data <- replace(data, result1, values=quantile(data, 0.95))
  result2 <- which(data < extreme.threshold.lower)
  data <- replace(data, result1, values=quantile(data, 0.05))
}

test_replace_ex <- apply(apply(BN_info_add_set[, -(1:7)], 2, Replace_extreme_outliers), 2, Find_extreme_outliers)
  

a <- apply(apply(BN_info_add_set[, -(1:7)], 2, Replace_extreme_outliers), 2, Find_extreme_outliers)
b <- apply(BN_info_add_set[, -(1:7)], 2, Find_extreme_outliers)


summary(a) # median : 0, mean : 2.7
summary(b) # median : 4, mean : 9.7

a[which(a > 3)]
b[which(b > 10)]

length(a[which(a > 3)]) # 4
length(b[which(b > 10)]) # 28

cbind(as.data.frame(a), 
      index = seq(1, nrow(as.data.frame(a)), 1)) %>% 
  rownames_to_column() %>% 
  rename(num_exoutlier = a) %>% 
  as_tibble() -> num_exoutlier_index_replace


BN_info_add_set_replace_ex <- cbind(BN_info_add_set[, (1:7)], 
                                    apply(BN_info_add_set[, -(1:7)], 2, Replace_extreme_outliers))


no_exoutlier_replace_ex <- names(BN_info_add_set_replace_ex)[-(which(names(BN_info_add_set_replace_ex) %in% 
                                                                       num_exoutlier_index_replace[which(num_exoutlier_index_replace$num_exoutlier > 3), ]$rowname))]
# no_exoutlier와 개수 확인 완료 71 == 71
length(names(BN_info_add_set_replace_ex)) - length(a[which(a > 3)])

summary(clogit(formula = as.formula(paste("Group ~", 
                                          paste(names(BN_info_add_set_replace_ex[, no_exoutlier_replace_ex][, -c(1,2,7)]), 
                                                collapse = " + "), "+ strata(set)")),
               data = BN_info_add_set_replace_ex[, no_exoutlier_replace_ex],
               control = coxph.control(iter.max = 1000), method='approximate'))


library(survminer)
ggsurvplot(survfit(Surv(rep(1, 546L), Group) ~ 
                     (beta_Hydroxybutyric_acid  > median(beta_Hydroxybutyric_acid , na.rm = T)), 
                   data = BN_info_add_set_replace_ex), data = BN_info_add_set_replace_ex)

#### test 1 : extreme outlier들을 95th, 5th으로 바꾸면? ####


### NEW ####

#### ####


#### <To DO> merge & some handling ####

# Using batch normalization 
data_BN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  mutate(set_pre = matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 1]) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  select(set_pre, Group, everything()) %>% 
  arrange(set_pre) %>% 
  mutate(set = matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 2]) %>% # mutate 'set' part
  select(set, everything()) %>% 
  arrange(set) %>% 
  select(set, Group, NO, sex, age, smoking, alcohol, stage_raw, stage, everything()) -> data_BN

# change row name & delete dummy metabolites
names(data_BN) <- c("set", "Group", "NO", "sex", "age", "smoking", "alcohol",
                    "stage_raw", "stage", "set_pre", "Name", "Group_RN.x",
                    "Batch", "order", metabolites_name, 
                    "NCC_num", "Group_RN.y", "TB_num", "주장기", "box", "위치")

#### <TO DO> rename_all을 이용한 이름 바꾸기 ####
  # rename_all(funs(gsub("[[:alpha:]]", "", make.names("set", "Group", "NO", "sex", "age", "smoking", "alcohol", 
  #                                                    "stage_raw", "stage", "set_pre", "Name", "Group_RN.x",
  #                                                    "Batch", "order", metabolites_name))))
#### ####
  
  ## stage 수정 전 stage 별 n개 체크
  # group_by(stage) %>% summarise(n = n())
  
## metabolites name matching 이후 사용할 수 없는 metabolites의 이름이 NA로 바뀜 
## NA의 이름을 가진 metabolites 제거 
data_BN <- data_BN[, -which(names(data_BN) == 'NA')]


## 1a, 4a, 4b 발견
## 4a, 4b는 4로 1a는 1로 수정
data_BN %>% 
  mutate(stage = gsub("^4[a-z]", "4", stage)) %>% 
  mutate(stage = gsub("^1[a-z]", "1", stage)) %>% 
  
  ## stage 수정 후 stage 별 n개 체크, 수정 완료 
  # group_by(stage) %>% summarise(n = n())
  mutate(stage = gsub("-", "0", stage)) %>% 
  mutate(stage = replace_na(stage, "0")) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  mutate(age = as.numeric(cut_number(.$age, 3)))%>% 
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> data_BN_ready
  
  # metabolites 이름 및 개수 체크  
  metabolites_name[-which(metabolites_name == "NA")] == colnames(data_BN_ready)[15:95]
  org_metabolites_nanme <- metabolites_name[-which(metabolites_name == "NA")] 
  
  
  
  ## change type of some variables to FACTOR ##
  mutate(Group = as.factor(.$Group)) %>% 
  mutate(sex = as.factor(ifelse(sex == 1, "male", "female"))) %>% 
  mutate(smoking = as.factor(ifelse(smoking == 1, "Y",
                                    ifelse(smoking == 2, "N", "null")))) %>% 
  mutate(alcohol = as.factor(ifelse(alcohol == 1, "Y",
                                    ifelse(smoking == 2, "N", "null")))) %>%
  mutate(stage = as.factor(stage)) %>% 
  mutate(age = as.factor(cut_number(.$age, 3))) -> BN_info
  ## change type of some variables to FACTOR ##

# Using median Normalization 
data_MN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  mutate(set_pre = matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 1]) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  select(set_pre, Group, everything()) %>% 
  arrange(set_pre) %>% 
  mutate(set = matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 2]) %>% # mutate 'set' part
  select(set, everything()) %>% 
  arrange(set) 

#### ####



#### ROC CURVE 1 vs 1 이므로 Comparison pair에 대한 반복 없음 ####
result = combn(group_value, 1)

# all metabolites 
cm <- colnames(data_BN)[-(1:6)]

# KBSI suggested metabolites
cm <- c("Acetylcarnitine", "Deca.carnitine", "Hex.carnitine", "Iso.carnitine", "Oct.carnitine", "Glutamate", "sn.glycerol.3.phosphocholine", "TMAO")
a <- ".Results"
cm <- paste0(cm, a)

# set names for saving plots 
folder_name <- "...graph_output/"
file_name <- "testplot"

data_BN %>% 
  as_tibble() %>% 
  dplyr::filter(Group %in% result) %>% 
  mutate(group1 = ifelse(Group %in% result[1, 1], 0, 1)) %>% 
  select(Group, group1, everything()) %>% 
  select(group1, cm) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) -> data_1 

for( i in 1:length(cm) ) {
  numbering <- i
  png_name <- paste0(folder_name, file_name, "_" , paste(result[1, 1]),
                     "_VS_", paste(result[1, 2]), "_", paste(cm[i]), ".png")
  
  png(png_name, width = 750, height = 750, pointsize = 20)
  
  ROC(form = as.formula(paste(colnames(data_1)[1], "~", cm[i])), data = data_1, plot="ROC")
  
  dev.off()
}

#### ####

#### CLR ####
data_BN_ready %>% 
  select(-c(stage_raw, NO, Name, set_pre, Group_RN.x,
            Batch, order, NCC_num, Group_RN.y, TB_num, 주장기, box, 위치))
            
            
  # formula를 위해 X value names에 공백 제거 
  rename_at(vars(matches(" ")), funs(str_replace(., " ", "_"))) %>% 
  # formula를 위해 X value names에 dash 제거 
  rename_at(vars(matches("-")), funs(str_replace_all(., "-", "_"))) %>% 
  # 숫자가 포함되어있는 metabolites를 HMDB를 참고, 이름 바꿔줌
  rename(beta_Hydroxybutyric_acid = '3_Hydroxybutyric_acid', 
         Methyl_folate = '5_Methyltetrahydrofolic_acid',
         Hydroxy_L_proline = '4_Hydroxyproline') -> BN_info



# metabolites들의 scale이 너무 큼. log scale로 바꿔보자. 
log_BN_info <- BN_info[, 8:98]
which(log_BN_info < 0) # 0보다 작은 값이 있는가? 없음
length(which(log_BN_info < 1)) # 944
length(which(log_BN_info == 0)) # 675
length(which(log_BN_info > 0 & log_BN_info < 1)) # 269 

# Use logarithm
BN_info_log <- cbind(BN_info[, 1:7], log2(BN_info[, 8:88]))
BN_info_log[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_log[, -(1:7)])
BN_info_log %>% as_tibble()

# Use Standardization
BN_info_st <- cbind(BN_info[, 1:7], scale((BN_info[, 8:88])))
BN_info_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_st[, -(1:7)])
BN_info_st %>% as_tibble()

# Use rescaling [0-1], https://gist.github.com/Nicktz/b06e7afcb52db888a10ee28da3d2f589
BN_info %>% 
  mutate_each_(funs(rescale), vars = names(.)[-(1:7)]) -> BN_info_re
  
# Use log + Standardization
BN_info_log_st <- cbind(BN_info[, 1:7], log(BN_info[, 8:88]))
BN_info_log_st[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info_log_st[, -(1:7)])
BN_info_log_st[, -(1:7)] <- scale(BN_info_log_st[, -(1:7)], T, T)

BN_info_log_st %>% as_tibble()


#### <TO DO> clogit 사용해보기 ####
library(survival)
library(lme4)
library(metafor)


#### SOME test ####
n <- 100
ai <- c(rep(0,n/2), rep(1,n/2))
bi <- 1-ai
ci <- c(rep(0,42), rep(1,8), rep(0,18), rep(1,32))
di <- 1-ci

### change data to long format 
event <- c(rbind(ai,ci))
group <- rep(c(1,0), times=n)
id    <- rep(1:n, each=2)


summary(clogit(event ~ group + strata(id)))

library(Epi)
data(bdendo)
data(bdendo11)

bdendo %>% as_tibble() # 1:4 매칭, case 1, control 2 
bdendo11 # 1:1 매칭, case 1, control 2 
help(bdendo)

summary(clogit(d ~ cest + dur + strata(set), bdendo)) # clogit == clogistic 
clogistic(d ~ cest + dur, strata = set, data = bdendo) ## clogit == clogistic
summary(glmer(d ~ cest + dur + (1|set), family = binomial(link = probit), bdendo))
summary(glmer(d ~ cest + dur + (1|set), family = binomial(link = logit), bdendo))




resp <- levels(logan$occupation)
n <- nrow(logan)
indx <- rep(1:n, length(resp))
logan2 <- data.frame(logan[indx,],
                     id = indx,
                     tocc = factor(rep(resp, each=n)))
logan2$case <- (logan2$occupation == logan2$tocc)
clogit(case ~ tocc + tocc:education + strata(id), logan2)

#### ####

base_var = colnames(BN_info_log)[3:6]
all_metabolites = colnames(BN_info_log)[8:88]

formula_special = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(Change_names(special_metabo), collapse = " + "), "+ strata(set)"))

formula_all = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(all_metabolites, collapse = " + "), "+ strata(set)"))

formula_candi = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(Change_names(candidate_metabo), collapse = " + "), "+ strata(set)"))



# Activate but not convergence 
summary(clogit(formula, data = BN_info_log))

# control arg를 이용해 iteration 횟수 증가시킴
# + coxph와 clogit의 동일성 파악
coxph(formula = Surv(rep(1, 546L), Group) ~ sex + age + smoking + 
        alcohol + beta_Hydroxybutyric_acid + Methyl_folate + Acetoacetic_acid + 
        L_Acetylcarnitine + Acetylcholine + Adenine + Adenosine + 
        Asymmetric_dimethylarginine + L_Alanine + Adenosine_monophosphate + 
        Hydroxy_L_proline + Trigonelline + L_Tryptophan + L_Tyrosine + 
        Uracil + Urea + Uric_acid + Uridine + L_Valine + Xanthine + 
        Xanthosine + strata(set), data = BN_info_log, method = "exact", control = coxph.control(iter.max = 20000))

# coxph == clogit 
summary(clogit(formula = Group ~ sex + age + smoking + 
                 alcohol + beta_Hydroxybutyric_acid + Methyl_folate + Acetoacetic_acid + 
                 L_Acetylcarnitine + Acetylcholine + Adenine + Adenosine + 
                 Asymmetric_dimethylarginine + L_Alanine + Adenosine_monophosphate + 
                 Hydroxy_L_proline + Trigonelline + L_Tryptophan + L_Tyrosine + 
                 Uracil + Urea + Uric_acid + Uridine + L_Valine + Xanthine + 
                 Xanthosine + strata(set), data = BN_info_log, control = coxph.control(iter.max = 20000)))

# iteration을 2만 번까지 늘려도 convergence가 안됨. 

summary(clogit(formula = formula_special, data = BN_info_log))
summary(clogit(formula = formula_candi, data = BN_info_log, control = coxph.control(iter.max = 20000, T)))
summary(clogit(formula = formula_all, data = BN_info_log, control = coxph.control(iter.max = 20000, T)))


#### Univariate conditional logistic regression ####

UsCLR <- function(data, target_position) {
  
  result <- list(NULL, NULL)
  summary_UsCLR <- c()
  
  
  list <- names(data[-target_position])
  
  for (i in 1 : length(list)){
    formula <- as.formula(paste("Group ~", list[i], "+ strata(set)"))
    result_ith_UsCLR <- round(summary(clogit(formula = formula, data = data, method = "efron"))$coefficients, 4)
    summary_UsCLR <- rbind(summary_UsCLR, result_ith_UCLR)
  }
  
  summary_UsCLR <- as.data.frame(summary_UsCLR)
  
  #### <TO DO> rename으로바꿔보기 ####
  colnames(summary_UsCLR)[5] <- "p_value"
  
  summary_UsCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) %>% 
    dplyr::filter(p_value <= 0.05) -> result[[1]]
  
  
  summary_UsCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) -> result[[2]]
  
  return(result)
}

#### ####


raw_result_unscale <- UsCLR(BN_info, c(1,2,7))
raw_result_log <- UsCLR(BN_info_log, c(1,2,7))
raw_result_st <- UsCLR(BN_info_st, c(1,2,7))

raw_result_st[[1]]
raw_result_log[[1]]
raw_result_unscale[[1]]


#### <TO DO> 설명할 수 있는 이유 찾기 ####
# scaling을 하지 않고 raw data로 univariate conditional logistic을 시행하면 차이 없음으로 나옴.
# 어떤 scaling이라도 하기만 하면 엄청 큰 차이가 있다고 나옴.
# 왜? scaline으로 결과가 바뀔 수 있는 건 알고 있지만 이렇게까지 바뀔 수 있나? 

clogit(Group ~ L_Glutamine + strata(set), data = BN_info) # 차이없음 
clogit(Group ~ L_Glutamine + strata(set), data = BN_info_log) # 차이 큼 
clogit(Group ~ L_Glutamine + strata(set), data = BN_info_st) # 차이 큼 
clogit(Group ~ L_Glutamine + strata(set), data = BN_info_re) # 차이 큼 
clogit(Group ~ L_Glutamine + strata(set), data = BN_info_log_st) # 차이 큼 

summary(BN_info$L_Glutamine)

boxplot(BN_info$L_Glutamine)
boxplot(BN_info_re$L_Glutamine)

#### <TO DO> 설명할 수 있는 이유 찾기 ####


#### Write xlsx ####
raw_result_unscale[[1]] %>% 
  write.xlsx("UCLR_sig_unscale.xlsx")

raw_result_unscale[[2]] %>% 
  write.xlsx("UCLR_all_unscale.xlsx")

raw_result_unscale[[2]][filtering, ] %>% 
  write.xlsx("UCLR_filtering_unscale.xlsx")

# 이렇게 여러 번 할 게 아니라 각각 index를 만들어서 excel로 편하게 볼 수 있게 하는 게 좋겠는데 

#### write xlsx ####

raw_result_unscale[[2]][filtering, ]

BN_info$L_Acetylcarnitine




filtering = c()

for(i in 1:length(raw_result_unscale[[2]][1][, 1])){
  for(j in 1:length(Change_names(candidate_metabo))){
    if (Change_names(candidate_metabo)[j] == raw_result_unscale[[2]][1][, 1][i]) {
      filtering <- c(filtering, i)
      
    }
  }
  
}

raw_result[[2]][filtering, ]
#### #####

#### (Be in Use) <PROBLEM< scailing을 해야하나? 해야하면 어떤 scailing을 해야 하나? ####
library(reshape2)
library(ggplot2)

sub_data <- melt(BN_info[, -c(1:7)])

cut_point_col <- round(length(unique(sub_data$variable)) / 2)

cut_point <- (cut_point_col * nrow(BN_info[, -c(1:7)]))
sub_data[cut_point+1, ]




ggplot(sub_data[1:cut_point, ], aes(x = value)) + 
  facet_wrap( ~ variable, scales = "free_x") + 
  geom_histogram()

ggplot(sub_data[cut_point+1 : nrow(sub_data), ], aes(x = value)) + 
  facet_wrap( ~ variable, scales = "free_x") + 
  geom_histogram()



explore_hist <- function(data, divived_num, folder_name, file_name, width, height){
  
  sub_data <- melt(data)
  cut_point_col <- round(length(unique(sub_data$variable)) / divived_num)  
  cut_point <- (cut_point_col * nrow(data))
  
  for(i in 1:divived_num){
    if(i == 1){
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      print(ggplot(sub_data[1:cut_point, ], aes(x = value)) + 
        facet_wrap( ~ variable, scales = "free_x") + 
        geom_histogram())
      
      dev.off()    
      
      
    } else if(i != 1 | i != divived_num) {
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      print(ggplot(sub_data[((cut_point*(divived_num-1))+1) : (cut_point*(divived_num+1)), ], aes(x = value)) + 
        facet_wrap( ~ variable, scales = "free_x") + 
        geom_histogram())
      
      dev.off()    
      
    } else {
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      
      print(ggplot(sub_data[((cut_point*(divived_num-1))+1) : nrow(sub_data), ], aes(x = value)) + 
        facet_wrap( ~ variable, scales = "free_x") + 
        geom_histogram())
      
      dev.off()    
    }
      
  }
}

explore_hist(BN_info[, -c(1:7)], 2, "...", "histogram")
explore_hist(BN_info_log[, -c(1:7)], 2, "...", "histogram_log")
explore_hist(BN_info_st[, -c(1:7)], 2, "...", "histogram_st")
explore_hist(BN_info_re[, -c(1:7)], 2, "...hist/", "histogram_re")
explore_hist(BN_info_log_st[, -c(1:7)], 2, "...hist/", "histogram_log_st")

#### PROBLEM scailing을 해야하나? 해야하면 어떤 scailing을 해야 하나? ####







#### <PROBLEM> an id statement is required for multi-state models ####
pro1_1 <- set[19:21] # 7번째 match
pro1_2 <- BN_info$Group[19:21] # OC가 없다. 

# matching_set_num가 틀렸거나 merge나 pre-processing 단계에서 pairing을 해줘야할 것 같다. 
# Fail 

#### <PROBLEM> an id statement is required for multi-state models ####  

BN_info$set[19:21]
BN_info$Group[19:21]
BN_info %>% as_tibble()


#### ####

#### Path way analysis ####

# list of metabolites
cat(gsub(".Results$", "", names(data_BN[, 7:97])), fill=1)
# a lots of undefined metabolites 

# after modification
metabolites_list <- read.xlsx(paste(dir, "name_map.xlsx", sep = "/"), stringsAsFactor = FALSE, sheetIndex = 1,)

# HMDB ID 기준 추출 
metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]
length(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]) # 80개 

# Compound name 기준 추출
metabolites_list$Match[which(metabolites_list$Match != "NA")]
length(metabolites_list$Match[which(metabolites_list$Match != "NA")]) # 81개 


# 중복 검사 
length(unique(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]))
sum(duplicated(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]))  

# copy & paste를 위한 cat
cat(as.character(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]), fill = 1)
cat(as.character(metabolites_list$Match[which(metabolites_list$Match != "NA")]), fill = 1)


# list of metabolites
cat(gsub(".Results$", "", names(data_BN[, 7:97])), fill=1)

#### ####

#### Comparison with C and OC group ####

data_BN_ready %>%
  as_tibble() %>% 
  select(Group, org_metabolites_nanme) %>% 
  group_by(Group) %>% 
  summarise_all(funs(mean, median, sd)) -> test


test_t <- as_tibble(cbind(nms = names(test), t(test)))
test_t <- test_t[-1, ]
names(test_t) <- c("Names", "C", "OC")

test_t$Names[1:81]
length(test_t$Names)
index <- c(rep("Mean", 81), rep("Median", 81), rep("sd", 81))

test_t <- cbind(test_t, index)
test_t$Names <- gsub("_mean$", "", test_t$Names)
test_t$Names <- gsub("_median$", "", test_t$Names)
test_t$Names <- gsub("_sd$", "", test_t$Names)

test_t %>% 
  write.xlsx("table.xlsx")


candidate_metabo <- c("beta-Hydroxybutyric acid ", "Acetylcholine", "L-Alanine", "L-Arginine", "L-Aspartic acid","L-Asparagine",
                      "L-Carnitine", "Choline" ,"Creatinine", "Dimethylglycine", "Gamma-Aminobutyric acid","Betaine",
                      "L-Glutamine", "Glycine", "L-Isoleucine", "L-Kynurenine", "L-Leucine", "L-Lysine", "L-Methionine", 
                      "Nicotinic acid", "L-Phenylalanine", "L-Proline", "Pyridoxamine", "Pyridoxine", "L-Serine", 
                      "Taurine", "L-Threonine", "Hydroxy_L_proline " , "Urea", "L-Valine",
                      "L-Acetylcarnitine", "Decanoylcarnitine", "L-Glutamic acid", "Hexanoylcarnitine", 
                       "Isovalerylcarnitine ", "L-Octanoylcarnitine", "Glycerophosphocholine", "Trimethylamine N-oxide")




special_metabo <- c("L-Acetylcarnitine", "Decanoylcarnitine", "L-Glutamic acid", "Hexanoylcarnitine", 
                    "Isovalerylcarnitine ", "L-Octanoylcarnitine", "Glycerophosphocholine", "Trimethylamine N-oxide")

length(candidate_metabo)
length(special_metabo)


data_BN_ready[, which(names(data_BN_ready) == candidate_metabo)]

position_cm <- c()
for(i in 1:data_BN_ready(BN_info[, -c(1,3:7)])) {
  for( j in 1:length(candidate_metabo)) {
    if(names(data_BN_ready[, -c(1,3:7)])[i] == candidate_metabo[j]) {
      position_cm <- c(position_cm, i)
    }
  }
}

position_sm <- c()
for(i in 1:ncol(data_BN_ready[, -c(1,3:7)])) {
  for( j in 1:length(special_metabo)) {
    if(names(data_BN_ready[, -c(1,3:7)])[i] == special_metabo[j]) {
      position_sm <- c(position_sm, i)
    }
  }
}

colnames(data_BN_ready[, -c(1,3:7)][, position_cm])
colnames(data_BN_ready[, -c(1,3:7)][, position_sm])

data_BN_ready[, -c(1,3:7)][, c(1, position_sm)] %>%
  as_tibble() %>% 
  group_by(Group) %>% 
  summarise_all(funs(mean, median, sd)) -> test


test_t <- as_tibble(cbind(nms = names(test), t(test)))
test_t <- test_t[-1, ]
names(test_t) <- c("Names", "C", "OC")

test_t$Names[1:length(position_sm)]
length(test_t$Names)
index <- c(rep("Mean", length(position_sm)), rep("Median", length(position_sm)), rep("sd", length(position_sm)))

test_t <- cbind(test_t, index)
test_t$Names <- gsub("_mean$", "", test_t$Names)
test_t$Names <- gsub("_median$", "", test_t$Names)
test_t$Names <- gsub("_sd$", "", test_t$Names)

test_t %>% 
  write.xlsx("table_sm.xlsx")


#### <TO DO> Function 만들기 ####
compare_summary_stat <- function(data, cadidated_name_lists, grouping_value_name){

  grouping_value_name <- enquo(grouping_value_name)
  
  data %>% 
    select(c(!!grouping_value_name, cadidated_name_lists)) -> function_data
  
  position <- c()
  for(i in 1 : ncol(function_data)) {
    for( j in 1 : length(cadidated_name_lists)) {
      if(names(function_data)[i] == cadidated_name_lists[j]) {
        position <- c(position, i)
      }
    }
  }
  
  function_data %>% 
    group_by(!!grouping_value_name) %>% 
    summarise_all(funs(mean, median, sd)) -> test
  
  test_t <- as_tibble(cbind(nms = names(test), t(test)))
  test_t <- test_t[-1, ]
  
  names(test_t) <- c("Names", "C", "OC")
  
  index <- c(rep("Mean", length(position)), rep("Median", length(position)), rep("sd", length(position)))
  
  test_t <- cbind(test_t, index)
  test_t$Names <- gsub("_mean$", "", test_t$Names)
  test_t$Names <- gsub("_median$", "", test_t$Names)
  test_t$Names <- gsub("_sd$", "", test_t$Names)
  
  return(test_t)
}

compare_summary_stat(data_BN_ready, org_metabolites_nanme, Group)


test_t %>% 
  write.xlsx("table_sm.xlsx")

#### ####

#### <TO DO> Function 만들기 ####
compare_summary_stat <- function(data, cadidated_name_lists, grouping_value_name){

  grouping_value_name <- enquo(grouping_value_name)
  
  data %>% 
    select(c(!!grouping_value_name, cadidated_name_lists)) -> function_data
  
  position <- c()
  for(i in 1 : ncol(function_data)) {
    for( j in 1 : length(cadidated_name_lists)) {
      if(names(function_data)[i] == cadidated_name_lists[j]) {
        position <- c(position, i)
      }
    }
  }
  
  function_data %>% 
    group_by(!!grouping_value_name) %>% 
    summarise_all(funs(mean, median, sd)) -> test
  
  test_t <- as_tibble(cbind(nms = names(test), t(test)))
  test_t <- test_t[-1, ]
  
  names(test_t) <- c("Names", "C", "OC")
  
  index <- c(rep("Mean", length(position)), rep("Median", length(position)), rep("sd", length(position)))
  
  test_t <- cbind(test_t, index)
  test_t$Names <- gsub("_mean$", "", test_t$Names)
  test_t$Names <- gsub("_median$", "", test_t$Names)
  test_t$Names <- gsub("_sd$", "", test_t$Names)
  
  return(test_t)
}

compare_summary_stat(data_BN_ready, org_metabolites_nanme, Group)


test_t %>% 
  write.xlsx("table_sm.xlsx")

#### ####

length(candidate_metabo)
length(special_metabo)

#### ####



#### <TO DO> Function 만들기 ####
matching_set_num <- function(data, Group_var_position, case_interval, control_interval) {
  set_case = seq(1, nrow(data), case_interval)
  set_control = seq(1, nrow(data), control_interval)[-set_case]
  set_pre = c()  
  n <- 1
  m <- 1
  
  for (i in 1:nrow(data)) {
    j <- 1
    if (data[[Group_var_position]][i] == "OC"){
      set_pre[i] <- set_case[n]
      n = n+1
    } else {
      set_pre[i] <- set_control[m]
      m = m+1
    }
  }
  # set_pre <- sort(set_pre) 
  # 이 단계에서 sorting을 하면 set이 이상하게 붙어버린다. 
  # set_pre를 붙이고 arrange(set_pre) 후 set을 붙여야 한다. 
  
  set = c()
  for (i in 1:(nrow(data)/case_interval)) {
    a = rep(i, case_interval)
    set = c(set, a)
  }
  
  result = matrix(c(set_pre, set), nrow(data), 2)
  return(result)
  
}
#### <TO DO> Fuctnion 만들기 끝 #### 
matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 1]
matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 2]

#### <TO DO> metabolites 이름 바꿔주는 function 만들기 ####
Change_names <- function(list){
  list <- gsub("^ | $", "", list)
  list <- gsub(" ", "_", list)
  list <- gsub("-", "_", list)
  
  return(list)
}

Change_names(special_metabo)

#### <DONE, TO DO> metabolites 이름 바꿔주는 function 만들기 ####

#### 결과보고를 위한 작성 ####

# functionazation 
report_result <- function(data, metabolites_name) {
  
  mean_t_test <- lapply(metabolites_name, function(v) {
    t.test(as.data.frame(data)[, v] ~ as.data.frame(data)[, 'Group'])
  })
  
  l <- list()
  j <- 1
  a <- c()
  for( i in 1:length(mean_t_test) ) {
    mean_t_test[[i]]$data.name <- paste(metabolites_name[i], "by Group" )
    if ( mean_t_test[[i]]$p.value < 0.05 ) {
      l[[j]] <- mean_t_test[[i]]
      j <- j+1
      a <- c(a, metabolites_name[i])
    }
  }
}


raw_info_add_set %>%
  group_by(Group) %>%
  summarise(n = n())

raw_info_add_set %>%
  group_by(Group) %>%
  select(8:88) %>% 
  summarise_all(funs(mean(., na.rm = T), median(., na.rm = T)))


# 1. Paired t-test 
mean_t_test <- lapply(all_metabolites, function(v) {
  t.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])
})



l <- list()
j <- 1
a <- c()
for( i in 1:length(mean_t_test) ) {
  mean_t_test[[i]]$data.name <- paste(all_metabolites[i], "by Group" )
  if ( mean_t_test[[i]]$p.value < 0.05 ) {
    l[[j]] <- mean_t_test[[i]]
    j <- j+1
    a <- c(a, all_metabolites[i])
  }
}

l # 총 55개의 metabolites들이 Group간 평균차이가 존재함. 
a # 55개의 metabolites들의 이름 

# candidate된 모든 metabolites들에서 Group간 평균차이가 존재함. 
candidate_metabo[which(Change_names(candidate_metabo) %in% a)]


# 2. 기본 변수 분포 보여주기 

raw_info_add_set %>% 
  group_by(Group, sex) %>% 
  summarise(n = n()) %>% 
  ggplot(., aes(x = factor(sex), y = n, fill = factor(Group))) + 
  geom_bar(stat = "identity", position = "dodge") + 
  scale_x_discrete(labels=c("Male", "Female")) +
  xlab("Gender") + ylab("Count") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)

raw_info_add_set %>% 
  group_by(Group, smoking) %>% 
  summarise(n = n()) %>% 
  ggplot(., aes(x = factor(smoking), y = n, fill = factor(Group))) + 
  geom_bar(stat = "identity", position = "dodge") + 
  scale_x_discrete(labels=c("Null", "Yes", "No")) +
  xlab("Smoking") + ylab("Count") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)

raw_info_add_set %>% 
  group_by(Group, alcohol) %>% 
  summarise(n = n()) %>% 
  ggplot(., aes(x = factor(alcohol), y = n, fill = factor(Group))) + 
  geom_bar(stat = "identity", position = "dodge") + 
  scale_x_discrete(labels=c("Null", "Yes", "No")) +
  xlab("Alcohol") + ylab("Count") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)

ggplot(melt(data_BN[, c("Group", "age")], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) +
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) + 
  xlab("Age")


# 3. histogram으로 분포보여주기
dir <- "..."
explore_hist <- function(data, divived_num, folder_name, file_name, width, height){
  
  sub_data <- melt(data)
  cut_point_col <- round(length(unique(sub_data$variable)) / divived_num)  
  cut_point <- (cut_point_col * nrow(data))
  
  for(i in 1:divived_num){
    if(i == 1){
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      print(ggplot(sub_data[1:cut_point, ], aes(x = value)) + 
              facet_wrap( ~ variable, scales = "free_x") + 
              geom_histogram()) + theme_minimal()
      
      dev.off()    
      
      
    } else if(i != 1 | i != divived_num) {
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      print(ggplot(sub_data[((cut_point*(divived_num-1))+1) : (cut_point*(divived_num+1)), ], aes(x = value)) + 
              facet_wrap( ~ variable, scales = "free_x") + 
              geom_histogram()) + theme_minimal()
      
      dev.off()    
      
    } else {
      
      png_name <- paste0(folder_name, file_name, "_", paste(i), ".png")
      png(png_name, width = width, height = height, pointsize = 20)
      
      
      print(ggplot(sub_data[((cut_point*(divived_num-1))+1) : nrow(sub_data), ], aes(x = value)) + 
              facet_wrap( ~ variable, scales = "free_x") + 
              geom_histogram()) + theme_minimal()
      
      dev.off()    
    }
    
  }
}


explore_hist(raw_info_add_set[, -c(1:7)], 2, dir, "histogram", 1500, 1000)
explore_hist(raw_info_add_set[, Change_names(candidate_metabo)], 2, dir, "candi_histogram", 1500, 1000)

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(candidate_metabo)[1:19])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(candidate_metabo)[20:38])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)


# 4. box plot으로 분포 보여주기
ggplot(melt(raw_info_add_set[,  c("Group", Change_names(candidate_metabo)[1:19])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)


ggplot(melt(raw_info_add_set[,  c("Group", Change_names(candidate_metabo)[20:38])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)



ggplot(melt(raw_info_add_set[,  c("Group", "sex", "age", "smoking", "alcohol")], id.var = "Group"), 
       aes(x=variable, y = value, fill = factor(Group))) + 
  geom_bar(stat = "identity", position = "dodge")  + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)


# 5. fold change 
raw_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(median)) -> fc_median

raw_info_add_set %>% 
  select(Group, Change_names(candidate_metabo)) %>% 
  group_by(Group) %>% 
  summarise_each(funs(mean)) -> fc_mean

## FC with median 
which(t(as.data.frame(fc_median[2, ] / fc_median[1, ])[-1])[, 1] > 1.50 | 
        t(as.data.frame(fc_median[2, ] / fc_median[1, ])[-1])[, 1] < 0.67)

## FC with mean 
which(t(as.data.frame(fc_mean[2, ] / fc_mean[1, ])[-1])[, 1] > 1.50 | 
        t(as.data.frame(fc_mean[2, ] / fc_mean[1, ])[-1])[, 1] < 0.67)


# 6. PSM을 이용한 matching
summary(matchit(Group ~ sex + age, method = "optimal", distance = "logit", data = raw_info_add_set, ratio = 2))

# all variable을 이용한 PSM
summary(matchit(formula = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+", paste(Change_names(candidate_metabo), collapse = " + ")))
                ,method = "optimal", data = raw_info_add_set, ratio = 2))

# 가독성을 위해 match 정보를 변수로 저장 
PSM_all_variable <- matchit(formula = Group ~ sex + age + smoking + alcohol + beta_Hydroxybutyric_acid + 
                              Acetylcholine + L_Alanine + L_Arginine + L_Aspartic_acid + 
                              L_Asparagine + L_Carnitine + Choline + Creatinine + Dimethylglycine + 
                              Gamma_Aminobutyric_acid + Betaine + L_Glutamine + Glycine + 
                              L_Isoleucine + L_Kynurenine + L_Leucine + L_Lysine + L_Methionine + 
                              Nicotinic_acid + L_Phenylalanine + L_Proline + Pyridoxamine + 
                              Pyridoxine + L_Serine + Taurine + L_Threonine + Hydroxy_L_proline + 
                              Urea + L_Valine + L_Acetylcarnitine + Decanoylcarnitine + 
                              L_Glutamic_acid + Hexanoylcarnitine + Isovalerylcarnitine + 
                              L_Octanoylcarnitine + Glycerophosphocholine + Trimethylamine_N_oxide,
                            method = "subclass", distance = "logit", data = raw_info_add_set, ratio = 2)

summary(PSM_all_variable)
length(unique(PSM_all_variable$subclass))


# sex, age를 이용한 PSM 결과를 저장, PSM1_raw_info...
PSM1_raw_info_add_set <- match.data(matchit(Group ~ sex + age, 
                                            method = "optimal", 
                                            distance = "logit",
                                            data = raw_info_add_set, ratio = 2))

# 모든 variable을 이용한 PSM 결과를 저장, PSM2_raw_info...
PSM2_raw_info_add_set <- match.data(PSM_all_variable)



# t-test로 test 결과 matching이 이상한 것 같다. 
lapply(Change_names(candidate_metabo), function(v) {
  t.test(as.data.frame(PSM2_raw_info_add_set)[, v] ~ PSM2_raw_info_add_set$Group)
})

# 내가 지금 이쯤부터 뭔가를 잘못하고 있는 것 같은데?
# matching부터 다시 하자. 




# 사용할 formula, significant한 metabolites + "sex", "age", "smoking", "alcohol"
PSM_formula_candi = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                                     paste(Change_names(candidate_metabo), collapse = " + "),
                                     "+ strata(subclass)"))


# PSM1_raw_info_add_set을 이용한 CLR
# 같은 Group과 같은 variable에 obs의 tie가 존재하므로 "exact"를 사용 할 수 없다. 
summary(clogit(formula = Group ~ beta_Hydroxybutyric_acid + 
                 Acetylcholine + L_Alanine + L_Arginine + L_Aspartic_acid + 
                 L_Asparagine + L_Carnitine + Choline + Creatinine + Dimethylglycine + 
                 Gamma_Aminobutyric_acid + Betaine + L_Glutamine + Glycine + 
                 L_Isoleucine + L_Kynurenine + L_Leucine + L_Lysine + L_Methionine + 
                 Nicotinic_acid + L_Phenylalanine + L_Proline + Pyridoxamine + 
                 Pyridoxine + L_Serine + Taurine + L_Threonine + Hydroxy_L_proline + 
                 Urea + L_Valine + L_Acetylcarnitine + Decanoylcarnitine + 
                 L_Glutamic_acid + Hexanoylcarnitine + Isovalerylcarnitine + 
                 L_Octanoylcarnitine + Glycerophosphocholine + Trimethylamine_N_oxide + strata(subclass), 
               data = PSM1_raw_info_add_set, method='efron'))
# not converge

# iteration을 늘려서 다시 시도
summary(clogit(formula = PSM_formula_candi, data = PSM1_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), method='efron'))
# error : Loglik converged before variable; coefficient may be infinite.

summary(clogit(formula = formula_special, 
               data = raw_info_add_set, control = coxph.control(iter.max = 10000), method='efron'))

summary(clogit(formula = Group ~ sex + age + smoking + 
                 alcohol + L_Acetylcarnitine + Decanoylcarnitine + L_Glutamic_acid + 
                 Hexanoylcarnitine + Isovalerylcarnitine + L_Octanoylcarnitine + 
                 Glycerophosphocholine + Trimethylamine_N_oxide + 
                 beta_Hydroxybutyric_acid + Acetylcholine + L_Alanine + 
                 L_Aspartic_acid + L_Asparagine + strata(subclass), 
               data = PSM1_raw_info_add_set, control = coxph.control(iter.max = 10000), method='efron'))

# 변수가 18개 이상되는 순간부터 error가 난다.
# 17개의 변수를 넣으면 모든 변수들이 유의하지 않게 된다. 
# 사실 그 이전부터 변수를 추가하면 추가할수록 Wald test stat은 계속 증가했었다.


summary(clogit(formula = Group ~ sex + age + smoking + 
                 alcohol + L_Isoleucine + L_Kynurenine + L_Leucine + L_Lysine + L_Methionine + 
                 L_Acetylcarnitine + Decanoylcarnitine + 
                 L_Glutamic_acid + Hexanoylcarnitine + Isovalerylcarnitine + 
                 L_Octanoylcarnitine + Glycerophosphocholine + Trimethylamine_N_oxide + strata(set), 
               data = raw_info_add_set, control = coxph.control(iter.max = 10000), method='efron'))


# Fold change가 큰 변수들의 개수를 줄이니까 18개 미만임에도 inf coef error가 난다. 
# PSM, 내 임의 매칭 모두 같은 error 



# PSM2_raw_info_add_set을 이용한 CLR
summary(clogit(formula = Group ~ smoking + alcohol + beta_Hydroxybutyric_acid + 
                 Acetylcholine + L_Alanine + L_Arginine + L_Aspartic_acid + 
                 L_Asparagine + L_Carnitine + Choline + Creatinine + Dimethylglycine + 
                 Gamma_Aminobutyric_acid + Betaine + L_Glutamine + Glycine + 
                 L_Isoleucine + L_Kynurenine + L_Leucine + L_Lysine + L_Methionine + 
                 Nicotinic_acid + L_Phenylalanine + L_Proline + Pyridoxamine + 
                 Pyridoxine + L_Serine + Taurine + L_Threonine + Hydroxy_L_proline + 
                 Urea + L_Valine + L_Acetylcarnitine + Decanoylcarnitine + 
                 L_Glutamic_acid + Hexanoylcarnitine + Isovalerylcarnitine + 
                 L_Octanoylcarnitine + Glycerophosphocholine + Trimethylamine_N_oxide + strata(subclass), 
               data = PSM2_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), 
               method='efron'))

summary(clogit(formula = as.formula(paste("Group ~ ", paste(a, collapse = " + "), "+ strata(subclass)")),
               data = PSM2_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), 
               method='efron'))

a <- c(base_var, Change_names(candidate_metabo))[-c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,29)]
a %in% Change_names(special_metabo)


summary(clogit(formula = Group ~ sex + age + smoking + 
                 alcohol + L_Acetylcarnitine + Decanoylcarnitine + L_Glutamic_acid + 
                 Hexanoylcarnitine + Isovalerylcarnitine + L_Octanoylcarnitine + 
                 Glycerophosphocholine + Trimethylamine_N_oxide + 
                 beta_Hydroxybutyric_acid + Acetylcholine + L_Alanine + 
                 L_Aspartic_acid + L_Asparagine + L_Carnitine + Choline + Creatinine + Dimethylglycine + 
                 Gamma_Aminobutyric_acid + Betaine + Taurine + Urea + 
                 strata(subclass), 
               data = PSM2_raw_info_add_set, control = coxph.control(iter.max = 10000), method='efron'))

# PSM2_raw_info_add_set(all var을 이용한 PSM) 의 경우
# 25개에서 에러 
# 24개 째에서 어떤 것을 넣느냐에 따라 wald stat이 조금 달라지긴 함. 

#### 결과보고를 위한 작성 ####


# CLR의 method에 대한 note
# CLR에서 arg로 등록되어 있는 method는 "exact", "efron", "approximate", "breslow" 등, 총 4개다. 
# exact을 제외한 나머지 세 방법은 approximate method이다.
# 'tie'에 대한 approximation 여부에 따라 exact vs non-exact로 나뉜다. 
# 이 때, tie란 말 그대로 같은 group(categorical response var) level 하에서의 variable 중 똑같은 obs을 말한다. 
# 4개의 방법 중 가장 대중적으로 쓰이는 것은 efron이다. 
# R를 제외한 대부분의 S/W에서 CLR method의 default는 efron이다. R의 clogit의 default는 exact다. 

larynx <- read.table( "http://www.ics.uci.edu/~dgillen/STAT255/Data/larynx.txt" )

dim(larynx)
unique(larynx$t2death[ larynx$death==1 ][which(duplicated(larynx$t2death[ larynx$death==1 ] ))])

larynx[which(duplicated(larynx$t2death[ larynx$death==1 ] )), ]
sum( duplicated(larynx$t2death[ larynx$death==1 ] ) )


#### 결과보고를 위한 작성 ####

# 결과 작성을 위한 함수 만들기
```

```r
#### 1.30 ####

#### 1. 정규성 검정 ####


raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  lapply(., shapiro.test) %>% 
  unlist() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  
  # 정규성 검정 결과
  dplyr::filter(grepl("p.value", rowname)) %>% 
  write.xlsx("normal_test_case.xlsx")

raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  select(all_metabolites) %>% 
  lapply(., shapiro.test) %>% 
  unlist() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  
  # 정규성 검정 결과
  dplyr::filter(grepl("p.value", rowname)) %>% 
  write.xlsx("normal_test_control.xlsx")



#### 1. 정규성 검정 ####

#### Primary task, basical table ####
#### base ####
# gender
raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, sex)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, sex)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

# age, continuous
raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, age)) %>% 
  dplyr::filter(Group == 0) %>% 
  summarise_all(funs(mean, sd))

raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, age)) %>% 
  dplyr::filter(Group == 1) %>% 
  summarise_all(funs(mean, sd))
#### base ####

#### age ####
raw_info_add_set %>% 
  rownames_to_column() %>% 
  type_convert(cols(rowname = col_double())) -> index_raw_info_add_set

# control age 추출 
index_raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  select(rowname, age) -> control_age

# case age 추출 
index_raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>% 
  select(rowname, age) -> case_age

# 다시 한번 quantile 확인 
round(quantile(as.data.frame(control_age)$age, probs = seq(0, 1, length = 5)))
round(quantile(as.data.frame(case_age)$age, probs = seq(0, 1, length = 5)))

# age를 categorical로 바꿔주는 함수 
age_to_categorical <- function(data){
  c <- as.vector(round(quantile(as.data.frame(data)$age, probs = seq(0, 1, length = 5))))
  cate_age <- c()
  
  for(i in 1:nrow(data)){
    if(as.data.frame(data)[i, "age"] <  c[2]) {
      cate_age[i] <- 1
    } else if(as.data.frame(data)[i, "age"] <  c[3]) {
      cate_age[i] <- 2
    } else if(as.data.frame(data)[i, "age"] <  c[4]) {
      cate_age[i] <- 3
    } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
      cate_age[i] <- 4
    }
  }
  result <- cbind(rowname = data$rowname, cate_age)
  return(result)
}

age_to_categorical_control <- function(data){
  c <- as.vector(round(quantile(as.data.frame(control_age)$age, probs = seq(0, 1, length = 5))))
  cate_age <- c()
  
  for(i in 1:nrow(data)){
    if(as.data.frame(data)[i, "age"] <  c[2]) {
      cate_age[i] <- 1
    } else if(as.data.frame(data)[i, "age"] <  c[3]) {
      cate_age[i] <- 2
    } else if(as.data.frame(data)[i, "age"] <  c[4]) {
      cate_age[i] <- 3
    } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
      cate_age[i] <- 4
    } else 
      cate_age[i] <- 4
  }
  result <- cbind(rowname = data$rowname, cate_age)
  return(result)
}

age_to_categorical_overall <- function(data){
  c <- as.vector(round(quantile(as.data.frame(raw_info_add_set)$age, probs = seq(0, 1, length = 5))))
  cate_age <- c()
  
  for(i in 1:nrow(data)){
    if(as.data.frame(data)[i, "age"] <  c[2]) {
      cate_age[i] <- 1
    } else if(as.data.frame(data)[i, "age"] <  c[3]) {
      cate_age[i] <- 2
    } else if(as.data.frame(data)[i, "age"] <  c[4]) {
      cate_age[i] <- 3
    } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
      cate_age[i] <- 4
    } else 
      cate_age[i] <- 4
  }
  result <- cbind(rowname = data$rowname, cate_age)
  return(result)
}

categorical_age <- rbind(age_to_categorical_overall(case_age), 
                         age_to_categorical_overall(control_age))

categorical_age %>% 
  as.data.frame() %>% 
  arrange(rowname) -> categorical_age

# age를 categorical로 바꾼 dataset 
index_raw_info_add_set %>% 
  merge(categorical_age, by = "rowname") %>% 
  select(rowname, set, Group, sex, age, cate_age, everything()) -> age_c_raw_info_add_set

# 4분위수를 기준, categorical age의 갯수
# control
age_c_raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, cate_age)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

# case
age_c_raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, cate_age)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

#### age ####

# smoking status
raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, smoking)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, smoking)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

# alcohol status
raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, alcohol)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

raw_info_add_set %>% 
  group_by(Group) %>% 
  select(c(Group, alcohol)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

#### metabolites ####
# control group mean by column-wise
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q25"))  %>% 
  rename_at(vars(matches("_q25$")), funs(str_replace(., "_q25", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q50"))  %>% 
  rename_at(vars(matches("_q50$")), funs(str_replace(., "_q50", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q75"))  %>% 
  rename_at(vars(matches("_q75$")), funs(str_replace(., "_q75", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

# caes group mean by column-wise
raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q25"))  %>% 
  rename_at(vars(matches("_q25$")), funs(str_replace(., "_q25", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q50"))  %>% 
  rename_at(vars(matches("_q50$")), funs(str_replace(., "_q50", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>%
  select(Group, age, 8:88) %>% 
  summarise_all(funs(q25 = quantile(., probs = .25),
                     q50 = quantile(., probs = .5),
                     q75 = quantile(., probs = .75))) %>% 
  select(contains("_q75"))  %>% 
  rename_at(vars(matches("_q75$")), funs(str_replace(., "_q75", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname)

#### metabolites ####

#### function to show ####
report_result_test <- function() {
  # gender
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, sex)) %>% 
    dplyr::filter(Group == 0) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r1
  
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, sex)) %>% 
    dplyr::filter(Group == 1) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r2
  
  # age, continuous
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, age)) %>% 
    dplyr::filter(Group == 0) %>% 
    summarise_all(funs(mean, sd)) -> r3
  
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, age)) %>% 
    dplyr::filter(Group == 1) %>% 
    summarise_all(funs(mean, sd)) -> r4
  
  #### age ####
  raw_info_add_set %>% 
    rownames_to_column() %>% 
    type_convert(cols(rowname = col_double())) -> index_raw_info_add_set
  
  # control age 추출 
  index_raw_info_add_set %>% 
    dplyr::filter(Group == 0) %>% 
    select(rowname, age) -> control_age
  
  # case age 추출 
  index_raw_info_add_set %>% 
    dplyr::filter(Group == 1) %>% 
    select(rowname, age) -> case_age
  
  # 다시 한번 quantile 확인 
  round(quantile(as.data.frame(control_age)$age, probs = seq(0, 1, length = 5)))
  round(quantile(as.data.frame(case_age)$age, probs = seq(0, 1, length = 5)))
  
  # age를 categorical로 바꿔주는 함수 
  age_to_categorical <- function(data){
    c <- as.vector(round(quantile(as.data.frame(data)$age, probs = seq(0, 1, length = 5))))
    cate_age <- c()
    
    for(i in 1:nrow(data)){
      if(as.data.frame(data)[i, "age"] <  c[2]) {
        cate_age[i] <- 1
      } else if(as.data.frame(data)[i, "age"] <  c[3]) {
        cate_age[i] <- 2
      } else if(as.data.frame(data)[i, "age"] <  c[4]) {
        cate_age[i] <- 3
      } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
        cate_age[i] <- 4
      }
    }
    result <- cbind(rowname = data$rowname, cate_age)
    return(result)
  }
  
  age_to_categorical_control <- function(data){
    c <- as.vector(round(quantile(as.data.frame(control_age)$age, probs = seq(0, 1, length = 5))))
    cate_age <- c()
    
    for(i in 1:nrow(data)){
      if(as.data.frame(data)[i, "age"] <  c[2]) {
        cate_age[i] <- 1
      } else if(as.data.frame(data)[i, "age"] <  c[3]) {
        cate_age[i] <- 2
      } else if(as.data.frame(data)[i, "age"] <  c[4]) {
        cate_age[i] <- 3
      } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
        cate_age[i] <- 4
      } else 
        cate_age[i] <- 4
    }
    result <- cbind(rowname = data$rowname, cate_age)
    return(result)
  }
  
  age_to_categorical_overall <- function(data){
    c <- as.vector(round(quantile(as.data.frame(raw_info_add_set)$age, probs = seq(0, 1, length = 5))))
    cate_age <- c()
    
    for(i in 1:nrow(data)){
      if(as.data.frame(data)[i, "age"] <  c[2]) {
        cate_age[i] <- 1
      } else if(as.data.frame(data)[i, "age"] <  c[3]) {
        cate_age[i] <- 2
      } else if(as.data.frame(data)[i, "age"] <  c[4]) {
        cate_age[i] <- 3
      } else if (as.data.frame(data)[i, "age"] <=  c[5]) {
        cate_age[i] <- 4
      } else 
        cate_age[i] <- 4
    }
    result <- cbind(rowname = data$rowname, cate_age)
    return(result)
  }
  
  categorical_age <- rbind(age_to_categorical_overall(case_age), 
                           age_to_categorical_overall(control_age))
  
  categorical_age %>% 
    as.data.frame() %>% 
    arrange(rowname) -> categorical_age
  
  # age를 categorical로 바꾼 dataset 
  index_raw_info_add_set %>% 
    merge(categorical_age, by = "rowname") %>% 
    select(rowname, set, Group, sex, age, cate_age, everything()) -> age_c_raw_info_add_set
  
  # 4분위수를 기준, categorical age의 갯수
  # control
  age_c_raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, cate_age)) %>% 
    dplyr::filter(Group == 0) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r5
  
  # case
  age_c_raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, cate_age)) %>% 
    dplyr::filter(Group == 1) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r6
  
  #### age ####
  
  # smoking status
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, smoking)) %>% 
    dplyr::filter(Group == 0) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r7
  
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, smoking)) %>% 
    dplyr::filter(Group == 1) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r8
  
  # alcohol status
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, alcohol)) %>% 
    dplyr::filter(Group == 0) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r9
  
  raw_info_add_set %>% 
    group_by(Group) %>% 
    select(c(Group, alcohol)) %>% 
    dplyr::filter(Group == 1) %>% 
    gather(Group, var) %>% 
    count(Group, var) %>% 
    spread(var, n, fill = 0) -> r10
  
  #### metabolites ####
  # control group mean by column-wise
  raw_info_add_set %>% 
    dplyr::filter(Group == 0) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q25"))  %>% 
    rename_at(vars(matches("_q25$")), funs(str_replace(., "_q25", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r11
  
  raw_info_add_set %>% 
    dplyr::filter(Group == 0) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q50"))  %>% 
    rename_at(vars(matches("_q50$")), funs(str_replace(., "_q50", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r12 
  
  raw_info_add_set %>% 
    dplyr::filter(Group == 0) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q75"))  %>% 
    rename_at(vars(matches("_q75$")), funs(str_replace(., "_q75", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r13 

  # caes group mean by column-wise
  raw_info_add_set %>% 
    dplyr::filter(Group == 1) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q25"))  %>% 
    rename_at(vars(matches("_q25$")), funs(str_replace(., "_q25", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r14
  
  raw_info_add_set %>% 
    dplyr::filter(Group == 1) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q50"))  %>% 
    rename_at(vars(matches("_q50$")), funs(str_replace(., "_q50", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r15 
  
  raw_info_add_set %>% 
    dplyr::filter(Group == 1) %>%
    select(Group, age, 8:88) %>% 
    summarise_all(funs(q25 = quantile(., probs = .25),
                       q50 = quantile(., probs = .5),
                       q75 = quantile(., probs = .75))) %>% 
    select(contains("_q75"))  %>% 
    rename_at(vars(matches("_q75$")), funs(str_replace(., "_q75", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> r16 

  #### metabolites ####
  
  result <- list(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16)
  return(result)
}

report_result_test() %>% 
  write.xlsx("median_25_75.xlsx")
#### function to show ####

#### distribution test ####
# age kruskal test 
lapply("age", function(v) {
  kruskal.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])
})

# metabolites kruskal test
kruskal.test <- lapply(all_metabolites, function(v) {
  kruskal.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])
})

dim(t(t(unlist(kruskal.test))))

t(t(unlist(kruskal.test))) %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  dplyr::filter(grepl("^p.value", rowname)) %>% 
  write.xlsx("kruskal_test_metabolites.xlsx")
#### distribution test ####

#### histogram #### 
ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[1:19])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) +
  ggsave(paste0(dir, "/hist_1.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[20:38])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) +
  ggsave(paste0(dir, "/hist_2.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[39:57])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) + 
  ggsave(paste0(dir, "/hist_3.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[58:76])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) + 
  ggsave(paste0(dir, "/hist_4.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[77:81])], id.var = "Group"), 
       aes(x = value, fill = factor(Group), colour = factor(Group))) + 
  geom_density(alpha = 0.5) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) + 
  ggsave(paste0(dir, "/hist_5.jpg"), width=30, height=15, units=c("cm"))
#### histogram #### 

#### box-plot #### 
ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[1:19])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)  + 
  ggsave(paste0(dir, "/box_1.jpg"), width=30, height=15, units=c("cm"))


ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[20:38])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE) + 
  ggsave(paste0(dir, "/box_2.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[39:57])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)  + 
  ggsave(paste0(dir, "/box_3.jpg"), width=30, height=15, units=c("cm"))


ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[58:76])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)  + 
  ggsave(paste0(dir, "/box_4.jpg"), width=30, height=15, units=c("cm"))

ggplot(melt(raw_info_add_set[,  c("Group", Change_names(all_metabolites)[77:81])], id.var = "Group"), 
       aes(x=variable, y=value)) + 
  geom_boxplot(aes(fill=as.factor(Group))) + 
  facet_wrap( ~ variable, scales="free") + 
  scale_fill_discrete(name = "C & OC", labels = c("C", "OC")) + 
  scale_colour_discrete(guide=FALSE)  + 
  ggsave(paste0(dir, "/box_5.jpg"), width=30, height=15, units=c("cm"))
#### box-plot #### 

#### Primary task, basical table ####





#### 2. control의 median 기준으로 나눌 것 ####
# 기존의 code, 전체를 기준으로 median으로 나눔
raw_info_add_set %>% 
  mutate_at(vars(8:88), list(~replace(., Group != 3, ntile(., 2)))) -> median_test_set

# control 기준, median 계산 
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  summarise_at(vars(8:88), funs(median)) -> median_standard


replace.using.median <- function(data){ 
  u <- matrix(0, nrow(data), ncol(data))
  
  for(i in 1:length(median_standard)){ 
    for (j in 1:nrow(data)){
      
      ## median보다 작으면 1, median보다 크면 2
      if(median_standard[, i] > data[j, i]) {
        u[j, i] <- 1 
      } else{
        u[j, i] <- 2
      }
    }
  }
  u <- as.data.frame(u)
  colnames(u) <- names(median_standard)
  return(u)
}

u <- replace.using.median(raw_info_add_set[, all_metabolites])
dim(u)

#### 함수 결과 검증  ####
u[, 1] # 함수를 이용한 beta_Hydroxy 변환 결과 
as.numeric(as.vector((6388 > raw_info_add_set[, 8]))) # 직접 해본 beta_Hydroxy 변환 결과 
## 같음 

dim(cbind(raw_info_add_set[, 1:7], u))
dim(raw_info_add_set)
## 같음 

# 새로운 data set으로 선언 
median_data_set <- as.data.frame(cbind(raw_info_add_set[, 1:7], u))


# 이전 code와 달라졌는지 확인 
# old version
median_test_set %>% 
  group_by(Group) %>% 
  select(c(Group, Change_names(all_metabolites))) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)

# new version
median_data_set %>% 
  group_by(Group) %>% 
  select(c(Group, Change_names(all_metabolites))) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  count(Group, var) %>% 
  spread(var, n, fill = 0)
# 달라졌음을 확인함 

#### 함수 결과 검증 : 맞음 ####

median_standard # Control group으로 계산한 median set
replace.using.median() # median_standard를 이용, categorical로 변환시켜주는 함수
median_data_set # 위의 두 object를 이용해 새로 선언한 dataset 

CLR_mfactor_c_HW <- function(data, metabolites_name, strata_name, point) { 
  
  m1 <- list()
  n <- c()
  m1_j <- 1
  
  a1 <-list()
  all_name <- c()
  
  for(i in 1:length(metabolites_name)) {
    formula <- as.formula(paste("Group ~ ", 
                                paste0("factor(", "sex)"),
                                "+ age", 
                                paste0("+ factor(", "smoking)"),
                                paste0("+ factor(", "alcohol)"),
                                paste0("+ factor(", metabolites_name[i], ")"),
                                paste0("+ strata(", strata_name, ")") ))
    
    r1 <- summary(clogit(formula = formula, 
                         data = data, control = coxph.control(iter.max = 100), method='exact'))
    
    # 모든 결과를 a1에 저장
    a1[[i]] <- r1
    all_name <- c(all_name, metabolites_name[i])
    
    # p-value, 0.05보다 작은 결과만 m1에 저장 
    if(r1$coefficients[point,5] < 0.05) { 
      m1[[m1_j]] <- r1
      m1_j <- m1_j+1
      n <- c(n, metabolites_name[i])
      
    }
  }
  
  result <- list(a1, all_name, m1, n)
  
  return(result)
}
i <- 81
#### Point 체크를 위한 따로 돌려보기 ####
r1 <- summary(clogit(formula = formula, 
                     data = median_data_set, control = coxph.control(iter.max = 100), method='exact'))

r1$coefficients[7,5]
#### Point 체크를 위한 따로 돌려보기 ####
# median에서는 point 9

CLR_median <- CLR_mfactor_c_HW(median_data_set, all_metabolites, "set", 7)

table_gen <- function(result, point) {
  
  z <- result
  q <- z[[2]]
  
  r <- matrix(0, length(z[[1]]), (length(z[[1]][[1]]$conf.int[point, ]))+1)
  
  for(i in 1:length(z[[1]])) {
    r[i, ] <- c(z[[1]][[i]]$conf.int[point, ], z[[1]][[i]]$coefficients[point, 5])
  }
  
  e <- as.data.frame(cbind(q, r))
  
  colnames(e) = c("Metabolites","exp(coef)", "exp(-coef)", "lower .95", "upper .95", "p-value")
  
  return(e)
}

table_gen(CLR_median, 7)

#### median 기준의 simple CLR ####
UsCLR <- function(data, target_position) {
  
  result <- list(NULL, NULL)
  summary_UsCLR <- c()
  
  
  list <- names(data[-target_position])
  
  for (i in 1 : length(list)){
    formula <- as.formula(paste("Group ~", list[i], "+ strata(set)"))
    
    result_ith_UsCLR1 <- summary(clogit(formula = formula, data = data, method = "efron"))$coefficients
    result_ith_UsCLR2 <- summary(clogit(formula = formula, data = data, method = "efron"))$conf.int
    
    
    sub_result <- c(result_ith_UsCLR1, result_ith_UsCLR2)
    
    summary_UsCLR <- rbind(summary_UsCLR, c(list[i], result_ith_UsCLR1, result_ith_UsCLR2))
  }
  
  summary_UsCLR <- as.data.frame(summary_UsCLR)
  
  #### <TO DO> rename으로바꿔보기 ####
  colnames(summary_UsCLR) <- c("Metabolites","coef", "exp(coef)", "se(coef)", "z", "p_value", "exp(coef)_re", "exp(-coef)_re", "lower .95", "upper .95")
  
  summary_UsCLR -> result[[1]]
  # tibble::rownames_to_column(., "Name") %>%
  # dplyr::arrange(p_value) %>%
  
  
  summary_UsCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) -> result[[2]]
  
  return(result)
}

SCLR_median <- UsCLR(median_data_set[, c("set","Group","sex","age","smoking","alcohol","stage", Change_names(all_metabolites))],
                     c(1,2,7))[[1]] 


#### median 기준의 simple CLR ####

# MCLR + SCLR, 결과 joint
table_gen(CLR_median, 7) %>% 
  cbind(SCLR_median[-(1:4), ]) %>% 
  as.data.frame() -> median_CLR

# control group, median 기준 n개
median_data_set %>% 
  group_by(Group) %>% 
  select(c(Group, 8:88)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 364), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> control_median_n

# case group, median 기준 n개
median_data_set %>% 
  group_by(Group) %>% 
  select(c(Group, 8:88)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 182), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> case_median_n

as.data.frame(median_standard) %>% 
  t() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  rename(metabolites = rowname, median = V1) -> median_criteria


#### TO write table ####
# 다시 체크 
n2 <- c()
for(i in 1:length(all_metabolites)) {
  if( i%%2 != 0){ 
    k <-  (i*2)-1
    
    b1 <- c(median_CLR[i, 1], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b2 <- c("Low", median_criteria[i, 2], case_median_n[k, 4], control_median_n[k, 4], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b3 <- c("High", median_criteria[i, 2], case_median_n[k+1, 4], control_median_n[k+1, 4],
            median_CLR[i, ])
    
    n1 <- rbind(b1, b2, b3)    
    
    } else {
      k <-  (i*2)-1
      
      b1 <- c(median_CLR[i, 1], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
      b2 <- c("Low", median_criteria[i, 2], case_median_n[k, 4], control_median_n[k, 4], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
      b3 <- c("High", median_criteria[i, 2], case_median_n[k+1, 4], control_median_n[k+2, 4],
              median_CLR[i, ])
      
      n1 <- rbind(b1, b2, b3)
    }
  n2 <- rbind(n2, n1)
    
}

# Check # 
as.data.frame(n2)[1:9, 1:4]
median_criteria[1:3, ]
case_median_n[1:6, ]
control_median_n[1:6, ]

as.data.frame(n2)[10:18, 1:4]
median_criteria[4:6, ]
case_median_n[7:12, ]
control_median_n[7:12, ]

as.data.frame(n2)[1:9, 5:10]
median_CLR[1:3, 1:6]

as.data.frame(n2)[10:18, 5:10]
median_CLR[4:6, 1:6]

as.data.frame(n2)[1:9, 11:20]
median_CLR[1:3, 7:16]

as.data.frame(n2)[10:18, 11:20]
median_CLR[4:6, 7:16]



n2 %>% 
  write.xlsx("median_result.xlsx")
#### TO write table ####


#### 2. control의 median 기준으로 나눌 것 ####




#### 3. control을 기준으로 3분할 ####
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>%
  select(8:88) %>% 
  summarise_all(funs(q33 = quantile(., probs = .33),
                     q66 = quantile(., probs = .66))) %>% 
  select(contains("_q33"))  %>% 
  rename_at(vars(matches("_q33$")), funs(str_replace(., "_q33", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname) -> mid_standard

raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>%
  select(8:88) %>% 
  summarise_all(funs(q33 = quantile(., probs = .33),
                     q66 = quantile(., probs = .66))) %>% 
  select(contains("_q66"))  %>% 
  rename_at(vars(matches("_q66$")), funs(str_replace(., "_q66", ""))) %>% 
  rownames_to_column %>%
  gather(variable, value, -rowname) -> high_standard



replace.using.mid.high <- function(data){ 
  u <- matrix(0, nrow(data), ncol(data))
  
  for(i in 1:nrow(mid_standard)){ 
    for (j in 1:nrow(data)){
      
      ## 33th 보다 작으면 1, 
      ## 1보다는 크고 66th보다 작으면 2
      ## 66th보다 크면 3
      if(mid_standard[i, 3] > data[j, i]) {
        u[j, i] <- 1 
      } else if(high_standard[i, 3] > data[j, i]) {
        u[j, i] <- 2
      } else {
        u[j, i] <- 3
      }
    }
  }
  u <- as.data.frame(u)
  colnames(u) <- all_metabolites
  return(u)
}

u <- replace.using.mid.high(raw_info_add_set[, all_metabolites])

#### 제대로 바뀌었는지 check ####
u %>% 
  as_tibble()

raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  mutate_at(vars(8:88), list(~replace(., Group == 0, ntile(., 3)))) %>% 
  select(8) %>% as.data.frame() -> check_divided

u[, 1] == as.vector(t(check_divided))
raw_info_add_set[, 8]
cbind(raw_info_add_set[, 8], u[, 1], check_divided)
#### 완료 제대로 바뀌었는지 check ####

mid_high_data_set <- as.data.frame(cbind(raw_info_add_set[, 1:7], u))


CLR_mfactor_c_HW <- function(data, metabolites_name, strata_name, point) { 
  
  m1 <- list()
  n <- c()
  m1_j <- 1
  
  a1 <-list()
  all_name <- c()
  
  for(i in 1:length(metabolites_name)) {
    formula <- as.formula(paste("Group ~ ", 
                                paste0("factor(", "sex)"),
                                "+ age", 
                                paste0("+ factor(", "smoking)"),
                                paste0("+ factor(", "alcohol)"),
                                paste0("+ factor(", metabolites_name[i], ")"),
                                paste0("+ strata(", strata_name, ")") ))
    
    r1 <- summary(clogit(formula = formula, 
                         data = data, control = coxph.control(iter.max = 100), method='exact'))
    
    # 모든 결과를 a1에 저장
    a1[[i]] <- r1
    all_name <- c(all_name, metabolites_name[i])
    
    # p-value, 0.05보다 작은 결과만 m1에 저장 
    if(r1$coefficients[point,5] < 0.05) { 
      m1[[m1_j]] <- r1
      m1_j <- m1_j+1
      n <- c(n, metabolites_name[i])
      
    }
  }
  
  result <- list(a1, all_name, m1, n)
  
  return(result)
}

#### Point 체크를 위한 따로 돌려보기 ####
r1 <- summary(clogit(formula = formula, 
                     data = median_data_set, control = coxph.control(iter.max = 100), method='exact'))

r1$coefficients[7,5]
#### Point 체크를 위한 따로 돌려보기 ####
# median에서는 point 9

CLR_mid_high <- CLR_mfactor_c_HW(mid_high_data_set, all_metabolites, "set", 8)

table_gen <- function(result, point) {
  
  z <- result
  q <- z[[2]]
  
  r <- matrix(0, 2, (length(z[[1]][[1]]$conf.int[point, ]))+1)
  r2 <- matrix(0, 2, (length(z[[1]][[1]]$conf.int[point, ]))+1)
  for(i in 1:length(z[[1]])) {
    r[1, ] <- c(z[[1]][[i]]$conf.int[point, ], z[[1]][[i]]$coefficients[point, 5])
    r[2, ] <- c(z[[1]][[i]]$conf.int[point+1, ], z[[1]][[i]]$coefficients[point+1, 5])
    
    r2 <- rbind(r2, r)
  }
  r2 <- r2[-c(1:2), ]
  
  e <- as.data.frame(cbind(rep(q, each =2), r2))
  
  colnames(e) = c("Metabolites","exp(coef)", "exp(-coef)", "lower .95", "upper .95", "p-value")
  
  return(e)
}

table_gen(CLR_mid_high, 7)



#### mid, high 기준의 simple CLR ####

UsCLR_mid_high <- function(data, target_position) {
  
  result <- list(NULL, NULL)
  summary_UsCLR <- c()
  
  list <- names(data[-target_position])
  
  for (i in 1 : length(list)){
    formula <- as.formula(paste("Group ~", 
                                paste0("factor(", list[i], ")"),
                                "+ strata(set)"))
    
    result_ith_UsCLR1 <- summary(clogit(formula = formula, data = data, method = "efron"))$coefficients
    result_ith_UsCLR2 <- summary(clogit(formula = formula, data = data, method = "efron"))$conf.int
    
    
    sub_result <- cbind(result_ith_UsCLR1, result_ith_UsCLR2)
    
    summary_UsCLR <- rbind(summary_UsCLR, sub_result)
  }
  
  as.data.frame(summary_UsCLR) %>% 
    rownames_to_column() -> summary_UsCLR
   
  
  #### <TO DO> rename으로바꿔보기 ####
  colnames(summary_UsCLR) <- c("Metabolites","coef", "exp(coef)", "se(coef)", "z", "p_value", "exp(coef)_re", "exp(-coef)_re", "lower .95", "upper .95")
  
  summary_UsCLR -> result[[1]]
  # tibble::rownames_to_column(., "Name") %>%
  # dplyr::arrange(p_value) %>%
  
  
  summary_UsCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) -> result[[2]]
  
  return(result)
}

SCLR_mid_high <- UsCLR_mid_high(mid_high_data_set[, c("set","Group","sex","age","smoking","alcohol","stage", Change_names(all_metabolites))],
                       c(1,2,4,7))[[1]] 

SCLR_mid_high # 체크 완료  



# MCLR + SCLR, 결과 joint
table_gen(CLR_mid_high, 7) %>% 
  cbind(SCLR_mid_high[-(1:5), ]) %>% 
  as.data.frame() -> mid_high_CLR

# control group, mid,high 기준 n개
mid_high_data_set %>% 
  group_by(Group) %>% 
  select(c(Group, 8:88)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 364), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> control_mid_high_n

# case group, mid,high 기준 n개
mid_high_data_set %>% 
  group_by(Group) %>% 
  select(c(Group, 8:88)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 182), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> case_mid_high_n

as.data.frame(mid_standard) -> mid_criteria

as.data.frame(high_standard) -> high_criteria




i <- 2

#### TO write table ####
n2 <- c()
for(i in 1:length(all_metabolites)) {
  # 만약 4분할하면 3을 4로 바꿔주면 됨 
  
  # index가 홀수인 경우 
  if( (((case_mid_high_n$index[i]+(3*as.numeric(i)))-3)%%2) != 0 ){

    j <- (i*3)-2 # 만약 4분할하면 3 -> 4, 2 -> 3
    k <-  (i*2)-1 # 만약 4분할하면 2 -> 3, 1 -> 2
    b1 <- c(mid_high_CLR[k, 1], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b2 <- c("Low", mid_criteria[i, 3], case_mid_high_n[j, 4], control_mid_high_n[j, 4], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b3 <- c("Mid", high_criteria[i, 3], case_mid_high_n[j+1, 4], control_mid_high_n[j+1, 4], 
            mid_high_CLR[k, ])
    b4 <- c("High", high_criteria[i, 3], case_mid_high_n[j+2, 4], control_mid_high_n[j+2, 4],
            mid_high_CLR[k+1, ])
    
    n1 <- rbind(b1, b2, b3, b4)    
    
    # index가 짝수인 경우 
  } else {
    j <- (i*3)-2
    k <- (i*2)-1  
    b1 <- c(mid_high_CLR[k, 1], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b2 <- c("Low", mid_criteria[i, 3], case_mid_high_n[j, 4], control_mid_high_n[j, 4], "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    b3 <- c("Mid", high_criteria[i, 3], case_mid_high_n[j+1, 4], control_mid_high_n[j+1, 4], 
            mid_high_CLR[k, ])
    b4 <- c("High", high_criteria[i, 3], case_mid_high_n[j+2, 4], control_mid_high_n[j+2, 4],
            mid_high_CLR[k+1, ])
    
    n1 <- rbind(b1, b2, b3, b4) 
  }
  n2 <- rbind(n2, n1)
  
}

# Check #

as.data.frame(n2)[1:20, 1:4]
case_mid_high_n[1:18, ]
control_mid_high_n[1:18, ]
mid_criteria[1:5, ]
high_criteria[1:5, ]

as.data.frame(n2)[1:28, 5:10]
as.data.frame(n2)[29:56, 5:10]
as.data.frame(mid_high_CLR)[1:28, 1:6]


as.data.frame(n2)[1:12, 11:20]
as.data.frame(mid_high_CLR)[1:6, 7:16]

as.data.frame(n2)[13:24, 11:20]
as.data.frame(mid_high_CLR)[7:12, 7:16]



n2 %>% 
  write.xlsx("mid_high_result.xlsx")  

#### TO write table ####

#### 3. control을 기준으로 3분할 ####

#### 1.30 ####

```


```r
#### fold change ####

#### volcano plot ####
library(muma)
library(ggrepel)

# Using median
# Using median
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  dplyr::select(all_metabolites) %>% 
  apply(. ,2 , FUN=median) -> group0median

raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>% 
  dplyr::select(all_metabolites) %>% 
  apply(. ,2, FUN=median) -> group1median

FC <- group1median / group0median
log2FC <- log(FC, 2)

pvalue <- lapply(all_metabolites, function(v) {
  kruskal.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])$p.value
})

pvalue.BHcorr <- p.adjust(pvalue, method = "BH") # FDR
pvalue.BHcorr.neglog <- -log10(pvalue.BHcorr)

volcano.data <- data.frame(log2FC, FC, group1median, group0median, pvalue.BHcorr.neglog)

volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC < -1 & pvalue.BHcorr.neglog > 1.301) -> red_set

volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC > 1 & pvalue.BHcorr.neglog > 1.301) -> green_set

volcano.data$pvalue.BHcorr <- pvalue.BHcorr

volcano.data %>% 
  rownames_to_column() -> volcano.data
  

# Using mean
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  select(all_metabolites) %>% 
  apply(. ,2 , FUN=mean) -> group0mean

raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  apply(. ,2, FUN=mean) -> group1mean

FC <- group1mean / group0mean
log2FC <- log(FC, 2)

pvalue <- lapply(all_metabolites, function(v) {
  kruskal.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])$p.value
})

pvalue.BHcorr <- p.adjust(pvalue, method = "BH") # FDR
pvalue.BHcorr.neglog <- -log10(pvalue.BHcorr)

volcano.data <- data.frame(log2FC, FC, group1mean, group0mean, pvalue.BHcorr.neglog)

volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC < -1 & pvalue.BHcorr.neglog > 1.301) -> red_set

volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC > 1 & pvalue.BHcorr.neglog > 1.301) -> green_set

volcano.data$pvalue.BHcorr <- pvalue.BHcorr

volcano.data %>% 
  rownames_to_column() -> volcano.data

volcano.data$sig <- ifelse(volcano.data$pvalue.BHcorr.neglog < 1.301, "Not Sig",
                           ifelse(volcano.data$log2FC < -1 & volcano.data$pvalue.BHcorr.neglog > 1.301, "log2(FC) ≤ -1", 
                                  ifelse(volcano.data$log2FC > 1 & volcano.data$pvalue.BHcorr.neglog > 1.301, "log2(FC) ≥ 1", "-1 < log2(FC) < 1")))


# visualization

volcanoEM <- ggplot(volcano.data, aes(x= log2FC, y=pvalue.BHcorr.neglog)) +  
  geom_point(aes(color=sig)) + 
  scale_color_manual(values = c("black", "red", "green","grey")) + 
  theme_bw(base_size = 12) +  
  theme(legend.position = "right", legend.title = element_blank()) + 
  geom_text_repel(data = subset(volcano.data, sig == "log2(FC) ≤ -1" | sig == "log2(FC) ≥ 1"), aes(label = rowname), size=5, box.padding = unit(0.35, "lines"), point.padding = unit(0.3, "lines")) +
  ggtitle("Figure 1.1 Volcano plot using median fold change and p-value of Kruskal test results") + labs(x=bquote(~log[2]~ "Fold change"), y=bquote(~-log[10]~adjusted-~italic(P))) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15, color = "black"))


plot(volcanoEM)



# K result 
# Using mean 
raw_info_add_set %>% 
  dplyr::filter(Group == 0) %>% 
  select(all_metabolites) %>% 
  apply(. ,2 , FUN=mean) -> group0mean

raw_info_add_set %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  apply(. ,2, FUN=mean) -> group1mean

FC <- group1mean / group0mean
log2FC <- log(FC, 2)

K_pvalue <- lapply(all_metabolites, function(v) {
  t.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])$p.value
})

K_pvalue.BHcorr <- p.adjust(K_pvalue, method = "BH") # FDR
K_pvalue.BHcorr.neglog <- -log10(K_pvalue.BHcorr)

K_volcano.data <- data.frame(log2FC, FC, group1mean, group0mean, K_pvalue.BHcorr.neglog)

K_volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC < -1 & K_pvalue.BHcorr.neglog > 1.301) -> red_set

K_volcano.data %>% 
  rownames_to_column() %>% 
  dplyr::filter(log2FC > 1 & K_pvalue.BHcorr.neglog > 1.301) -> green_set

K_volcano.data$pvalue.BHcorr <- K_pvalue.BHcorr

K_volcano.data %>% 
  rownames_to_column() -> K_volcano.data

K_volcano.data$sig <- ifelse(K_volcano.data$K_pvalue.BHcorr.neglog < 1.301, "Not Sig",
                             ifelse(K_volcano.data$log2FC < -1 & K_volcano.data$K_pvalue.BHcorr.neglog > 1.301, "log2(FC) ≤ -1", 
                                    ifelse(K_volcano.data$log2FC > 1 & K_volcano.data$K_pvalue.BHcorr.neglog > 1.301, "log2(FC) ≥ 1", "-1 < log2(FC) < 1")))


K_volcanoEM <- ggplot(K_volcano.data, aes(x= log2FC, y=K_pvalue.BHcorr.neglog)) +  
  geom_point(aes(color=sig)) + 
  scale_color_manual(values = c("black", "red", "green","grey")) + 
  theme_bw(base_size = 12) +  
  theme(legend.position = "right", legend.title = element_blank()) + 
  geom_text_repel(data = subset(K_volcano.data, sig == "log2(FC) ≤ -1" | sig == "log2(FC) ≥ 1"), aes(label = rowname), size=5, box.padding = unit(0.35, "lines"), point.padding = unit(0.3, "lines")) +
  ggtitle("Figure 1.2 Volcano plot using mean fold change p-value of Student's t-test results") + labs(x=bquote(~log[2]~ "Fold change"), y=bquote(~-log[10]~adjusted-~italic(P))) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15, color = "black"))

plot(K_volcanoEM)
#### volcano plot ####

#### attach metabolite class ####
library(omu)
name_map <- read.csv("name_map.csv")
name_map <- name_map[-8, ]
name_map$KEGG

test_kegg <- cbind(volcano.data_dir[, c(1,2)], KEGG = name_map$KEGG)


test_kegg_class <- assign_hierarchy(test_kegg, keep_unknowns = TRUE, identifier = "KEGG") 
dim(test_kegg_class)


test_kegg_class$index[duplicated(test_kegg_class$index)]

test_kegg_class[test_kegg_class$index == 53, ]

assign_hierarchy(name_map, keep_unknowns = TRUE, identifier = "KEGG")
#### attach metabolite class ####



#### comparison fold change direction ####
volcano.data %>% 
  mutate(index = seq(1, 81, 1)) %>%
  select(index, everything()) -> volcano.data_dir

# medain case 
colnames(volcano.data_dir) <- c("index", "metabolite", "log2medianFC", "median FC", "-log10ad-p", "ad-p_kruskal", "sig_median")
volcano.data_dir <- cbind(volcano.data_dir, dir_median =  as.numeric(volcano.data_dir$log2medianFC > 0))

# mean case
colnames(volcano.data_dir) <- c("index", "metabolite", "log2meanFC", "mean FC", "Case mean", "Control mean", "-log10ad-p", "ad-p_kruskal", "sig_median")
volcano.data_dir <- cbind(volcano.data_dir, dir_median =  as.numeric(volcano.data_dir$log2meanFC > 0))


K_volcano.data %>% 
  mutate(index = seq(1, 81, 1)) %>%
  select(index, everything()) -> K_volcano.data_dir

colnames(K_volcano.data_dir) <- c("index", "metabolite", "log2meanFC", "mean FC", "Case mean", "Control mean", "-log10ad-p", "ad-p_student_t", "sig_mean")
K_volcano.data_dir <- cbind(K_volcano.data_dir, dir_mean =  as.numeric(K_volcano.data_dir$log2meanFC > 0))

volcano.data_dir %>% 
  merge(K_volcano.data_dir, by = "index") %>% 
  arrange(desc(log2meanFC.x)) -> dir_test

dir_test %>% 
  write.csv("direction_FC.csv")

kruskal.test <- lapply(all_metabolites, function(v) {
  kruskal.test(as.data.frame(raw_info_add_set_log)[, v] ~ as.data.frame(raw_info_add_set_log)[, 'Group'])
})

m <- c()
for(i in 1:81) {
  if(kruskal.test[[i]]$p.value < 0.05) {
    mm <- i
    m <- c(m, mm)
  }
}
# candidate metabolites after kruscal-wallis test 
sig_kruscal_metabo <- all_metabolites[m]
length(sig_kruscal_metabo)

# candidate metabolites after student's t test
length(Change_names(candidate_metabo))

# metabolites that have significance in all result
all_sig_result_metabolite <- c("...")
length(all_sig_result_metabolite)

# Remarkable metabolites using volcano plot
remark_fc_metabo <- volcano.data[which(volcano.data$sig == "log2(FC) ≥ 1" | volcano.data$sig == "log2(FC) ≤ -1"), ][, 1]
length(remark_fc_metabo)

all_sig_result_metabolite[all_sig_result_metabolite %in% remark_fc_metabo]

all_sig_result_metabolite 


all_sig_result_metabolite[all_sig_result_metabolite %in% Change_names(candidate_metabo)]

remark_fc_metabo[remark_fc_metabo %in% all_sig_result_metabolite]

#### comparison fold change direction ####

#### fold change ####

#### Lasso ####
library(glmnet)
library(RFmarkerDetector)

#### 1. baseline lasso, log transformation data case ####
obs <- model.matrix(Group~., raw_info_add_set_log[, -c(1,3,4,5,6,7)])[,-1]
obs <- autoscale(obs) # auto scaling : UV scaling 
obs <- paretoscale(obs) # pareto scaling 
group <- raw_info_add_set_log$Group

set.seed(1575)
train = sample(1:nrow(obs), nrow(obs)/2)
test = (-train)
ytest = group[test]

cv.lasso <- cv.glmnet(obs[train,], group[train], alpha=1, family = "binomial") # lasso logistic regression 
lasso.coef = predict(cv.lasso, type = "coefficients", s=cv.lasso$lambda.min) # coefficients
lasso.prediction = predict(cv.lasso, s=cv.lasso$lambda.min, newx = x[test,]) # coefficients


plot(cv.lasso) ## 1 
plot(cv.lasso$glmnet.fit, xvar="lambda", label=TRUE) ## 2
plot(cv.lasso$glmnet.fit, xvar="norm", label=TRUE) ## 3

# lambda가 아래인것들에서 선택하면 됨 두번째플랏에서!

cv.lasso$lambda
cv.lasso$lambda.1se

a = cv.lasso$lambda.min
b = cv.lasso$lambda.1se
c = coef(cv.lasso, s=cv.lasso$lambda.min)

length(which(c != 0 ))
c[which(c != 0 ), ] %>% 
  as.data.frame() %>% 
  write.xlsx("lasso_pareto.xlsx")

as.data.frame(c[which(c != 0 ), ]) %>% 
  rownames_to_column() %>% 
  .[, 1] %>% 
  .[-1] -> lasso_pareto_metabolite

lasso_auto <- as.data.frame(c[which(c != 0 ), ])
lasso_pareto <- as.data.frame(c[which(c != 0 ), ])

length(lasso_auto[, 1])
length(lasso_pareto[, 1])

as.data.frame(lasso_auto) %>% 
  write.xlsx("lasso_auto.xlsx")

as.data.frame(lasso_pareto) %>% 
  write.xlsx("lasso_pareto.xlsx")


# 계수 수동적으로 불러오는법.
# 0219, 반복에 따른 차이가 있는지 확인하기 
lambda_min1 = cv.lasso$lambda.min
small.lambda.index1 <- which(cv.lasso$lambda == cv.lasso$lambda.min)
small.lambda.betas1 <- cv.lasso$glmnet.fit$beta[, small.lambda.index]

lambda_min2 = cv.lasso$lambda.min
small.lambda.index2 <- which(cv.lasso$lambda == cv.lasso$lambda.min)
small.lambda.betas2 <- cv.lasso$glmnet.fit$beta[, small.lambda.index]

lambda_min3 = cv.lasso$lambda.min
small.lambda.index3 <- which(cv.lasso$lambda == cv.lasso$lambda.min)
small.lambda.betas3 <- cv.lasso$glmnet.fit$beta[, small.lambda.index]

small.lambda.betas1[which(small.lambda.betas1 !=0)]
small.lambda.betas2[which(small.lambda.betas2 !=0)]
small.lambda.betas3[which(small.lambda.betas3 !=0)]

length(small.lambda.betas1[which(small.lambda.betas1 !=0)])
length(small.lambda.betas2[which(small.lambda.betas2 !=0)])
length(small.lambda.betas3[which(small.lambda.betas3 !=0)])

small.lambda.betas[which(small.lambda.betas !=0)] # 44개, 위의 lasso_metabolite와 같음. 
length(small.lambda.betas[which(small.lambda.betas !=0)])
repeat_lasso <- function(x, y) { 
  
  a <- c()
  b <- c()
  c <- matrix(0, ncol(x), 1)
  
  for(i in 1:10) { 
    CVGLM <- cv.glmnet(x, y, 
                       nfolds = nrow(x), type.measure = "class", 
                       alpha = 1, # alpha : 1이어야 lasso
                       grouped = TRUE, family = "binomial")
    
    lambda_min = CVGLM$lambda.min
    small.lambda.index <- which(CVGLM$lambda == CVGLM$lambda.min)
    small.lambda.betas <- CVGLM$glmnet.fit$beta[, small.lambda.index]
    
    a <- c(a, lambda_min)
    b <- c(b, small.lambda.index)
    c <- cbind(c, as.matrix(small.lambda.betas))
    
  }
  result <- list(a,b,c)
  
  return(result)
}


test_pareto <- repeat_lasso(obs, group)

test_auto[[1]]
test_pareto[[1]]

test_auto[[2]]
test_pareto[[2]]

test_auto[[3]][, 2][test_auto[[3]][, 2] != 0]
test_pareto[[3]][, 2][test_pareto[[3]][, 2] != 0]

test_0220[[1]]
test_0220[[2]]
test_0220[[3]][, 2][test_0220[[3]][, 2] != 0]

# 각각 100번의 결과가 같은 것 확인
# 두 결과에서 선택된 대사체도 같은 것 확인 
# 0220, 혹시나 해본 결과도 같음.


#### 궁금해서 해보는 스케일링 후 결과의 range, normality test ####
## normality test 

# auto scaling
raw_info_add_set_log %>% 
  select(Group, all_metabolites) %>% 
  
  # autoscaling 
  autoscale(.) %>% 
  as.data.frame() %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  lapply(., shapiro.test) %>% 
  unlist() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  
  # 정규성 검정 결과
  dplyr::filter(grepl("p.value", rowname)) %>% 
  type_convert(cols(. = col_double())) %>% 
  dplyr::filter(.<0.05)

# pareto scaling
raw_info_add_set_log %>% 
  select(Group, all_metabolites) %>% 
  
  # paretoscaling 
  paretoscale(.) %>% 
  as.data.frame() %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  lapply(., shapiro.test) %>% 
  unlist() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  
  # 정규성 검정 결과
  dplyr::filter(grepl("p.value", rowname)) %>% 
  type_convert(cols(. = col_double())) %>% 
  dplyr::filter(.<0.05)

# Non-scaling 
raw_info_add_set_log %>% 
  select(Group, all_metabolites) %>% 
  dplyr::filter(Group == 1) %>% 
  select(all_metabolites) %>% 
  lapply(., shapiro.test) %>% 
  unlist() %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  
  # 정규성 검정 결과
  dplyr::filter(grepl("p.value", rowname)) %>% 
  type_convert(cols(. = col_double())) %>% 
  dplyr::filter(.<0.05)

# scaling 유무에 상관없이 세 결과가 같다. 왜지? 

#### scaling test ####
# auto scale과 pareto scale은 정규성에 영향을 미치지 못한다? 
scaling_test <- sample(x=1:1000,size=300)

hist(scaling_test)
hist(log(scaling_test))
hist(autoscale(log(scaling_test), F))
hist(paretoscale(as.data.frame(log(scaling_test)), F))


shapiro.test(log(scaling_test))
shapiro.test(autoscale(log(scaling_test), F))
shapiro.test(paretoscale(as.data.frame(log(scaling_test)), F))

shapiro.test(scaling_test)
shapiro.test(autoscale(scaling_test, F))
shapiro.test(paretoscale(as.data.frame(scaling_test), F))

# 유의한 건 log를 하고 안하고일때만임. 뭐지? 

#### Range ####

Range_after_autoscaling <- function(data) {
 
  #### Using all data with autoscaling  #### 
  data %>% 
    select(all_metabolites) %>% 
    
    # autoscaling 
    autoscale(., F) %>% 
    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table
  
  test_summary_table %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table
  
  #### Using filtered data by group = 1 with autoscaling  #### 
  data %>% 
    # autoscaling 
    autoscale(.) %>% 
    dplyr::filter(Group == 1) %>% 
    select(all_metabolites) %>% 
    
    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table_1
  
  test_summary_table_1 %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table_1
  
  #### Using filtered data by group = 0 with autoscaling  #### 
  data %>%
    # autoscaling 
    autoscale(.) %>% 
    dplyr::filter(Group == 0) %>% 
    select(all_metabolites) %>% 

    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table_0
  
  test_summary_table_0 %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table_0
  
  
  
  
  #### indexing for re-ordering ####
  a <- c()
  for( i in 1:length(all_metabolites)) {
    b <- which(tidy_summary_table$var %in% all_metabolites[i])
    a <- c(a, b)
  }
  
  result <- list(Overall = tidy_summary_table[a, ], 
                 Case = tidy_summary_table_1[a, ], 
                 Control = tidy_summary_table_0[a, ])
  
  #### result ####
  return(result)
}
Range_after_paretoscaling <- function(data) {
  
  #### Using all data with paretoscaling  #### 
  data %>% 
    select(all_metabolites) %>% 
    
    # paretotoscaling 
    paretoscale(., F) %>% 
    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table
  
  test_summary_table %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table
  
  #### Using filtered data by group = 1 with paretoscaling  #### 
  data %>% 
    # paretoscaling 
    paretoscale(.) %>% 
    dplyr::filter(Group == 1) %>% 
    select(all_metabolites) %>% 
    
    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table_1
  
  test_summary_table_1 %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table_1
  
  #### Using filtered data by group = 0 with paretoscaling  #### 
  data %>% 
    # paretoscaling 
    paretoscale(.) %>% 
    dplyr::filter(Group == 0) %>% 
    select(all_metabolites) %>% 
    
    as.data.frame() %>% 
    summarise_each(funs(aaaMin = min, 
                        aaaQ25 = quantile(., probs=0.25), 
                        aaaMedian = median, 
                        aaaQ75 = quantile(., probs=0.75), 
                        aaaMax = max,
                        aaaMean = mean, 
                        aaaSd = sd)) -> test_summary_table_0
  
  test_summary_table_0 %>% 
    gather(stat, val) %>% 
    separate(stat, into = c("var", "stat"), sep = "_aaa") %>% 
    spread(stat, val) %>% 
    select(var, Min, Q25, Median, Q75, Max, Mean, Sd) -> tidy_summary_table_0
  
  
  
  
  #### indexing for re-ordering ####
  a <- c()
  for( i in 1:length(all_metabolites)) {
    b <- which(tidy_summary_table$var %in% all_metabolites[i])
    a <- c(a, b)
  }
  
  result <- list(Overall = tidy_summary_table[a, ], 
                 Case = tidy_summary_table_1[a, ], 
                 Control = tidy_summary_table_0[a, ])
  
  #### result ####
  return(result)
}

do.call(rbind.data.frame, Range_after_autoscaling(raw_info_add_set_log)) %>% 
  rownames_to_column() %>% 
  mutate(rowname = gsub("\\.[^0-10]+", "", rowname)) %>% 
  write.csv("range_autoscaling.csv")

do.call(rbind.data.frame, Range_after_paretoscaling(raw_info_add_set_log)) %>% 
  rownames_to_column() %>% 
  mutate(rowname = gsub("\\.[^0-10]+", "", rowname)) %>% 
  write.csv("range_paretoscaling.csv")


#### 1. baseline lasso, log transformation data case ####


#### 2. log-ratio lasso ####
library(devtools)
install_github("stephenbates19/logratiolasso")

library(logratiolasso)

set.seed(10)
n <- 100 #number of observations
p <- 20 #number of features

x <- abs(matrix(rnorm(n*p), nrow = n)) #positive raw features
w <- log(x) #logarithmically transformed features
y <- w[, 1] - w[, 2] + rnorm(n) #response

centered_w <- scale(w, center = TRUE, scale = FALSE)
centered_y <- y - mean(y)


# 2-1 constrained Lasso 
x <- model.matrix(Group~., raw_info_add_set_log[, -c(1,3,4,5,6,7)])[,-1]
# x <- autoscale(x) # auto scaling : UV scaling 
x <- paretoscale(x) # pareto scaling 
y <- raw_info_add_set_log$Group


model_fit <- glmnet.constr(x, y, family = "binomial")
dim(model_fit$beta)

cv_model_fit <- cv.glmnet.constr(model_fit, x, y)
cv_model_fit$cvm #CV estimate of error
cv_model_fit$beta #best beta value
cv_model_fit$beta[which(cv_model_fit$beta != 0)]
length(cv_model_fit$beta[which(cv_model_fit$beta != 0)])

# 2-2 two stage log-lasso
# 2-2-1 fisrt stage
ts_model <- two_stage(x, y, k_max = 5, family = "binomial")

ts_model$betas[[10]]

cv_ts_model <- cv_two_stage(x, y, k_max = 5, family = "binomial")
cv_ts_model$lambda_min #index of best lambda
cv_ts_model$k_min #number of ratios

cv_ts_model$beta_min

# 2-2-2 second stage
cv_ts_model2 <- cv_two_stage(x, y, k_max = 5, second.stage = "yhat", family = "binomial")
cv_ts_model2$beta_min
all_metabolites[which(cv_ts_model2$beta_min != 0)]

# 2-3 Approximate forward stepwise selection
afs_model <- approximate_fs(x, y, k_max = 5)
afs_model$beta

afs_cv <- cv_approximate_fs(x, y, k_max = 5, n_folds = 10)
afs_cv$cvm
#### 2. log-ratio lasso ####

#### Plus- Lasso prediction test ####
library(glmnet)

x <- model.matrix(Group~.,  raw_info_add_set_log[, -c(1,3,4,5,6,7)])[,-1]
y <- raw_info_add_set_log$Group

set.seed(1575)
train = sample(1:nrow(x), nrow(x)/2)
test = (-train)
ytest = y[test]

cv.lasso_test <- cv.glmnet(x[train,], y[train], alpha=1, 
                      nfolds = nrow(obs), type.measure = "class", 
                      grouped = TRUE, family = "binomial") 


lasso.fit_test = predict(cv.lasso_test, type = "class", s=cv.lasso_test$lambda.min) # coefficients
lasso.prediction = predict(cv.lasso_test, type = "class", s=cv.lasso_test$lambda.min, newx = x[test,]) # coefficients

raw_info_add_set_log$Group
dim(lasso.prediction)

row.names(lasso.prediction)[1]

row.names(raw_info_add_set)
seq(1, 546, 1)

a <- c()
b <- matrix(0, 1, 2)

for( i in 1:length(lasso.prediction)) {
  if(which(row.names(lasso.prediction)[i] == row.names(raw_info_add_set_log)) != 0) {
    a <- c(lasso.prediction[i, 1], raw_info_add_set_log$Group[which(row.names(lasso.prediction)[i] == row.names(raw_info_add_set_log))])
    b <- rbind(b, a)
  }
}

sum(b[, 1] == b[, 2]) / nrow(b) 

#### Plus- Lasso prediction test ####





#### 3. Conditional logistic regression with lasso ####
test_classo <- clogitLasso(X = as.matrix(raw_info_add_set[, 8:88]), 
                           y = raw_info_add_set$Group, 
                           strata = raw_info_add_set$set)


length(test_classo$beta[100, ][which(test_classo$beta[100, ] != 0)])
length(test_classo$beta[90, ][which(test_classo$beta[90, ] != 0)])
length(test_classo$beta[75, ][which(test_classo$beta[75, ] != 0)])
length(test_classo$beta[50, ][which(test_classo$beta[50, ] != 0)])

plot(test_classo)


test_classo_log <- clogitLasso(X = as.matrix(raw_info_add_set_log[, 8:88]), 
                           y = raw_info_add_set$Group, 
                           strata = raw_info_add_set$set)

test_classo_log

plot(test_classo_log)
#### Conditional logistic regression with lasso ####

#### Lasso ####

#### Heatmap ####
library(gplots)
data(mtcars)
x  <- as.matrix(mtcars)
rc <- rainbow(nrow(x), start=0, end=.3)
cc <- rainbow(ncol(x), start=0, end=.3)

##
## demonstrate the effect of row and column dendrogram options
##
heatmap.2(x, key = T)
heatmap.2(x, key=TRUE , key.xlab="New value", key.ylab="New count", margins = c(10,10))
heatmap.2(x, margins = c(10,10), col = colorRampPalette(c('yellow','green','red'))(256), tracecol = FALSE, key = TRUE, keysize = 1.5, density.info="histogram") ## default - dendrogram plotted and reordering done.
aheatmap.2(x, dendrogram="none") ##  no dendrogram plotted, but reordering done.
heatmap.2(x, dendrogram="row")  ## row dendrogram plotted and row reordering done.
heatmap.2(x, dendrogram="col")  ## col dendrogram plotted and col reordering done.


t(raw_info_add_set[, -c(1,3:7)]) %>% 
  as.data.frame() %>% 
  rownames_to_column() -> omu_test_data

colnames(omu_test_data) <- c("Metabolite", paste("Sample", seq(1,546, 1)))
heatmap_test <- as.matrix(column_to_rownames(omu_test_data, var = "Metabolite"))


raw_info_add_set[, -c(1,3:7)] %>% 
  dplyr::arrange(Group) %>%
  select(-Group) %>% 
  t(.) %>% 
  as.data.frame() %>% 
  rownames_to_column() -> omu_test_data_arr

colnames(omu_test_data_arr) <- c("Metabolite", paste("Sample", seq(1,546, 1)))
heatmap_test_arr <- as.matrix(column_to_rownames(omu_test_data_arr, var = "Metabolite"))


  
# non-arrange version
heatmap.2(heatmap_test[1:10, ], trace = "none", col =  colorRampPalette(c("darkblue","white","darkred"))(100),
          margins=c(8,8)) #Colv=FALSE

# arrange version
heatmap.2(heatmap_test_arr[Change_names(candidate_metabo)[1:19], ], trace = "none", col =  colorRampPalette(c("darkblue","white","darkred"))(300),
          margins=c(8,8))

heatmap.2(heatmap_test_arr[Change_names(candidate_metabo)[20:38], ], trace = "none", col =  colorRampPalette(c("darkblue","white","darkred"))(300),
          margins=c(8,8))

heatmap.2(heatmap_test_arr[Change_names(special_metabo), ], trace = "none", col =  colorRampPalette(c("darkblue","white","darkred"))(300),
          margins=c(8,20), key=TRUE, cexCol=1, cexRow=0.7, density.info="none",lwid = c(5,15), lhei = c(3,15))

#### Example ####
# install step 
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("leukemiasEset")
library(leukemiasEset)

pvalues <- c()
for(i in 1:nrow(exprs(leukemiasEset))) { 
  R <- t.test(exprs(leukemiasEset)[i, leukemiasEset$LeukemiaType == "ALL"],
              exprs(leukemiasEset)[i, leukemiasEset$LeukemiaType == "CLL"], 
              var.equal = TRUE) 
  pvalues <- c(pvalues, R$p.value)
}
adjPval <- p.adjust(pvalues, method = "fdr")

difexp <- exprs(leukemiasEset)[c(which(adjPval < 0.01)),c(1:12, 25:36)]

heatmap.2(difexp,
          trace = "none",
          cexCol = 0.6,
          ColSideColors = as.character(as.numeric(factor(leukemiasEset$LeukemiaType[c(1:12, 25:36)]))),
          main = "Differentially expressed genes\nin ALL and CLL samples",
          cex.main = 1.5,
          key = TRUE,
          keysize = 1.5,
          col=bluered(256),
          density.info = "histogram")

#### Example ####
#### Heatmap ####

#### 02.06 ####
#### Metaboanalyst test ####
raw_info_add_set %>% 
  select(-c(3:7)) %>% 
  mutate(index = seq(1, 546, 1)) %>% 
  select(index, everything()) %>% 
  arrange(Group) -> metabo_test

cbind(Sample = c(paste0("Control_", seq(1,364, 1)), paste0("Case_", seq(1,182, 1))), metabo_test[, 1]) %>% 
  arrange(index) %>% 
  select(index, Sample) -> id

metabo_test <- cbind(Sample = c(paste0("Control_", seq(1,364, 1)), paste0("Case_", seq(1,182, 1))), metabo_test[, -1])
colnames(metabo_test)[3] <- "Label" 
metabo_test[, -2] %>% 
  write.csv("metabo_test.csv",row.names = F)

metabo_test[, -2] %>% 
  select(Sample, Label, remark_fc_metabo) %>% 
  write.csv("remark_fc_metabo.csv",row.names = F)

metabo_test[, -2] %>% 
  select(Sample, Label, all_sig_result_metabolite) %>% 
  write.csv("all_sig_result_metabolite.csv",row.names = F)

metabo_test[, -2] %>% 
  select(Sample, Label, remark_fc_metabo[remark_fc_metabo %in% all_sig_result_metabolite]) %>% 
  write.csv("remark_inter_all_sig.csv",row.names = F)
#### Metaboanalyst test ####
#### 02.06 ####


#### 02.09 ####
#### PCA ####
# prcomp
install.packages("ggfortify")
library(ggfortify)

raw_info_add_set_log[, c(8:88)] %>% 
  mutate(Group = as.factor(rep(c("Case", "Control", "Control"), 182))) %>% 
  # select(Group, everything()) %>% 
  autoplot(prcomp(.[, 1:81], center = T, scale. = T), 
           data = ., colour = "Group", frame = T, frame.type = "norm") + 
  theme_bw() + 
  ggtitle("Figure 1. PCA plot with all metabolites") + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  scale_color_discrete(name = "Group")



# pcaMethods
BiocManager::install("pcaMethods")
library(pcaMethods)
test_pca_n <- pca(prep(raw_info_add_set_log[, c(8:88)], scale = "none", center=T), method="svd", nPcs=7, cv="q2")
test_pca_p <- pca(prep(raw_info_add_set_log[, c(8:88)], scale = "pareto", center=T), method="svd", nPcs=7, cv="q2")
test_pca_v <- pca(prep(raw_info_add_set_log[, c(8:88)], scale = "vector", center=T), method="svd", nPcs=7, cv="q2")
test_pca_u <- pca(prep(raw_info_add_set_log[, c(8:88)], scale = "uv", center=T), method="svd", nPcs=7, cv="q2")

test_pca_n
test_pca_p
test_pca_v
test_pca_u

plotPcs(test_pca_n)

test_pca_n@cvstat
test_pca_p@cvstat
test_pca_v@cvstat
test_pca_u@cvstat

# opls
library(ropls)
PCA_opls <- opls(raw_info_add_set_log[, c(8:88)])
PCA_opls
  
  
#### PCA ####

#### PLS-DA ####
library(mixOmics)

Y <- as.factor(rep(c("Case", "Control", "Control"), 182))
plsda.test <- plsda(X = raw_info_add_set_log[, c(8:88)], Y, ncomp = 2)
plotIndiv(plsda.test, ind.names = FALSE, 
          ellipse = TRUE, legend = TRUE, title = "Figure1. test", 
          col.per.group = c("orangered2", "green3"),
          pch = 20, # point 모양
          X.label = "Component 1 (19%)", Y.label = "Component 2 (11%)", legend.title = "Group") 

test.vip <- vip(plsda.test)
barplot(test.vip[, 1][which(test.vip[, 1] > 1)])

#### PLS-DA ####
#### 02.09 ####


#### 02.10 metabolites list up #### 

#### 1. Kruskal-Wallis test ####
kruskal.metabolite <- c()

for(i in 1:81) {
  if(kruskal.test[[i]]$p.value < 0.05) {
    kruskal.metabolite <- c(kruskal.metabolite, all_metabolites[i])
  }
}

as.data.frame(kruskal.metabolite)[, 1]
#### 1. Kruskal-Wallis test ####

#### 2. Fold-change ####
volcano.data %>% 
  dplyr::filter(pvalue.BHcorr < 0.05) %>% 
  dplyr::select(rowname) -> median_FC.metabolite

median_FC.metabolite[ ,1]

as.data.frame(kruskal.metabolite)[, 1] %in% median_FC.metabolite[ ,1] # complete overlap 
#### 2. Fold-change ####

#### 3. continous CLR with log scale ####
#### multiple ####
log_mid_high_CLR_conti[,'p-value'] <- as.numeric(as.character(log_mid_high_CLR_conti[,'p-value']))

log_mid_high_CLR_conti[, 1:6] %>% 
  # as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  dplyr::filter(`p-value` < 0.05) %>% 
  dplyr::select(Metabolite) -> multi_CLR_conti # 55개 

#### simple ####
log_mid_high_CLR_conti[, 7:16] %>% 
  type_convert(cols(NO = col_double())) %>% 
  # as.data.frame() %>% 
  dplyr::filter(`p_value` < 0.05) %>% 
  dplyr::select(Metabolites) -> simple_CLR_conti # 55개 

#### result ####
multi_CLR_conti[, 1] %in% simple_CLR_conti[, 1] # 하나 빼고 겹침 
sum(multi_CLR_conti[, 1] %in% simple_CLR_conti[, 1]) # 54개 

as.character(multi_CLR_conti[, 1]) %in% simple_CLR_conti[, 1]
simple_CLR_conti[, 1] %in% as.character(multi_CLR_conti[, 1])

as.character(multi_CLR_conti[, 1])[6] # simple에만 유의함 
simple_CLR_conti[, 1][38] # multiple에만 유의함 


#### 3. continous CLR with log scale ####



#### 4. categorical CLR with log scale ####
#### multiple ####
log_mid_high_CLR[,'p-value'] <- as.numeric(as.character(log_mid_high_CLR[,'p-value']))

log_mid_high_CLR[, 1:6] %>% 
  # as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  dplyr::filter(`p-value` < 0.05) %>% 
  dplyr::select(Metabolites) -> multi_CLR_cate # 개수만 101개 

#### simple #### 
log_mid_high_CLR[, 7:16] %>% 
  type_convert(cols(NO = col_double())) %>% 
  # as.data.frame() %>% 
  dplyr::filter(`p_value` < 0.05) %>% 
  dplyr::select(Metabolites) -> simple_CLR_cate_1 # 개수만 100개 

log_mid_high_CLR[, c(1, 7:16)] %>% 
  type_convert(cols(NO = col_double())) %>% 
  # as.data.frame() %>% 
  dplyr::filter(`p_value` < 0.05) %>% 
  dplyr::select(Metabolites) -> simple_CLR_cate_2 # 개수만 100개 

#### result ####
length(unique(multi_CLR_cate[, 1])) # multiple에서 최소 한 개라도 유의한 metabolite는 56개 
length(unique(simple_CLR_cate_2[, 1])) # simple에서 최소 한 개라도 유의한 metabolite는 58개 

length(multi_CLR_cate[, 1][duplicated(multi_CLR_cate)]) # multiple에서 mid, high 모두 sig한 metabolite 45개 
length(simple_CLR_cate_2[, 1][duplicated(simple_CLR_cate_2)]) # simple에서 mid, high 모두 sig한 metabolite 42개 

# mutiple에서 둘 중 하나만 sig한 metabolite는 11개 
multi_CLR_cate[-which( duplicated(multi_CLR_cate)|duplicated(multi_CLR_cate, fromLast=T) ), ]
# high, high, high, high, high, high, high, high, high, high, high
# 모두 high에서만 유의함. 따라서 high에서만 유의한 metabolite 총 11개 

# simple에서 둘 중 하나만 sig한 metabolite는 16개 
simple_CLR_cate_2[-which( duplicated(simple_CLR_cate_2)|duplicated(simple_CLR_cate_2, fromLast=T) ), ]

# 2개는 mid에만, 14개는 high에서만 significant
simple_CLR_cate_1[-which( duplicated(simple_CLR_cate_2)|duplicated(simple_CLR_cate_2, fromLast=T) ), ]


#### 4. categorical CLR with log scale ####

#### 5. Pathway analysis ####
# 순서대로 Arginine biosynthesis, Alanine, aspartate and glutamate metabolism, 
# Glycine, serine and threonine metabolism, Arginine and proline metabolism, 
# Cysteine and methionine metabolism, Nicotinate and nicotinamide metabolism

Change_names(c("L-Glutamate", "L-Arginine",	"L-Citrulline",	"L-Aspartate",	"L-Glutamine",	"Urea", "Fumarate"))
Change_names(c("N-Acetyl-L-aspartate",	"L-Aspartate", "L-Asparagine"	,"L-Alanine" , "L-Glutamate", "4-Aminobutanoate", "L-Glutamine", "Fumarate"	, "Succinate"))
Change_names(c("L-Serine", "Choline"	, "Betaine"	, "Dimethylglycine"	, "L-Cystathionine"	, "Glycine", "L-Threonine"	, "Creatine", "L-Cysteine"))
Change_names(c("L-Arginine", "Creatine", "4-Aminobutanoate", "S_Adenosylmethionine"	, "Hydroxyproline", "L-Proline", "L-Glutamate"))
Change_names(c("S_Adenosylmethionine", "L-Cystathionine", "L-Serine", "L-Methionine", "S_Adenosylhomocysteine", "L-Cysteine"))
Change_names(c("L-Aspartate", "NAD", "Nicotinamide", "Nicotinate"))
            
path_metabolite <- unique(c(Change_names(c("L-Glutamate", "L-Arginine",	"L-Citrulline",	"L-Aspartate",	"L-Glutamine",	"Urea", "Fumarate"))
                            , Change_names(c("N-Acetyl-L-aspartate",	"L-Aspartate", "L-Asparagine"	,"L-Alanine" , "L-Glutamate", "4-Aminobutanoate", "L-Glutamine", "Fumarate"	, "Succinate"))
                            , Change_names(c("L-Serine", "Choline"	, "Betaine"	, "Dimethylglycine"	, "L-Cystathionine"	, "Glycine", "L-Threonine"	, "Creatine", "L-Cysteine"))
                            , Change_names(c("L-Arginine", "Creatine", "4-Aminobutanoate", "S_Adenosylmethionine"	, "Hydroxyproline", "L-Proline", "L-Glutamate"))
                            , Change_names(c("S_Adenosylmethionine", "L-Cystathionine", "L-Serine", "L-Methionine", "S_Adenosylhomocysteine", "L-Cysteine"))
                            , Change_names(c("L-Aspartate", "NAD", "Nicotinamide", "Nicotinate"))))

path_metabolite

#### 5. Pathway analysis ####

#### 6. final intersection ####
install.packages("VennDiagram")
library(VennDiagram)

median_FC.metabolite[ ,1]

multi_CLR_conti
simple_CLR_conti

unique(multi_CLR_cate[, 1])
unique(simple_CLR_cate_2[, 1])

path_metabolite

all_metabolites[ which( all_metabolites %in% median_FC.metabolite[ ,1] ) ] 

# Target
median_FC.metabolite[ ,1]
unique(multi_CLR_cate[, 1])
path_metabolite
rownames(as.data.frame(auto_small.lambda.betas[auto_small.lambda.betas != 0]))

sum(all_metabolites %in% median_FC.metabolite[ ,1])
sum(all_metabolites %in% unique(multi_CLR_cate[, 1]))
sum(all_metabolites %in% path_metabolite)
sum(all_metabolites %in% rownames(as.data.frame(auto_small.lambda.betas[auto_small.lambda.betas != 0])))

as.matrix(all_metabolites %in% median_FC.metabolite[ ,1])
as.matrix(all_metabolites %in% unique(multi_CLR_cate[, 1]))
as.matrix(all_metabolites %in% path_metabolite)
as.matrix(all_metabolites %in% rownames(as.data.frame(auto_small.lambda.betas[auto_small.lambda.betas != 0])))

venn_test <- as.data.frame(cbind(all_metabolites %in% median_FC.metabolite[ ,1], 
                                 all_metabolites %in% unique(multi_CLR_cate[, 1]), 
                                 all_metabolites %in% path_metabolite, 
                                 all_metabolites %in% rownames(as.data.frame(auto_small.lambda.betas[auto_small.lambda.betas != 0]))))

row.names(venn_test) <- all_metabolites
colnames(venn_test) <- c("FC", "CLR", "path", "LASSO")
venn_test

venn.diagram(
  x = list(
    FC = which(venn_test$FC==TRUE),   # A 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    CLR = which(venn_test$CLR==TRUE),   # B 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    path = which(venn_test$path==TRUE),   # C 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    LASSO = which(venn_test$LASSO==TRUE)    # D 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
  ),
  filename = "Venn_Diagram_4set.tiff",
  col = "black",   # 벤 다이어그램 테두리 색상을 설정합니다.
  lty = "dotted",   # 벤 다이어그램 테두리 선 모양을 설정합니다.
  fill = c("dodgerblue", "goldenrod1", "darkorange1", "seagreen3"),   # 각 벤 다이어그램 내부 색상을 설정합니다.
  alpha = 0.50,   # 벤 다이어그램의 알파 투명도를 설정합니다.
  cat.col = c("dodgerblue", "goldenrod1", "darkorange1", "seagreen3"),   # 각 벤 다이어그램의 명칭에 대한 색상을 설정합니다.
  cat.cex = 1.5,   # 각 벤 다이어그램의 명칭에 대한 글자 크기를 설정합니다.
  cat.fontface = "bold",   # 각 벤 다이어그램의 명칭에 대한 글자를 볼드체로 설정합니다.
  margin = 0.05   #  벤 다이어그램 주위의 공간을 설정합니다.
)

first <- intersect(all_metabolites, median_FC.metabolite[ ,1])
second <- intersect(first, multi_CLR_conti[ ,1])
third <- intersect(second, unique(multi_CLR_cate[, 1]))
forth <- intersect(third, unique(simple_CLR_cate_2[, 1]))

fifth <- intersect(forth, simple_CLR_conti[, 1])
sixth <- intersect(fifth, path_metabolite)

fifth
sixth

#### 6. final intersection ####

#### 7. list with pathway ####
metabolites_table <- read.xlsx2(paste(dir, "metabolites_listup.xlsx", sep= "/"), sheetIndex = 1, stringsAsFactors=FALSE)

pathway_result <- read.xlsx2(paste(dir, "pathway_results.xlsx", sep= "/"), sheetIndex = 1, stringsAsFactors=FALSE)

colnames(metabolites_table) <- metabolites_table[2, ]
metabolites_table <- metabolites_table[-c(1:2), -c(3:5)]

metabolites_table %>% 
  type_convert(cols(Impact = col_double())) -> metabolites_table

test_name <- metabolites_table[, 3]
test_name <- test_name[-c(43:50)]

test_name <- gsub(";", ",", test_name)
test_name <- gsub("*\n*", "", test_name)
test_name <- gsub(" ", "", test_name)

test_name <- strsplit(test_name, ",")

test_name[[4]] <- test_name[[4]][-4]
test_name[[11]] <- c("Glutathione disulfide", "Glycine","L-Glutamate","L-Cysteine", "5-Oxoproline")
test_name[[2]] <- c("L-Glutamate",  "L-Arginine",   "L-Citrulline", "L-Aspartate",  "L-Glutamine", "Urea", "Fumarate")
test_name[[3]] <- c("N-Acetyl-L-aspartate", "L-Aspartate",          "L-Asparagine", "L-Alanine", "L-Glutamate",
                    "L-Glutamine", "4-Aminobutanoate", "Fumarate", "Succinate")
test_name[[4]] <- c("L-Serine", "Choline", "Betaine", "N-Dimethylglycine", "L-Cystathionine", "Glycine",
                    "L-Threonine", "Creatine", "L-Cysteine")
test_name[[8]] <- c("L-Arginine", "Creatine", "4-Aminobutanoate", "S-Adenosyl-L-methionine",
                    "Hydroxyproline", "L-Proline", "L-Glutamate")

#### Check step ####
m <- c()
for(i in 1:42) {
  m1 <- length(test_name[[i]])
  m <- c(m, m1)
}

which(m != pathway_result$Hits)
sum(m == pathway_result$Hits) == 42

#### Commit Involved metabolite ####
# imfact와 FDR을 이용한 metabolites list 
involve_metabolite <- test_name # invovled metabolites로 commit


#### Big problem ####
Change_names(involve_metabolite[[1]])[which(Change_names(involve_metabolite[[1]]) %in% median_FC.metabolite[, 1])]

# pathway analysis에서는 L-Aspartate로 나옴. 
# 지금까지의 metabolite name vector에서는 L_Aspartic_acid로 썼음. 
median_FC.metabolite[, 1] == "L_Aspartic_acid"
involve_metabolite[[1]] == "L-Aspartate"

# 겹치는 패턴을 찾아내서 FC와 CLR에 추가하는 게 나을 것 같은데? 
# 가령 -tate == acid 
median_FC.metabolite[, 1]
median_FC.metabolite[, 1][which(grepl(pattern = "_acid$", x = median_FC.metabolite[, 1]))]

#### Solve the problem : all_metabolites를 기준으로 뭐가 다른지 먼저 파악하기 
Change_names(involve_metabolite[[1]]) %in% all_metabolites # 20개 중 2개 불일치
length(involve_metabolite[[1]])

Change_names(involve_metabolite[[1]])[-which(Change_names(involve_metabolite[[1]]) %in% all_metabolites)] # L_Aspartate, L-Glutamate

all_metabolites == "L_Glutamic_acid"

# 그럼 다른 이름을 갖는 metabolites들만 먼저 빼내보자. 
filtering_double_name <- function(list_of_matabolites) {
  
  Change_names <- function(list){
    list <- gsub("^ | $", "", list)
    list <- gsub(" ", "_", list)
    list <- gsub("-", "_", list)
    
    return(list)
  }
  
  result_list1 <- list()
  result_list2 <- list()
  result_vector <- c()
  
  for(i in 1:length(list_of_matabolites)) {
    logical_position <- Change_names(list_of_matabolites[[i]]) %in% all_metabolites
    
    total_match <- sum(logical_position)
    total_non_match <- length(list_of_matabolites[[i]]) - sum(logical_position)
    
    non_matched_name <- Change_names(list_of_matabolites[[i]])[which(!(logical_position))]
    matched_name <- Change_names(list_of_matabolites[[i]])[which(logical_position)]
    
    total_result <- c(total_match, total_non_match, total_match + total_non_match)
    result_vector <- rbind(result_vector, total_result)
  
    result_list1[[i]] <- matched_name
    result_list2[[i]] <- non_matched_name
  }
  
  row.names(result_vector) <- seq(1, length(list_of_matabolites), 1)
  colnames(result_vector) <- c("mathed", "non-matched", "total")
  result_vector <- as.data.frame(result_vector)
  
  
  return_list <- list(result_vector, result_list1, result_list2)
  names(return_list) <- c("# of", "matched_name", "non_matched_name")
  return(return_list)
}


involve_metabolite[[42]][which(!(Change_names(involve_metabolite[[42]]) %in% all_metabolites))]

# function test 
f_test <- filtering_double_name(involve_metabolite)

# Hits의 개수가 모두 일치하는 것 확인
f_test[[1]][, 3] == pathway_result$Hits
sum(f_test[[1]][, 3] == pathway_result$Hits)

# involved의 개수가 1이면, 즉 Hit가 1이면 무조건 mathced인데 아닌 경우가 있다. 
# 이름이 다른 거겠지..............
f_test[["non_matched_name"]]
f_test[["matched_name"]]
f_test[["# of"]]

# filtering_double_name 함수 내에서 all_metabolite를 이용했기 때문에 non_matched_name list는 null이 되어야 맞다. 
# 즉, non_matched_name list에 있는 모든 이름들은 내가 사용한 이름들과 다른 것들이다. 
unique(unlist(f_test[["non_matched_name"]])) # 다른 이름은 전체 26개.

#### 이제 위의 이름들을 내가 사용한 타입의 이름들로 바꿔주자. ####
double_name <- list()

# 1st pathway에서 다른 이름의 개수 : 2개 
Change_names(involve_metabolite[[1]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[1]])[which(Change_names(involve_metabolite[[1]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[1]])[which(Change_names(involve_metabolite[[1]]) %in% all_metabolites)]
double_name[[1]] <- c("L_Aspartic_acid", "L_Glutamic_acid",
                      Change_names(involve_metabolite[[1]])[which(Change_names(involve_metabolite[[1]]) %in% all_metabolites)])
sum(double_name[[1]] %in% all_metabolites) == length(double_name[[1]])

# 2nd pathway에서 다른 이름의 개수 : 4개 
Change_names(involve_metabolite[[2]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[2]])[which(Change_names(involve_metabolite[[2]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[2]])[which(Change_names(involve_metabolite[[2]]) %in% all_metabolites)]
double_name[[2]] <- c("L_Aspartic_acid", "L_Glutamic_acid", "Citrulline", "Fumaric_acid",
                      Change_names(involve_metabolite[[2]])[which(Change_names(involve_metabolite[[2]]) %in% all_metabolites)])
sum(double_name[[2]] %in% all_metabolites) == length(double_name[[2]])

# 3nd pathway에서 다른 이름의 개수 : 7개 
Change_names(involve_metabolite[[3]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[3]])[which(Change_names(involve_metabolite[[3]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[3]])[which(Change_names(involve_metabolite[[3]]) %in% all_metabolites)]
double_name[[3]] <- c("N_Acetyl_L_Aspartic_acid", "L_Aspartic_acid", 
                      "L_Glutamic_acid", "Gamma_Aminobutyric_acid", "Fumaric_acid", "Succinic_acid",
                      Change_names(involve_metabolite[[3]])[which(Change_names(involve_metabolite[[3]]) %in% all_metabolites)])
sum(double_name[[3]] %in% all_metabolites) == length(double_name[[3]])

# 4th pathway에서 다른 이름의 개수 : 1개 
Change_names(involve_metabolite[[4]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[4]])[which(Change_names(involve_metabolite[[4]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[4]])[which(Change_names(involve_metabolite[[4]]) %in% all_metabolites)]
double_name[[4]] <- c("Dimethylglycine",
                      Change_names(involve_metabolite[[4]])[which(Change_names(involve_metabolite[[4]]) %in% all_metabolites)])
sum(double_name[[4]] %in% all_metabolites) == length(double_name[[4]])

# 5th pathway에서 다른 이름의 개수 : 2개 
Change_names(involve_metabolite[[5]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[5]])[which(Change_names(involve_metabolite[[5]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[5]])[which(Change_names(involve_metabolite[[5]]) %in% all_metabolites)]
double_name[[5]] <- c("Adenosine_monophosphate", "Uric_acid",
                      Change_names(involve_metabolite[[5]])[which(Change_names(involve_metabolite[[5]]) %in% all_metabolites)])
sum(double_name[[5]] %in% all_metabolites) == length(double_name[[5]])

# 6th pathway에서 다른 이름의 개수 : 0개 
Change_names(involve_metabolite[[6]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[6]])[which(Change_names(involve_metabolite[[6]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[6]])[which(Change_names(involve_metabolite[[6]]) %in% all_metabolites)]
double_name[[6]] <- c(
                      Change_names(involve_metabolite[[6]])[which(Change_names(involve_metabolite[[6]]) %in% all_metabolites)])
sum(double_name[[6]] %in% all_metabolites) == length(double_name[[6]])

# 7th pathway에서 다른 이름의 개수 : 5개 
Change_names(involve_metabolite[[7]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[7]])[which(Change_names(involve_metabolite[[7]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[7]])[which(Change_names(involve_metabolite[[7]]) %in% all_metabolites)]
double_name[[7]] <- c("beta_Hydroxybutyric_acid", "Acetoacetic_acid", "Gamma_Aminobutyric_acid",
                      "L_Glutamic_acid", "Succinic_acid",
                      Change_names(involve_metabolite[[7]])[which(Change_names(involve_metabolite[[7]]) %in% all_metabolites)])
sum(double_name[[7]] %in% all_metabolites) == length(double_name[[7]])

# 8th pathway에서 다른 이름의 개수 : 4개 
Change_names(involve_metabolite[[8]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[8]])[which(Change_names(involve_metabolite[[8]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[8]])[which(Change_names(involve_metabolite[[8]]) %in% all_metabolites)]
double_name[[8]] <- c("Gamma_Aminobutyric_acid", "S_Adenosylmethionine", "Hydroxy_L_proline",
                      "L_Glutamic_acid",
                      Change_names(involve_metabolite[[8]])[which(Change_names(involve_metabolite[[8]]) %in% all_metabolites)])
sum(double_name[[8]] %in% all_metabolites) == length(double_name[[8]])

# 9th pathway에서 다른 이름의 개수 : 2개 
Change_names(involve_metabolite[[9]]) %in% unique(unlist(f_test[["non_matched_name"]]))

# 그 이름의 형태
Change_names(involve_metabolite[[9]])[which(Change_names(involve_metabolite[[9]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
Change_names(involve_metabolite[[9]])[which(Change_names(involve_metabolite[[9]]) %in% all_metabolites)]
double_name[[9]] <- c("S_Adenosylmethionine", "S_Adenosylhomocysteine",
                      Change_names(involve_metabolite[[9]])[which(Change_names(involve_metabolite[[9]]) %in% all_metabolites)])
sum(double_name[[9]] %in% all_metabolites) == length(double_name[[9]])

name_check <- function(list_of_metabolites) {
  
  result <- list()
  
  for(i in 1: length(list_of_metabolites)) {
    a <- sum(Change_names(list_of_metabolites[[i]]) %in% unique(unlist(f_test[["non_matched_name"]])))
    
    b <- Change_names(list_of_metabolites[[i]])[which(Change_names(list_of_metabolites[[i]]) %in% unique(unlist(f_test[["non_matched_name"]])))]
    c <- Change_names(list_of_metabolites[[i]])[which(Change_names(list_of_metabolites[[i]]) %in% all_metabolites)]
    
    d <- list(a, b, c)
    names(d) <- c("# of nonmatched", "nonmatched", "matched")
    
    result[[i]] <- d
  }
  return(result)
  
}
matched_name <- function(list_of_metabolites) {
  r <- list()
  for( i in 1:length(list_of_metabolites)) {
    r[[i]] <- Change_names(list_of_metabolites[[i]])[which(Change_names(list_of_metabolites[[i]]) %in% all_metabolites)]
  }
  
  return(r)
}

name_check_result <- name_check(involve_metabolite)
matched_name <- matched_name(involve_metabolite)


# 10th : 4
name_check_result[[10]]
double_name[[10]] <- c("L_Aspartic_acid", "NAD", "Niacinamide", "Nicotinic_acid", matched_name[[10]])
sum(double_name[[10]] %in% all_metabolites) == length(double_name[[10]])

# 11th : 3
name_check_result[[11]]
double_name[[11]] <- c("L_Glutamic_acid", "Pyroglutamic_acid", "Oxidized_glutathione", matched_name[[11]])
sum(double_name[[11]] %in% all_metabolites) == length(double_name[[11]])

# 12th : 1
name_check_result[[12]]
double_name[[12]] <- c("Hippuric_acid", matched_name[[12]])
sum(double_name[[12]] %in% all_metabolites) == length(double_name[[12]])

# 13th : 1
name_check_result[[13]]
double_name[[13]] <- c("L_Aspartic_acid", matched_name[[13]])
sum(double_name[[13]] %in% all_metabolites) == length(double_name[[13]])

# 14th : none
name_check_result[[14]]
double_name[[14]] <- c(matched_name[[14]])
sum(double_name[[14]] %in% all_metabolites) == length(double_name[[14]])

# 15th : 2
name_check_result[[15]]
double_name[[15]] <- c("beta_Hydroxybutyric_acid", "Acetoacetic_acid",  matched_name[[15]])
sum(double_name[[15]] %in% all_metabolites) == length(double_name[[15]])

# 16th : 1
name_check_result[[16]]
double_name[[16]] <- c("L_Glutamic_acid", matched_name[[16]])
sum(double_name[[16]] %in% all_metabolites) == length(double_name[[16]])

# 17th : 1
name_check_result[[17]]
double_name[[17]] <- c("L_Glutamic_acid", matched_name[[17]])
sum(double_name[[17]] %in% all_metabolites) == length(double_name[[17]])

# 18th : 1
name_check_result[[18]]
double_name[[18]] <- c("L_Glutamic_acid", "L_Aspartic_acid", matched_name[[18]])
sum(double_name[[18]] %in% all_metabolites) == length(double_name[[18]])

# 19th : none
name_check_result[[19]]
double_name[[19]] <- c(matched_name[[19]])
sum(double_name[[19]] %in% all_metabolites) == length(double_name[[19]])

# 20th : 1
name_check_result[[20]]
double_name[[20]] <- c("L_Glutamic_acid", matched_name[[20]])
sum(double_name[[20]] %in% all_metabolites) == length(double_name[[20]])

# 21th : none
name_check_result[[21]]
double_name[[21]] <- c(matched_name[[21]])
sum(double_name[[21]] %in% all_metabolites) == length(double_name[[21]])

# 22th : 1
name_check_result[[22]]
double_name[[22]] <- c("L_Aspartic_acid", matched_name[[22]])
sum(double_name[[22]] %in% all_metabolites) == length(double_name[[22]])

# 23th : none
name_check_result[[23]]
double_name[[23]] <- c(matched_name[[23]])
sum(double_name[[23]] %in% all_metabolites) == length(double_name[[23]])

# 24th : 1
name_check_result[[24]]
double_name[[24]] <- c("Acetoacetic_acid", matched_name[[24]])
sum(double_name[[24]] %in% all_metabolites) == length(double_name[[24]])

# 25th : 3
name_check_result[[25]]
double_name[[25]] <- c("Acetoacetic_acid", "Fumaric_acid", "Norepinephrine", matched_name[[25]])
sum(double_name[[25]] %in% all_metabolites) == length(double_name[[25]])

# 26th : none
name_check_result[[26]]
double_name[[26]] <- c(matched_name[[26]])
sum(double_name[[26]] %in% all_metabolites) == length(double_name[[26]])

# 27th : 2
name_check_result[[27]]
double_name[[27]] <- c("Fumaric_acid", "Succinic_acid", matched_name[[27]])
sum(double_name[[27]] %in% all_metabolites) == length(double_name[[27]])

# 28th : 1
name_check_result[[28]]
double_name[[28]] <- c("Glycerophosphocholine", matched_name[[28]])
sum(double_name[[28]] %in% all_metabolites) == length(double_name[[28]])

# 29th : 2
name_check_result[[29]]
double_name[[29]] <- c("Lactate", "Fumaric_acid", matched_name[[29]])
sum(double_name[[29]] %in% all_metabolites) == length(double_name[[29]])

# 30th : none
name_check_result[[30]]
double_name[[30]] <- c(matched_name[[30]])
sum(double_name[[30]] %in% all_metabolites) == length(double_name[[30]])

# 31th : none
name_check_result[[31]]
double_name[[31]] <- c(matched_name[[31]])
sum(double_name[[31]] %in% all_metabolites) == length(double_name[[31]])

# 32th : 1
name_check_result[[32]]
double_name[[32]] <- c("Methyl_folate", matched_name[[32]])
sum(double_name[[32]] %in% all_metabolites) == length(double_name[[32]])

# 33th : 1
name_check_result[[33]]
double_name[[33]] <- c("Glycocholic_acid", matched_name[[33]])
sum(double_name[[33]] %in% all_metabolites) == length(double_name[[33]])

# 34th : none
name_check_result[[34]]
double_name[[34]] <- c(matched_name[[34]])
sum(double_name[[34]] %in% all_metabolites) == length(double_name[[34]])

# 35th : 1
name_check_result[[35]]
double_name[[35]] <- c("L_Glutamic_acid", matched_name[[35]])
sum(double_name[[35]] %in% all_metabolites) == length(double_name[[35]])

# 36th : none
name_check_result[[36]]
double_name[[36]] <- c(matched_name[[36]])
sum(double_name[[36]] %in% all_metabolites) == length(double_name[[36]])

# 37th : none
name_check_result[[37]]
double_name[[37]] <- c(matched_name[[37]])
sum(double_name[[37]] %in% all_metabolites) == length(double_name[[37]])

# 38th : 1
name_check_result[[38]]
double_name[[38]] <- c("Glycerophosphocholine", matched_name[[38]])
sum(double_name[[38]] %in% all_metabolites) == length(double_name[[38]])

# 39th : none
name_check_result[[39]]
double_name[[39]] <- c(matched_name[[39]])
sum(double_name[[39]] %in% all_metabolites) == length(double_name[[39]])

# 40th : 1
name_check_result[[40]]
double_name[[40]] <- c("Succinic_acid", matched_name[[40]])
sum(double_name[[40]] %in% all_metabolites) == length(double_name[[40]])

# 41th : none
name_check_result[[41]]
double_name[[41]] <- c(matched_name[[41]])
sum(double_name[[41]] %in% all_metabolites) == length(double_name[[41]])

# 42th : none
name_check_result[[42]]
double_name[[42]] <- c("Lactate", matched_name[[42]])
sum(double_name[[42]] %in% all_metabolites) == length(double_name[[42]])
#### 이제 위의 이름들을 내가 사용한 타입의 이름들로 바꿔주자. ####

# 기존의 criteria였던 impact를 제외하고 FDR만 사용해서 pathway_metabolite 다시 선언 
path_metabolite <- unique(unlist(double_name[1 : 10]))


#### overlap check ####

vector <- c()
result <- c()

i <- 1
for(i in 1:length(double_name)) {
  
  a <- median_FC.metabolite[, 1][which(median_FC.metabolite[, 1] %in% double_name[[i]])]
  b <- unique(multi_CLR_cate[, 1])[which(unique(multi_CLR_cate[, 1]) %in% double_name[[i]])]
  c <- a[which(a %in% b)]
  n <- c(setdiff(a, b), setdiff(b, a))
  
  
  
  d <- length(a)
  e <- length(b)
  f <- length(c)
  m <- length(n)
  
  g <- paste(a, collapse = ", ")
  h <- paste(b, collapse = ", ")
  i <- paste(c, collapse = ", ")
  l <- paste(n, collapse = ", ")
  
  vector <- c(m, l, f, i, d, g, e, h)
  
  result <- rbind(result, vector)
  result <- as.data.frame(result)
  colnames(result) <- c("# of complement", "complement", "# of intersection", "intersection", "# of FC", "FC", "# of CLR", "CLR")
}


result %>% as_tibble()

as.data.frame(result) %>% 
  write.xlsx("path_way_overlap_result.xlsx")

#### overlap check ####

#### component ####
component <- metabolites_table[, 4]
component <- component[-c(43:50)]

# component <- gsub('*; ', ", ", component)
# component <- gsub('*\n*', "", component)

#### Problem : 위의 gsub가 제대로 반영이 안됨
#### solve : space로 공백을 주지 않고 \\s로 공백을 입력함. 
ts <- gsub(';\\s', ",", as.character(component[[2]]))
ts <- gsub('*\n*', "", ts)

# ts <- gsub('^\\s+', "", ts) 공백으로 시작하는 character의 공백을 없앨 것. 
ts <- strsplit(ts, ",")
ts # component[[2]]가 제대로 잘린 모습을 확인. 

# component <- gsub('*, *', ",", component)
# component <- gsub(" ", "", component)

#### edit
# ","로 strsplit 불가 : 각 metabolite에서 ","를 사용하는 경우가 있음. 
# 따라서 특정 문자만 제거해주고 ;으로 자르면 될 것 같음
component <- gsub('*\n*', "", component) # \n를 제거 
component <- strsplit(component, ";\\s|;") # component[[4]]에 ";"만 있는 경우가 있어 or로 추가 

sum(unlist(lapply(component, length)) == pathway_result$Total) # 42, clear 

# 변환 완료 
component 


#### component ####

# FC metablolite 
all_metabolites[which(all_metabolites %in% median_FC.metabolite[, 1])] # intersection
all_metabolites[-which(all_metabolites %in% median_FC.metabolite[, 1])] # complement

# CLR metablolite
length(unique(multi_CLR_cate[, 1])) # 57

all_metabolites[which(all_metabolites %in% unique(multi_CLR_cate[, 1]))] # intersection
all_metabolites[-which(all_metabolites %in% unique(multi_CLR_cate[, 1]))] # complement


path_metabolite %in% all_metabolites[which(all_metabolites %in% median_FC.metabolite[, 1])]

#### 7. list with pathway ####
```


```r
#### 0225 permutation AUC ####
install.packages("Biocomb")
library(Biocomb)
library(gtools)

# example for dataset without missing values
data(data_test)
data_test

# class label must be factor
data_test <- raw_info_add_set_log

data_test[,ncol(data_test)+1] <- as.factor(data_test[,2])

# FC, CLR, path, LASSO 따로따로
FC_AUC <- compute.aucs(dattable=data_test[, -c(1:7)][c(FC_metabolite, "V89")]) %>% 
  write.csv("FC_AUC.csv")
CLR_AUC <- compute.aucs(dattable=data_test[, -c(1:7)][c(unique(multi_CLR_cate[, 1]), "V89")]) %>% 
  write.csv("CLR_AUC.csv")
path_AUC <- compute.aucs(dattable=data_test[, -c(1:7)][c(path_metabolite, "V89")]) %>% 
  write.csv("path_AUC.csv")
LASSO_AUC <- compute.aucs(dattable=data_test[, -c(1:7)][c(LASSO_metabolite, "V89")]) %>% 
  write.csv("LASSO_AUC.csv")

out[which(out$AUC > 0.8), ]$Biomarker
arrange(out, desc(AUC))[1:(81*0.2), ]


#### 0225 permutation AUC ####
```

```r
#### 0225 heatmap, random forest, SVM ####
# 1. heatmap
FC_metabolite <- c("...")
unique(multi_CLR_cate[, 1])
path_metabolite
LASSO_metabolite <- rownames(as.data.frame(auto_small.lambda.betas[auto_small.lambda.betas != 0]))

raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))] %>% 
  write.csv("FC_meta.csv")

raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", unique(multi_CLR_cate[, 1])))] %>% 
  write.csv("CLR_meta.csv")

raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", path_metabolite))] %>% 
  write.csv("path_meta.csv")

raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", LASSO_metabolite))] %>% 
  write.csv("lasso_meta.csv")


# 2. Random forest
library(randomForest)
randomForest(as.factor(Group) ~ ., 
             data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))], 
             mtry = floor(sqrt(9)), ntree = 500, importance = T, do.trace = 100)

randomForest(as.factor(Group) ~ ., 
             data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", unique(multi_CLR_cate[, 1])))], 
             mtry = floor(sqrt(57)), ntree = 500, importance = T, do.trace = 100)

randomForest(as.factor(Group) ~ ., 
             data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", path_metabolite))], 
             mtry = floor(sqrt(48)), ntree = 500, importance = T, do.trace = 100)

randomForest(as.factor(Group) ~ ., 
             data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", LASSO_metabolite))], 
             mtry = floor(sqrt(27)), ntree = 500, importance = T, do.trace = 100)

# 3. SVM
library(e1071)

a <- svm(as.factor(Group) ~ ., 
    data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))])

b <- predict(a, raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))][ ,-1])

table(raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))][, 1], b)

a <- svm(as.factor(Group) ~ ., 
         data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", unique(multi_CLR_cate[, 1])))])

b <- predict(a, raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", unique(multi_CLR_cate[, 1])))][ ,-1])

table(raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", unique(multi_CLR_cate[, 1])))][, 1], b)

a <- svm(as.factor(Group) ~ ., 
         data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", path_metabolite))])

b <- predict(a, raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", path_metabolite))][ ,-1])

table(raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", path_metabolite))][, 1], b)

a <- svm(as.factor(Group) ~ ., 
         data=raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", LASSO_metabolite))])

b <- predict(a, raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", LASSO_metabolite))][ ,-1])

table(raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", LASSO_metabolite))][, 1], b)




#### MY heatmap 나중에 다시 시도 ####
t(raw_info_add_set_log[all_metabolites][which(all_metabolites %in% FC_metabolite)]) %>% 
  # rownames(.) <- .$Group %>% 
  pheatmap(., show_rownames=T, show_colnames=F)

# Generate annotations for rows and columns
annotation_col = data.frame(
  CellType = factor(rep(c("CT1", "CT2"), 5)), 
  Time = 1:5
)
rownames(annotation_col) = paste("Test", 1:10, sep = "")

annotation_row = data.frame(
  GeneClass = factor(rep(c("Path1", "Path2", "Path3"), c(10, 4, 6)))
)
rownames(annotation_row) = paste("Gene", 1:20, sep = "")

# Display row and color annotations
pheatmap(test, annotation_col = annotation_col)
pheatmap(test, annotation_col = annotation_col, annotation_legend = FALSE)
pheatmap(test, annotation_col = annotation_col, annotation_row = annotation_row)

Group_with_all_meta <- c("Group", all_metabolites)
raw_info_add_set_log[Group_with_all_meta][which(Group_with_all_meta %in% c("Group", FC_metabolite))] %>% 
  pheatmap()

pheatmap()
#### ####
#### 0225 heatmap, random forest, SVM ####

```




```
#### 02.10 metabolites list up #### 

#### Package "ropls" ####
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("ropls")

data(sacurine)
names(sacurine)
attach(sacurine)
strF(dataMatrix)
strF(variableMetadata)

sacurine.pca <- opls(dataMatrix)

a <- as.matrix(raw_info_add_set[, -c(1:7)])
rownames(a) <- g_index
head(a)  

test <- opls(a, crossvalI = 15)
plot(test, typeVc = c("outlier", "predict-train", "xy-score", "xy-weight"))


data(foods) ## see Eriksson et al. (2001); presence of 3 missing values (NA)
head(foods)
foodMN <- as.matrix(foods[, colnames(foods) != "Country"])
rownames(foodMN) <- foods[, "Country"]
head(foodMN)
foo.pca <- opls(foodMN)
#### Package "ropls" ####

```

```r
#### 0302 KBSI feedback ####
#### pre. library and seed ####
library(caTools)
library(sampling)
library(splitstackshape)
library(caret)
library(RFmarkerDetector)
library(glmnet)
library(pROC)
library(erer)
library(survival)
library(VennDiagram)
set.seed(102)


#### 1. divide dataset and pre-processing ####
train.index <- createDataPartition(unique(raw_info_add_set$set), p = .8, list = FALSE)
train.index[1] == raw_info_add_set$set

# extract corrected data with train.index
a <- c()
for(i in 1 : length(train.index)) { 
  b <- which(train.index[i] == raw_info_add_set$set)
  a <- c(a, b)
  }

# check same as legnth of train.index and length of extracted data
length(a) == length(train.index) * 3 # same 

# raw dataset에 index로 train, test를 넣어주자.
as.numeric(seq(1, 546, 1) %in% a)
train.test.index <- ifelse(as.numeric(seq(1, 546, 1) %in% a) == 1, "train", "test")

# index와 train, test index를 추가한 dataset
raw_info_add_set %>% 
  mutate(train.test.index = train.test.index) %>% 
  mutate(index = seq(1, nrow(.), 1)) %>% 
  select(index, train.test.index, everything()) -> raw_info_add_set_tr.te

# log transformation and scaling 
b <- paretoscale(log(raw_info_add_set_tr.te[, all_metabolites] + 1), exclude = F) # log trans and pareto scaling
raw_info_add_set_tr.te_log.pareto <- as.data.frame(cbind(raw_info_add_set_tr.te[, 1:9], b)) # cbind 

dim(raw_info_add_set_tr.te_log.pareto) == dim(raw_info_add_set_tr.te) # check dimension


# train, test의 분포 알아보기
## matching data라 나이와 성별이 최대한 비슷하게 나뉘어야 함. 
ggplot(raw_info_add_set_tr.te_log.pareto, aes(x = age, fill = train.test.index)) + 
  geom_histogram(alpha = 0.5, aes(y = ..density..), position = 'identity')

ggplot(raw_info_add_set_tr.te_log.pareto, aes(x = age, fill = train.test.index)) + 
  geom_density(alpha = 0.2)

raw_info_add_set_tr.te_log.pareto %>% 
  group_by(train.test.index) %>% 
  count(sex)

ggplot(raw_info_add_set_tr.te_log.pareto, aes(x = sex, fill = train.test.index)) + 
  geom_bar()

ggplot(raw_info_add_set_tr.te_log.pareto, aes(x = train.test.index, y = age, fill = train.test.index)) + 
  geom_boxplot()

train_obs <- dplyr::filter(raw_info_add_set_tr.te_log.pareto, train.test.index == "train")
test_obs <- dplyr::filter(raw_info_add_set_tr.te_log.pareto, train.test.index == "test")

#### 2. 5-Fold dataset ####
# createFolds는 index를 return한다. 
set.seed(102)

fold.index <- createFolds(unique(train_obs$set), k=5, list=TRUE, returnTrain=FALSE)

c <- list()
for(i in 1 : length(fold.index)) { 
  a <- c()
  
  for( j in 1 : length(fold.index[[i]])) {
    b <- rep(unique(train_obs$set)[fold.index[[i]][j]], 3)
    a <- c(a, b)
  }
  c[[i]] <- a   
}

length(c[[3]]) == length(fold.index[[3]])*3 # 개수 일치 
unique(c[[3]]) %in% train_obs$set # set index 일치 

# 위의 결과를 fold.set으로 선언
fold.set <- c 

# 1st fold의 test obs만 filtering 성공
train_obs[which(train_obs$set %in% fold.set[[1]]), ]$set == fold.set[[1]]


#### 3. LASSO ####
set.seed(102)
LASSO_5fold <- function(train, fold.set) { 
  result <- list()
  
  for (i in 1:length(fold.set)) {
    cv.lasso <- cv.glmnet(as.matrix(train[-which(train$set %in% fold.set[[i]]), all_metabolites]), 
                          train[-which(train$set %in% fold.set[[i]]), ]$Group,
                          alpha=1, family = "binomial") # lasso logistic regression 
    lasso.min_lambda <- glmnet(as.matrix(train[-which(train$set %in% fold.set[[i]]), all_metabolites]), 
                              train[-which(train$set %in% fold.set[[i]]), ]$Group,
                              alpha=1, lambda=cv.lasso$lambda.min, family = "binomial") # coefficients
    lasso.coef <- as.data.frame(as.matrix(coef(lasso.min_lambda)))
    
    
    # check accuracy of each fold
    lasso.prediction <- predict(lasso.min_lambda, s=cv.lasso$lambda.min, 
                               newx = as.matrix(train[which(train$set %in% fold.set[[i]]), all_metabolites]), 
                               type = "class")
    
    table <- table(pred=lasso.prediction, true = train[which(train$set %in% fold.set[[i]]), ]$Group)
    accuracy <- mean(lasso.prediction == train[which(train$set %in% fold.set[[i]]), ]$Group)
    AUC <- roc(train[which(train$set %in% fold.set[[i]]), ]$Group, as.numeric(lasso.prediction), plot=FALSE)$auc
    
    # lasso.prediction_test <- predict(lasso.min_lambda, s=cv.lasso$lambda.min, 
    #                             newx = as.matrix(train[which(train$set %in% fold.set[[i]]), all_metabolites]), 
    #                             type = "class")
    # 
    # table_test <- table(pred=lasso.prediction_test, true = train[which(train$set %in% fold.set[[i]]), ]$Group)
    # accuracy_test <- mean(lasso.prediction_test == train[which(train$set %in% fold.set[[i]]), ]$Group)
    # ACU_test <- roc(train[which(train$set %in% fold.set[[i]]), ]$Group, as.numeric(lasso.prediction_test), plot=FALSE)$auc
    
    result[[i]] <- list(lasso.min_lambda, cv.lasso$lambda.min, lasso.coef, table, accuracy, AUC)
  }
  
  names(result) <- c("1st LASSO CV", "2nd LASSO CV", "3nd LASSO CV", "4th LASSO CV", "5th LASSO CV")
  
  return(result)
  
}

test.LASSO_5fold <- LASSO_5fold(train = train_obs, fold.set = fold.set)
capture.output(test.LASSO_5fold, file = "LASSO_test.csv")

lasso.prediction.test <- predict(test.LASSO_5fold[[1]][[1]], s = test.LASSO_5fold[[1]][[2]], 
                                newx = as.matrix(test_obs[, all_metabolites]), 
                                type = "class")
table.test <- table(pred = lasso.prediction.test, true = test_obs$Group)
AUC.test1 <- roc(test_obs$Group, as.numeric(lasso.prediction.test), plot = TRUE)$auc

lasso.prediction.test <- predict(test.LASSO_5fold[[2]][[1]], s = test.LASSO_5fold[[2]][[2]], 
                                 newx = as.matrix(test_obs[, all_metabolites]), 
                                 type = "class")
table.test <- table(pred = lasso.prediction.test, true = test_obs$Group)
AUC.test2 <- roc(test_obs$Group, as.numeric(lasso.prediction.test), plot = TRUE)$auc

lasso.prediction.test <- predict(test.LASSO_5fold[[3]][[1]], s = test.LASSO_5fold[[3]][[2]], 
                                 newx = as.matrix(test_obs[, all_metabolites]), 
                                 type = "class")
table.test <- table(pred = lasso.prediction.test, true = test_obs$Group)
AUC.test3 <- roc(test_obs$Group, as.numeric(lasso.prediction.test), plot = TRUE)$auc

lasso.prediction.test <- predict(test.LASSO_5fold[[4]][[1]], s = test.LASSO_5fold[[4]][[2]], 
                                 newx = as.matrix(test_obs[, all_metabolites]), 
                                 type = "class")
table.test <- table(pred = lasso.prediction.test, true = test_obs$Group)
AUC.test4 <- roc(test_obs$Group, as.numeric(lasso.prediction.test), plot = TRUE)$auc

lasso.prediction.test <- predict(test.LASSO_5fold[[5]][[1]], s = test.LASSO_5fold[[5]][[2]], 
                                 newx = as.matrix(test_obs[, all_metabolites]), 
                                 type = "class")
table.test <- table(pred = lasso.prediction.test, true = test_obs$Group)
AUC.test5 <- roc(test_obs$Group, as.numeric(lasso.prediction.test), plot = TRUE)$auc


AUC.test1; AUC.test2; AUC.test3; AUC.test4; AUC.test5;



lasso.final <- glmnet(as.matrix(train[-which(train$set %in% fold.set[[i]]), all_metabolites]), 
                           train[-which(train$set %in% fold.set[[i]]), ]$Group,
                           alpha=1, lambda=cv.lasso$lambda.min, family = "binomial") # coefficients
lasso.coef <- as.data.frame(as.matrix(coef(lasso.final)))


# check accuracy of each fold




#### 5-fold CV LASSO ####
cv.lasso <- cv.glmnet(as.matrix(train_obs[, all_metabolites]), 
                      train_obs$Group,
                      alpha=1, family = "binomial", nfolds = 5) # lasso logistic regression 
lasso.min_lambda <- glmnet(as.matrix(train_obs[, all_metabolites]), 
                           train_obs$Group,
                           alpha=1, lambda=cv.lasso$lambda.min, family = "binomial") # coefficients

lasso.1se <- glmnet(as.matrix(train_obs[, all_metabolites]), 
                    train_obs$Group,
                    alpha=1, lambda=cv.lasso$lambda.1se, family = "binomial") # coefficients


lasso.min_coef <- as.data.frame(as.matrix(coef(lasso.min_lambda)))
lasso.1se_coef <- as.data.frame(as.matrix(coef(lasso.1se)))

lasso.prediction.min_test <- predict(lasso.min_lambda, s = cv.lasso$lambda.min, 
                                 newx = as.matrix(test_obs[, all_metabolites]), 
                                 type = "class")

lasso.prediction.1se_test <- predict(lasso.1se, s = cv.lasso$lambda.1se, 
                                     newx = as.matrix(test_obs[, all_metabolites]), 
                                     type = "class")

AUC.test_min <- roc(test_obs$Group, as.numeric(lasso.prediction.min_test), plot = TRUE)$auc
AUC.test_1se <- roc(test_obs$Group, as.numeric(lasso.prediction.1se_test), plot = TRUE)$auc

lasso.min_coef %>% 
  rownames_to_column() %>% 
  write.csv("lasso.min_coef.csv")

lasso.1se_coef %>% 
  rownames_to_column() %>% 
  write.csv("lasso.1se_coef.csv")

#### 4. Logistic Regression ####
set.seed(102)


#### Part 1. change to categorical variable ####
replace.using.mid.high <- function(data){ 
  
  data %>% 
    dplyr::filter(Group == 0) %>%
    select(all_metabolites) %>% 
    summarise_all(funs(q33 = quantile(., probs = .33),
                       q66 = quantile(., probs = .66))) %>% 
    select(contains("_q33"))  %>% 
    rename_at(vars(matches("_q33$")), funs(str_replace(., "_q33", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> mid_standard_log
  
  data %>% 
    dplyr::filter(Group == 0) %>%
    select(all_metabolites) %>% 
    summarise_all(funs(q33 = quantile(., probs = .33),
                       q66 = quantile(., probs = .66))) %>% 
    select(contains("_q66"))  %>% 
    rename_at(vars(matches("_q66$")), funs(str_replace(., "_q66", ""))) %>% 
    rownames_to_column %>%
    gather(variable, value, -rowname) -> high_standard_log
  
  
  u <- matrix(0, nrow(data), ncol(data))
  
  for(i in 1:nrow(mid_standard)){ 
    for (j in 1:nrow(data)){
      
      ## 33th 보다 작으면 1, 
      ## 1보다는 크고 66th보다 작으면 2
      ## 66th보다 크면 3
      if(mid_standard_log[i, 3] > data[j, i]) {
        u[j, i] <- 1 
      } else if(high_standard_log[i, 3] > data[j, i]) {
        u[j, i] <- 2
      } else {
        u[j, i] <- 3
      }
    }
  }
  u <- as.data.frame(u)
  colnames(u) <- all_metabolites
  
  result <- list(u, mid_standard_log, high_standard_log)
  names(result) <- c("change to categorical", "mid_standard_log_pareto", "high_standard_log_pareto")
  return(result)
}

u <- replace.using.mid.high(raw_info_add_set_tr.te_log.pareto[, all_metabolites])

#### 제대로 바뀌었는지 check ####
u[[1]] %>% 
  as_tibble()

raw_info_add_set_tr.te_log.pareto %>% 
  group_by(Group) %>% 
  mutate_at(vars(all_metabolites), list(~replace(., Group == 0, ntile(., 3)))) %>% 
  select(15) %>% as.data.frame() -> check_divided

cbind(u[[1]][, 6], check_divided)

# log tras 후 low, mid, high로 나눈 dataset 선언
tr.re.log.pareto.mid.high <- as.data.frame(cbind(raw_info_add_set_tr.te_log.pareto[, 1:9], u[[1]]))

cate_train_obs <- dplyr::filter(tr.re.log.pareto.mid.high, train.test.index == "train")
cate_test_obs <- dplyr::filter(tr.re.log.pareto.mid.high, train.test.index == "test")




#### Part 2. 5-fold-crossvalidation ####

LR_5fold <- function(train, fold.set) { 
  fold_result <- data.frame(matrix(rep(0, 81*10), 81, 10))
  colnames(fold_result) <- c("1st fold AUC ", "1st fold test AUC", 
                             "2nd fold AUC ", "2nd fold test AUC",
                             "3nd fold AUC ", "3nd fold test AUC",
                             "4th fold AUC ", "4th fold test AUC",
                             "5th fold AUC ", "5th fold test AUC")
  row.names(fold_result) <- all_metabolites
  
  LR_result <- data.frame(matrix(rep(0, 81*3), 81, 3))
  colnames(LR_result) <- c("metabolite", "average of AUC in 5f-CV ", "average of AUC in test set")
  
  result <- list()
  
  #### 하나의 fold 당 81개의 metabolite를 대상으로 한 LR model이 building 되어야 함. 
  for (i in 1:length(fold.set)) {
    for (j in 1:length(all_metabolites)) { 
    
      #### 하나의 metabolite와 여러 개의 comfounder(sex, age, smoking, alcohol)
      formula <- as.formula(paste("Group ~ ", 
                                  paste0("factor(", "sex)"),
                                  "+ age", 
                                  paste0("+ factor(", "smoking)"),
                                  paste0("+ factor(", "alcohol)"),
                                  "+",  
                                  paste0("factor(", all_metabolites[j]), ")" ))
      
      LR_model <- glm(formula = formula, 
                      data = cate_train_obs[-which(cate_train_obs$set %in% fold.set[[i]]), ],
                      family = "binomial")
      
      # fold 내에서의 prediction 
      predict_fold <- predict(LR_model, cate_train_obs[which(cate_train_obs$set %in% fold.set[[i]]), ], type = "response")
      
      # fold 내에서의 prediction를 이용한 AUC
      ROC_fold <- ROC(predict_fold, stat = cate_train_obs[which(cate_train_obs$set %in% fold.set[[i]]), ]$Group, 
                        AUC = TRUE)
      
      # fold 내의 model과 test set을 이용한 prediction
      predict_test <- predict(LR_model, cate_test_obs, type = "response")
      ROC_test <- ROC(predict_test, stat = cate_test_obs$Group, AUC = TRUE)
      
      fold_result[j, c((2*i)-1, (2*i))] <- c(ROC_fold$AUC, ROC_test$AUC)
      
      }
  }
  
  return(fold_result)
  
}

test.LR_5fold <- LR_5fold(train = cate_train_obs, fold.set = fold.set)

test.LR_5fold %>% 
  write.csv("LR_5fold.csv")


#### 5. Conditional Logistic Regression ####
# categorical variable을 이용한 CLR with multiple comfound 
CLR_mfactor_c_HW <- function(data, all_metabolites, strata_name, point) { 
  
  m1 <- list()
  n <- c()
  m1_j <- 1
  
  a1 <-list()
  all_name <- c()
  
  for(i in 1:length(all_metabolites)) {
    formula <- as.formula(paste("Group ~ ", 
                                paste0("factor(", "sex)"),
                                "+ age", 
                                paste0("+ factor(", "smoking)"),
                                paste0("+ factor(", "alcohol)"),
                                paste0("+ factor(", all_metabolites[i], ")"),
                                paste0("+ strata(", strata_name, ")") ))
    
    r1 <- summary(clogit(formula = formula, 
                         data = data, control = coxph.control(iter.max = 100), method='breslow'))
    r1 <- cbind(r1$conf.int, pvalue = r1$coefficients[, 5], FDR = p.adjust(r1$coefficients[, 5],method="BH"))
    
    # 모든 결과를 a1에 저장
    a1[[i]] <- r1
    all_name <- c(all_name, all_metabolites[i])
    
    # FDR, 0.05보다 작은 결과만 m1에 저장
    if(r1[point, 6] < 0.05) {
      m1[[m1_j]] <- r1
      m1_j <- m1_j+1
      n <- c(n, all_metabolites[i])
    }
  }
  
  result <- list(a1, all_name, m1, n)
  
  return(result)
}

#### Point 체크를 위한 따로 돌려보기 ####
r1 <- summary(clogit(formula = formula, 
                     data = log_mid_high_data_set, control = coxph.control(iter.max = 100), method='exact'))

fdr_test <- summary(clogit(formula = formula, 
                           data = tr.re.log.pareto.mid.high, control = coxph.control(iter.max = 100), method='breslow'))

p.adjust(fdr_test$coefficients[, 5],method="BH")

cbind(fdr_test$conf.int, fdr_test$coefficients[, 5], p.adjust(fdr_test$coefficients[, 5],method="BH"))
#### Point 체크를 위한 따로 돌려보기 ####
# point 8 -> High categorical variable의 위치 

log_pareto_mid_high_CLR <- CLR_mfactor_c_HW(tr.re.log.pareto.mid.high, all_metabolites, "set", 8)

table_gen <- function(result, point) {
  
  z <- result
  q <- z[[2]]
  
  r <- matrix(0, 2, (length(z[[1]][[1]][point, ])))
  r2 <- matrix(0, 2, (length(z[[1]][[1]][point, ])))
  
  for(i in 1:length(z[[1]])) {
    r[1, ] <- c(z[[1]][[i]][point, ])
    r[2, ] <- c(z[[1]][[i]][point+1, ])
    
    r2 <- rbind(r2, r)
  }
  r2 <- r2[-c(1:2), ]
  
  e <- as.data.frame(cbind(rep(q, each =2), r2))
  
  colnames(e) = c("Metabolites","exp(coef)", "exp(-coef)", "lower .95", "upper .95", "p-value", "FDR")
  
  return(e)
}

CLR_summary <- table_gen(log_pareto_mid_high_CLR, 7)



# control group, mid,high 기준 n개
tr.re.log.pareto.mid.high %>% 
  group_by(Group) %>% 
  select(c(Group, all_metabolites)) %>% 
  dplyr::filter(Group == 0) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 364), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> control_log_mid_high_n

# case group, mid,high 기준 n개
tr.re.log.pareto.mid.high %>% 
  group_by(Group) %>% 
  select(c(Group, all_metabolites)) %>% 
  dplyr::filter(Group == 1) %>% 
  gather(Group, var) %>% 
  cbind(index=rep(1:81, each = 182), .)%>% 
  count(Group, var, index) %>% 
  arrange(index) %>% 
  as.data.frame() -> case_log_mid_high_n

as.data.frame(mid_standard_log) -> mid_criteria_log
as.data.frame(high_standard_log) -> high_criteria_log

#### TO write table ####

n2 <- c()
for(i in 1:length(all_metabolites)) {
  # 만약 4분할하면 3을 4로 바꿔주면 됨 
  
  # index가 홀수인 경우 
  if( (((case_log_mid_high_n$index[i]+(3*as.numeric(i)))-3)%%2) != 0 ){
    
    j <- (i*3)-2 # 만약 4분할하면 3 -> 4, 2 -> 3
    k <-  (i*2)-1 # 만약 4분할하면 2 -> 3, 1 -> 2
    b1 <- c(CLR_summary[k, 1], "", "", "", "", "", "", "", "", "", "")
    # l1 <- c("Continuous", "", "", "", log_mid_high_CLR_conti[i, ])
    b2 <- c("Low", mid_criteria_log[i, 3], case_log_mid_high_n[j, 4], control_log_mid_high_n[j, 4], "", "", "", "", "", "", "")
    b3 <- c("Mid", high_criteria_log[i, 3], case_log_mid_high_n[j+1, 4], control_log_mid_high_n[j+1, 4], 
            CLR_summary[k, ])
    b4 <- c("High", high_criteria_log[i, 3], case_log_mid_high_n[j+2, 4], control_log_mid_high_n[j+2, 4],
            CLR_summary[k+1, ])
    
    n1 <- rbind(b1, b2, b3, b4)    
    
    # index가 짝수인 경우 
  } else {
    j <- (i*3)-2
    k <- (i*2)-1  
    b1 <- c(CLR_summary[k, 1], "", "", "", "", "", "", "", "", "", "")
    # l1 <- c("Continuous", "", "", "", log_mid_high_CLR_conti[i, ])
    b2 <- c("Low", mid_criteria_log[i, 3], case_log_mid_high_n[j, 4], control_log_mid_high_n[j, 4], "", "", "", "", "", "", "")
    b3 <- c("Mid", high_criteria_log[i, 3], case_log_mid_high_n[j+1, 4], control_log_mid_high_n[j+1, 4], 
            CLR_summary[k, ])
    b4 <- c("High", high_criteria_log[i, 3], case_log_mid_high_n[j+2, 4], control_log_mid_high_n[j+2, 4],
            CLR_summary[k+1, ])
    
    n1 <- rbind(b1, b2, b3, b4) 
  }
  n2 <- rbind(n2, n1)
  
}


#### Check #####
as.data.frame(n2)[1:20, 1:4]
case_mid_high_n[1:18, ]
control_mid_high_n[1:18, ]
mid_criteria_log[1:5, ]
high_criteria_log[1:5, ]

as.data.frame(n2)[1:12, 5:11]
as.data.frame(CLR_summary)[1:6, ]

as.data.frame(n2)[13:24, 5:11]
as.data.frame(CLR_summary)[7:12, ]
#### Check #####


n2 %>% 
  write.xlsx("CLR_result.xlsx") 




#### 6 Fold change ####

# raw_info_add_set_tr.te_log.pareto %>% 
#   dplyr::filter(Group == 0) %>% 
#   dplyr::select(all_metabolites) %>% 
#   apply(. ,2 , FUN=median) -> group0median
# 
# raw_info_add_set_tr.te_log.pareto %>% 
#   dplyr::filter(Group == 1) %>% 
#   dplyr::select(all_metabolites) %>% 
#   apply(. ,2, FUN=median) -> group1median
# 
# FC <- group1median / group0median
# FC_edit <- FC + min(FC)
# log2FC <- log(abs(FC), 2)
# 
# pvalue <- lapply(all_metabolites, function(v) {
#   kruskal.test(as.data.frame(raw_info_add_set)[, v] ~ as.data.frame(raw_info_add_set)[, 'Group'])$p.value
# })
# 
# pvalue.BHcorr <- p.adjust(pvalue, method = "BH") # FDR
# pvalue.BHcorr.neglog <- -log10(pvalue.BHcorr)
# 
# volcano.data <- data.frame(log2FC, FC, group1median, group0median, pvalue.BHcorr.neglog, unlist(pvalue))
# 
# volcano.data %>% 
#   rownames_to_column() %>% 
#   dplyr::filter(log2FC < -1 & pvalue.BHcorr.neglog > 1.301) -> red_set
# 
# volcano.data %>% 
#   rownames_to_column() %>% 
#   dplyr::filter(log2FC > 1 & pvalue.BHcorr.neglog > 1.301) -> green_set
# 
# volcano.data$pvalue.BHcorr <- pvalue.BHcorr
# 
# volcano.data %>% 
#   rownames_to_column() -> volcano.data
# volcano.data$sig <- ifelse(volcano.data$pvalue.BHcorr.neglog < 1.301, "Not Sig",
#                            ifelse(volcano.data$log2FC < -1 & volcano.data$pvalue.BHcorr.neglog > 1.301, "log2(FC) ≤ -1", 
#                                   ifelse(volcano.data$log2FC > 1 & volcano.data$pvalue.BHcorr.neglog > 1.301, "log2(FC) ≥ 1", "-1 < log2(FC) < 1")))
# 
# volcanoEM <- ggplot(volcano.data, aes(x= log2FC, y=pvalue.BHcorr.neglog)) +  
#   geom_point(aes(color=sig)) + 
#   scale_color_manual(values = c("black", "red", "green","grey")) + 
#   theme_bw(base_size = 12) +  
#   theme(legend.position = "right", legend.title = element_blank()) + 
#   geom_text_repel(data = subset(volcano.data, sig == "log2(FC) ≤ -1" | sig == "log2(FC) ≥ 1"), aes(label = rowname), size=5, box.padding = unit(0.35, "lines"), point.padding = unit(0.3, "lines")) +
#   ggtitle("Figure 1.1 Volcano plot using median fold change and p-value of Kruskal test results") + labs(x=bquote(~log[2]~ "Fold change"), y=bquote(~-log[10]~adjusted-~italic(P))) + 
#   theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15, color = "black"))
# 
# 
# plot(volcanoEM)


#### 7. venndiagram ####
#### part1. metabolite name 추출 
# 1) LASSO
lasso.min_coef %>% 
  rownames_to_column() %>% 
  dplyr::filter(s0 != 0) %>% 
  select(1) -> lasso_min_meta

lasso.1se_coef %>% 
  rownames_to_column() %>% 
  dplyr::filter(s0 != 0) %>% 
  select(1) -> lasso_1se_meta

# 2) LR
apply(test.LR_5fold, 1, mean) %>% 
  as.data.frame() %>% 
  rownames_to_column() %>% 
  dplyr::filter(. > 0.8) %>%
  dplyr::arrange(desc(.)) %>% 
  select(1) -> LR_meta

# 3) CLR
CLR_meta <- log_pareto_mid_high_CLR[[4]]

# 2)와 CLR joint
sum(CLR_meta %in% LR_meta[, 1])




# 4) FC
FC_metabolite


unique(c(lasso_1se_meta[, 1], LR_meta[, 1], CLR_meta, FC_metabolite))[-1]

#### part2. venndiagram 
# venn <- as.data.frame(cbind(all_metabolites %in% lasso_min_meta[, 1], 
#                             all_metabolites %in% lasso_1se_meta[, 1], 
#                             all_metabolites %in% LR_meta[, 1], 
#                             all_metabolites %in% CLR_meta, 
#                             all_metabolites %in% FC_metabolite))

venn <- as.data.frame(cbind(all_metabolites %in% lasso_1se_meta[, 1], 
                            all_metabolites %in% LR_meta[, 1], 
                            all_metabolites %in% CLR_meta, 
                            all_metabolites %in% FC_metabolite))

row.names(venn) <- all_metabolites
colnames(venn) <- c("Lasso_1se", "LR_AUC", "CLR_FDR", "FC")
venn

venn.diagram(
  x = list(
    FC = which(venn$FC==TRUE),   # A 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    Lasso_1se = which(venn$Lasso_1se==TRUE),   # B 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    LR = which(venn$LR==TRUE),   # C 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
    CLR = which(venn$CLR==TRUE) # D 그룹에서 평가를 좋게한 인터뷰 대상자 번호를 찾아냅니다.
  ),
  filename = "Venn_Diagram_4set.tiff",
  col = "black",   # 벤 다이어그램 테두리 색상을 설정합니다.
  lty = "dotted",   # 벤 다이어그램 테두리 선 모양을 설정합니다.
  fill = c("dodgerblue", "goldenrod1", "darkorange1", "seagreen3"),   # 각 벤 다이어그램 내부 색상을 설정합니다.
  alpha = 0.50,   # 벤 다이어그램의 알파 투명도를 설정합니다.
  cat.col = c("dodgerblue", "goldenrod1", "darkorange1", "seagreen3"),   # 각 벤 다이어그램의 명칭에 대한 색상을 설정합니다.
  cat.cex = 1.5,   # 각 벤 다이어그램의 명칭에 대한 글자 크기를 설정합니다.
  cat.fontface = "bold",   # 각 벤 다이어그램의 명칭에 대한 글자를 볼드체로 설정합니다.
  margin = 0.05   #  벤 다이어그램 주위의 공간을 설정합니다.
)

venn %>% 
  write.xlsx("venn.xlsx")

unique(c(lasso_1se_meta[, 1], LR_meta[, 1], CLR_meta, FC_metabolite))[-1] %>% 
  write.xlsx("union.xlsx")
#### 0302 ####
```

```r
#### 0306 ####
library(randomForest)
library(caret)
set.seed(102)

#### train part ####
# repeated 5fold CV search
fitControl <- trainControl(method = "repeatedcv", number = 5, repeats = 5)
rf_fit <- train(as.factor(Group) ~ ., data = train_obs[, c("Group", union_metabolite)], 
                method = "rf", trControl = fitControl, verbose = F, importance = T)

plot(rf_fit)
varImpPlot(rf_fit$finalModel)

importance(rf_fit$finalModel, type = 1)
importance(rf_fit$finalModel, type = 2)



# repeated 5fold CV + grid search 
fitControl_grid <- trainControl(method = "repeatedcv", number = 5, repeats = 5, search = "grid")
tunegrid <- expand.grid(mtry = 1:length(union_metabolite))
rf_fit_grid <- train(as.factor(Group) ~ ., data = train_obs[, c("Group", union_metabolite)], 
                     method = "rf", trControl = fitControl, verbose = F, importance = T, tuneGrid = tunegrid)
plot(rf_fit_grid)
varImpPlot(rf_fit_grid$finalModel)

importance(rf_fit_grid$finalModel, type = 1)
importance(rf_fit_grid$finalModel, type = 2)


#### repeated 5fold CV for tuning hyper-parameters, mtry, ntree ####
customRF <- list(type = "Classification",
                 library = "randomForest",
                 loop = NULL)

customRF$parameters <- data.frame(parameter = c("mtry", "ntree"),
                                  class = rep("numeric", 2),
                                  label = c("mtry", "ntree"))

customRF$grid <- function(x, y, len = NULL, search = "grid") {}

customRF$fit <- function(x, y, wts, param, lev, last, weights, classProbs) {
  randomForest(x, y,
               mtry = param$mtry,
               ntree=param$ntree)
}

#Predict label
customRF$predict <- function(modelFit, newdata, preProc = NULL, submodels = NULL)
  predict(modelFit, newdata)

#Predict prob
customRF$prob <- function(modelFit, newdata, preProc = NULL, submodels = NULL)
  predict(modelFit, newdata, type = "prob")

customRF$sort <- function(x) x[order(x[,1]),]
customRF$levels <- function(x) x$classes



control <- trainControl(method="repeatedcv", 
                        number=5, 
                        repeats=5,
                        allowParallel = TRUE)

tunegrid <- expand.grid(.mtry=c(1:15),.ntree=seq(40, 400, 40))
metric <- "Accuracy"
set.seed(102)
custom <- train(as.factor(Group)~., data=train_obs[, c("Group", union_metabolite)], method=customRF, 
                metric = metric, tuneGrid=tunegrid, trControl=control) # $importance 추가 전 
plot(custom)
varImpPlot(custom$finalModel)

importance(custom$finalModel, type = 1)
importance(custom$finalModel, type = 2)



customRF$importance <- TRUE
metric <- c("Accuracy", "kappa")
custom2 <- train(as.factor(Group)~., data=train_obs[, c("Group", union_metabolite)], method=customRF, 
                metric = metric, tuneGrid=tunegrid, trControl=control) # $importance 추가 후 

varImpPlot(custom2$finalModel)


importance(custom2$finalModel, type = 1)
importance(custom2$finalModel, type = 2)






#### test part ####
test_rf_fit <- predict(rf_fit, newdata = test_obs[, c("Group", union_metabolite)]) %>% confusionMatrix(as.factor(test_obs$Group))
test_rf_fit_grid <- predict(rf_fit_grid, newdata = test_obs[, c("Group", union_metabolite)]) %>% confusionMatrix(as.factor(test_obs$Group))
test_rf_custom <- predict(custom, newdata = test_obs[, c("Group", union_metabolite)]) %>% confusionMatrix(as.factor(test_obs$Group))


test_rf_fit$overall
test_rf_fit_grid$overall
test_rf_custom$overall


#### 0306 ####

```
