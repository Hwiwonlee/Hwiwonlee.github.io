```r
library(googledrive)
library(tidyverse)
library(lubridate)

drive_auth()
data_in_drive <- drive_find(type = "csv", pattern = "doctor_who")


for(i in 1:4){ 
  drive_download(file = data_in_drive$name[i], path = data_in_drive$name[i], overwrite = TRUE)
}

#### 1. data load and setting ####

### 1.1 load 
doctor_who_dwguide <- read_csv("doctor_who_dwguide.csv")
doctor_who_imdb_details <- read_csv("doctor_who_imdb_details.csv")
doctor_who_all_scripts <- read_csv("doctor_who_all-scripts.csv")
doctor_who_all_detailsepisodes <- read_csv("doctor_who_all-detailsepisodes.csv")


### 1.2 modify the data set 
## 1.2.1 doctor_who_dwguide
# broadcastdate : Change to date column
# views : remove the unit, "m" and change to numeric 
doctor_who_dwguide %>% 
  mutate(broadcastdate = parse_date_time(broadcastdate, orders = "%d %b %Y")) %>% 
  mutate(views = as.numeric(str_remove(views, "m"))) -> doctor_who_dwguide
  

## 1.2.2 doctor_who_all_detailsepisodes
# first_diffusion consist with character of two type, start with alphabet or numeric
# extraction for modification
# first diffusion of "Pond Life" is 27-31 Aug, 2012. 
doctor_who_all_detailsepisodes %>% 
  filter(grepl("^[A-Z]", first_diffusion) | grepl("Pond Life", title)) %>% 
  pull(., first_diffusion) -> need_to_change

doctor_who_all_detailsepisodes %>% 
  filter(grepl("^[0-9]", first_diffusion))

index <- which(doctor_who_all_detailsepisodes$first_diffusion %in% need_to_change)

# Not broadcast mean really not broadcasting. It is Shada which episode of 4th doctor
change_list <- c("Jan 14, 1967", "Nov 11, 1967", 
                 "Aug 8, 2014",
                 "Sep 20, 2014", 
                 "Nov 8, 2014", 
                 "Dec 25, 2014", 
                 "Oct 31, 2015",
                 "Aug 27, 2012", 
                 "Not broadcast",
                 "Oct 1, 1998", 
                 "Sep 7, 1998", 
                 "Mar 2, 1998")

# Correction the first_diffusion values using index and change_list
doctor_who_all_detailsepisodes$first_diffusion[index] <- change_list


doctor_who_all_detailsepisodes %>% 
  mutate(`first_diffusion` = 
           case_when ( 
             grepl("^[0-9]", `first_diffusion`) ~ parse_date_time(`first_diffusion`, orders = "%d %b, %Y"), 
             grepl("^[A-Z]", `first_diffusion`) ~ parse_date_time(`first_diffusion`, orders = "%b %d, %Y")
           )
    ) -> doctor_who_all_detailsepisodes
  # %>% filter(is.na(first_diffusion)) # just Shada 

doctor_who_imdb_details         
         
doctor_who_all_scripts         
         



doctor_who_all_detailsepisodes[147, ]
  
# lubridate test
date <- doctor_who_dwguide$broadcastdate  
date[1:10]
mdy(date[1:10])

set.seed(100)
date[sample(seq(1, length(date), 1), 10)]
set.seed(100)
parse_date_time(date[sample(seq(1, length(date), 1), 10)], orders = "%d %b %Y")

```
