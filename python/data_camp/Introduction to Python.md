# 1. Python Basics
PASS

# 2. Python Lists
## 2.1 Problem
일반적으로 우리는 단 하나의 변수(A variable)가 아닌 변수들(Variables)을 다루게 된다. 따라서 여러 개의 변수를 가질 수 있는 data type이 필요한데, 지금 살펴볼 "List"가 그 중 하나이다. 

```python
fruits1 = ["apple", 3, "ananas", 1, "banana", 5, "grape", 2]
apple = 3
ananas = 1
banana = 5
grape = 2
fruits2 = ["apple", apple, "ananas", ananas, "banana", banana, "grape", grape] ## 변수로 list를 만들 수도 있음
fruits1 == fruits2 ## True
fruits = fruits1

# Lists in the list
List_fruits = [["apple", 3], ["ananas", 1], ["banana", 5], ["grape", 2]]

# Zero Indexing 
fruits[0] ## '0'번째 element를 call하면 1번째 element가 call됨
fruits[1] ## '1'번째 element를 call하면 2번째 element가 call됨

# Indexing
fruits[1] - fruits[-1] # 3 - 2 = 1
fruits[-1] ## -index도 가능 
List_fruits[0]
List_fruits[0][0] 
List_fruits[0][1] ## 리스트 안에 리스트가 있는 경우 몇 겹의 리스트로 감싸고 있는지에 따라 indexing calling이 늘어난다

# Slicing and dicing
""" 
Slicing : list[start:end]
해당 list에서 (start)번째부터 (end-1)번째까지의 elemnent를 call
start의 value가 없는 경우는 '처음부터'
end의 value가 없는 경우는 '끝까지'
"""
Like_fruits = fruits[:4]
Hate_fruits = fruits[4:]
## 같은 결과 
Like_fruits = fruits[0:4] 
Hate_fruits = fruits[4:8]

# Replace list elements
fruits[2] = "pine apple"
fruits

# Delete list elements
del(fruits[2:4]) ## Pine apple 삭제 

# Copy list 
"""
Python에서는 R처럼 A = B로 object를 복사하면 큰일난다. 
fruits_A = fruits
fruits_A = list(fruits)
fruits_B = fruits_A
del(fruits_A[0:2])
print(fruits_A) 
print(fruits_B) 
## 바꾼 건 fruits_A인데 fruits_B까지 바뀌었음을 볼 수 있다. 
## Python에서는 A = B를 commit하면 object는 그대로이고 "이름"만 추가되기 때문
## 즉, 기존에는 "A"로 call할 수 있었던 object를 "B"로도 call할 수 있게 될 뿐, 독립된 object를 갖는 것은 아니다.
"""
fruits_copy = list(fruits)
del(fruits_copy[0:2])
print(fruits)
print(fruits_copy)
```


# 3. Functions and Packages
Python에는 수많은 bulit-in function과 package들이 존재하므로 모든 function을 외워 쓴다는 건 불가능에 가깝다. 억지로 외우지 않아도 자주 쓰는 function은 손에 익으며 필요에 맞게 그때그때 package와 function을 찾아쓰는 것이 정신건강에 이롭다.

## 3.1 Function
Function이란 object가 '정의된 performance'를 수행하도록 하는 연산문의 집합이다. 목적과 필요에 따라 이미 정의된 많은 function들이 존재하고 있으며 사용자 본인의 목적에 맞게 수정하거나 새로 정의할 수도 있다. 
```python
"""
help(fucntion name) : 해당 fucntion의 도움말

print() : value 출력 
type() : variable의 유형 출력 
len() : list의 길이 출력 

str() # string으로 변환 
int() # integer로 변환 
bool() # boolean으로 변환 
float() # floate로 변환 
"""
# sorted() example
part1 = [8,5,3,4]
part2 = [1,6,7,2]
part = part1 + part2
part_sorted_R = sorted(part, reverse = True) ## reverse argument : 역순여부 
part_sorted = sorted(part, reverse = False)

print(part_sorted_R)
print(part_sorted)
```

## 3.2 Method
'method'는 function와 마찬가지로 '정의된 performance'를 수행하게 하지만 사용 방법이 다르므로 구분해서 배워두는 것이 이해하기 좋다. 
method는 object에 속해있다는 점에서 function과 차이를 갖는다. 왜 method가 object에 속해있다고 정의되는지 아래 예제를 통해 알아보자. 
```python
"""
method 사용법
object.method(parameters) 
"""
Like_one = "apple"
print(Like_one.upper()) ## method upper() : str을 대문자로 변환
print(Like_one.count('p')) ## method count() : commit된 argument와 같은 값이 object에 몇 번 나오는지 return

Numbers = [1,3,3,5,7,9,11]
print(Numbers.index(5)) ## method index() : commit된 argument와 같은 값의 index를 return
print(Numbers.count(3)) ## method count() : commit된 argument와 같은 값이 object에 몇 번 나오는지 return
Numbers.append(13) ## method append() : commit된 arg와 같은 값을 object 맨 끝에 추가 
Numbers.append(100)
print(Numbers)
Numbers.remove(100) ## method remove() : commit된 arg와 같은 값 하나를 object의 가장 앞쪽에서부터 삭제
Numbers.reverse() ## method reverse() : object 안의 value를 거꾸로 정렬(크기를 고려하지 않음)
print(Numbers)
```
## 3.3 Package
Python을 사용한다면 많은 수의 function과 method를 사용하게 된다. project가 쌓이고 쌓일수록 더 많은 function과 method를 이용할 수 밖에 없으며 이렇게 만들어진 혹은 사용한 fucntion과 method를 각각 관리한다는 것은 어불성설이다. 따라서 목적과 쓰임에 맞춰 function과 method를 모아놓고 관리하기 쉽게 하나의 형태로 만든 것이 package이다. package는 "Directory of Python scripts"로 정의할 수도 있는데, 이 때 각각의 script를 'module'이라 부른다. 말이 중구난방한데, module이란 package 안의 script로 '특정 목적에 맞게 정의된 function, method, type 등'을 통칭하는 말이다.  

