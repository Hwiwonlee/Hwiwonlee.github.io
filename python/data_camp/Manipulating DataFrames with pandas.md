# 1. Extracting and transforming data

Pandas에서 지원하는 DataFrame은 data analysis에 굉장히 유용한 object다. DataFrame형태가 특별한 것은 아니지만 Pandas에서 DataFrame에 적용할 수 있는 유용한 function과 method를 지원하고 있기 때문이다. 이번에 배울 data set을 추출하거나 편집하는 등의 data preprocessing에서도 Pandas는 여러 기능들을 제공하고 있다. Pandas의 function과 method를 이용해 data set을 편집해보자. 

## 1.1 Indexing DataFrames
Index를 통해 dataframe의 특정 obs에 접근하거나 추출하는 방법을 알아보자. 전에 배운 accessor, .loc, .iloc를 이용한 방법을 되새겨보는 시간 또한 가질 것이다. 

```python
# Positional and labeled indexing
## 선거 data인 election를 이용함. 
election.head()
x = 4 ## Assign the row position of election.loc['Bedford']: x
y = 4 ## Assign the column position of election['winner']: y

print(election.iloc[x, y] == election.loc['Bedford', 'winner']) ## Print the boolean equivalence
## 즉 label을 arg로 갖는 .loc와 index를 arg로 갖는 .iloc의 결과가 같은 것을 보임 

# Indexing and column rearrangement
import pandas as pd
election = pd.read_csv(filename, index_col='county') ## Read in filename and set the index: election
## pd.read_csv(, index_col = column) : dataset의 특정 열을 index로 선언할 때 사용 
results = election[['winner', 'total', 'voters']] ## 'winner', 'total', 'voters'만 뽑아내기 

print(results.head())
````

## 1.2 Slicing DataFrames
indexing의 가장 기본인 slicing으로 DF의 data를 추출해보자. 잊을만 하면 한번씩 말하지만 python은 zero-indexing이고 (start) : (end-1)의 colon indexing이 default다. 

```python
# Slicing rows
p_counties = election['Perry':'Potter']
print(p_counties)

p_counties_rev = election['Potter':'Perry':-1] ## Slice the row labels 'Potter' to 'Perry' in reverse order: p_counties_rev
## dataset에는 a:b로 되어 있지만 reverse-ordering은 b:a:-1로 가능하다. 
print(p_counties_rev)
## row indexing이 default다. 

# Slicing columns
left_columns = election.loc[:, :'Obama']
print(left_columns.head())

middle_columns = election.loc[:, 'Obama':'winner']
print(middle_columns.head())

right_columns = election.loc[:, 'Romney':]
print(right_columns.head())
## column label indexing를 위해 .loc를 사용했다.

# Subselecting DataFrames with lists
rows = ['Philadelphia', 'Centre', 'Fulton']
cols = ['winner', 'Obama', 'Romney']

three_counties = election.loc[rows, cols] ## 이런 식의 subselecting도 가능하다. 
print(three_counties)
```

## 1.3 Filtering DataFrames
이전까지 slicing이나 indexing을 배웠지만 filtering이 data analysis 상황에서 좀 더 일반적인 도구이다. dataset이 점점 커지면서 우린 dataset에서 특정 조건을 갖는 obs를 찾거나 subdataset을 만들어야 하는 경우가 많아지는데 이 때 filtering을 이용한다. 이제 Pandas를 이용한 filtering 방법을 알아보자. 

```python
# Thresholding data
high_turnout = election['turnout'] >= 70 ## Create the boolean array: high_turnout

high_turnout_df = election[high_turnout] ## Filter the election DataFrame with the high_turnout array: high_turnout_df
## filtering의 기본 스킬 중 하나인 boolean 을 이용한 masking이다. 조건에 맞는 row만 뽑아내기 위한 방법이다. 

print(high_turnout_df)

# Filtering columns using other columns
import numpy as np

