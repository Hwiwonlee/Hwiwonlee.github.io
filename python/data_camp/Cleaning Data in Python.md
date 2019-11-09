# 1. Exploring your data

data 분석 과정에서 가장 긴 시간이 걸리는 과정이 전처리(pre-processing)이고 전처리 과정의 대부분이 cleaning 혹은 wraggling이라 불리는 dataset 편집 작업이다. 아래의 문제들이 이 과정에서 우리가 해결해야할 문제들의 대표적인 예시들이다. 이제 하나하나 살펴보며 python으로 해결하는 방법을 배워보자. 
- Inconsistent column names
- Missing data
- Outliers
- Duplicate rows
- Untidy
- Need to process columns
- Column types can signal unexpected data values

## 1.1 Diagnose data for cleaning
```python
# Loading and viewing your data
import pandas as pd
df = pd.read_csv(dir)
print(df.head())
print(df.tail())
print(df.shape) ## check nrow X rcol
print(df.columns) ## check the columns name
## .shape와 columns은 df의 attritute이므로 '()'를 붙이지 않는다. '()'를 붙이는 건 method만이다. 
print(df_subset.head()) 
print(df_subset.tail()) ## df '일부'의 head와 tail

# Further diagnosis
print(df.info())
print(df_subset.info())
## .info method는 df의 주요한 정보들을 모두 알려주는 매우 유용한 method다. 
## '주요한 정보'란 row와 column의 수, column에 있는 결측치의 수, 저장된 data의 type 등을 의미한다. 
```

## 1.2 Exploratory data analysis (EDA)
EDA는 특별한 model, method 혹은 insight 없이 dataset 만으로 진행할 수 있는 데이터 분석 방법이다. 보통 dataset이 가진 data의 전반적인 상태를 알아보기 위한 목적으로 진행하며 전처리 전에 결측치 유무와 같은 dataset의 문제를 알아보기 위해 한번, 전처리 후에 문제가 해결되었는지 알아보기 위해 한번 시행한다. 한번, 한번이라고 했지만 전처리 과정 내내 EDA로 값을 확인하는 것이 보통이므로 방법을 잘 알아두는 것이 좋다. 강의=에서는 비교적 간단한 방법을 소개해주고 있다. 

```python
print(df['Borough'].value_counts(dropna=False)) 
print(df['State'].value_counts(dropna=False))
print(df['Site Fill'].value_counts(dropna=False)) ## 각각 'column'에 빈번하게 나오는 value를 count해서 return하는 방법들이다. dropna는 결측치를 제외할 것인지에 대한 parameer이다. 

df.describe() ## EDA의 기본인 summary statistics을 보여주는 method 
```

## 1.3 Visual exploratory data analysis
EDA를 비롯해 널리 사용되는 3개의 plot, Histogram, Boxplot, Scatter plot을 소개하겠다. 먼저 Histogram은 변수의 분포를 알기 위한 목적으로 사용된다. Boxplot은 Historam과 유사한 모양을 갖지만 이상치 검출을 위해 사용되며 Scatter plot은 두 개의 변수 사이의 관계나 분포를 알아보기 위해 사용된다. 위의 세가지 plot은 몇 가지 방법으로 응용 가능하며 data의 개략적인 형태를 명확하게 보여줄 수 있는 좋은 방법들이다. 

```python
# Visualizing single variables with histograms
import pandas as pd
import matplotlib.pyplot as plt
df['Existing Zoning Sqft'].describe()

df['Existing Zoning Sqft'].plot(kind='hist', rot=70, logx=True, logy=True)
## pandas의 .plot() method를 이용한 plotting이다. kind = 'hist'로 histogram을 선택하고 x와 y를 log scale로 변환했다. 
## rot은 x 눈금의 회전 정도인데...필수인가보다.
## .plot()에 대한 더 많은 이야기 : https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.DataFrame.plot.html

plt.show()


# Visualizing multiple variables with boxplots
df.boxplot(column='initial_cost', by='Borough', rot=90)
## 'initial_cost' columns의 값를 대상으로 'Borough' column의 값을 기준으로 grouping해서 box plot을 그린다. 
## Manhattan의 initial_cost에 이상치가 보인다. error인지 이상치인지는 나중에 판단한다. 
plt.show()

# Visualizing multiple variables with scatter plots
df.plot(kind='scatter', x='initial_cost', y='total_est_fee', rot=70)
plt.show() ## 이상치에 의한 plot의 왜곡 

df_subset.plot(kind='scatter', x='initial_cost', y='total_est_fee', rot=70)
plt.show() ## subset으로 plot의 왜곡없이 볼 수 있다. 물론, 이상치가 제거된 것은 아니다. 
```

# 2. Tidying data for analysis

