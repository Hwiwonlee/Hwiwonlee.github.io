# 1. Exploring the raw data
## 1.1 Exploring the data
```python
# Summarizing the data
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('Training.csv')

df.info()
print(df.describe())

plt.hist(df['FTE'].dropna())

plt.title('Distribution of %full-time \n employee works')
plt.xlabel('% of full-time')
plt.ylabel('num employees')
plt.show()
```

## 1.2 Looking at the datatypes

```python
# Exploring datatypes in pandas
df.dtypes.value_counts() 
```
> .dtypes : feature의 type return <br> .value_counts() : 해당 dataset의 value 값을 count해서 return

```python
# Encode the labels as categorical variables
categorize_label = lambda x: x.astype('category') ## Define the lambda function: categorize_label

df[LABELS] = df[LABELS].apply(categorize_label, axis = 0) ## Convert df[LABELS] to a categorical type

print(df[LABELS].dtypes) ## Print the converted dtypes
```
> .apply(func, axis) : axis = 0은 '해당 func을 column에 적용하라'는 의미다. 

```python
# Counting unique labels
import matplotlib.pyplot as plt

num_unique_labels = df[LABELS].apply(pd.Series.nunique, axis = 0) ## Calculate number of unique values for each label: num_unique_labels
num_unique_labels.plot(kind='bar') ## Plot number of unique values for each label

plt.xlabel('Labels')
plt.ylabel('Number of unique values')
plt.show()
```
## 1.3 How do we measure success?

```python
# Computing log loss with NumPy
## Compute and print log loss for 1st case
correct_confident_loss = compute_log_loss(correct_confident, actual_labels)
print("Log loss, correct and confident: {}".format(correct_confident_loss)) 

## Compute log loss for 2nd case
correct_not_confident_loss = compute_log_loss(correct_not_confident, actual_labels)
print("Log loss, correct and not confident: {}".format(correct_not_confident_loss)) 

## Compute and print log loss for 3rd case
wrong_not_confident_loss = compute_log_loss(wrong_not_confident, actual_labels)
print("Log loss, wrong and not confident: {}".format(wrong_not_confident_loss)) 

## Compute and print log loss for 4th case
wrong_confident_loss = compute_log_loss(wrong_confident, actual_labels)
print("Log loss, wrong and confident: {}".format(wrong_confident_loss)) 

## Compute and print log loss for actual labels
actual_labels_loss = compute_log_loss(actual_labels, actual_labels)
print("Log loss, actual labels: {}".format(actual_labels_loss)) 

```
> Q. Log loss? 알아보자. <br> A. 

# 2. Creating a simple first model
## 2.1 It's time to build a model

```python
# Setting up a train-test split in scikit-learn
numeric_data_only = df[NUMERIC_COLUMNS].fillna(-1000) ## Create the new DataFrame: numeric_data_only

label_dummies = pd.get_dummies(df[LABELS]) ## Get labels and convert to dummy variables: label_dummies

## Create training and test sets
X_train, X_test, y_train, y_test = multilabel_train_test_split(numeric_data_only,
                                                               label_dummies,
                                                               size=0.2, 
                                                               seed=123)
print("X_train info:")
print(X_train.info())
print("\nX_test info:")  
print(X_test.info())
print("\ny_train info:")  
print(y_train.info())
print("\ny_test info:")  
print(y_test.info()) 
```
> To do. pd.get_dummies()의 효과는?

```python
# Training a model
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

numeric_data_only = df[NUMERIC_COLUMNS].fillna(-1000) ## Create the DataFrame: numeric_data_only
label_dummies = pd.get_dummies(df[LABELS]) ## Get labels and convert to dummy variables: label_dummies

## Create training and test sets
X_train, X_test, y_train, y_test = multilabel_train_test_split(numeric_data_only,
                                                               label_dummies,
                                                               size=0.2, 
                                                               seed=123)

clf = OneVsRestClassifier(LogisticRegression()) ## Instantiate the classifier: clf
clf.fit(X_train, y_train) ## Fit the classifier to the training data
print("Accuracy: {}".format(clf.score(X_test, y_test))) ## Print the accuracy
```
> To do. OneVsRestClassifier(LogisticRegression()) 이거 좀 신기하게 생겼는데? 

## 2.2 Making predictions

