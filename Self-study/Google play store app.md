```r

library(tidyverse)
library(lubridate)
library(googledrive)
library(extrafont)
library(showtext)
library(pheatmap)
library(reshape2)
library(viridis)
library(BBmisc)
library(heatmaply)
library(forcats)


font_add_google('Nanum Gothic', 'NanumGothic')
font_add_google("Gochi Hand", "gochi") 
font_add_google("Do Hyeon", "BMDOHYEON")
font_add_google("Jua", "BMJua")
font_add_google("Yeon Sung", "BMYeonSung")
showtext_auto()


drive_auth()
data_in_drive <- drive_find(type = "csv", pattern = "googleplaystore")


for(i in 1:2){ 
  drive_download(file = data_in_drive$name[i], path = data_in_drive$name[i], overwrite = TRUE)
}


googleplaystore_user_reviews <- read_csv("googleplaystore_user_reviews.csv")
googleplaystore <- read_csv("googleplaystore.csv")

googleplaystore_user_reviews
googleplaystore %>% 
  mutate(Installs = factor(Installs, levels = c("Free", "0", "0+", "1+", "5+", "10+", "50+", "100+", "500+", 
                                                "1,000+", "5,000+", "10,000+", "50,000+", 
                                                "100,000+", "500,000+", "1,000,000+", "5,000,000+", 
                                                "10,000,000+", "50,000,000+", "100,000,000+", "500,000,000+", 
                                                "1,000,000,000+"))) -> googleplaystore

#### 1. https://www.kaggle.com/mdp1990/google-play-app-store-eda-data-visualisation ####
### 1.1 Simple work
# App with large number of reviews

googleplaystore %>% 
  arrange(desc(Reviews)) %>% 
  head(1) %>% as.data.frame()

# Paid Vs Free
googleplaystore %>% 
  dplyr::count(Type)

googleplaystore %>% 
  dplyr::filter(Type != "Free" & Type != "Paid")

# App with the largest number of installs
googleplaystore %>% 
  dplyr::filter(Installs != "Free") %>% 
  mutate_at(vars(Installs), ~str_replace(., "\\+$", "")) %>%
  mutate_at(vars(Installs), ~str_remove_all(., ",")) %>% 
  mutate(Installs = as.numeric(Installs)) %>% 
  group_by(App) %>% 
  summarise(sum = sum(Installs)) %>% 
  arrange(desc(sum)) %>% 
  ungroup() %>% 
  head(10) %>% 
  # ordering 
  mutate(App = factor(App, levels=unique(App))) %>% 
  ggplot(aes(x = App, y = sum, fill = App)) + 
  geom_bar(stat = "identity") + 
  theme_minimal() + 
  ggtitle('Top 10 Apps having Highest Installs') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Install Counts")
  
# App with the largest size
# 숫자 M, k, +와 "Varies with device"로 이뤄져 있음
# "Varies with device"를 제외하고 나머지 obs의 개수를 알아보자 
googleplaystore[which(grepl(pattern = "\\+", googleplaystore$Size)), ] %>% 
  as.data.frame() # 1개 

googleplaystore[which(grepl(pattern = "\\k", googleplaystore$Size)), ] %>% 
  as.data.frame() # 316개

googleplaystore[which(grepl(pattern = "\\M", googleplaystore$Size)), ] %>% 
  as.data.frame() # 8829개

# +제외하고 단위 맞춰주기


googleplaystore %>% 
  # https://stackoverflow.com/questions/28860069/regular-expressions-regex-and-dplyrfilter : filter에서 regex 사용하기 
  dplyr::filter(Size != "Varies with device" & !grepl("\\+$", Size)) %>% 
  mutate(KB = ifelse(grepl("k", Size), "k", "M")) %>% 
  mutate_at(vars(Size), ~str_replace(., "M", "")) %>% 
  mutate_at(vars(Size), ~str_replace(., "k", "")) %>% 
  mutate(Size = as.numeric(Size)) %>% 
  mutate(Size = ifelse(KB == "k", Size/1000, Size)) %>%
  arrange(desc(Size)) %>% 
  head(10)

# 보면 알겠지만 Size의 max가 100M라서 top rank는 다 100M임.
# Task의 largest size, 'Word Search Tab 1 FR' app은 단위가 KB라 large size 축에도 못낌

# Most Popular Category
googleplaystore %>% 
  # select(Category) %>% is.na() %>% sum() # na 없음
  dplyr::count(Category) %>% 
  arrange(desc(n)) %>% 
  head(10) %>% 
  mutate(Category = factor(Category, levels = unique(Category))) %>%
  ggplot(aes(x = Category, y = n, fill = Category)) + 
  geom_bar(stat = "identity") + 
  theme_minimal() + 
  ggtitle('Most Popular Category') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Register Counts")

# count of content Rating 
googleplaystore %>% 
  dplyr::count(`Content Rating`) %>% 
  arrange(desc(n)) %>%
  mutate(`Content Rating` = factor(`Content Rating`, levels = unique(`Content Rating`))) %>% 
  ggplot(aes(x = `Content Rating`, y = n, fill = `Content Rating`)) + 
  geom_bar(stat = "identity") + 
  theme_minimal() + 
  ggtitle('Most Popular Category') + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Register Counts")


general_bar_plot <- function(dataset, colName){ 
  variable <- enquo(`colName`)
  
  dataset %>% 
    # https://stackoverflow.com/questions/48062213/dplyr-using-column-names-as-function-arguments
    dplyr::count(!!variable) %>% 
    arrange(desc(n)) %>% 
    mutate(variable = factor(!!variable, levels = unique(!!variable))) %>% 
    # !!variable을 factorizing해서 variable로 만들었기 때문에 이후로는 variable로 쓴다
    # !!variable로 넣으면 bar ordering이 꼬임
    ggplot(aes(x = variable, y = n, fill = variable)) + 
    geom_bar(stat = "identity") + 
    theme_minimal()
  
}

general_bar_plot(googleplaystore, `Content Rating`) + 
  ggtitle("Content Rating") + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Counts")

general_bar_plot(googleplaystore, Category) + 
  ggtitle("Category") + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Counts")
  
googleplaystore %>% 
  dplyr::filter(Type != 0 & Type != NaN) %>% 
  group_by(Type, Category) %>% 
  summarise_at(vars(Rating), funs(mean(., na.rm = T), sd(., na.rm = T))) %>% 
  arrange(desc(mean)) %>% 
  mutate(Category = factor(Category, levels = unique(Category))) %>% 
  ggplot(aes(x = Category, y = mean, fill = Category)) + 
  geom_bar(stat = "identity") +
  # https://stackoverflow.com/questions/54505654/change-order-of-bars-in-ggplot : barplot의 error bar 
  geom_errorbar(aes(ymin = mean-sd, ymax = mean+sd),
                width = .2, position = position_dodge(.5))+
  facet_wrap(facets = Type ~ . , nrow = 2, scales = "free_y") + 
  # https://stackoverflow.com/questions/30280499/different-y-limits-on-ggplot-facet-grid-bar-graph : y축의 limit 설정
  coord_cartesian(ylim=c(3.5,5)) + 
  theme_minimal() + 
  ggtitle("Average Ratings by App Category") + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Average Rating")

googleplaystore %>% 
  dplyr::filter(Type != 0 & Type != NaN) %>% 
  group_by(Type, Category) %>% 
  summarise_at(vars(Rating), funs(mean(., na.rm = T))) %>% 
  arrange(desc(Rating)) %>% 
  pivot_wider(names_from = "Type", values_from = "Rating") %>% 
  drop_na() %>% 
  group_by(Category) %>% 
  mutate(diff = `Paid` - `Free`) %>% 
  arrange(desc(diff)) %>% ungroup() %>% 
  mutate(Category = factor(Category, levels = unique(Category))) %>% 
  ggplot(aes(x = Category, y = diff, fill = Category)) +
  geom_bar(stat = "identity") + 
  theme_minimal() + 
  ggtitle("Difference of Ratings between Paid and Free Apps Across App Categories") + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 90), 
        legend.position = "none") + 
  labs(x="Apps", y="Difference of Rating")
```
```r
#### 2. ML to Visualization & Prediction of App Ratings ####
# https://www.kaggle.com/rajeshjnv/ml-to-visualization-prediction-of-app-ratings  
### 1. pandas_profiling.ProfileReport(data)를 이용한 feature overview
# R에서 비슷한 기능을하는 pakcage, DataExplorer와 skimr을 이용해봤는데 이거다!라는 느낌은 없다. 
## https://cran.r-project.org/web/packages/skimr/vignettes/skimr.html
## https://cran.r-project.org/web/packages/DataExplorer/vignettes/dataexplorer-intro.html

plot_intro(googleplaystore)
plot_str(googleplaystore)
plot_missing(googleplaystore)  
skim(googleplaystore)

# NA 개수 파악
googleplaystore %>% 
  summarise_all(funs(sum(is.na(.)))) %>% as.data.frame()


# categorical variable overview
## Category
googleplaystore %>% 
  dplyr::count(`Category`, sort = T) %>% as.data.frame()

# 1.9???? 

## Type
googleplaystore %>% 
  dplyr::count(`Type`, sort = T)
# 0 : 1개. NaN : 1개

googleplaystore %>% 
  dplyr::filter(Type == "NaN") %>% as.data.frame()
## 커맨드엔컨커인데...설치된 적이 없고 리뷰도 없네? 이게 dataset 만들기 바로 직전에 나온 어플이라면?

googleplaystore %>% 
  dplyr::filter(grepl(", 2018", `Last Updated`)) %>% 
  dplyr::count(`Last Updated`, sort = F) %>% as.data.frame() 
## 그렇지도 않네? 
## Price가 0이니까 Type = Free, Reviews가 0이니까 Rating을 0으로 주자. 

## Content Rating
googleplaystore %>% 
  dplyr::count(`Content Rating`, sort = T)
# NA : 1개

## Genres
googleplaystore %>% 
  dplyr::count(`Genres`) %>% 
  arrange(n) %>% 
  as.data.frame()

## Last Updated
googleplaystore %>% 
  dplyr::count(`Last Updated`, sort = T)
# 날짜형이니까 날짜로 바꿔주는 게 좋을 것 같다. 

## Current Ver
googleplaystore %>% 
  dplyr::count(`Current Ver`, sort = T)

googleplaystore %>% 
  dplyr::filter(is.na(`Current Ver`)) %>% as.data.frame()

## Android Ver
googleplaystore %>% 
  dplyr::count(`Android Ver`, sort = T)

googleplaystore %>% 
  dplyr::filter(is.na(`Android Ver`)) %>% as.data.frame()

## Installs : 인스톨 횟수, n번 이상의 형태로 categorical variable임. 
googleplaystore %>% 
  dplyr::count(`Installs`, sort = T) %>% 
  arrange(Installs)

## Size : App 크기, 단위 MB, KB가 붙어있어 Character variable로 정의되어 있다. 단위 통일을 한 후 numeric으로 바꿔야 한다. 
googleplaystore %>% 
  dplyr::count(`Size`, sort = T)

### 1.1 Overview 결과 : 관측값 제거 및 수정
# Life Made WI-Fi Touchscreen Photo Frame apps을 보면 value들이 좀 밀려있는 것 같은 인상이 받는다. 
# Category가 1.9, Rating이 19, Size가 1,000+ 등등. 빼자. 

# Command & Conquer: Rivals와 Life Made WI-Fi Touchscreen Photo Frame를 수정한 dataset 
googleplaystore %>% 
  mutate(Rating = ifelse(App == "Command & Conquer: Rivals", 0, Rating)) %>% 
  mutate(Type = ifelse(App == "Command & Conquer: Rivals", "Free", Type)) %>% 
  dplyr::filter(App != "Life Made WI-Fi Touchscreen Photo Frame") -> googleplaystore

### 1.2 Overview 결과 : variable 변환
# Installs : 인스톨 횟수를 factor로 바꿔주자. 
googleplaystore %>% 
  mutate(Installs = factor(Installs, levels = c("Free", "0", "0+", "1+", "5+", "10+", "50+", "100+", "500+", 
                                                "1,000+", "5,000+", "10,000+", "50,000+", 
                                                "100,000+", "500,000+", "1,000,000+", "5,000,000+", 
                                                "10,000,000+", "50,000,000+", "100,000,000+", "500,000,000+", 
                                                "1,000,000,000+"))) -> googleplaystore
# Size : MB 단위로 맞춰준다. 
googleplaystore %>% 
  # https://stackoverflow.com/questions/28860069/regular-expressions-regex-and-dplyrfilter : filter에서 regex 사용하기 
  dplyr::filter(Size != "Varies with device" & !grepl("\\+$", Size)) %>% 
  mutate(KB = ifelse(grepl("k", Size), "k", "M")) %>% 
  mutate_at(vars(Size), ~str_replace(., "M", "")) %>% 
  mutate_at(vars(Size), ~str_replace(., "k", "")) %>% 
  mutate(Size = as.numeric(Size)) %>% 
  mutate(Size = ifelse(KB == "k", Size/1000, Size)) -> googleplaystore

# Last Updated : date variable로 바꾸자.
# https://stackoverflow.com/questions/36971015/mdy-lubridate-unable-to-identify-january
# 일반적인 방법의 mdy로하면 틀린 날짜가 return된다. 
googleplaystore %>% 
  mutate(`Last Updated date` = str_remove(`Last Updated`, ",")) %>% 
  mutate(`Last Updated date` = str_remove(`Last Updated date`, " ")) %>% 
  mutate(`Last Updated date` = mdy(`Last Updated date`)) -> googleplaystore


### 2. EDA
### 2.1 Piechart for "Type"
googleplaystore %>% 
  count(Type) %>% 
  mutate(n = n/9145) %>% 
  ggplot(aes(x = "", y = n, fill = Type)) + 
  geom_bar(width = 1, stat = "identity", color = "white") +
  coord_polar("y") +
  theme_void() + 
  ggtitle("Type distribution in Google play store" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  geom_text(aes(label = paste0(round(n*100,1),"%")), 
            position = position_stack(vjust = 0.5)) 

### 2.2 Line plot for "Last Updated" and "Type"
googleplaystore %>% 
  mutate(year = year(`Last Updated date`)) %>% 
  group_by(Type) %>% 
  count(year) %>% 
  ggplot(aes(x = year, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  geom_point(aes(colour = Type)) + 
  theme_minimal() + 
  # https://stackoverflow.com/questions/26195231/ggplot2-manually-specifying-colour-with-geom-line : line plot에 색깔 넣기
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Year", y="") + 
  ggtitle("App udated or added over the years" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))


### 2.3 
googleplaystore %>% 
  dplyr::filter(Type == "Free") %>% 
  mutate(month = month(`Last Updated date`)) %>% 
  count(month) %>% 
  mutate(month = factor(month)) %>% 
  ggplot(aes(x = month, y = n)) + 
  geom_bar(stat = "identity", fill = "springgreen3") + 
  theme_minimal() + 
  labs(x="Month", y="") + 
  ggtitle("Free App added over the month" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))


googleplaystore %>% 
  dplyr::filter(Type == "Paid") %>% 
  mutate(month = month(`Last Updated date`)) %>% 
  count(month) %>% 
  mutate(month = factor(month)) %>% 
  ggplot(aes(x = month, y = n)) + 
  geom_bar(stat = "identity", fill = "dodgerblue1") + 
  theme_minimal() + 
  labs(x="Month", y="") + 
  ggtitle("Paid App added over the month" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))


### 2.4 Content Rating
googleplaystore %>% 
  group_by(Type) %>% 
  count(`Content Rating`) %>% 
  ggplot(aes(x = `Content Rating`, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  geom_point(aes(colour = Type)) + 
  theme_minimal() + 
  # https://stackoverflow.com/questions/26195231/ggplot2-manually-specifying-colour-with-geom-line : line plot에 색깔 넣기
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Content Rating", y="") + 
  ggtitle("Ratings of the free vs paid app" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

googleplaystore %>% 
  dplyr::filter(Type == "Free") %>% 
  count(`Content Rating`, sort = T) %>%  
  mutate(`Content Rating` = factor(`Content Rating`, levels = unique(`Content Rating`))) %>% 
  ggplot(aes(x = `Content Rating`, y = n)) + 
  geom_bar(stat = "identity", fill = "palegreen2") + 
  theme_minimal() + 
  labs(x="Content Rating", y="") + 
  ggtitle("Free App Content Rating" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

googleplaystore %>% 
  dplyr::filter(Type == "Paid") %>% 
  count(`Content Rating`, sort = T) %>%  
  mutate(`Content Rating` = factor(`Content Rating`, levels = unique(`Content Rating`))) %>% 
  ggplot(aes(x = `Content Rating`, y = n)) + 
  geom_bar(stat = "identity", fill = "royalblue1") + 
  theme_minimal() + 
  labs(x="Content Rating", y="") + 
  ggtitle("Paid App Content Rating" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

### 2.5 Rating 
googleplaystore %>% 
  group_by(Type) %>% 
  count(`Rating`) %>% 
  ggplot(aes(x = `Rating`, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  theme_minimal() + 
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Rating", y="") + 
  ggtitle("Ratings of the free vs paid app" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

googleplaystore %>% 
  dplyr::filter(Type == "Free") %>% 
  count(`Rating`) %>% 
  dplyr::filter(!is.nan(Rating)) %>% 
  mutate(`Rating` = factor(`Rating`, levels = unique(`Rating`))) %>% 
  ggplot(aes(x = `Rating`, y = n)) + 
  geom_bar(stat = "identity", fill = "palegreen2") + 
  theme_minimal() + 
  labs(x="Rating", y="") + 
  ggtitle("Free App Rating" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  scale_x_discrete(breaks=seq(1, 5, 0.5))

googleplaystore %>% 
  dplyr::filter(Type == "Paid") %>% 
  count(`Rating`) %>% 
  dplyr::filter(!is.nan(Rating)) %>% 
  mutate(`Rating` = factor(`Rating`, levels = unique(`Rating`))) %>% 
  ggplot(aes(x = `Rating`, y = n)) + 
  geom_bar(stat = "identity", fill = "royalblue1") + 
  theme_minimal() + 
  labs(x="Rating", y="") + 
  ggtitle("Paid App Rating" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
  scale_x_discrete(breaks=seq(1, 5, 0.5))

### 2.6 Category
googleplaystore %>% 
  group_by(Type) %>% 
  count(`Category`) %>% 
  ggplot(aes(x = `Category`, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  theme_minimal() + 
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Category", y="") + 
  ggtitle("App Category" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 45, hjust = 1))

### 2.7 Android version 
googleplaystore %>% 
  group_by(Type) %>% 
  count(`Android Ver`) %>% 
  ggplot(aes(x = `Android Ver`, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  theme_minimal() + 
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Android Ver", y="") + 
  ggtitle("Android Versions" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 45, hjust = 1))


### 2.8 Installed App
googleplaystore %>% 
  group_by(Type) %>% 
  count(`Installs`) %>% 
  ggplot(aes(x = `Installs`, y = n)) + 
  geom_line(aes(group = Type, colour = Type), size = 1.3) + 
  theme_minimal() + 
  scale_colour_manual(values = c(Free = "steelblue3", Paid = "sienna2")) + 
  labs(x="Installs", y="") + 
  ggtitle("Installed App" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        axis.text.x = element_text(angle = 45, hjust = 1))

### 2.9 Content Rating of Rating >= 4
googleplaystore %>% 
  dplyr::filter(Rating >= 4) %>% 
  count(`Content Rating`) %>% 
  ggplot(aes(x = `Content Rating`, y = n)) + 
  geom_bar(stat = "identity", fill = "steelblue3") + 
  theme_minimal() + 
  labs(x="Content Rating", y="") + 
  ggtitle("Content Rating of Rating >= 4" ) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15))

```
