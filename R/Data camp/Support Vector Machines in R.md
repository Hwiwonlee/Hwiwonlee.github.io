
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

```
