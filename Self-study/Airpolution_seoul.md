

```r
# kaggle page
# https://www.kaggle.com/bappekim/air-pollution-in-seoul/kernels

library(raster) # 행정구역 구분을 위한 package
library(tidyverse)
library(lubridate)
library(ggmap)
library(rgdal)
library(googledrive)
library(extrafont)
library(showtext)
library(container)
library(pheatmap)
library(reshape2)
library(viridis)
library(BBmisc)
library(heatmaply)

# R에서 폰트쓰기
# https://kuduz.tistory.com/1101
# https://blog.jongbin.com/2016/12/ggplot2-korean-font/
# https://danbi-ncsoft.github.io/etc/2018/07/24/use-your-font-in-r.html

font_add_google('Nanum Gothic', 'NanumGothic')
font_add_google("Gochi Hand", "gochi") 
font_add_google("Do Hyeon", "BMDOHYEON")
font_add_google("Jua", "BMJua")
font_add_google("Yeon Sung", "BMYeonSung")
showtext_auto()

# guide : https://googledrive.tidyverse.org/
# https://rpubs.com/Evan_Jung/rgoogledrive
# install.packages("googledrive")
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


# google map API 등록
register_google(key="API 키", write = TRUE)


#### TASK 1. ggmap을 이용해 오염도를 지도에 표시하기 ####
# ggmap을 이용한 관측소 표시
## ggmap 가이드 
## https://kuduz.tistory.com/1042
## https://lovetoken.github.io/r/data_visualization/2016/10/18/ggmap.html
## https://mrkevinna.github.io/R-%EC%8B%9C%EA%B0%81%ED%99%94-3/

# 목표 : https://www.kaggle.com/bappekim/visualizing-the-location-of-station-using-folium
ggmap(get_map("seoul", zoom=11, maptype="roadmap")) +
  # Q. 행정구역을 따로 표시하고 싶은데 어떻게 하지? 
  # geom_polygon(data=korea[korea$NAME_1 == "Seoul", ], aes(x=long, y=lat, group=group), fill='white', color='black')
  # overlapping 문제 때문에 polygon을 위쪽으로 옮김
  geom_polygon(data=seoul_data, aes(x=long, y=lat, group=group), fill='white', color='blue', alpha = 0.5) +
  geom_point(data = Measurement_station_info, mapping = aes(x = Longitude, y = Latitude),
             shape = '▼',
             color = 'black',
             size = 6) + # '▼'모양으로 station 위치 표시
  geom_text(data = Measurement_station_info, aes(x = Longitude, y = Latitude, label = `Station name(district)`),
            color = 'black',
            hjust = 0.5,
            vjust = -1.0,
            size = 2.5,
            fontface = 'bold',
            family = 'NanumGothic') # station의 이름 표시('구'를 기준으로 위치하고 있다) 




# 서울의 행정구역을 표시해보기
## raster package를 이용해 한국의 행정구역 받기
korea <- getData('GADM', country='kor', level=2)
ggplot() + geom_polygon(data=korea[korea$NAME_1 == "Seoul", ], aes(x=long, y=lat, group=group), fill='white', color='black') 
## 뭉개진 것처럼 나온다. 

# http://www.gisdeveloper.co.kr/?p=2332에서 시군구 geo dataset을 받음. 
geo_data <- shapefile('.../SIG.shp')

## geo_data[1:25, ] : 서울의 행정구역, 위도랑 경도가 이상한데? 
ggplot() + geom_polygon(data=geo_data[1:25, ], aes(x=long, y=lat, group=group), fill='white', color='black')

## 위치정보를 표시하는 형식으로 geo_data는 GRS80을 사용하고 있다. 
## 그러나 우리가 아는 보편적인 위도경도의 형식은 WGS84이므로 
## GRS80을 WGS84로 변환해줘야 한다. 
# 참고 : https://m.blog.naver.com/PostView.nhn?blogId=hss2864&logNo=221645854030&proxyReferer=https:%2F%2Fwww.google.com%2F
seoul_data <- spTransform(geo_data[1:25, ], CRS("+proj=longlat +ellps=WGS84 + datum=WGS84 +no_efs"))

## 제대로 나오는 것을 확인
ggplot() + geom_polygon(data=seoul_data, aes(x=long, y=lat, group=group), fill='white', color='black')

# 공기오염도에 따라 "shape"의 색깔 바꿔보기
## 각 item의 오염도 기준
Measurement_item_info

## 시간대별 관측소의 공기오염도
Measurement_summary[, c("SO2", "NO2", "O3", "CO", "PM10", "PM2.5")]

# 각 factor에 따라 공기오염도의 기준을 불러오는 함수
get_criteria <- function(Measurement_item_info, item) { 
  criteria <- Measurement_item_info[Measurement_item_info[, "Item name"] == item, 4:7]
  return(criteria)
}

# 공기오염도의 기준에 따라 색깔을 지정해주는 함수
Color <- function(dataset, Measurement_item_info, item){ 
  polution_factor <- names(dataset)[grepl("[0-9]$|O$", item)]
  get_criteria <- get_criteria(Measurement_item_info, item)
  
  a <- ifelse(dataset[, item] <= as.numeric(get_criteria[1]), "blue",
              ifelse(dataset[, item] <= as.numeric(get_criteria[2]), "green",
                     ifelse(dataset[, item] <= as.numeric(get_criteria[3]), "yellow", "red")
              )
  )
  return(a)
}

seoul_roadmap <- get_map("seoul", zoom=11, maptype="roadmap")

# 지도를 그려주는 함수
seoul_map <- function(dataset, Measurement_item_info, Measurement_station_info, seoul_data, item, ymd_hms){ 
  
  get_criteria <- function(Measurement_item_info, item) { 
    criteria <- Measurement_item_info[Measurement_item_info[, "Item name"] == item, 4:7]
    return(criteria)
  }
  
  Color <- function(dataset, Measurement_item_info, item){ 
    polution_factor <- names(dataset)[grepl("[0-9]$|O$", item)]
    get_criteria <- get_criteria(Measurement_item_info, item)
    
    a <- ifelse(dataset[, item] <= as.numeric(get_criteria[1]), "blue",
                ifelse(dataset[, item] <= as.numeric(get_criteria[2]), "green",
                       ifelse(dataset[, item] <= as.numeric(get_criteria[3]), "orange", "red")
                )
    )
    return(a)
  }
  
  dataset %>% 
    mutate_at(vars(matches(item)), funs(Color = Color(dataset[, item], Measurement_item_info, item))) %>% 
    dplyr::filter(`Measurement date` == ymd_hms(ymd_hms)) -> dataset
    
  Measurement_station_info <- Measurement_station_info %>%
    mutate(`Station name(district, 한글)` = c("종로구", "중구", "용산구", "은평구", "서대문구", "마포구", "성동구", "광진구", "동대문구",
                                            "중랑구", "성북구", "강북구", "도봉구", "노원구", "양천구", "강서구", "구로구", "금천구",
                                            "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"))
  
  title <- paste0(ymd_hms," ", item, " 상황")
  
  map <- ggmap(seoul_roadmap) +
    geom_polygon(data=seoul_data, aes(x=long, y=lat, group = group), fill='white', color='blue', alpha = 0.5) +
    geom_point(data = dataset, mapping = aes(x = Longitude, y = Latitude),
               shape = '▼',
               color = dataset$Color,
               size = 25) + # '▼'모양으로 station 위치 표시
    geom_text(data = Measurement_station_info, aes(x = Longitude, y = Latitude, label = `Station name(district, 한글)`),
              color = 'black',
              hjust = 0.5,
              vjust = -1.3,
              size = 8,
              fontface = 'bold',
              family = 'NanumGothic') +  # station의 이름 표시('구'를 기준으로 위치하고 있다) 
    ggtitle(title) + 
    theme(plot.title = element_text(family = "NanumGothic", face = "bold", size = 20))
  
  return(map)
}

# per hour의 기준으로 지도를 반복해서 그려주는 함수
generate_png_per_hour <- function(from, to) { 
  time <- seq.POSIXt(from = as.POSIXct(from), to = as.POSIXct(to), by = "hour")
  time <- time[-length(time)]
  
  for( i in 1:length(time)){ 
    a <- format(time[i], '%Y-%m-%d %H:%M:%S')
    seoul_map(Measurement_summary, Measurement_item_info, Measurement_station_info, seoul_data, item = "PM10", a)
    ggsave(file=paste0(format(time[i], '%Y-%m-%d'), "_", i, "_PM10", ".png"))
  }
}

```

