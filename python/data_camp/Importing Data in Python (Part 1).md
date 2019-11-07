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
HDF5 files이란 Hierarchical Data Format version 5을 말한다. 대용량의 numerical data를 저장하기 위한 file이며 이때의 '대용량'이란 hundreds of gigabytes나 terabytes 수준에 달한다. HDF5는 최대 exabytes의 수준까지 저장가능하다고 하니 정말로 '대용량'인 셈이다. 
```python
# Using h5py to import HDF5 files
import numpy as np
import h5py

file = 'LIGO_data.hdf5' ## LIGO : Laser Interferometer Gravitational-Wave Observatory
## 추가적인 정보는 아래의 링크에서 확인해볼 수 있다.
## https://ko.wikipedia.org/wiki/%EB%A0%88%EC%9D%B4%EC%A0%80_%EA%B0%84%EC%84%AD%EA%B3%84_%EC%A4%91%EB%A0%A5%ED%8C%8C_%EA%B4%80%EC%B8%A1%EC%86%8C
## https://www.gw-openscience.org/events/GW150914/

data = h5py.File(file, 'r') ## 'r' is 'read only'

# Print the datatype of the loaded file
print(type(data))

# Print the keys of the file
for key in data.keys():
    print(key)

# Extracting data from your HDF5 file
group = data['strain']

for key in group.keys():
    print(key)

strain = data['strain']['Strain'].value
num_samples = 10000
time = np.arange(0, 1, 1/num_samples)

plt.plot(time, strain[:num_samples])
plt.xlabel('GPS Time (s)')
plt.ylabel('strain')
plt.show()
```

## 2.4Importing MATLAB files
```python
# Loading .mat files
import scipy.io
mat = scipy.io.loadmat('albeck_gene_expression.mat')
print(type(mat)) ## dict 형태로 load됨 

# The structure of .mat in Python
print(mat.keys())
print(type(mat['CYratioCyt']))
print(np.shape(mat['CYratioCyt']))

data = mat['CYratioCyt'][25, 5:]
fig = plt.figure()
plt.plot(data)
plt.xlabel('time (min.)')
plt.ylabel('normalized fluorescence (measure of expression)')
plt.show()
```

