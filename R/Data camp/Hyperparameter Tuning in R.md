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
### Hyperparameter tuning with mlr
mlr package를 이용한 hyperparameter tuning을 보여준다. 사실  mlr package는 ML을 목적으로 만들어진 package라 좀 더 공부해보는 것도 의미있을 것 같다. 흥미로웠던 부분은 mlr이 일련의 work flow를 정의해야만 작동된다는 것이었다. 물론, 다른 패키지나 함수들도 명시적으로 정의되어있진 않지만 work flow라는게 존재하지만 mlr처럼 명확하게 정의하고 있진 않다. work flow가 분명한 mlr package을 쓰는 것 자체가 분석의 과정에 익숙해지는 계기가 될 것 같다.  
#### Modeling with mlr
```r
# Create classification taks
task <- makeClassifTask(data = knowledge_train_data, 
                        target = "UNS")

# Call the list of learners
listLearners() %>%
 as.data.frame() %>%
 select(class, short.name, package) %>%
 filter(grepl("classif.", class))

# Create learner
lrn <- makeLearner("classif.randomForest", 
                   predict.type = "prob", 
                   fix.factors.prediction = TRUE)

```


#### Random search with mlr
낯설어서 그런 것이겠지...? 되게 어려워보이는데?   
```r
# Get the parameter set for neural networks of the nnet package
getParamSet("classif.nnet")

# Define set of parameters
param_set <- makeParamSet(
  makeDiscreteParam("size", values = c(2,3,5)),
  makeNumericParam("decay", lower = 0.0001, upper = 0.1)
)

# Print parameter set
print(param_set)

# Define a random search tuning method.
ctrl_random <- makeTuneControlRandom()
```

#### Perform hyperparameter tuning with mlr
```r
# Define a random search tuning method.
ctrl_random <- makeTuneControlRandom(maxit = 6)

# Define a 3 x 3 repeated cross-validation scheme
cross_val <- makeResampleDesc("RepCV", folds = 3 * 3)

# Tune hyperparameters
tic()
lrn_tune <- tuneParams(lrn,
                       task,
                       resampling = cross_val,
                       control = ctrl_random, 
                       par.set = param_set)
toc()
```

#### Evaluating hyperparameters with `mlr`
```r
# Create holdout sampling
holdout <- makeResampleDesc("Holdout")

# Perform tuning
lrn_tune <- tuneParams(learner = lrn, task = task, resampling = holdout, control = ctrl_random, par.set = param_set)

# Generate hyperparameter effect data
hyperpar_effects <- generateHyperParsEffectData(lrn_tune, partial.dep = TRUE)

# Plot hyperparameter effects
plotHyperParsEffect(hyperpar_effects, 
    partial.dep.learn = "regr.glm",
    x = "minsplit", y = "mmce", z = "maxdepth",
    plot.type = "line")
```

### Advanced tuning with `mlr`
#### Define aggregated measures
```r
# Create holdout sampling
holdout <- makeResampleDesc("Holdout", predict = "both")

# Perform tuning
lrn_tune <- tuneParams(learner = lrn, 
                       task = task, 
                       resampling = holdout, 
                       control = ctrl_random, 
                       par.set = param_set,
                       measures = list(acc, setAggregation(acc, train.mean), mmce, setAggregation(mmce, train.mean)))
```

#### Setting hyperparameters
다 좋은데, hyperparameter의 이름을 다 알아야하는건가? lrn에서 따로 조회할 수 있는 방법을 알아보자.  
```r
# Set hyperparameters
lrn_best <- setHyperPars(lrn, par.vals = list(size = 1, 
                                              maxit = 150, 
                                              decay = 0))

# Train model
model_best <- train(lrn_best, task)
```


### Hyperparameter tuning with h2o

#### Prepare data for modelling with h2o
```r
# Initialise h2o cluster
h2o.init()

# Convert data to h2o frame
seeds_train_data_hf <- as.h2o(seeds_train_data)

# Identify target and features
y <- "seed_type"
x <- setdiff(colnames(seeds_train_data_hf), y)

# Split data into train & validation sets
sframe <- h2o.splitFrame(seeds_train_data_hf, seed = 42)
train <- sframe[[1]]
valid <- sframe[[2]]

# Calculate ratio of the target variable in the training set
summary(train$seed_type, exact_quantiles = TRUE)
```

#### Modeling with h2o
```r
# Train random forest model
rf_model <- h2o.randomForest(x = x,
                             y = y,
                             training_frame = train,
                             validation_frame = valid)

# Calculate model performance
perf <- h2o.performance(rf_model, valid = TRUE)

# Extract confusion matrix
h2o.confusionMatrix(perf)

# Extract logloss
h2o.logloss(perf)
```

#### Grid and Random search with h2o
```r
# Define hyperparameters
dl_params <- list(hidden = list(c(50, 50), c(100,100)),
                  epochs = c(5, 10, 15),
                  rate = c(0.001, 0.005, 0.01))
                  
# Define search criteria
search_criteria <- list(strategy = "RandomDiscrete", 
                        max_runtime_secs = 10, # this is way too short & only used to keep runtime short!
                        seed = 42)

# Train with random search
dl_grid <- h2o.grid("deeplearning", 
                    grid_id = "dl_grid",
                    x = x, 
                    y = y,
                    training_frame = train,
                    validation_frame = valid,
                    seed = 42,
                    hyper_params = dl_params,
                    search_criteria = search_criteria)
```

#### Stopping criteria
datacamp course를 들을 때마다 종종, '이름'정하는데 에러가 난다. stopping_metric을 반드시 misclassification으로 해야하는 이유가 있을까?  
```r
# Define early stopping
stopping_params <- list(strategy = "RandomDiscrete", 
                        stopping_metric = "misclassification",
                        stopping_rounds = 2, 
                        stopping_tolerance = 0.1,
                        seed = 42)
```

### Automatic machine learning with h2o
#### AutoML in h2o and scoring the leaderboard
setting을 주면 자동적으로 ml을 실행해주는 방법인데, 꽤 편리해보인다. 리더보드를 이용한 model 평가 결과를 주는 것도 가독성이 좀 떨어지긴 하지만 괜찮아 보인다.  
```r
# Run automatic machine learning
automl_model <- h2o.automl(x = x, 
                           y = y,
                           training_frame = train,
                           max_runtime_secs = 10,
                           sort_metric = "mean_per_class_error",
                           valid = valid,
                           # nfolds = 3, 
                           seed = 42)
```

```r
# Extract the leaderboard
lb <- automl_model@leaderboard
head(lb)

# Assign best model new object name
aml_leader <- automl_model@leader

# Look at best model
summary(aml_leader)
```
