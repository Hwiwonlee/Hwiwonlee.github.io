# 1. Writing your own functions
## 1.1 User-defined functions
앞서 봤던 function들은 다른 사람들이 특정 목적을 위해 만들어놓은 것들이다. 그렇다면 내가 다뤄야할 문제들에 대한 function이 존재하지 않는다면 어떻게 해야할까? Python에서는 사용자 스스로 자신의 함수를 build up 할 수 있다.
```Python
# Simple example for user-defined functions
def python_is():
    """Print a string with three exclamation marks"""
    ## Concatenate the strings: python_def
    python_def = 'Python is an interpreted, high-level, general-purpose programming language' + '!!!'    
    
    print(python_def) ## Print python_def

python_is() ## Call python_is

# Modify to Single-parameter function
def python_is(some_word): ## some_word is paramter
    ## Concatenate the strings: python_def
    python_def = some_word + '!!!'
   
    print(python_def) ## Print python_def

python_is('Python is an interpreted, high-level, general-purpose programming language')
## 'Python is..' is argument

# Next step, modfify to function that return single value
def python_is(some_word): ## some_word is paramter
    ## Concatenate the strings: python_def
    python_def = some_word + '!!!'
   
    return(python_def) ## return python_def

## Pass 'Python is...' to python_is: value
value = python_is('Python is an interpreted, high-level, general-purpose programming language')

print(value) ## print value and check
```
function을 정의할 때 최종 결과에 return()을 사용하는 것을 권장한다. 왜냐하면 user-defined function 내부에 return()으로 결과가 정의되어야 function defining 작업이 끝났다고 python script에서 판단하기 때문이다. 사용자 입장에서 function의 결과를 object로 저장하는 것으로 끝낼 수 있다고 생각할 수 있고 실제로 return()을 사용하지 않아도 오류가 나진 않는다. 그러나 return()으로 함수를 닫지 않으면 함수 정의 이후로 계속 들여쓰기가 적용되어 귀찮기도 하거니와 python script 상에서 들여쓰기가 차지하는 문법적 비중이 상당히 크므로 함수를 만들 때 return()을 사용하는 것이 모두를 위해 좋다.
```python
# Function with multiple parameters
def python_is(some_str1, some_str2): ## some_str1 and some_str2 are paramters
    ## Concatenate some_str1 with '!!!': str1
    str1 = some_str1 + '!!!'
    ## Concatenate some_str2 with '!!!': str2
    str2 = some_str2 + '!!!'
    
    str_sum = str1 + "\n" + str2
    return(str_sum) ## return str_sum

## Pass 'Python is...' and 'Created...' to python_is: value
## 'Python is...' and 'Created...' are argumets
value = python_is('Python is an interpreted, high-level, general-purpose programming language', 
'Created by Guido van Rossum and first released in 1991')

print(value) ## print value and check
```

## 1.2 A brief introduction to tuples
튜플(tuple)은 리스트와 비슷한 자료형이지만 '저장된 value를 직접적으로 바꿀 수 없다'는 차이점을 갖는다. 이 특징은 튜플의 정체성과 같은 것이라 리스트와 튜플을 올바르게 다루기 위해서 반드시 알아두어야 한다. 
```python
# A brief introduction to tuples
nums = 3,4,6 ## nums is the tuple
nums[0] = 2 ## TypeError : 'tuple' object does not support item assignment

num1 = nums[0]
num2 = nums[1]
num3 = nums[2]

# Construct even_nums
even_nums = 2, num2, num3
print(even_nums)
type(even_nums) ## even_nums is the tuple
```
```python
# Update function using tuple
def python_is(some_str1, some_str2): 
    str1 = some_str1 + '!!!'
    str2 = some_str2 + '!!!'
    
    str1_str2 = (str1, str2) ## Construct a tuple with str1 and str2: str1_str2
    return(str1_str2) ## return str1_str2

## Pass 'Python is...' and 'Created...' to python_is(): value1, value2
## Unpacked a tuple, str1_str2
value1, value2 = python_is('Python is an interpreted, high-level, general-purpose programming language', 
'Created by Guido van Rossum and first released in 1991')

print(value1) ## print value1 and check
print(value2) ## print value2 and check
```
## 1.3 Bringing it all together
csv를 이용한 예제인데, raw data를 구할 때까지는 data camp의 내용을 써야겠다. 
```python
# Import pandas
import pandas as pd

# Import Twitter data as DataFrame: df
df = pd.read_csv("tweets.csv")

# Initialize an empty dictionary: langs_count
langs_count = {}

# Extract column from DataFrame: col
col = df['lang']

# Iterate over lang column in DataFrame
for entry in col:

    # If the language is in langs_count, add 1 
    if entry in langs_count.keys():
        langs_count[entry] += 1
    # Else add the language to langs_count, set the value to 1
    else:
        langs_count[entry] = 1

# Print the populated dictionary
print(langs_count)

# Define count_entries()
def count_entries(df, col_name):
    """Return a dictionary with counts of 
    occurrences as value for each key."""

    # Initialize an empty dictionary: langs_count
    langs_count = {}
    
    # Extract column from DataFrame: col
    col = df[col_name]
    
    # Iterate over lang column in DataFrame
    for entry in col:

        # If the language is in langs_count, add 1
        if entry in langs_count.keys():
            langs_count[entry] += 1
        # Else add the language to langs_count, set the value to 1
        else:
            langs_count[entry] = 1

    # Return the langs_count dictionary
    return langs_count

# Call count_entries(): result
result = count_entries(tweets_df, 'lang')

# Print the result
print(result)
```
# 2. Default arguments, variable-length arguments and scope
## 2.1 Scope and user-defined functions
python에서 Scope는 3개의 구분으로 나뉜다. 
    1) global scope : defined in the main body of a script
    2) local scope : defined inside a function 
    3) bulit-in scope : names in the pre-defined built-ins module
