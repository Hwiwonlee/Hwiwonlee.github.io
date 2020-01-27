LOG

[Function to pass parameter to perform group_by in R](https://stackoverflow.com/questions/55246913/function-to-pass-parameter-to-perform-group-by-in-r)  
[Plot every column in a data frame as a histogram on one page using ggplot](https://stackoverflow.com/questions/13035834/plot-every-column-in-a-data-frame-as-a-histogram-on-one-page-using-ggplot)  
[Outlier detection and treatment with R](https://www.r-bloggers.com/outlier-detection-and-treatment-with-r/)  
[GGPlot Legend Title, Position and Labels](https://www.datanovia.com/en/blog/ggplot-legend-title-position-and-labels/#change-legend-title)  
[Plot multiple boxplot in one graph](https://stackoverflow.com/questions/14604439/plot-multiple-boxplot-in-one-graph)  



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

UCLR <- function(data, target_position) {
  
  result <- list(NULL, NULL)
  summary_UCLR <- c()
  
  
  list <- names(data[-target_position])
  
  for (i in 1 : length(list)){
    formula <- as.formula(paste("Group ~", list[i], "+ strata(set)"))
    result_ith_UCLR <- round(summary(clogit(formula = formula, data = data))$coefficients, 4)
    summary_UCLR <- rbind(summary_UCLR, result_ith_UCLR)
  }
  
  summary_UCLR <- as.data.frame(summary_UCLR)
  
  #### <TO DO> rename으로바꿔보기 ####
  colnames(summary_UCLR)[5] <- "p_value"
  
  summary_UCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) %>% 
    dplyr::filter(p_value <= 0.05) -> result[[1]]
  
  
  summary_UCLR %>% 
    tibble::rownames_to_column(., "Name") %>% 
    dplyr::arrange(p_value) -> result[[2]]
    
  return(result)
}

#### ####

raw_result_unscale <- UCLR(BN_info, c(1,2,7))
raw_result_log <- UCLR(BN_info_log, c(1,2,7))
raw_result_st <- UCLR(BN_info_st, c(1,2,7))

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
summary(clogit(formula = Group ~ smoking + alcohol + beta_Hydroxybutyric_acid + 
                 Acetylcholine + L_Alanine + L_Arginine + L_Aspartic_acid + 
                 L_Asparagine + L_Carnitine + Choline + Creatinine + Dimethylglycine + 
                 Gamma_Aminobutyric_acid + Betaine + L_Glutamine + Glycine + 
                 L_Isoleucine + L_Kynurenine + L_Leucine + L_Lysine + L_Methionine + 
                 Nicotinic_acid + L_Phenylalanine + L_Proline + Pyridoxamine + 
                 Pyridoxine + L_Serine + Taurine + L_Threonine + Hydroxy_L_proline + 
                 Urea + L_Valine + L_Acetylcarnitine + Decanoylcarnitine + 
                 L_Glutamic_acid + Hexanoylcarnitine + Isovalerylcarnitine + 
                 L_Octanoylcarnitine + Glycerophosphocholine + Trimethylamine_N_oxide, 
               data = PSM1_raw_info_add_set, method='exact'))

summary(clogit(formula = PSM_formula_candi, data = PSM1_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), method='exact'))

summary(clogit(formula = PSM_formula_candi, data = PSM1_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), method='breslow'))

summary(clogit(formula = PSM_formula_candi, data = PSM1_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), method='approximate'))


# PSM2_raw_info_add_set을 이용한 CLR
summary(clogit(formula = PSM_formula_candi, 
               data = PSM2_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), 
               method='exact'))

summary(clogit(formula = as.formula(paste("Group ~ ", paste(a, collapse = " + "), "+ strata(subclass)")),
               data = PSM2_raw_info_add_set, 
               control = coxph.control(iter.max = 10000), 
               method='exact'))

a <- c(base_var, Change_names(candidate_metabo))[-c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,29)]
a %in% Change_names(special_metabo)


clogistic(formula = Group ~ L_Acetylcarnitine + Decanoylcarnitine + L_Glutamic_acid + 
                    Hexanoylcarnitine + Isovalerylcarnitine + L_Octanoylcarnitine + 
                    Glycerophosphocholine + Trimethylamine_N_oxide,
          strata = subclass, data = PSM2_raw_info_add_set, iter.max = 10000)

#### 결과보고를 위한 작성 ####

```
