# 1. Introduction and flat files
## 1.1 Import text files
```python
# Importing entire text files
book = open('book_file_name.txt', mode ='r') ## mode = 'r' is to read
print(book.read()) ## Print it
print(book.closed) ## Check whether file is closed, False

book.close() ## # Close file
print(book.closed) ## True

# Read & print the first 3 lines
with open('book_file_name.txt') as book:
    print(file.readline())
    print(file.readline())
    print(file.readline())
```

## 1.2 Importing flat files using NumPy
파이썬에서는 관측값의 변수를 나타내는 column을 feature or attribute, 관측값의 정보가 입력되는 row를 field라고 하는 모양이다. kaggle에서도 variable대신에 feature로 column을 말하더라니. 파이썬에 data를 불러오는 대표적인 module, Numpy를 이용하는 방식과 Pandas를 이용하는 방식에 대해 배워보자. 먼저 Numpy를 이용하는 방법을 알아볼탠데 Numpy를 숫자처리에 효과적인 module로 data의 형태가 numerical한 경우 좋다. 물론 str 속성을 가진 numerical obs, integer나 float도 불러올 수 있다. 가령 data가 mixed type(숫자와 문자가 섞인 경우)인 경우 error가 발생하므로 이 경우엔 Pandas를 사용하자.  

```python
# Using NumPy to import flat files
import numpy as np
improt matplotlib.pyplot as plt

file = 'file.csv'
digits = np.loadtxt(file, delimiter=',') ## delimiter=',' obs를 구분할 '지점'을 정의. csv file을 load했으므로 구분점은 ','이다.  
print(type(digits))

## Select and reshape a row
im = digits[21, 1:] ## np.array digits의 22th row를 im에 저장 
im_sq = np.reshape(im, (28, 28)) ## im을 28 x 28 array로 변경. 

## Plot reshaped data 
plt.imshow(im_sq, cmap='Greys', interpolation='nearest')  
plt.show() ## mnist dataset을 이용한 손글씨 plotting이다. 아마 im에 정의된 것이 22번째 손글씨인 듯

# Customizing your NumPy import
data = np.loadtxt(file, delimiter='\t', skiprows=1, usecols=[0, 4])
## delimiter='\t' : tap으로 구분된 자료이므로 \t arg
## skiprows=1 : 생략할 row의 개수 설정
## usecols=[0, 4] : 불러올 columns 설정, 1st부터 3nd까지의 column load

# Importing different datatypes
## mixed_value : 1st row는 string, 나머지는 float의 numerical 
file = 'mixed_value.txt'
data = np.loadtxt(file, delimiter='\t', dtype=str) 
## dtype = str : string type으로 data load, 전체를 불러오기 위해 string type으로 load 선택. 

print(data[0]) ## str 확인 

data_float = np.loadtxt(file, delimiter='\t', dtype=float, skiprows=1)
## 첫 행에 포함된 str을 제거하고 data를 float로 load
print(data_float[0 : 10]) # float 확인 

# Working with mixed datatypes 
## titanic data는 대표적인 mixed data table
file = 'directory/titanic.csv'
titanic_data = np.recfromcsv(file, delimiter = ',', names=True, dtype=None)
print(titanic_data[:3])
```
## 1.3 Importing flat files using pandas
dataset이 하나의 형식의 entry로 구성될 가능성은 극히 적다. 오히려 feature에 따라 여러 type의 entry가 뒤섞여있을 가능성이 크다. 이 경우 Pandas를 이용한 dataframe으로 import하는 것이 좋다. pandas는 import뿐 아니라 데이터 분석에 사용할 수 있는 여러 function과 method가 있으므로 깊히 익혀두면 좋다. 
```python
# Using pandas to import flat files as DataFrames
import pandas as pd 
file = 'directory/titanic.csv'
df = pd.read_csv(file)
print(df.head())

file = 'numerical_data'
data = pd.read_csv(file, nrows = 5, header=None) ## header = None : column이름 제거, column이름을 제거하면 column name이 자리에 맞는 숫자로 return된다.
data_array = np.array(data)

# Customizing your pandas import
import matplotlib.pyplot as plt

file = 'directory/titanic_tab.csv'
data = pd.read_csv(file, sep='\t', comment='#', na_values='Nothing')
## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html 에서 comment와 na_values 확인 
## na_values : NA/NaN로 인식할 추가 문자열(Additional strings to recognize as NA/NaN.)
## comment : 해당 문자열로 시작하는 line는 무시하고 넘어간다. 
##           Indicates remainder of line should not be parsed. If found at the beginning of a line, the line will be ignored altogether. 
print(data.head())

## Plot 'Age' variable in a histogram
pd.DataFrame.hist(data[['Age']])
plt.xlabel('Age (years)')
plt.ylabel('count')
plt.show()
```