```r
#### TASK 2. EDA(Explanatory Data Analysis) ####
# https://www.kaggle.com/mateuscco/air-pollution-in-seoul-eda-with-maps
Measurement_summary
Measurement_info
Measurement_station_info

Measurement_summary %>% 
  dplyr::filter(grepl("2017", `Measurement date`)) %>% dim() # 219000     11

Measurement_summary %>% 
  dplyr::filter(grepl("2018", `Measurement date`)) %>% dim() # 219000     11

Measurement_summary %>% 
  dplyr::filter(grepl("2019", `Measurement date`)) %>% dim() # 209511(-9489)     11

# 1. 2019년에 각 station별로 빠진 날짜와 시간 살펴보기

length(seq.POSIXt(from = as.POSIXct("2019-01-01"), to = as.POSIXct("2020-01-01"), by = "hour")[-1]) * 25

time_index <- seq.POSIXt(from = as.POSIXlt("2019-01-01", tz = "UTC"), to = as.POSIXlt("2020-01-01", tz = "UTC"), by = "hour")[-8761]
time_2019 <- Measurement_summary$`Measurement date`[grepl("2019", Measurement_summary$`Measurement date`)]

## 25개의 station의 2019년도 기록을 불러오기 위한 함수
time_2019 <- function(Measurement_summary) { 
  
  # 2020-01-01을 제외한 19년도의 time stamp(1시간 단위)
  time_index <- seq.POSIXt(from = as.POSIXlt("2019-01-01", tz = "UTC"), to = as.POSIXlt("2020-01-01", tz = "UTC"), by = "hour")[-8761]
  
  Measurement_summary %>% 
    dplyr::filter(grepl("2019", `Measurement date`)) %>% 
    dplyr::select(`Station code`, `Measurement date`) -> station_date
  
  result <- as.character(time_index)
  
  for( i in 1 : 25) { 
    print(i)
    
    j <- 100+i
    a <- as.character(station_date$`Measurement date`[station_date$`Station code` == j])
    result <- cbind(result, a)
    
    result[, i][which(duplicated(result[, i]))] <- NA
  }
  result <- as.data.frame(result)
  names(result) <- c("index", paste(seq(101, 125, 1)))
  
  a <- list()
  
  for( i in 1 : 25) { 
    a[[i]] <- c(result[, 1], result[, i+1])[-which(c(duplicated(c(result[, 1], result[, i+1]), fromLast = T) | duplicated(c(result[, 1], result[, i+1]))))]  
  }
  names(a) <- paste(seq(101, 125, 1))
  b <- list(result, a)
  
  return(b)
}

time_2019_station <- time_2019(Measurement_summary)
str(time_2019_station[[1]]) # 각각의 station에 등록된 시간들
str(time_2019_station[[2]]) # 각각의 station에서 누락된 시간들


## 각 station별로 2019년에 빠진 시간의 개수
time_2019_station[[1]] %>% 
  summarise_all(funs(sum(is.na(.))))


## Measurement_info에 장비 상태(Instrument status)가 존재한다. 
Measurement_info %>% 
  mutate(`Instrument status` = 
           case_when(
             `Instrument status` == 0 ~ "Normal", 
             `Instrument status` == 1 ~ "Need for calibration", 
             `Instrument status` == 2 ~ "Abnormal", 
             `Instrument status` == 4 ~ "Power cut off", 
             `Instrument status` == 8 ~ "Under repair", 
             `Instrument status` == 9 ~ "abnormal data", 
           )
  ) -> Measurement_info


Measurement_info %>% 
  group_by(`Station code`) %>% 
  count(`Instrument status`) %>%
  dplyr::filter(`Instrument status` != "Normal") %>% # normal 제외하고 보기 위한 코드
  ungroup() %>% 
  ggplot(aes(x = `Instrument status`, y = n, fill = `Instrument status`)) + 
  geom_bar(stat = "identity") + 
  coord_flip() + 
  facet_wrap(facets = `Station code` ~., ncol = 5) 
  
# 1. dataset 준비
# mutate_at에 실패한 함수, level 
level = function(x) {
  # 들어온 column의 name과 Item name를 비교. 일치하는 자리 찾기 
  index <- which(names(x) == Measurement_item_info$`Item name`)
  # 알맞은 pollution factor의 criteria를 정의 
  criteria <- Measurement_item_info[index, 4:7]
  # pollution factor의 value와 criteria를 비교해서 leveling
  a <- ifelse(x <= as.numeric(criteria[1]), "Good", 
              ifelse(x <= as.numeric(criteria[2]), "Normal",
                     ifelse(x <= as.numeric(criteria[3]), "Bad", "Very bad")
              )
  )
  return(a)
}


Measurement_info %>% 
  mutate(`Station code` = 
           case_when(
             `Station code` == 101 ~ Measurement_station_info$`Station name(district)`[1], 
             `Station code` == 102 ~ Measurement_station_info$`Station name(district)`[2], 
             `Station code` == 103 ~ Measurement_station_info$`Station name(district)`[3], 
             `Station code` == 104 ~ Measurement_station_info$`Station name(district)`[4], 
             `Station code` == 105 ~ Measurement_station_info$`Station name(district)`[5], 
             `Station code` == 106 ~ Measurement_station_info$`Station name(district)`[6], 
             `Station code` == 107 ~ Measurement_station_info$`Station name(district)`[7], 
             `Station code` == 108 ~ Measurement_station_info$`Station name(district)`[8], 
             `Station code` == 109 ~ Measurement_station_info$`Station name(district)`[9], 
             `Station code` == 110 ~ Measurement_station_info$`Station name(district)`[10], 
             `Station code` == 111 ~ Measurement_station_info$`Station name(district)`[11], 
             `Station code` == 112 ~ Measurement_station_info$`Station name(district)`[12], 
             `Station code` == 113 ~ Measurement_station_info$`Station name(district)`[13], 
             `Station code` == 114 ~ Measurement_station_info$`Station name(district)`[14], 
             `Station code` == 115 ~ Measurement_station_info$`Station name(district)`[15], 
             `Station code` == 116 ~ Measurement_station_info$`Station name(district)`[16], 
             `Station code` == 117 ~ Measurement_station_info$`Station name(district)`[17], 
             `Station code` == 118 ~ Measurement_station_info$`Station name(district)`[18], 
             `Station code` == 119 ~ Measurement_station_info$`Station name(district)`[19], 
             `Station code` == 120 ~ Measurement_station_info$`Station name(district)`[20], 
             `Station code` == 121 ~ Measurement_station_info$`Station name(district)`[21], 
             `Station code` == 122 ~ Measurement_station_info$`Station name(district)`[22], 
             `Station code` == 123 ~ Measurement_station_info$`Station name(district)`[23], 
             `Station code` == 124 ~ Measurement_station_info$`Station name(district)`[24], 
             `Station code` == 125 ~ Measurement_station_info$`Station name(district)`[25]
           )
  ) %>% 
  mutate(`Instrument status` =
           case_when(
             `Instrument status` == 0 ~ "Normal",
             `Instrument status` == 1 ~ "Need for calibration",
             `Instrument status` == 2 ~ "Abnormal",
             `Instrument status` == 4 ~ "Power cut off",
             `Instrument status` == 8 ~ "Under repair",
             `Instrument status` == 9 ~ "abnormal data",
           )
  ) %>%
  mutate(`Item code` = 
           case_when(
             `Item code` == 1 ~ "SO2", 
             `Item code` == 3 ~ "NO2", 
             `Item code` == 5 ~ "CO", 
             `Item code` == 6 ~ "O3", 
             `Item code` == 8 ~ "PM10",
             `Item code` == 9 ~ "PM2.5"
           )
  ) %>% 
  
  # pivot_wider를 이용해 Item code를 column으로 뿌려주고 그에 맞는 Average value을 할당해준다. 
  # https://stackoverflow.com/questions/57993552/r-tidyr-mutate-and-spread-multiple-columns
  pivot_wider(
    names_from = `Item code`,
    values_from = `Average value`
  ) %>% 
  # 모든 pollution factor들을 한번에 각각의 criteria에 따라 leveling할 수 있을까? 
  # mutate_at(vars(`SO2`:PM2.5), funs(level = level)) # 실패
  mutate(`SO2_level` = 
           case_when (
             `SO2` <= as.numeric(Measurement_item_info[1, 4]) ~ "Good", 
             `SO2` <= as.numeric(Measurement_item_info[1, 5]) ~ "Normal",
             `SO2` <= as.numeric(Measurement_item_info[1, 6]) ~ "Bad",
             `SO2` <= as.numeric(Measurement_item_info[1, 7]) ~ "Very bad"
           )
  ) %>% 
  mutate(`NO2_level` = 
           case_when (
             `NO2` <= as.numeric(Measurement_item_info[2, 4]) ~ "Good", 
             `NO2` <= as.numeric(Measurement_item_info[2, 5]) ~ "Normal",
             `NO2` <= as.numeric(Measurement_item_info[2, 6]) ~ "Bad",
             `NO2` <= as.numeric(Measurement_item_info[2, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`CO_level` = 
           case_when (
             `CO` <= as.numeric(Measurement_item_info[3, 4]) ~ "Good", 
             `CO` <= as.numeric(Measurement_item_info[3, 5]) ~ "Normal",
             `CO` <= as.numeric(Measurement_item_info[3, 6]) ~ "Bad",
             `CO` <= as.numeric(Measurement_item_info[3, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`O3_level` = 
           case_when (
             `O3` <= as.numeric(Measurement_item_info[4, 4]) ~ "Good", 
             `O3` <= as.numeric(Measurement_item_info[4, 5]) ~ "Normal",
             `O3` <= as.numeric(Measurement_item_info[4, 6]) ~ "Bad",
             `O3` <= as.numeric(Measurement_item_info[4, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`PM10_level` = 
           case_when (
             `PM10` <= as.numeric(Measurement_item_info[5, 4]) ~ "Good", 
             `PM10` <= as.numeric(Measurement_item_info[5, 5]) ~ "Normal",
             `PM10` <= as.numeric(Measurement_item_info[5, 6]) ~ "Bad",
             `PM10` <= as.numeric(Measurement_item_info[5, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`PM2.5_level` = 
           case_when (
             `PM2.5` <= as.numeric(Measurement_item_info[6, 4]) ~ "Good", 
             `PM2.5` <= as.numeric(Measurement_item_info[6, 5]) ~ "Normal",
             `PM2.5` <= as.numeric(Measurement_item_info[6, 6]) ~ "Bad",
             `PM2.5` <= as.numeric(Measurement_item_info[6, 7]) ~ "Very bad"
           )
  ) %>% 
  mutate(`Year` = year(`Measurement date`)) %>% 
  mutate(`Month` = month(`Measurement date`)) %>%
  mutate(`Day` = day(`Measurement date`)) %>% 
  mutate(`Hour` = hour(`Measurement date`)) %>% 
  rename(`Date` = `Measurement date`, 
         `Station` = `Station code`, 
         `Status` = `Instrument status`) -> Measurement_info

  
Measurement_info %>% 
  summarise_each(funs(sum(is.na(.)))) %>% as.data.frame() # 각 column별로 NA 개수 확인

paste0('Fist date is ', format(head(Measurement_info$Date, 1), '%Y-%m-%d %H:%M:%S'))
paste0('Last date is ', format(tail(Measurement_info$Date, 1), '%Y-%m-%d %H:%M:%S'))

# 2. Exploratory analysis
## 2.1 Status에 따라 나누기
Measurement_info %>% 
  dplyr::filter(`Status` != "Normal") -> bad_measure

Measurement_info %>% 
  dplyr::filter(`Status` == "Normal") -> normal_measure

normal_measure %>% 
  group_by(`Date`) %>% 
  summarise_at(vars(3:8), funs(mean(., na.rm = T))) %>% 
  mutate(`SO2_level` = 
           case_when (
             `SO2` <= as.numeric(Measurement_item_info[1, 4]) ~ "Good", 
             `SO2` <= as.numeric(Measurement_item_info[1, 5]) ~ "Normal",
             `SO2` <= as.numeric(Measurement_item_info[1, 6]) ~ "Bad",
             `SO2` <= as.numeric(Measurement_item_info[1, 7]) ~ "Very bad"
           )
  ) %>% 
  mutate(`NO2_level` = 
           case_when (
             `NO2` <= as.numeric(Measurement_item_info[2, 4]) ~ "Good", 
             `NO2` <= as.numeric(Measurement_item_info[2, 5]) ~ "Normal",
             `NO2` <= as.numeric(Measurement_item_info[2, 6]) ~ "Bad",
             `NO2` <= as.numeric(Measurement_item_info[2, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`CO_level` = 
           case_when (
             `CO` <= as.numeric(Measurement_item_info[3, 4]) ~ "Good", 
             `CO` <= as.numeric(Measurement_item_info[3, 5]) ~ "Normal",
             `CO` <= as.numeric(Measurement_item_info[3, 6]) ~ "Bad",
             `CO` <= as.numeric(Measurement_item_info[3, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`O3_level` = 
           case_when (
             `O3` <= as.numeric(Measurement_item_info[4, 4]) ~ "Good", 
             `O3` <= as.numeric(Measurement_item_info[4, 5]) ~ "Normal",
             `O3` <= as.numeric(Measurement_item_info[4, 6]) ~ "Bad",
             `O3` <= as.numeric(Measurement_item_info[4, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`PM10_level` = 
           case_when (
             `PM10` <= as.numeric(Measurement_item_info[5, 4]) ~ "Good", 
             `PM10` <= as.numeric(Measurement_item_info[5, 5]) ~ "Normal",
             `PM10` <= as.numeric(Measurement_item_info[5, 6]) ~ "Bad",
             `PM10` <= as.numeric(Measurement_item_info[5, 7]) ~ "Very bad"
           )
  ) %>%
  mutate(`PM2.5_level` = 
           case_when (
             `PM2.5` <= as.numeric(Measurement_item_info[6, 4]) ~ "Good", 
             `PM2.5` <= as.numeric(Measurement_item_info[6, 5]) ~ "Normal",
             `PM2.5` <= as.numeric(Measurement_item_info[6, 6]) ~ "Bad",
             `PM2.5` <= as.numeric(Measurement_item_info[6, 7]) ~ "Very bad"
           )
  ) -> overview_measure

## 2.3  overview_measure의 box plot 그리기 
overview_measure %>%
  select(2:7) %>% 
  gather(key = "key", value = "value") %>% 
  # mutate(key = factor(key, levels=c('SO2', 'NO2', 'CO', 'O3', 'PM10', 'PM2.5'))) %>% 
  mutate(key = factor(key, levels=unique(key))) %>% 
  ggplot(aes(y = value)) + 
  geom_boxplot(fill='#56B4E9') + 
  facet_wrap( ~ key, ncol = 6, scales = "free") + 
  ggtitle('Distribution of pollutants') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

## 2.4  overview_measure의 summary statistics table
overview_measure %>% 
  select(2:7) %>% 
  gather(key = "key", value = "value") %>% 
  group_by(key) %>% 
  # https://stackoverflow.com/questions/30488389/using-dplyr-window-functions-to-calculate-percentiles
  # https://stackoverflow.com/questions/53787714/dplyr-summarise-all-with-quantile-and-other-functions
  summarise_at(vars(value), funs(min, max, mean, sd, 
                                 quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))))) %>%
  unnest(cols = c(quantile)) %>% 
  # https://stackoverflow.com/questions/34004008/transposing-in-dplyr : gather, spread를 이용한 transpose
  # gather(variable, summary_stat, min:`75%`) %>%
  # spread(key, summary_stat) %>%

  # https://stackoverflow.com/questions/47126197/how-to-transpose-t-in-the-tidyverse-using-tidyr : pivot을 이용한 transpose
  pivot_longer(min:`75%`, "variable", "value") %>% 
  pivot_wider(variable, key) %>% 
  select(variable, SO2, NO2, CO, O3, PM10, PM2.5) %>% 
  arrange(factor(variable, 
                 levels = c('min', 'max', 'mean', 'sd', '25%', '50%', '75%')))


## 2.5 overview_measure의 pollution level의 stacked bar plot 
overview_measure %>%
  select(8:13) %>% 
  pivot_longer(1:6, 'variable', 'value') %>% 
  # https://stringr.tidyverse.org/reference/str_replace.html : 문자 value의 특정 부분만 replace
  mutate_at(vars(variable), ~str_replace(., "_", " ")) %>% 
  group_by(variable) %>% 
  dplyr::count(value) %>% 
  ggplot(aes(x = variable, y = n, fill = value)) + 
  geom_bar(stat="identity", position = "stack") + 
  ggtitle('Levels of pollution in Seoul from 2017 to 2019') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  theme(legend.title = element_blank()) + 
  # http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
  # https://stackoverflow.com/questions/51272689/ggplot2-how-to-change-the-order-of-a-legend : legend의 label reordering 
  scale_fill_manual(breaks=c("Good","Normal", "Bad", "Very bad"),
                    values=c("steelblue3", "springgreen3", "sienna2", "red3"), 
                    labels=c("Good","Normal", "Bad", "Very bad")) + 
  labs(x="Pollutants", y="Stacked n")


## 2.6 Does pollutants have correlation?
# Get upper triangle of the correlation matrix
get_upper_tri <- function(cormat){
  cormat[lower.tri(cormat)]<- NA
  return(cormat)
}

round(cor(na.omit(normal_measure[, 4:9])), 2) %>% 
  get_upper_tri() %>% 
  melt() %>% 
  ggplot(aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile() + 
  # http://www.sthda.com/english/wiki/ggplot2-quick-correlation-matrix-heatmap-r-software-and-data-visualization
  geom_text(aes(Var1, Var2, label = value), color = "white", size = 4) +
  # https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html
  # https://www.r-graph-gallery.com/79-levelplot-with-ggplot2.html
  scale_fill_viridis(option = "magma", discrete=FALSE) + 
  ggtitle('Correlation between Pollutants') + 
  # https://stackoverflow.com/questions/35090883/remove-all-of-x-axis-labels-in-ggplot
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.title.x=element_blank(),
        axis.title.y=element_blank())


## 2.7 How pollutant concentrations varies with location?
na.omit(normal_measure) %>% 
  select(c(2, 4:9)) %>%
  group_by(Station) %>% 
  summarise_at(vars(1:6), funs(mean)) -> district_pol # 신기하네. column 7 개로 나오는데 2:7하면 7은 없는 자리라고 에러난다. 
  
  
district_pol %>% 
  # https://stackoverflow.com/questions/15215457/standardize-data-columns-in-r : 와-우
  mutate_at(vars(2:7), ~(scale(.) %>% as.vector)) %>% 
  column_to_rownames(var = "Station") %>% 
  pheatmap(., cluster_rows = FALSE, cluster_cols = FALSE, 
           color = YlGnBu(10), border_color = FALSE, angle_col = 0)

## 2.8 What really happened on that December 11th? : 19년 12월 11일에 갑자기 증가한 미세먼지 농도에 대하여
overview_measure %>% 
  dplyr::filter(`Date` == as.POSIXlt("2019-12-11 10:00:00", tz = "UTC")) -> reported_day_morning

overview_measure %>% 
  dplyr::filter(`Date` == as.POSIXlt("2019-12-11 22:00:00", tz = "UTC")) -> reported_day_night

normal_measure %>% 
  group_by(Station) %>% 
  dplyr::filter(`Date` == as.POSIXlt("2019-12-11 10:00:00", tz = "UTC"))

normal_measure %>% 
  group_by(Station) %>% 
  dplyr::filter(`Date` == as.POSIXlt("2019-12-11 22:00:00", tz = "UTC"))

overview_measure %>% 
  dplyr::filter(`Date` >= as.POSIXlt("2019-12-01", tz = "UTC")) %>% 
  select(c(1, 2:7)) %>% 
  pivot_longer(-Date, "variable", "value") %>%
  # https://stackoverflow.com/questions/14262497/fixing-the-order-of-facets-in-ggplot
  # facet_wrap에서의 ordering 고정
  mutate(variable = factor(variable, levels=unique(variable))) %>% 
  ggplot(aes(x = Date, y = value)) + 
  geom_path(aes(group = 1), colour = "steelblue3") + 
  # geom_point() + 
  facet_wrap(facets = `variable` ~., nrow = 6, scales = "free_y") + 
  ggtitle('Pollutant concentrations on December 2019') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  labs(x="Date in december 2019", y="Polluntants value") + 
  theme_minimal()

## 2.9 Does the concentration of pollutants have seazonality and tendency? (to be expanded) 
normal_measure %>% 
  group_by(Hour) %>% 
  select(4:9) %>% 
  summarise_at(1:6, funs(mean(., na.rm = T))) %>% 
  pivot_longer(-Hour, "variable", "value") %>% 
  # facet_wrap에서의 ordering 고정
  mutate(variable = factor(variable, levels=unique(variable))) %>% 
  ggplot(aes(x = Hour, y = value)) + 
  geom_path(aes(group = 1), colour = "springgreen3") + 
  facet_wrap(facets = `variable` ~ . , nrow = 6, scales = "free_y") + 
  ggtitle('Pollutant concentrations along the day') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  labs(x="Hours", y="Polluntants value") + 
  theme_minimal()

normal_measure %>% 
  mutate(`Date` = format(`Date`, "%Y-%m-%d")) %>% 
  group_by(`Date`) %>% 
  select(4:9) %>% 
  summarise_at(1:6, funs(mean(., na.rm = T))) %>% 
  pivot_longer(-Date, "variable", "value") %>% 
  # facet_wrap에서의 ordering 고정
  mutate(variable = factor(variable, levels=unique(variable))) %>% 
  
  ggplot(aes(x = Date, y = value)) + 
  geom_path(aes(group = 1), colour = "sienna2") + 
  # https://cran.r-project.org/web/packages/lemon/vignettes/facet-rep-labels.html : x축 눈금 없애기
  facet_wrap(facets = `variable` ~ . , nrow = 6, scales = "free_y") + 
  ggtitle('Pollutant concentrations along the years') + 
  scale_x_discrete(breaks=c("2017-01-01", "2017-05-01", "2017-09-01",
                              "2018-01-01", "2018-05-01", "2018-09-01",
                              "2019-01-01", "2019-05-01", "2019-09-01", "2019-12-01")) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) +
  labs(x="Date", y="Polluntants value") + 
  theme_minimal()


## 2.10 Appendix
### 2.10.1 What happens when an instrument doesn't work properly?

Measurement_info %>% 
  dplyr::count(`Status`) %>% 
  arrange(n) %>% 
  mutate(Status = factor(Status, level = unique(Status))) %>% 
  # dplyr::filter(`Status` != "Normal") %>% # normal 제외하고 보기 위한 코드
  ggplot(aes(x = `Status`, y = n, fill = `Status`)) + 
  geom_bar(stat = "identity") + 
  coord_flip() + 
  # http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
  scale_fill_manual(breaks=c("Normal","Need for calibration", "Abnormal", "Power cut off", "Under repair", "abnormal data"),
                    values=c("chartreuse3", "sienna2", "red3", "azure3", "deepskyblue3", "firebrick4"), 
                    labels=c("Normal","Need for calibration", "Abnormal", "Power cut off", "Under repair", "abnormal data")) + 
  ggtitle('Distribution of status values') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) +
  labs(x="Station status", y="Occurrence") + 
  theme_minimal()


Measurement_info %>% 
  group_by(`Station`) %>% 
  dplyr::count(`Status`) %>%
  arrange(n) %>% 
  mutate(Status = factor(Status, level = unique(Status))) %>% 
  dplyr::filter(`Status` != "Normal") %>% # normal 제외하고 보기 위한 코드
  ungroup() %>% 
  ggplot(aes(x = `Status`, y = n, fill = `Status`)) + 
  geom_bar(stat = "identity") + 
  coord_flip() + 
  facet_wrap(facets = `Station` ~., ncol = 5, scales = "free_x") +
  scale_fill_manual(breaks=c("Need for calibration", "Abnormal", "Power cut off", "Under repair", "abnormal data"),
                    values=c("sienna2", "red3", "azure3", "deepskyblue3", "firebrick4"), 
                    labels=c("Need for calibration", "Abnormal", "Power cut off", "Under repair", "abnormal data")) + 
  ggtitle('Distribution of status values') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) +
  labs(x="Station status", y="Occurrence") + 
  theme_minimal()

### 2.10.2. Is there a pattern in when a instrument stop working?
bad_measure %>% 
  group_by(Hour) %>% 
  dplyr::count(`Status`) %>% 
  ungroup() %>% 
  pivot_wider(names_from = `Status`, values_from = `n`) %>% 
  column_to_rownames(var = "Hour") %>% 
  pheatmap(., cluster_rows = FALSE, cluster_cols = FALSE, 
           color = YlGnBu(10), border_color = FALSE, angle_col = 0, display_numbers = T, number_format = "%.0f")

Measurement_info %>% 
  dplyr::filter(Status != "Normal") %>% 
  group_by(Station) %>% 
  dplyr::count(Status) %>% 
  summarise(n = sum(n)) %>%
  arrange(n) %>% 
  mutate(Station = factor(Station, level = unique(Station))) %>% 
  ggplot(aes(x = n, y = Station, fill = Station)) + 
  geom_bar(stat = "identity") + 
    ggtitle('Amount of times that problems occured by district') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) +
  labs(x="Occurrence", y="Station") + 
  theme_minimal() + 
  theme(legend.position = "none")

bad_measure %>% 
  group_by(Station) %>% 
  dplyr::count(`Status`) %>% 
  ungroup() %>% 
  pivot_wider(names_from = `Status`, values_from = `n`) %>% 
  # https://stackoverflow.com/questions/49342097/replace-na-on-numeric-columns-with-mutate-if-and-replace-na : na값 대체하기
  mutate_if(is.numeric, replace_na, replace = 0) %>% 
  column_to_rownames(var = "Station") %>% 
  pheatmap(., cluster_rows = FALSE, cluster_cols = FALSE, 
           color = YlGnBu(10), border_color = FALSE, angle_col = 0, display_numbers = T, number_format = "%.0f")
```
