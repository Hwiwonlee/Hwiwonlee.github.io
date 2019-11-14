# 1. Data ingestion & inspection

## 1.1 Review of pandas DataFrames
Pandas는 빠른 numeric array 계산을 위해 NumPy를 기반으로 상호작용한다.
```python
# NumPy and pandas working together
## World Development Indicators의 dataset을 사용
import numpy as np

np_vals = df.values ## Create array of DataFrame values: np_vals 

np_vals_log10 = np.log10(np_vals) ## Create new array of base 10 logarithm values: np_vals_log10
df_log10 = np.log10(df) ## Create array of new DataFrame by passing df to np.log10(): df_log10

[print(x, 'has type', type(eval(x))) for x in ['np_vals', 'np_vals_log10', 'df', 'df_log10']] ## Print original and new data containers
```
## 1.2 Building DataFrames from scratch

```python
# Zip lists to build a DataFrame
zipped = list(zip(list_keys, list_values)) ## Zip the 2 lists together into one list of (key,value) tuples: zipped
print(zipped) ## Inspect the list using print()

data = dict(zipped) ## Build a dictionary with the zipped list: data
df = pd.DataFrame(data) ## Build and inspect a DataFrame from the dictionary: df
print(df)

# Labeling your data
list_labels = ['year', 'artist', 'song', 'chart weeks']
df.columns = list_labels ## Assign the list of labels to the columns attribute: df.columns

# Building DataFrames with broadcasting
state = 'PA'
data = {'state':state, 'city':cities} ## Already set in cities list 
df = pd.DataFrame(data) ## Construct a DataFrame from dictionary data: df

print(df)
```

## 1.3 Importing & exporting data
[pd.read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)의 기본적인 document

```python
# Reading a flat file
df1 = pd.read_csv(data_file)

new_labels = ['year', 'population'] ## Create a list of the new column labels: new_labels
df2 = pd.read_csv(data_file, header=0, names=new_labels) ## Read in the file, specifying the header and names parameters: df2
## header = 0 : file의 column name을 그대로 사용, 사실 names랑 같이 쓸 필요가 없다.
## header = 1,2,3,4... : file의 nth row를 columns name으로 사용, n-1개의 row는 사라진다. 
## header = None : file의 column name을 zero-indexing으로 바꿔준다. 
print(df1)
print(df2)

# Delimiters, headers, and extensions
## Yahoo finance의 file을 이용함. 
df1 = pd.read_csv(file_messy)
print(df1.head()) 

df2 = pd.read_csv(file_messy, delimiter=' ', header=3, comment='#') ## Read in the file with the correct parameters: df2
## comment = '#' : file에 포함된 '#'절을 comment로 처리, 읽어오지 않도록 한다. 

print(df2.head())

df2.to_csv(file_clean, index=False) ## Save the cleaned up DataFrame to a CSV file without the index
df2.to_excel('file_clean.xlsx', index=False) ## Save the cleaned up DataFrame to an excel file without the index
```

## 1.4 Plotting with pandas

```python
# Plotting series using pandas 
df.plot(color = 'red') ## Create a plot with color='red'

plt.title('Temperature in Austin')
plt.xlabel('Hours since midnight August 1, 2010')
plt.ylabel('Temperature (degrees F)')

plt.show()

# Plotting DataFrames
df.plot()
plt.show() ## Plot all columns (default), 3개의 line plot이 scale 차이가 있어서 명확히 보이지 않음.

df.plot(subplots = True)
plt.show() ## Plot all columns as subplots, 3개의 line plot을 따로 그려내기 

column_list1 = ['Dew Point (deg F)']
df[column_list1].plot()
plt.show() ## Plot just the Dew Point data, colums_list1에 대한 line plot

column_list2 = ['Temperature (deg F)','Dew Point (deg F)']
df[column_list2].plot()
plt.show() ## Plot the Dew Point and Temperature data, but not the Pressure data, column_list2에 대한 line plot
```
# 2. Exploratory data analysis
## 2.1 Visual exploratory data analysis
```python
# pandas line plots
## Yahoo Finance data
y_columns = ['AAPL', 'IBM']
df.plot(x='Month', y=y_columns) ## Generate a line plot

plt.title('Monthly stock prices')
plt.ylabel('Price ($US)')$

plt.show()

# pandas scatter plots
## Auto MPG Data Set in UCI ML repository
df.plot(kind='scatter', x='hp', y='mpg', s=sizes) ## Generate a scatter plot

plt.title('Fuel efficiency vs Horse-power')
plt.xlabel('Horse-power')
plt.ylabel('Fuel efficiency (mpg)')

plt.show()

# pandas box plots
cols = ['weight','mpg']
df[cols].plot(kind = 'box', subplots = True)
plt.show()
           
# pandas hist, pdf and cdf
## tips dataset in Seaborn package 

fig, axes = plt.subplots(nrows=2, ncols=1) ## This formats the plots such that they appear on separate rows

df.fraction.plot(ax=axes[0], kind='hist', normed=True, bins=30, range=(0,.3)) ## Plot the PDF
plt.show()

df.fraction.plot(ax=axes[1], kind='hist', normed=True, bins=30, cumulative=True, range=(0,.3)) ## Plot the CDF
plt.show()
## ax=axes[int] : int row에 해당 plot을 그림, 위의 경우 .subplots() method에서 2x1 format을 선언했으므로 각각 1st, 2nd row에 그려진다 
```

