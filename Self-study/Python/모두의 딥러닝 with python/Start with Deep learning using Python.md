## ch 7. 다중 퍼셉트론의 기초

NAND(Negative AND), AND, OR의 함수로 XOR의 문제 해결하기


```python
import numpy as np

# weight와 bias 설정
w11 = np.array([-2, -2])
w12 = np.array([2, 2])
w2 = np.array([1, 1])
b1 = 3
b2 = -1
b3 = -1 


# perceptron
def MLP(x, w, b):
    y = np.sum(w * x) + b
    if y <= 0:
        return 0 
    else:
        return 1
    
# NAND gate
def NAND(x1, x2):
    return MLP(np.array([x1, x2]), w11, b1)
    
# OR gate
def OR(x1, x2):
    return MLP(np.array([x1, x2]), w12, b2)

# AND gate
def AND(x1, x2):
    return MLP(np.array([x1, x2]), w2, b3)

# XOR gate
def XOR(x1, x2):
    return AND(NAND(x1, x2), OR(x1, x2))


# x1, x2 값을 번갈아 이용해 y 출력
if __name__ == '__main__':
    for x in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        y = XOR(x[0], x[1])
        print("입력 값 X: " + str(x) + "출력 값  y = " + str(y))
        
```

    입력 값 X: (0, 0)출력 값  y = 0
    입력 값 X: (1, 0)출력 값  y = 1
    입력 값 X: (0, 1)출력 값  y = 1
    입력 값 X: (1, 1)출력 값  y = 0
    

## 심화학습, 코드로 확인하는 신경망 


```python

## 환경 변수 설정
# 1) input, target
data = [
    [[0, 0], [0]],
    [[0, 1], [1]],
    [[1, 0], [1]],
    [[1, 1], [0]],
]

# 2) interation, leanring rate, mo
iter = 5000
lr = 0.1
mo = 0.9

# 3) 활성화 함수, sigmoid
# 미분 여부에 따라 다른 값 설정
def sigmoid(x, derivative = False):
    if (derivative = True):
        return x * (1-x)
    return 1 / (1 + np.exp(-x))

# 4) 활성화 함수, tah
# tanh 함수의 미분은 1-(활성화 홤수 출력의 제곱)
def tanh(x, derivative = False):
    if (derivative = True):
        return 1 - x ** 2
    return np.tanh(x)

# 5) 가중치 배열 
def makeMatrix(i, j , fill = 0.0):
    mat = []
    for i in range(i):
        mat.append([fill] * j)
    return mat
```
