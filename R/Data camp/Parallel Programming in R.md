## Partitioning by task or by data  
1. Partitioning by task : 목적에 따른 결과를 내기 위해 function을 정의하고 내부에 각 과정을 nested function으로 정의하는 방법.  
2. Partitioning by data : 하나의 dataset을 병렬적으로 처리(혹은 계산)하는 방법.  

```r
library(janeaustenr)
library(stringr)

# Vector of words from all six books
words <- janeausten_words()

# Most frequent "a"-word that is at least 5 chars long
max_frequency(letter = "a", words = words, min_length = 5)

# Partitioning
result <- lapply(letters, max_frequency,
                words = words, min_length = 5) %>% unlist()

# Barplot of result
barplot(result, las = 2)
```

## Models of parallel computing  
1. Programming paradigms  
- Master-worker : 기본적이지만 유용한 병렬처리 방식  
- Map-reduce paradigm : 분산된 data를 처리하기 위한 방식, hadoop, spark에서 유용, **Scalable data processing in R cource**에서 배울 수 있음.  

```r
n_replicates <- 50
n_numbers_per_replicate <- 10000

# From previous step
mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

# Create a vector to store the results
result <- rep(NA, n_replicates)

# Set the random seed to 123
set.seed(123)

# Set up a for loop with iter from 1 to n_replicates
for(iter in 1:n_replicates) {
  # Call mean_of_rnorm with n_numbers_per_replicate
  result[iter] <- mean_of_rnorm(n_numbers_per_replicate)
}

# View the result
hist(result)


# Repeat n_numbers_per_replicate, n_replicates times
n <- rep(n_numbers_per_replicate, n_replicates)

# Call mean_of_rnorm() repeatedly using sapply()
result <- sapply(
  # The vectorized argument to pass
  n, 
  # The function to call
  mean_of_rnorm
)

# View the results
hist(result)

```



```r
# Function definition of ar1_multiple_blocks_of_trajectories()
ar1_multiple_blocks_of_trajectories <- function(ids, ...) {
  # Call ar1_block_of_trajectories() for each ids
  trajectories_by_block <- lapply(ids, ar1_block_of_trajectories, ...)
  
  # rbind results
  do.call(rbind, trajectories_by_block)
}

# Create a sequence from 1 to number of blocks
traj_ids <- seq_len(nrow(ar1est)) # 1:nrow(ar1est)와 같음

# Generate trajectories for all rows of the estimation dataset
trajs <- ar1_multiple_blocks_of_trajectories(
  ids = traj_ids, rate0 = 0.015,
  block_size = 10, traj_len = 15
)

# Show results
show_migration(trajs)


```
