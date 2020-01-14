```r
data_BN <- read.xlsx("...BN_mastersheet.xlsx", sheetIndex = 1)
data_MN <- read.xlsx("...MN_mastersheet.xlsx", sheetIndex = 1)


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
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC"))

  # group_by(Group) %>% summarise(n = n())

data_BN %>% 
  group_by(Group) %>%  summarise(n=n())


data_info <- read.xlsx("...mastersheet_matching.xlsx", header=FALSE, sheetIndex = 1)
data_info <- data_info[-1, ]
names(data_info) <- c("NCC_num", "Group_RN", "TB_num", "NO", "sex", "age", "smoking", "alcohol", "주장기", "stage_raw", "stage", "box", "위치")

data_info %>% 
  type_convert(cols(NO = col_double())) -> data_info

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


#### <To DO> merge ####

# Using batch normalization 
data_BN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  mutate(set_pre = set_pre) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  select(set_pre, Group, everything()) %>% 
  arrange(set_pre) %>% 
  mutate(set = set) %>% # mutate 'set' part
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
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) -> BN_info

## 전체 stage 수정 후 stage 별 n개 체크, 수정 완료 
# group_by(stage) %>% summarise(n = n())



# Using median Normalization 
data_MN %>% 
  type_convert(cols(NO = col_double())) %>% 
  merge(data_info, by = 'NO') %>% # Merge part 
  as_tibble() %>%
  mutate(set_pre = set_pre) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) %>% 
  select(set_pre, Group, everything()) %>% 
  arrange(set_pre) %>% 
  mutate(set = set) %>% # mutate 'set' part
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



cut(BN_info$age, 4)
cut_number(BN_info$age,3)

as.numeric(cut_number(BN_info$age,3))



BN_info %>% 
  select(-c(stage_raw, NO, Name, set_pre, Group_RN.x,
            Batch, Order, NCC_num, Group_RN.y, TB_num, 주장기, box, 위치)) %>% 
  mutate(Group = ifelse(Group == "C", 0, 1)) %>% 
  mutate(age = as.numeric(cut_number(BN_info$age, 3))) -> BN_info

BN_info <- cbind(BN_info[, 1:7], log(BN_info[, 8:98]))
BN_info[] <- Map(function(x) replace(x, is.infinite(x), 0.01), BN_info)

BN_info %>% as_tibble()

# metabolites들의 scale이 너무 큼. log scale로 바꿔보자. 
log_BN_info <- BN_info[, 8:98]
which(log_BN_info < 0) # 0보다 작은 값이 있는가? 없음
length(which(log_BN_info < 1)) # 944
length(which(log_BN_info == 0)) # 675
length(which(log_BN_info > 0 & log_BN_info < 1)) # 269 





res_clogistic <- clogistic(Group ~ .-set, strata = set, data = BN_info, iter.max=30)

coef(summary(res_clogistic))[,4]

coef(res_clogistic)[2]

str(summary(res_clogistic), max = 1)
str(res_clogistic, max = 1)


#### <TO DO> clogit 사용해보기 ####


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
  set_pre <- sort(set_pre)
  
  set = c()
  for (i in 1:(nrow(data)/case_interval)) {
    a = rep(i, case_interval)
    set = c(set, a)
  }
  
  result = matrix(c(set_pre, set), nrow(data), 2)
  return(result)
  
}
#### <TO DO> Fuctnion 만들기 #### 
matching_set_num(data_BN[1:546, ], 3, 3, 1)

```