## 2.1 Tidy data
> Q. tidy data와 melt의 관계?

```python
# Reshaping your data using melt
from pydataset import data
airquality = data('airquality')
print(airquality.head())

airquality_melt = pd.melt(airquality, id_vars=['Month', 'Day']) 
## id_vars = ['col_name'] : observation을 식별하는 기준이 될 column. melting에 기준이 되어 나머지 column들을 melting한다.  

print(airquality_melt.head())

# Customizing melted data
airquality_melt = pd.melt(airquality, id_vars=['Month', 'Day'], var_name='measurement', value_name='reading')
## var_name = melting된 column들이 속한 column의 이름을 편집 
## value_name = melting된 column들이 가지고 있던 value의 이름을 편집 

print(airquality_melt.head())
```

## 2.2 Pivoting data

```python
# Pivot data
print(airquality_melt.head())

airquality_pivot = airquality_melt.pivot_table(index=['Month', 'Day'], columns='measurement', values='reading')
## index = ['col_name'] : pivotting에 주축이 되어줄 column
## columns = 'col_name' : index를 기준으로 value들이 column이 될 열
## values = 'col_name' : index와 'columns'에 속한 값들. 위의 columns에서 '열'로 풀린 해당 열에 맞춰 data value 자리에 들어간다. 
print(airquality_pivot.head())

# Resetting the index of a DataFrame
print(airquality_pivot.index)

airquality_pivot_reset = airquality_pivot.reset_index() ## 월, 일이었던 index를 초기화, default index인 observation numbering이 됨.  

print(airquality_pivot_reset)
print(airquality_pivot_reset.head())

# Pivoting duplicate values
airquality_pivot = airquality_dup.pivot_table(index=['Month', 'Day'], columns='measurement', values='reading', aggfunc=np.mean)
```
> # Pivoting duplicate values 는 잘 모르겠다. aggfunce의 default가 mean이어서 그런가? np.sum을 해보니 확실히 바뀌는 게 있다. 

[출처](https://rfriend.tistory.com/275)

```python
import pandas as pd
data = pd.DataFrame({'cust_id': ['c1', 'c1', 'c1', 'c2', 'c2', 'c2', 'c3', 'c3', 'c3'],
                     'prod_cd': ['p1', 'p2', 'p3', 'p1', 'p2', 'p3', 'p1', 'p2', 'p3'],
                     'grade' : ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B'],
                     'pch_amt': [30, 10, 0, 40, 15, 30, 0, 0, 10]})

# print(pd.pivot_table(data, index=['cust_id', 'grade'], columns='prod_cd', values='pch_amt'))
# pd.pivot_table(data, index='cust_id', columns=['grade', 'prod_cd'], values='pch_amt')
print(data)
print(pd.pivot_table(data, index='grade', columns='prod_cd', values='pch_amt'))
print(pd.pivot_table(data, index='grade', columns='prod_cd', values='pch_amt', aggfunc=np.sum))
print(pd.pivot_table(data, index='grade', columns='prod_cd', values='pch_amt', aggfunc=np.mean))
```
index가 'grade' : ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B']로, column이 'prod_cd': ['p1', 'p2', 'p3', 'p1', 'p2', 'p3', 'p1', 'p2', 'p3']로 선언되었다. 이 경우, pd.pivot_table()은 같은 (row, col)을 갖는 '중복값'을 aggfunc으로 처리, 하나의 value로 return하게 된다. aggfunc을 정의해주지 않으면 default로 'mean'이 설정되어 같은 (row, col)을 갖는 중복값 사이의 평균을 return한다. 

**Q.aggregation 되지 않은 값을 볼 수는 없나?**

**A.** (11.09)

## 2.3 Beyond melt and pivot

```python
# Splitting a column with .str
tb_melt = pd.melt(tb, id_vars=['country', 'year'])

## problem : variable, 'm014' means 'male' with 0 ~ 14 ages
## So, splitting a column with .str
tb_melt['gender'] = tb_melt.variable.str[0] ## m014 중 'm'만 잘라오기 
tb_melt['age_group'] = tb_melt.variable.str[1:] ## m014 중 나머지 014만 잘라오기 

print(tb_melt.head())


# Splitting a column with .split() and .get()
ebola = pd.read_csv(dir)

ebola_melt = pd.melt(ebola, id_vars=['Date', 'Day'], var_name='type_country', value_name='counts')
print(ebola_melt)

# Splitting a column with .split() and .get()
ebola_melt['str_split'] = ebola_melt.type_country.str.split('_')

# Create the 'type' column
ebola_melt['type'] = ebola_melt.str_split.str.get(0)

# Create the 'country' column
ebola_melt['country'] = ebola_melt.str_split.str.get(1)

# Print the head of ebola_melt
print(ebola_melt.head())

```
