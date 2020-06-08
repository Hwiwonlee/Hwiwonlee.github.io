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
# preloading function : show_migration

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


```r
# From previous step
library(parallel)
ncores <- detectCores(logical = FALSE)
n <- ncores:1

# Use lapply to call rnorm for each n,
# setting mean to 10 and sd to 2 
lapply(n, rnorm, mean = 10, sd = 2)


# Using cluster for parallel computing
# Create a cluster
cl <- makeCluster(ncores)

# Use clusterApply to call rnorm for each n in parallel,
# again setting mean to 10 and sd to 2 
clusterApply(cl, x = ncores:1, fun = rnorm, mean = 10, sd = 2)

# Stop the cluster
stopCluster(cl)
```

### Sum in parallel  
summation을 두 부분으로 나눠서 병렬처리  
```r
# Evaluate partial sums in parallel
part_sums <- clusterApply(cl, x = c(1, 51),
                    fun = function(x) sum(x:(x + 49)))
# Total sum
total <- sum(unlist(part_sums))

# Check for correctness
total == sum(1:100)

```

### More tasks than workers  
rnorm()을 이용해, 10000번의 random sampling을 시행한 후 평균을 구하는 mean_of_rnorm를 50번 반복하는 작업을 병렬처리.  
```r
# Create a cluster and set parameters
cl <- makeCluster(2)
n_replicates <- 50
n_numbers_per_replicate <- 10000

# Parallel evaluation on n_numbers_per_replicate, n_replicates times
means <- clusterApply(cl, 
             x = rep(n_numbers_per_replicate, n_replicates), 
             fun = mean_of_rnorm)
                
# View results as histogram
hist(unlist(means))
```