```python
# Use your model to predict values on holdout data
clf = OneVsRestClassifier(LogisticRegression()) ## Instantiate the classifier: clf

clf.fit(X_train, y_train) ## Fit it to the training data
holdout = pd.read_csv('HoldoutData.csv', index_col=0) ## Load the holdout data: holdout

predictions = clf.predict_proba(holdout[NUMERIC_COLUMNS].fillna(-1000)) ## Generate predictions: predictions
```

```python
# Writing out your results to a csv for submission
predictions = clf.predict_proba(holdout[NUMERIC_COLUMNS].fillna(-1000)) ## Generate predictions: predictions

## Format predictions in DataFrame: prediction_df
prediction_df = pd.DataFrame(columns=pd.get_dummies(df[LABELS]).columns,
                             index=holdout.index,
                             data=predictions)


prediction_df.to_csv('predictions.csv') ## Save prediction_df to csv
score = score_submission(pred_path = 'predictions.csv') ## Submit the predictions for scoring: score

print('Your model, trained with numeric data only, yields logloss score: {}'.format(score))
```

## 2.3 Representing text numerically

```python
# Creating a bag-of-words in scikit-learn
from sklearn.feature_extraction.text import CountVectorizer ## Import CountVectorizer
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)' ## Create the token pattern: TOKENS_ALPHANUMERIC
 
df.Position_Extra.fillna('', inplace=True) ## Fill missing values in df.Position_Extra
vec_alphanumeric = CountVectorizer(token_pattern=TOKENS_ALPHANUMERIC) ## Instantiate the CountVectorizer: vec_alphanumeric

vec_alphanumeric.fit(df.Position_Extra) ## Fit to the data

## Print the number of tokens and first 15 tokens
msg = "There are {} tokens in Position_Extra if we split on non-alpha numeric"
print(msg.format(len(vec_alphanumeric.get_feature_names())))
print(vec_alphanumeric.get_feature_names()[:15])
```

```python
# Combining text columns for tokenization
## Define combine_text_columns()
def combine_text_columns(data_frame, to_drop=NUMERIC_COLUMNS + LABELS):
    """ converts all text in each row of data_frame to single vector """
    
    ## Drop non-text columns that are in the df
    to_drop = set(to_drop) & set(data_frame.columns.tolist())
    text_data = data_frame.drop(to_drop, axis = 1)
    
    ## Replace nans with blanks
    text_data.fillna("", inplace = True)
    
    ## Join all text items in a row that have a space in between
    return text_data.apply(lambda x: " ".join(x), axis=1)
```

```python
# What's in a token?
from sklearn.feature_extraction.text import CountVectorizer ## Import the CountVectorizer

TOKENS_BASIC = '\\S+(?=\\s+)' ## Create the basic token pattern
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)' ## Create the alphanumeric token pattern

vec_basic = CountVectorizer(token_pattern = TOKENS_BASIC) ## Instantiate basic CountVectorizer: vec_basic
vec_alphanumeric = CountVectorizer(token_pattern = TOKENS_ALPHANUMERIC) ## Instantiate alphanumeric CountVectorizer: vec_alphanumeric

text_vector = combine_text_columns(df) ## Create the text vector

vec_basic.fit_transform(text_vector) ## Fit and transform vec_basic

## Print number of tokens of vec_basic
print("There are {} tokens in the dataset".format(len(vec_basic.get_feature_names())))

vec_alphanumeric.fit_transform(text_vector) ## Fit and transform vec_alphanumeric

## Print number of tokens of vec_alphanumeric
print("There are {} alpha-numeric tokens in the dataset".format(len(vec_alphanumeric.get_feature_names())))
```

# 3. Improving your model
## 3.1 Pipelines, feature & text preprocessing
```python
# Instantiate pipeline

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

## Split and select numeric data only, no nans 
X_train, X_test, y_train, y_test = train_test_split(sample_df[['numeric']],
                                                    pd.get_dummies(sample_df['label']), 
                                                    random_state=22)

## Instantiate Pipeline object: pl
pl = Pipeline([('clf', OneVsRestClassifier(LogisticRegression()))])

pl.fit(X_train, y_train) ## Fit the pipeline to the training data

accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on sample data - numeric, no nans: ", accuracy)
```

