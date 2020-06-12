#### basic ML with caret 
```r
# Create partition index
index <- createDataPartition(breast_cancer_data$diagnosis, p = 0.7, list = FALSE)

# Subset `breast_cancer_data` with index
bc_train_data <- breast_cancer_data[index, ]
bc_test_data  <- breast_cancer_data[-index, ]

# Define 3x5 folds repeated cross-validation
fitControl <- trainControl(method = "repeatedcv", number = 5, repeats = 3)

# Run the train() function
gbm_model <- train(diagnosis ~ ., 
                   data = bc_train_data, 
                   method = "gbm", 
                   trControl = fitControl,
                   verbose = FALSE)

# Look at the model
gbm_model
```

#### Tune hyperparameters
```r
# Set seed.
set.seed(42)
# Start timer.
tic()
# Train model.
gbm_model <- train(diagnosis ~ ., 
                   data = bc_train_data, 
                   method = "gbm", 
                   trControl = trainControl(method = "repeatedcv", number = 5, repeats = 3),
                   verbose = FALSE,
                   tuneLength = 4)
# Stop timer.
toc()

# Define hyperparameter grid.
hyperparams <- expand.grid(n.trees = 200, 
                           interaction.depth = 1, 
                           shrinkage = 0.1, 
                           n.minobsinnode = 10)
modelLookup("gbm")


# Apply hyperparameter grid to train().
set.seed(42)
gbm_model <- train(diagnosis ~ ., 
                   data = bc_train_data, 
                   method = "gbm", 
                   trControl = trainControl(method = "repeatedcv", number = 5, repeats = 3),
                   verbose = FALSE,
                   tuneGrid = hyperparams)
```

#### Cartesian grid search in caret

```r
# Define Cartesian grid
man_grid <- expand.grid(degree = c(1, 2, 3), 
                        scale = c(0.1, 0.01, 0.001), 
                        C = 0.5)

# Start timer, set seed & train model
tic()
set.seed(42)
svm_model_voters_grid <- train(turnout16_2016 ~ ., 
                   data = voters_train_data, 
                   method = "svmPoly", 
                   trControl = fitControl,
                   verbose= FALSE,
                   tune.Grid = man_grid)
toc()

```

#### Plot hyperparameter model output
```r
# Plot default
plot(svm_model_voters_grid)

# Plot Kappa level-plot
plot(svm_model_voters_grid, metric = "Kappa", plotType = "level")

```

#### Grid search with range of hyperparameters
```r
# Define the grid with hyperparameter ranges
big_grid <- expand.grid(size = seq(from = 1, to = 5, by = 1), decay = c(0, 1))

# Train control with grid search
fitControl <- trainControl(method = "repeatedcv", number = 3, repeats = 5, search = "grid")

# Train neural net
tic()
set.seed(42)
nn_model_voters_big_grid <- train(turnout16_2016 ~ ., 
                   data = voters_train_data, 
                   method = "nnet", 
                   trControl = fitControl,
                   verbose = FALSE,
                   tuneGrid = big_grid)
toc()
```

#### Random search with caret
```r
# Train control with random search
fitControl <- trainControl(method = "repeatedcv",
                           number = 3,
                           repeats = 5,
                           search = "random")

# Test 6 random hyperparameter combinations
tic()
nn_model_voters_big_grid <- train(turnout16_2016 ~ ., 
                   data = voters_train_data, 
                   method = "nnet", 
                   trControl = fitControl,
                   verbose = FALSE,
                   tuneLength = 6)
toc()
```

#### Adaptive Resampling with caret
```r
# Define trainControl function
fitControl <- trainControl(method = "adaptive_cv",
                           number = 3, repeats = 3,
                           adaptive = list(min = 3, alpha = 0.05, method = "BT", complete = FALSE),
                           search = "random")

# Start timer & train model
tic()
svm_model_voters_ar <- train(turnout16_2016 ~ ., 
                   data = voters_train_data, 
                   method = "nnet", 
                   trControl = fitControl,
                   verbose = FALSE,
                   tuneLength = 6)
toc()

```
