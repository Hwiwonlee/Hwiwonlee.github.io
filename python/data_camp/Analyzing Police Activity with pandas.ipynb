# 1. Preparing the data for analysis
## 1.1 Stanford Open Policing Project dataset and data preprocessing

```python
# Examining the dataset
import pandas as pd
ri = pd.read_csv('police.csv')
print(ri.head())
print(ri.isnull().sum())

# Dropping columns
print(ri.shape)

ri.drop(['county_name', 'state'], axis='columns', inplace=True) ## Drop the 'county_name' and 'state' columns
## 'county_name' : 모든 obs가 NaN
## 'state' : 모든 obs가 같은 값

print(ri.shape)

# Dropping rows
print(ri.isnull().sum())

ri.dropna(subset=['driver_gender'], inplace=True) ## Drop all rows that are missing 'driver_gender'

print(ri.isnull().sum())
print(ri.shape)
```
- .dropna() : na를 drop
- .drop() : na에 관계 없이 drop 
  - axis : '축'을 정의; inplace : 기존의 df를 drop한 상태의 df로 대체할 것인가? 


## 1.2 Using proper data types

```python
# Fixing a data type
print(ri.is_arrested.head()) ## Examine the head of the 'is_arrested' column : object
ri['is_arrested'] = ri.is_arrested.astype('bool') ## Change the data type of 'is_arrested' to 'bool'

print(ri.is_arrested.dtype)
```

## 1.3 Creating a DatetimeIndex

```python
# Combining object columns
print(ri.head()) ## stop_date : Y-M-D; stop_time : H:M
combined = ri.stop_date.str.cat(ri.stop_time, sep = ' ') ## Concatenate 'stop_date' and 'stop_time' (separated by a space)

ri['stop_datetime'] = pd.to_datetime(combined) ## Convert 'combined' to datetime format
print(ri.dtypes)
```

> To do. df를 overview할 수 있는 method나 attribute가 많은 것 같다. 나중에 정리해보자. 

```python
# Setting the index
ri.set_index('stop_datetime', inplace=True) ## Set 'stop_datetime' as the index
print(ri.index) ## Examine the index
print(ri.columns) ## Examine the columns
```

# 2. Exploring the relationship between gender and policing
## 2.1 Do the genders commit different violations?

```python
# Examining traffic violations
print(ri.violation.value_counts()) ## Count the unique values in 'violation'
## .value_counts() : Series를 대상으로 unique한 value의 개수 합을 return

print(ri.violation.value_counts(normalize=True)) ## Express the counts as proportions
## .value_counts(nomalize = T) : proportions으로 return

# Comparing violations by gender
female = ri[ri['driver_gender'] == 'F'] ## Create a DataFrame of female drivers 
male = ri[ri['driver_gender'] == 'M'] ## Create a DataFrame of male drivers

print(female.violation.value_counts(normalize = True)) ## Compute the violations by female drivers (as proportions)
print(male.violation.value_counts(normalize = True)) ## Compute the violations by male drivers (as proportions)
```

## 2.2 Does gender affect who gets a ticket for speeding?

```python
# Comparing speeding outcomes by gender
female_and_speeding = ri[(ri.driver_gender == "F") & (ri.violation_raw == "Speeding")] ## Create a DataFrame of female drivers stopped for speeding
male_and_speeding = ri[(ri.driver_gender == "M") & (ri.violation_raw == "Speeding")] ## Create a DataFrame of male drivers stopped for speeding

print(female_and_speeding.stop_outcome.value_counts(normalize = True)) ## Compute the stop outcomes for female drivers (as proportions)
print(male_and_speeding.stop_outcome.value_counts(normalize = True)) ## Compute the stop outcomes for male drivers (as proportions)
```

## 2.3 Does gender affect whose vehicle is searched?
```python
# Calculating the search rate
print(ri.search_conducted.dtype) ## Check the data type of 'search_conducted'
print(ri.search_conducted.value_counts(normalize=True)) ## Calculate the search rate by counting the values
print(ri.search_conducted.mean()) ## Calculate the search rate by taking the mean

# Comparing search rates by gender
print(ri[ri.driver_gender == 'F'].search_conducted.mean())
print(ri[ri.driver_gender == 'M'].search_conducted.mean())

print(ri.groupby('driver_gender').search_conducted.mean()) ## 위의 결과를 한 줄로 얻을 수 있음

# Adding a second factor to the analysis
print(ri.groupby(['driver_gender', 'violation']).search_conducted.mean()) ## Calculate the search rate for each combination of gender and violation
print(ri.groupby(['violation', 'driver_gender']).search_conducted.mean()) ## Reverse the ordering to group by violation before gender
```
> Q. column의 순서를 바꾸는 것이 아니라 저 안에서 order를 바꿀 수는 없을까?  <br> A. 

