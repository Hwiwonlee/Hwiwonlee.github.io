# 1. Using iterators in PythonLand
## 1.1 Introduction to iterators
iterators를 iterables과 비교하면서 알아보자. 
- iterable : 반복 가능한 object를 말하며 list, dict, set, str, bytes, tuple, range, file connections 등이다.
- iterator : next()를 이용해 값을 차례대로 꺼낼 수 있는 object
자세한 내용은 아래 내용을 참고해서 공부해보자.
https://kkamikoon.tistory.com/91
https://wikidocs.net/16068

```python
# Iterating over iterables, str case
Demacia = ["Garen", "Lux", "Xin Zhao", "Jarvan IV"] ## List는 대표적인 iterable이다. 
for champ in Demacia: ## for exp를 이용한 iteration
    print(champ)

Demacia_champ = iter(Demacia) ## iter()를 이용해 iterable을 iterator로 변환 

## Print each item from the iterator
print(next(Demacia_champ))
print(next(Demacia_champ))
print(next(Demacia_champ))
print(next(Demacia_champ))

# Iterating over iterables, number case
small_number = iter(range(5)) ## iteration 생성 
print(next(small_number))
print(next(small_number))
print(next(small_number)) 
print(next(small_number)) 
print(next(small_number)) 
print(next(small_number)) ##error : StopIteration:, ranage를 초과하는 횟수의 iteration을 하는 경우 error

## iterable, range()를 이용한 iteration
for i in range(5) : 
    print(i)

# Iterators as function arguments
## iterators and iterables를 arguments로 갖는 대표적인 function : list(), sum()
## 사실, 이전에 다 해본 것들이지만 iterator와 iterable의 개념을 알았으니 iteration의 원리에 집중해서 코드를 짜보자. 

values = range(10,21)
values_list = list(values) ## iterables, range와 list
print(values)
print(values_list)

values_sum = sum(values)
values_sum_list = sum(values_list) ## sum()의 작동원리가 iteration에 기초하기 때문
print(values_sum)
print(values_sum_list) ## 두 결과가 같은 것을 확인 
```

## 1.2 Playing with iterators
iterator와 iterable를 argument로 가질 수 있는 대표적인 function, enumerate()와 zip()를 알아보자.
- enumerate(list) : argument로 선언된 list를 tuple로 바꿔준다. 이 때 list의 value 마다 index를 추가해 tuple로 바꿔주며 list의 value만큼의 tuple을 return한다. 
- zip(list, list) : argument로 선언된 두 개의 list에서 같은 index에 있는 value끼리 tuple로 만들어 return한다. 
 
```python
# Using enumerate
SKT_T1 = ['Quinn','Gragas', 'Ryze', 'Varus', 'Leona']
SKT_T1_list = list(enumerate(SKT_T1))
SKT_T1_tuple = tuple(enumerate(SKT_T1))
print(SKT_T1_list)
print(SKT_T1_tuple) ## enumerate class는 list와 tuple 가능하다. 

for index1, value1 in enumerate(SKT_T1):
    print(index1, value1)
##     
for index2, value2 in enumerate(SKT_T1, start = 1): ## start index를 '1'로 설정 
    print(index2, value2)

# Using zip
Champ = ['Quinn','Gragas', 'Ryze', 'Varus', 'Leona']
Position = ['Top', 'Jungle', 'Mid', 'ADC', 'Supporter']
Player = ['Khan', 'Clid', 'Faker', 'Teddy', 'Effort']

data_zip = zip(Champ, Position, Player)
data = list(zip(Champ, Position, Player))
print(data_zip)
print(data) ## zip class와 list로 바꾼 zip class의 비교 

for value1, value2, value3 in data_zip:
    print(value1, value2, value3)
    
for value1, value2, value3 in data:
    print(value1, value2, value3)
## 같은 결과가 나오는 것을 확인

# Using * and zip to 'unzip'
Position = ('Top', 'Jungle', 'Mid', 'ADC', 'Supporter')
Player = ('Khan', 'Clid', 'Faker', 'Teddy', 'Effort')

data1 = zip(Position, Player)
print(*data1) ## operator *를 이용한 unzip

data1 = zip(Position, Player)
result1, result2 = zip(*data1) ## zip()과 *를 이용한 unpacked 

print(result1 == Position)
print(result2 == Player) ## unpack된 결과인 result1와 result2가 원래의 tuple과 같은 것을 확인 
```

