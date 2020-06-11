
### Linear SVM  
SVM의 이론적 배경보다는 classifier의 기능적인 면을 간략하게 설명하고 넘어감. 따로 정리하는 과정이 필요할 것 같다. 
```r
# dataset
df <- data.frame(x1 = runif(600), 
                 x2 = runif(600))
# 80:20으로 train-test split

# SVM model using svm function in e1071 package
library(e1071)
str(trainset)
#build svm model, setting required parameters
svm_model<- svm(y ~ ., 
                data = trainset, 
                type = "C-classification", 
                kernel = "linear", 
                scale = FALSE)
                
                
#list components of model
names(svm_model)

#list values of the SV, index and rho
svm_model$SV
svm_model$index
svm_model$rho

#compute training accuracy
pred_train <- predict(svm_model, trainset)
mean(pred_train == trainset$y)

#compute test accuracy
pred_test <- predict(svm_model, testset)
mean(pred_test == testset$y)
```

#### Visualizing support vectors using ggplot
경계 근처에 위치한 점에 포인트를 줌.
```r
#load ggplot
library(ggplot2)

#build scatter plot of training dataset
scatter_plot <- ggplot(data = trainset, aes(x = x1, y = x2, color = y)) + 
    geom_point() + 
    scale_color_manual(values = c("red", "blue"))

str(trainset)
str(svm_model)
 
#add plot layer marking out the support vectors 
layered_plot <- 
    scatter_plot + geom_point(data = trainset[svm_model$index, ], aes(x = x1, y = x2), color = "purple", size = 4, alpha = 0.5)

#display plot
layered_plot
```

#### Visualizing decision & margin bounds using `ggplot2`
가중 벡터와 svm model로부터 결정경계의 계수와 절편을 계산하는 방법을 포함하고 있음.  
```r
#calculate slope and intercept of decision boundary from weight vector and svm model
w <- t(svm_model$coefs) %*% svm_model$SV

slope_1 <- -w[1]/w[2]
intercept_1 <- svm_model$rho/w[2]

#build scatter plot of training dataset
scatter_plot <- ggplot(data = trainset, aes(x = x1, y = x2, color = y)) + 
    geom_point() + scale_color_manual(values = c("red", "blue"))
    
#add decision boundary
plot_decision <- scatter_plot + geom_abline(slope = slope_1, intercept = intercept_1) 

#add margin boundaries
plot_margins <- plot_decision + 
 geom_abline(slope = slope_1, intercept = intercept_1 - 1/w[2], linetype = "dashed")+
 geom_abline(slope = slope_1, intercept = intercept_1 + 1/w[2], linetype = "dashed")
 
#display plot
plot_margins
```

#### Visualizing decision boundaries and margins

```r
# bulid linear svm using cost = 1 and cost = 100
svm_model_1 <- svm(y ~ ., 
                data = trainset, 
                type = "C-classification", 
                kernel = "linear", 
                cost = 1, # default setting
                scale = FALSE)
svm_model_100 <- svm(y ~ ., 
                data = trainset, 
                type = "C-classification", 
                kernel = "linear", 
                cost = 100, # default setting
                scale = FALSE)

# calculate weight vector, intercept and slope of decision boundary 
w_1 <- t(svm_model_1$coefs) %*% svm_model_1$SV

slope_1 <- -w_1[1]/w_1[2]
intercept_1 <- svm_model_1$rho/w_1[2]

w_100 <- t(svm_model_100$coefs) %*% svm_model_100$SV

slope_100 <- -w_100[1]/w_100[2]
intercept_100 <- svm_model_100$rho/w_100[2]

# plotting
# add decision boundary and margins for cost = 1 to training data scatter plot
train_plot_with_margins <- train_plot + 
    geom_abline(slope = slope_1, intercept = intercept_1) +
    geom_abline(slope = slope_1, intercept = intercept_1-1/w_1[2], linetype = "dashed")+
    geom_abline(slope = slope_1, intercept = intercept_1+1/w_1[2], linetype = "dashed")

# display plot
train_plot_with_margins

# add decision boundary and margins for cost = 100 to training data scatter plot
train_plot_with_margins <- train_plot_100 + 
    geom_abline(slope = slope_100, intercept = intercept_100, color = "goldenrod") +
    geom_abline(slope = slope_100, intercept = intercept_100-1/w_100[2], linetype = "dashed", color = "goldenrod")+
    geom_abline(slope = slope_100, intercept = intercept_100+1/w_100[2], linetype = "dashed", color = "goldenrod")

# display plot 
train_plot_with_margins
```

### Multiclass problems
iris set을 이용해 binary classifier인 SVM이 3개 이상의 class를 어떻게 분리하는지 간단히 설명함. 
```r
# buid SVM and calculate accuracy in 100 times 
for (i in 1:100){
  	#assign 80% of the data to the training set
    iris[, "train"] <- ifelse(runif(nrow(iris)) < 0.8, 1, 0)
    trainColNum <- grep("train", names(iris))
    trainset <- iris[iris$train == 1, -trainColNum]
    testset <- iris[iris$train == 0, -trainColNum]
  	#build model using training data
    svm_model <- svm(Species~ ., data = trainset, 
                     type = "C-classification", kernel = "linear")
  	#calculate accuracy on test data
    pred_test <- predict(svm_model, testset)
    accuracy[i] <- mean(pred_test == testset$Species)
}
mean(accuracy) 
sd(accuracy)
```

