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

# 3. Rearranging and reshaping data
## 3.1 Pivoting DataFrames
Pivoting이란 DF가 갖는 column을 '주축'으로 정의한 후 정의된 '주축'을 중심으로 obs을 넣어 새로운 형태의 DF를 만드는 방법이다. 이 때 사용하는 방법은 Pandas.pivot(index, columns, values)으로 index가 rows, columns가 columns, values가 obs으로 들어가게 된다.
```python
# Pivoting a single variable
visitors_pivot = users.pivot(index = 'weekday', columns = 'city', values = 'visitors') ## Pivot the users DataFrame: visitors_pivot
print(visitors_pivot) 


# Pivoting all variables
signups_pivot = users.pivot(index = 'weekday', columns = 'city', values = 'signups') ## Pivot users with signups indexed by weekday and city: signups_pivot

print(signups_pivot)

pivot = users.pivot(index = 'weekday', columns = 'city') ## Pivot users pivoted by both signups and visitors: pivot
pivot = users.pivot(index = 'weekday', columns = 'city', values = ['visitors', 'signups']) ## same result 
## 같은 결과가 나오는 이유는 users DF에서 index, columns를 빼면 남는 column이 2개 밖에 없기 때문. 

# Print the pivoted DataFrame
print(pivot)
```

## 3.2 Stacking & unstacking DataFrames

```python
# Stacking & unstacking I
byweekday = users.unstack(level = 'weekday') ## Unstack users by 'weekday': byweekday
print(byweekday)

print(byweekday.stack(level = 'weekday')) ## Stack byweekday by 'weekday' and print it

# Stacking & unstacking II
bycity = users.unstack(level = 'city') ## Unstack users by 'city': bycity

print(bycity)

print(bycity.stack(level = 'city')) ## Stack bycity by 'city' and print it
```
> Q. 왜 I과 II의 차이가 생기는 걸까? /n 답이 바로 뒤에 나오네.

```python
# Restoring the index order
newusers = bycity.stack(level = 'city') ## Stack 'city' back into the index of bycity: newusers

newusers = newusers.swaplevel(0, 1) ## Swap the levels of the index of newusers: newusers
## row 수준에서 multindex의 순서를 바꿔버림 
 
print(newusers) ## Print newusers and verify that the index is not sorted

newusers = newusers.sort_index() ## Sort the index of newusers: newusers, 순서 정렬 

print(newusers) ## Print newusers and verify that the index is now sorted
print(newusers.equals(users)) ## Verify that the new DataFrame is equal to the original

```

# 3.4 Melting DataFrames
Melting이란 DF에서 column형태로 있던 변수를 row level로 만들어 새로운 변수 안에 포함시키는 것이다. 쉽게 예를 들면 임상시험에서 처치 A, 처치 B, 처치 C 등 각 처치를 변수로 정의하고 그 안에 '효과'등의 observation을 넣은 경우, melt의 대상을 처치 A, B, C의 변수로 하고 해당 변수들을 '처치'로 묶어 '처치'변수 안에 row level의 처치 A, 처치 B, 처치 C로 변환하는 것이 melt이다. melitng이 필요한 이유는 알고리즘과 함수와 같은 computing 과정에서 사람이 읽기 편한 wide-wise보다 컴퓨터가 연산하기 좋은 long-wise의 형태가 더 좋기 때문이다. 

```python
# Adding names for readability
visitors_by_city_weekday = visitors_by_city_weekday.reset_index() ## Reset the index: visitors_by_city_weekday
print(visitors_by_city_weekday)

visitors = pd.melt(visitors_by_city_weekday, id_vars=['weekday'], value_name='visitors') ## Melt visitors_by_city_weekday: visitors
print(visitors)

# Going from wide to long
skinny = pd.melt(users, id_vars=['weekday', 'city']) ## Melt users: skinny
print(skinny)


# Obtaining key-value pairs with melt()
users_idx = users.set_index(['city', 'weekday']) ## Set the new index: users_idx
print(users_idx)

kv_pairs = pd.melt(users_idx, col_level = 0) ## Obtain the key-value pairs: kv_pairs
print(kv_pairs)

```

## 3.5 Pivot tables
```python
# Setting up a pivot table
by_city_day = users.pivot_table(index = 'weekday', columns = 'city') ## Create the DataFrame with the appropriate pivot table: by_city_day
print(by_city_day)

# Using other aggregations in pivot tables
count_by_weekday1 = users.pivot_table(index = 'weekday', aggfunc = 'count') ## Use a pivot table to display the count of each column: count_by_weekday1

print(count_by_weekday1)

count_by_weekday2 = users.pivot_table(index = 'weekday', aggfunc = len) ## Replace 'aggfunc='count'' with 'aggfunc=len': count_by_weekday2

print('==========================================')
print(count_by_weekday1.equals(count_by_weekday2))

# Using margins in pivot tables
signups_and_visitors = users.pivot_table(index = 'weekday', aggfunc = sum) ## Create the DataFrame with the appropriate pivot table: signups_and_visitors

print(signups_and_visitors)

signups_and_visitors_total = users.pivot_table(index = 'weekday', aggfunc = sum, margins = True) ## Add in the margins: signups_and_visitors_total 

print(signups_and_visitors_total)
```
