```r
# library
library(sas7bdat)


#### 1. preprocess ####
# dataset 
data <- read.sas7bdat(paste0(dir, "...sas7bdat"))

data %>% 
  as_tibble() %>% 
  group_by(cohort) %>% 
  count()

colnames(data) %>% 
  gsub("_[0-9]$|[0-9]$", "", .) %>%
  unique()

data %>% 
  dplyr::filter(cohort == "NC") %>% 
  mutate(RID_n = str_replace(RID, "_[0-9]*$", "")) %>% 
  distinct(RID_n)




data %>% 
  group_by(cohort) %>% 
  # dplyr::filter(cohort == "NC") %>% 
  # select(contains("edate")) %>% 
  dplyr::filter(is.na(edate0) == F & (is.na(edate1) == F |  is.na(edate2) == F | is.na(edate3) == F |
                                        is.na(edate4) == F | is.na(edate5) == F | is.na(edate6) == F)) %>%
  dplyr::filter(cohort == "NC") %>% 
  select(contains("edate"))


data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(is.na(edate1) == F ~ edate1, 
                                 is.na(edate2) == F ~ edate2, 
                                 is.na(edate3) == F ~ edate3, 
                                 is.na(edate4) == F ~ edate4, 
                                 is.na(edate5) == F ~ edate5, 
                                 is.na(edate6) == F ~ edate6, 
                                 TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  # dplyr::filter(edate_after != 0) %>% 
  # count() # follow-up count 
  
  dplyr::filter(is.na(crp) == F) %>%
  count() # number of observation with non-zero cpr value

# edate 1 ~ 6을 합치지 말고 구분해보기
data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    is.na(edate1) == F ~ edate1, 
    # is.na(edate2) == F ~ edate2, 
    # is.na(edate3) == F ~ edate3, 
    # is.na(edate4) == F ~ edate4, 
    # is.na(edate5) == F ~ edate5, 
    # is.na(edate6) == F ~ edate6, 
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count
  
  # dplyr::filter(is.na(crp) == F) %>% 
  # count() # number of observation with non-zero cpr value

data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    # is.na(edate1) == F ~ edate1, 
     is.na(edate2) == F ~ edate2, 
    # is.na(edate3) == F ~ edate3, 
    # is.na(edate4) == F ~ edate4, 
    # is.na(edate5) == F ~ edate5, 
    # is.na(edate6) == F ~ edate6, 
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count

data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    # is.na(edate1) == F ~ edate1, 
    # is.na(edate2) == F ~ edate2, 
    is.na(edate3) == F ~ edate3,
    # is.na(edate4) == F ~ edate4, 
    # is.na(edate5) == F ~ edate5, 
    # is.na(edate6) == F ~ edate6, 
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count

data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    # is.na(edate1) == F ~ edate1, 
    # is.na(edate2) == F ~ edate2, 
    # is.na(edate3) == F ~ edate3, 
    is.na(edate4) == F ~ edate4,
    # is.na(edate5) == F ~ edate5, 
    # is.na(edate6) == F ~ edate6, 
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count

data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    # is.na(edate1) == F ~ edate1, 
    # is.na(edate2) == F ~ edate2, 
    # is.na(edate3) == F ~ edate3, 
    # is.na(edate4) == F ~ edate4, 
    is.na(edate5) == F ~ edate5,
    # is.na(edate6) == F ~ edate6, 
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count


data %>%
  mutate(index = seq(1, nrow(data), 1)) %>% 
  group_by(cohort) %>% 
  mutate(edate = edate0) %>% 
  mutate(edate_after = case_when(
    # is.na(edate1) == F ~ edate1, 
    # is.na(edate2) == F ~ edate2, 
    # is.na(edate3) == F ~ edate3, 
    # is.na(edate4) == F ~ edate4, 
    # is.na(edate5) == F ~ edate5, 
    is.na(edate6) == F ~ edate6,
    TRUE ~ 0)) %>% 
  select(index, RID, cohort, edate, edate_after, crp) %>%
  # count() # baseline count
  
  dplyr::filter(edate_after != 0) %>%
  count() # follow-up count
```
