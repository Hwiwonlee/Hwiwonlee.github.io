# Intermediate Python for Data Science
## 1. Matplotlib
Matplotlib는 시각화 module이 주를 이루는 package다. Chapter 1. Matplotlib는 Matplotlib에 어떤 function이 있고 어떻게 활용하는지 알아볼 것이다. 

### 1.1 Line plot and scatter plot 
Line plot과 scatter plot, 즉 선 그림과 산포도는 기초적인 plot 중 대표적인 예이다. 일반적으로 2차원의 자료구조에서 각 차원의 데이터값 사이에 존재하는 선형관계를 나타낼 때 선 그림을, data가 얼마나 퍼져 있는지 알아보고 싶을 때 산포도를 사용한다. 
```python
"""
1980년부터 2020년까지 어느 도시의 인구가 1000부터 5100까지 100씩 증가했다고 가정해보자.
"""
year = list(range(1980, 2021, 1))
pop = list(range(1000, 5100, 100))
print(year)
print(pop)

import matplotlib.pyplot as plt ## matplotlib.pyplot를 'plt'로 import
plt.plot(year, pop) ## plp.plot(x, y) : 선언된 arg인 year와 pop list를 이용해 line plot 생성 
plt.show() ## 생성된 plot 출력

plt.scatter(year, pop)  
plt.xscale('log') ## 'year'의 scale을 log로 변환, plot을 만든 후 scale을 변환하는 것이 특징이다.  
plt.show()
```
### 1.2 Histogram
Histogram은 data의 분포를 알아보기 위해 사용한다. Histogram은 data가 갖고 있는 전체 구간을 정해진 bins만큼으로 나눈 후, 각 bin안에 나눠진 구간에 속하는 data value의 빈도수로 그릴 수 있다. 
```python
score = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,9,10]
plt.hist(score) ## plt.hist(list, bins) : bins는 따로 정의하지 않으면 default, 10이다.
plt.show()
plt.clf() ## 앞서 그린 plot을 삭제 
plt.hist(score, bins = 3) ## bins를 3개로 정의한 histogram
plt.show()
```

### 1.3 Customization
시각화에서 data를 표현하기에 적절한 plot을 정하는 것만 중요하다고 생각할 수 있는데, 명확한 plot형태를 갖추는 것도 상당히 중요한 일이다. plot의 x축과 y축의 의미가 무엇인지, plot 안에 다른 색깔들을 사용했다면 각각의 색이 무엇을 의미하는지, 단위가 어떤지 등등, plot의 형태를 다루는 Customization는 메세지를 간결하고 명확하게 전달하기 위한 시각화에 필수적인 요소이다. 

```python
# plot 먼저 
plt.scatter(pop, year)

# Strings, plot에 들어갈 strings
xlab = 'population'
ylab = 'years'
title = 'Changes population in the city'

# Add axis labels, 위에서 추가한 strings을 적절한 위치에 추가 
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(title)

plt.show()

# Definition of tick_val and tick_lab
"""
'tick', 한 틱, 두 틱할 때 그 '틱'인데 한글로 뭐라고 해야할지 모르겠네. 아! 눈금!
plot은 개략적인 정보만 전달하면 되므로 자잘한 숫자들보다 큰 덩어리로 보여주는 것이 효과적일 때가 있다. 그 때, xticks() 함수를 사용한다. 
xtick()이 있는 것처럼 ytick()도 있으며 xtick((대체될 눈금), (대체할 눈금))
"""
tick_val = [1000, 2000, 3000, 4000, 5000]
tick_lab = ['1k', '2k', '3k', '4k', '5k']
plt.xticks(tick_val, tick_lab)
plt.show()

# Size, color and additional customization

## 아직 raw data가 없어서 data camp 코드를 그대로 가져왔다. 
# Import numpy as np
import numpy as np

# Store pop as a numpy array: np_pop
np_pop = np.array(pop)

# Double np_pop
np_pop = np_pop * 2

# Update: set s argument to np_pop
plt.scatter(gdp_cap, life_exp, s = np_pop, c = col, alpha = 0.8)
"""
plt.scatter()에서 parameter 's'가 의미하는 것이 point의 'size'이다. 
위의 예제의 경우, size를 '인구수'로 정의하므로써 인구수에 따른 point의 크기 차이를 만들어냈다.
마찬가지로 c가 의미하는 것은 color로 미리 만들어준 color object 'col'로 해당 plot의 point 색깔을 정의했다.
마지막으로 alpha는 '투명도'이다. 0부터 1까지의 값을 줄 수 있으며 0은 완전 투명, 1은 완전 불투명으로 정의되었다.
"""

# Additional customizations
plt.text(1550, 71, 'India') ## plt.text(x, y, string) : x, y의 값과 일치하는 plot의 point에 string 추가 
plt.text(5700, 80, 'China')

# Add grid() call
plt.grid(True) ## plot의 바탕에 grid 추가 


```




