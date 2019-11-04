https://www.kaggle.com/startupsci/titanic-data-science-solutions/notebook#Titanic-Data-Science-Solutions

### 들어가기 전에
본 글은 1) kaggle에 익숙해지기 위해 2) Python이 실제로 어떻게 사용되는지 알기 위해 3) 영어 공부 및 글쓰기 능력 강화 등의 목적으로 작성되었다. 
kaggle에 올라와있는 '좋은' notebook을 대상으로 했으며 이번 글은 Titanic Data Science Solutions의 번역과 내용 이해를 위한 comment로 이뤄져 있다.
나의 이해가 제 1 목적이므로 원문의 구성과 조금 달라질 수 있다. 얼마나 계속될지는 모르겠지만 최대한 하는데까지 해보자. 

# Titanic Data Science Solutions
## 1. Introduction

본 글은 책, Data Science Solutions<sup>[[1]](#footnote_1)</sup>의 한 부분이다. 
본 글은 kaggle과 같은 사이트에서 볼 수 있는 data science 경연이나 문제들을 해결할 수 있는 일반적인 업무 흐름에 따라 작성되었다.

kaggle에는 data science로 해결할 수 있는 수 많은 과제들이 문제를 해결하기 위해 제출된 더 많은 수의 훌륭한 보고서들이 있다.
그러나 대부분의 보고서는 전문가가 전문가를 위해 쓴 글이기 때문에 '어떻게 해결방법이 고안되었는가'를 설명할 때 일부를 생략하기도 한다. 
물론 주요 독자인 data science의 전문가는 문제가 되지 않지만 이 글을 보고 있을 입문자들에겐 올바른 이해를 위해 생략된 일부가 꼭 필요할 것이다.
본 글의 목적은 해결 방법이 어떻게 고안되었는지를 명확히 보여주는 것이다. 따라서 단계별로 진행되는 업무흐름을 명시할 것이고 문제 해결 방법 제시를 위해 진행되는 모든 의사결정과 이유를 각 단계마다 명확히 보일 것이다. 

### 1.1 Workflow stages
data science 경연에서 제출할 보고서를 작성할 때, 아래의 7개의 흐름을 따라가는 것을 제안한다. 

1. 질문이나 문제를 정의할 것
1. training data와 testing data를 명시할 것
1. data 전처리(Wrangle, prepare, cleanse)
1. data를 분석, 탐색하거나 패턴을 확인할 것
1. 문제 해결을 위한 모델을 세우고 모델을 통해 예측할 것
1. 시각화를 비롯한 결과 제시를 통해 문제 해결 과정을 보일 것
1. 결과를 제출할 것

위의 과정은 일반적으로 따라갈 수 있는 흐름이지만 모든 일이 그렇듯, 예외가 발생할 수 있다. 아래의 경우가 일반적인 흐름을 따르지 않는, 이례적인 사례들이다.

- 여러 개의 과정을 섞어서 진행하는 경우. 시각화를 이용해 data를 분석하는 경우.
- 위의 과정에서 명시된 것보다 더 이른 단계에서 분석을 시작하는 경우. 전처리 이전과 이후에 data를 분석하는 경우. 
- 전체 과정에서 한 단계를 여러번 반복하는 경우. 시각화 단계가 여러번 반복되는 경우.
- 한 단계를 모두 제외시키는 경우. 경연 결과에서 해당 단계를 보이지 않아도 된다고 판단한 경우.

### 1.2 Question and problem definition

kaggle과 같은 경연 사이트들은 경연참가자들의 data science model을 훈련시키고 검증 dataset을 통해 검증하는 일련의 작업을 지원하기 위해 dataset을 제공한다. 따라서 경연에 참가하는 팀들은 목적에 부합하는 문제 해결 방법을 제시해야하며 요구하는 문제를 이해하는 과정을 반드시 거쳐야 한다. Titanic Survival competition에서 해결해야 할 문제는 [kaggle에 이미 제시되어 있다.](https://www.kaggle.com/c/titanic)  

> 당신에게 타이타닉 침몰 사건에서 생존하거나 사망한 승객의 명단 표본이 training dataset으로, 생존하거나 사망했다는 정보가 없는 명단이 test  dataset으로 주어졌습니다. training dataset으로 학습시킨 당신의 model로 test dataset에 속한 사람들의 생존 혹은 사망 여부를 예측하시는 것이 이번 경연의 문제입니다. 

위의 문제를 이해하고 model을 만드는데 참고할만한 정보가 있다. 아래의 정보들은 [여기에서 확인](https://www.kaggle.com/c/titanic)할 수 있으며 주요 내용만 정리해보았다.

- 1912년 4월 15일, 타이타닉의 첫 출항 중, 타이타닉은 빙산에 부딪혀 가라앉았고 탑승객과 선원을 포함한 2224명 중 1502명이 사망했다. 다시 말해, 전체 탑승자 중 32% 만이 살아남았다. 
- 타이타닉의 난파 후 탑승자들의 생존률을 떨어트린 요인 중 하나는 타이타닉에 충분한 수의 구명선이 없었다는 것이다.
- 운에 의한 여러가지 요소를 제외하더라도 생존자들에겐 유사한 경향성이 나타나는데 여성이거나 어린아이거나 높은 등급의 객실을 이용했다는 것 등이다. 

### 1.3 Workflow goals
Data science를 통한 문제 해결 방법은 7가지의 중요한 목표를 달성하는 과정으로 이해할 수 있다. 

1. **자료를 분류**. 자료(dataset)를 항목에 맞게 분류하거나 구분하는 작업이다. 자료를 목적에 부합하도록 각 범주로 분류시킬 수 있다면 범주 사이의 상관 관계나 특성에 대한 연구를 해볼 수 있다. 
1. **상관관계 찾기**. training dataset의 자료가 갖는 변수<sup>[[2]](#footnote_2)</sup>들을 이용해 문제에 접근할 수 있는 방법 중 하나다. dataset이 갖는 변수 중 어떤 것이 문제 해결을 위한 핵심인가? 통계적으로 dataset의 어떤 변수가 문제해결과 [상관관계](https://en.wikiversity.org/wiki/Correlation)가 있다고 말할 수 있는가? 변수 안의 값들을 변화시켰을 때 model의 결과값이 어떻게 바뀌는가? 변수와 model의 결과값이 같은 방향성을 갖는가? 아니면 정 반대의 방향성을 갖는가? 변수와 결과값의 상관관계 분석은 숫자 자료형뿐 아니라 명목 자료형에서도 사용할 수 있으므로 주어진 dataset을 이용한 대표적인 검정이다. 만약 상관관계를 찾는다면 이후의 단계 진행을 좀 더 쉽게 할 수 있을 것이다. 
1. **모형을 통한 분석에 적절한 형태로 자료를 변환**. 모형을 설정하는 단계에서 data를 모형에 적합시키기 위한 적절한 형태로 변형하는 것은 매우 중요하다. 아무리 좋은 모형이더라도 적합시키는 data의 형식이 잘못되었다면 제대로된 결과값이 나오지 않기 때문이다. 변환의 대상이 되는 data의 형식은 변수가 갖는 값의 형식(예를 들어 숫자형, 명목형 등)과 data 그 자체의 형태(예를 들어 array, data frame 등) 모두를 포괄한다. 
1. **결측치(missing value) 확인**. 전처리(Preprocessing) 단계에서의 핵심은 결측치(Missing value)를 찾고 가능하다면 적절한 값으로 대체하는 것이다. 결측치가 포함된 상태의 자료로는 제대로된 결과값이 나오지 않는 경우가 대부분이기 때문에 이 단계를 반드시 거쳐야 한다.
1. **이상치(outliers) 확인**. 이상치(outliers)란 관측값이 갖는 부적절한 값(예를 들어 나이가 0.72살로 입력된 경우)을 의미한다. 이상치가 포함된 자료, 특별히 training dataset으로는 높은 수준의 training 결과를 기대하기 어려우므로 가능하다면 적절한 값으로 이상치를 대체해야 한다. 
1. **변수 변환**. 할 수 있다면 이미 존재하는 변수나 변수의 집합 등을 이용해 새로운 변수를 만드는 것도 문제해결에 도움을 준다. 충분하지 않은 관측값 하에서 지나치게 많은 변수를 모형에 포함시키면 [낮은 수준의 정확성](https://en.wikipedia.org/wiki/Curse_of_dimensionality)을 갖게 되기 때문이다. 
1. **결과보고**. 최고의 결과를 적절한 도구를 통해 드러내는 것은 경쟁에 참여하는 모든 참가자가 해내야할 목표다. 알맞은 시각화와 표, 분명한 문장으로 결과를 제시하자.

<a name="footnote_1">[1]</a> Data Science Solutions의 저자와 notebook Titanic Data Science Solutions의 저자가 같다
<a name="footnote_2">[2]</a> Feature를 '변수'(Variable)로 번역했다. 


## 2. 탐색적 자료 분석(Exploratory Data Analysis, EDA)
이번 장에서는 Titanic training dataset을 이용해 탐색적 자료 분석을 해보겠다. 탐색적 자료 분석은 자료와 변수의 개략적인 형태, 특징 등을 알기 위한 대표적인 방법이다. 자세한 내용은 [위키피디아의 EDA](https://en.wikipedia.org/wiki/Exploratory_data_analysis)를 참고하길 바란다.

```python
# EDA와 전처리를 위한 module
import pandas as pd
import numpy as np
import random as rnd

# 시각화를 위한 module
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline ## notebook을 실행한 브라우저에서 바로 그림을 볼 수 있게 해줌.

# machine learning을 위한 module
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
```

### 2.1 dataset 불러오기
파이썬의 Pandas module을 이용하면 손쉽게 csv 확장자로 저장된 dataset을 불러올 수 있다. Titanic 경연에서 제공되는 training dataset과 test dataset은 csv확장자이므로 Pandas를 이용해 불러와보자. EDA를 진행하기 위해 train dataset과 test dataset을 하나의 dataset으로 합칠 것이다. 사실 하나의 dataset에서 EDA 후, train, test set으로 나눠 모형의 정확성 검증하는 것이 일반적인 데이터 분석의 순서이므로 EDA를 하기 위해 train set과 test set을 합치는 것은 매우 당연한 일이다.

```python
train_df = pd.read_csv(directory of train dataset)
test_df = pd.read_csv(directory of test dataset)
combine = [train_df, test_df]
```

### 2.2 dataset이 가진 변수와 관측값 파악하기
이 과정은 EDA의 기초면서 데이터 분석의 토대를 다지는 일이다. 명확히 내용과 과정을 전달하기 위해 문답형식을 이용했다. 마찬가지로 Pandas module의 함수를 이용해 진행할 것이다. 

```python

```