## 1.3 Using iterators to load large files into memory
대용량의 파일을 메모리로 가져올 때 iterator를 효과적으로 사용할 수 있다. 좀 더 구체적으로, Large data set을 가져올 때 'chucking'하는 작업에서 iterator를 사용할 수 있다. 'chucking'은 쉽게 '덩어리'로 이해하면 된다. 한번에 대용량의 파일 전체를 memory에 불러오면 memory performance를 떨어뜨릴 수도 있기 때문에 많은 경우 큰 용량의 file을 chuck로 분할시키는 chucking을 이용한다. chuck로 나누는 과정에서 순차적인 차례에 따를 때 iterator를 사용하게 된다. 아래의 예제를 통해 알아보자. 추가로 chuck의 개념과 특징에 대한 링크를 첨부한다. 
https://www.unidata.ucar.edu/blogs/developer/en/entry/chunking_data_why_it_matters

```python
# Processing large amounts of Twitter data

# Initialize an empty dictionary: counts_dict
counts_dict = dict()

# Iterate over the file chunk by chunk
for chunk in pd.read_csv('tweets.csv', chunksize = 10):

    # Iterate over the column in DataFrame
    for entry in chunk['lang']:
        if entry in counts_dict.keys():
            counts_dict[entry] += 1
        else:
            counts_dict[entry] = 1

# Print the populated dictionary
print(counts_dict)

# Define count_entries()
def count_entries(csv_file, c_size, colname):
    """Return a dictionary with counts of
    occurrences as value for each key."""
    
    # Initialize an empty dictionary: counts_dict
    counts_dict = {}

    # Iterate over the file chunk by chunk
    for chunk in pd.read_csv(csv_file, chunksize=c_size):

        # Iterate over the column in DataFrame
        for entry in chunk[colname]:
            if entry in counts_dict.keys():
                counts_dict[entry] += 1
            else:
                counts_dict[entry] = 1

    # Return counts_dict
    return counts_dict

# Call count_entries(): result_counts
result_counts = count_entries('tweets.csv', 10, 'lang')

# Print result_counts
print(result_counts)
```

# 2. List comprehensions and generators
## 2.1 List comprehensions
List comprehensions은 복잡한 구조로 이뤄졌지만 실제론 단순한 작업을 하는 loop code를 a single line으로 만들어주는 방법이다. single line code way들이 다 그렇지만 list comprehensions 또한 가독성과 효율성 사이의 trade off가 존재한다. 그렇지만 복잡한 구조를 갖는 loop code도 가독성에서는 그렇게 좋은 수준이 아니므로 list comprehensions를 익혀둔다면 script의 공간과 coding 시간에 있어서 좋은 효율을 가질 수 있게 될 것이다. 

```python
# Writing list comprehensions
## 1부터 10까지 제곱을 return하는 list comprehensions 만들기 
squares = [i ** 2 for i in range(1,11)]
## [output expression for iterator variable in iterable]

# Nested list comprehensions
## 10 by 10 matrix 만들기 
matrix = [[col for col in range(0, 10)] for row in range(0, 10)] 

for row in matrix:
    print(row)
```
위의 Nested list comprehension에 잠깐 주목해보자. 이전에 봤던 nested function처럼 python은 여러가지 nested 용법이 존재하며 nested list comprehension도 그 중 하나이다. nested list comprehension의 구조는 [[output expression for iterator variable in iterable] for iterator variable in iterable]과 같다. inner list comprehension은 일반적인 list comprehension과 같은 구조로 이뤄져 있다. outer list comprehension은 조금 다른 구조로 되어 있는데 inner list comprehension이 outer list comprehension의 output expression이라고 이해하면 된다. 즉, 예제의 nested list comprehension은 inner의 [0, 1, ..., 9]가 outer의 output expression되어 iterator variable, row로 저장되고 for loop와 range(0, 10)에 의해 10번 반복되는 것이다. 

