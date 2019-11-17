# 1. Reading multiple data files
## 1.1 Preparing data

```python
# Reading DataFrames from multiple files
import pandas as pd 

bronze = pd.read_csv('Bronze.csv')
silver = pd.read_csv('Silver.csv')
gold = pd.read_csv('Gold.csv')

print(gold.head())

# Reading DataFrames from multiple files in a loop
import pandas as pd
filenames = ['Gold.csv', 'Silver.csv', 'Bronze.csv']

## Create the list of three DataFrames: dataframes
dataframes = []
for f in filenames:
    dataframes.append(pd.read_csv(f))

print(dataframes[0].head())

# Combining DataFrames from multiple data files
import pandas as pd
medals = gold.copy() ## Make a copy of gold: medals

new_labels = ['NOC', 'Country', 'Gold'] ## Create list of new column labels: new_labels
medals.columns = new_labels ## Rename the columns of medals using new_labels

medals['Silver'] = silver['Total']
medals['Bronze'] = bronze['Total'] ## Add columns 'Silver' & 'Bronze' to medals

print(medals.head())
```

## 1.2 Reindexing DataFrames

```python
# Sorting DataFrame with the Index & columns
import pandas as pd
weather1 = pd.read_csv('monthly_max_temp.csv', index_col= 'Month') ## Read 'monthly_max_temp.csv' into a DataFrame: weather1
print(weather1.head())

weather2 = weather1.sort_index() ## Sort the index of weather1 in alphabetical order: weather2
print(weather2.head())

weather3 = weather1.sort_index(ascending=False) ## Sort the index of weather1 in reverse alphabetical order: weather3
print(weather3.head())

weather4 = weather1.sort_values('Max TemperatureF') ## Sort weather1 numerically using the values of 'Max TemperatureF': weather4
print(weather4.head())

```
> Q. index_col과 parse_date의 차이는?
> A. index_col : row index 열 정의, parse_dates : 인덱스 열이나 복수 열의 날짜를 가져올지 여부를 결정 

```python
# Reindexing DataFrame from a list
import pandas as pd

weather2 = weather1.reindex(year) ## Reindex weather1 using the list year: weather2
print(weather2)

weather3 = weather1.reindex(year).ffill() ## Reindex weather1 using the list year with forward-fill: weather3
## .ffill() method : 결측치가 있는 경우, 결측치 앞의 obs으로 결측치를 채움
print(weather3)

# Reindexing using another DataFrame Index
import pandas as pd
common_names = names_1981.reindex(names_1881.index) ## Reindex names_1981 with index of names_1881: common_names

print(common_names.shape)


common_names = common_names.dropna()
print(common_names.shape)
```

## 1.3 Arithmetic with Series & DataFrames
```python
temps_f = weather[['Min TemperatureF', 'Mean TemperatureF', 'Max TemperatureF']] ## Extract selected columns from weather as new DataFrame: temps_f

temps_c = (temps_f - 32) * 5/9 ## Convert temps_f to celsius: temps_c
temps_c.head()

temps_c.columns = temps_c.columns.str.replace('F', 'C') ## Rename 'F' in column names with 'C': temps_c.columns
print(temps_c.head())

# Computing percentage growth of GDP
import pandas as pd

gdp = pd.read_csv('GDP.csv', parse_dates=True, index_col='DATE') ## Read 'GDP.csv' into a DataFrame: gdp
post2008 = gdp.loc['2008': , : ] ## Slice all the gdp data from 2008 onward: post2008
print(post2008.tail(8))

yearly = post2008.resample('A').last() ## Resample post2008 by year, keeping last(): yearly
print(yearly)

yearly['growth'] = yearly.pct_change() * 100 ## Compute percentage growth of yearly: yearly['growth']
print(yearly)
```

> Q. resample('A')가 뭐였더라? 
> A. resample(rule = 'A') : Rule means the offset string or object representing target conversion. 이 때, 'A'는 annual, 그러니까 연 단위에서 resample 진행

```python
# Converting currency of stocks
import pandas as pd

sp500 = pd.read_csv('sp500.csv', parse_dates=True, index_col='Date')
exchange = pd.read_csv('exchange.csv', parse_dates=True, index_col='Date')

dollars = sp500[['Open', 'Close']]
print(dollars.head())

pounds = dollars.multiply(exchange['GBP/USD'], axis='rows') ## Convert dollars to pounds: pounds
print(pounds.head())
```

# 2.Concatenating data
## 2.1 Appending & concatenating Series

