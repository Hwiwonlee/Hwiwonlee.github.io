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

### Exploring the cluster object  
- str(cl) : cl에 대한 structure 확인. socket과 같은 backend setting도 알아두면 좋을 듯.  
  - SOCK은 OS에 상관없이 사용가능하므로 default로 설정되어 있음.  
- clusterCall : lapply()처럼 object, function으로 사용가능. Sys.getpid로 cluster에 할당된 id를 확인.  
```r
# Load the parallel package
library(parallel)

# Make a cluster with 4 nodes
cl <- makeCluster(4)

# Investigate the structure of cl
str(cl)

# What is the process ID of the workers?
clusterCall(cl, Sys.getpid)

# Stop the cluster
stopCluster(cl)
```

### Socket vs Fork
- Socket : The socket cluster failed to print a_global_var because Workers in a socket cluster start with an empty environment. Thus, a_global_var was not defined.  
- Fork : The fork cluster did not update a_global_var after it was updated because Workers in a fork cluster start with a copy of the master environment. After forking, they do not see changes on the master. Thus, a_global_var was not updated.  
```r
# type = "PSOCK"
# A global variable and is defined
a_global_var <- "before"

# Create a socket cluster with 2 nodes
cl_sock <- makeCluster(2, type = "PSOCK")

# Evaluate the print function on each node
clusterCall(cl_sock, print_global_var)

# Stop the cluster
stopCluster(cl_sock)
```
```r
# type = "FORK"
# A global variable and is defined
a_global_var <- "before"

# Create a fork cluster with 2 nodes
cl_fork <- makeCluster(2, type = "FORK")

# Change the global var to "after"
a_global_var <- "after"

# Evaluate the print fun on each node again
clusterCall(cl_fork, print_global_var)

# Stop the cluster
stopCluster(cl_fork)
```

### The core of parallel  
#### Parallel vs. Sequential  
Not all embarrassingly parallel aplications are suited for parallel processing.
##### Processing overhead:  
- Starting/stopping cluster
- Number of messages sent between nodes and master
- Size of messages (sending big data is expensive)
##### Things to consider:  
- How big is a single task (green bar)
- How much data need to be sent
- How much gain is there by running it in parallel ⟶ benchmark
  - 아래 예제에서 볼 수 있듯, dataset의 크기가 작고 반복수가 늘어나면 sequential process의 benchmark가 더 좋게 나온다. 

```r
mean_of_rnorm_sequentially <- function(n_numbers_per_replicate, n_replicates) { 
  n <- rep(n_numbers_per_replicate, n_replicates)
  lapply(n, mean_of_rnorm)
}
mean_of_rnorm_in_parallel <- function(n_numbers_per_replicate, n_replicates) { 
  n <- rep(n_numbers_per_replicate, n_replicates)
  clusterApply(cl, n, mean_of_rnorm) 
}

# Set numbers per replicate to 5 million
n_numbers_per_replicate <- 5000000

# Set number of replicates to 4
n_replicates <- 4

# Run a microbenchmark
microbenchmark(
  # Call mean_of_rnorm_sequentially()
  mean_of_rnorm_sequentially(n_numbers_per_replicate, n_replicates), 
  # Call mean_of_rnorm_in_parallel()
  mean_of_rnorm_in_parallel(n_numbers_per_replicate, n_replicates),
  times = 1, 
  unit = "s"
)

# Change the numbers per replicate to 100
n_numbers_per_replicate <- 100

# Change number of replicates to 100
n_replicates <- 100

# Rerun the microbenchmark
microbenchmark(
  mean_of_rnorm_sequentially(n_numbers_per_replicate, n_replicates), 
  mean_of_rnorm_in_parallel(n_numbers_per_replicate, n_replicates),
  times = 1, 
  unit = "s"
)
```

### Initialization of nodes
- Each cluster node starts with an empty environment (no libraries loaded).  
- Repeated communication with the master is expensive.  
  - Example:  
  ```r
  clusterApply(cl, rep(1000, n), rnorm, sd = 1:1000)
  ```
    Master sends a vector of 1:1000 to all n tasks (n can be very large).  

- Good practice: Master initializes workers at the beginning with everything that stays constant or/and is time consuming. Examples:  
  - sending static data    
  - loading libraries  
  - evaluating global functions  

#### Loading package on nodes  
```r
# From previous step
myrdnorm <- function(n, mean = 0, sd = 1) 
    rdnorm(n, mean = mean, sd = sd)
n_numbers_per_replicate <- 1000
n_replicates <- 20
n <- rep(n_numbers_per_replicate, n_replicates)

# Load extraDistr on master
library(extraDistr)

# Load extraDistr on all workers
clusterEvalQ(cl, 
  library(extraDistr)
)

# Run myrdnorm in parallel. It should work now!
res <- clusterApply(cl, n, myrdnorm)

# Plot the result
plot(table(unlist(res)))
```

#### Exporting global objects using clusterExport()  
```r
# Set global objects on master: mean to 20, sd to 10
mean <- 20
sd <- 10

# Load extraDistr on workers
clusterEvalQ(cl, 
  library(extraDistr)
)

# Export global objects to workers
clusterExport(cl, c("mean", "sd"))

# Run myrdnorm in parallel
res <- clusterApply(cl, n, myrdnorm)

# Plot the results
plot(table(unlist(res)))
```
