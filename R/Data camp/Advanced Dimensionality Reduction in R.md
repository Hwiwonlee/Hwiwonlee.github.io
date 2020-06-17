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

## Introduction to t-SNE
### Building a t-SNE embedding
#### Introduction to t-SNE
  - Published by Van der Maaten & Hinton in 2008  
  - Non-linear dimensionality reduction technique  
  - Works well for most ofthe problems and is a very good method for visualizing high dimensional datasets  
  - Rather than keeping dissimilar points apart (like PCA) it keeps the low-dimensional representation of similar points together  
  
#### t-SNE method
  1. Use PCA to reduce the input dimensions into a small number  
  2. Construct a probability distribution over pairs of original high dimensional records  
  3. Dene a similarity probability distribution ofthe points in the low-dimensional embedding  
  4. Minimize theK-L divergence between the two distributions using gradient descent method  

embedding이라는 단어가 낯설어서 찾아봤더니 의미가 모호하고 그 의미조차 분야마다 다르다. 아마 [wiki](https://en.wikipedia.org/wiki/Embedding)에서 말하는 것처럼 수리적인 의미로 임베딩이라는 단어를 사용하는 것 같은데, 좌표축을 바꾼다는 의미일까? 
> In mathematics, an embedding (or imbedding[1]) is one instance of some mathematical structure contained within another instance, such as a group that is a subgroup.  


```r
# Compute t-SNE without doing the PCA step
tsne_output <- Rtsne(mnist_sample[,-1], PCA = FALSE, dims = 3)

# Show the obtained embedding coordinates
head(tsne_output$Y)

# Store the first two coordinates and plot them 
tsne_plot <- data.frame(tsne_x = tsne_output$Y[, 1], tsne_y = tsne_output$Y[, 2], 
                        digit = as.factor(mnist_sample$label))

# Plot the coordinates
ggplot(tsne_plot, aes(x = tsne_x, y = tsne_y, color = digit)) + 
	ggtitle("t-SNE of MNIST sample") + 
	geom_text(aes(label = digit)) + 
	theme(legend.position = "none")
	
	
# Inspect the output object's structure
str(tsne_output)

# Show total costs after each 50th iteration
tsne_output$itercosts

# Plot the evolution of the KL divergence at each 50th iteration
plot(tsne_output$itercosts, type = "l")

# Show the K-L divergence of each record after the final iteration
tsne_output$costs

# Plot the K-L divergence of each record after the final iteration
plot(tsne_output$costs, type = "l")
```

### Optimal number of t-SNE iterations
#### Whatis a hyper-parameter?
A parameter whose value is not learned from the data and is set beforehand  
 - Number ofiterations  
 - Perplexity  
 - Learning rate  
Optimization criterium: K-L divergence  

```r
# Generate a three-dimensional t-SNE embedding without PCA
set.seed(1234)
tsne_output <- Rtsne(mnist_sample[, -1], PCA = FALSE, dims = 3)

# Generate a new t-SNE embedding with the same hyper-parameter values
set.seed(1234)
tsne_output_new <- Rtsne(mnist_sample[, -1], PCA = FALSE, dims = 3)

# Check if the two outputs are identical
identical(tsne_output, tsne_output_new)

# Set seed to ensure reproducible results
set.seed(1234)

# Execute a t-SNE with 2000 iterations
tsne_output <- Rtsne(mnist_sample[, -1], max_iter = 2000)

# Observe the output costs 
tsne_output$itercosts

# Get the 50th iteration with the minimum K-L cost
which.min(tsne_output$itercosts)
```


### Effect of perplexity parameter
#### What is the perplexity parameter?
 - Balance attention between local and global aspects ofthe dataset  
 - A guess about the number of close neighbors  
 - In a real setting is important to try different values  
 - Must be lower than the number ofinput records  

```r
# Set seed to ensure reproducible results
set.seed(1234)

# Execute a t-SNE with perplexity 5
tsne_output <- Rtsne(mnist_sample[, -1], max_iter = 1200, perple = 5)

# Observe the returned K-L divergence costs at every 50th iteration
tsne_output$itercosts

# Set seed to ensure reproducible results
set.seed(1234)

# Execute a t-SNE with perplexity 20
tsne_output <- Rtsne(mnist_sample[, -1], max_iter = 1200, perple = 20)

# Observe the returned K-L divergence costs at every 50th iteration
tsne_output$itercosts

# Set seed to ensure reproducible results
set.seed(1234)

# Execute a t-SNE with perplexity 50
tsne_output <- Rtsne(mnist_sample[, -1], max_iter = 1200, perple = 50)

# Observe the returned K-L divergence costs at every 50th iteration
tsne_output$itercosts

# Observe the K-L divergence costs with perplexity 5 and 50
tsne_output_5$itercosts
tsne_output_50$itercosts

# Generate the data frame to visualize the embedding
tsne_plot_5 <- data.frame(tsne_x = tsne_output_5$Y[, 1], tsne_y = tsne_output_5$Y[, 2], digit = as.factor(mnist_10k$label))
tsne_plot_50 <- data.frame(tsne_x = tsne_output_50$Y[, 1], tsne_y = tsne_output_50$Y[, 2], digit = as.factor(mnist_10k$label))

# Plot the obtained embeddings
ggplot(tsne_plot_5, aes(x = tsne_x, y = tsne_y, color = digit)) + 
	ggtitle("MNIST t-SNE with 1300 iter and Perplexity=5") + geom_text(aes(label = digit)) + 
	theme(legend.position="none")
ggplot(tsne_plot_50, aes(x = tsne_x, y = tsne_y, color = digit)) + 
	ggtitle("MNIST t-SNE with 1300 iter and Perplexity=50") + geom_text(aes(label = digit)) + 
	theme(legend.position="none")
```

### Classifying digits with t-SNE
```r
# Prepare the data.frame
tsne_plot <- data.frame(tsne_x = tsne$Y[1:5000, 1], 
                        tsne_y = tsne$Y[1:5000, 2], 
                        digit = as.factor(mnist_10k[1:5000, ]$label))

# Plot the obtained embedding
ggplot(tsne_plot, aes(x = tsne_x, y = tsne_y, color = digit)) + 
	ggtitle("MNIST embedding of the first 5K digits") + 
	geom_text(aes(label = digit)) + 
	theme(legend.position="none")
	
# Get the first 5K records and set the column names
dt_prototypes <- as.data.table(tsne$Y[1:5000,])
setnames(dt_prototypes, c("X","Y"))

# Paste the label column as factor
dt_prototypes[, label := as.factor(mnist_10k[1:5000,]$label)]

# Compute the centroids per label
dt_prototypes[, mean_X := mean(X), by = label]
dt_prototypes[, mean_Y := mean(Y), by = label]

# Get the unique records per label
dt_prototypes <- unique(dt_prototypes, by = "label")
dt_prototypes

# Store the last 5000 records in distances and set column names
distances <- as.data.table(tsne$Y[5001:10000, ])
setnames(distances, c("X","Y"))

# Paste the true label
distances[, label := mnist_10k[5001:10000,]$label]

# Filter only those labels that are 1 or 0 
distances_filtered <- distances[label == 1 | label == 0]

# Compute Euclidean distance to prototype of digit 1
distances_filtered[, dist_1 := sqrt( (X - dt_prototypes[label == 1,]$mean_X)^2 + 
                             (Y - dt_prototypes[label == 1,]$mean_Y)^2)]
			     
# Compute the basic statistics of distances from records of class 1
summary(distances[label == 1]$dist_1)

# Compute the basic statistics of distances from records of class 0
summary(distances[label == 0]$dist_1)

# Plot the histogram of distances of each class
ggplot(distances, aes(x = dist_1, fill = as.factor(label))) +
  	geom_histogram(binwidth = 5, alpha = .5, position = "identity", show.legend = FALSE) + 
  	ggtitle("Distribution of Euclidean distance 1 vs 0")

```

## Using t-SNE with Predictive Models
### Credit card fraud detection

```r
# Look at the data dimensions
dim(creditcard)

# Explore the column names
names(creditcard)

# Explore the structure
str(creditcard)

# Generate a summary
summary(creditcard)

# Plot a histogram of the transaction time
ggplot(creditcard, aes(x = Time)) + 
	geom_histogram()
	
# Extract positive and negative instances of fraud
creditcard_pos <- creditcard[Class == 1]
creditcard_neg <- creditcard[Class == 0]

# Fix the seed
set.seed(1234)

# Create a new negative balanced dataset by undersampling
creditcard_neg_bal <- creditcard_neg[sample(1:nrow(creditcard_neg), nrow(creditcard_pos))]

# Generate a balanced train set
creditcard_train <- rbind(creditcard_pos, creditcard_neg_bal)
```

### Training random forests models

```r
# Fix the seed
set.seed(1234)

# Separate x and y sets
train_x <- creditcard_train[, -31]
train_y <- creditcard_train$Class

# Train a random forests
rf_model <- randomForest(x = train_x, y = train_y, ntree = 100)

# Plot the error evolution and variable importance
varImpPlot(rf_model)
plot(rf_model)

# Set the seed
set.seed(1234)

# Generate the t-SNE embedding 
tsne_output <- Rtsne(as.matrix(creditcard_train[, -31]), check_duplicates = FALSE, PCA = FALSE)

# Generate a data frame to plot the result
tsne_plot <- data.frame(tsne_x = tsne_output$Y[,1],
                        tsne_y = tsne_output$Y[,2],
                        Class = creditcard_train$Class)

# Plot the embedding usign ggplot and the label
ggplot(tsne_plot, aes(x = tsne_x, y = tsne_y, color = Class)) + 
  ggtitle("t-SNE of credit card fraud train set") + 
  geom_text(aes(label = Class)) + theme(legend.position = "none")
```

#### Training a random forest with embedding features
t-SNE 후에 줄어든 feature를 이용해 RF를 시행하면 빠른 속도로 괜찮은 결과를 얻을 수 있다.  
```r
# Fix the seed
set.seed(1234)

# Train a random forest
rf_model_tsne <- randomForest(train_tsne_x, train_tsne_y, ntree = 100)

# Plot the error evolution
plot(rf_model_tsne)

# Plot the variable importance
varImpPlot(rf_model_tsne)
```

### Predicting data
train-test split을 한 raw dataset으로 RF를 한 결과와 t-SNE 후에 RF를 시행한 결과를 비교해보자. AUC로 비교해본 결과 t-SNE 후에 RF를 시행한 결과가 아주 약간이지만 더 좋은 결과를 보인다. 
```r
# Predict on the test set using the random forest 
pred_rf <- predict(rf_model, creditcard_test, type = "prob")

# Plot a probability distibution of the target class
hist(pred_rf[,2])

# Compute the area under the curve
pred <- prediction(pred_rf[, 2], creditcard_test$Class)
perf <- performance(pred, measure = "auc") 
perf@y.values

# Predict on the test set using the random forest generated with t-SNE features
pred_rf <- predict(rf_model_tsne, test_x, type = "prob")

# Plot a probability distibution of the target class
hist(pred_rf[,2])

# Compute the area under the curve
pred <- prediction(pred_rf[,2], creditcard_test$Class)
perf <- performance(pred, "auc") 
perf@y.values
```

### Visualizing neural networks layers

```r
# Observe the dimensions
dim(layer_128_train)

# Show the first six records of the last ten columns
head(layer_128_train[, 119:128])

# Generate a summary of all columns
summary(layer_128_train)
```
