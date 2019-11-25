# 1. Classification
## 1.1 Supervised learning


## 1.2 Exploratory data analysis

```python
# Visual EDA
## Congressional Voting Records Data Set
plt.figure()
sns.countplot(x='education', hue='party', data=df, palette='RdBu')
plt.xticks([0,1], ['No', 'Yes'])
plt.show()
```

```python
# Visual EDA
plt.figure()
sns.countplot(x='missile', hue='party', data=df, palette='RdBu')
plt.xticks([0,1], ['No', 'Yes'])
plt.show()

plt.figure()
sns.countplot(x='satellite', hue='party', data=df, palette='RdBu')
plt.xticks([0,1], ['No', 'Yes'])
plt.show()
```

## 1.3 Classification challenge
```python
# k-Nearest Neighbors: Fit
from sklearn.neighbors import KNeighborsClassifier ## Import KNeighborsClassifier from sklearn.neighbors

## Create arrays for the features and the response variable
y = df['party'].values
X = df.drop('party', axis=1).values

knn = KNeighborsClassifier(n_neighbors=6) ## Create a k-NN classifier with 6 neighbors
knn.fit(X=X, y=y) ## Fit the classifier to the data
```

```python
# k-Nearest Neighbors: Predict
from sklearn.neighbors import KNeighborsClassifier  ## Import KNeighborsClassifier from sklearn.neighbors

## Create arrays for the features and the response variable
y = df['party'].values
X = df.drop('party', axis = 1).values

knn = KNeighborsClassifier(n_neighbors=6) ## Create a k-NN classifier with 6 neighbors: knn
knn.fit(X, y) ## Fit the classifier to the data


y_pred = knn.predict(X) ## Predict the labels for the training data X

# Predict and print the label for the new data point X_new
new_prediction = knn.predict(X_new)
print("Prediction: {}".format(new_prediction))
```

> Q. KNeighborsClassifier을 사용한 fitting, prediction이 어떻게 진행되는지 잘 모르겠다. <br> A. 

## 1.4 Measuring model performance

```python
# The digits recognition dataset
## THE MNIST DATABASE of handwritten digits
from sklearn import datasets
import matplotlib.pyplot as plt
 
digits = datasets.load_digits() ## Load the digits dataset: digits

## Print the keys and DESCR of the dataset
print(digits.keys())
print(digits.DESCR)

## Print the shape of the images and data keys
print(digits.images.shape)
print(digits.data.shape)

## Display digit 1010
plt.imshow(digits.images[1010], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()

```

