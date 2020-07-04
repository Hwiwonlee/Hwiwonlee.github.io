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

overview <- function(dataset, threshold_value = 0.005) { 
  a <- unlist(lapply(dataset, class))
  
  b <- sapply(lapply(FertilizersProduct[, a == "numeric"], unique), length)
  c <- names(d[which(d < round(nrow(dataset)*threshold_value, 0))])
  a[which(names(a) %in% c)] <- "character"
  
  # Frequency of unique value of character or factor variables
  unique_value_list <- lapply(dataset[, which(a == "character" | a == "factor")], table)
  
  # summary stats of numeric variables
  summary_stat_list <- function(dataset){
    
    summary_stat <- function(target){ 
      dataset %>% 
        dplyr::select(target) %>% 
        summarise_all(funs(min, 
                           quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))), 
                           max, 
                           mean, sd)) %>%
        unnest(cols = c(quantile))
    } 
    
    list <- lapply(names(dataset[, which(a == "numeric")]), summary_stat)
    names(list) <- names(dataset[, which(a == "numeric")])
    
    return(list)
  }
  
  summary_stat_list <- summary_stat_list(FertilizersProduct)
  
  result <- list(unique_value_list, summary_stat_list)
  names(result) <- c("Categorical varibles", "Numeric variables")
  return(result)
}
overview(FertilizersProduct)


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

unique(FertilizersProduct$Element)

summary_stat <- function(target){ 
  FertilizersProduct %>% 
    dplyr::filter(Element == target) %>% 
    summarise_at(vars(Value), funs(min, 
                                   quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))), 
                                   max, 
                                   mean, sd)) %>%
    unnest(cols = c(quantile))
}
summary_stat("Export Quantity")

summary_stat_list <- function(dataset){
  
  summary_stat <- function(target){ 
    dataset %>% 
      dplyr::filter(Element == target) %>% 
      summarise_at(vars(Value), funs(min, 
                                     quantile = list(as.tibble(as.list(quantile(., probs = c(0.25, 0.5, 0.75))))), 
                                     max, 
                                     mean, sd)) %>%
      unnest(cols = c(quantile))
  } 
  
  list <- lapply(unique(dataset$Element), summary_stat)
  names(list) <- unique(dataset$Element)
  
  return(list)
}
summary_stat_list(FertilizersProduct)


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

## 2,1 Each continent 
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


## 2.2 Whole world
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


## 2.3 # Trend of Random country 
trend_country <- function(country) { 
  
  FertilizersProduct %>% 
    dplyr::select(-matches(" ")) %>% 
    dplyr::filter(Area == country) %>% 
    group_by(Year, Element) %>% 
    summarise(sum_value = sum(Value)) %>% 
    ggplot(aes(x = Year, y = sum_value, color = Element, fill = Element)) +
    geom_line(size = 1.5) + 
    theme_minimal() + 
    ggtitle(paste0('Line Plot of Each Element of ',  country)) + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15)) + 
    labs(x="Years", y="Amount") + 
    scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3))
  
}

trend_country(unique(FertilizersProduct$Area)[sample(length(unique(FertilizersProduct$Area)), 1)])

# Trend of korea 
FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  group_by(Year, Element) %>% 
  summarise(sum_value = sum(Value)) %>% 
  ggplot(aes(x = Year, y = sum_value, color = Element, fill = Element)) +
  geom_line(size = 1.5) + 
  facet_wrap(Element ~ ., ncol = 1, scales = "free_y") +
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "none") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3))


FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  # mutate(Year = as.character(Year)) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Import", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = as.numeric(Year), y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))
  

FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  # mutate(Year = as.character(Year)) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Export", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = as.numeric(Year), y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))


FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  # mutate(Year = as.character(Year)) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Production", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = as.numeric(Year), y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))

FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  # mutate(Year = as.character(Year)) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Use", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = as.numeric(Year), y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))

FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  # mutate(Year = as.character(Year)) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Use", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(3,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = as.numeric(Year), y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))


FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  dplyr::filter(Area == "Republic of Korea") %>% 
  dplyr::filter(grepl("Import", Element)) %>% # target
  group_by(Element, Item) %>%
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  group_by(Element) %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% # select top n
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = Year, y = Value, color = Item)) +
  geom_line(size = 1) + 
  geom_point(size = 1.3) + 
  facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Line Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))



