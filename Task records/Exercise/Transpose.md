```r
# library
library(xlsx)

# pre : import data set 
dir <- "..."
transpose_data <- read.csv2(paste(dir,"transpose.csv", sep = "/"), header = TRUE, sep = ",")


# pre : cut useless column 
transpose_data <- transpose_data[, -2]
transpose_data <- transpose_data[-7655, ]

# pre : 등록번호와 수진일의 중복 파악
transpose_data %>% 
  as_tibble() %>% 
  select(c(1,2)) %>% 
  group_by(등록번호) %>% 
  unique() %>% 
  ungroup() -> head

# 없는 것으로 판단됨
# *이게 spread 상태의 index와 날짜의 형태

# pre : Esophagogastroduodenoscopy가 두 번 시행되는 것을 확인
# 하나는 _1로 하나는 _2로 수정해야 함. 

# Esophagogastroduodenoscopy를 포함하는 검사명의 index 추출
c <- c()
for (i in 1:nrow(transpose_data)) { 
  if (transpose_data$검사명[i] == "Esophagogastroduodenoscopy") { 
    c <- c(c,i)
  }
}
# index를 이용해 _1, _2로 수정 
transpose_data$검사명[c] <- c("Esophagogastroduodenoscopy_1", "Esophagogastroduodenoscopy_2") 
  

# pre : 검사명 만큼의 null data frame 추가 
test <- data.frame(matrix("", nrow(head), length(unique(transpose_data$검사명))))
colnames(test) <- unique(transpose_data$검사명)

# pre : 검사명_판정문으로 검사갯수만큼의 column을 가진 null data frame 추가 
paste0(unique(transpose_data$검사명), "_판정문")
diagnosis <- matrix("", nrow(head), length(paste0(unique(transpose_data$검사명), "_판정문")))
colnames(diagnosis) <- unique(paste0(unique(transpose_data$검사명), "_판정문"))

# pre : transpose틀 완성
data <- cbind(head, test, diagnosis)
colnames(data)[-c(1,2)] <- sort(colnames(data)[-c(1,2)])

transpose_test <- function(data, index_column, return_data) { 
  
  index <- unique(data[, index_column])
  
  for (i in 1:length(index)) { 
    # https://stackoverflow.com/questions/27197617/filter-data-frame-by-character-column-name-in-dplyr
    data %>% 
      dplyr::filter(!!as.symbol(index_column) == index[i]) -> subset
    
    for ( j in 1:nrow(subset)) { 
      
      which_index <- which(subset$검사명[j] == colnames(return_data))
      return_data[i, which_index] <- subset$검사결과[j]
      
      if(which_index != 0) {
        return_data[i, (which_index + 1) ] <- subset$판정문[j]
        
      }
    }
  }
  
  return(return_data)
  
}


test_0316 <- transpose_test(data = transpose_data, index_column = "등록번호", return_data = data)
transpose_result <- apply(test_0316, MARGIN = 2, function(x) {gsub("\n$", "", x)})
transpose_result %>% 
  write.csv("transpose_result.csv")

```

```r
#### test and check ####
unique(transpose_data$등록번호)
length(unique(transpose_data$등록번호)) # end of i

# 등록번호로 subset 설정 
transpose_data %>% 
  dplyr::filter(등록번호 == some_integer) -> subset

# for문 예시 
# index of for 
i <- 1 # i번째 obs
j <- 1 # j번째 검사

# subset의 j번째 검사명과 data의 검사명이 같은가? 
subset$검사명[j] == colnames(data)

# subset의 j번째 검사명과 data의 검사명이 같은 위치는? 
which(subset$검사명[j] == colnames(data))

# i번째 obs의 subset의 j번째 검사명과 data의 검사명이 같은 위치에 검사결과를 넣기
data[i, which(subset$검사명[j] == colnames(data))] <- subset$검사결과[j]


for(j in 1:nrow(subset)) {
  index <- which(subset$검사명[j] == colnames(data))
  data[i, which(subset$검사명[j] == colnames(data))] <- subset$검사결과[j]
  if(index != 0) {
    data[i, which(subset$검사명[j] == colnames(data)) + 1 ] <- subset$판정문[j]
  }
}

data[1, ] # 작동 확인, 넣은 값에 오류 없음
a <- 등록번호

class(transpose_data[, a])
class(transpose_data$등록번호)

index <- unique(transpose_data[, "등록번호"])

for (i in 1:length(index)) { 
  
  transpose_data %>% 
    dplyr::filter(등록번호 == index[i]) -> subset
  
  for ( j in 1:nrow(subset)) { 
    
    which_index <- which(subset$검사명[j] == colnames(data))
    data[i, which_index] <- subset$검사결과[j]
    if(which_index != 0) {
      data[i, (which_index + 1) ] <- subset$판정문[j]
      
    }
  }
}



```
