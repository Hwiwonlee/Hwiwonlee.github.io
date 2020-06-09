## foreach package
#### What is foreach for?
- Developed by Rich Calaway and Steve Weston.
- Provides a new looping construct for repeated execution.
- Supports running loops in parallel.
- Unified interface for sequential and parallel processing.
- Greatly suited for embarrassingly parallel applications.
- Can use lsit comprehension like python.

#### Word frequency with foreach
```r
# Object words is a vector of all words from the included books in the janeaustenr package 

# Using lapply function 
result <- lapply(letters, max_frequency,
            words = words, min_length = 5) %>% unlist

# Using foreach function
# foreach() %do% construct
result <- foreach(let = letters, .combine = c) %do% 
                max_frequency(let, words = words, min_length = 5)
                
# Plot results 
barplot(result, las = 2)

# foreach()%do% construct with 2 iterators
# Use the iterator n to define multiple values of the min_length argument. It is equal to 2 in the first 13 iterations and equal to 6 in the last 13 iterations. 
result <- foreach(let = letters, n = c(rep(2, 13), rep(6,13)), .combine = c) %do%
                max_frequency(let, words = words, min_length = n)
            
# Plot results
barplot(result, las = 2)

```


#### Using doParallel
In one of the previous exercises, you parallelized the function myrdnorm() which uses the package extraDistr to generate discrete random numbers. Here you will implement a parallel foreach solution to the same problem, using the doParallel backend. doParallel provides an argument .packages which ensures that external packages are loaded on all nodes.

```r
# Register doParallel with 3 cores
registerDoParallel(cores = 3)

# foreach()%dopar% loop
res <- foreach(r = rep(1000, 100), .combine = rbind, 
            .packages = "extraDistr") %dopar% myrdnorm(r)
# Another useful option in addition to .packages is .export for exporting objects from master to workers.

# Dimensions of res
dim_res <- dim(res)
```

#### Word frequency with doParallel
```r
# Function for doParallel foreach
freq_doPar <- function(cores, min_length  = 5) {
    # Register a cluster of size cores
    registerDoParallel(cores = cores)
    
    # foreach loop
    foreach(let = chars, .combine = c, 
            .export = c("max_frequency", "select_words", "words"),
            .packages = c("janeaustenr", "stringr")) %dopar%
        max_frequency(let, words = words, min_length = min_length)
}

# Run on 2 cores
freq_doPar(cores = 2)
```

#### Word frequency with doFuture and benchmarking
```r
# Function for doFuture foreach
freq_doFut <- function(cores, min_length = 5) {
    # Register and set plan
    registerDoFuture()
    plan(cluster, workers = cores)
    
    # foreach loop
    foreach(let = chars, .combine = c) %dopar% 
        max_frequency(let, words = words, min_length = min_length)
}

# Benchmark
microbenchmark(freq_seq(min_length), 
               freq_doPar(cores, min_length), 
               freq_doFut(cores, min_length),
               times = 1)
               
# 소요시간 : freq_doPar < freq_seq < freq_doFut               
```

### Future and future.apply package
#### Word frequency with future.apply
```r
# Main function
freq_fapply <- function(words, chars = letters, min_length = 5) {
    unlist(
        future_lapply(chars, max_frequency, words = words, 
                         min_length = min_length)
    )
}

# Extract words
words <- extract_words_from_text(obama_speech)

# Call the main function
res <- freq_fapply(words)

# Plot results
barplot(res, las = 2)
```

#### Planning future
```r
# multicore function
fapply_mc <- function(cores = 2, ...) {
    # future plan
    plan(multicore, workers = cores)
    freq_fapply(words, chars, ...)
}

# cluster function
fapply_cl <- function(cores = NULL, ...) {
    # default value for cores
    if(is.null(cores))
        cores <- rep(c("oisin", "oscar"), each = 16)
        
    # future plan
    plan(cluster, workers = cores)
    freq_fapply(words, chars, ...)
}
```

```r
# Microbenchmark
microbenchmark(fapply_seq = fapply_seq(),
               fapply_mc_2 = fapply_mc(2), 
               fapply_mc_10 = fapply_mc(10),
               fapply_cl = fapply_cl(2), 
               times = 1)
# fapply_cl is slowest one
```

### Load balancing and scheduling
#### Load balancing
```r
# Benchmark clusterApply and clusterApplyLB
microbenchmark(
    clusterApply(cl, tasktime, Sys.sleep),
    clusterApplyLB(cl, tasktime, Sys.sleep),
    times = 1
)

# Plot cluster usage
plot_cluster_apply(cl, tasktime, Sys.sleep)
plot_cluster_applyLB(cl, tasktime, Sys.sleep)
```
#### Scheduling
```r
# bias_tasktime that generates very uneven load.
# Plot cluster usage for parSapply
plot_parSapply(cl, tasktime, Sys.sleep)

# Microbenchmark
microbenchmark(
    clusterApplyLB(cl, bias_tasktime, Sys.sleep),
    parSapply(cl, bias_tasktime, Sys.sleep),
    times = 1
)

# Plot cluster usage for parSapply and clusterApplyLB
plot_parSapply(cl, bias_tasktime, Sys.sleep)
plot_cluster_applyLB(cl, bias_tasktime, Sys.sleep)
```
