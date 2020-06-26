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

#### 1. https://www.kaggle.com/mdp1990/google-play-app-store-eda-data-visualisation 
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