```python
import math as mt ## 'math' package를 import하고 이름을 mt로 바꿈 
r = 0.32
Cir = 2 * mt.pi * r ## package.name, mt.pi : 원주율, 3.141592.....
Area = mt.pi * r ** 2
print("원둘레: " + str(Cir))
print("원넓이: " + str(Area))

# 선택적 import
import math ## math를 먼저 import
from math import radians # math로부터 radians를 import
radians(360) # math로 부터 function radians()를 가져와서 사용
````

# 4. NumPy
List는 많은 이점을 가지고 있지만 '연산이 불가능하다'는 단점 때문에 data science 측면에서는 사용하기 어렵다. List의 단점을 해결한 것이 Numpy package의 array()이다. numpy.array()를 사용하면 기존의 list를 연산 가능한 list로 변환되어 손쉽게 이용할 수 있다. 

```python
# Numpy example
Score = [10, 2, 8, 9, 5.5, 3]

import numpy as np ## numpy package를 import하고 이름을 np로 변환 
np_Score = np.array(Score)
print(type(np_Score)) ## <class 'numpy.ndarray'> 
print(type(Score)) ## <class 'list'>

# Height, weight and BMI
H = [182, 165, 175, 160, 180, 155]
W = [90, 50, 73, 42, 100, 45]
np_H = np.array(H)
np_W = np.array(W)
bmi = np_W / (np_H/100) ** 2
print(bmi)

light_W = np_W < 50 ## 논리연산 결과를 light_W에 저장, 50미만의 weight를 가지면 'True' 50 이상의 weight를 가지면 False
print(light_W)
print(bmi[light_W]) ## True자리의 bmi만 print됨을 볼 수 있다. 
"""
boolean 결과를 이용한 indexing은 자주 볼 수 있는 extract method 중 하나이다. 
"""

# Numpy's side effect
np.array([True, 2, 3]) + np.array([3, 4, False]) ## array([4,6,3]) : True가 '1'의 값을 갖고 False가 '0'의 값을 갖기 때문이다. 
```
## 4.1 Similariry between Numpy Arrays and lists
Numpy Arrays는 연산 가능 여부에 있어서 list와 차이를 갖는다. 그러나 Numpy Arrays를 다루는 방법은 기존의 list와 크게 다를 바 없다. 이 점은 Numpy arrays의 장점 중 하나이다. 
```python
np_W[2:6]
np_W[:6]
np_H[-3:-1]
np_H[3:]
```
## 4.2 2D Numpy Arrays
쉽게 설명하면 "행렬"이다. 즉 행과 열의 2차원을 갖는 Numpy Arrays를 2D(Dimension) Numpy Arrays이라 정의한다. 

```python
# np_W와 np_H를 이용해 2D numpy arrays 만들기
np_2D = np.array([np_W, np_H])
np_2D.shape ## (2, 6) 확인 
print(np_2D) ## 2 by 6 형태

# Subsetting 2D NumPy Arrays
"""
2D_numpy_arrays[(row section), (col section)]
각 section에서의 subsetting은 마찬가지로 ':'을 이용한다.  
"""
np_2D[0,:] ## 1행 
np_2D[1,:] ## 2행
np_2D[, 2:4] ## error
np_2D[:, 2:4] ## 1행과 2행에서 3,4열만 출력
np_2D[1, 2:] ## 2행에서 3~6열 출력

# 2D Numpy arrays의 연산
"""
Numpy arrays와 마찬가지로 2D Numpy arrays의 연산 또한 'element-wise'(즉, element와 element끼리 연산함)의 규칙을 따른다. 
"""
np_a = np.array([[1, 2], [3, 4], [5, 6]])
print(np_a)
print(np_a.shape)
np_a + np.array([10, 10])
np_a * np.array([3, 5])
```
## 4.3 Basic Statistic using Numpy
'연산가능한 list'를 만드는 Numpy arrays function도 유용하지만 Numpy package 안에는 통계 분석에 기초적인 여러 함수들이 포함되어 있다. 

```python
print(np.mean(np_W)) ## mean() in Numpy
print(np.median(np_H)) ## median() in Numpy
print(np.std(np_H)) ## std() in Numpy, std means Standard deviation
print(np.corrcoef(np_W, np_H)) ## corrcoef() in Numpy, corrcoef means Correlation coefficient
```