General_lineplot <- function(dataset, country = country, Elements = Elements, start = n, end = m) { 

  # dataset is target dataset, FertilizersProduct
  # country is target country 
  # Elements means one or more elements in "Element column"
  # start, end are integer value that you want to see the position like rank. 
    
  dataset %>% 
    
    # Data set up 
    dplyr::select(-matches(" ")) %>% 
    dplyr::filter(Area == country) %>%
    dplyr::filter(Element %in% Elements) %>% 
    
    # To arrange values use dense_rank function through the each groups mean value
    group_by(Element, Item) %>% 
    mutate( across(contains('Value'), 
                   .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
    ungroup() %>% 
    group_by(Element) %>% 
    mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
    
    # Just filter some items on your choice
    # start value is n and end value in m
    # In general, start is 1, end is 3, 5, or 10 for select just "top n"
    # But if you need to spread the lines, you will select you wants
    dplyr::filter(Value_rank %in% seq(start, end, 1)) %>% 
    mutate(Item = factor(Item, levels = unique(Item))) %>%
    
    # ggplot part 
    ggplot(aes(x = Year, y = Value, color = Item)) +
    geom_line(size = 1.1) + 
    geom_point(size = 1.3) + 
    facet_wrap(Element ~ ., ncol = 3, scales = "free_y") + 
    theme_minimal() + 
    ggtitle(paste0('Line Plot of Selected Element(s) of ', country)) + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "bottom") + 
    labs(x="Years", y="Amount") + 
    scale_x_continuous(breaks=seq(min(dataset$Year), max(dataset$Year), 3)) +
    scale_y_continuous(labels = function(x) format(x, scientific = FALSE))
  
}

General_lineplot(dataset = FertilizersProduct, 
                 country = "Republic of Korea", 
                 Elements = c("Agricultural Use"), 
                 start = 1, 
                 end = 5)

General_lineplot(dataset = FertilizersProduct, 
                 country = "Republic of Korea", 
                 Elements = c("Agricultural Use"), 
                 start = 3, 
                 end = 5)


FertilizersProduct %>% 
  dplyr::select(-matches(" ")) %>% 
  dplyr::filter(Area == "Finland") %>% 
  dplyr::filter(Element %in% c("Production", "Export Quantity")) %>% 
  pivot_wider(names_from = Element, values_from = Value, names_prefix = "Value ") %>% 
  mutate(across(contains("Value"), ~replace_na(.x, 0))) %>% 
  pivot_longer(cols = c("Value Export Quantity", "Value Production"), 
               names_to = "Element", values_to = "Value") %>% 
  mutate(Element = str_remove(Element, "Value "))  %>% 
  group_by(Item) %>% 
  
  
  mutate( across(contains('Value'), 
                 .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
  ungroup() %>% 
  mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>% 
  
  
  
  
  
  
  dplyr::filter(Value_rank %in% seq(1,5,1)) %>%
  arrange(Value_rank) %>% 
  mutate(Item = factor(Item, levels = unique(Item))) %>% 
  ggplot(aes(x = Year, y = Value, color = Element, fill = Element)) +
  geom_bar(stat = "identity", position = "dodge") + 
  facet_wrap(Item ~ ., ncol = 3, scales = "free_y") + 
  theme_minimal() + 
  ggtitle(paste0('Bar Plot of Each Element of Republic of Korea')) + 
  theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
        legend.position = "bottom") + 
  labs(x="Years", y="Amount") + 
  scale_x_continuous(breaks=seq(min(FertilizersProduct$Year), max(FertilizersProduct$Year), 3)) + 
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE))


General_barplot <- function(dataset, country = country, Elements = Elements, start = n, end = m) { 
  
  # dataset is target dataset, FertilizersProduct
  # country is target country 
  # Elements means one or more elements in "Element column"
  # start, end are integer value that you want to see the position like rank.
    
  dataset %>% 
    dplyr::select(-matches(" ")) %>% 
    dplyr::filter(Area == "Finland") %>% 
    dplyr::filter(Element %in% Elements) %>% 
    pivot_wider(names_from = Element, values_from = Value, names_prefix = "Value ") %>% 
    mutate(across(contains("Value"), ~replace_na(.x, 0))) %>% 
    pivot_longer(cols = paste0("Value ", Elements), 
                 names_to = "Element", values_to = "Value") %>% 
    mutate(Element = str_remove(Element, "Value "))  %>% 
    group_by(Item) %>% 
    
    # 각각의 Item에 대하여 선택된 element의 value 평균을 구함.
    # 문제는 평균이기 때문에 n개의 item을 선택하는 경우, 특정 element의 양이 큰 경우에 영향을 크게 받는다는 것. 
    # 해결책은...특정 element에 대한 n개의 Item을 선택하고, 그 (Item, element)와 다른 element를 비교해보자는 것.
    mutate( across(contains('Value'), 
                   .fns = list(rank = ~mean(.x, na.rm = T))) ) %>% 
    ungroup() %>% 
    mutate(Value_rank = dense_rank(desc(Value_rank))) %>% 
    
    # Just filter some items on your choice
    # start value is n and end value in m
    # In general, start is 1, end is 3, 5, or 10 for select just "top n"
    # But if you need to spread the lines, you will select you wants
    dplyr::filter(Value_rank %in% seq(n,m,1)) %>%
    arrange(Value_rank) %>% 
    mutate(Item = factor(Item, levels = unique(Item))) %>% 
    
    # ggplot part 
    ggplot(aes(x = Year, y = Value, color = Element, fill = Element)) +
    geom_bar(stat = "identity", position = "dodge") + 
    facet_wrap(Item ~ ., ncol = 3, scales = "free_y") + 
    theme_minimal() + 
    ggtitle(paste0('Bar Plot of Each Element of Republic of Korea')) + 
    theme(plot.title = element_text(face = "bold", hjust = 0.5, size = 15), 
          legend.position = "bottom") + 
    labs(x="Years", y="Amount") + 
    scale_x_continuous(breaks=seq(min(dataset$Year), max(dataset$Year), 3)) + 
    scale_y_continuous(labels = function(x) format(x, scientific = FALSE))
  
}

General_barplot(dataset = FertilizersProduct, 
                 country = "Republic of Korea", 
                 Elements = c("Export Quantity", "Import Quantity", "Production"), 
                 start = 1, 
                 end = 5)


```