```python
# Preprocessing numeric features
from sklearn.preprocessing import Imputer

## Create training and test sets using only numeric data
X_train, X_test, y_train, y_test = train_test_split(sample_df[['numeric', 'with_missing']],
                                                    pd.get_dummies(sample_df['label']), 
                                                    random_state=456)

## Insantiate Pipeline object: pl
pl = Pipeline([
        (('imp', Imputer())),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])


pl.fit(X_train, y_train) ## Fit the pipeline to the training data

## Compute and print accuracy
accuracy = pl.score(X_test, y_test)
print("\nAccuracy on sample data - all numeric, incl nans: ", accuracy)
```

## 3.2 Text features and feature unions


```python
# Preprocessing text features
from sklearn.feature_extraction.text import CountVectorizer

## Split out only the text data
X_train, X_test, y_train, y_test = train_test_split(sample_df['text'],
                                                    pd.get_dummies(sample_df['label']), 
                                                    random_state=456)

## Instantiate Pipeline object: pl
pl = Pipeline([
        ('vec', CountVectorizer()),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])

pl.fit(X_train, y_train) ## Fit to the training data

accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on sample data - just text data: ", accuracy)
```

```python
# Multiple types of processing: FunctionTransformer
from sklearn.preprocessing import FunctionTransformer ## Import FunctionTransformer

## Obtain the text data: get_text_data
get_text_data = FunctionTransformer(lambda x: x['text'], validate=False) 

## Obtain the numeric data: get_numeric_data
get_numeric_data = FunctionTransformer(lambda x: x[['numeric', 'with_missing']], validate=False)

just_text_data = get_text_data.fit_transform(sample_df) ## Fit and transform the text data: just_text_data
just_numeric_data = get_numeric_data.fit_transform(sample_df) ## Fit and transform the numeric data: just_numeric_data

## Print head to check results
print('Text Data')
print(just_text_data.head())
print('\nNumeric Data')
print(just_numeric_data.head())
```
> Q. get_text_data.fit_transform(sample_df)? 이게 왜 전처리 과정에 있는 걸까? <br> A. 

```python
# Multiple types of processing: FeatureUnion
from sklearn.pipeline import FeatureUnion ## Import FeatureUnion

## Split using ALL data in sample_df
X_train, X_test, y_train, y_test = train_test_split(sample_df[['numeric', 'with_missing', 'text']],
                                                    pd.get_dummies(sample_df['label']), 
                                                    random_state=22)

## Create a FeatureUnion with nested pipeline: process_and_join_features
process_and_join_features = FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer())
                ]))
             ]
        )

## Instantiate nested pipeline: pl
pl = Pipeline([
        ('union', process_and_join_features),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])


pl.fit(X_train, y_train) ## Fit pl to the training data

accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on sample data - all data: ", accuracy)
```
> To do : FeatureUnion의 구조 이해해보기. 어마어마하네

## 3.3 Choosing a classification model

```python
# Using FunctionTransformer on the main dataset
from sklearn.preprocessing import FunctionTransformer

dummy_labels = pd.get_dummies(df[LABELS]) ## Get the dummy encoding of the labels
NON_LABELS = [c for c in df.columns if c not in LABELS] ## Get the columns that are features in the original df

## Split into training and test sets
X_train, X_test, y_train, y_test = multilabel_train_test_split(df[NON_LABELS],
                                                               dummy_labels,
                                                               0.2, 
                                                               seed=123)

## Preprocess the text data: get_text_data
get_text_data = FunctionTransformer(combine_text_columns, validate=False)

## Preprocess the numeric data: get_numeric_data
get_numeric_data = FunctionTransformer(lambda x: x[NUMERIC_COLUMNS], validate=False)
```

```python
# Add a model to the pipeline
## Complete the pipeline: pl
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer())
                ]))
             ]
        )),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])

pl.fit(X_train, y_train) ## Fit to the training data
accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on budget dataset: ", accuracy)
```
> To do. 와 pipeline 어마어마하네. 


```python
# Try a different class of model
from sklearn.ensemble import RandomForestClassifier

## Edit model step in pipeline
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer())
                ]))
             ]
        )),
        ('clf', RandomForestClassifier())
    ])

pl.fit(X_train, y_train) ## Fit to the training data
accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on budget dataset: ", accuracy)
```

