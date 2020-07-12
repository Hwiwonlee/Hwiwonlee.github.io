```r
library(googledrive)
library(tidyverse)
library(lubridate)


drive_auth()
#### 1. data load and setting ####
# 20.07.11 작업용 노트북에서 drive_auth() 실행시 Can't get Google credentials 에러 발생
# 1) https://github.com/tidyverse/googledrive/issues/276
# 2) https://gargle.r-lib.org/articles/non-interactive-auth.html#provide-a-service-account-token-directly-1
# 위 링크 들의 문제해결과 같진 않지만 에러 메시지를 좀 더 자세히 출력하는 options(gargle_quiet = FALSE)를 이용함.
# 2)에서 json 파일을 이용한 인증을 방법으로 제시해서 따라해보았지만 실패.
# options 설정 후 drive_auth(path = "mypath.json")를 실행하니 패키지 openssl이 설치되어 있지 않다는 에러 발견
# openssl을 설치하고 평소와 같이 drive_auth()를 이용하니 바로 계정이 연결 됌.

data_in_drive <- drive_find(type = "csv", pattern = "doctor_who")

for(i in 1:4){ 
  drive_download(file = data_in_drive$name[i], path = data_in_drive$name[i], overwrite = TRUE)
}


### 1.1 load 
doctor_who_dwguide <- read_csv("doctor_who_dwguide.csv")
doctor_who_imdb_details <- read_csv("doctor_who_imdb_details.csv")
doctor_who_all_scripts <- read_csv("doctor_who_all-scripts.csv")
doctor_who_all_detailsepisodes <- read_csv("doctor_who_all-detailsepisodes.csv")


### 1.2 some change valeu type in the data sets 
## 1.2.1 doctor_who_dwguide
names(doctor_who_dwguide)

# episodenbr : (numeric) Index of episode. Each episode has unique episodenbr value
# title : (chr) episode title
# weekday : (chr) broadcasting day based on UK
# broadcastdate : (chr) broadcasting date based on UK, format = "%d %b %Y"
# broadcasthour : (time) broadcasting hour based on UK, format = "00:00"
# duration : (time) duration of episode, foramt ="00:00:00"
# views : (chr) Average Audience, number of viewers based on UK
# share : (chr) Audience Share based on UK
# AI : (numeric) Appreciation Index in UK (https://en.wikipedia.org/wiki/Appreciation_Index)
# chart : (numeric) position at the BARB(Broadcasters' Audience Research Board) Week Top 30 Chart
# cast : (chr) List of actors and actresses
# crew : (chr) List of crews
# summary : (chr) summary of episode 


# broadcastdate : Change to date column
# views : remove the unit, "m" and change to numeric 
doctor_who_dwguide %>% 
  mutate(broadcastdate = parse_date_time(broadcastdate, orders = "%d %b %Y")) %>% 
  mutate(views = as.numeric(str_remove(views, "m"))) -> doctor_who_dwguide


## 1.2.2 doctor_who_all_detailsepisodes
names(doctor_who_all_detailsepisodes)

# epsodeid : (chr) index of episode, format : 0-0 or just chr like webS7, TimeRND2011...
# title : (chr) title of episode
# first_diffusion : (chr) first broadcast date based on UK, format = "%d %b, %Y", "%b %d, %Y" or just chr 
# doctorid : (numeric) index of doctor

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

## 1.2.3 doctor_who_imdb_details : the IMDB rating of the episode of the modern area (post 2005)
names(doctor_who_imdb_details)

# number : (numeric) episode number at the each season, not unique value
# title : (chr) title of episode
# rating : (numeric) rating of IMDb(Internet Movie Database)
# nbr_votes : (numeric) number of vote at the IMDb rating 
# description : (chr) summary of episode
# season : (numeric) season number

doctor_who_imdb_details         



## 1.2.4 doctor_who_all_scripts
names(doctor_who_all_scripts)

# idx : (numeric) index of script
# text : (chr) text which the location setting or content of talk
# detail : (chr) speaker or speakers
# episodeid : (chr) index of episode, format : 0-0
# doctorid : (chr) index of doctor



### 1.3 Handling the kind of index 
# Each dataset has identifier, like the index, about each episode.
# If I use this fact, wouldn't we be able to merge these four data sets?

# doctor_who_dwguide has "episodenbr", "title"
# doctor_who_all_detailsepisodes has "episodeid", "title"
# doctor_who_imdb_details has "number", "title"
# doctor_who_all_scripts has "episodeid"

# In fact, The amount of the episode that each dataset has is as follow : 
# doctor_who_dwguide(851) > doctor_who_all_detailsepisodes(328) > doctor_who_all_scripts(306) > doctor_who_imdb_details(148)


# intersection between doctor_who_all_detailsepisodes(328) and doctor_who_all_scripts(306)
unique(doctor_who_all_detailsepisodes$episodeid)[unique(doctor_who_all_detailsepisodes$episodeid) %in% unique(doctor_who_all_scripts$episodeid)]

# The episode that doctor_who_all_detailsepisodes only has is as follow : 22. 
unique(doctor_who_all_detailsepisodes$episodeid)[-which(unique(doctor_who_all_detailsepisodes$episodeid) %in% unique(doctor_who_all_scripts$episodeid))]

# I think, should filter some value start with "string" in the "episodeid" 
# First, check up the values 
doctor_who_all_detailsepisodes %>% 
  filter(grepl("^[A-Z]", episodeid)) %>% 
  pull(episodeid)
# "CIN2007", "Dreamland", "TimeRND2011", "CIN2012", "Bounty", "DeadTime", "PTemple" 

# Actually, "Doctor who" has a lot of some kind of special contents not TV drama or holiday drama. 
# For example, "Dreamland" is the comics at the 10th Doctor,  
# "Bounty", "DeadTime", "PTemple", these three contents are audio drama at the 8th doctor and 
# CIN2007, TimeRND2011, CIN2012, are some kind of shortest drama like the clip.
# So if I merge the dataset about only the TV drama, will remove these all observation. 

# It's a little late, but I have to deal with why the amount of episodes contained in each data set is different.
# doctor_who_dwguide has greatest amount of episode. 
# doctor_who_dwguide has most(maybe all) episodes except for special episodes such as audio, comics and clips.
# Honestly, if focus on the just "title", doctor_who_all_detailsepisodes has a lot of episode, maybe also all episode too
# However, in the doctor_who_all_detailsepisodes, some series be integrated just one title especially old season's series.
# For example, series of An Unearthly Child at the 1st doctor.

doctor_who_dwguide %>% 
  filter(between(episodenbr, 1, 12)) %>% pull(title)

doctor_who_all_detailsepisodes %>% 
  filter(grepl("^1-", episodeid))

# In the doctor_who_dwguide, series of "An Unearthly Child" has four episode and 
# serise of "The Daleks" has seven episode. Then just numbering to 1 from 11. 
# But in the doctor_who_all_detailsepisodes, series of "An Unearthly Child" sum up just only one observation,  
# also serise of "The Daleks" too. The difference came from here.


# 1) episodeid split to season and number or add doctorid, season and number
# 2) arrange using doctorid, season, number

doctor_who_all_scripts %>% 
  # Delete not broadcast episodes 
  filter(!grepl("-0[0-9]$", episodeid)) %>%
  filter(!grepl("^[A-Z]", episodeid)) %>% 
  # "The Infinite Quest", comics episode 
  filter(episodeid != "29-14") %>% 
  # "Vastra Investigates", chrismas Prequel, webcast  
  filter(episodeid != "33-59") %>% 
  # change "3-1-5" to 3-1.5 at the episodeid 
  mutate(episodeid = ifelse(episodeid == "3-1-5", "3-1.5", episodeid)) %>% 
  filter(grepl("^[0-9]", episodeid)) %>% 
  separate(episodeid, c("season", "number"), "-") %>% 
  mutate(across(c(season, number), as.numeric)) %>% 
  arrange(doctorid, season, number)

doctor_who_all_detailsepisodes %>% 
  # Delete not broadcast episodes 
  filter(!grepl("-0[0-9]$", episodeid)) %>%
  filter(!grepl("^[A-Z]", episodeid)) %>% 
  # "The Infinite Quest", comics episode 
  filter(episodeid != "29-14") %>% 
  # "Vastra Investigates", chrismas Prequel, webcast  
  filter(episodeid != "33-59") %>% 
  # change "3-1-5" to 3-1.5 at the episodeid 
  mutate(episodeid = ifelse(episodeid == "3-1-5", "3-1.5", episodeid)) %>% 
  separate(episodeid, c("season", "number"), "-") %>% 
  mutate(across(c(season, number), as.numeric)) %>% 
  arrange(doctorid, season, number)
  # %>% select(title) %>% pull(title) -> titles # for saving the titles at the doctor_who_all_detailsepisodes
  

doctor_who_imdb_details %>% 
  select(season, number, everything()) %>% 
  # Edit the season count using old season
  mutate(season = season+26)


doctor_who_dwguide %>% 
  arrange(episodenbr) # %>% pull(title) -> titles2 # for saving the titles at the doctor_who_dwguide




# Have to make sure that the same titles obtained by doctor_who_all_detailsepisodes and
# titles2 obtained by doctor_who_dwguide are the same

titles %in% titles2

sum(grepl(":", titles))
sum(grepl(":", titles2))

# There has some issues about the "title" 
# In each title, Entire title are almost same but some characters are different(ex, ",", "the" moreover, upper and lower case)

tolower(unique(str_remove(titles2, ":.*"))) # 313
tolower(titles) # 319

titles[-which(tolower(titles) %in% tolower(unique(str_remove(titles2, ":.*"))))]


titles[194:196]
grep("The Return of Doctor Mysterio, by Stephen Moffat", titles)
grep("The Return Of Doctor Mysterio", unique(str_remove(titles2, ":.*")))

unique(str_remove(titles2, ":.*"))[grep("Mysterio", unique(str_remove(titles2, ":.*")))]
str_remove(titles2, ":.*")[grep("Curse of", str_remove(titles2, ":.*"))]

# titles에 바꿀 목록
grep("Reign of Terror", titles) # "The Reign of Terror"
grep("Galaxy Four", titles) # "Galaxy 4"
unique(str_remove(titles2, ":.*"))[grep("Master Plan", unique(str_remove(titles2, ":.*")))] # "The Dalek's Master Plan"
unique(str_remove(titles2, ":.*"))[grep("Colony In Space", unique(str_remove(titles2, ":.*")))] # "The Daemons"
grep("Masque of Mandragora", titles) # "The Masque of Mandragora"
unique(str_remove(titles2, ":.*"))[grep("Gate", unique(str_remove(titles2, ":.*")))] # "Warrior's Gate"
grep("Time Flight", titles) # "Time-Flight"
grep("The Mysterious Planet", titles) # "The Trial Of A Time Lord (The Mysterious Planet)"
grep("Mindwarp", titles) # "The Trial Of A Time Lord (Mindwarp)"
grep("Terror of the Vervoids", titles) # "The Trial Of A Time Lord (Terror of the Vervoids)"
grep("The Ultimate Foe", titles) # "The Trial Of A Time Lord (The Ultimate Foe)"
grep("Love and Monsters", titles) # "Love & Monsters"
grep("Family of Blood", titles) # "The Family of Blood"
grep("Curse of the Black Spot", titles) # "The Curse of the Black Spot"
grep("The Doctor, the Widow, and the Wardrobe", titles) # "The Doctor, The Widow and the Wardrobe"
grep("The Return of Doctor Mysterio, by Stephen Moffat", titles) # "The Return of Doctor Mysterio 
titles2[grep("The End of Time", titles2)] # ":" change to ","

titles[which(grepl("Wardrobe", titles))]
titles2[which(grepl("Wardrobe", titles2))]

lowetitles

tolower(titles)


doctor_who_all_scripts %>% 
  filter(grepl("3-1-5", episodeid))

doctor_who_all_scripts %>% 
  filter(grepl("^3-", episodeid)) %>% distinct(episodeid)

doctor_who_all_detailsepisodes %>% 
  filter(grepl("3-1-5", episodeid))

doctor_who_dwguide %>% 
  filter(title == "Mission to the Unknown")

doctor_who_dwguide %>% 
  filter(between(episodenbr, 86, 90)) %>% select(1:4) %>% as.data.frame()
  
  
doctor_who_dwguide %>% 
  filter(episodenbr == 30)

doctor_who_all_scripts %>% 
  filter(grepl("37", episodeid)) %>% 
  distinct(episodeid)

doctor_who_all_detailsepisodes %>% 
  filter(grepl("CIN2012", episodeid))

doctor_who_dwguide %>% 
  filter(between(year(broadcastdate), 1996, 2005)) %>% select(1:7)

doctor_who_imdb_details %>% 
  filter(grepl("The Great Detective", title))


sort(doctor_who_dwguide$episodenbr)
unique(doctor_who_all_scripts$episodeid)
sort(unique(doctor_who_all_detailsepisodes$episodeid))
nrow(doctor_who_imdb_details)

doctor_who_all_detailsepisodes$title
doctor_who_dwguide$title
doctor_who_imdb_details$title

```