## 2.2 Statistical exploratory data analysis

```python
# Bachelor's degrees awarded to women
## Using Bachelor's degrees awarded to women dataset
print(df.Engineering.min())
print(df.Engineering.max())

mean = df.mean(axis='columns') ## Construct the mean percentage per year: mean

mean.plot()
plt.show()

# Median vs mean
## Titanic dataset
print(df['fare'].describe()) ## Print summary statistics of the fare column with .describe()

df.fare.plot(kind = 'box')
plt.show()

# Quantile
## Gapminer dataset
print(df['2015'].count()) ## Print the number of countries reported in 2015
print(df.quantile([0.05, 0.95])) ## Print the 5th and 95th percentiles

years = ['1800','1850','1900','1950','2000']
df[years].plot(kind='box')
plt.show()

# Standard deviation of temperature
## Weather Undergroun dataset

print(january.mean(), march.mean()) ## Print the mean of the January and March data
print(january.std(), march.std()) ## Print the standard deviation of the January and March data

```

## 2.3 Separating populations

```python
# Separate and summarize
global_mean = df.mean()
global_std = df.std()

us = df[df['origin'] == 'US'] ## Filter the US population from the origin column: us

us_mean = us.mean()
us_std = us.std()

print(us_mean - global_mean)
print(us_std - global_std)

# Separate and plot
fig, axes = plt.subplots(nrows=3, ncols=1) ## Display the box plots on 3 separate rows and 1 column

titanic.loc[titanic['pclass'] == 1].plot(ax=axes[0], y='fare', kind='box')
titanic.loc[titanic['pclass'] == 2].plot(ax=axes[1], y='fare', kind='box')
titanic.loc[titanic['pclass'] == 3].plot(ax=axes[2], y='fare', kind='box') 
## Generate a box plot of the fare prices for the 1st, 2nd, 3nd passenger class

plt.show()

```
# 3. Time series in pandas
## 3.1 Indexing time series
Dataset에 '시간'이 기록되어 있는 것은 흔히 볼 수 있다. 시간을 하나의 변수로 보고 model에 포함시킬 수도 있지만 시간을 index로 정의해 data를 분류할 수도 있다. 이번엔 시간을 index로 놓고 data frame을 분석하는 방법에 대해 알아보자. 

```python
# Creating and using a DatetimeIndex
## datacamp에 load되어 있는 data다. 따로 시계열 raw data를 구해보자. 
time_format = '%Y-%m-%d %H:%M' ## 선호하는 'time index'의 양식을 미리 정의해두는 것이 가독성을 위해 좋다. 

my_datetimes = pd.to_datetime(date_list, format=time_format)  
## pd.to_datetime(arg, format) : arg에는 integer, float, string, datetime, list, tuple, 1-d array, Series 가능. format에는 바꾸고 싶은 format을 string으로 선언

time_series = pd.Series(temperature_list, index=my_datetimes) 
## Construct a pandas Series using temperature_list and my_datetimes: time_series
time_series.head()

# Partial string indexing and slicing
ts1 = ts0.loc['2010-10-11 21:00:00':'2010-10-11 22:00:00'] ## Extract the hour from 9pm to 10pm on '2010-10-11': ts1
ts2 = ts0.loc['2010-07-04'] ## Extract '2010-07-04' from ts0: ts2
ts3 = ts0.loc['2010-12-15' : '2010-12-31'] ## Extract data from '2010-12-15' to '2010-12-31': ts3

## ts0는 2010-01-01 00:00:00부터 2010-12-31 23:00:00 까지 1시간 단위로 temperature를 저장한 data frame.
## 생각보다 slicing이 너그럽게 되는 것 같다.

# Reindexing the Index
ts3 = ts2.reindex(ts1.index) ## Reindex without fill method: ts3 
ts4 = ts2.reindex(ts1.index, method = 'ffill') ## Reindex with fill method, using forward fill: ts4
## .reindex(arg, method = '') : method를 정의해주지 않으면 새로 정의되는 index에 부합되지 않는 obs는 'NaN'으로 채워진다. 
## method = 'ffill'은 forward fill, 즉 NaN의 대상값 기준 앞쪽에 있는 value로 채워지고 'bfill'는 backward fill, 'ffill'의 반대다. 

sum12 = ts1 + ts2
sum13 = ts1 + ts3
sum14 = ts1 + ts4
```

