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
plt.ylabel('Price ($US)')

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
