```r
data_BN <- read.xlsx("...BN_mastersheet.xlsx", sheetIndex = 1)
data_MN <- read.xlsx("...MN_mastersheet.xlsx", sheetIndex = 1)


colnames(data_BN)[1:6] <- c("Name", "NO", "Group", "Group_RN", "Batch", "Order")
colnames(data_MN)[1:4] <- c("Name", "NO", "Group", "Group_RN")

data_BN <- data_BN[-1, ]
data_MN <- data_MN[-1, ]

data_BN %>% 
  as_tibble() %>% 
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_BN
  # group_by(Group) %>% summarise(n = n())

data_MN %>% 
  as_tibble() %>% 
  mutate(Group = replace(Group, str_detect(Group, "-131"), "OC")) %>% 
  mutate(Group = replace(Group, str_detect(Group, "-51"), "OC")) -> data_MN
  # group_by(Group) %>% summarise(n = n())


data_BN %>% 
  group_by(Group) %>%  summarise(n=n())

data_1 %>% 
  group_by(group1) %>%  summarise(n=n())


group_value = c("C", "OC")
#### ####

#### 1 vs 1 이므로 Comparison pair에 대한 반복 없음 ####
result = combn(group_value, 1)

# all metabolites 
cm <- colnames(data_BN)[-(1:6)]

# KBSI suggested metabolites
cm <- c("Acetylcarnitine", "Deca.carnitine", "Hex.carnitine", "Iso.carnitine", "Oct.carnitine", "Glutamate", "sn.glycerol.3.phosphocholine", "TMAO")
a <- ".Results"
cm <- paste0(cm, a)

# set names for saving plots 
folder_name <- "...graph_output/"
file_name <- "testplot"

data_BN %>% 
  as_tibble() %>% 
  dplyr::filter(Group %in% result) %>% 
  mutate(group1 = ifelse(Group %in% result[1, 1], 0, 1)) %>% 
  select(Group, group1, everything()) %>% 
  select(group1, cm) %>% 
  type_convert(cols(X3_hydroxybutyrate.Results = col_double())) -> data_1 

for( i in 1:length(cm) ) {
  numbering <- i
  png_name <- paste0(folder_name, file_name, "_" , paste(result[1, 1]),
                     "_VS_", paste(result[1, 2]), "_", paste(cm[i]), ".png")
  
  png(png_name, width = 750, height = 750, pointsize = 20)
  
  ROC(form = as.formula(paste(colnames(data_1)[1], "~", cm[i])), data = data_1, plot="ROC")
  
  dev.off()
}

#### ####

```