3) bulit-in scope는 거의 사용할 일이 없으므로 2.1에서 다룰 내용은 1) global scope와 2) local scope에 집중되어 있다. global와 local을 구분해서 함수를 정의하는 것은 object나 variable 관리에 있어서 매우 중요하므로 위 개념을 예제로 익혀보자. 
```python
# Create a string: nation
nation = "Demacia"

# Define change_nation()
def change_nation():
    """Change the value of the global variable nation."""

    global nation ## Use nation in global scope
    
    nation = "noxus" # Change the value of nation in global: nation
    
print(nation) ## Print nation

change_nation() ## Call change_nation()
print(nation) ## # Print nation
```

## 2.2 Nested functions
'Nested'란 겹겹이 둘러 싸인 형태를 말할 때 사용하곤 한다. Nested functions이란 'function A'안에 'function A''가 있는 구조를 의미한다. 복잡한 작업을 하기 위한 function을 build-up할 때 중요한 작업들을 function의 각 부분으로 나누고 function안의 function으로 정의함으로써 가독성을 높히고 오류도 줄이는 효과를 기대할 수 있기 때문에 많이 사용된다. 실제로 module에 속한 대부분의 function은 Nested function임을 볼 수 있다.

```python
# Define three_shouts
def str_three(str1, str2, str3):
    """Returns a tuple of strings
    concatenated with '!!!'."""

    # Define inner
    def inner(str0):
        """Returns a string concatenated with '!!!'."""
        return str0 + '!!!'

    return (inner(str1), inner(str2), inner(str3)) ## Return a tuple of strings

print(str_three('Python', 'is', 'good')) # Call str_three() and print
```
```python
# Define echo
def echo(n):
    """Return the inner_echo function."""

    # Define inner_echo
    def inner_echo(word1):
        """Concatenate n copies of word1."""
        echo_word = word1 * n
        return echo_word
        
    return inner_echo ## Return inner_echo

twice = echo(2) ## Call echo: twice
thrice = echo(3) ## Call echo: thrice

print(twice('Hi'), thrice('Hi')) ## Call twice() and thrice() then print
```
위의 echo function은 Nested function의 Closure(아마 폐쇄성?)을 보여주기 위한 예제이다. data camp에서 말하는 closure의 정의는 다음과 같다.
'Closure' means that the nested or inner function remembers the state of its enclosing scope when called. Thus, anything defined locally in the enclosing scope is available to the inner function even when the outer function has finished execution.
한글로 쉽게 풀어보자. Nested function의 폐쇄성이란 선언된 outer function의 argument를 inner function이 기억하고 있음을 의미한다. 즉, outer function의 실행이 종료됐을지라도 inner function에서 outer function의 argument로 선언된 enclosing scope를 계속 사용할 수 있다는 말이다. 쓰면서도 느꼈지만 그렇게 쉽지는 않은 것 같다. 아래의 링크를 공부해서 '범위'의 개념을 구체화 시켜보자.
https://sebastianraschka.com/Articles/2014_python_scope_and_namespaces.html#2-leg---local-enclosed-and-global-scope
http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%B4%EB%A1%9C%EC%A0%80-closure/

이제 echo function의 실행 과정을 알아보자. outer function은 echo(n)이고 inner function은 inner_echo(word1)이다. echo()는 inner_echo를 return하고 inner echo는 echo_word를 return한다. twice와 thrice에서 paratemer n에 각각 2와 3의 argument를 입력했다. 이제 n = 2, n = 3은 twice의 inner_echo와 thrice의 inner_echo에서 enclosing scope에 의해 사용할 수 있는 varible이 되었다. twice와 thrice에 똑같이 'Hi' argument를 입력했다. 'Hi'는 ineer_echo의 word1 parameter의 argument가 되고 enclosed value 2, 3에 의해 각각 'Hi'가 2번, 3번 반복되는 결과를 볼 수 있게 된다.