## 2. Dictionaries & Pandas
A, B, C, ... , Z의 임의의 도시가 있고 각각의 도시가 "인구수"라는 값을 갖는다고 가정해보자. 만약, 리스트(이 때의 리스트는 2D가 아닌 1차원 리스트로 한정한다)를 사용해서 이 상황을 다룰려면 도시 리스트 Cities와 인구수 리스트 Population 두 개의 리스트가 필요하다. 한 도시의 인구수를 알기 위해 두 개의 리스트를 이용하는 것은 비효율적인 동시에 직관적이지 않다. Dictionary type의 자료형은 이 문제를 해결하기 위해 Key:value형태로 자료를 저장한다. 이번 챕터에서는 Dictionary와 유용한 Package인 Pandas에 대해 알아볼 것이다. 

### 2.1 Dictionary
Dictionary는 Key:value의 구조로 data를 저장한다. 앞서 보았던 List와 비교해보면서 차이점을 알아보자. 
```python
# If I used two lists
countries = ['Korea', 'Japan', 'China', 'Taiwan']
capitals = ['Seoul', 'Tokyo', 'Beijing', 'Taipei']
ind_Korea = countries.index('Korea') # Korea에 해당하는 index를 return, 0
print(capitals[ind_Korea])

# Just use Dictionary
contries_capitals = {'Korea':'Seoul', 'Japan':'Tokyo', 'China':'Beijing', 'Taiwan':'Taipei'}
print(contries_capitals)
type(contries_capitals) # type : dict 확인 

# Print out the keys in contries_capitals
print(contries_capitals.keys()) ## Dict.keys() : 해당 Dict의 keys를 return
# Print out the values in contries_capitals
print(contries_capitals.values()) ## Dict.values() : 해당 Dict의 values를 return
# Print out value that belongs to key 'Taiwan'
print(contries_capitals['Taiwan'])

# Add Russia to contries_capitals
contries_capitals['Russia'] = 'Moscow'
# Print out italy in europe
print('Russia' in contries_capitals)
print(contries_capitals)

# Remove Japan to contries_capitals
del(contries_capitals['Japan'])
print('Japan' in contries_capitals)
print(contries_capitals)

# Dictionariception : Dictionary of dictionaries, Dictionary 안에 Dictionary. 
contries_capitals = { 'Korea': { 'capital':'Seoul', 'population':51.46 },
                     'Japan': { 'capital':'Tokyo', 'population':126.78 },
                     'China': { 'capital':'Beijing', 'population':13864 },
                     'Taiwan': { 'capital':'Taipei', 'population':23.49 } }

add = {'capital':'Moscow', 'population':144.49} ## 추가할 자료
contries_capitals['Russia'] = add ## Dict, contries_capitals안에 추가 
print(contries_capitals) ## 확인 
print(contries_capitals['Korea']) ## 'Korea' key를 갖는 values 출력
print(contries_capitals['Korea']['capital']) ## Korea key와 capital key를 갖는 value 출력 
```