## 2.2 Advanced comprehensions
좀 더 다양한 comprehension의 용법에 대해 알아보자. 더하여 comprehension이라는 도구는 list에만 국한되지 않고 다른 자료형에서도 사용할 수 있는데, 그 중 하나인 Dictionary comprehension에 대해서도 알아볼 것이다.

```python
# Using conditionals in comprehensions
Demacia = ["Garen", "Lux", "Xin Zhao", "Jarvan IV"]
condition_len = [champ for champ in Demacia if len(champ) >= 7] ## for loop와 if condition을 이용한 list comprehension
## [output expression for iterator variable in iterable condition expression]의 구조다. 

# Using if-else conditionals in comprehensions
new_condition_len = [champ if len(champ) >= 7 else ' ' for champ in Demacia]
## if만 사용했던 예제와 if-else를 사용한 지금의 예제의 차이점은 '조건'의 위치다.
## if-else를 사용한다면 condition이 output expression의 위치에 와야 한다. 
print(new_condition_len) 

# Dict comprehensions
Demacia = ["Garen", "Lux", "Xin Zhao", "Jarvan IV"]
Dict_len = {champ : len(champ) for champ in Demacia}
## Dict comprehension은 Key와 value가 필요하므로 ':'를 이용한 output expression이 반드시 정의되어야 한다.
print(Dict_len)
```

## 2.3 Introduction to generator expressions
Generator expression은 comprehension처럼 전체 value를 한번에 return하지 않고 한번에 하나씩 return시키는 generator를 만드는 방법이다. Generator expression는 메모리 관리에 장점이 있는 방법으로 session expire를 불러올 정도의 대용량처리를 할 때 유용하게 사용할 수 있다. 사용방법은 comrehension과 크게 다르지 않다. Generator function는 generator를 return하는 함수로 일반적인 함수의 형태처럼 'def'로 정의된다. Generator functions의 특징은 keyword yield 의해 generator를 생성한다는 점이며 yield call될 때마다 generator를 생성하므로 마찬가지로 메모리 관리에 장점을 갖는다. 
https://mingrammer.com/introduce-comprehension-of-python/#generator-expression-ge
http://pythonstudy.xyz/python/article/23-Iterator%EC%99%80-Generator

```python
# Write your own generator expressions
result = (num for num in range(31))
print(result) ## generator object
type(result) ## generator

print(next(result))
print(next(result))
print(next(result))

for value in result:
    print(value)
    
# Changing the output in generator expressions
Demacia = ["Garen", "Lux", "Xin Zhao", "Jarvan IV"]
lengths = (len(champ) for champ in Demacia) ## generator expression
type(lengths) ## generator 확인 

for length in lengths : 
    print(length)
    
# Build a generator using generator functions
def get_lengths(some_list):
    """Generator function that yields the
    length of the strings in input_list."""

    for name in some_list:
        yield(len(name)) # Use keyward Yield and yield the length of a string
        
for length in get_lengths(Demacia):
    print(length)
    
# Wrapping up comprehensions and generators.
# Extract the created_at column from df: tweet_time
tweet_time = df.created_at

# Extract the clock time: tweet_clock_time
tweet_clock_time = [entry[11:19] for entry in tweet_time]

# Print the extracted times
print(tweet_clock_time)

# Extract the created_at column from df: tweet_time
tweet_time = df.created_at

# Extract the clock time: tweet_clock_time
tweet_clock_time = [entry[11:19] for entry in tweet_time if entry[17:19] == '19']

# Print the extracted times
print(tweet_clock_time)
```

# 3. Bringing it all together! : Case study