```python
# Can you adjust the model or parameters to improve accuracy?
from sklearn.ensemble import RandomForestClassifier

## Add model step to pipeline: pl
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer())
                ]))
             ]
        )),
        ('clf', RandomForestClassifier(n_estimators=15))
    ])

pl.fit(X_train, y_train) ## Fit to the training data
accuracy = pl.score(X_test, y_test) ## Compute and print accuracy
print("\nAccuracy on budget dataset: ", accuracy)
```

# 4. Learning from the experts
## 4.1 Learning from the expert: processing

```python
# Deciding what's a word
from sklearn.feature_extraction.text import CountVectorizer

text_vector = combine_text_columns(X_train) ## Create the text vector
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)' ## Create the token pattern: TOKENS_ALPHANUMERIC

## Instantiate the CountVectorizer: text_features
text_features = CountVectorizer(token_pattern=TOKENS_ALPHANUMERIC)

text_features.fit(text_vector) ## Fit text_features to the text vector

## Print the first 10 tokens
print(text_features.get_feature_names()[:10])
```

```python
# N-gram range in scikit-learn
## Import pipeline
from sklearn.pipeline import Pipeline

## Import classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

## Import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

## Import other preprocessing modules
from sklearn.preprocessing import Imputer
from sklearn.feature_selection import chi2, SelectKBest

chi_k = 300 ## Select 300 best features

## Import functional utilities
from sklearn.preprocessing import FunctionTransformer, MaxAbsScaler
from sklearn.pipeline import FeatureUnion

## Perform preprocessing
get_text_data = FunctionTransformer(combine_text_columns, validate=False)
get_numeric_data = FunctionTransformer(lambda x: x[NUMERIC_COLUMNS], validate=False)

## Create the token pattern: TOKENS_ALPHANUMERIC
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)'

## Instantiate pipeline: pl
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer(token_pattern=TOKENS_ALPHANUMERIC,
                                                   ngram_range=(1, 2))),
                    ('dim_red', SelectKBest(chi2, chi_k))
                ]))
             ]
        )),
        ('scale', MaxAbsScaler()),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])
```

## 4.2 Learning from the expert: a stats trick


```python
# Implement interaction modeling in scikit-learn
## Instantiate pipeline: pl
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', CountVectorizer(token_pattern=TOKENS_ALPHANUMERIC,
                                                   ngram_range=(1, 2))),  
                    ('dim_red', SelectKBest(chi2, chi_k))
                ]))
             ]
        )),
        ('int', SparseInteractions(degree=2)),
        ('scale', MaxAbsScaler()),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])
```

## 4.3 Learning from the expert: a computational trick and the winning model

```python
# Implementing the hashing trick in scikit-learn
from sklearn.feature_extraction.text import HashingVectorizer

## Get text data: text_data
text_data = combine_text_columns(X_train)

## Create the token pattern: TOKENS_ALPHANUMERIC
TOKENS_ALPHANUMERIC = '[A-Za-z0-9]+(?=\\s+)' 

## Instantiate the HashingVectorizer: hashing_vec
hashing_vec = HashingVectorizer(token_pattern = TOKENS_ALPHANUMERIC)

## Fit and transform the Hashing Vectorizer
hashed_text = hashing_vec.fit_transform(text_data)

## Create DataFrame and print the head
hashed_df = pd.DataFrame(hashed_text.data)
print(hashed_df.head())
```

```python
# Build the winning model
from sklearn.feature_extraction.text import HashingVectorizer

## Instantiate the winning model pipeline: pl
pl = Pipeline([
        ('union', FeatureUnion(
            transformer_list = [
                ('numeric_features', Pipeline([
                    ('selector', get_numeric_data),
                    ('imputer', Imputer())
                ])),
                ('text_features', Pipeline([
                    ('selector', get_text_data),
                    ('vectorizer', HashingVectorizer(token_pattern=TOKENS_ALPHANUMERIC,
                                                     non_negative=True, norm=None, binary=False,
                                                     ngram_range=(1, 2))),
                    ('dim_red', SelectKBest(chi2, chi_k))
                ]))
             ]
        )),
        ('int', SparseInteractions(degree=2)),
        ('scale', MaxAbsScaler()),
        ('clf', OneVsRestClassifier(LogisticRegression()))
    ])
```
