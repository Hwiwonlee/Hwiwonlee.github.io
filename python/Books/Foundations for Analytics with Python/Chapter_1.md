# 1. 파이썬 기초
## 1.1 파이썬 스크립트를 생성하는 방법
## 1.2 파이썬 스크립트 실행 방법
## 1.3 명렬 줄에서 유용한 팁 몇가지
```python
x = 4
y = 5
z = x + y
print("output #1 : {0:d}".format(z))

# {0:d}를 위한 예제
for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x)) ## x를 두자리, x^2를 세자리. x^3를 네자리로 print

## Q. 2d로 통일하면 두자리로만 나올까?
for x in range(1, 11):
    print('{0:2d} {1:2d} {2:2d}'.format(x, x*x, x*x*x))
## A. 돌려보면 알겠지만 nd에서 말하는 n자리는 해당 값이 할당될 공간이다. 쉽게 말해서 자릿 수에 따른 '줄맞춤'이라고 이해하면 편하다. 
        
a = [1,2,3,4]
b = ["first","second","third","fourth"]
c = a+b
print("output #2 : {0}, {1}, {2}".format(a,b,c))
print("output #3 : ",a,",",b,",",c) ## format없이 똑같은 결과를 내기 위한 code
```
https://docs.python.org/ko/3.8/tutorial/inputoutput.html

Print()를 이용할 때 str.format() method를 이용하는 것이 눈에 띈다. Data camp나 Jump to Python의 방법과는 또 다르다. 위의 링크와 구글링을 통해 확인한 바, f-string이 나옴으로 인해 str.format()이 구버전이 되었지만 복잡한 문자열을 처리할 때 오타를 방지한다는 측면은 꽤 괜찮은 장점으로 보인다. 그러나 여전히 문자열의 길이가 늘어나고 문자열 안에 포함될 변수들이 많아지는 경우 이용이 복잡하다는 단점은 존재하는 것 같다. 

