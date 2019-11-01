# 1. Writing your own functions
## 1.1 User-defined functions
앞서 봤던 function들은 다른 사람들이 특정 목적을 위해 만들어놓은 것들이다. 그렇다면 내가 다뤄야할 문제들에 대한 function이 존재하지 않는다면 어떻게 해야할까? Python에서는 사용자 스스로 자신의 함수를 build up 할 수 있다.
```Python
# Simple example for user-defined functions
def python_is():
    """Print a string with three exclamation marks"""
    # Concatenate the strings: shout_word
    python_def = 'Python is an interpreted, high-level, general-purpose programming language' + '!!!'
    

    # Print shout_word
    print(python_def)

# Call shout
python_is()
```
