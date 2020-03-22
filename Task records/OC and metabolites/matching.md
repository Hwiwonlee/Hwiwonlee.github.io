개인정보 및 변수명 가려서 업로드  
그럼 남는 게 없는데...이걸 어떻게 비식별화하지?  

```r
control_sample <- read.xlsx2(paste(dir,"OC_C_sample_matching.xlsx", sep = "/"), sheetIndex = 1)
case_sample <- read.xlsx2(paste(dir,"OC_C_sample_matching.xlsx", sep = "/"), sheetIndex = 2)



case_sample %>% 
  dplyr::select(-c(1, 7, 8)) %>% 
  dplyr::filter(나이.1 != "") %>% 
  mutate_each_(funs(as.numeric), c(1,2,6)) %>% 
  rename(나이 = 나이.1) %>% 
  group_by(성별) %>% 
  arrange(나이) -> case_sample_2
# summarise(quantile = list(enframe(quantile(나이, probs=c(0,0.25,0.5,0.75,1))))) %>% 
# unnest(cols = c(quantile)) 
# 남 (46, 62, 71, 76.8, 90)
# 여 (43, 54.8, 62, 74.5, 88)
# count(나이) %>% 
# mutate(n_2 = ifelse(나이<50, 4, ifelse(나이<60, 5, ifelse(나이<70, 6, ifelse(나이<80, 7, ifelse(나이<90, 8, 9)))))) %>% 
# count(n_2) -> sampling_num

# ggplot(aes(x=나이)) + geom_histogram() + facet_grid(.~성별)

case_sample_2 <- data.frame(case_sample_2[, -1], Y = 1)

control_sample %>%
  dplyr::select(-4) %>% 
  mutate_each_(funs(as.numeric), 5) %>% 
  group_by(성별) %>% 
  arrange(나이) %>% 
  dplyr::filter(나이 > 40) -> control_sample_2
# # ggplot(aes(x=나이)) + geom_histogram() + facet_grid(.~성별)
# mutate(n_2 = ifelse(나이<50, 4, ifelse(나이<60, 5, ifelse(나이<70, 6, ifelse(나이<80, 7, ifelse(나이<90, 8, 9)))))) %>% 
# dplyr::filter(성별 == "남") %>% 
# group_by(n_2) -> man_control_sample

control_sample_2 <- data.frame(control_sample_2, Y = 0)







data <- as.data.frame(rbind(as.matrix(control_sample_2), as.matrix(case_sample_2)))
data$나이 <- as.numeric(data$나이)

data %>% 
  dplyr::filter(성별 == "남") -> man_data

data %>% 
  dplyr::filter(성별 == "여") -> woman_data
nrow(man_data) + nrow(woman_data) == nrow(data)


man_data %>% 
  # group_by(Y) %>% 
  # summarise(quantile = list(enframe(quantile(나이, probs=c(0,0.25,0.5,0.75,1))))) %>%
  # unnest(cols = c(quantile)) %>% 
  ggplot(aes(x=factor(Y), y=나이, fill=factor(Y))) +
  geom_boxplot()+
  scale_fill_discrete(name = "Control & Case", labels = c("Control", "Case")) + 
  scale_colour_discrete(guide=FALSE) + 
  labs(x="Control & Case") + ggtitle("Boxplot to show Man's age distribution each group")



woman_data %>% 
  # group_by(Y) %>% 
  # summarise(quantile = list(enframe(quantile(나이, probs=c(0,0.25,0.5,0.75,1))))) %>%
  # unnest(cols = c(quantile)) %>% 
  ggplot(aes(x=factor(Y), y=나이, fill=factor(Y))) +
  geom_boxplot()+
  scale_fill_discrete(name = "Control & Case", labels = c("Control", "Case")) + 
  scale_colour_discrete(guide=FALSE) + 
  labs(x="Control & Case") + ggtitle("Boxplot to show Woman's age distribution each group")

matching_index <- function(data, formula) { 
  
  a <- matchit(formula = formula, data = data, method = "nearest", ratio = 1)
  
  as.data.frame(a$match.matrix) %>% 
    rownames_to_column() %>% 
    rename(case_index = rowname, control_index = "1") %>% 
    mutate_all(funs(as.numeric)) -> matching_index
  
  return(matching_index)
}


man_matching_index <- matching_index(man_data, formula = as.formula("Y ~ 나이"))
woman_matching_index <- matching_index(woman_data, formula = as.formula("Y ~ 나이"))


man_data[man_matching_index[, 2], ] %>% 
  write.xlsx("man_matching.xlsx")


woman_data[woman_matching_index[, 2], ] %>% 
  write.xlsx("woman_matching.xlsx")


```