### 2.2 Pandas
보통, 데이터 분석 업무는 많은 양의 데이터를 대상으로 한다. 특히, observation 수와 variable의 개수가 늘어나면 날수록 다루기가 쉽지 않다. Python의 Pandas package는 위와 같은 상황에서 데이터 분석을 비교적 간편하게 할 수 있게 고안되었다. Pandas는 numpy package를 기반으로 만들어졌다. Pandas는 "array 내부의 data type이 통일되어야 한다"는 numpy array의 단점을 보완한 Data frame object를 생성할 수 있게 해주며 이로써 좀 더 일반적인 상황에서의 데이터 분석을 지원한다. Pandas 만으로도 많은 경우의 데이터 분석을 할 수 있으므로 이번 챕터 이후, 추가로 공부해보길 바란다. 
```python
countries = ['Korea', 'Japan', 'China', 'Taiwan']
capitals = ['Seoul', 'Tokyo', 'Beijing', 'Taipei']
pop = [51.46, 126.78, 13864, 23.49]
Dict = {'countries' : countries, 'capitals' : capitals, 'populations' : pop} 

import pandas as pd
Infor = pd.DataFrame(Dict)
print(Infor) ## Keys가 col로 value가 row로 채워지는 것을 확인

row_labels = ['KR', 'JP', 'CHN', 'TPW'] ## 행 이름
Infor.index = row_labels ## 행 이름 바꾸기 
print(Infor)

# Import the Infor.csv data: Infor
Infor = pd.read_csv('Infor.csv') ## csv파일은 없지만 이렇게 하면 된다. 
Infor_index_col = pd.read_csv('cars.csv', index_col = 0) ## index_col = 0 : 앞서 했던 행 이름 바꾸기를 자동으로 진행.
print(Infor)
print(Infor_index_col)
```
#### 2.2.1 The way for accessing the row and column with DataFrame 
Dataframe의 열과 행을 출력 혹은 추출, 편집하고자 할 때 사용할 수 있는 방법은 크게 두 가지로 나뉘는데, 1) square brackets way, 2) loc, iloc function 이다. square brackets way를 이용하는 방법은 column에 접근하는 DF[['label']]와 row에 접근하는 DF[index]가 있다.  
```python
# Print out country column as Pandas Series using Label based calling
print(Infor['capitals'])
print(type(Infor['capitals'])) ## <class 'pandas.core.series.Series'>

# Print out country column as Pandas DataFrame using Label based calling
print(Infor[['capitals']])
print(type(Infor[['capitals']])) ## <class 'pandas.core.frame.DataFrame'>
## Label based calling에서 DataFrame으로 object를 갖고 오려면 double square brackets을 이용하자. 

# Print out DataFrame with countries and capitals columns using Label based calling
print(Infor[['countries', 'capitals']])
print(Infor[0:2])
```
##### Pandas series와 one-column Data frame의 차이?
https://stackoverflow.com/questions/26047209/what-is-the-difference-between-a-pandas-series-and-a-single-column-dataframe/26240208
구글링과 위 코드의 결과값으로 두 object의 차이를 설명해보자. Pandas series는 Data frame를 구성하는 data struct의 부분(=하나의 column)이다. 그렇지만 Pandas series는 Data frame이 아니다. 코드 실행에 있어서 두 object가 차이를 갖는지 모르겠지만 개념 상으로는 차이가 있다. 위의 stackoverflow의 댓글에는 Dimension에 따라 series와 Data frame을 구분하는 경우도 있는 것 같은데 질문의 전제 조건이 one-column Data frame과 Pandas series에 대한 비교이므로 적절한 답변은 아닌 것 같다. 

loc은 Label based, iloc는 index baesd function으로 argument에 유의해야 한다. square brackets method와 달리 열, 행 모두 double square brackets을 사용해야만 DataFrame을 return받을 수 있으므로 loc or iloc function을 사용할 것이라면 double square brackets에 주의하도록 하자.  
```python
print(Infor.iloc[0]) 
print(Infor.loc['KR']) ## single square bracket을 사용하면 Pandas Series

print(Infor.iloc[[0]])
print(Infor.loc[['KR']]) ## double square brackets을 사용하면 DataFrame

print(Infor.iloc[[0,1,2], [0]])
print(Infor.loc[['KR','JP','CHN'], ['countries']])

print(Infor.iloc[:, [0]])
print(Infor.loc[:, ['countries']]) ## 전체 column을 선택하고 싶다면 column argument에 ':' 입력

print(Infor.iloc[[0,1], :]) 
print(Infor.loc[['KR','JP']]) ## 전체 row를 선택하고 싶다면 row argument를 생략하거나 column과 마찬가지로 argument에 ':' 입력
```

## 3. Logic, Control Flow and Filtering
### 3.1 Comparison operators
Comparison operators, 즉 비교 연산자를 이용한다면 조건에 맞는 observation만 선택할 수 있으므로 데이터를 추출하는 filtering 작업이 굉장히 단순해진다. 이번 챕터에서는 비교 연산자에 대한 기본을 공부해보자. 

