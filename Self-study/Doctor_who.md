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



### 1.3 Handling the index 
## 1.3.1 Titles and episodeid 
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
  arrange(doctorid, season, number) %>% select(title) %>% pull(title) -> titles # for saving the titles at the doctor_who_all_detailsepisodes

doctor_who_dwguide %>% 
  arrange(episodenbr) %>% pull(title) -> titles2 # for saving the titles at the doctor_who_dwguide


# Have to make sure that the same titles obtained by doctor_who_all_detailsepisodes and
# titles2 obtained by doctor_who_dwguide are the same

titles %in% titles2

sum(grepl(":", titles))
sum(grepl(":", titles2))

# There has some issues about the "title" 
# In each title, Entire title are almost same but some characters are different(ex, ",", "the" moreover, upper and lower case)
# Exactly, the title in doctor_who_dwguide is some kind of the basic. 
# Because in the old season, until season 26, Doctor who had nested structure which had one main title and several sub titles. 
# For example, the first season and the first story, "An Unearthly Child" had four episodes.
# This structure disappeared as it entered the new season.
# Anyway, the title in doctor_who_dwguide has basic type title which is "main title : sub title"
# But the title in doctor_who_all_detailsepisodes has incomplete title that sub title was gone.
# Moreover, doctor_who_all_detailsepisodes has index, episodeid, that just identify main title but omit the sub titles.
# That means, doctor_who_all_detailsepisodes has no information(for example, duration, views as you see at doctor_who_dwguide) about each episode in the old season. 
# Which one is best? 
# Well, the title and index in doctor_who_dwguide seem to be the best. 
# because in the A, each episode contained main story has some unique values which are broadcasthour, duration, views and so on and then if the two data sets have the same title, the two data sets could be merged into one.
# Unlike what seems to be seen, it is not an easy matter to judge.
# Now I assume to merge two dataset, just focus on whether title in doctor_who_dwguide and doctor_who_all_detailsepisodes are the same or different.

tolower(unique(str_remove(titles2, ":.*"))) # 313
tolower(titles) # 319

# A list to see how different it is.
titles[-which(tolower(titles) %in% tolower(unique(str_remove(titles2, ":.*"))))]

# Results of above that
grep("Reign of Terror", titles) # "The Reign of Terror"
grep("Galaxy Four", titles) # "Galaxy 4"
unique(str_remove(titles2, ":.*"))[grep("Master Plan", unique(str_remove(titles2, ":.*")))] # "The Dalek's Master Plan"
unique(str_remove(titles2, ":.*"))[grep("The Dæmons", unique(str_remove(titles2, ":.*")))] # "The Daemons"
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

doctor_who_all_detailsepisodes %>% 
  mutate(title = 
           case_when(
             title == "Reign of Terror" ~ "The Reign of Terror",
             title == "Galaxy Four" ~ "Galaxy 4",
             title == "Masque of Mandragora" ~ "The Masque of Mandragora",
             title == "Time Flight" ~ "Time-Flight",
             title == "The Mysterious Planet" ~ "The Trial Of A Time Lord (The Mysterious Planet)",
             title == "Mindwarp" ~ "The Trial Of A Time Lord (Mindwarp)",
             title == "Terror of the Vervoids" ~ "The Trial Of A Time Lord (Terror of the Vervoids)",
             title == "The Ultimate Foe" ~ "The Trial Of A Time Lord (The Ultimate Foe)",
             title == "Love and Monsters" ~ "Love & Monsters",
             title == "Family of Blood" ~ "The Family of Blood",
             title == "Curse of the Black Spot" ~ "The Curse of the Black Spot", 
             title == "The Doctor, the Widow, and the Wardrobe" ~ "The Doctor, the Widow and the Wardrobe",
             title == "The Return of Doctor Mysterio, by Stephen Moffat" ~ "The Return of Doctor Mysterio",
             TRUE ~ title
           )
  ) %>% 
  filter(!grepl("-0[0-9]$", episodeid)) %>%
  filter(!grepl("^[A-Z]|^[a-z]", episodeid)) %>% 
  filter(title != "Shada") %>% 
  # "The Infinite Quest", comics episode 
  filter(episodeid != "29-14") %>% 
  # "Vastra Investigates", chrismas Prequel, webcast  
  filter(episodeid != "33-59") %>% 
  # change "3-1-5" to 3-1.5 at the episodeid 
  mutate(episodeid = ifelse(episodeid == "3-1-5", "3-1.5", episodeid)) %>% 
  separate(episodeid, c("season", "number"), "-") %>% 
  mutate(across(c(season, number), as.numeric)) %>% 
  arrange(doctorid, season, number) -> doctor_who_all_detailsepisodes