```python
# Appending pandas Series
import pandas as pd
jan = pd.read_csv('sales-jan-2015.csv', parse_dates=True, index_col='Date')
feb = pd.read_csv('sales-feb-2015.csv', parse_dates=True, index_col='Date')
mar = pd.read_csv('sales-mar-2015.csv', parse_dates=True, index_col='Date')

jan_units = jan['Units']
feb_units = feb['Units']
mar_units = mar['Units']

quarter1 = jan_units.append(feb_units).append(mar_units) ## Append feb_units and then mar_units to jan_units: quarter1
## Chaining .append()

print(quarter1.loc['jan 27, 2015':'feb 2, 2015'])
print(quarter1.loc['feb 26, 2015':'mar 7, 2015'])
print(quarter1.sum())

# Concatenating pandas Series along row axis
units = [] ## Initialize empty list: units

## Build the list of Series
for month in [jan, feb, mar]:
    units.append(month['Units'])

quarter1 = pd.concat(units) ## Concatenate the list: quarter1

print(quarter1.loc['jan 27, 2015':'feb 2, 2015'])
print(quarter1.loc['feb 26, 2015':'mar 7, 2015'])
```

## 2.2 Appending & concatenating DataFrames

```python
# Appending DataFrames with ignore_index
names_1881['year'] = 1881
names_1981['year'] = 1981 ## Add 'year' column to names_1881 and names_1981

combined_names = names_1881.append(names_1981, ignore_index = True) ## Append names_1981 after names_1881 with ignore_index=True: combined_names
## with ignore_index=True : 기존 index를 무시하고 append

print(names_1981.shape)
print(names_1881.shape)
print(combined_names.shape)

print(combined_names[combined_names.loc[:, 'name'] == 'Morgan']) ## Print all rows that contain the name 'Morgan'

# Concatenating pandas DataFrames along column axis
weather_list = [weather_max, weather_mean] ## Create a list of weather_max and weather_mean
weather = pd.concat(weather_list, axis=1) ## Concatenate weather_list horizontally, 옆으로 붙이기 

print(weather)

# Reading multiple files to build a DataFrame
medals =[] ##Initialize an empyy list: medals

for medal in medal_types:
    file_name = "%s_top5.csv" % medal ### Create the file name: file_name
    columns = ['Country', medal] ## Create list of column names: columns
    medal_df = pd.read_csv(file_name, header=0, index_col = 'Country', names = columns) ## Read file_name into a DataFrame: medal_df
    medals.append(medal_df) ## Append medal_df to medals

medals_df = pd.concat(medals, axis = 'columns') ## Concatenate medals horizontally: medals_df

print(medals_df)
```

## 2.3 Concatenation, keys, & MultiIndexes

```python
# Concatenating vertically to get MultiIndexed rows
for medal in medal_types:

    file_name = "%s_top5.csv" % medal
    
    medal_df = pd.read_csv(file_name, index_col = 'Country') ## Read file_name into a DataFrame: medal_df
   
    medals.append(medal_df) ## Append medal_df to medals
    ## medal_type에 따라 append는 했지만 medal type에 대한 index는 없는 상태.(나라만 index로 있음) 

medals = pd.concat(medals, keys = ['bronze', 'silver', 'gold']) ## Concatenate medals: medals
## multindex를 keys로 선언해서 각 구분을 ['bronze', 'silver', 'gold']로 정의함 
## multindex : medal_type, Country

print(medals)

# Slicing MultiIndexed DataFrames
medals_sorted = medals.sort_index(level = 0) ## Sort the entries of medals: medals_sorted

print(medals_sorted.loc[('bronze','Germany')])
print(medals_sorted.loc['silver'])

idx = pd.IndexSlice ## Create alias for pd.IndexSlice: idx

print(medals_sorted.loc[idx[:,'United Kingdom'], :]) ## Print all the data on medals won by the United Kingdom
```
> Q. sort_index(level)?  

> Q. idx = pd.InderSlice?


```python
# Concatenating horizontally to get MultiIndexed columns
february = pd.concat(dataframes, keys=['Hardware', 'Software', 'Service'], axis=1) ## Concatenate dataframes: february
print(february.info())

idx = pd.IndexSlice ## Assign pd.IndexSlice: idx

slice_2_8 = february.loc['Feb. 2, 2015':'Feb. 8, 2015', idx[:, 'Company']] ## Create the slice: slice_2_8

print(slice_2_8)

# Concatenating DataFrames from a dict
month_list = [('january', jan), ('february', feb), ('march', mar)] ## Make the list of tuples: month_list
month_dict = {} ## Create an empty dictionary: month_dict

for month_name, month_data in month_list:

    ## Group month_data: month_dict[month_name]
    month_dict[month_name] = month_data.groupby('Company').sum()

sales = pd.concat(month_dict) ## Concatenate data in month_dict: sales

print(sales)

idx = pd.IndexSlice
print(sales.loc[idx[:, 'Mediacore'], :])
```