```python
# Create arrays
import numpy as np
my_score = np.array([90.0, 85.3, 23.1, 68.5])
your_score = np.array([84.0, 91.0, 88.0, 68.0])

# my_score higher than or equal to 85
print(my_score >= 85) ## [ True  True False False]
my_score_85 = my_score[my_score >= 85] ## Filtering my scores higher than or equal to 85
print(my_score_85)

# my_score lower than your_score
print(my_score < your_score) ## [False  True  True False]
my_lose = my_score[my_score < your_score] ## Filtering my_score lower than your_score
print(my_lose)
```

### 3.2 Boolean operators
Comparison operators와 마찬가지로 Boolean operators도 조건에 맞는 observation을 추출할 때 유용하게 사용할 수 있다. Boolean operators, and, or, not에 대해 알아보자. 

```python
# 'and' 조건 중 하나라도 False면 False를 return
print(True and True) ## T
print(True and False) ## F
print(False and True) ## F
print(False and False) ## F

# 'and' 조건 중 하나라도 True면 True를 return
print(True or True) ## T
print(True or False) ## T
print(False or True) ## T
print(False or False) ## F

# 'not' 해당 boolean에 역(inverse)을 취함
print(not True) ## F
print(not False) ## T

# boolean operations with numpy array
print(np.logical_or(my_score > 30.0, my_score < 70)) ## # np.logical_or(condition1, condition2, ...) : 해당 조건에 대해 'or' boolean operation 실행
print(np.logical_and(my_score > 70.0, my_score < 100)) ## np.logical_and(condition1, condition2, ...) : 해당 조건에 대해 'and' boolean operation 실행
```
### 3.3 Conditional statements
if, else, else if(elif)와 같은 조건문 또한 data fitering에 사용할 수 있는 유용한 도구이다. python에서 조건문 사용 방법을 알아보자. 

```python
score = 90
if score > 85 :
    print("High level")
elif area > 70 : 
    print("Medium level")
else :
    print("Low level")
```

### 3.4 Filtering Pandas DataFrame
지금까지 Numpy array나 하나의 variable를 대상으로한 filtering 방법을 알아보았다. 이제 좀 더 일반적인 상황인, Pandas DataFrame을 대상으로 한 filtering and selection 방법을 알아보자. 
```python
countries = ['Korea', 'Japan', 'China', 'Taiwan', 'Russia']
capitals = ['Seoul', 'Tokyo', 'Beijing', 'Taipei', 'Moscow']
pop = [51.46, 126.78, 13864, 23.49, 144.49]
have_triped = [True, True, False, True, False]
Dict = {'countries' : countries, 'capitals' : capitals, 'populations' : pop, 'triped' : have_triped} 

import pandas as pd
Infor = pd.DataFrame(Dict)
print(Infor) ## Keys가 col로 value가 row로 채워지는 것을 확인

row_labels = ['KR', 'JP', 'CHN', 'TPW', 'RUS'] ## 행 이름
Infor.index = row_labels ## 행 이름 바꾸기 
print(Infor)

triped = Infor['triped'] ## triped가 True인 것만 select
print(triped)
select = Infor[triped] ## Infor DataFrame에 triped가 True인 것만 select해서 select object에 저장
print(select) ## 확인 

# 위의 코드를 한 줄로 편집
select = Infor[Infor['triped']]
print(select)

# 백만 이상의 인구수를 가진 나라만 filtering
pop = Infor['populations']
many_pop = pop > 100

Huge_pop = Infor[many_pop]
print(Huge_pop)

# 한 줄로 정리
Huge_pop = Infor[Infor['populations'] > 100]
print(Huge_pop)

# 백만 이상, 오백만 이하의 인구수를 가진 나라만 filtering 
import numpy as np
between = np.logical_and(Infor['populations'] > 100, Infor['populations'] < 500) ## filtering option, between 선언
medium_pop = Infor[between]
print(medium_pop)

# 한줄로 정리
medium_pop = Infor[np.logical_and(Infor['populations'] > 100, Infor['populations'] < 500)]
print(medium_pop) ## 조건이 복잡해지는 경우 헷갈릴 수 있으므로 '조건'만 object로 저장해서 관리하는 것을 추천
```

## 4. Loops
### 4.1 While Loop
While loop는 빈번하게 사용하진 않지만 반복 계산이 필요한 경우, 유용하게 사용할 수 있다. While loop를 사용할 때 유의해야할 점은 '반드시 깨져야 하는 조건'을 만드는 것이다. 설정된 조건이 어느 시점에서도 깨지지 않는다면 While loop는 무한히 반복되므로 별다른 추가 옵션을 사용하지 않았다면 세션을 강제 종료하는 수 밖에 없기 때문이다. 
```python
# Initialize number
number = -10

# Code the while loop
while number != 0 :
    print("calculating...")
    if number > 0 :
      number = number - 1
    else : 
      number = number + 1    
    print(number)
```