doctor_who_all_scripts %>% 
  filter(!grepl("-0[0-9]$", episodeid)) %>%
  filter(!grepl("^[A-Z]|^[a-z]", episodeid)) %>% 
  # "The Infinite Quest", comics episode 
  filter(episodeid != "29-14") %>% 
  # "Vastra Investigates", chrismas Prequel, webcast  
  filter(episodeid != "33-59") %>% 
  # change "3-1-5" to 3-1.5 at the episodeid 
  mutate(episodeid = ifelse(episodeid == "3-1-5", "3-1.5", episodeid)) %>%
  separate(episodeid, c("season", "number"), "-") %>% 
  mutate(across(c(season, number), as.numeric)) %>% 
  arrange(doctorid, season, number) -> doctor_who_all_scripts

doctor_who_imdb_details %>% 
  select(season, number, everything()) %>% 
  # Edit the season count using old season
  mutate(season = season+26) -> doctor_who_imdb_details

doctor_who_dwguide %>% 
  mutate(title = str_replace(title, "The Daleks' Master Plan", "The Dalek's Master Plan")) %>% 
  mutate(title = str_replace(title, "The Dæmons", "The Daemons")) %>% 
  mutate(title = str_replace(title, "Warriors' Gate", "Warrior's Gate")) %>% 
  mutate(title = str_replace(title, "The End of Time:", "The End of Time,")) %>% 
  filter(title != "The TV Movie") %>% 
  arrange(episodenbr) -> doctor_who_dwguide




# Let's see if the titles are the same.
doctor_who_all_detailsepisodes$title -> new_titles
doctor_who_dwguide %>% 
  mutate(title = str_remove(title, ":.*")) %>% pull(title) %>% unique(.) -> new_titles2

new_titles[!(tolower(new_titles) %in% tolower(new_titles2))]
new_titles2[!(tolower(new_titles2) %in% tolower(new_titles))]
# Same! 


# How about "doctor_who_dwguide"? Is it same or not? 
doctor_who_all_detailsepisodes %>% 
  filter(season >= 27) %>% 
  filter(!(toupper(title) %in% toupper(doctor_who_imdb_details$title)))

# Is Is there really no "The End of Time" in doctor_who_imdb_details?
doctor_who_imdb_details %>% 
  filter(season == 30) # Yes

# I don't understand that. Because "The End of Time" series was one of the best episode among the new season.
# So I decided to look up the data about the 7 episodes above in imdb and add them to doctor_who_imdb_details

doctor_who_all_detailsepisodes %>% 
  filter(season >= 27) %>% 
  filter(!(toupper(title) %in% toupper(doctor_who_imdb_details$title))) %>% 
  select(season, number, title) -> add_imdb_details

# I found them! 
add_imdb_details %>% 
  mutate(rating = c(7.4, 7.4, 8.8, 8.2, 8.9, 9.4, 8.4)) %>% 
  mutate(nbr_votes = c(3990, 3945, 5035, 4653, 5258, 16801, 5798)) %>% 
  mutate(description = c("The Doctor arrives in London on Christmas Eve in 1851 where he encounters the Cybermen and a man who claims he's a Time Lord called the Doctor.",
                         "A meeting in a London bus with jewel thief Lady Christina takes a turn for the worst for the Doctor when the bus takes a detour to a desert-like planet, where the deadly Swarm awaits.",
                         "In a Mars base the inhabitants are being infected by a mysterious water creature which takes over its victims. The Doctor is thrust into the middle of this catastrophe knowing a larger one is waiting around the corner.", 
                         "The Ood have given a warning to The Doctor. The Master is returning yet that is not the biggest threat. A darkness is coming which brings with it The End of Time.", 
                         "With almost everyone on Earth now recast in his image, The Master controls the Earth. He's shocked however when he realises one person hasn't changed; Donna Noble. The Doctor soon understands what the pounding in the Master's head is; it's the Time Lords, who are trying to return and re-establish Gallifrey. If they succeed, it'll mean the Last Great Time War will re-start, and all the horrors which came with it. In order to stop Rasillon's mad plan, the Doctor must make a choice. Finally, the Ood's prophecy for the Doctor becomes true, and he takes the TARDIS on a trip, to see friends for one last time, before he's to regenerate.", 
                         "In 2013, something terrible is awakening in London's National Gallery; in 1562, a murderous plot is afoot in Elizabethan England; and somewhere in space an ancient battle reaches its devastating conclusion.", 
                         "The Doctor's worst enemies, The Daleks, The Cybermen, The Angels and The Silence, return, as the doctor's eleventh life comes to a close, and his twelfth life begins.")
  ) -> add_imdb_details

