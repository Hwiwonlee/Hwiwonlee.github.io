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
> Q. 왜 I과 II의 차이가 생기는 걸까?  답이 바로 뒤에 나오네.

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

# 4. Grouping data
## 4.1 Categoricals and groupby

```python
# Grouping by multiple columns
by_class = titanic.groupby('pclass') ## Group titanic by 'pclass'
count_by_class = by_class['survived'].count() ## Aggregate 'survived' column of by_class by count
print(count_by_class)


by_mult = titanic.groupby(['embarked', 'pclass']) ## Group titanic by 'embarked' and 'pclass'
count_mult = by_mult['survived'].count() ## Aggregate 'survived' column of by_mult by count
print(count_mult)
```

```python
# Grouping by another series
life = pd.read_csv(life_fname, index_col='Country') ## Read life_fname into a DataFrame: life
regions = pd.read_csv(regions_fname, index_col='Country') ## Read regions_fname into a DataFrame: regions

life_by_region = life.groupby((regions['region'])) ## Group life by regions['region']: life_by_region

print(life_by_region['2010'].mean())
```
> Q. 이게 어떻게 groupby가 되는거지?
> A. 같은 index를 갖고 있었구나. 

## 4.2 Groupby and aggregation

```python
# Computing multiple aggregates of multiple columns
by_class = titanic.groupby('pclass') ## Group titanic by 'pclass': by_class
by_class_sub = by_class[['age','fare']] ## Select 'age' and 'fare'

aggregated = by_class_sub.agg(['max', 'median']) ## Aggregate by_class_sub by 'max' and 'median': aggregated
## by_class[['age','fare']]의 결과로 얻은 pclass x age, fare를 obs의 max와 median 담은 df로 aggregation

print(aggregated.loc[:, ('age','max')])
print(aggregated.loc[:, ('fare','median')])

# Aggregating on index levels/fields
gapminder = pd.read_csv('gapminder.csv', index_col = ['Year','region','Country']).sort_index()
gapminder.head() ## multindex

by_year_region = gapminder.groupby(level = ['Year', 'region']) ## Group gapminder by 'Year' and 'region': by_year_region
## multindex 상황에서 index level을 arg로 주고 groupby를 실행함.

## Define the function to compute spread: spread
def spread(series):
    return series.max() - series.min()
aggregator = {'population':'sum', 'child_mortality':'mean', 'gdp':spread} ## Create the dictionary: aggregator

aggregated = by_year_region.agg(aggregator) ## Aggregate by_year_region using the dictionary: aggregated
## function과 dict을 agg의 arg로 선언할 수도 있다. 

print(aggregated.tail(6))

# Grouping on a function of the index
sales = pd.read_csv('sales.csv', index_col = 'Date', parse_dates = True)
by_day = sales.groupby(sales.index.strftime('%a')) ## Create a groupby object: by_day


units_sum = by_day['Units'].sum()
print(units_sum)
```
.strftime('%a')에 대한 [정보](https://datascienceschool.net/view-notebook/465066ac92ef4da3b0aba32f76d9750a/)는 해당 링크에서 찾았다. .strftime(format)은 날짜와 시간 정보를 문자열로 바꿔주는 method로 위에 선언된 '%a'는 영어로된 요일 문자열로 바꾸라는 의미다.

## 4.3 Groupby and transformation

```python
# Detecting outliers with Z-Scores
from scipy.stats import zscore ## Import zscore

standardized = gapminder_2010.groupby('region')['life','fertility'].transform(zscore) ## Group gapminder_2010: standardized
## DF를 'region'으로 groupby하고 ['life','fertility'] column을 뽑아 해당 값들을 zscore로 바꾼 DF를 standardized에 저장 

outliers = (standardized['life'] < -3) | (standardized['fertility'] > 3) ## Construct a Boolean Series to identify outliers: outliers
## 이상치 판별기 

gm_outliers = gapminder_2010.loc[outliers] ## Filter gapminder_2010 by the outliers: gm_outliers
## 이상치 판별기를 이용해 gapminder_2010에서 이상치를 제외시켰다. 

print(gm_outliers)

# Filling missing data (imputation) by group
by_sex_class = titanic.groupby(['sex','pclass']) ## Create a groupby object: by_sex_class

## Write a function that imputes median
def impute_median(series):
    return series.fillna(series.median())

titanic.age = by_sex_class.age.transform(impute_median) ## Impute age and assign to titanic['age']
## 위에서 만든 impute_median 함수를 이용해 age column을 대상으로 transform을 시행함. 

print(titanic.tail(10))

# Other transformations with .apply
regional = gapminder_2010.groupby('region') ## Group gapminder_2010 by 'region': regional
reg_disp = regional.apply(disparity) ## Apply the disparity function on regional: reg_disp
## 미리 정의해둔 disparity함수를 이용함. 

print(reg_disp.loc[['United States','United Kingdom','China'], :]) ## Print the disparity of 'United States', 'United Kingdom', and 'China'
````

## 4.4 Groupby and filtering

```python
# Grouping and filtering with .apply()
by_sex = titanic.groupby('sex') ## Create a groupby object using titanic over the 'sex' column: by_sex

## c_deck_survival
def c_deck_survival(gr):

    c_passengers = gr['cabin'].str.startswith('C').fillna(False)

    return gr.loc[c_passengers, 'survived'].mean()

c_surv_by_sex = by_sex.apply(c_deck_survival) ## Call by_sex.apply with the function c_deck_survival

print(c_surv_by_sex)

# Grouping and filtering with .filter()
sales = pd.read_csv('sales.csv', index_col='Date', parse_dates=True) ## Read the CSV file into a DataFrame: sales
by_company = sales.groupby('Company') ## Group sales by 'Company': by_company

by_com_sum = by_company.Units.sum() ## Compute the sum of the 'Units' of by_company: by_com_sum
print(by_com_sum)

by_com_filt = by_company.filter(lambda g : g['Units'].sum() > 35) ## Filter 'Units' where the sum is > 35: by_com_filt
print(by_com_filt)

# Filtering and grouping with .map()
under10 = (titanic['age'] < 10).map({True:'under 10', False:'over 10'}) ## Create the Boolean Series: under10
## 타이타닉 승선객의 나이 10살을 기준으로 10살 미만이면 under 10, 10살 이상이면 over 10으로 'age'를 변경 

survived_mean_1 = titanic.groupby(under10)['survived'].mean() ## Group by under10 and compute the survival rate
## titanic과 under10이 같은 index를 가지므로 under10에 의해 groupby 시행 가능. 
print(survived_mean_1)

survived_mean_2 = titanic.groupby([under10, 'pclass'])['survived'].mean() ## Group by under10 and pclass and compute the survival rate
print(survived_mean_2)
```

# 5. Bring it all together

```python
# Using .pivot_table() to count medals by type
counted = medals.pivot_table(index = 'NOC', values = 'Athlete', columns = 'Medal', aggfunc = 'count') ## Construct the pivot table: counted 

counted['totals'] = counted.sum(axis='columns') ## Create the new column: counted['totals']
counted = counted.sort_values('totals', ascending=False) ## Sort counted by the 'totals' column

print(counted.head(15))
```
> counted의 totals column은 counted에서 열 방향으로 sum을 시행하는 것이므로 axis='columns'를 붙여준다. (x)  
> 찾아보니 default가 columns이다. interger로 arg를 써도 되는데 0 : col, 1 : row다.   
> 아무리 생각해도 이상해서 (왜냐면 orginal dataset의 columns은 ['bronze', 'silver', 'gold', 'total']이었다) 실행해서 살펴보니 axis='columns'으로 실행하면 row 기준으로 덧셈이 된다. 그러니까 axis='columns' = 1, axis='rows' = 0과 같다. 왜 이렇지? 

```python
# Applying .drop_duplicates()
ev_gen = medals[['Event_gender', 'Gender']] ## Select columns: ev_gen
ev_gen_uniques = ev_gen.drop_duplicates() ## Drop duplicate pairs: ev_gen_uniques, 중복값을 모두 drop해버리는 method 

print(ev_gen_uniques)

# Finding possible errors with .groupby()
medals_by_gender = medals.groupby(['Event_gender', 'Gender']) ## Group medals by the two columns: medals_by_gender
medal_count_by_gender = medals_by_gender.count() ## Create a DataFrame with a group count: medal_count_by_gender

print(medal_count_by_gender)
```
```python
# Locating suspicious data
sus = (medals.Event_gender == 'W') & (medals.Gender == 'Men') ## Create the Boolean Series: sus
suspect = medals[sus]  ## Create a DataFrame with the suspicious row: suspect

print(suspect)
```
> Boolean Series를 만들 때 조건문에 ()를 쳐춰야 한다. 위의 경우 and로 연결되어 있지만 각 조건문마다 ()를 쳐줘야 실행된다. 

```python
# Using .nunique() to rank by distinct sports
country_grouped = medals.groupby('NOC') ## Group medals by 'NOC': country_grouped
Nsports = country_grouped.Sport.nunique() ## Compute the number of distinct sports in which each country won medals: Nsports
## .nunique() method는 categorical.nunique()로 쓰이며 유일한 categorical의 개수를 센다. 


Nsports = Nsports.sort_values(ascending=False) ## Sort the values of Nsports in descending order

print(Nsports.head(15))

# Counting USA vs. USSR Cold War Olympic Sports
during_cold_war = (medals['Edition'] >= 1952) & (medals['Edition'] <= 1988) ## Create a Boolean Series that is True when 'Edition' is between 1952 and 1988: during_cold_war

is_usa_urs = medals.NOC.isin(['USA','URS']) ## Extract rows for which 'NOC' is either 'USA' or 'URS': is_usa_urs
## list 안에 같이 쓰면 default로 'or' 조건문이 실행된다. 

cold_war_medals = medals.loc[during_cold_war & is_usa_urs] ## Use during_cold_war and is_usa_urs to create the DataFrame: cold_war_medals
 
country_grouped = cold_war_medals.groupby('NOC')

Nsports = country_grouped.Sport.nunique().sort_values(ascending=False) ## Create Nsports

print(Nsports)

# Counting USA vs. USSR Cold War Olympic Medals
medals_won_by_country = medals.pivot_table(index = 'Edition', columns = 'NOC', values = 'Athlete', aggfunc = 'count') ## Create the pivot table: medals_won_by_country

cold_war_usa_urs_medals = medals_won_by_country.loc[1952:1988, ['USA','URS']] ## Slice medals_won_by_country: cold_war_usa_urs_medals

most_medals = cold_war_usa_urs_medals.idxmax(axis = 'columns') ## Create most_medals 
## .idxmax(axis) : 선언된 axis에 따라 기준을 잡고 기준에서의 최대값을 return한다. 
## axis = 'rows'(=0)이면 '열'을 기준으로 각 열이 갖는 최대값이 속한 index를 return한다. 
## axis = 'columns'(=1)이면 '행'을 기준으로 각 행이 갖는 최대값이 속한 열을 reutrn한다. 


print(most_medals.value_counts())


# Visualizing USA Medal Counts by Edition: Line Plot
## Create the DataFrame: usa
usa = medals[medals['NOC'] == 'USA']

usa_medals_by_year = usa.groupby(['Edition', 'Medal'])['Athlete'].count() ## Group usa by ['Edition', 'Medal'] and aggregate over 'Athlete'
usa_medals_by_year = usa_medals_by_year.unstack(level = 'Medal') ## Reshape usa_medals_by_year by unstacking
## unstack을 해주는 이유? 위에 groupby에서 ['Edition', 'Medal']로 multindex가 돼서 x, y축이 없어졌고 이 때문에 plot을 그릴 수가 없음
## 따라서 .unstack(level = 'Medal')를 실행, index로 'Edition'을 갖고 columns으로 'Medal'을 갖는 DF로 reshaping 해줌. 

usa_medals_by_year.plot() ## Plot the DataFrame usa_medals_by_year
plt.show()
plt.clf()

usa_medals_by_year.plot.area() ## Create an area plot of usa_medals_by_year
plt.show()
plt.clf()

# Visualizing USA Medal Counts by Edition: Area Plot with Ordered Medals

medals.Medal = pd.Categorical(values = medals.Medal, categories=['Bronze', 'Silver', 'Gold'], ordered=True) ## Redefine 'Medal' as an ordered categorical
medals.info() ## Medal : category 확인 

usa = medals[medals.NOC == 'USA']
usa_medals_by_year = usa.groupby(['Edition', 'Medal'])['Athlete'].count()
usa_medals_by_year = usa_medals_by_year.unstack(level='Medal')
usa_medals_by_year.plot.area()
plt.show()

```