### 4.2 For Loop
"For each variable in sequence, excute expression."의 한 문장으로 정리할 수 있는 For loop는 while보다 유연하게 사용할 수 있는 반복문이다. 그러나 For loop를 지나치게 사용한다면 코드가 복잡해질 뿐 아니라 처리 속도 또한 느려진다. 따라서 advanced level에서는 반복문 보다 좀 더 '멋진' 방법을 사용하는 것이 권장된다. 그러나 지금은 beginner level이므로 일단은 기본적인 사용에 익숙해지도록 하자. 
```python
my_score = [90.0, 85.3, 23.1, 68.5]
for index, score in enumerate(my_score) : ## enumerate()를 사용하면 (index, element)의 형태이므로 variable argument에 index, score 선언
    print(str(index+1)+"번째 시험 점수 "+": "+ str(score))
```
##### Bulit-in function enumerate()?
https://docs.python.org/3/library/functions.html#enumerate
반복 대상의 element가 위치한 index와 반복 대상의 element를 tuple형태로 return 해주는 function.

```python
Score = [['math', 90.0], ['history',85.3], ['english', 23.1], ['korean', 68.5]]
for name, score in Score : ## inner list의 자료 순서가 과목명, 점수이므로 name, score로 variable argument에 name, score 선언 
    print(str(name)+" test score "+": "+ str(score))
```

### 4.3 Looping Data Structures
지금까지 list와 단일 변수를 대상으로 한 반복문 사용에 대해 알아봤다. 그렇다면 Dictionary, nD array 그리고 Pandas DataFrame 자료형도 같은 방법으로 반복문을 실행시킬 수 있을까? 다르다면 무엇이 다를까? 

```python
# For loop with dictionary
Dict = {'Korea':'Seoul', 'Japan':'Tokyo', 'China':'Beijing', 'Taiwan':'Taipei', 'Russia':'Moscow'}
for countries, capitals in Dict.items() : ## dictionary.items() : dictionary object를 대상으로 곧장 for loop에 넣을 수 없다. 반드시 items() method를 사용할 것. 
    print("the capital of " + countries + " is " + str(capitals))
    
# For loop with Numpy array
import numpy as np
# 1D numpy array
my_score = np.array([90.0, 85.3, 23.1, 68.5])
for value in my_score : 
    print(str(value) +" point")

# 2D numpy array
my_score = np.array([90.0, 85.3, 23.1, 68.5])
your_score =  np.array([84.0, 91.0, 88.0, 68.0])
my_your_score = np.array([my_score, your_score])
print(my_your_score)
for value in np.nditer(my_your_score): ## numpy.nditer(2D numpy array) : 2D numpy array를 행 기준으로 나열해 반복문을 실행시킬 수 있게 한다. 
    print(str(value) +" point")

for value in my_your_score: 
    print(str(value) +" point") ## 비교해볼 것

# Pandas DataFrame
countries = ['Korea', 'Japan', 'China', 'Taiwan', 'Russia']
capitals = ['Seoul', 'Tokyo', 'Beijing', 'Taipei', 'Moscow']
pop = [51.46, 126.78, 13864, 23.49, 144.49]
have_triped = [True, True, False, True, False]
Dict = {'countries' : countries, 'capitals' : capitals, 'populations' : pop, 'triped' = have_triped} 

import pandas as pd
Infor = pd.DataFrame(Dict)
row_labels = ['KR', 'JP', 'CHN', 'TPW', 'RUS'] ## 행 이름
Infor.index = row_labels ## 행 이름 바꾸기 
print(Infor)

for label, row in Infor.iterrows() : 
    print(label) ## name of columns
    print(row) ## print out each row with Pandas.Series
    
for label, row in Infor.iterrows() : 
    print(str(label) + "'s populations : " + str(row['populations']))
    ## row['populations'] : 각 row에서 'populations'에 해당하는 element만 추출 

for label, row in Infor.iterrows() : 
    Infor.loc[label, "COUNTRIES"] = row["countries"].upper()
    ## row["countries"].upper() : 각 row에서 'countries'에 해당하는 element를 대문자로 변환 
    ## DF.loc[label, "COUNTRIES"] : COUNTRIES column을 생성하고 label 기준으로 .upper()결과를 저장
print(Infor) ## for loop 확인    

# apply : element-wise loop function
Infor["CAPITALS"] = Infor["capitals"].apply(str.upper)
## object.apply(function) : 해당 object의 element에 선언된 function을 적용시킨다. 
## apply function을 이용하면 반복문을 깔끔하게 정리할 수 있으므로 반드시 익혀두자.
print(Infor)
```