```python
# Train/Test Split + Fit/Predict/Accuracy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

## Create feature and target arrays
X = digits.data
y = digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42, stratify=y) ## Split into training and test set

knn = KNeighborsClassifier(n_neighbors=7) ## Create a k-NN classifier with 7 neighbors: knn
knn.fit(X_train, y_train) ## Fit the classifier to the training data

print(knn.score(X_test, y_test)) ## Print the accuracy
```
> train_test_split(arrays, test_size, train_size, random_state, shuffle, stratify) <br> 
random_state : 데이터 분할시 셔플이 이루어지는데 이를 위한 시드값 (int나 RandomState로 입력) <br>
shuffle : 셔플여부설정 (default = True) <br> stratify : 지정한 Data의 비율을 유지한다. 예를 들어, Label Set인 Y가 25%의 0과 75%의 1로 이루어진 Binary Set일 때, stratify=Y로 설정하면 나누어진 데이터셋들도 0과 1을 각각 25%, 75%로 유지한 채 분할된다. [출처](http://blog.naver.com/PostView.nhn?blogId=siniphia&logNo=221396370872&redirect=Dlog&widgetTypeCall=true&directAccess=false)

```python
# Overfitting and underfitting
## Setup arrays to store train and test accuracies
neighbors = np.arange(1, 9)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

## Loop over different values of k
for i, k in enumerate(neighbors):
    ## Setup a k-NN Classifier with k neighbors: knn
    knn = KNeighborsClassifier(n_neighbors=k)

    ## Fit the classifier to the training data
    knn.fit(X_train, y_train)
    
    ## Compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, y_train)

    ## Compute accuracy on the testing set
    test_accuracy[i] = knn.score(X_test, y_test)

## Generate plot
plt.title('k-NN: Varying Number of Neighbors')
plt.plot(neighbors, test_accuracy, label = 'Testing Accuracy')
plt.plot(neighbors, train_accuracy, label = 'Training Accuracy')
plt.legend()
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy')
plt.show()

```

# 2. Regression
## 2.1 Introduction to regression

```python
# Importing data for supervised learning
import numpy as np
import pandas as pd

df = pd.read_csv('gapminder.csv')

## Create arrays for features and target variable
y = df['life'].values
X = df['fertility'].values

## Print the dimensions of X and y before reshaping
print("Dimensions of y before reshaping: {}".format(y.shape))
print("Dimensions of X before reshaping: {}".format(X.shape))

## Reshape X and y
y = y.reshape(-1, 1)
X = X.reshape(-1, 1)

## Print the dimensions of X and y after reshaping
print("Dimensions of y after reshaping: {}".format(y.shape))
print("Dimensions of X after reshaping: {}".format(X.shape))
```
> .reshape(row, col) : 기존의 numpy.array의 차원을 재구성하고 싶을 때 사용한다. <br>
row, col에는 integer가 들어가지만 예외로 '-1'을 사용할 수 있다. '-1'의 의미는 -1이 아닌 arg에 근거해 나누라는 것으로, 위의 y.reshape(-1, 1)을 예로 들면 col을 1로 맞춰놓고 나머지를 row로 배분하라는 의미다. 

## 2.2 The basics of linear regression

```python
# Fit & predict for regression
from sklearn.linear_model import LinearRegression

reg = LinearRegression() ## Create the regressor: reg

prediction_space = np.linspace(min(X_fertility), max(X_fertility)).reshape(-1,1) ## Create the prediction space

reg.fit(X_fertility, y) ## Fit the model to the data

y_pred = reg.predict(prediction_space) ## Compute predictions over the prediction space: y_pred

print(reg.score(X_fertility, y)) ## Print R^2 

plt.plot(prediction_space, y_pred, color='black', linewidth=3)
plt.show()
```

```python
# Train/test split for regression
# Import necessary modules
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)

# Create the regressor: reg_all
reg_all = LinearRegression()

# Fit the regressor to the training data
reg_all.fit(X_train, y_train)

# Predict on the test data: y_pred
y_pred = reg_all.predict(X_test)

# Compute and print R^2 and RMSE
print("R^2: {}".format(reg_all.score(X_test, y_test)))
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error: {}".format(rmse))
```

## 2.3 Cross-validation

```python
# 5-fold cross-validation
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import cross_val_score 

reg = LinearRegression() ## Create a linear regression object: reg
cv_scores = cross_val_score(reg, X, y, cv=5) ## Compute 5-fold cross-validation scores: cv_scores

print(cv_scores) ## Print the 5-fold cross-validation scores
print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores)))
```
```python
# k-fold CV comparison
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import cross_val_score 

reg = LinearRegression() ## Create a linear regression object: reg

cvscores_3 = cross_val_score(reg, X, y, cv=3) ## Perform 3-fold CV
print(np.mean(cvscores_3))

cvscores_10 = cross_val_score(reg, X, y, cv=10) ## Perform 10-fold CV
print(np.mean(cvscores_10))
```

## 2.4 Regularized regression

```python
# Regularization I: Lasso
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.4, normalize = True) ## Instantiate a lasso regressor: lasso
lasso.fit(X, y) ## Fit the regressor to the data

lasso_coef = lasso.fit(X, y).coef_ ## Compute and print the coefficients
print(lasso_coef)

plt.plot(range(len(df_columns)), lasso_coef)
plt.xticks(range(len(df_columns)), df_columns.values, rotation=60)
plt.margins(0.02)
plt.show()
```

```python
# Regularization I: Ridge
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

## Setup the array of alphas and lists to store scores
alpha_space = np.logspace(-4, 0, 50)
ridge_scores = []
ridge_scores_std = []

## Create a ridge regressor: ridge
ridge = Ridge(normalize = True)

## Compute scores over range of alphas
for alpha in alpha_space:

    ## Specify the alpha value to use: ridge.alpha
    ridge.alpha = alpha
    
    ## Perform 10-fold CV: ridge_cv_scores
    ridge_cv_scores = cross_val_score(ridge, X, y, cv=10)
    
    ## Append the mean of ridge_cv_scores to ridge_scores
    ridge_scores.append(np.mean(ridge_cv_scores))
    
    ## Append the std of ridge_cv_scores to ridge_scores_std
    ridge_scores_std.append(np.std(ridge_cv_scores))

display_plot(ridge_scores, ridge_scores_std) ## Display the plot
```

# 3. Fine-tuning your model
## 3.1 How good is your model
'얼마나 정확히 분류하는가'가 기준으로 삼으면 model의 accuracy를 산술적으로 계산할 수 있다. 산술적으로 계산하기 위해 '기준'에 대한 판별조건이 필요한데, '걸러내야할 것을 얼마나 잘 분류하는가'와 '걸러내지 말아야할 것을 얼마나 잘 분류하는가'가 판별조건이다. 예를 들어, 1천만 개의 e-mail에서 spam mail을 찾아내는 classifier를 만들었다고 했을 때 위의 판별조건에 따라 'spam을 잘 분류하는지'와 'spam이 아닌 것을 잘 분류하는지'가 해당 classifier의 accuracy score가 되는 것이다. 

```python
# Metrics for classification
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix 

## Create training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state=42)

knn = KNeighborsClassifier(n_neighbors=6) ## Instantiate a k-NN classifier: knn
knn.fit(X_train, y_train) ## Fit the classifier to the training data

y_pred = knn.predict(X_test) ## Predict the labels of the test data: y_pred

## Generate the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```
## 3.2 Logistic regression and the ROC curve


```python
# Building a logistic regression model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

## Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state=42)

logreg = LogisticRegression() ## Create the classifier: logreg
logreg.fit(X_train, y_train) ## Fit the classifier to the training data
y_pred = logreg.predict(X_test) ## Predict the labels of the test set: y_pred

## Compute and print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```
```python
# Plotting an ROC curve
from sklearn.metrics import roc_curve

## Compute predicted probabilities: y_pred_prob
y_pred_prob = logreg.predict_proba(X_test)[:,1]

## Generate ROC curve values: fpr, tpr, thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

## Plot ROC curve
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='Logistic Regression')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

```
## 3.3 Area under the ROC curve : AUC

```python
# AUC computation
from sklearn.metrics import roc_auc_score 
from sklearn.model_selection import cross_val_score

## Compute predicted probabilities: y_pred_prob
y_pred_prob = logreg.predict_proba(X_test)[:,1]

## Compute and print AUC score
print("AUC: {}".format(roc_auc_score(y_test, y_pred_prob)))

## Compute cross-validated AUC scores: cv_auc
cv_auc = cross_val_score(logreg, X, y, cv = 5, scoring = 'roc_auc')

print("AUC scores computed using 5-fold cross-validation: {}".format(cv_auc))
```

## 3.4 Hyperparameter tuning

```python
# Hyperparameter tuning with GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

## Setup the hyperparameter grid
c_space = np.logspace(-5, 8, 15)
param_grid = {'C': c_space}

logreg = LogisticRegression() ## Instantiate a logistic regression classifier: logreg
logreg_cv = GridSearchCV(logreg, param_grid, cv=5) ## Instantiate the GridSearchCV object: logreg_cv
logreg_cv.fit(X, y) ## Fit it to the data

## Print the tuned parameters and score
print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_)) 
print("Best score is {}".format(logreg_cv.best_score_))
```

```python
# Hyperparameter tuning with RandomizedSearchCV
from scipy.stats import randint
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import RandomizedSearchCV

## Setup the parameters and distributions to sample from: param_dist
param_dist = {"max_depth": [3, None],
              "max_features": randint(1, 9),
              "min_samples_leaf": randint(1, 9),
              "criterion": ["gini", "entropy"]}

tree = DecisionTreeClassifier() ## Instantiate a Decision Tree classifier: tree
tree_cv = RandomizedSearchCV(tree, param_dist, cv=5) ## Instantiate the RandomizedSearchCV object: tree_cv
tree_cv.fit(X, y) ## Fit it to the data

## Print the tuned parameters and score
print("Tuned Decision Tree Parameters: {}".format(tree_cv.best_params_))
print("Best score is {}".format(tree_cv.best_score_))
```

## 3.5 Hold-out set for final evaluation

```python
# Hold-out set in practice I: Classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

## Create the hyperparameter grid
c_space = np.logspace(-5, 8, 15)
param_grid = {'C': c_space, 'penalty': ['l1', 'l2']}

logreg = LogisticRegression() ## Instantiate the logistic regression classifier: logreg
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42) ## Create train and test sets

logreg_cv = GridSearchCV(logreg, param_grid, cv = 5) ## Instantiate the GridSearchCV object: logreg_cv
logreg_cv.fit(X_train, y_train) ## Fit it to the training data

print("Tuned Logistic Regression Parameter: {}".format(logreg_cv.best_params_))
print("Tuned Logistic Regression Accuracy: {}".format(logreg_cv.best_score_))

```

```python
# Hold-out set in practice II: Regression
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split

## Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

## Create the hyperparameter grid
l1_space = np.linspace(0, 1, 30)
param_grid = {'l1_ratio': l1_space}

elastic_net = ElasticNet() ## Instantiate the ElasticNet regressor: elastic_net
gm_cv = GridSearchCV(elastic_net, param_grid, cv=5) ## Setup the GridSearchCV object: gm_cv
gm_cv.fit(X_train, y_train) ## Fit it to the training data

y_pred = gm_cv.predict(X_test)
r2 = gm_cv.score(X_test, y_test)
mse = mean_squared_error(y_test, y_pred)
print("Tuned ElasticNet l1 ratio: {}".format(gm_cv.best_params_))
print("Tuned ElasticNet R squared: {}".format(r2))
print("Tuned ElasticNet MSE: {}".format(mse))
```

# 4. Preprocessing and pipelines
## 4.1 Preprocessing data
```python
# Exploring categorical features
import pandas as pd
df = pd.read_csv('gapminder.csv')

df.boxplot('life', 'Region', rot=60) ## Create a boxplot of life expectancy per region

plt.show()
```

```python
# Creating dummy variables
df_region = pd.get_dummies(df) ## Create dummy variables: df_region
print(df_region.columns) ## Print the columns of df_region

df_region = pd.get_dummies(df, drop_first=True) ## Create dummy variables with drop_first=True: df_region
print(df_region.columns) ## Print the new columns of df_region
```

```python
# Regression with categorical features
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

ridge = Ridge(alpha = 0.5, normalize = True) ## Instantiate a ridge regressor: ridge
ridge_cv = cross_val_score(ridge, X, y, cv = 5) ## Perform 5-fold cross-validation: ridge_cv
print(ridge_cv) ## Print the cross-validated scores
```

## 4.2 Handling missing data

```python
# Dropping missing data
df[df == '?'] = np.nan ## Convert '?' to NaN
print(df.isnull().sum()) ## Print the number of NaNs

print("Shape of Original DataFrame: {}".format(df.shape)) ## Print shape of original DataFrame

df = df.dropna() ## Drop missing values and print shape of new DataFrame
print("Shape of DataFrame After Dropping All Rows with Missing Values: {}".format(df.shape)) ## Print shape of new DataFrame
```

```python
# Imputing missing data in a ML Pipeline I
from sklearn.preprocessing import Imputer
from sklearn.svm import SVC

imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=0) ## Setup the Imputation transformer: imp
clf = SVC() ## Instantiate the SVC classifier: clf

## Setup the pipeline with the required steps: steps
steps = [('imputation', imp),
        ('SVM', clf)]
```

```python
# Imputing missing data in a ML Pipeline II
from sklearn.preprocessing import Imputer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

steps = [('imputation', Imputer(missing_values='NaN', strategy='most_frequent', axis=0)),
        ('SVM', SVC())]

pipeline = Pipeline(steps) ## Create the pipeline: pipeline

## Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

pipeline.fit(X_train, y_train) ## Fit the pipeline to the train set
y_pred = pipeline.predict(X_test) ## Predict the labels of the test set

print(classification_report(y_test, y_pred)) ## Compute metrics
```

## 4.3 Centering and scaling

```python
# Centering and scaling your data
from sklearn.preprocessing import scale ## Import scale

X_scaled = scale(X) ## Scale the features: X_scaled

## Print the mean and standard deviation of the unscaled features
print("Mean of Unscaled Features: {}".format(np.mean(X))) 
print("Standard Deviation of Unscaled Features: {}".format(np.std(X)))

## Print the mean and standard deviation of the scaled features
print("Mean of Scaled Features: {}".format(np.mean(X_scaled))) 
print("Standard Deviation of Scaled Features: {}".format(np.std(X_scaled)))
```
```python
# Centering and scaling in a pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

## Setup the pipeline steps: steps
steps = [('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier())]
        
pipeline = Pipeline(steps) ## Create the pipeline: pipeline

## Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

knn_scaled = pipeline.fit(X_train, y_train) ## Fit the pipeline to the training set: knn_scaled
knn_unscaled = KNeighborsClassifier().fit(X_train, y_train) ## Instantiate and fit a k-NN classifier to the unscaled data

## Compute and print metrics
print('Accuracy with Scaling: {}'.format(knn_scaled.score(X_test, y_test)))
print('Accuracy without Scaling: {}'.format(knn_unscaled.score(X_test, y_test)))
```

```python
# Bringing it all together I: Pipeline for classification
## Setup the pipeline
steps = [('scaler', StandardScaler()),
         ('SVM', SVC())]

pipeline = Pipeline(steps)

## Specify the hyperparameter space
parameters = {'SVM__C':[1, 10, 100],
              'SVM__gamma':[0.1, 0.01]}

## Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 21)

cv = GridSearchCV(pipeline, parameters, cv = 3) ## Instantiate the GridSearchCV object: cv
cv.fit(X_train, y_train) ## Fit to the training set

y_pred = cv.predict(X_test) ## Predict the labels of the test set: y_pred

## Compute and print metrics
print("Accuracy: {}".format(cv.score(X_test, y_test)))
print(classification_report(y_test, y_pred))
print("Tuned Model Parameters: {}".format(cv.best_params_))
```

> Q. 'step_name__parameter_name'의 이유가 있나? <br> A. 


```python
# Bringing it all together II: Pipeline for regression
## Setup the pipeline steps: steps
steps = [('imputation', Imputer(missing_values='NaN', strategy='mean', axis=0)),
         ('scaler', StandardScaler()),
         ('elasticnet', ElasticNet())]

pipeline = Pipeline(steps) ## Create the pipeline: pipeline 
parameters = {'elasticnet__l1_ratio':np.linspace(0,1,30)} ## Specify the hyperparameter space

## Create train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

gm_cv = GridSearchCV(pipeline, parameters) ## Create the GridSearchCV object: gm_cv
gm_cv.fit(X_train, y_train) ## Fit to the training set

## Compute and print the metrics
r2 = gm_cv.score(X_test, y_test)
print("Tuned ElasticNet Alpha: {}".format(gm_cv.best_params_))
print("Tuned ElasticNet R squared: {}".format(r2))
```