```python
# Define echo_shout()
def echo_shout(word):
    """Change the value of a nonlocal variable"""
 
    echo_word = word*2 ## Concatenate word with itself: echo_word
    
    print(echo_word) # Print echo_word
    
    # Define inner function shout()
    def shout():
        """Alter a variable in the enclosing scope"""    
        nonlocal echo_word ## Use echo_word in nonlocal scope
        ## 즉, 따로 local variable을 선언하는 것이 아니라 앞서 받았던 ehco_word를 그대로 가져와서 사용

        echo_word = echo_word + '!!!' ## Change echo_word to echo_word concatenated with '!!!'
    
    shout() ## Call function shout()
    print(echo_word) # Print echo_word

echo_shout('hello') ## Call function echo_shout() with argument 'hello'
```
## 2.3 Default and flexible arguments

```python
# Functions with one default argument
def shout_echo(str1, echo = 1):
    """Concatenate echo copies of str11 and three
     exclamation marks at the end of the string."""

    echo_str1 = str1 * echo ## Concatenate echo copies of str11 using *: echo_str1
    shout_str1 = echo_str1 + '!!!' ## Concatenate '!!!' to echo_str1: shout_str1

    return shout_str1 ## Return shout_str1

no_echo = shout_echo("Demacia") ## # Call shout_echo() with "Demacia": no_echo
with_echo = shout_echo("Demacia", echo = 5) ## Call shout_echo() with "Demacia" and echo=5: with_echo

print(no_echo)
print(with_echo) ## Print no_echo and with_echo

# Functions with multiple default arguments
def shout_echo_intense(str1, echo = 1, intense = False):
    """Concatenate echo copies of word1 and three
    exclamation marks at the end of the string.
    Moreover change the word shape according to intense"""

    echo_str1 = str1 * echo ## Concatenate echo copies of str11 using *: echo_str1
    
    # Make echo_str1 uppercase if intense is True
    if intense is True:
        # Make uppercase and concatenate '!!!': echo_word_intense
        echo_word_intense = echo_str1.upper() + '!!!'
    else:
        # Concatenate '!!!' to echo_str1: echo_word_intense
        echo_word_intense = echo_str1 + '!!!'

    return echo_word_intense ## Return echo_word_new
    
with_intense_echo = shout_echo_intense("Demacia", echo = 5, intense = True)
intense_no_echo = shout_echo_intense("Demacia", intense = True)

print(with_intense_echo)
print(intense_no_echo)

# Functions with variable-length arguments (*args)
def champs(*args): ## args is a tuple.
    """Concatenate strings in *args together."""
    
    name_space = "" ## Initialize an empty string: name_space

    # Concatenate the strings in args
    for name in args:
        name_space += name

    return name_space ## Return name_space

one_champ = champs("Garen")
many_champs = champs("Garen", "Lux", "Xin Zhao", "Jarvan IV")

print(one_champ)
print(many_champs)

# Functions with variable-length keyword arguments (**kwargs)
def report_status(**kwargs): ## kwargs is a dictionary.
    """Print out the status of players."""

    print("\nBEGIN: REPORT\n")

    # Iterate over the key-value pairs of kwargs
    for key, value in kwargs.items():
        # Print out the keys and values, separated by a colon ':'
        print(key + ": " + value)

    print("\nEND REPORT")

report_status(ID = "Khan", Champ = "Fiora", Position = "TOP", Team = "SKT T1")
report_status(ID = "Vizicsacsi", Champ = "Poppy", Position = "TOP", Team = "SPLYCE")
```

## 2.4 Bringing it all together
마찬가지로 tweet.csv를 이용한 예제. 적당한 csv를 구하자.

```pyhon
# Define count_entries()
def count_entries(df, col_name = 'lang'):
    """Return a dictionary with counts of
    occurrences as value for each key."""

    # Initialize an empty dictionary: cols_count
    cols_count = {}

    # Extract column from DataFrame: col
    col = df[col_name]
    
    # Iterate over the column in DataFrame
    for entry in col:

        # If entry is in cols_count, add 1
        if entry in cols_count.keys():
            cols_count[entry] += 1

        # Else add the entry to cols_count, set the value to 1
        else:
            cols_count[entry] = 1

    # Return the cols_count dictionary
    return cols_count

# Call count_entries(): result1
result1 = count_entries(tweets_df, 'lang')

# Call count_entries(): result2
result2 = count_entries(tweets_df, 'source')

# Print result1 and result2
print(result1)
print(result2)

# Define count_entries()
def count_entries(df, *args):
    """Return a dictionary with counts of
    occurrences as value for each key."""
    
    #Initialize an empty dictionary: cols_count
    cols_count = {}
    
    # Iterate over column names in args
    for col_name in args:
    
        # Extract column from DataFrame: col
        col = df[col_name]
    
        # Iterate over the column in DataFrame
        for entry in col:
    
            # If entry is in cols_count, add 1
            if entry in cols_count.keys():
                cols_count[entry] += 1
    
            # Else add the entry to cols_count, set the value to 1
            else:
                cols_count[entry] = 1

    # Return the cols_count dictionary
    return cols_count

# Call count_entries(): result1
result1 = count_entries(tweets_df, 'lang')

# Call count_entries(): result2
result2 = count_entries(tweets_df, 'lang', 'source')

# Print result1 and result2
print(result1)
print(result2)
```
