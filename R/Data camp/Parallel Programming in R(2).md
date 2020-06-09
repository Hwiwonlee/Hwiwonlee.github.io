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
