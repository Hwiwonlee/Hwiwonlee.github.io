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
#### Distance metrics to compute similarity
The similarity between MNIST digits can be computed using a distance metric.    
A metric is a function that for any given points,x, y, z the output satises:    
  1. **Triangle inequality**: *d(x, z)* ≤ *d(x, y)* + *d(y, z)*  
  2. **Symmetric property**: *d(x, y)* = *d(y, x)*  
  3. **Non-negativity and identity**: *d(x, y)* ≥ 0 and *d(x, y)* = 0 only *if x = y*  

#### Minkowski family of distances
Minkowski : d= (&sum;|P<sub>i</sub>-Q<sub>i</sub>|<sup>p</sup>)<sup>1/p</sup>  
  - For example, if p equal to 1 then d same as Manhattan distance, if p equal to 2 then d same as Euclidean distance.
  
#### Kullback-Leibler (KL) divergence  
  - Not a metric since it does not satisfy the symmetric and triangle inequality properties  
  - Measures differences in probability distributions  
  - A divergence of 0 indicates that the two distributions are identical  
  - A common distance metric in Machine Learning (t-SNE). For example, in decision trees it is called *Information Gain*  

Kullback-Leibler (KL) divergence은 기본 개념정도만 알고 넘어갔었는데 한 번 제대로 알아보는 것도 의미있을 것 같다. 
```r

```
