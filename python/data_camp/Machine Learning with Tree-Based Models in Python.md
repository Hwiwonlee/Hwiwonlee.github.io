# 1. Classification and Regression Trees
## 1.1 Decision tree for classification

```python
# Train your first classification tree
## Import DecisionTreeClassifier from sklearn.tree
from sklearn.tree import DecisionTreeClassifier

## Instantiate a DecisionTreeClassifier 'dt' with a maximum depth of 6
dt = DecisionTreeClassifier(max_depth=6, random_state=SEED)

## Fit dt to the training set
dt.fit(X_train, y_train)

## Predict test set labels
y_pred = dt.predict(X_test)
print(y_pred[0:5])
```

```python
# Evaluate the classification tree
## Import accuracy_score
from sklearn.metrics import accuracy_score

y_pred = dt.predict(X_test) ## Predict test set labels

acc = accuracy_score(y_test, y_pred) ## Compute test set accuracy  
print("Test set accuracy: {:.2f}".format(acc))
```

```python
# Logistic regression vs classification tree
## Import LogisticRegression from sklearn.linear_model
from sklearn.linear_model import  LogisticRegression

## Instatiate logreg
logreg = LogisticRegression(random_state=1)

## Fit logreg to the training set
logreg.fit(X_train, y_train)

## Define a list called clfs containing the two classifiers logreg and dt
clfs = [logreg, dt]

## Review the decision regions of the two classifiers
plot_labeled_decision_regions(X_test, y_test, clfs)

```
## 1.2 Classification tree Learning

```python
# Using entropy as a criterion
## Import DecisionTreeClassifier from sklearn.tree
from sklearn.tree import DecisionTreeClassifier

## Instantiate dt_entropy, set 'entropy' as the information criterion
dt_entropy = DecisionTreeClassifier(max_depth=8, criterion='entropy', random_state=1)

## Fit dt_entropy to the training set
dt_entropy.fit(X_train, y_train)

```

```python
# Entropy vs Gini index
## Import accuracy_score from sklearn.metrics
from sklearn.metrics import accuracy_score

## Use dt_entropy to predict test set labels
y_pred= dt_entropy.predict(X_test)

## Evaluate accuracy_entropy
accuracy_entropy = accuracy_score(y_test, y_pred)

## Print accuracy_entropy
print('Accuracy achieved by using entropy: ', accuracy_entropy)

## Print accuracy_gini
print('Accuracy achieved by using the gini index: ', accuracy_gini)
```
## 1.3 Decision tree for regression

```python
# Train your first regression tree
## Import DecisionTreeRegressor from sklearn.tree
from sklearn.tree import DecisionTreeRegressor

## Instantiate dt
dt = DecisionTreeRegressor(max_depth=8,
             min_samples_leaf=0.13,
            random_state=3)

## Fit dt to the training set
dt.fit(X_train, y_train)
```

```python
# Evaluate the regression tree
## Import mean_squared_error from sklearn.metrics as MSE
from sklearn.metrics import mean_squared_error as MSE

y_pred = dt.predict(X_test) ## Compute y_pred
mse_dt = MSE(y_test, y_pred) ## Compute mse_dt
rmse_dt = mse_dt ** 0.5 ## Compute rmse_dt
print("Test set RMSE of dt: {:.2f}".format(rmse_dt))
```

```python
# Linear regression vs regression tree
y_pred_lr = lr.predict(X_test) ## Predict test set labels 
mse_lr = MSE(y_test, y_pred_lr) ## Compute mse_lr
rmse_lr = mse_lr ** 0.5 ## Compute rmse_lr

print('Linear Regression test set RMSE: {:.2f}'.format(rmse_lr))
print('Regression Tree test set RMSE: {:.2f}'.format(rmse_dt))
```

# 2. The Bias-Variance Tradeoff
## 2.1 Generalization Error
Bias-Variance Tradeoff에 대한 대략적인 설명

## 2.2 Diagnose bias and variance problems

```python
# Instantiate the model
## Import train_test_split from sklearn.model_selection
from sklearn.model_selection import train_test_split

SEED = 1 ## Set SEED for reproducibility

## Split the data into 70% train and 30% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

## Instantiate a DecisionTreeRegressor dt
dt = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.26, random_state=SEED)
```

```python
# Evaluate the 10-fold CV error
## Compute the array containing the 10-folds CV MSEs
MSE_CV_scores = - cross_val_score(dt, X_train, y_train, cv=10, 
                       scoring='neg_mean_squared_error',
                       n_jobs=-1)

RMSE_CV = (MSE_CV_scores.mean())**(0.5) ## Compute the 10-folds CV RMSE
print('CV RMSE: {:.2f}'.format(RMSE_CV))
```

