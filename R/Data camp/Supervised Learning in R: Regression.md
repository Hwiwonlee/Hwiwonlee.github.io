```r
# 다음 3개의 함수의 차이? 
# Call summary() on unemployment_model to get more details
summary(lm_model)

# Call glance() on unemployment_model to see the details in a tidier form
glance(lm_model)

# Call wrapFTest() on unemployment_model to see the most relevant details
wrapFTest(lm_model)
```

## Difference of summary(), glance(), wrapFTest()  
Purpose of these three function, summary(), glance(), wrapFTest(), is arranging result of some model to more easily understand.  
```{r}
model <- lm(cty ~ displ + hwy + drv, data = mpg)
summary(model)
glance(model) %>% as.data.frame()
wrapFTest(model)
```
As you have seen, most detailed result is obtained by using summary(). Result of summary() has a lot of things about model. There are range of residual, information of coefficients like estimate, standard deviation, t value, p-value, $R^2$, $AdjustedR^2$, F-value and p-value. But this result is little bit complex to read and understand. Using glance() or wrapFTest(), you can see some information about model even if some information disappear. Especially, glance() focus on the statistical significance of model. So, if you need to 'glance' the model, I will recommand that please use glance().  

#### Usage WVPlots package
[WVPlots examples](https://cran.r-project.org/web/packages/WVPlots/vignettes/WVPlots_examples.html)

#### Vignette of vtreat package
[Vignette of vtreat](https://cran.r-project.org/web/packages/vtreat/vignettes/vtreat.html)
```r
# WVPlots Package 
WVPlots::GainCurvePlot()

# vtreat Package
vtreat::kWayCrossValidation()
```

```r
# mpg is in the workspace
summary(mpg)

# splitPlan is in the workspace
set.seed(100)
splitPlan <- vtreat::kWayCrossValidation(nRows = nrow(mpg), nSplits = 3, dframe = NULL, y = NULL)
str(splitPlan)

# Run the 3-fold cross validation plan from splitPlan
k <- 3 # Number of folds
mpg$pred.cv <- 0 

# k is the number of folds
# splitPlan is the cross validation plan
for(i in 1:k) {
  split <- splitPlan[[i]]
  
  # Build a model on the training data 
  # from this split 
  # (lm, in this case)
  model <- lm(cty ~ hwy, data = mpg[split$train, ])
  
  # make predictions on the 
  # application data from this split
  mpg$pred.cv[split$app] <- predict(model, newdata = mpg[split$app, ])
}

# Predict from a full model
mpg$pred <- predict(lm(cty ~ hwy, data = mpg))

# Get the rmse of the full model's predictions
rmse(mpg$pred, mpg$cty)

# Get the rmse of the cross-validation predictions
rmse(mpg$pred.cv, mpg$cty)
```


#### model.matrix를 이용한 Examining the structure of categorical inputs.
[model.matrix()](https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/model.matrix)  
[r에서 design matrix 만들기](https://statkclee.github.io/ml/ml-r-design-matrix.html)


#### Modeling an interaction
Recall that the operator : designates the interaction between two variables.  
The operator * designates the interaction between the two variables, plus the main effects.  
`x*y = x + y + x:y`


#### Poisson과 quasipoisson


#### GAM과 s() function 


#### ranger()를 이용한 random forest 


```r
# one-hot-encoding for categorical data set 
## guide
# In this exercise you will use vtreat to one-hot-encode a categorical variable on a small example. vtreat creates a treatment plan to transform categorical variables into indicator variables (coded "lev"), and to clean bad values out of numerical variables (coded "clean").
# 
# To design a treatment plan use the function designTreatmentsZ()
# 
# treatplan <- designTreatmentsZ(data, varlist)
# data: the original training data frame
# varlist: a vector of input variables to be treated (as strings).
# designTreatmentsZ() returns a list with an element scoreFrame: a data frame that includes the names and types of the new variables:
#   
#   scoreFrame <- treatplan %>% 
#   magrittr::use_series(scoreFrame) %>% 
#   select(varName, origName, code)
# varName: the name of the new treated variable
# origName: the name of the original variable that the treated variable comes from
# code: the type of the new variable.
# "clean": a numerical variable with no NAs or NaNs
# "lev": an indicator variable for a specific level of the original categorical variable.
# (magrittr::use_series() is an alias for $ that you can use in pipes.)
# 
# For these exercises, we want varName where code is either "clean" or "lev":
#   
#   newvarlist <- scoreFrame %>% 
#   filter(code %in% c("clean", "lev") %>%
#            magrittr::use_series(varName)
#          To transform the data set into all numerical and one-hot-encoded variables, use prepare():
#            
#            data.treat <- prepare(treatplan, data, varRestrictions = newvarlist)
#          treatplan: the treatment plan
#          data: the data frame to be treated
#          varRestrictions: the variables desired in the treated data


# vtreat on a small example
# dframe is in the workspace
dframe

# Create and print a vector of variable names
(vars <- c("color", "size"))

# Load the package vtreat
library(vtreat)

# Create the treatment plan
treatplan <- designTreatmentsZ(dframe, vars)

# Examine the scoreFrame
(scoreFrame <- treatplan %>%
    use_series(scoreFrame) %>%
    select(varName, origName, code))

# We only want the rows with codes "clean" or "lev"
(newvars <- scoreFrame %>%
    filter(code %in% c("clean", "lev")) %>%
    use_series(varName))

# Create the treated training data
(dframe.treat <- prepare(treatplan, dframe, varRestriction = newvars))

```

Novel levels
When a level of a categorical variable is rare, sometimes it will fail to show up in training data. If that rare level then appears in future data, downstream models may not know what to do with it. When such novel levels appear, using model.matrix or caret::dummyVars to one-hot-encode will not work correctly.

vtreat is a "safer" alternative to model.matrix for one-hot-encoding, because it can manage novel levels safely. vtreat also manages missing values in the data (both categorical and continuous).

In this exercise you will see how vtreat handles categorical values that did not appear in the training set. The treatment plan treatplan and the set of variables newvars from the previous exercise are still in your workspace. dframe and a new data frame testframe are also in your workspace.


Find the right number of trees for a gradient boosting machine

For this exercise, the key arguments to the xgb.cv() call are:

data: a numeric matrix.
label: vector of outcomes (also numeric).
nrounds: the maximum number of rounds (trees to build).
nfold: the number of folds for the cross-validation. 5 is a good number.
objective: "reg:linear" for continuous outcomes.
eta: the learning rate.
max_depth: depth of trees.
early_stopping_rounds: after this many rounds without improvement, stop.
verbose: 0 to stay silent.
```r
# The July data is in the workspace
ls()

# Load the package xgboost
library(xgboost)
str(bikesJuly)
# Run xgb.cv
cv <- xgb.cv(data = as.matrix(bikesJuly.treat), 
            label = bikesJuly$cnt,
            nrounds = 100,
            nfold = 5,
            objective = "reg:linear",
            eta = 0.3,
            max_depth = 6,
            early_stopping_rounds = 10,
            verbose = 0    # silent
)

# Get the evaluation log 
elog <- cv$evaluation_log

# Determine and print how many trees minimize training and test error
elog %>% 
   summarize(ntrees.train = which.min(train_rmse_mean),   # find the index of min(train_rmse_mean)
             ntrees.test  = which.min(test_rmse_mean))   # find the index of min(test_rmse_mean)

```


Fit an xgboost bike rental model and predict
In this exercise you will fit a gradient boosting model using xgboost() to predict the number of bikes rented in an hour as a function of the weather and the type and time of day. You will train the model on data from the month of July and predict on data for the month of August.

The datasets for July and August are loaded into your workspace. Remember the vtreat-ed data no longer has the outcome column, so you must get it from the original data (the cnt column).

For convenience, the number of trees to use, ntrees from the previous exercise is in the workspace.

The arguments to xgboost() are similar to those of xgb.cv().

```r
# Examine the workspace
ls()

# The number of trees to use, as determined by xgb.cv
ntrees

# Run xgboost
bike_model_xgb <- xgboost(data = as.matrix(bikesJuly.treat), # training data as matrix
                   label = bikesJuly$cnt,  # column of outcomes
                   nrounds = ntrees,       # number of trees to build
                   objective = "reg:linear", # objective
                   eta = 0.3,
                   depth = 6,
                   verbose = 0  # silent
)

# Make predictions
bikesAugust$pred <- predict(bike_model_xgb, as.matrix(bikesAugust.treat))

# Plot predictions (on x axis) vs actual bike rental count
ggplot(bikesAugust, aes(x = pred, y = cnt)) + 
  geom_point() + 
  geom_abline()

```
