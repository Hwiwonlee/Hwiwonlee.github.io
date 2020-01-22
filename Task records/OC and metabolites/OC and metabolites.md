LOG

[Function to pass parameter to perform group_by in R](https://stackoverflow.com/questions/55246913/function-to-pass-parameter-to-perform-group-by-in-r)
[Plot every column in a data frame as a histogram on one page using ggplot](https://stackoverflow.com/questions/13035834/plot-every-column-in-a-data-frame-as-a-histogram-on-one-page-using-ggplot)


```r
data_BN <- read.xlsx("...BN_mastersheet.xlsx", sheetIndex = 1, stringsAsFactors=FALSE)
data_MN <- read.xlsx("...MN_mastersheet.xlsx", sheetIndex = 1, stringsAsFactors=FALSE)


colnames(data_BN)[1:6] <- c("Name", "NO", "Group", "Group_RN", "Batch", "Order")
colnames(data_MN)[1:4] <- c("Name", "NO", "Group", "Group_RN")

data_BN <- data_BN[-1, ]
data_MN <- data_MN[-1, ]

data_BN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  
  # metabolites 결과에서 붙어나온 .Results를 삭제 
  rename_at(vars(matches(".Results$")), funs(str_replace(., ".Result", ""))) %>% 
  
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_BN
  # group_by(Group) %>% summarise(n = n())

data_MN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  
  # metabolites 결과에서 붙어나온 .Results를 삭제 
  rename_at(vars(matches(".Results$")), funs(str_replace(., ".Result", ""))) %>% 
  
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_MN

  # group_by(Group) %>% summarise(n = n())

data_BN %>% 
  group_by(Group) %>%  summarise(n=n())


data_info <- read.xlsx("...info_mastersheet.xlsx", header=FALSE, sheetIndex = 1, stringsAsFactors=FALSE)
data_info <- data_info[-1, ]
names(data_info) <- c("NCC_num", "Group_RN", "TB_num", "NO", "sex", "age", "smoking", "alcohol", "주장기", "stage_raw", "stage", "box", "위치")

data_info %>% 
  type_convert(cols(NO = col_double())) -> data_info

data_info %>% 
  group_by(smoking, alcohol) %>% 
  summarise(n = n())

metabolites_list <- read.xlsx("...name_map.xlsx", sheetIndex = 1)

# 공백 제거 
metabolites_name <- gsub(" $", "", metabolites_list$Match)
length(metabolites_name) # 91개  
length(metabolites_name[-which(metabolites_list$Match == "NA")]) # 81개
#### ####

#### <TO do> Oral cancer & metabolites는 1:2 matching이니까 set value를 하나 만들자. ####

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

#### (Be in Use) <PROBLEM< scailing을 해야하나? 해야하면 어떤 scailing을 해야 하나? ####

Drawing_hist_each_var <- function(data, target_var_list){
  # 1. data를 받고
  # 2. column에 따라 histogram을 그리고
  #    - 전체적인 개형을 판단하기 위함이므로 여러 개를 한 화면에 그려도 될 것 같음
  #    - 색 등으로 grouping을 해볼 수도 있겠다. 
  # 3. 저장한다.
  
  sub_data <- data[target_var_list]
  
  for( i in 1:ncol(sub_data)){
    ggplot
  }
  
}

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

library(MetaboAnalystR)

mSet <- InitDataObjects("conc", "pathora", FALSE)
cmpd.vec <- c(..)

mSet <- Setup.MapData(mSet, cmpd.vec);
mSet <- CrossReferencing(mSet, "hmdb");
mSet <- CreateMappingResultTable(mSet)

#### ERROR ####

mSet <- SetKEGG.PathLib(mSet, "hsa")

#### ERROR ####

mSet <- SetMetabolomeFilter(mSet, F);
mSet <- CalculateOraScore(mSet, "rbc", "hyperg")
mSet <- PlotPathSummary(mSet, "path_view_0_", "png", 72, width=NA)


```