doctor_who_imdb_details %>% 
  bind_rows(add_imdb_details) %>% 
  arrange(season, number) -> doctor_who_imdb_details

# One more check 
doctor_who_all_detailsepisodes %>% 
  filter(season >= 27) %>% 
  filter(!(toupper(title) %in% toupper(doctor_who_imdb_details$title)))


# Add the doctorid to doctor_who_imdb_details
doctor_who_imdb_details %>% 
  left_join(doctor_who_all_detailsepisodes, by = "title", suffix = c(".keep", ".drop")) %>% 
  select(-matches("drop|first|nbr")) %>% 
  # dplyr 1.0.0: select, rename, relocate
  # https://www.tidyverse.org/blog/2020/03/dplyr-1-0-0-select-rename-relocate/
  rename_with(~str_remove(.x, ".keep"), contains("keep")) -> doctor_who_imdb_details

doctor_who_all_detailsepisodes
doctor_who_all_scripts
doctor_who_dwguide
doctor_who_imdb_details

# As so far, I just check the title in each variable and split the episodeid to season and number. 
# What remains is to unify the index between datasets.

## 1.3.2 Index for identify each episdoe
# As I mentioned at 1.3.1, because of different index, These datasets have problem to merge. 
# Except doctor_who_dwguide, three dataset use the episodeid(spliited by two part, season and number) as index. 
# only doctor_who_dwguide uses episodenbr as index. 
# So, Which index would be better? Or how can we unify the indexes, episodeid and episodenbr?
# Honestly, If I analysis about only "new season", all problem will be gone. 
# Because, in only "old season", episodenbr has unique value of each episode but episodeid has unique value of each main title. 
# As all the old season does but here is just one example, the first main title at the first season is An Unearthly Child. 
# In the datasets using "episodeid" as index, An Unearthly Child has index value, "1-1"
# But, In the dataset using "episodenbr" as index, An Unearthly Child has index value according to number of the "sub title".
# In this case, An Unearthly Child has four subtitle from "None" to "The Firemaker". So episodenbr has unique value from 1 to 4 in same maintitle, An Unearthly Child.
# Therefore this problem occur just old season, from the season 1 to season 26, values. 
# Frankly speaking, I'm only going to analyze new season's data, but let's think about analyzing it with all the data to practice EDA.
# Well, How can solve this problem? How can handle this problem?
# In short, Here is just only one way no matter what I choice whether use episodeid or episodenbr because of unbalanced data.
# The one way is that selects both index, episodeid and episodenbr.
# More detail, The way is here, 
# 1) doctor_who_dwguide be added episodeid based on each episode's main title and doctor_who_all_detatilsepisodes
# 2) doctor_who_all_detatilsepisodes be added episodenbr based on each doctor_who_dwguide's first episode of each main title

# Actually I wish I had unification of letter case of title earlier, but it's not too late now.
doctor_who_all_detailsepisodes$title <- toupper(doctor_who_all_detailsepisodes$title)
doctor_who_dwguide$title <- toupper(doctor_who_dwguide$title)
doctor_who_imdb_details$title <- toupper(doctor_who_imdb_details$title)

# First I add season and number(obtained by episodeid) to doctor_whodwguide
doctor_who_dwguide %>% 
  mutate(title = str_remove(string = title, pattern = ":.*")) %>% 
  select(1,2) %>% 
  group_by(title) %>% 
  left_join(doctor_who_all_detailsepisodes, by = "title") %>% 
  ungroup() %>% 
  select(1,3,4,6) %>% 
  left_join(doctor_who_dwguide, by = "episodenbr") -> doctor_who_dwguide