too_close = election['margin'] <= 1 ## for masking
election.winner[too_close] = np.nan ## Assign np.nan to the 'winner' column where the results were too close to call

print(election.info())

# Filtering using NaNs 
df = titanic[['age', 'cabin']]
print(df.shape)

print(df.dropna(how = 'any').shape) ## how='any' : 행에서 Na가 하나라도 있으면 drop
print(df.dropna(how = 'all').shape) ## how='all' : 행에서 모든 obs가 Na면 drop

print(titanic.dropna(thresh=1000, axis='columns').info()) 
## Drop columns in titanic with less than 1000 non-missing values
## 1000개 미만의 non-missing value를 가진 column을 drop
## .dropna()의 default는 행 기준이다. axis를 따로 설정해주면 바꿀 수 있음. 
```

## 1.4 Transforming DataFrames

```python
# Using apply() to transform a column
def to_celsius(F): ## Write a function to convert degrees Fahrenheit to degrees Celsius: to_celsius
    return 5/9*(F - 32)

df_celsius = weather[['Mean TemperatureF', 'Mean Dew PointF']].apply(to_celsius) ## Apply the function over 'Mean TemperatureF' and 'Mean Dew PointF': df_celsius
df_celsius .columns = ['Mean TemperatureC', 'Mean Dew PointC'] ## Reassign the column labels of df_celsius

print(df_celsius.head())

# Using .map() with a dictionary
red_vs_blue = {'Obama':'blue','Romney':'red'} ## Create the dictionary: red_vs_blue

election['color'] = election['winner'].map(red_vs_blue) ## Use the dictionary to map the 'winner' column to the new column: election['color']
## election['winner']의 obs에 따라 이미 정의해준 dict, 'red_vs_blue'로 red or blue를 추가(.map)

print(election.head())

# Using vectorized functions
from scipy.stats import zscore
turnout_zscore = zscore(election['turnout']) ## Call zscore with election['turnout'] as input: turnout_zscore

print(type(turnout_zscore)) 

election['turnout_zscore'] = turnout_zscore ## Assign turnout_zscore to a new column: election['turnout_zscore']

print(election.head())
```

# 2. Advanced indexing
## 2.1 Index objects and labeled data

```python
# Changing index of a DataFrame
new_idx = [month.upper() for month in sales.index]
sales.index = new_idx

print(sales)

## Q. 이거 이해 안되는데

# Changing index name labels
sales.index.name = 'MONTHS'
print(sales)

sales.columns.name = 'PRODUCTS'
print(sales)

# Building an index, then a DataFrame
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales.index = months

print(sales)
````

## 2.2 Hierarchical indexing
Index도 level을 가질 수 있는데 수준에 따른 indexing이 hierarchical indexing혹은 Multindex다. hierarchical indexing이 무엇인지, 어떻게 접근할 수 있는지 알아보자. 


```python
# Extracting data with a MultiIndex
print(sales.loc[['CA', 'TX']]) ## Print sales.loc[['CA', 'TX']]
print(sales['CA':'TX']) ## Print sales['CA':'TX']

# Setting & sorting a MultiIndex
sales = sales.set_index(['state', 'month']) ## Set the index to be the columns ['state', 'month']: sales
sales = sales.sort_index() ## Sort the MultiIndex: sales

print(sales)

# Using .loc[] with nonunique indexes
sales = sales.set_index('state') ## Set the index to the column 'state': sales
print(sales)

print(sales.loc['NY'])

# Indexing multiple levels of a MultiIndex
NY_month1 = sales.loc[('NY', slice(1)), : ] ## Look up data for NY in month 1 in sales: NY_month1
CA_TX_month2 = sales.loc[(('CA', 'TX'), 2), : ] ## Look up data for CA and TX in month 2: CA_TX_month2
all_month2 = sales.loc[(('NY', 'CA', 'TX'), 2), : ] ## Access the inner month index and look up data for all states in month 2: all_month2

```