## 1.4 파이썬 기본 구성 요소
### 1.4.1 숫자
```python
a = 38819/float(3)
print("output #4 : {0:2f}".format(a))
print("output #5 : {0:4f}".format(a))
## 책 내용대로라면 각각 소수점 아래 두자리, 네자리까지 print되어야 하는데 아니네?
```
### 1.4.2 문자열
```python
print("output #6 : {0:s}".format('Python is an interpreted, high-level, general-purpose programming language.'))
sentence = "Python is"
print(f'output #7 : {sentence} an interpreted, high-level, general-purpose programming language.') ## f-string을 이용한 print
print("output #8 : {0:s}".format("""Python is an interpreted, high-level, general-purpose programming language.
Created by Guido van Rossum and first released in 1991,
Python's design philosophy emphasizes code readability with its notable use of significant whitespace.""")) 
## 책에는 '\'로 줄 띄어쓰기를 했는데 에러 나서 """로 그냥 해봄.
print("output #9 : {0:s}".format('''Python is an interpreted, high-level, general-purpose programming language.
Created by Guido van Rossum and first released in 1991,
Python's design philosophy emphasizes code readability with its notable use of significant whitespace.''')) 
## output #9와 같은 결과 

# split(기준, n번 분할) : 선언된 argument에 따라 string을 분할, List로 return시키는 method 
sentence = "Python is an interpreted, high-level, general-purpose programming language"
sentence_1 = sentence.split() ## default setting : '공백'을 기준으로 최대한 분할 
sentence_2 = sentence.split(" ", 2) ## 공백을 기준으로 2번 분할 
sentence_3 = sentence.split("i") ## String i를 기준으로 최대한 분할
print("output #10 : {0}".format(sentence_1))
print("output #11 : First Part:{0}, Second Part:{1}, Third Part:{2}".format(sentence_2[0], sentence_2[1], sentence_2[2]))
print("output #12 : First Part:{0}, Second Part:{1}, Third Part:{2}, Fourth Part:{3}, Fifth Part:{4}"
.format(sentence_3[0], sentence_3[1], sentence_3[2], sentence_3[3], sentence_3[4]))

# join() : str.join(object)로 사용, 선언된 str를 기준으로 list의 element를 join시켜서 return시키는 method
print("output # 13 : {0}".format(" ".join(sentence_1)))

# object.strip(str) : 선언된 str를 object에서 삭제한 후 return
sen = "++Python is an interpreted, high-level, general-purpose programming language--"
print("output #14 : {0}".format(sen.strip("+-")))

# object.replace(str1, str2) : 선언된 str1를 str2로 교체시킨 후 return
print("output #15 : {0}".format(sen.replace("+", "-")))

# object.lower, upper, capitalize() : object의 str를 각각 소문자, 대문자, 첫 글자 대문자로 변환시키는 method
print("output #16 : {0}".format(sentence.lower()))
print("output #17 : {0}".format(sentence.upper()))
print("output #18 : {0}".format(sentence.capitalize()))
```
### 1.4.3 정규표현식(Regular expression)
보통 '정규표현식'은 후반에 나오는데 이 책은 놀랍게도 초반에 나와서 초보자들의 멘탈을 공격하고 있다. 데이터 분석에서 정규표현식은 자료의 패턴을 찾는데 사용되곤 하는데, 정규표현식 자체가 그렇게 사용자 친화적이지 않기 때문에 진입장벽이 있다. 그렇지만 나온 김에 짚고 넘어가자. 
```python
python_wiki = """Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.[27]Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. Python is often described as a "batteries included" language due to its comprehensive standard library.[28] Python was conceived in the late 1980s as a successor to the ABC language. Python 2.0, released in 2000, introduced features like list comprehensions and a garbage collection system capable of collecting reference cycles. Python 3.0, released in 2008, was a major revision of the language that is not completely backward-compatible, and much Python 2 code does not run unmodified on Python 3. Due to concern about the amount of code written for Python 2, support for Python 2.7 (the last release in the 2.x series) was extended to 2020. Language developer Guido van Rossum shouldered sole responsibility for the project until July 2018 but now shares his leadership as a member of a five-person steering council.[29][30][31]The Python 2 language, i.e. Python 2.7.x, is "sunsetting" on January 1, 2020, and the Python team of volunteers will not fix security issues, or improve it in other ways after that date.[32][33] With the end-of-life, only Python 3.5.x and later will be supported.[citation needed]Python interpreters are available for many operating systems. A global community of programmers develops and maintains CPython, an open source[34] reference implementation. A non-profit organization, the Python Software Foundation, manages and directs resources for Python and CPython development."""

# python_wiki에서 일정한 패턴 찾기 
import re ## re module을 import
python_wiki_list = python_wiki.split() ## python_wiki를 공백 기준으로 split
pattern = re.compile(r"Python", re.I) 
## compile() function : 텍스트 기반의 패턴을 정규표현식으로 컴파일
### r"Python" : 'raw string'임을 의미하는 'r'을 사용
### re.I function : 컴파일에서 선언된 텍스트 기반의 패턴에서 대소문자를 무시하도록 함. 
### Q. raw string은 뭐지?
count = 0
for x in python_wiki_list:
    if pattern.search(x): ## object.search(var) : re module에 속한 object.search method() 해당 object가 var가 포함되어 있는지 check 
        count += 1 ## if의 조건을 만족한다면 count에 1을 더한다. 
print("Output #19 : {0:d}".format(count))  

# 문자열 내에서 발견된 패턴 출력하기
pattern = re.compile(r"(?P<match_word>Python)", re.I)
## 일치하는 문자열을 출력하기 위한 (?P<그룹 이름>찾을 패턴) : 메타 문자
print("Output #20:")
for x in python_wiki_list:
    if pattern.search(x):
        print("{:s}".format(pattern.search(x).group('match_word')))
        ## 결과가 True라면 pattern.search(x)의 자료구조에서.group('match_word')로 match_word 그룹의 값을 가져온 후 그 값 = 찾을 패턴 = Python을 출력한다
        
# 문자열 내 "Python"을 "파이썬"으로 대체하기
string_check = r"Python"
pattern = re.compile(string_check, re.I)
print("Output #21: {:s}".format(pattern.sub("파이썬", python_wiki)))
## pattern.sub(str. object) method : object를 대상으로 pattern에 일치하는 부분을 찾아 str으로 대체함. 
```