# 3. Working with relational databases in Python
relational databases, 그러니까 ['관계형 데이터베이스'](https://ko.wikipedia.org/wiki/%EA%B4%80%EA%B3%84%ED%98%95_%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4)는 이름이나 개념, 용어가 생소할 뿐이지 사실 쉽게 찾아볼 수 있는 형태이다. '관계형'이라는 이름이 붙은 이유는 data를 저장하고 있는 여러 테이블들이 '관계'를 맺고 있기 때문인데 가령 테이블 '주문 목록', '고객 목록', '직원 목록'의 테이블 3개가 관계형 데이터베이스 형태로 저장되어 있다고 하자. 이 때, '주문 번호', '고객 ID', '직원 ID'을 정의하는 고유 키(primary key)가 존재하고 고유 키로 row(관계형 데이터베이스 하에서는 튜플 또는 레코드)가 구분된다. 따라서, '주문 목록' 테이블는 '주문 번호'가 고유 키가 되어 주문(row)을 식별할 수 있도록 하며 '주문'에 관련된 column이 외래 키로 추가되어 테이블을 이룬다. [목적에 맞게 table을 편집해 비교적 간략하게 볼 수 있으며 유지보수가 간편하다는 장점이 있지만 추가적인 연산이나 저장공간이 필요하므로 더 많은 자원이 활용되어 시스템의 부하가 높다는 단점 또한 존재한다.](https://m.blog.naver.com/PostView.nhn?blogId=acornedu&logNo=221040291485&proxyReferer=https%3A%2F%2Fwww.google.com%2F) 흔히 볼 수 있는 SQL(Structure Query Language)를 이용한 데이터베이스가 관계형 데이터베이스의 대표적인 예다. 

## 3.1 Creating a database engine in Python
파이썬을 이용해 데이터 베이스 엔진을 만들 수도 있다. SQL를 기반으로한 데이터베이스 엔진은 여러 종류가 있지만 빠르고 간단하게 실습할 수 있는 SQLite를 사용할 것이다. 파이썬에서는 SQL을 사용할 수 있는 여러개의 module이 존재하는데 그 중 데이터 베이스 관리에 많이 사용되는 SQLAlchemy를 사용해 데이터 베이스 엔진을 만들어도록 하겠다. 

```python
# Creating a database engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Chinook.sqlite')
## Chinook에 대한 추가적인 정보는 아래의 링크를 참고하자.
## https://github.com/lerocha/chinook-database

# What are the tables in the database?
table_names = engine.table_names()
print(table_names)
```

## 3.2 Querying relational databases in Python
SQL기반의 데이터베이스를 다루는 일이므로 당연히, query를 통해 데이터베이스에서 data를 가져올 수 있게 되어 있다. 이 과정을 파이썬으로 실습해보자. 과정의 순서는 아래와 같다. 
- Import packages and functions
- Create the database engine
- Connect to the engine
- Query the database
- Save query results to a DataFrame
- Close the connection

```python
# The Hello World of SQL Queries!
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('sqlite:///Chinook.sqlite') ## 1.import package and creat engine

con = engine.connect() ## 2. connect to the engine

rs = con.execute('SELECT * FROM album') ## 3. query the db
## 'SELECT * FROM album' : SQL 쿼리, album table의 모든(*) column을 선택(SELECT)함. 

df = pd.DataFrame(rs.fetchall()) ## 4. save query results to a df
## query.fetchall() : 모든 row를 가져올 것. 

con.close() ## 5. close connection
print(df.head())

# Customizing the Hello World of SQL Queries
## 1단계는 미리 진행해뒀다고 가정
## with을 이용한 진행으로 SQL 쿼리의 중요한 부분에 대한 가독성을 높일 수 있음 
with engine.connect() as con:
    rs = con.execute("SELECT LastName, Title FROM Employee")
    df = pd.DataFrame(rs.fetchmany(3)) ## query.fetchmany(int) : int만큼의 row를 가져옴 
    df.columns = rs.keys() ## db에서는 'column'을 key라 한다. 
print(len(df))

# Filtering your database records using SQL's WHERE
engine = create_engine('sqlite:///Chinook.sqlite')

with engine.connect() as con:
    rs = con.execute('SELECT * FROM Employee WHERE EmployeeId >= 6') ## WHERE condtion : SQL 쿼리에서의 filtering에 사용, 
    df = pd.DataFrame(rs.fetchall())
    df.columns = rs.keys()
print(df.head())

# Ordering your SQL records with ORDER BY
engine = create_engine('sqlite:///Chinook.sqlite')

with engine.connect() as con:
    rs = con.execute('SELECT * FROM Employee ORDER BY BirthDate') ## ORDER BY key : SQL 쿼리에서의 Ordering에 사용 
    df = pd.DataFrame(rs.fetchall())
    df.columns = rs.keys()
print(df.head())
```

## 3.3 Querying relational databases directly with pandas
3.2에서 실습해본 내용은 SQL db에 접근, 쿼리를 통해 data를 가져오는 정석적인 과정이다. 이미 우리가 알고 있는 Pandas package로 이 과정을 조금 더 간편하게 해볼 수 있다. 

```python
# Pandas and The Hello World of SQL Queries!
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///Chinook.sqlite')

df = pd.read_sql_query("SELECT * FROM Album", engine) ## Pandas.read_sql_query("QUERY", engine)
print(df.head())

with engine.connect() as con:
    rs = con.execute("SELECT * FROM Album")
    df1 = pd.DataFrame(rs.fetchall())
    df1.columns = rs.keys()

print(df.equals(df1)) ## pandas를 이용한 방법과 3.2의 방법이 같은가? 같음. 

# Pandas for more complex querying
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///Chinook.sqlite")
df = pd.read_sql_query("SELECT * FROM Employee WHERE EmployeeID >= 6 ORDER BY BirthDate", engine)
## 쿼리 부분이 길면 따로 저장해서 해도 됨
query = "SELECT * FROM Employee WHERE EmployeeID >= 6 ORDER BY BirthDate"
df1 = pd.read_sql_query(query, engine)
print(df.head())
print(df1.head())
```

## 3.4 Advanced querying: exploiting table relationships
```python
# The power of SQL lies in relationships between tables: INNER JOIN
with engine.connect() as con:
    rs = con.execute("SELECT Title, Name FROM Album INNER JOIN Artist on Album.ArtistID = Artist.ArtistID")
    ## title과 Name을 선택 / Album table과 Artist table로부터 "INNER JOIN하는 것만"/ "INNER JOIN의 조건은 Album table의 ArtistID와 Artist table의 AristID가 같아야 함.   
    df = pd.DataFrame(rs.fetchall())
    df.columns = rs.keys()
print(df.head())

# Filtering your INNER JOIN
df = pd.read_sql_query("SELECT * FROM PlaylistTrack INNER JOIN Track on PlaylistTrack.TrackId = Track.TrackId WHERE Milliseconds < 250000", engine)
print(df.head())
```