### Polynomial Kernels
#### Generating a 2d radially separable dataset
```r
#set number of variables and seed
n <- 400
set.seed(1)

#Generate data frame with two uniformly distributed predictors, x1 and x2
df <- data.frame(x1 = runif(n, min = -1, max = 1), 
                 x2 = runif(n, min = -1, max = 1))

#We want a circular boundary. Set boundary radius 
radius <- 0.8
radius_squared <- radius^2

#create dependent categorical variable, y, with value -1 or 1 depending on whether point lies
#within or outside the circle.
df$y <- factor(ifelse(df$x1^2 + df$x2^2 < radius_squared, -1, 1), levels = c(-1, 1))

#load ggplot
library(ggplot2)

#build scatter plot, distinguish class by color
scatter_plot <- ggplot(data = df, aes(x = x1, y = x2, color = y)) + 
    geom_point() +
    scale_color_manual(values = c("red", "blue"))

#display plot
scatter_plot
```

#### Visualizing transformed radially separable data  
Visualize it in the x1^2-x2^2 plane. As a reminder, the separation boundary for the data is the circle x1^2 + x2^2 = 0.64(radius = 0.8 units). 
```r
# df, dataset, is same as before part

# transform data
df1 <- data.frame(x1sq = df$x1^2, x2sq = df$x2^2, y = df$y)

#plot data points in the transformed space
plot_transformed <- ggplot(data = df1, aes(x = x1sq, y = x2sq, color = y)) + 
    geom_point()+ guides(color = FALSE) + 
    scale_color_manual(values = c("red", "blue"))

# add decision boundary and visualize
plot_decision <- plot_transformed + geom_abline(slope = -1, intercept = 0.64)
plot_decision
```

#### SVM with polynomial kernel
```r
svm_model<- 
    svm(y ~ ., data = trainset, type = "C-classification", 
        kernel = "polynomial", degree = 2)

#measure training and test accuracy
pred_train <- predict(svm_model, trainset)
mean(pred_train == trainset$y)
pred_test <- predict(svm_model, testset)
mean(pred_test == testset$y)

#plot
plot(svm_model, trainset)
```
#### Using tune.svm for finding optimal parameter values
대부분의 Machine learning 방법론에서 최적의 parameter 값을 찾아 model fitting 혹은 evaluation에 사용하길 권장하는데, 이는 optimal value가  model performance에 영향을 미치기 때문이다. tune.svm()을 이용해 svm의 optimal parameter value를 찾아보자.  
```r
#tune model
tune_out <- 
    tune.svm(x = trainset[, -3], y = trainset[, 3], 
             type = "C-classification", 
             kernel = "polynomial", degree = 2, cost = 10^(-1:2), 
             gamma = c(0.1, 1, 10), coef0 = c(0.1, 1, 10))

str(tune_out$best.parameters)
#list optimal values
tune_out$best.parameters$gamma
tune_out$best.parameters$coef0
tune_out$best.parameters$cost
```

### Radial Basis Function Kernels

#### Generating a complex dataset
```r
#number of data points
n <- 1000

#set seed
set.seed(1)

#create dataframe
df <- data.frame(x1 = rnorm(n, mean = -0.5, sd = 1), 
                 x2 = runif(n, min = -1, max = 1))
                 
#set radius and centers
radius <- 0.8
center_1 <- c(-0.8, 0)
center_2 <- c(0.8, 0)
radius_squared <- radius^2

#create binary classification variable
df$y <- factor(ifelse((df$x1-center_1[1])^2 + (df$x2-center_1[2])^2 < radius_squared|
                      (df$x1-center_2[1])^2 + (df$x2-center_2[2])^2 < radius_squared, -1, 1),
                      levels = c(-1, 1))
                      
# Load ggplot2
library(ggplot2)

# Plot x2 vs. x1, colored by y
scatter_plot<- ggplot(data = df, aes(x = x1, y = x2, color = y)) + 
    # Add a point layer
    geom_point() + 
    scale_color_manual(values = c("red", "blue")) +
    # Specify equal coordinates
    coord_equal()
 
scatter_plot 
```


#### The RBF Kernel

Q. gamma와 point value 사이의 거리 *r* 과의 관계? 
```r
#create vector to store accuracies and set random number seed
accuracy <- rep(NA, 100)
set.seed(2)

#calculate accuracies for 100 training/test partitions
for (i in 1:100){
    df[, "train"] <- ifelse(runif(nrow(df))<0.8, 1, 0)
    trainset <- df[df$train == 1, ]
    testset <- df[df$train == 0, ]
    trainColNum <- grep("train", names(trainset))
    trainset <- trainset[, -trainColNum]
    testset <- testset[, -trainColNum]
    svm_model<- svm(y ~ ., data = trainset, type = "C-classification", kernel = "radial")
    pred_test <- predict(svm_model, testset)
    accuracy[i] <- mean(pred_test == testset$y)
}

#print average accuracy and standard deviation
mean(accuracy)
sd(accuracy)
```

```r
#tune model
tune_out <- tune.svm(x = trainset[, -3], y = trainset[, 3], 
                     gamma = 5*10^(-2:2), 
                     cost = c(0.01, 0.1, 1, 10, 100), 
                     type = "C-classification", kernel = "radial")

#build tuned model
svm_model <- svm(y~ ., data = trainset, type = "C-classification", kernel = "radial", 
                 cost = tune_out$best.parameters$cost, 
                 gamma = tune_out$best.parameters$gamma)

#calculate test accuracy
pred_test <- predict(svm_model, testset)
mean(pred_test == testset$y)

#Plot decision boundary against test data
plot(svm_model, testset)
```