```python
# Evaluate the training error
## Import mean_squared_error from sklearn.metrics as MSE
from sklearn.metrics import mean_squared_error as MSE

dt.fit(X_train, y_train) ## Fit dt to the training set
y_pred_train = dt.predict(X_train) ## Predict the labels of the training set
RMSE_train = (MSE(y_train, y_pred_train))**(0.5) ## Evaluate the training set RMSE of dt

print('Train RMSE: {:.2f}'.format(RMSE_train))
```

## 2.3 Ensemble Learning

```python
# Define the ensemble
## Indian Liver Patient Dataset
SEED=1 ## Set seed for reproducibility

lr = LogisticRegression(random_state=SEED) ## Instantiate lr
knn = KNN(n_neighbors=27) ## Instantiate knn
dt = DecisionTreeClassifier(min_samples_leaf=0.13, random_state=SEED) ## Instantiate dt

## Define the list classifiers
classifiers = [('Logistic Regression', lr), ('K Nearest Neighbours', knn), ('Classification Tree', dt)]
```

```python
# Evaluate individual classifiers
## Iterate over the pre-defined list of classifiers
for clf_name, clf in classifiers:    
 
    clf.fit(X_train, y_train) ## Fit clf to the training set
    y_pred = clf.predict(X_test) ## Predict y_pred
    
    accuracy = accuracy_score(y_test, y_pred)  ## Calculate accuracy
   
    ## Evaluate clf's accuracy on the test set
    print('{:s} : {:.3f}'.format(clf_name, accuracy))
```

```python
# Better performance with a Voting Classifier
## Import VotingClassifier from sklearn.ensemble
from sklearn.ensemble import VotingClassifier

vc = VotingClassifier(estimators=classifiers) ## Instantiate a VotingClassifier vc
vc.fit(X_train, y_train)   ## Fit vc to the training set

y_pred = vc.predict(X_test) ## Evaluate the test set predictions

accuracy = accuracy_score(y_test, y_pred) ## Calculate accuracy score
print('Voting Classifier: {:.3f}'.format(accuracy))
```
# 3. Bagging and Random Forests
## 3.1 Bagging
```python
# Define the bagging classifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier

dt = DecisionTreeClassifier(random_state=1) ## Instantiate dt

bc = BaggingClassifier(base_estimator=dt, n_estimators=50, random_state=1) ## Instantiate bc
```

```python
# Evaluate Bagging performance
bc.fit(X_train, y_train) ## Fit bc to the training set
y_pred = bc.predict(X_test) ## Predict test set labels

acc_test = accuracy_score(y_test, y_pred) ## Evaluate acc_test
print('Test set accuracy of bc: {:.2f}'.format(acc_test)) 
```

## 3.2 Out of Bag Evaluation


```python
# Prepare the ground
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier

dt = DecisionTreeClassifier(min_samples_leaf=8, random_state=1) ## Instantiate dt

## Instantiate bc
bc = BaggingClassifier(base_estimator=dt, 
            n_estimators=50,
            oob_score=True,
            random_state=1)

```

```python
# OOB Score vs Test Set Score
bc.fit(X_train, y_train) ## Fit bc to the training set 
y_pred = bc.predict(X_test) ## Predict test set labels

acc_test = accuracy_score(y_test, y_pred) ## Evaluate test set accuracy
acc_oob = bc.oob_score_ ## Evaluate OOB accuracy

## Print acc_test and acc_oob
print('Test set accuracy: {:.3f}, OOB accuracy: {:.3f}'.format(acc_test, acc_oob))
```

## 3.3Random Forests (RF)


```python
# Train an RF regressor
## https://www.kaggle.com/c/bike-sharing-demand/data

## Import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

## Instantiate rf
rf = RandomForestRegressor(n_estimators=25,
            random_state=2)
            

rf.fit(X_train, y_train) ## Fit rf to the training set    
```

```python
# Evaluate the RF regressor
from sklearn.metrics import mean_squared_error as MSE

y_pred = rf.predict(X_test) ## Predict the test set labels
rmse_test = MSE(y_test,y_pred) ** (0.5) ## Evaluate the test set RMSE
print('Test set RMSE of rf: {:.2f}'.format(rmse_test))
```

```python
# Visualizing features importances
# Create a pd.Series of features importances
importances = pd.Series(data=rf.feature_importances_,
                        index= X_train.columns)

# Sort importances
importances_sorted = importances.sort_values()

# Draw a horizontal barplot of importances_sorted
importances_sorted.plot(kind='barh', color='lightgreen')
plt.title('Features Importances')
plt.show()
```

# 4. Boosting
## 4.1 Adaboost