## 3.2 Resampling time series data
'시간'을 index로 사용하는 시계열 자료의 특징은 '얼마만큼의 시간을 하나의 단위로 정의하느냐'에 따라 summary statistics의 값이 달라질 수 있다는 것이다. 즉 시간 단위, 일 단위, 주 단위, 연 단위 등의 주관적인 기준에 따라 summary statistics의 값이 달라질 수 있다. python에서는 이를 손쉽게 해결해줄 방법을 제공하고 있다. 더불어 python에서 정말 자주 볼 수 있고 실제로도 유용한 method chaining에 대해서도 간단히 알아보자. 
```python
# Resampling and frequency
df1 = df['Temperature'].resample('6H').mean() ## Downsample to 6 hour data and aggregate by mean: df1
df2 = df['Temperature'].resample('D').count() ## Downsample to daily data and count the number of data points: df2
## .resample('unit') : unit의 기준은 D : Day, H : Hour 등등, 더 많은 기준이 있는 것 같다. 
## Down-sampling : 시간 단위를 길게 잡아 row의 개수를 줄이는 방법 
## Up-sampling : 시간 단위를 짧게 잡아 row의 개수를 늘리는 방법 
```

다음 예제는 시계열 분석에서 말하는 '이동 평균'(Moving average or Rolling mean)를 다루고 있다. 이동 평균이란 말 그대로 시간의 흐름에 따라 변화하는 평균으로 '일정 기간의 평균'으로 이해하면 될 것이다. 예제에서 '일정 기간'(unit이라고 이해할 수 있는)은 24시간, 즉 하루 단위로 정의되었다. 시간의 흐름을 유의미하게 다루는 시계열 분석에서는 일반적인 개념 중 하나다. [위키피디아](https://en.wikipedia.org/wiki/Moving_average)의 자세한 설명을 참고하자.

```python
# Separating and resampling
august = df['Temperature'].loc['2010-08-01':'2010-08-31'] ## Extract temperature data for August
august_highs = august.resample('D').max() ## Downsample to obtain only the daily highest temperatures in August

february = df['Temperature'].loc['2010-02-01':'2010-02-28'] ## Extract temperature data for February
february_lows = february.resample('D').min() ## # Downsample to obtain the daily lowest temperatures in February

# Rolling mean and frequency
unsmoothed = df['Temperature']['2010-Aug-01':'2010-Aug-15'] ## Extract data from 2010-Aug-01 to 2010-Aug-15
smoothed = df['Temperature']['2010-Aug-01':'2010-Aug-15'].rolling(window=24).mean() ## Apply a rolling mean with a 24 hour window

august = pd.DataFrame({'smoothed':smoothed, 'unsmoothed':unsmoothed}) ## Create a new DataFrame with columns smoothed and unsmoothed

august.plot() ## Looking the rolling mean in the plot
plt.show()
```

```python
# Resample and roll with it
august = df['Temperature']['2010-08-01':'2010-08-31'] # # Extract the August 2010 data
daily_highs = august.resample('D').max() ## Resample to daily data, aggregating by max

daily_highs_smoothed = daily_highs.rolling(window = 7).mean() 
## Use a rolling 7-day window with method chaining to smooth the daily high temperatures in August
print(daily_highs_smoothed)
```

## 3.3 Manipulating time series data

```python
# Method chaining and filtering
## 항공기 이착륙에 대한 dataset
df.columns = df.columns.str.strip() ## Strip extra whitespace from the column names
## .str.strip([chars]) : 선언된 chars를 해당 문자열에서 삭제

dallas = df['Destination Airport'].str.contains('DAL') ## Extract data for which the destination airport is Dallas
## .str.contains(str) : 해당 data set에서 str이 속해있는 것만 filtering, T/F로 뽑힘 

daily_departures = dallas.resample('D').sum() ## Compute the total number of Dallas departures each day
## T/F는 1/0으로 계산되니까 '하루'를 기준으로 resample해서 더하면 int로 return됨. 

stats = daily_departures.describe() ## Generate the summary statistics for daily Dallas departures
```

다음의 예제에서는 .interpolate(how = 'method') 를 이용한 시계열 dataset 내에서의 NaN에 대한 보간법(interpolation method)을 다룬다. 이전에 배웠던 'ffill'과 bfill'은 앞 혹은 뒤의 value를 그대로 가져온다는 점에서 상대적으로 큰 오차를 가질 수 있는 문제가 있었다. 이러한 단점 때문에 .interpolate()가 제안되었고 interpolate()는 3개의 방법으로 NaN를 채워넣는다. NaN를 메꿔넣는 3가지의 방법은 아래와 같다. 예제에서는 1)만 다룬다. 추가적인 정보는 [페이지](https://rfriend.tistory.com/264)를 참고하자. 
1) 시계열데이터의 값에 선형으로 비례하는 방식으로 결측값 보간
1) 시계열 날짜 index를 기준으로 결측값 보간
1) DataFrame 값에 선형으로 비례하는 방식으로 결측값 보간
1) 추가적인 옵션, 결측값 보간 개수 제한하기

