
Comparing read times of CSV and RDS files using system.time()
```r
# How long does it take to read movies from CSV?
system.time(read.csv("movies.csv"))

# How long does it take to read movies from RDS?
system.time(readRDS("movies.rds"))
```

Elapsed time
- Using system.time() is convenient, but it does have its drawbacks when comparing multiple function calls. The microbenchmark package solves this problem with the microbenchmark() function.

```r
# Load the microbenchmark package
library(microbenchmark)

# Compare the two functions
compare <- microbenchmark(read.csv("movies.csv"), 
                          readRDS("movies.rds"), 
                          times = 10)

# Print compare
print(compare)

```

Memory allocation
- R code의 실행 자체를 빠르게 만들 수는 없지만 code를 어떻게 짜느냐에따라 속도가 좌우되기도 한다. 목적과 결과는 같지만 더 빠른 길이 존재한다는 것이다. 
```r
n <- 30000
# Slow code
growing <- function(n) {
    x <- NULL
    for(i in 1:n)
        x <- c(x, rnorm(1))
    x
}

n <- 30000
# Fast code
pre_allocate <- function(n) {
    x <- numeric(n) # Pre-allocate
    for(i in 1:n) 
        x[i] <- rnorm(1)
    x
}

system.time(res_growing <- growing(n = 30000))
system.time(res_allocate <- pre_allocate(n = 30000))


```

Profiling a function
- profvis package의 profvis() 알아보기 
```r
# Load the data set
data(movies, package = "ggplot2movies") 

# Load the profvis package
library(profvis)

# Profile the following code with the profvis function
profvis({
  # Load and select data
  comedies <- movies[movies$Comedy == 1, ]

  # Plot data of interest
  plot(comedies$year, comedies$rating)

  # Loess regression line
  model <- loess(rating ~ year, data = comedies)
  j <- order(comedies$year)
  
  # Add fitted line to the plot
  lines(comedies$year[j], model$fitted[j], col = "red")
})     ## Remember the closing brackets!

```

Moving to parApply
To run code in parallel using the parallel package, the basic workflow has three steps.

1. Create a cluster using makeCluster().
2. Do some work.
3. Stop the cluster using stopCluster().
The simplest way to make a cluster is to pass a number to makeCluster(). This creates a cluster of the default type, running the code on that many cores.

The object dd is a data frame with 10 columns and 100 rows. The following code uses apply() to calculate the column medians:

apply(dd, 2, median)
To run this in parallel, you swap apply() for parApply(). The arguments to this function are the same, except that it takes a cluster argument before the usual apply() arguments.

```r
# Determine the number of available cores
detectCores()

# Create a cluster via makeCluster
cl <- makeCluster(2)

# Parallelize this code
parApply(cl, dd, 2, median)

# Stop the cluster
stopCluster(cl)

```