# 2. Importing data from other file types
# 2.1 Introduction to other file types
데이터나 분석 결과를 포함하고 있는 파일 형식은 굉장히 다양하다. 익숙하게 보는 excel file이나 matlab, SAS, SPSS 등등, 파이썬은 대부분의 file들을 module을 통해 불러올 수 있다. 대표적으로 사용하는 몇 개의 파일 형식을 파이썬으로 불러와보자. 특별히, 파이썬 기반의 pickled file에 대해서도 알아볼 것이다. 

flat data(예를 들어 list, dict)를 파일로 저장할 때는 기존의 file importing을 이용하면 되지만 flat data가 아닌 자료형은 일반적인 방법으로는 데이터를 저장하거나 불러올 수 없다. 이 경우, 파이썬에서는 pickle module을 사용해 텍스트 이외의 자료형을 파일로 저장하고 불러올 수 있다. pickle module은 모든 파이썬 데이터 객체를 저장하고 읽을 수 있다.

```python
# Loading a pickled file
import pickle

## Open pickle file and load data: d 
with open('file.pkl', 'rb') as file: ## 'rb' : 'read only'의 의미. 다른 arg로는 'binary'가 있다. 
    d = pickle.load(file)
    
print(d)
print(type(d))

# Listing sheets in Excel files
import pandas as pd

file = 'file_nanme.xlsx'
xls = pd.ExcelFile(file) ## Load spreadsheet: xls
print(xls.sheet_names) ## Print sheet names

# Importing sheets from Excel files
df1 = xls.parse('2004') ## sheet name을 call해서 sheet를 object로 저장하는 방법 
df2 = xls.parse(0) ## sheet의 index를 call해서 sheet를 obejct로 저장하는 방법

print(df1.head())
print(df2.head())

# Customizing your spreadsheet import
# Parse the first sheet and rename the columns: df1
df1 = xls.parse(0, skiprows=1, names=['Country', 'AAM due to War (2002)'])
## sheet를 index로 call, 1행 생략, column name을 바꿔줌(list type으로 작성) 

# Parse the first column of the second sheet and rename the column: df2
df2 = xls.parse(1, usecols=[0], skiprows=1, names=['Country'])
## sheet를 index로 call, 1열 생략(반드시 list type으로 작성), 1행 생략, column name을 바꿔줌(list type으로 작성)

print(df1.head())
print(df2.head())
```
## 2.2 Importing SAS/Stata files using pandas
```python
# Importing SAS files
from sas7bdat import SAS7BDAT
with SAS7BDAT('sales.sas7bdat') as file:
    df_sas = file.to_data_frame() ## .to_data_frame() : dataframe으로 바꿔주는 좋은 method
print(df_sas.head())

# Importing Stata files
import pandas as pd
df = pd.read_stata('disarea.dta') ##pd.read_stata()를 이용해 stata file을 df로 읽어올 수 있다. 
print(df.head())
```

## 2.3 Importing HDF5 files
