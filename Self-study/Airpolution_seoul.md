

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


# ggmap을 이용한 관측소 표시
## ggmap 가이드 
## https://kuduz.tistory.com/1042
## https://lovetoken.github.io/r/data_visualization/2016/10/18/ggmap.html
## https://mrkevinna.github.io/R-%EC%8B%9C%EA%B0%81%ED%99%94-3/

# R에서 폰트 쓰기
font_add_google('Nanum Gothic', 'NanumGothic')
showtext_auto()

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

# R에서 폰트쓰기
# https://kuduz.tistory.com/1101
# https://blog.jongbin.com/2016/12/ggplot2-korean-font/
# https://danbi-ncsoft.github.io/etc/2018/07/24/use-your-font-in-r.html
# install.package("extrafont")
# install.package("showtext")

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
##### 2. EDA ####
# https://www.kaggle.com/mateuscco/air-pollution-in-seoul-eda-with-maps
```