```python
# Define the AdaBoost classifier
from sklearn.tree import DecisionTreeClassifier

## Import AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier

## Instantiate dt
dt = DecisionTreeClassifier(max_depth=2, random_state=1)

## Instantiate ada
ada = AdaBoostClassifier(base_estimator=dt, n_estimators=180, random_state=1)
```

```python
# Train the AdaBoost classifier
ada.fit(X_train, y_train) ## Fit ada to the training set

## Compute the probabilities of obtaining the positive class
y_pred_proba = ada.predict_proba(X_test)[:,1]
```

```python
# Evaluate the AdaBoost classifier
## Import roc_auc_score
from sklearn.metrics import roc_auc_score

ada_roc_auc = roc_auc_score(y_test, y_pred_proba) ## Evaluate test-set roc_auc_score
print('ROC AUC score: {:.2f}'.format(ada_roc_auc))
```

# 4.2 Gradient Boosting (GB)

```python
# Define the GB regressor
## https://www.kaggle.com/c/bike-sharing-demand/data
## Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

## Instantiate gb
gb = GradientBoostingRegressor(max_depth=4, 
            n_estimators=200,
            random_state=2)
```

```python
# Train the GB regressor
gb.fit(X_train, y_train) ## Fit gb to the training set
y_pred = gb.predict(X_test) ## Predict test set labels
```

```python
# Evaluate the GB regressor
from sklearn.metrics import mean_squared_error as MSE

mse_test = MSE(y_test, y_pred) ## Compute MSE
rmse_test = mse_test ** 0.5 ## Compute RMSE
print('Test set RMSE of gb: {:.3f}'.format(rmse_test))
```

## 4.3 Stochastic Gradient Boosting (SGB)

```python
# Regression with SGB
## https://www.kaggle.com/c/bike-sharing-demand/data
## Import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor

## Instantiate sgbr
sgbr = GradientBoostingRegressor(max_depth=4, 
            subsample=0.9,
            max_features=0.75,
            n_estimators=200,                                
            random_state=2)
```

```python
# Train the SGB regressor
sgbr.fit(X_train, y_train) ## Fit sgbr to the training set
y_pred = sgbr.predict(X_test) ## Predict test set labels
```

```python
# Evaluate the SGB regressor
## Import mean_squared_error as MSE
from sklearn.metrics import mean_squared_error as MSE

mse_test = MSE(y_test, y_pred) ## Compute test set MSE
rmse_test = mse_test ** 0.5 ## Compute test set RMSE
print('Test set RMSE of sgbr: {:.3f}'.format(rmse_test))
```
# 5. Model Tuning
## 5.1 Tuning a CART's Hyperparameters
```python
# Set the tree's hyperparameter grid
## Define params_dt
params_dt = dict({'max_depth':[2,3,4], 'min_samples_leaf' : [0.12, 0.14, 0.16, 0.18]})
```

```python
# Search for the optimal tree
from sklearn.model_selection import GridSearchCV ## Import GridSearchCV

## Instantiate grid_dt
grid_dt = GridSearchCV(estimator=dt,
                       param_grid=params_dt,
                       scoring='roc_auc',
                       cv=5,
                       n_jobs=-1)
```

```python
# Evaluate the optimal tree
## Import roc_auc_score from sklearn.metrics
from sklearn.metrics import roc_auc_score

## Extract the best estimator
best_model = grid_dt.best_estimator_

## Predict the test set probabilities of the positive class
y_pred_proba = best_model.predict_proba(X_test)[:,1]

## Compute test_roc_auc
test_roc_auc = roc_auc_score(y_test, y_pred_proba)
print('Test set ROC AUC score: {:.3f}'.format(test_roc_auc))
```

## 5.2 Tuning a RF's Hyperparameters

```python
# Set the hyperparameter grid of RF
params_rf = dict({'n_estimators' : [100,350,500], 'max_features' : ['log2', 'auto', 'sqrt'], 'min_samples_leaf' : [2, 10, 30]})
```

```python
# Search for the optimal forest
## Import GridSearchCV
from sklearn.model_selection import GridSearchCV

## Instantiate grid_rf
grid_rf = GridSearchCV(estimator=rf,
                       param_grid=params_rf,
                       scoring='neg_mean_squared_error',
                       cv=3,
                       verbose=1,
                       n_jobs=-1)
```

```python
# Evaluate the optimal forest
## Import mean_squared_error from sklearn.metrics as MSE 
from sklearn.metrics import mean_squared_error as MSE

best_model = grid_rf.best_estimator_ ## Extract the best estimator 
y_pred = best_model.predict(X_test) ## Predict test set labels 
rmse_test = (MSE(y_test, y_pred) ** 0.5) ## Compute rmse_test

print('Test RMSE of best model: {:.3f}'.format(rmse_test)) 
```
