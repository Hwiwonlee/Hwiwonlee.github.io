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
# Show the labels of the first 10 records
mnist_sample$label[1:10]

# Compute the Euclidean distance of the first 10 records
distances <- dist(mnist_sample[1:10, -1])

# Show the distances values
distances

# Plot the numeric matrix of the distances in a heatmap
heatmap(as.matrix(distances), 
    	Rowv = NA, symm = TRUE, 
        labRow = mnist_sample$label[1:10], 
        labCol = mnist_sample$label[1:10])
        
# Minkowski distance or order 3
distances_3 <- dist(mnist_sample[1:10, -1], method = "minkowski", p = 3)
distances_3
heatmap(as.matrix(distances_3), 
        Rowv = NA, symm = TRUE, 
        labRow = mnist_sample$label[1:10], 
        labCol = mnist_sample$label[1:10])

# Minkowski distance of order 2
distances_2 <- dist(mnist_sample[1:10, -1], method = "minkowski", p = 2)
distances_2
heatmap(as.matrix(distances_2), 
        Rowv = NA, symm = TRUE, 
        labRow = mnist_sample$label[1:10], 
        labCol = mnist_sample$label[1:10])
        
# Get the first 10 records
mnist_10 <- mnist_sample[1:10, -1]

# Add 1 to avoid NaN when rescaling
mnist_10_prep <- mnist_10 + 1

# Compute the sums per row
sums <- rowSums(mnist_10_prep)

# Compute KL divergence
distances <- distance(mnist_10_prep/sums, method = "kullback-leibler")
heatmap(as.matrix(distances), 
        Rowv = NA, symm = TRUE, 
        labRow = mnist_sample$label[1:10], 
        labCol = mnist_sample$label[1:10])
```

### PCA and t-SNE

```r
# Get the principal components from PCA
pca_output <- prcomp(mnist_sample[, -1])

# Observe a summary of the output
summary(pca_output)

# Store the first two coordinates and the label in a data frame
pca_plot <- data.frame(pca_x = pca_output$x[, 1], pca_y = pca_output$x[, 2], 
                       label = as.factor(mnist_sample$label))

# Plot the first two principal components using the true labels as color and shape
ggplot(pca_plot, aes(x = pca_x, y = pca_y, color = label)) + 
	ggtitle("PCA of MNIST sample") + 
	geom_text(aes(label = label)) + 
	theme(legend.position = "none")

# t-SNE를 직접 시행하지는 않는다. 
# Explore the tsne_output structure
str(tsne_output)

# Have a look at the first records from the t-SNE output
head(tsne_output$Y)

# Store the first two coordinates and the label in a data.frame
tsne_plot <- data.frame(tsne_x = tsne_output$Y[, 1], tsne_y = tsne_output$Y[, 2], 
                        label = as.factor(mnist_sample$label))

# Plot the t-SNE embedding using the true labels as color and shape
ggplot(tsne_plot, aes(x = tsne_x, y = tsne_y, color = label)) + 
	ggtitle("T-Sne output") + 
	geom_text(aes(label = label)) + 
	theme(legend.position = "none")
```