### 1.4.4 날짜
날짜 data는 특정 자료형을 갖지는 않지만 실제 분석에서 빈번하게 사용되는 변수 중 하나이다. '초'까지 포함한 세세한 형태를 갖고 있기도 하며 문자와 숫자가 결합된 형태를 갖고 있는 경우도 있어 어떤 식으로든 전처리가 필요한 data이다. 이제 날짜를 어떻게 다뤄야 하는지 알아보자. 
```python
from math import exp, log, sqrt
import re
from datetime import date, time, datetime, timedelta
## datetime은 날짜 data를 다루기 용이한 module이다. 

# '오늘'을 가져오는 두가지 방법
today = date.today() ## date.today() : 년-월-일의 날짜 형태
print("Output #22: today : {0!s}".format(today)) ## {0!s} : print의 arument가 숫자여도 string으로 바꿔서 return
print("Output #23: today : {0!s}".format(today.year))
print("Output #24: today : {0!s}".format(today.month))
print("Output #25: today : {0!s}".format(today.day))
datetime = datetime.today() ## datetime.today() : 년-월-일 시:분:초
print("Output #26: {0!s}".format(datetime))

# timedelta를 이용한 날짜 계산
day = timedelta(days=+1)
tomorrow = today + day
print("Output #27: tomorrow : {0!s}".format(tomorrow))
yesterday = today - day
print("Output #28: a : {0!s}".format(yesterday))

h_30 = timedelta(hours=+25)
h_10 = timedelta(hours=+10)
print("Output #29: {0!s} {1!s}".format(h_30.days, h_30.seconds))
print("Output #30: {0!s} {1!s}".format(h_10.days, h_10.seconds))
```
결과를 보면 timdelta의 결과는 조금 낯선 형태로 return됨을 알 수 있다. 결과를 다시 써보면 Output #28: 1일 3600초, Output #29: 0일 36000초가 된다. timedelta() function의 결과값은 일과 초를 기준으로 정규화되어 있기 때문에 이와 같으며 만약 'timedelta(hours=-30)'이라면 -1일 3600초가 된다. 
```python
print(today.strftime) ## built-in method strftime of datetime.date object

print("Output #31: {:s}".format(today.strftime('%m/%d/%y')))
print("Output #32: {:s}".format(today.strftime('%m, %d, %Y')))
print("Output #33: {:s}".format(today.strftime('%y-%m-%d')))
print("Output #34: {:s}".format(today.strftime('%B %d %y')))
print("Output #35: {:s}".format(today.strftime('%b %D %Y')))
```
예제 코드에서 사용한 %m, %d, %y 등은 format specifier(형식 지정자 혹은 서식 지정자)로 formatting에서 사용되는 방법이다. '%'뒤에 어떤 문자가 오고 경우에 따라선 대소문자에 따라 기능의 차이가 있기 때문에(%y와 %Y의 결과를 보면 알 수 있다.) 모든 format specifier를 외우는 것은 조금 피곤한 일이다. 그러므로 format specifier를 이용한 formatting이 있다는 사실과 대략적인 개념만 알아두자. datetime module에서 사용할 수 있는 format specifier에 궁금하다면 아래의 링크를 참고하자. 
https://docs.python.org/3/library/datetime.html


### 1.4.5 List
List는 python에서 자주 등장하는 자료형 중 하나다. 실제로 데이터 분석에서도 빈번하게 마주칠 수 있다니 잘 익혀두는 것이 좋을 것이다. 기본적인 개념은 제외한 책의 예제 몇가지를 보자. 

```python
# sorted()와 lambda function을 이용한 리스트 정렬
a = [[1,3,5,7], [2,4,6,8], [8,2,5,0]]
a_sorted_by_index_1 = sorted(a, key = lambda index : index[1])
print("Outpu #36 : {}".format(a_sorted_by_index_1))

print(sorted("This is a test string from Andrew".split(), key=str.lower))
a = "This is a test string from Andrew"
b = a.split()
print(sorted(b, key = str.lower))

student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
sorted(student_tuples, key=lambda student: student[2])   # sort by age
```
예제 코드에서 첫번째 sorted code는 책의 예제, 두번째, 세번째 sorted code는 docs.python.org에서 가져온 예제다. sorted() 에서 가장 이해가 안되는 부분은 parameter key다. 이해가 안되는 내용은 아래와 같다 

- Q1 .lambda fucntion에서 argument를 index로 정의하고 exp를 index[1]로 정의했다. 그렇다면 list a의 두번째 index의 값을 기준으로 정렬하라는 의미인데 nested list인 list a에서 a[1]인지, a[n][1]인지 sorted()가 어떻게 판단하는가?
- Q2. 두번째 예제에서 key의 arument로 str.lower를 주었다. 이는 sorted()에 정의된 key 중 하나인가? 

