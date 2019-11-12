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
train_df = pd.read_csv(directory_train)
test_df = pd.read_csv(directory_test)
combine = [train_df, test_df]
```

### 2.2 dataset이 가진 변수와 관측값 파악하기
이 과정은 EDA의 기초면서 데이터 분석의 토대를 다지는 일이다. 명확히 내용과 과정을 전달하기 위해 문답형식을 이용했다. 마찬가지로 Pandas module의 함수를 이용해 진행할 것이다. 

**Q1. Dataset에 어떤 변수를 포함하고 있는가?**

변수를 다루기 위해 변수 이름을 아는 것은 중요한 일이다. 변수 이름이 무엇을 의미하는지는 [kaggle의 data page](https://www.kaggle.com/c/titanic/data)를 참고하면 된다.

```python
print(train_df.columns.values) ## train_df의 열 이름 출력
```


**Q2. 어떤 변수가 범주형 변수(categorical variable)인가?**

데이터 분석에 사용되는 변수는 크게 숫자형 변수와 범주형 변수로 나뉜다. 각 변수마다 사용할 수 있는 분석 방법이 다르기 때문에 어떤 변수가 어떤 형태를 갖고 있는지 반드시 알아야 한다. 비슷한 성질의 변수끼리 묶어두는 것도 좋다. 범주형 변수의 예로 순서가 없는 명목형(nominal), 순서가 있는 서열형(ordinal), 항목에 대한 전체 비율로 표현되는 비율형(ratio), 구간에 기반해서 얻은 등간형(interval) 등이 있다. 

- 명목형 변수 : Survived, Sex, and Embarked. 서열형 변수 : Pclass.


**Q3. 어떤 변수가 숫자형 변수(Numerical variable)인가?**

숫자형 변수의 예로는 이산형(discrete), 연속형(continuous), 시계열(time-serise) 등이 있으며 마찬가지로 변수의 형태에 따른 최적의 분석 방법과 시각화 방법이 다르므로 반드시 구분해야 한다. 

- 연속형 변수 : Age, Fare. 이산형 변수: SibSp, Parch.

> 보통 나이는 이산형 변수로 두는데 연속형 변수로 두는 이유가 있을까?

```python
train_df.loc[(train_df['Age'] < 10), : ]
## PassengerId = 832의 승객의 나이가 0.83임을 확인. 이 값이 만약 이상치가 아니라면 연속형 변수로 정의하는 것이 옳다
```

```python
# preview the data
train_df.head() # .head(int) : 선언된 dataframe의 index 0:5까지의 자료를 출력. 선언된 int만큼의 자료를 출력한다. 
```


**Q4. 어떤 변수가 혼합형 변수(mixed variable)인가?**

동일한 변수 안에 숫자형, 문자형 값들이 존재하는 경우는 생각보다 굉장히 흔하다. 간단한 예를 들면 '주소'부터 그런 형식이다. '문자형'으로 정의해서 변수를 정리할 수도 있지만 편집이 필요한 경우도 있으니 혼합형 변수를 확인해야 한다. 
- Ticket 변수가 숫자와 영어의 혼합형을 값으로 갖는 변수이다. Cabin 또한 같은 형태이다. 


**Q5. 잘못된 값이나 오타를 포함한 변수가 있는가?**

많은 변수와 관측값을 포함한 dataset에서 곧바로 오타나 잘못된 값을 찾아내기는 어렵지만, 우리가 다루고 있는 titanic dataset처럼 작은 dataset에서는 비교적 쉽게 찾아낼 수 있다.
- Name은 이름을 표현하는 많은 방법들이 있기 때문에 이 방법들을 수정해야할 값들로 볼 수 있다. 가령, 이름에 큰따옴표를 쓰는 경우를 예로 들 수 있다.

```python
train_df.tail() ## PassengerId : 889의 승객이름에 큰따옴표를 볼 수 있다.
```


**Q6. 관측값에 공백이나 값없음(null) 혹은 결측치(missing value)가 포함되어 있는가?**

앞서 말했지만 대부분의 통계 분석 과정에서 '값이 존재하지 않는 경우'는 '결과의 정확성'에 악영향을 미치기 때문에 가능하다면 다른 값으로 대체하거나 수정해야만 한다. 
> [결측치 처리에 대한 괜찮은 링크](https://eda-ai-lab.tistory.com/14)를 첨부한다. 

- train dataset에서 Cabin > Age > Embarked의 순으로 null값이 포함되어 있다.
- test dataset에서 Cabin > Age의 순으로 null값이 포함되어 있다. 

```python
# .isnull()과 .sum()을 이용한 결측치 탐색
train_df.isnull().sum() ## Cabin : 687, Age : 177, Embarked : 2
test_df.isnull().sum() ## Cabin : 327, Age : 86
```


**Q7. 관측값이 어떤 형식을 갖고 있는가?**

앞서 변수가 범주형인가 숫자형인가를 따졌다면 이젠 관측값이 어떤 형태로 저장되어있는지를 알아봐야 한다. 
- train dataset에서는 7개의 변수가 정수나 부동소수점형태의 자료이고 test dataset에서는 6개의 변수가 그렇다. 
- dataset에 상관없이 5개의 변수의 자료가 문자형을 갖는다. 

> train dataset과 test dataset에서 numerical value를 갖는 변수가 각각 7개와 6개로 차이나는 이유는 test dataset이 Survived를 포함하고 있지 않기 때문이다. 

```python
train_df.info()
print('_'*40) ## 미관을 위한 경계선을 추가한 것. 
test_df.info()
```


**Q8. dataset에서 숫자형 변수들은 어떤 분포를 갖는가?**

통계분석에서 관측값이 갖는 '분포(distribution)'를 알아보는 것은 매우 중요하다. 분포에 대해 조사해봄으로써 작게는 변수 안에서 관측값들이 갖는 개략적인 모습을 파악할 수 있고 크게는 모수적 방법(parametric method)과 비모수적 방법(non-parametric method)을 이용해 분석을 할 것인지에 대한 의사결정을 내리는 근거가 될 수 있기 때문이다. 모델 적합에 이용할 train dataset을 이용해 분포를 알아보자. 

- train testset에 포함된 것은 전체 승객 2,224명 중 40%에 해당하는 891명에 대한 자료들이다.
- Survived는 범주형 변수로 0과 1의 값을 갖으며 각각 사망, 생존을 의미한다. 
- train testset을 기준으로 38%의 생존률을 갖지만 실제 생존률은 32%이다. 
- 75% 이상의, 대부분의 승객들은 부모나 아이없이 타이타닉에 승선했다. 
- 약 30%의 승객들은 형제자매와/또는 배우자와 함께 승선했다.
- 1% 미만의 승객들은 $512 이상의 값을 지불하고 승선했다.
- 65-80살의 승객들은 1% 미만이다. 

```python
train_df.describe()
# Review survived rate using percentiles=[.61, .62] knowing our problem description mentions 38% survival rate.
# Review Parch distribution using percentiles=[.75, .8]
# SibSp distribution [.68, .69]
# Age and Fare [.1, .2, .3, .4, .5, .6, .7, .8, .9, .99]
```

**Q9. dataset에서 범주형 변수들은 어떤 분포를 갖는가?**
- Name 변수에서 중목되는 이름은 없다. 
- Sex는 두 개의 범주를 가지며 탑승객의 65%가 남성이다.
- Cabin은 dataset 전반에 걸쳐 중복되는 경우가 있다. 이는 여러 승객들이 한 객실을 사용했음을 의미한다.
- Embarked는 세 개의 범주를 가지며 'S' 항수를 이용한 탑승객이 제일 많았다.
- Ticket에서 22%의 관측값에서 중복값을 발견했다.

```python
train_df.describe(include=['O']) ## 'O' : Strings object에 대한 decribe를 요청하는 arg
## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html 참고 
```

### 2.3 데이터 분석에 근거한 가정
아래는 이후의 데이터 분석에서 근거할 가정들이다. 실제 분석을 하기 전 이 가정들을 만족하는지 확인해볼 것이다. 


**상관성<sup>[[3]](#footnote_3)</sup>** 
어떤 변수가 생존과 어떤 관련있는지 밝혀내야한다. 간편한 분석 과정을 통해 대략적인 상관성을 찾은 후 modelling에 포함시킬지 여부를 판단할 것이다. 

**Completing**
1) 'Survived'와 'Age'가 관계 있다고 가정하고 만족하는지 확인.
2) 'Embarked'가 'Survived'나 다른 변수과 관계가 있다고 가정하고 만족하는지 확인.


**변수 제거(Correcting)**
1) 'Ticket'은 지나치게 높은 중복도(22%)를 갖고 있어 생존여부와의 상관성이 떨어진다고 추정, 이후의 분석에서 제외한다. 
1) 'Cabin'은 train dataset과 test dataset, 두 dataset에서 공통적으로 너무 많은 결측치를 갖고 있으므로 제외한다.
1) 임의로 매긴 PassengerId도 생존여부와 관련없으므로 제외한다.
1) 'Name' 또한 생존여부와 관계없으므로 제외한다. 


**변수 생성**
1) 부모-자녀나 형제-자매 혹은 배우자와 함께 승선한 승객들이 많으므로 이를 표현하기 위해 'Family' 변수를 추가한다.
1) 'Name'을 조작하여 'Title'이라는 새로운 변수를 만들 것이다.
1) 연속형 변수인 'Age'를 편집해 서열척도 기반의 'Age band'를 추가할 것이다.
1) 분석을 위해 'Fare range'를 추가할 것이다. 

> '나이'나 '운임'등의 연속형 혹은 이산형 자료를 범주형으로 바꾸면 범주형 분석 도구를 사용해 분석할 수 있으므로 분석과정이 편해진다. 


**개략적인 가설설정(Classifying)**

앞서 설명한 문제에 대해 가정을 추가할 수 있다.

1) 여성의 생존률이 더 높을 것이다.
1) 아이의 생존률이 더 높을 것이다.
1) 상류층 승객의 생존률이 더 높을 것이다. 


<a name="footnote_3">[3]</a> 상관계수를 이용한 상관관계 판단이 아닌 "그냥 A와 B가 관계가 있지 않을까?" 수준의 가정이다.


### 2.4 주축 변수를 이용한 기초 분석

가정들을 확인하기 위해 가정의 주축되는 변수들 간의 상관관계를 간략하게 살펴볼 필요가 있다. 아직 전처리 단계 전이므로 결측치나 이상치에 대한 조작없이 시행해야 할 것이기 때문에 이 과정에서 결측치를 포함한 관측값들은 제외될 것이다. 대상이 되는 변수들은 범주형(Sex), 서열형(Pclass) 혹은 이산형(SibSp, Parch) 등이다. 

- *Pclass* '개략적인 가설설정' 단계에서 가정한 3번째 가정인 '상류층 승객의 생존률이 더 높을 것이다.'가 어느 정도 사실로로 보인다. 따라서 'Pclass'를 model에 포함시켜 model을 만들어보겠다.
- *Sex* '개략적인 가설설정' 단계에서 가정한 1번째 가정인 '여성의 생존률이 더 높을 것이다.'가 사실(여성의 74%가 생존)로 보인다.
- *SibSp* and *Parch* 결측값을 제외한 자료들을 이용했을 때, 이 변수들과 생존여부는 큰 관계가 없어보인다. 관계를 알아내는 것보다 이렇게 특정 변수로 묶어내는 것이 최선의 결과일 수도 있다.

```python
train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train_df[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
## train_df[["A", "B"]].groupby(['A'], as_index=False).mean().sort_values(by='B', ascending=False)
## df에서 "A"와 "B" column 선택 / "A" 컬럼의 value를 기준으로 묶고 / 평균을 계산 / 계산 결과를 'B' column에 대하여 내림차순 정렬
## pd.groupby(, as_index = boolean) : 그룹화한 결과를 종합해서 객체로 반환할 때 index에 의한 정렬을 할 것인가? as_index=False 이 효과적인  “SQL-style”의 결과물임.
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html 참고
```

### 2.5 시각화를 이용한 기초 분석
시각화 방법을 이용해서 위에서 설정한 가정의 만족 여부를 알아보자. 

#### 2.5.1 숫자 변수들과 'Survived'의 연관성
히스토그램은 'Age'(위에서 나잇대로 수정한 Age band)과 같이 연속적인 숫자들의 분포를 설명하기 좋은 그래프다. 히스토그램이 그려지는 범위와 구간(bins)들은 자동으로 정의되는데 옵션에서 인수(argument)를 주어 수정할 수 있다. 앞서 가정했던 '영유아의 생존률이 더 높은가'를 히스토그램으로 알아보자. 

**분석 결과**
- 영유아(4세 이하)는 높은 수준의 생존률을 보인다. 
- 나이가 가장 많은 (80살)의 승객이 살아남았다.
- 많은 수의 15-25살 사이의 승객들은 살아남지 못했다.
- 타이타닉에 탑승한 많은 승객들은 15-35살에 속한다. 

**분석 결과를 통한 의사결정**
이와 같은 간단한 분석들로 처음, work flow 단계에서 가정했던 내용에 대한 의사결정을 할 수 있다.  
- model에 'Age'를 포함시켜야 한다. (개략적인 가설설정 #2)
- 'Age'의 null값을 처리해야 한다. (변수 제거 #1)
- 'Age'를 'Age band'로 바꿔줘야 한다. (변수 생성 #3)

```python
g = sns.FacetGrid(train_df, col='Survived') ## .FaceGrid(df, col=col) : '기준'이 될 col을 선언해서 그래프가 그려진 판을 먼저 짬. 
g.map(plt.hist, 'Age', bins=20)
```
#### 2.5.2 숫자형 변수 + 서열형 변수들과 'Survived'의 연관성
숫자형 변수와 범주형 변수는 '숫자'로 표현가능하기 때문에 한번에 묶어서 그래프로 만들 수 있다.

**분석 결과**
- Pclass=3이 승객 중 대부분을 차지하지만 이 중 많은 수가 살아남지 못했다. 따라서 개략적인 가설설정 #2이 가설로써 의미있을 것으로 보인다.
- Pclass=2와 Pclass=3의 영유아 승객들은 대부분 살아남았다. 따라서 개략적인 가설설정 #2이 가설로써 의미있을 것으로 보인다.
- Pclass=1의 대부분의 승객은 살아남았다. 따라서 개략적인 가설설정 #3이 가설로써 의미있을 것으로 본다.
- Pclass와 Survived로 구분하여 승객들의 나이를 히스토그램으로 나타냈다.

**분석 결과를 통한 의사결정**
'Pclass'를 model에 포함시키자.

```python
grid = sns.FacetGrid(train_df, col='Pclass', hue='Survived')
grid = sns.FacetGrid(train_df, col='Survived', row='Pclass', size=2.2, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend();

```
#### 2.5.3 범주형 변수와 'Survived'의 연관성
범주형 변수들과의 연관성을 보자. 

**분석 결과**
- 여성 승객의 생존률이 남성보다 더 높다. 따라서 개략적인 가설설정 #1이 가설로써 의미있을 것으로 보인다.
- Exception in Embarked=C where males had higher survival rate. This could be a correlation between Pclass and Embarked and in turn Pclass and Survived, not necessarily direct correlation between Embarked and Survived.
- Pclass=2에 비해 Pclass=3(C와 Q 항구에서 탑승한)의 남성이 생존률이 높다. 
- 승선이 이뤄진 항구와 Pclass=3의 남성 탑승객 사이의 생존률이 다르다. 

**분석 결과를 통한 의사결정**
- 'Sex'를 model에 추가
- Complete and add Embarked feature to model training.


```python
# grid = sns.FacetGrid(train_df, col='Embarked')
grid = sns.FacetGrid(train_df, row='Embarked', size=2.2, aspect=1.6)
grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
grid.add_legend()
```

#### 2.5.4 범주형 변수와 숫자형 변수들과 'Survived'의 연관성
2.5.3에서 숫자가 아닌 범주형 변수들과 Survived의 연관성을 봤다면 이젠 숫자형태의 범주형 변수들과 Survived의 연관성을 보자. 

**분석 결과**
- 높은 수준의 요금을 내고 탑승한 승객의 생존률이 더 높음. 따라서 요금 구간(fare range)이라는 변수를 만들 것. 
- 승선한 항구와 생존률과의 연관성이 있는 것으로 보임. 

> 2.5.3의 결과와 배치되는 거 아닌가? 해석을 잘못했나?

**분석 결과를 통한 의사결정**
- 요금 구간을 의미하는 변수 생성


```python
# grid = sns.FacetGrid(train_df, col='Embarked', hue='Survived', palette={0: 'k', 1: 'w'})
grid = sns.FacetGrid(train_df, row='Embarked', col='Survived', size=2.2, aspect=1.6)
grid.map(sns.barplot, 'Sex', 'Fare', alpha=.5, ci=None)
grid.add_legend()
```

## 3. 전처리 과정(Wrangle data)
지금까지 우리는 가지고 있는 dataset으로 문제해결을 위한 여러 가정과 그에 맞는 의사결정을 했다. 이 과정에서 아직까지 실제 dataset을 조작한 일은 없다. 이제 dataset을 조작해 변수를 편집하고 새로운 변수를 만들어보자. 

### 3.1 변수 편집
변수 편집을 변수 제거와 변수 수정의 두 과정으로 나눌 수 있다. 3.2 변수 생성까지 이 과정으로 포함할 수도, 굳이 '변수 편집'이라는 항목으로 묶지 않아도 된다. 이렇게 구분한 것은 항목 수준을 맞춰주기 위함일 뿐 특별한 의미는 없다. 

#### 3.1.1 변수 제거
정리정돈의 시작은 무엇을 버릴지에서 시작한다. 쓸모없는 변수를 제거하면 dataset의 크기가 줄어들어 분석 시간과 복잡도에서 이점을 갖게 된다. 지금까지의 가정과 의사결정으로 우리는 'Cabin'(correcting #2)과 'Ticket'(correcting #1)을 제거하기로 했다. 당연한 이야기지만 제거하기로 한 변수가 있다면 train set과 test set 둘 다 제거해주어야 한다. 

```python
print("Before", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(['Ticket', 'Cabin'], axis=1)
test_df = test_df.drop(['Ticket', 'Cabin'], axis=1)
combine = [train_df, test_df]

print("After", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)
```
> 왜 combine[0].shape, combine[1].shape을 넣었는지는 모르겠다. train, test 둘 다 감소된 걸 보이고 싶었나?

#### 3.1.2 이미 가지고 있는 변수를 추출해 새로운 변수 만들기 - Title
'Name'과 'PassengerId'를 버리기 전에, 'Name'에 포함된 호칭(title)을 추출해 호칭과 생존 간의 관계가 있는지 알아보자. 

호칭을 추출하기 위한 아래의 코드는 정규표현식을 이용했다. 정규표현식 패턴, (\W+\.)는 'Name'변수에 있는 'W'로 시작하고 '.'으로 끝나는 문자열을 추출하기 위한 것이다. expand = False는 결과를 데이터프레임으로 받기 위해 추가했다. 

**분석결과**

호칭, 나이, 생존률을 고려했을 때 아래의 결과를 얻었다.
- 대부분의 호칭은 나이대와 높은 관련성이 있었다. 예를 들어 'Master'는 평균 연령 5살이었다. (정확히는 6살에 가깝다. 5.99)
- 나이대와 호칭의 생존률 사이에는 약간의 차이가 있다.
- 확실히 생존률이 높은 호칭은(Mme, Lady, Sir)이었고 낮은 호칭은(Don, REv, Jonkheer)이었다.

**의사결정**

우리는 model training을 위해 새로운 'Title'변수를 계속 유지하기로 결정했다.

```python
for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

pd.crosstab(train_df['Title'], train_df['Sex'])
(train_df.Age[train_df['Title'] == 'Master'].mean() + test_df.Age[test_df['Title'] == 'Master'].mean())/2 ## 5.99
```
```python
title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

train_df.head()
```

이제 쓸모없는 'Name'와 PassengerId'를 training set과 test set에서 버릴 때가 됐다. 

```python
train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis=1)
combine = [train_df, test_df]
train_df.shape, test_df.shape
```

#### 3.1.3 변수 수정 - 범주형 변수
이제 문자열을 갖고 있는 범주형 변수의 값을 숫자로 바꿔줄 것이다. 이 과정은 대부분의 수리적 모델 알고리즘이 '숫자'를 기반으로 만들어졌기 때문에 숫자형태의 범주 표현을 쓰는 것이 좋기 때문에 필요하다. 
'Sex'를 성별에 따라 여성 = 1, 남성 = 0의 값을 갖도록 바꾸자. 

```python
## combine에서 dataset을 반복하기 
for dataset in combine: 
    dataset['Sex'] = dataset['Sex'].map( {'female': 1, 'male': 0} ).astype(int)
## map() 함수는 built-in 함수로 list 나 dictionary 와 같은 iterable 한 데이터를 인자로 받아 
## list 안의 개별 item을 함수의 인자로 전달하여 결과를 list로 형태로 반환해 주는 함수이다.
## astype() 함수는 해당 값의 type을 바꿔주는 함수. 


train_df.head() ## combine을 대상으로 for문을 실행해도 combine의 대상이었던 train, test set 모두 다 바뀐다. 
```

#### 3.1.4 숫자형 연속 변수 수정
결측값 또는 Null값을 이미 갖고 있는 값들에 근거해서 추정해 채워넣어주어야 한다. 먼저 'Age'를 대상으로 해보자. 

결측값 또는 Null의 숫자형 연속 변수를 채워넣는 방법에는 대표적인 세 가지가 있다. 
1. 갖고 있는 관측값의 평균과 표준편차를 이용해 채워넣는 방법.
1. 결측값 또는 Null이 속한 변수와 다른 변수와의 관련성을 이용하는 방법. 우리가 지금 사용하고 있는 Titanic data set의 경우, 'Age', 'Gender', 'Pclass' 사이의 관련성이 존재한다. 'Age'의 결측값 또는 Null을 추정하기 위해 'Plass'와 'Gender'의 조합 세트를(combination set) 통해 'Age'의 중앙값을 이용한다. 가령 Pclass=1과 Gender=0에서의 'Age'의 중앙값, Pclass=1과 Gender=0에서의 'Age'의 중앙값을 구하는 식이다. 
1. 앞선 두 방법을 혼합한 방법. 두 번째 방법에서 중앙값을 사용해 추정했다면 이 방법에서는 평균과 표준쳔차를 이용해 분포를 정의하고 분포 안에서 난수를 뽑아 결측치 또는 Null을 채워넣는다. 

방법 1과 3은 분포를 이용한 난수를 기반하고 있으므로 model에 대한 오차를 수반할 수 밖에 없다. 그러므로 여러 번의 실행마다 다른 값이 나올 확률이 존재하기 때문에 우리는 방법 2를 사용하겠다. 

```python
# grid = sns.FacetGrid(train_df, col='Pclass', hue='Gender')
grid = sns.FacetGrid(train_df, row='Pclass', col='Sex', size=2.2, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend()
```
이제 'Pclass'와 'Gender'를 이용해 'Age'의 빈 값들을 채워보자. 

```python
guess_ages = np.zeros((2,3))
guess_ages
```

성별이 두 개의 수준을 갖고 객실이 세 개의 수준을 가지므로 'Age'의 결측값을 채울 수 있는 두 변수의 경우의 수는 총 6개이다. 

```python
for dataset in combine:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = dataset[(dataset['Sex'] == i) & \
                                  (dataset['Pclass'] == j+1)]['Age'].dropna()

            # age_mean = guess_df.mean()
            # age_std = guess_df.std()
            # age_guess = rnd.uniform(age_mean - age_std, age_mean + age_std)

            age_guess = guess_df.median()

            # Convert random age float to nearest .5 age
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5
            
    for i in range(0, 2):
        for j in range(0, 3):
            dataset.loc[ (dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1),\
                    'Age'] = guess_ages[i,j]

    dataset['Age'] = dataset['Age'].astype(int)

train_df.head()
```

#### 3.1.5 숫자형 연속 변수 생성 - 나이대
3.1.4에서 'Age'의 결측값을 추정해 채워넣었다. 이제 'Age'를 'Age bands'로 바꿔보자. 

```python
train_df['AgeBand'] = pd.cut(train_df['Age'], 5)
train_df[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)

## Age band를 숫자형 범주로 바꿔 'Age'로 대체시키기 
for dataset in combine:    
    dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[ dataset['Age'] > 64, 'Age']
train_df.head()

## AgeBand 정리 
train_df = train_df.drop(['AgeBand'], axis=1)
combine = [train_df, test_df]
train_df.head()
```

#### 3.1.6 이미 가지고 있는 변수를 추출해 새로운 변수 만들기 - IsAlone
'Parch'와 'SibSp'를 이용해 'FamilySize'를 만들고 'FamilySize'를 이용해 승객이 Titanic에 가족과 함께 탔는지 아닌지를 알 수 있도록 해보자. 두 변수를 의미가 같은 하나의 변수로 줄인다면 변수 규모를 줄일 수 있어 모형 적합에 긍정적인 효과를 기대할 수 있다.  

```python
for dataset in combine:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1

train_df[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)
```
만든 'FamilySize'를 이용하면 Titanic에 혼자 탑승 했는지, 가족과 함께 탑승했는지 알 수 있게 되므로 새로운 변수, 'IsAlone'를 만들 수 있다. 

```python
for dataset in combine:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()

## 'Parch', 'SibSp', 'FamilySize' 제거 
train_df = train_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
test_df = test_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
combine = [train_df, test_df]

train_df.head()
```

Pclass와 Age를 이용한 새로운 변수, 'Age x Pcalss'를 만들었다. 

```python
for dataset in combine:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass

train_df.loc[:, ['Age*Class', 'Age', 'Pclass']].head(10)
```

#### 3.1.7 범주형 변수 수정 
'Embarked'에 속한 S, Q, C의 값은 정박했던 항구에 기인한 값들이다. 우리가 갖고 있는 training set에는 2개의 결측값이 존재하는데 결측값을 간단한 방법을 이용해 채워보자. 

```python
freq_port = train_df.Embarked.dropna().mode()[0] 
freq_port # 'S' : S, Q, C 중 S의 값이 가장 많음. 
## .dropna() method : na를 모두 버림
## .mode() : 최빈값


for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port) 
    ## na를 최빈값인 'S'로 채움
    
train_df[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)
```

채워진 'Embarked'의 값 S, Q, C를 숫자형태로 바꾸자. 

```python
for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

train_df.head()
```
#### 3.1.8 숫자형 변수 수정 - 빠르게 바꾸는 방법
'Fare'에는 단 하나의 결측값이 존재한다. 3.1.7에서 본 것 같이 전체 관측값에 비해 압도적으로 적은 개수의 결측값은 '최빈값'을 이용해 채우는 것이 타당하다. 단 한 줄의 코드로 'Fare'의 결측값을 최빈값으로 채워보자. 

```python
test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
test_df.head()
```

이 때, 단 하나의 값만 채워넣는 것이므로 3.1.4에서 본 것처럼 복잡한 과정은 필요없다. 'Fare'를 구간으로 나눈 'FareBand'를 만들어보자.

```python
train_df['FareBand'] = pd.qcut(train_df['Fare'], 4)
train_df[['FareBand', 'Survived']].groupby(['FareBand'], as_index=False).mean().sort_values(by='FareBand', ascending=True)
```

'FareBand'를 기준으로 'Fare'의 값을 대체하자. 

```python
for dataset in combine:
    dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
    dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

train_df = train_df.drop(['FareBand'], axis=1)
combine = [train_df, test_df]
    
train_df.head(10)
```

아래의 dataset이 최종적인 test data set의 형태이다.

```python
test_df.head(10)

```













