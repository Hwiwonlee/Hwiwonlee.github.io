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
metabolites_list$Match -> metabolites_name

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
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> BN_info
  
  # metabolites 이름 및 개수 체크  
  metabolites_name[-which(metabolites_name == "NA")] == colnames(BN_info)[8:88]

  
  
  
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
BN_info %>% 
  select(-c(stage_raw, NO, Name, set_pre, Group_RN.x,
            Batch, order, NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) -> BN_info


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

base_var = colnames(BN_info_st)[3:6]
all_metabolites = colnames(BN_info_st)[8:98]

formula = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(cm, collapse = " + "), "+ strata(set)"))

formula = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(all_metabolites, collapse = " + "), "+ strata(set)"))



BN_info %>% as_tibble() %>% 
  select(smoking) %>% 
  group_by(smoking) %>% 
  summarise(n = n())


summary(clogit(Group ~ sex + age + smoking + alcohol + ... + strata(set), data = BN_info_st))

summary(clogit(Group ~ smoking + ... + strata(set), data = BN_info_st))




summary(glmer(Group ~  sex + age + smoking + ... + (1 | set), 
              data = BN_info_st, family=binomial, nAGQ = 100))

summary(glmer(Group ~ Oct.carnitine.Results + Glutamate.Results + sn.glycerol.3.phosphocholine.Results + 
                        TMAO.Results + (1 | set), 
                      data = BN_info, family=binomial, nAGQ = 100))


clogistic(Group ~ smoking + ..., strata = set, data = BN_info_st, iter.max = 17)



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
metabolites_list <- read.xlsx("...name_map.xlsx", sheetIndex = 1, stringsAsFactors=FALSE)

# HMDB ID 기준 추출 
length(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")])

# 중복 검사 
length(unique(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]))
sum(duplicated(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")]))  

# copy & paste를 위한 cat
cat(metabolites_list$HMDB[which(metabolites_list$HMDB != "NA")], fill = 1)


# list of metabolites
cat(gsub(".Results$", "", names(data_BN[, 7:97])), fill=1)

#### ####

#### Comparison with C and OC group ####

BN_info %>%
  as_tibble() %>% 
  select(-c(1,3:7)) %>% 
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


candidate_metabo <- c(...)




special_metabo <- c(...)

length(candidate_metabo)
length(special_metabo)


BN_info[, which(names(BN_info) == candidate_metabo)]

position_cm <- c()
for(i in 1:ncol(BN_info[, -c(1,3:7)])) {
  for( j in 1:length(candidate_metabo)) {
    if(names(BN_info[, -c(1,3:7)])[i] == candidate_metabo[j]) {
      position_cm <- c(position_cm, i)
    }
  }
}

position_sm <- c()
for(i in 1:ncol(BN_info[, -c(1,3:7)])) {
  for( j in 1:length(special_metabo)) {
    if(names(BN_info[, -c(1,3:7)])[i] == special_metabo[j]) {
      position_sm <- c(position_sm, i)
    }
  }
}

colnames(BN_info[, -c(1,3:7)][, position_cm])
colnames(BN_info[, -c(1,3:7)][, position_sm])

BN_info[, -c(1,3:7)][, c(1, position_sm)] %>%
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
compare_summary_stat <- function(data, Group_postion, position_sm){
  data[, c(Group_postion, position_sm)] %>%
    as_tibble() %>% 
    group_by(Group) %>% 
    summarise_all(funs(mean, median, sd)) -> test
  
  test_t <- as_tibble(cbind(nms = names(test), t(test)))
  test_t <- test_t[-Group_postion, ]
  
  index <- c(rep("Mean", length(position_sm)), rep("Median", length(position_sm)), rep("sd", length(position_sm)))

  cbind(test_t, index) %>% 
    mutate(nms = ifelse(grepl("_mean$", nms)|
                          grepl("_median$", nms)|
                          grepl("_sd$", nms), 
                        gsub("_mean$|_median$|_sd$", "", nms), "ERROR")) -> test_t
  
  if(grepl("ERROR", test_t$nms) == TRUE) {
    stop("In dropping summary stat tag process, occured error. So please check mutate step")
  }
  
  return(test_t)
}

test_function <- compare_summary_stat(BN_info[, -c(1,3:7)], 1, position_sm)
test_function

## Plus, Compare_summary_stat function의 argument 중 dataset의 group column을 따로 줄 수는 없을까? 
## group_by(Group)이 아니라 Group를 argument로 commit 할 수 있을까? 


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