# test of equality between original doctor_who_dwguide and atfer modification one.  
# select(-c(2:4)) %>% 
# all_equal(doctor_who_dwguide) # TRUE, Totally same.

# Next, I add episodenbr(obtained by doctor_who_dwguide) to three datasets  
doctor_who_dwguide %>% 
  mutate(title = str_remove(string = title, pattern = ":.*")) %>% 
  select(1, 5) %>% 
  filter(!duplicated(title)) %>% 
  right_join(doctor_who_all_detailsepisodes, by = "title") -> doctor_who_all_detailsepisodes

# test of equality between original doctor_who_all_detailsepisodes and atfer modification one.  
# select(-1) %>% 
# all_equal(doctor_who_all_detailsepisodes) # TRUE, Totally same. 

doctor_who_dwguide %>% 
  mutate(title = str_remove(string = title, pattern = ":.*")) %>% 
  select(1, 5) %>% 
  filter(!duplicated(title)) %>% 
  right_join(doctor_who_imdb_details, by = "title") -> doctor_who_imdb_details


doctor_who_dwguide %>% 
  filter(episodenbr %in% c(728, 729, 745, 777, 795, 817, 840, 841)) %>% 
  pull(doctorid) -> putinimdb


doctor_who_imdb_details$doctorid[which(is.na(doctor_who_imdb_details$doctorid))] <- putinimdb

# test of equality between original doctor_who_imdb_details and atfer modification one.  
# select(-1) %>%
# all_equal(doctor_who_imdb_details) # TRUE, Totally same.

doctor_who_all_scripts %>% 
  left_join(doctor_who_all_detailsepisodes, by = c("season", "number", "doctorid")) %>% 
  select(-first_diffusion) -> doctor_who_all_scripts

# test of equality between original doctor_who_all_scripts and atfer modification one.  
# select(-(8:10)) %>% 
# all_equal(doctor_who_all_scripts) # TRUE, Totally same.



# For the readability, unify the columns 
doctor_who_dwguide %>% 
  select(episodenbr, season, number, doctorid, title, everything()) -> doctor_who_dwguide

doctor_who_all_detailsepisodes %>% 
  select(episodenbr, season, number, doctorid, title, everything()) -> doctor_who_all_detailsepisodes

doctor_who_imdb_details %>% 
  select(episodenbr, season, number, doctorid, title, everything()) %>% 
  # This is wrong. episodenbr 804, Twice Upon a Time is the last episode of 12th doctor. 
  # Even if appear new doctor, 13th doctor, this is wrong numbering. 
  mutate(season = ifelse(episodenbr == 840, 36, season)) %>% 
  mutate(number = ifelse(episodenbr == 840, 13, number)) -> doctor_who_imdb_details

doctor_who_all_scripts %>% 
  select(episodenbr, season, number, doctorid, title, idx, everything()) -> doctor_who_all_scripts

# Let's check 
doctor_who_dwguide
doctor_who_all_detailsepisodes
doctor_who_imdb_details
doctor_who_all_scripts

# This is end of Handling the index part. 
# In next part, I will extract the "new season" data at these four dataset and then analysis. 

#### 2. Analysis ####
# Before the analysis I should extract the "new season" data.
doctor_who_dwguide %>% 
  filter(season >= 27) -> new_doctor_who_dwguide

doctor_who_all_detailsepisodes %>% 
  filter(season >= 27) -> new_doctor_who_all_detailsepisodes

doctor_who_imdb_details %>% 
  filter(season >= 27) -> new_doctor_who_imdb_details

doctor_who_all_scripts %>% 
  filter(season >= 27) -> new_doctor_who_all_scripts

# Note that some episodes is missing in the doctor_who_all_scripts.
# As below result, new_doctor_who_all_scripts has 137 episode not 155 episode which included in other dataset
new_doctor_who_all_scripts %>% 
  count(episodenbr) # 137 unique episodenbr


# some practice 
# Which one is the best or worst episode(based on some metric) for each season and doctor
new_doctor_who_dwguide %>% 
  mutate(share = as.numeric(str_remove(share, "%"))) %>% 
  # select the season or doctor
  group_by(season) %>% 
  # group_by(doctorid) %>% 
  
  # select the metric
  
  # filter(AI == max(AI)) %>% 
  # filter(AI == max(views)) %>% 
  # filter(AI == max(chart)) %>% 
  filter(share == max(share)) %>% 
  
  select(season, number, doctorid, title, AI, views, share, chart)