사실 두번째 질문은 코드가 그렇게 실행되니까라고 생각하고 넘길 수 있겠는데 첫번째 질문은 쉽게 이해가 안된다. 이 글을 쓰다가 적절한 실험 예제를 생각해냈다. 
```python
# sorted()의 key parameter의 작동원리
a = [1,3,5,7, 2,4,6,8, 8,2,5,0]
a_sorted_by_index_1 = sorted(a, key = lambda index : index[1]) ## error
a_sorted_by_index_1 = sorted(a, key = lambda index : index)
print(a_sorted_by_index_1)

b = [[[1,3],[5,7]], [[2,4],[6,8]], [[8,2],[5,0]]]
b_sorted_by_index_1 = sorted(b, key = lambda index : index[1][1]) ## error

c = [[[1,3,6,6],[5,7,2,3]], [[2,4,1,1],[6,8,0,9]], [[8,2,1,2],[5,0,2,2]]]
c_sorted_by_index_2 = sorted(c, key = lambda index : index[2]) ## list index out of range
c_sorted_by_index_1 = sorted(c, key = lambda index : index[1])
c_sorted_by_index_12 = sorted(c, key = lambda index : index[1][2])
print(c_sorted_by_index_1)
print(c_sorted_by_index_12)
```
docs.python.org에 따르면 sorted의 key는 하나의 인자를 받는 함수를 지정하는데, iterable의 각 요소들로부터 비교 키를 추출하는 데 사용된다고 한다. 위의 코드를 통해 선언된 key argument가 어떻게 indexing돼서 정렬에 이용되는지 실험해보았다. Q1.과 코드의 결과를 보면 알겠지만 key에 적용된 argument는 sorted의 대상되는 iterable의 한단계 안에서 실행된다. 쉽게 말해 a = [[1,3,5,7], [2,4,6,8], [8,2,5,0]]을 sorted의 iterable로 선언한다면 sorted 내부에서 [1,3,5,7], [2,4,6,8], [8,2,5,0]로 정의되고 sorted()에서 함께 선언된 key = index[1]에 의해 정렬될 수 있게 되는 것이다. 
Q. 까지 적었는데 lambda function에 의한 진행일 수도 있다는 생각이 들었다. 이건 어떻게 실험해보면 될까?
```python
# itmegetter()와 sorted()를 이용한 정렬
from operator import itemgetter
a = [[111,1,2,32], [91,20,1,23],[39102,7,65,1], [290,101,6,1], [1,2,3,4], [6,5,11,92031]]
a_sorted_itemgetter = sorted(a, key = itemgetter(2,1)) ## 3번째 index의 value에 의해 정렬한 후 2번째 index의 value에 의해 정렬하라
print(a_sorted_itemgetter)
```

### 1.4.6 Tuple
Tuple은 리스트와 비슷한 형태로 저장되는 자료형이지만 '직접적으로 수정할 수 없다'는 차이점이 있다. 리스트와 더불어 데이터 분석 과정에서 자주 볼 수 있는 자료형이다. 

### 1.4.7 Dictionary
Dictionary는 key:value 형태로 정의되는 자료형이다. 마찬가지로 많이 쓰이는 형태 중 하나이다. 
```python
# items() method와 sorted()를 이용한 dictionary의 정렬
## dictionary는 기본적으로 순서가 존재하지 않지만 sorted를 이용하면 순서대로 정렬시킬 수 있다.
dict0 = {'a':3, 'b':2, 'c':1}
dict0_ordered_by_key = sorted(dict0.items(), key = lambda item : item[0]) ## 
dict0_ordered_by_value = sorted(dict0.items(), key = lambda item : item[1])
print(dict1)
print(dict2)
```

### 1.4.8 Control flow(제어흐름)
Control flow는 논리구조를 넣기 위한 도구다. 말은 어렵지만 이미 알고 있는 반복문(for, while loop), 조건문(if-elif-else) 등이며 추가적으로 반복문을 간단하게 이용할 수 있는 list, set, dictionary comprehension등 또한 control flow에 속한다. 

### 1.4.9 User-defined function
### 1.4.10 try-except
try-except의 예외처리는 어쩌면 당연히 존재하는 error을 대응하기 위한 방법이다. try-except 말고도 try-except-else-finally의 구조도 가능하다. 
```python
def getMean(values) : 
    return sum(values)/len(values)

list0 = []

try :
    result = getMean(list0)
except ZeroDivisionError as detail:
    print("(error) : {}".format(float('nan')))
    print("(error) : {}".format(detail))
else : 
    print("(result): {}".format(result))
finally:
    print("(finally): The finally block is executed every time")
```
먼저 try가 실행되고 try 단계에서 오류가 발생하면 except의 expression들이 실행된다. 만약 try 단계에서 오류가 발생하지 않으면 else의 expression이 실행된다. try 단계의 오류발생 유무와 무관하게 마지막엔 finally 단계가 실행된다. 
