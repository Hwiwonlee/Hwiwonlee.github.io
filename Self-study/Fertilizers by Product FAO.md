```r
library(tidyverse)
library(countrycode)


# 1. Import the dataset
drive_auth()
data_in_drive <- drive_find(type = "csv", pattern = "Fertilizers")


for(i in 1:1){ 
  drive_download(file = data_in_drive$name[i], path = data_in_drive$name[i], overwrite = TRUE)
}

FertilizersProduct <- read_csv("FertilizersProduct.csv")

## 1.1 Expain columns and values
names(FertilizersProduct)
FertilizersProduct %>% 
  count(Flag, sort = T)

# Area Code : Unique number for indentifying country like index
# Area : Name of country
# Item Code : Unique number for indentifying item like index
# Item : Name of item
# Element Code : Unique number for indentifying event like index
# Element : Some event like trade or production
# Year Code, Year : Just year, exactly same
# Unit : Unit of fertilizer, 1000 US$ or tonnes
# Value : Amount or volume related by unit 
# Flag : Index about the method to get these values
## A - Aggregate; may include official; semi-official; estimated or calculated data;
## E - Expert sources from FAO (including other divisions);
## Fb - Data obtained as a balance;
## Fm - Manual Estimation;
## P - Provisional official data;
## Qm - Official data from questionnaires and/or national sources and/or COMTRADE (reporters);
## R - Estimated data using trading partners database;
## W - Data reported on country official publications or web sites (Official) or trade country files;
## Z - ? No information 

# 각각의 물품, 나라, 연도에 따라 Element와 Value가 입력된 상태. 


### Check the missing value
FertilizersProduct %>% 
  summarise_all(~sum(is.na(.))) %>% as.data.frame()
### none 

## 1.2 dataset correction 
FertilizersProduct %>% 
  # Côte d'Ivoire의 이름이 C\xf4te로 깨져서 나옴, o로 대체
  mutate(Area = str_replace(Area, "\xf4", "ô")) -> FertilizersProduct
# 끝. 

# 5개의 대륙을 추가, Continent  
# https://stackoverflow.com/questions/47510141/get-continent-name-from-country-name-in-r
FertilizersProduct$Continent <- countrycode(sourcevar = as.data.frame(FertilizersProduct)[, "Area"],
                                            origin = "country.name",
                                            destination = "continent")
FertilizersProduct %>% 
  mutate(Continent = ifelse(grepl("Serbia|Montenegro", Area), "Europe", Continent)) -> FertilizersProduct

FertilizersProduct %>% 
  count(Continent)
# 끝. 

# Value == 0?
# 없으면 공백일 수도 있는데 왜 Value = 0이 존재할까? 
FertilizersProduct %>% 
  dplyr::filter(Value == 0) %>% 
  count(Area, sort = T)

# 모든 나라가 같은 연도에 같은 observation을 갖을까? 
FertilizersProduct %>% 
  group_by(Area) %>% 
  count(Year) %>% 
  pivot_wider(names_from = "Area",
              values_from = "n") %>% 
  dplyr::select(1, sample(seq(2, length(unique(FertilizersProduct$Area)), 1), 4))
# 응. 아니야. 
# 심지어 일부 나라는 아예 조사가 되지 않은 연도도 있다. 


# Value의 -1043? 
FertilizersProduct %>% 
  dplyr::filter(Value == 0) %>% as.data.frame()


FertilizersProduct %>% 
  dplyr::filter(Area == "Switzerland" & 
                  Element == "Agricultural Use" &
                  Unit == "tonnes" &
                  `Item Code` == 4023) %>% 
  arrange(desc(Year)) %>% 
  dplyr::select(-matches(" ")) %>% as.data.frame()


# Export & Import의 Item list와 Production & Agriculture Use의 Item list가 다르다? 
FertilizersProduct %>% 
  group_by(Element) %>% 
  count(Item) %>% count(Element) 
# Export & Import는 22개의 Item, Production & Agriculture Use는 23개의 Item. 

FertilizersProduct %>% 
  group_by(Element) %>% 
  count(Item) %>%
  ungroup() %>% 
  pivot_wider(names_from = Element, values_from = n) %>% as.data.frame()
# Other NK compounds만 차이가 있다. 
# 끝. 


# 2. EDA 
FertilizersProduct %>% 
  count(Element)

FertilizersProduct %>% 
  count(Value)



## 2,1 Using Element 
barplot_value_country <- function(target) { 
  FertilizersProduct %>% 
    dplyr::filter(Element == target) %>% 
    group_by(Area) %>%
    summarise(sum = sum(Value)) %>% 
    arrange(desc(sum)) %>% 
    head(10) %>% 
    arrange(sum) %>% 
    mutate(Area = factor(Area, levels = unique(Area))) %>% 
    ggplot(aes(x = Area, y = sum, fill = Area)) + 
    geom_bar(stat = "identity") +
    coord_flip() + 
    ggtitle(paste0('Top 10 Country Having Highest ', target)) + 
    theme_minimal() + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "none") + 
    labs(x="Country", y=paste0(target))
  
}

barplot_value_country("Export Quantity")
barplot_value_country("Import Quantity")

barplot_value_country("Export Value")
barplot_value_country("Import Value")

barplot_value_country("Agricultural Use")
barplot_value_country("Production")



FertilizersProduct %>% 
  dplyr::filter(Element == "Export Quantity") %>% 
  summarise_at(vars(Value), funs(min, mean, sd, 
                                 quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))), 
                                 max)) %>%
  unnest(cols = c(quantile))

FertilizersProduct %>% 
  dplyr::filter(Element == "Export Value") %>% 
  summarise_at(vars(Value), funs(min, mean, sd, 
                                 quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))), 
                                 max)) %>%
  unnest(cols = c(quantile))

FertilizersProduct %>% 
  dplyr::filter(Element == "Export Quantity") %>% 
  group_by(Continent) %>% 
  summarise(sum = sum(Value))

### 2.1.2 Using boxplot, Visualization about values of Export & Import
# Distribution of element's values among the continent
boxplot_value_continent <- function(target) {
  
  FertilizersProduct %>% 
    dplyr::filter(Element == target) %>% 
    # 0을 가진 observation이 있으므로 0.001을 더해서 NA를 방지함
    ggplot(aes(x = log(Value+0.001), color = Continent)) +
    geom_boxplot(position = "dodge", outlier.shape = "*", outlier.size = 5) +
    facet_wrap(Continent ~ .,  ncol = 5) + 
    coord_flip() + 
    ggtitle(paste0('Boxplot about ', target, ' in five continent')) + 
    theme_bw() + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "none") + 
    labs(x=paste0('log(', target, ')'), y="")
  
}

boxplot_value_continent("Export Quantity")
boxplot_value_continent("Import Quantity")

boxplot_value_continent("Export Value")
boxplot_value_continent("Import Value")

boxplot_value_continent("Agricultural Use")
boxplot_value_continent("Production")

# Barplot of element's values among the item
barplot_value_continent <- function(target) { 
  FertilizersProduct %>% 
    dplyr::filter(Element == target) %>% 
    group_by(Continent, Item) %>% 
    summarise(sum = sum(Value)) %>% 
    ggplot(aes(x = Continent, y = sum, color = Continent, fill = Continent)) +
    geom_bar(stat = 'identity') + 
    facet_wrap(Item ~ ., ncol = 3, scales = "free_y") + 
    theme_bw() + 
    ggtitle(paste0('Bar plot about ', target, ' in Each Items')) + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "none") + 
    labs(x="Continent", y="Amount")
  
}
barplot_value_continent("Export Quantity")
barplot_value_continent("Import Quantity")

barplot_value_continent("Export Value")
barplot_value_continent("Import Value")

barplot_value_continent("Agricultural Use")
barplot_value_continent("Production")



# Distribution of element's values among the item
boxplot_value_item <- function(target) {
  
  FertilizersProduct %>% 
    dplyr::filter(Element == target) %>% 
    # 0을 가진 observation이 있으므로 0.001을 더해서 NA를 방지함
    ggplot(aes(x = log(Value+0.001), color = Item)) +
    geom_boxplot(position = "dodge", outlier.shape = "*", outlier.size = 5) +
    facet_wrap(Item ~ .,  ncol = 5) +
    theme_bw() +
    ggtitle(paste0('Boxplot about ', target, ' in each items')) +
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "none") + 
    labs(x=paste0('log(', target, ')'), y="")
  
}

boxplot_value_item("Export Quantity")
boxplot_value_item("Import Quantity")

boxplot_value_item("Export Value")
boxplot_value_item("Import Value")

boxplot_value_item("Agricultural Use")
boxplot_value_item("Production")

# Barplot of element's values among the item
barplot_value_item <- function(target) { 
  FertilizersProduct %>% 
    group_by(Year, Item) %>% 
    dplyr::filter(Element == target) %>% 
    summarise(sum = sum(Value)) %>% 
    ggplot(aes(x = Year, y = sum, color = Item, fill = Item)) +
    geom_bar(stat = 'identity') + 
    facet_wrap(Item ~ ., ncol = 3) + 
    theme_bw() + 
    ggtitle(paste0('Bar plot about ', target, ' in Each Items')) + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "none") + 
    labs(x="Years", y="Amount") + 
    scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3))
    
}

barplot_value_item("Export Quantity")
barplot_value_item("Import Quantity")

barplot_value_item("Export Value")
barplot_value_item("Import Value")

barplot_value_item("Agricultural Use")
barplot_value_item("Production")


FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  group_by(Year, Element) %>% 
  summarise(sum_value = sum(Value)) %>% 
  ggplot(aes(x = Year, y = sum_value, color = Element, fill = Element)) +
  geom_line(group = 1) + 
  facet_wrap(Element ~ ., ncol = 1, scales = "free_y") +
  theme_minimal() + 
  ggtitle(paste0('Line plot about South Korea in Each Element')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "none") + 
  labs(x="Years", y="Amount")


```
