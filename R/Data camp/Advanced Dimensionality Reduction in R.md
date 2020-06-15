## Introduction to Advanced Dimensionality Reduction  
### Exploring the MNIST dataset  
Why do we need dimensionality reduction techniques?  
  - t-Distributed Stochastic Neighbor Embedding (t-SNE)  
  - Generalized Low Rank Models (GLRM)  
Advantages of dimensionality reduction techniques:  
  1) Feature selection  
  2) Data compressed into a few important features  
  3) Memory-saving and speeding up of machine learning models  
  4) Visualisation of high dimensional datasets  
  5) Imputing missing data (GLRM)  
```r
# Have a look at the MNIST dataset names
names(mnist_sample)

# Show the first records
str(mnist_sample)

# Labels of the first 6 digits
head(mnist_sample$label)

# Plot the histogram of the digit labels
hist(mnist_sample$label)

# Compute the basic statistics of all records
summary(mnist_sample)

# Compute the basic statistics of digits with label 0
summary(mnist_sample[, mnist_sample$label == 0])
```

### Distance metrics


```r

```