```python
# Missing values and interpolation
ts2_interp = ts2.reindex(ts1.index).interpolate(how='linear') ## Reset the index of ts2 to ts1, and then use linear interpolation to fill in the NaNs
differences = np.abs(ts1 - ts2_interp) ## Compute the absolute difference of ts1 and ts2_interp
print(differences.describe()) ## Generate and print summary statistics of the differences
```

```python
# Time zones and conversion
mask = df['Destination Airport'] == 'LAX' ## Build a Boolean mask to filter for the 'LAX' departure flights: mask
la = df[mask] ## Use the mask to subset the data: la
## 이런 식의 boolean return을 이용한 filtering을 masking이라 한다. 

times_tz_none = pd.to_datetime( la['Date (MM/DD/YYYY)'] + ' ' + la['Wheels-off Time'] ) ## Combine two columns of data to create a datetime series
times_tz_central = times_tz_none.dt.tz_localize('US/Central') ## Localize the time to US/Central
times_tz_pacific = times_tz_central.dt.tz_convert('US/Pacific') ## Convert the datetimes from US/Central to US/Pacific
```

## 3.4 Time series visualization
모든 데이터 분석의 결과가 그렇지만 간단하고 명확하게 보여주기 위해 시각화(visualizaiton)을 선호하는 편이다. 시계열 분석은 특히 시각화 방법을 쉽게 접할 수 있는 분야 중 하난데, 증권시장을 생각해보면 바로 이해할 수 있을 것이다. 

```python
# Plotting time series, datetime indexing
df.plot()
plt.show()

df.Date = pd.to_datetime(df['Date']) ## Convert the 'Date' column into a collection of datetime objects
df.set_index('Date', inplace=True) ## Set the index to be the converted 'Date' column

df.plot()
plt.show()

## 처음 결과와의 차이점은 index가 datatime object로 바뀌어서 xaxis가 '날짜'가 되었다는 것이다. 

# Plotting date ranges, partial indexing
df.Temperature['2010-Jun':'2010-Aug'].plot()
plt.show()
plt.clf() ## Plot the summer data

df.Temperature['2010-06-10':'2010-06-17'].plot()
plt.show()
plt.clf() ## Plot the one week data
```

# 4. Case Study - Sunlight in Austin
## 4.1 Reading and cleaning the data

```python
# Reading in a data file
import pandas as pd

df = pd.read_csv(data_file)
print(df.head()) ## 첫 열의 data가 column name으로 올라가 있음. 

df_headers = pd.read_csv(data_file, header=None) ## Read in the data file with header=None
print(df_headers.head()) ## 문제 해결 

# Re-assigning column names
column_labels_list = column_labels.split(',') ## Split on the comma to create a list: column_labels_list
## 이미 columns_labels이 정의되어 있었음. 

df.columns = column_labels_list ## Assign the new column labels to the DataFrame: df.columns

df_dropped = df.drop(list_to_drop, axis = 'columns') ## Assign the new column labels to the DataFrame: df.columns
## axis는 버리도록 선언된 value를 찾을 축. 
## 이미 버릴 list인 list_to_drop이 정의되어 있었음. 
print(df_dropped.head()) 

# Cleaning and tidying datetime data
df_dropped['date'] = df_dropped['date'].astype(str) ## Convert the date column to string: df_dropped['date']
df_dropped['Time'] = df_dropped['Time'].apply(lambda x:'{:0>4}'.format(x)) ## Pad leading zeros to the Time column: df_dropped['Time']

date_string = df_dropped['date'] + df_dropped['Time'] ## Concatenate the new date and Time columns: date_string
date_times = pd.to_datetime(date_string, format='%Y%m%d%H%M') ## Convert the date_string Series to datetime: date_times
df_clean = df_dropped.set_index(date_times) ## Set the index to be the new date_times container: df_clean

print(df_clean.head())

# Cleaning the numeric columns
print(df_clean.loc['2011-06-20 08:00:00' : '2011-06-20 09:00:00', 'dry_bulb_faren']) ## Print the dry_bulb_faren temperature between 8 AM and 9 AM on June 20, 2011

df_clean['dry_bulb_faren'] = pd.to_numeric(df_clean['dry_bulb_faren'], errors='coerce') ## Convert the dry_bulb_faren column to numeric values: df_clean['dry_bulb_faren']

print(df_clean.loc['2011-06-20 08:00:00' : '2011-06-20 09:00:00', 'dry_bulb_faren']) ## Print the transformed dry_bulb_faren temperature between 8 AM and 9 AM on June 20, 2011

df_clean['wind_speed'] = pd.to_numeric(df_clean['wind_speed'], errors='coerce')
df_clean['dew_point_faren'] = pd.to_numeric(df_clean['dew_point_faren'], errors='coerce') ## Convert the wind_speed and dew_point_faren columns to numeric values
```

