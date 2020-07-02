
`Caret` 패키지는 예측변수로 이뤄진 데이터셋(Predictor data) 전처리(Pre-precess)를 위한 여러 함수를 포함하고 있다. 이 함수들은 예측변수 데이터가 모두 숫자형(Numeric data)으로 이뤄져 있음을 가정하고 있기 때문에 사용하기 전에 숫자형 자료로 바꿔줘야 한다. 흔히 "더미 변수화"로 불리는 작업이 위와 같은 과정이며 `model.matrix`나 곧장 설명할 `caret` 패키지의 `dummyVars`을 사용할 수 있다. 

후에 다루겠지만, `train`와 [`recipes`](https://recipes.tidymodels.org/)를 사용해서 전처리 과정에서 더욱 다양하고 사용자의 입맛대로 설정 가능한 옵션들을 어떻게 다룰 수 있는지 알려주도록 하겠다. 

## 3.1 가변수(Dummy Variables) 만들기(Creating Dummy Variables)  
**가변수**(Dummy variable)란 n개의 수준(level)을 갖는 범주형 변수(Categorical variable)를 0과 1의 값(value)을 갖는 n-1개의 변수로 만드는 방법이다. 실제론 하나의 변수로 정리할 수 있지만 0과 1의 값을 갖는 가상의 변수를 갖는다고 하여 가변수라는 이름이 붙었다.  
`dummyVars`는 1개 혹은 그 이상의 범주형 변수(Factor)들을 가변수의 (full rank보다 작은) 집합 (사실 '집합'보다는 행렬로 이해하는 것이 좀 더 직관적이다.) 으로 만드는 함수다.  

예를 들어, [`earth`](https://cran.r-project.org/web/packages/earth/index.html) 패키지의 `etitanic` 데이터셋은 2개의 범주형 변수, `pclass`(1등석, 2등석, 3등석)과 `sex`(여성, 남성)을 갖고 있다. R에서 기본적으로 지원하는 함수, `model.matrix`를 이용해 가변수를 만들 수 있다. 

```r
library(earth)
data(etitanic)
head(model.matrix(survived ~ ., data = etitanic))
```
`caret` 패키지의 `dummyVars`로는 이렇게 만들 수 있다.
```r
dummies <- dummyVars(survived ~ ., data = etitanic)
head(predict(dummies, newdata = etitanic))
```
`dummyVars`로 만든 결과를 보면 intercept 열(column)이 존재하지 않고 각 범주형 변수들의 수준대로 가변수가 만들어진 것을 볼 수 있다. 이런 특성 때문에 `dummyVars`의 결과는 `lm`과 같은 일부 model 함수들에 적용하기에 적합하지 않을 수 있다.  
> n개의 수준을 갖는 범주형 변수는 n-1개의 가변수를 생성해 표현할 수 있지만 `dummyVars`는 n개의 가변수를 생성해 표현한다. 예를 들어 m개의 범주형 변수가 존재하는 자료형에 대해 `dummyVars`로 가변수화를 시키는 경우, m개의 가변수가 추가로 생기는 것과 같다. 변수의 개수가 늘어난다는 것은 곧 [차원의 저주](https://en.wikipedia.org/wiki/Curse_of_dimensionality)에 대한 부담이 증가한다는 것과 일맥상통하므로 model 적합 및 예측에 적절하지 않을 수 있다는 것이다.  

## 3.2 0 그리고 0에 가까운 분산을 갖는 예측 변수(Zero- and Near Zero-Variance Predictors)  
종종 어떤 경우의 시뮬레이션에서는 데이터 생성 매커니즘이 단일 유일값(Single unique value. 이 경우, "0의 분산을 갖는 예측변수", “zero-variance predictor”)을 갖는 예측변수를 생성할 수 있다.  