## 2.4 Outer and inner join

```python
# Concatenating DataFrames with inner join
medal_list = [bronze, silver, gold] ## Create the list of DataFrames: medal_list
medals = pd.concat(medal_list, keys=['bronze', 'silver', 'gold'], axis=1, join='inner') ## Concatenate medal_list horizontally using an inner join: medals

print(medals)

# Resampling & concatenating DataFrames with inner join
china_annual = china.resample('A').last().pct_change(10).dropna() ## Resample and tidy china: china_annual
us_annual = us.resample('A').last().pct_change(10).dropna() ## Resample and tidy us: us_annual
## Chain .pct_change(10) as an aggregation method to compute the percentage change with an offset of ten years.
## Chain .dropna() to eliminate rows containing null values.

gdp = pd.concat([china_annual, us_annual], join = 'inner', axis = 1) ## Concatenate china_annual and us_annual: gdp

print(gdp.resample('10A').last())
```

# 3. Merging data
## 3.1 Merging DataFrames

```python
# Merging on a specific column
merge_by_city = pd.merge(revenue, managers, on = 'city') ## Merge revenue with managers on 'city': merge_by_city
print(merge_by_city)

merge_by_id = pd.merge(revenue, managers, on = 'branch_id') ## Merge revenue with managers on 'branch_id': merge_by_id
print(merge_by_id)

##pd.merge의 return default는 inner join이다. 

# Merging on columns with non-matching labels
combined = pd.merge(revenue, managers, left_on = 'city', right_on = 'branch') ## Merge revenue & managers on 'city' & 'branch': combined
## label이 중복되는 경우 merge 실행이 안되는데, left_on, right_on으로 label의 방향을 정해주면 해당 방향에 label에 맞는 df를 merge시킨다.

print(combined)

# Merging on multiple columns
revenue['state'] = ['TX','CO','IL','CA'] ## Add 'state' column to revenue: revenue['state']
managers['state'] = ['TX','CO','CA','MO'] ## Add 'state' column to managers: managers['state']

combined = pd.merge(revenue, managers, on = ['branch_id','city','state']) ## Merge revenue & managers on 'branch_id', 'city', & 'state': combined

print(combined)
```

## 3.2 Joining DataFrames
```python
revenue_and_sales = pd.merge(revenue, sales, how = 'right', on = ['city', 'state']) ## Merge revenue and sales: revenue_and_sales
print(revenue_and_sales)

sales_and_managers = pd.merge(sales, managers, how = 'left', left_on = ['city', 'state'], right_on = ['branch', 'state']) ## Merge sales and managers: sales_and_managers

print(sales_and_managers)

# Merging DataFrames with outer join
merge_default = pd.merge(sales_and_managers, revenue_and_sales) ## Perform the first merge: merge_default
print(merge_default)

merge_outer = pd.merge(sales_and_managers, revenue_and_sales, how = 'outer') ## Perform the second merge: merge_outer
print(merge_outer)

merge_outer_on = pd.merge(sales_and_managers, revenue_and_sales, how = 'outer', on = ['city','state']) ## Perform the third merge: merge_outer_on

print(merge_outer_on)
```

## 3.3 Ordered merges

```python
# Using merge_ordered()
tx_weather = pd.merge_ordered(austin, houston) ## Perform the first ordered merge: tx_weather
print(tx_weather)

tx_weather_suff = pd.merge_ordered(austin, houston, suffixes=['_aus','_hus'], on='date') ## Perform the second ordered merge: tx_weather_suff
print(tx_weather_suff)

tx_weather_ffill = pd.merge_ordered(austin, houston, suffixes=['_aus','_hus'], on='date', fill_method='ffill') ## Perform the third ordered merge: tx_weather_ffill
print(tx_weather_ffill)

# Using merge_asof()
merged = pd.merge_asof(auto, oil, left_on='yr', right_on='Date') ## Merge auto and oil: merged
print(merged.tail())

yearly = merged.resample('A', on= 'Date')[['mpg','Price']].mean() ## Resample merged: yearly
print(yearly)

print(yearly.corr()) ## Resample merged: yearly
```
> Q. merge_ordered()와 merge.asof()의 차이점? 
> A. A와 마찬가지로 B 함수도 on 열을 사용하여 값을 순서대로 병합하지만, 왼쪽 DataFrame의 각 행에 대해서는 'on' 열 값이 왼쪽 값보다 작은 오른쪽 DataFrame의 행만 유지된다.