## 2.4 Does gender affect who is frisked during a search?

```python
# Counting protective frisks
print(ri.search_type.value_counts()) ## Count the 'search_type' values
ri['frisk'] = ri.search_type.str.contains('Protective Frisk', na=False) ## Check if 'search_type' contains the string 'Protective Frisk'

print(ri['frisk'].dtype) ## Check the data type of 'frisk'
print(ri['frisk'].sum()) ## Take the sum of 'frisk'

# Comparing frisk rates by gender
searched = ri[ri['search_conducted'] == True] ## Create a DataFrame of stops in which a search was conducted
print(searched.frisk.mean()) ## Calculate the overall frisk rate by taking the mean of 'frisk'
print(searched.groupby('driver_gender').frisk.mean()) ## Calculate the frisk rate for each gender
```

# 3. Visual exploratory data analysis
## 3.1 Does time of day affect arrest rate?

```python
# Calculating the hourly arrest rate
print(ri.is_arrested.mean()) ## Calculate the overall arrest rate
print(ri.groupby(ri.index.hour).is_arrested.mean()) ## Calculate the hourly arrest rate
## ri.index.hour로 groupby를 실행, date object가 ri의 index이기 때문에 가능 

hourly_arrest_rate = ri.groupby(ri.index.hour).is_arrested.mean()

# Plotting the hourly arrest rate
import matplotlib.pyplot as plt
hourly_arrest_rate.plot() ## Create a line plot of 'hourly_arrest_rate'

plt.xlabel('Hour')
plt.ylabel('Arrest Rate')
plt.title('Arrest Rate by Time of Day')

plt.show()
```

## 3.2 Are drug-related stops on the rise?

```python
# Plotting drug-related stops
print(ri.drugs_related_stop.resample('A').mean()) ## Calculate the annual rate of drug-related stops
## .resample('A') : 연 단위로 obs를 묶음 
annual_drug_rate = ri.drugs_related_stop.resample('A').mean()

annual_drug_rate.plot()
plt.show()

# Comparing drug and search rates
annual_search_rate = ri.search_conducted.resample('A').mean() ## Calculate and save the annual search rate
annual = pd.concat([annual_drug_rate, annual_search_rate], axis='columns') ## Concatenate 'annual_drug_rate' and 'annual_search_rate'

annual.plot(subplots=True)
plt.show()
```

## 3.3 What violations are caught in each district?

```python
# Tallying violations by district
print(pd.crosstab(ri.district, ri.violation)) ## Create a frequency table of districts and violations
all_zones = pd.crosstab(ri.district, ri.violation) 

print(all_zones.loc['Zone K1':'Zone K3', :]) ## Select rows 'Zone K1' through 'Zone K3'
k_zones = all_zones.loc['Zone K1':'Zone K3', :]

# Plotting violations by district
k_zones.plot(kind = 'bar') ## Create a bar plot of 'k_zones'

plt.show()
plt.clf

k_zones.plot(kind = 'bar', stacked = True) ## Create a stacked bar plot of 'k_zones'

plt.show()
```

## 3.4 How long might you be stopped for a violation?

```python
# Converting stop durations to numbers
print(ri.stop_duration.unique()) ## Print the unique values in 'stop_duration'

mapping = {'0-15 Min' : 8, '16-30 Min': 23, '30+ Min': 45} ## Create a dictionary that maps strings to integers

ri['stop_minutes'] = ri.stop_duration.map(mapping) ## Convert the 'stop_duration' strings to integers using the 'mapping'
## dict과 map을 이용한 값 변환

print(ri.stop_minutes.unique()) ## Print the unique values in 'stop_minutes'

# Plotting stop length
print(ri.groupby('violation_raw').stop_minutes.mean()) ## Calculate the mean 'stop_minutes' for each value in 'violation_raw'
stop_length = ri.groupby('violation_raw').stop_minutes.mean() 

stop_length.sort_values().plot(kind = 'barh') ## Sort 'stop_length' by its values and create a horizontal bar plot
plt.show()
```

