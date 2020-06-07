Build a classification tree using rpart package
```r
# Look at the data
str(creditsub)

# Create the model
credit_model <- rpart(formula = default ~ ., 
                      data = creditsub, 
                      method = "class")

# Display the results
rpart.plot(x = credit_model, yesno = 2, type = 0, extra = 0)

```
Compare models with a different splitting criterion
- gini는 random forest에서도 나오는 것 같은데, purity와 함께 찾아보자. 
```r
# Train a gini-based model
credit_model1 <- rpart(formula = default ~ ., 
                       data = credit_train, 
                       method = "class",
                       parms = list(split = "gini"))

# Train an information-based model
credit_model2 <- rpart(formula = default ~ ., 
                       data = credit_train, 
                       method = "class",
                       parms = list(split = "information"))

# Generate predictions on the validation set using the gini model
pred1 <- predict(object = credit_model1, 
             newdata = credit_test,
             type = "class")    

# Generate predictions on the validation set using the information model
pred2 <- predict(object = credit_model2, 
             newdata = credit_test,
             type = "class") 

# Compare classification error
ce(actual = credit_test$default, 
   predicted = pred1)
ce(actual = credit_test$default, 
   predicted = pred2)  

```

Tuning the model
- tree-based model의 특징인 pruning을 거친다. 
```r
# Plot the "CP Table"
plotcp(grade_model)

# Print the "CP Table"
print(grade_model$cptable)

# Retrieve optimal cp value based on cross-validated error
opt_index <- which.min(grade_model$cptable[, "xerror"])
cp_opt <- grade_model$cptable[opt_index, "CP"]

# Prune the model (to optimized cp value)
grade_model_opt <- prune(tree = grade_model, 
                         cp = cp_opt)
                          
# Plot the optimized model
rpart.plot(x = grade_model_opt, yesno = 2, type = 0, extra = 0)

```
Boosted Trees
- Boosted Tree part에서 GBM 방법을 좀 더 자세히 알아보기


Compare all models based on AUC
- Decision Trees, Bagged Trees, Random Forest and Gradient Boosting Machine (GBM)를 이용한 prediction의 AUC 비교 
```r
# Generate the test set AUCs using the two sets of predictions & compare
actual <- credit_test$default
dt_auc <- auc(actual = actual, predicted = dt_preds)
bag_auc <- auc(actual = actual, predicted = bag_preds)
rf_auc <- auc(actual = actual, predicted = rf_preds)
gbm_auc <- auc(actual = actual, predicted = gbm_preds)

# Print results
sprintf("Decision Tree Test AUC: %.3f", dt_auc)
sprintf("Bagged Trees Test AUC: %.3f", bag_auc)
sprintf("Random Forest Test AUC: %.3f", rf_auc)
sprintf("GBM Test AUC: %.3f", gbm_auc)


# List of predictions
preds_list <- list(dt_preds, bag_preds, rf_preds, gbm_preds)

# List of actual values (same for all)
m <- length(preds_list)
actuals_list <- rep(list(credit_test$default), m)

# Plot the ROC curves
pred <- prediction(preds_list, actuals_list)
rocs <- performance(pred, "tpr", "fpr")
plot(rocs, col = as.list(1:m), main = "Test Set ROC Curves")
legend(x = "bottomright", 
       legend = c("Decision Tree", "Bagged Trees", "Random Forest", "GBM"),
       fill = 1:m)

```