# 4. Case Study - Summer Olympics


```#Import pandas
# Loading Olympic edition DataFrame
import pandas as pd
file_path = 'Summer Olympic medallists 1896 to 2008 - EDITIONS.tsv'
editions = pd.read_csv(file_path, sep='\t')

editions = editions[['Edition', 'Grand Total', 'City', 'Country']]
print(editions)python

import pandas as pd
file_path = 'Summer Olympic medallists 1896 to 2008 - IOC COUNTRY CODES.csv'
ioc_codes = pd.read_csv(file_path)

ioc_codes = ioc_codes[['Country', 'NOC']]
print(ioc_codes.head())
print(ioc_codes.tail())
```
```python
# Building medals DataFrame
import pandas as pd

## Create empty dictionary: medals_dict
medals_dict = {}

for year in editions['Edition']:

    ## Create the file path: file_path
    file_path = 'summer_{:d}.csv'.format(year)
    
    ## Load file_path into a DataFrame: medals_dict[year]
    medals_dict[year] = pd.read_csv(file_path)
    
    ## Extract relevant columns: medals_dict[year]
    medals_dict[year] =  medals_dict[year][['Athlete', 'NOC', 'Medal']]
    
    ## Assign year to column 'Edition' of medals_dict
    medals_dict[year]['Edition'] = year
    
medals = pd.concat(medals_dict, ignore_index = True) ## Concatenate medals_dict: medals

print(medals.head())
print(medals.tail())
```

> Q. 위의 for loop가 어떤 식으로 굴러가는지 잘 모르겠네
> A.

```python
# Counting medals by country/edition in a pivot table
medal_counts = medals.pivot_table(index = 'Edition', values = 'Athlete', columns = 'NOC', aggfunc = 'count') ## Construct the pivot_table: medal_counts

print(medal_counts.head())
print(medal_counts.tail())

# Computing fraction of medals per Olympic edition
totals = editions.set_index('Edition') ## Set Index of editions: totals
totals = totals['Grand Total'] ## Reassign totals['Grand Total']: totals

fractions = medal_counts.divide(totals, axis = 'rows') ## Divide medal_counts by totals: fractions

print(fractions.head())
print(fractions.tail())
```
```python
# Computing percentage change in fraction of medals won
mean_fractions = fractions.expanding().mean() ## Apply the expanding mean: mean_fractions
fractions_change = mean_fractions.pct_change() * 100 ## Compute the percentage change: fractions_change

fractions_change = fractions_change.reset_index('Edition') ## Reset the index of fractions_change: fractions_change

print(fractions_change.head())
print(fractions_change.tail())
```
> Q. .expanding()?
> A. 

```python
# Building hosts DataFrame
import pandas as pd

hosts = pd.merge(editions, ioc_codes, how = 'left') ## Left join editions and ioc_codes: hosts
hosts = hosts[['Edition','NOC']].set_index('Edition') ## Extract relevant columns and set index: hosts

## Fix missing 'NOC' values of hosts
print(hosts.loc[hosts.NOC.isnull()])
hosts.loc[1972, 'NOC'] = 'FRG'
hosts.loc[1980, 'NOC'] = 'URS'
hosts.loc[1988, 'NOC'] = 'KOR'

hosts = hosts.reset_index() ## Reset Index of hosts: hosts

print(hosts)

# Reshaping for analysis
import pandas as pd

reshaped = pd.melt(fractions_change, id_vars = 'Edition', value_name = 'Change') ## Reshape fractions_change: reshaped
print(reshaped.shape, fractions_change.shape) ## Print reshaped.shape and fractions_change.shape

chn = reshaped.loc[reshaped['NOC'] == 'CHN'] ## Extract rows from reshaped where 'NOC' == 'CHN': chn

print(chn.tail())

# Merging to compute influence
import pandas as pd

merged = pd.merge(reshaped, hosts, how='inner') ## Merge reshaped and hosts: merged
print(merged.head())

influence = merged.set_index('Edition').sort_index() ## Set Index of merged and sort it: influence
print(influence.head())

# Plotting influence of host country
import matplotlib.pyplot as plt

change = influence['Change'] ## Extract influence['Change']: change
ax = change.plot(kind = 'bar') ## Make bar plot of change: ax

## Customize the plot to improve readability
ax.set_ylabel("% Change of Host Country Medal Count")
ax.set_title("Is there a Host Country Advantage?")
ax.set_xticklabels(editions['City'])

plt.show()
```