## 5. Case Study: Hacker Statistics
### 5.1 Random number generate
무작위 숫자를 만드는 것은 시뮬레이션에서는 빈번한 일이다. 그러나 잘못된 난수 생성은 시뮬레이션의 신뢰도에 영향을 미칠 수도 있기 때문에 확실히 짚고 넘어가자.

```python
import numpy as np

# Set the seed
np.random.seed(777)
print(np.random.rand())

# Use randint() to simulate a dice
print(np.random.randint(1,7)) 
print(np.random.randint(1,7)) ## numpy.random.randint(start,end) : start~end-1까지의 정수 중 임의의 정수 생성

# Dice and next step
step = 30 ## Initial step
dice = np.random.randint(1,7) ## Roll the dice

if dice <= 2 :
    step = step - 1
elif dice <= 5 :
    step = step + 1
else :
    step = step + np.random.randint(1,7) 
    
print(dice)
print(step)
```
```python
import numpy as np
np.random.seed(777)

# Initialize random_walk
random_walk = [0] ## start point

for x in range(100) :
    step = random_walk[-1] ## Set step: last element in random_walk
    dice = np.random.randint(1,7) ## # Roll the dice

    ## Determine next step
    if dice <= 2:
        ## step = step - 1
        ## zero에서 더 뒤로 갈 수는 없으므로 최소값을 0에 고정 
        step = max(0, step - 1)
    elif dice <= 5:
        step = step + 1
    else:
        step = step + np.random.randint(1,7)
        
    random_walk.append(step) ## append next_step to random_walk

print(random_walk) ## Print random_walk

import matplotlib.pyplot as plt 

plt.plot(random_walk) ## Plot random_walk
plt.show() ## Show the plot
```

```python
# 10번의 random walks을 반복해보자. 
all_walks = []
for i in range(10) :
   
    ## Code from before, random_walk
    random_walk = [0]
    for x in range(100) :
        step = random_walk[-1]
        dice = np.random.randint(1,7)

        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + np.random.randint(1,7)
        random_walk.append(step)

    ## Append random_walk to all_walks
    all_walks.append(random_walk)

print(all_walks) ## Print all_walks

np_aw = np.array(all_walks) ## Convert all_walks to Numpy array: np_aw

plt.plot(np_aw)
plt.show() ## check

plt.clf() ## Clear the wrong figure

np_aw_t = np.transpose(np_aw) ## Transepose np_aw
plt.plot(np_aw_t)
plt.show()
```
##### tranpose method로 plot이 바뀌는 이유?
https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
```python
print(np_aw_t)
print(np_aw)

print(np_aw_t.shape)
print(np_aw.shape)
```
위의 코드를 실행해보면 알겠지만 transpose method는 np.array의 행렬을 transpose하는 역할을 한다. transpose유무에 따라 바뀌는 plot형태로 미루어볼때,  plt.plot()로 그려지는 plot의 argument가 다음과 같은 구조를 갖고 있는게 아닌가 추측해볼 수 있다.
    (1) 그래프의 개수 = row의 개수 = number of variables
    (2) x축 = 시행횟수 = col 개수 = number of observations
    (3) y축 = step 크기 = value of elements

```python
# 500번의 random walk simulation
all_walks = []
for i in range(500) :
   
    ## Code from before, random_walk
    random_walk = [0]
    for x in range(100) :
        step = random_walk[-1]
        dice = np.random.randint(1,7)

        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step = step + 1
        else:
            step = step + np.random.randint(1,7)
        random_walk.append(step)

    ## Append random_walk to all_walks
    all_walks.append(random_walk)

np_aw = np.array(all_walks) ## Convert all_walks to Numpy array: np_aw
np_aw_t = np.transpose(np_aw) ## Transepose np_aw
ends = np_aw_t[-1,:] ## 마지막의 step만 ends에 저장 

plt.hist(ends) ## Q. 500번의 simulation에서 random_walk 결과들의 분포는 어떨까? 
plt.show() ## display plot
plt.clf()
```
