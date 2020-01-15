```r
data_BN <- read.xlsx("C:/Users/75533/Working/dataset/Oral cancer normalization data/BN_NCC_mastersheet.xlsx", sheetIndex = 1)
data_MN <- read.xlsx("C:/Users/75533/Working/dataset/Oral cancer normalization data/MN_NCC_mastersheet.xlsx", sheetIndex = 1)


colnames(data_BN)[1:6] <- c("Name", "NO", "Group", "Group_RN", "Batch", "Order")
colnames(data_MN)[1:4] <- c("Name", "NO", "Group", "Group_RN")

data_BN <- data_BN[-1, ]
data_MN <- data_MN[-1, ]

data_BN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_BN
  # group_by(Group) %>% summarise(n = n())

data_MN %>% 
  as_tibble() %>% 
  type_convert(cols(NO = col_double())) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_MN

  # group_by(Group) %>% summarise(n = n())

data_BN %>% 
  group_by(Group) %>%  summarise(n=n())


data_info <- read.xlsx("C:/Users/75533/Working/dataset/Oral cancer normalization data/환자정보 mastersheet_matching.xlsx", header=FALSE, sheetIndex = 1)
data_info <- data_info[-1, ]
names(data_info) <- c("NCC_num", "Group_RN", "TB_num", "NO", "sex", "age", "smoking", "alcohol", "주장기", "stage_raw", "stage", "box", "위치")

data_info %>% 
  type_convert(cols(NO = col_double())) -> data_info

data_info %>% 
  group_by(smoking, alcohol) %>% 
  summarise(n = n())

dim(data_info)
dim(data_MN)
dim(data_BN)
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
  select(set, Group, NO, sex, age, smoking, alcohol, stage_raw, stage, everything()) %>%
  
  ## stage 수정 전 stage 별 n개 체크
  # group_by(stage) %>% summarise(n = n())
  ## 1a, 4a, 4b 발견 
  
  mutate(stage = gsub("^4[a-z]", "4", stage)) %>% 
  mutate(stage = gsub("^1[a-z]", "1", stage)) %>% 
  
  ## stage 수정 후 stage 별 n개 체크, 수정 완료 
  # group_by(stage) %>% summarise(n = n())
  mutate(stage = gsub("-", "0", stage)) %>% 
  mutate(stage = replace_na(stage, "0")) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  mutate(age = as.numeric(cut_number(.$age, 3)))%>% 
  mutate(Group = ifelse(Group == "OC", 1, 0)) -> BN_info
  
  
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
folder_name <- "C:/Users/75533/Working/R/graph_output/"
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

library(Epi)
data(bdendo)
data(bdendo11)

bdendo %>% as_tibble() # 1:4 매칭, case 1, control 2 
bdendo11 # 1:1 매칭, case 1, control 2 
help(bdendo)


BN_info %>% 
  select(-c(stage_raw, NO, Name, set_pre, Group_RN.x,
            Batch, Order, NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) -> BN_info


# metabolites들의 scale이 너무 큼. log scale로 바꿔보자. 
log_BN_info <- BN_info[, 8:98]
which(log_BN_info < 0) # 0보다 작은 값이 있는가? 없음
length(which(log_BN_info < 1)) # 944
length(which(log_BN_info == 0)) # 675
length(which(log_BN_info > 0 & log_BN_info < 1)) # 269 

# Use logarithm
BN_info <- cbind(BN_info[, 1:7], log(BN_info[, 8:98]))
BN_info[, -(1:7)] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info[, -(1:7)])
BN_info %>% as_tibble()





res_clogistic <- clogistic(Group ~ .-set, strata = set, data = BN_info, iter.max=30)

res_clogistic


coef(summary(res_clogistic))[,4]

coef(res_clogistic)[2]

str(summary(res_clogistic), max = 1)
str(res_clogistic, max = 1)


#### <TO DO> clogit 사용해보기 ####
library(survival)
library(lme4)

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



base_var = colnames(BN_info[3:6])
formula = as.formula(paste("Group ~", paste(base_var, collapse = " + "), "+",
                           paste(cm, collapse = " + "), "+ strata(set)"))




BN_info %>% as_tibble()


summary(clogit(Group ~ sex + age + smoking + alcohol + Acetylcarnitine.Results + 
                 Deca.carnitine.Results + Hex.carnitine.Results + Iso.carnitine.Results + 
                 Oct.carnitine.Results + Glutamate.Results + sn.glycerol.3.phosphocholine.Results + 
                 TMAO.Results + strata(set), data = BN_info))

result_glmer <- glmer(Group ~  sex + age + smoking + alcohol + Acetylcarnitine.Results + 
                        Deca.carnitine.Results + Hex.carnitine.Results + Iso.carnitine.Results + 
                        Oct.carnitine.Results + Glutamate.Results + sn.glycerol.3.phosphocholine.Results + 
                        TMAO.Results + (1 | set), 
                      data = BN_info, family=binomial(link=probit), nAGQ = 100)

step(result_glmer)


clogistic(Group ~ sex + age + smoking + alcohol + Acetylcarnitine.Results + 
            Deca.carnitine.Results + Hex.carnitine.Results + Iso.carnitine.Results + 
            Oct.carnitine.Results + Glutamate.Results + sn.glycerol.3.phosphocholine.Results + 
            TMAO.Results, strata = set, data = BN_info, iter.max = 20)



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
metabolites_list <- read.xlsx("C:/Users/75533/Working/dataset/Oral cancer normalization data/name_map.xlsx", sheetIndex = 1)

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
#### <TO DO> Fuctnion 만들기 #### 
matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 1]
matching_set_num(data_BN[1:546, ], 3, 3, 1)[, 2]
```