# Now I'm ready to analyze.
### 2.1 Drawing some plots
# Barplot to show difference of number of episode for each season and doctor
new_doctor_who_dwguide %>% 
  mutate(season = season-26) %>% 
  mutate(episodenbr = episodenbr - min(episodenbr) + 1) %>% 
  group_by(doctorid) %>% 
  count(season) %>% 
  ggplot(aes(x = season, y = n, color = factor(doctorid), fill = factor(doctorid))) +
  geom_bar(stat = "identity") + 
  labs(color = "Doctor",
       fill = "Doctor",
       x = "Season", 
       y = "Number of Episodes") + 
  theme_minimal() +
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Number of Episodes for Each Season and Doctor")

## 2.1.1 Using lineplot part
lineplot <- function(dataset, x, y, color) { 
  
  lineplot <- dataset %>% 
    mutate(season = season-26) %>% 
    mutate(episodenbr = episodenbr - min(episodenbr) + 1) %>% 
    # https://stackoverflow.com/questions/58786357/how-to-pass-aes-parameters-of-ggplot-to-function
    # https://adv-r.hadley.nz/evaluation.html#tidy-evaluation
    ggplot(aes(x = {{x}}, y = {{y}}, color = factor({{color}}))) +
    geom_line() + 
    geom_point() + 
    theme_minimal()
  return(lineplot)
  
  }

# To show that rating trend for each season
lineplot(new_doctor_who_imdb_details, x = episodenbr, y = rating, color = season) + 
  labs(color = "Season", 
       x = "Episode number", 
       y = "Rating") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Rating Trend for Each Season")

# To show that rating trend for each doctor
lineplot(new_doctor_who_imdb_details, x = episodenbr, y = rating, color = doctorid) + 
  labs(color = "Doctor",
       x = "Episode number", 
       y = "Rating") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Rating Trend for Each Doctor")

# To show that AI(Appreciation Index) trend for each doctor
lineplot(new_doctor_who_dwguide, x = episodenbr, y = AI, color = doctorid) + 
  labs(color = "Season", 
       x = "Episode number", 
       y = "Rating") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Rating Trend for Each Season")

# To show that views trend for each doctor
lineplot(new_doctor_who_dwguide, x = episodenbr, y = views, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Episode number", 
       y = "Views") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "View Trend for Each Season")

# To show that chart trend for each doctor
lineplot(new_doctor_who_dwguide, x = episodenbr, y = chart, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Episode number", 
       y = "Chart") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Chart Trend for Each Season")

## 2.1.2 Using boxplot part
boxplot <- function(dataset, x, y, color) { 
  
  boxplot <- dataset %>% 
    mutate(season = season-26) %>% 
    mutate(episodenbr = episodenbr - min(episodenbr) + 1) %>% 
    # https://stackoverflow.com/questions/58786357/how-to-pass-aes-parameters-of-ggplot-to-function
    # https://adv-r.hadley.nz/evaluation.html#tidy-evaluation
    ggplot(aes(x = factor({{x}}), y = {{y}})) +
    geom_boxplot(aes(fill = factor({{color}}))) + 
    theme_minimal()
  
  return(boxplot)
  
}

# Using boxplot, To show that rating trend for each doctor
boxplot(new_doctor_who_imdb_details, x = season, y = rating, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Season", 
       y = "Rating") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Boxplot Showing Rating Trend for Each Season and Doctor")

# Using boxplot, To show that AI(Appreiciation Index) trend for each doctor
boxplot(new_doctor_who_dwguide, x = season, y = AI, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Season", 
       y = "Rating") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Boxplot Showing AI Trend for Each Season and Doctor")

# Using boxplot, To show that views trend for each doctor
boxplot(new_doctor_who_dwguide, x = season, y = views, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Season", 
       y = "Views") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Box Plot Showing View Trend for Each Season and Doctor")

# Using boxplot, To show that chart trend for each doctor
boxplot(new_doctor_who_dwguide, x = season, y = chart, color = doctorid) + 
  labs(fill = "Doctor",
       x = "Season", 
       y = "Chart") + 
  theme(legend.position = "bottom", 
        plot.title = element_text(face = "bold", hjust = 0.5, size = 13)) + 
  ggtitle(label = "Box Plot Showing Chart Trend for Each Season and Doctor")


```
