

```r
library(tidyverse)
library(lubridate)

# guide : https://googledrive.tidyverse.org/
# https://rpubs.com/Evan_Jung/rgoogledrive
install.packages("googledrive")
library(googledrive)
drive_auth()
data_in_drive <- drive_find(type = "csv", pattern = "Measurement")


for(i in 1:4){ 
  drive_download(file = data_in_drive$name[i], path = data_in_drive$name[i], overwrite = TRUE)
}


Measurement_info <- read_csv("Measurement_info.csv")
Measurement_summary <- read_csv("Measurement_summary.csv")
Measurement_station_info <- read_csv("Measurement_station_info.csv")
Measurement_item_info <- read_csv("Measurement_item_info.csv")


unique(Measurement_info$`Station code`) # 25개의 station이 존재. 
unique(Measurement_info$`Item code`) # 각 station마다 6개의 item이 존재. 

# 따라서 Measurement_info의 nrow는 3 * 365 * 24 * 25 * 6 = 3942000이어야 하...는데?

length(Measurement_info$`Measurement date`) # 3885066
length(unique(Measurement_info$`Measurement date`)) # 25906

# 그러나 Measurement_info의 행 개수는 3885066이다. 
# 같은 hour를 갖는 중복치를 모두 제외해봐도 25906개로 != 3 * 365 * 24 = 26280에 못미친다.  
# 이 말인즉슨, Measurement_info에는 날짜와 시간에 빠진 observation이 존재한다는 것.

Measurement_info %>% 
  dplyr::filter(grepl("2017", `Measurement date`)) %>% 
  select(`Measurement date`) %>% 
  unique() %>% 
  nrow() # 8760 = 365 * 24

Measurement_info %>% 
  dplyr::filter(grepl("2018", `Measurement date`)) %>% 
  select(`Measurement date`) %>% 
  unique() %>% 
  nrow() # 8760 = 365 * 24

Measurement_info %>% 
  dplyr::filter(grepl("2019", `Measurement date`)) %>% 
  select(`Measurement date`) %>% 
  unique() %>% 
  nrow() # 8386 != 365 * 24

Measurement_info %>% 
  dplyr::filter(grepl("2019", `Measurement date`)) %>% 
  select(`Measurement date`) %>% 
  mutate(month = month(`Measurement date`)) %>% 
  mutate(day = day(`Measurement date`)) %>% 
  count(month, day) %>%  # 355 x 3
  dplyr::filter(n != 3600) %>% as.data.frame() # 28

# 2019년 기록은 365일이 아니라 355일로 이뤄져 있다.
# 355 * 24 = 8520  != 8386이므로 355일 중에서도 빠진 "시간"이 존재한다. 

# 2017년과 18년은 365일 모두 기록되어 있다. 
Measurement_info %>%
  dplyr::filter(grepl("2017", `Measurement date`)) %>%
  select(`Measurement date`) %>%
  mutate(month = month(`Measurement date`)) %>%
  mutate(day = day(`Measurement date`)) %>%
  count(month, day) %>% # 365 x 3
  dplyr::filter(n != 3600) # 0

Measurement_info %>% 
  dplyr::filter(grepl("2018", `Measurement date`)) %>% 
  select(`Measurement date`) %>% 
  mutate(month = month(`Measurement date`)) %>%
  mutate(day = day(`Measurement date`)) %>%
  count(month, day) %>% # 365 x 3
  dplyr::filter(n != 3600) # 0

# 어떤 station에서 observation이 누락되었는지 알아보자. 
# Measurement_summary에서 모든 station에서 누락된 observation이 없다면 1년 동안의 observation 개수는 365 * 24 * 25개이다. 
Measurement_summary %>% 
  dplyr::filter(grepl("2017", `Measurement date`)) %>% 
  group_by(`Station code`) # 219,000

Measurement_summary %>% 
  dplyr::filter(grepl("2018", `Measurement date`)) %>% 
  group_by(`Station code`) # 219,000

Measurement_summary %>% 
  dplyr::filter(grepl("2019", `Measurement date`)) %>% 
  group_by(`Station code`) # 209,511, 3489개의 observation이 없다. 
# 3489개인 이유는 애초에 2019년 dataset이 355일로 구성되어있기 때문. 

Measurement_summary %>% 
  dplyr::filter(grepl("2019", `Measurement date`)) %>% 
  group_by(`Station code`) %>% 
  mutate(month_day = str_sub(`Measurement date`, 1, 10)) %>% 
  count(month_day) %>% 
  dplyr::filter(n != 24) %>% 
  mutate(dif = 24 - `n`) %>% 
  
  #### graph part ####
  # ungroup() %>% 
  # ggplot(., aes(x = month_day, y = n)) + 
  # facet_wrap(~`Station code`, ncol = 5) + 
  # geom_point()
  
  
  summarise(sum = sum(`dif`)) %>% summarise(total_sum = sum(`sum`)) # 3489

register_google(key="API 키", write = TRUE)
seoul_map <- get_map("seoul", zoom=11, maptype="roadmap")
ggmap(seoul_map)

```