# 4. Analyzing the effect of weather on policing
## 4.1 Exploring the weather dataset

```python
# Plotting the temperature
weather = pd.read_csv('weather.csv')

print(weather[['TMIN', 'TAVG', 'TMAX']].describe()) ## Describe the temperature columns
weather[['TMIN', 'TAVG', 'TMAX']].plot(kind='box') ## Create a box plot of the temperature columns

plt.show()

# Plotting the temperature difference
weather['TDIFF'] = weather.TMAX - weather.TMIN ## Create a 'TDIFF' column that represents temperature difference

print(weather.TDIFF.describe()) ## Describe the 'TDIFF' column

weather.TDIFF.plot(kind = 'hist', bins = 20) ## Create a histogram with 20 bins to visualize 'TDIFF'
plt.show()
```

## 4.2 Categorizing the weather

```python
# Counting bad weather conditions
WT = weather.loc[:,'WT01':'WT22'] ## Copy 'WT01' through 'WT22' to a new DataFrame
weather['bad_conditions'] = WT.sum(axis = 'columns') ## Calculate the sum of each row in 'WT'

weather['bad_conditions'] = weather.bad_conditions.fillna(0).astype('int') ## Replace missing values in 'bad_conditions' with '0'

weather['bad_conditions'].plot(kind = 'hist') ## Create a histogram to visualize 'bad_conditions' 
plt.show() ## Display the plot

# Rating the weather conditions
print(weather.bad_conditions.value_counts().sort_index()) ## Count the unique values in 'bad_conditions' and sort the index

mapping = {0:'good', 1:'bad', 2:'bad', 3:'bad', 4:'bad', 5:'worse', 6:'worse', 7:'worse', 8:'worse', 9:'worse'} ## Create a dictionary that maps integers to strings
weather['rating'] = weather.bad_conditions.map(mapping) ## Convert the 'bad_conditions' integers to strings using the 'mapping'

print(weather['rating'].value_counts())


# Changing the data type to category
cats = ['good', 'bad', 'worse']

weather['rating'] = weather.rating.astype('category', ordered=True, categories = cats) ## Change the data type of 'rating' to category
print(weather['rating'].head())
```

> To do. .astype()이 유용한 것 같다. astype()에 대해 정리해보자. 

## 4.3 Merging datasets

```python
# Preparing the DataFrames
ri.reset_index(inplace = True) ## Reset the index of 'ri'
print(ri.head())

weather_rating = weather[['DATE', 'rating']] ## Create a DataFrame from the 'DATE' and 'rating' columns
print(weather_rating.head())

# Merging the DataFrames
print(ri.shape)

ri_weather = pd.merge(left=ri, right=weather_rating, left_on='stop_date', right_on='DATE', how='left') ## Merge 'ri' and 'weather_rating' using a left join

print(ri_weather.shape)
ri_weather.set_index('stop_datetime', inplace=True) ## Set 'stop_datetime' as the index of 'ri_weather'
```

## 4.4 Does weather affect the arrest rate?

```python
# Comparing arrest rates by weather rating
print(ri_weather.is_arrested.mean())
print(ri_weather.groupby('rating').is_arrested.mean()) ## Calculate the arrest rate for each 'rating'
print(ri_weather.groupby(['violation', 'rating']).is_arrested.mean()) ## Calculate the arrest rate for each 'violation' and 'rating'

# Selecting from a multi-indexed Series
arrest_rate = ri_weather.groupby(['violation', 'rating']).is_arrested.mean()
print(arrest_rate)

print(arrest_rate.loc['Moving violation', 'bad']) ## Print the arrest rate for moving violations in bad weather
print(arrest_rate.loc['Speeding']) ## Print the arrest rates for speeding violations in all three weather conditions

# Reshaping the arrest rate data
print(arrest_rate.unstack()) ## Unstack the 'arrest_rate' Series into a DataFrame

print(ri_weather.pivot_table(index='violation', columns='rating', values='is_arrested')) ## Create the same DataFrame using a pivot table
```
