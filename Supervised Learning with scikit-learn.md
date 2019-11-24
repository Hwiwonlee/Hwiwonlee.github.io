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