## 4.2 Statistical exploratory data analysis

```python
# Signal min, max, median
print(df_clean['dry_bulb_faren'].median()) ## Print the median of the dry_bulb_faren column
print(df_clean.loc['2011-Apr':'2011-Jun', 'dry_bulb_faren'].median()) ## Print the median of the dry_bulb_faren column for the time range '2011-Apr':'2011-Jun'
print(df_clean.loc['2011-Jan', 'dry_bulb_faren'].median()) ## Print the median of the dry_bulb_faren column for the month of January

# Signal variance
daily_mean_2011 = df_clean.resample('D').mean() ## Downsample df_clean by day and aggregate by mean
daily_temp_2011 = daily_mean_2011['dry_bulb_faren'].values # # Extract the dry_bulb_faren column from daily_mean_2011 using .values
## numpy array로 return됨 

daily_climate = df_climate.resample('D').mean() ## Downsample df_climate by day and aggregate by mean: daily_climate
daily_temp_climate = daily_climate.reset_index()['Temperature'] ## Extract the Temperature column from daily_climate using .reset_index()
## Q. .reset_index()가 잘 이해가 안되네. 

difference = daily_temp_2011 - daily_temp_climate
print(difference.mean())

# Sunny or cloudy
is_sky_clear = df_clean['sky_condition']=='CLR'
sunny = df_clean[is_sky_clear]
sunny_daily_max = sunny.resample('D').max()

sunny_daily_max.head()

is_sky_overcast = df_clean['sky_condition'].str.contains('OVC')
overcast = df_clean[is_sky_overcast]
overcast_daily_max = overcast.resample('D').max()

overcast_daily_max.head()

sunny_daily_max_mean = sunny_daily_max.mean()
overcast_daily_max_mean = overcast_daily_max.mean()
print(sunny_daily_max_mean - overcast_daily_max_mean)
```

## 4.3 Visual exploratory data analysis

```python
# Weekly average temperature and visibility
import  matplotlib.pyplot as plt

weekly_mean = df_clean[['visibility', 'dry_bulb_faren']].resample('W').mean()
print(weekly_mean.corr())

weekly_mean.plot(subplots=True)
plt.show()

# Daily hours of clear sky
is_sky_clear = df_clean['sky_condition'] == 'CLR'
resampled = is_sky_clear.resample('D')
sunny_hours = resampled.sum()
total_hours = resampled.count()
sunny_fraction = sunny_hours / total_hours

sunny_fraction.plot(kind='box')
plt.show()

# Heat or humidity
monthly_max = df_clean[['dew_point_faren', 'dry_bulb_faren']].resample('M').max()
monthly_max.plot(kind = 'hist', bins = 8, alpha = 0.5, subplots = True)

plt.show()

# Probability of high temperatures
august_max = df_climate.loc['2010-08', 'Temperature'].max() ## Extract the maximum temperature in August 2010 from df_climate: august_max
print(august_max)

august_2011 = df_clean.loc['2011-08', 'dry_bulb_faren'].resample('D').max() ## Resample August 2011 temps in df_clean by day & aggregate the max value: august_2011
august_2011_high = august_2011.loc[august_2011 > august_max] ## Filter for days in august_2011 where the value exceeds august_max: august_2011_high

august_2011_high.plot(kind = 'hist', normed = True, cumulative = True, bins = 25) ## Construct a CDF of august_2011_high

plt.show()
```
