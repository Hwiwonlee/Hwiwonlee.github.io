
`Caret` 패키지는 예측변수로 이뤄진 데이터셋(Predictor data) 전처리(Pre-precess)를 위한 여러 함수를 포함하고 있다. 이 함수들은 예측변수 데이터가 모두 숫자형(Numeric data)으로 이뤄져 있음을 가정하고 있기 때문에 사용하기 전에 숫자형 자료로 바꿔줘야 한다. 흔히 "더미 변수화"로 불리는 작업이 위와 같은 과정이며 `model.matrix`나 곧장 설명할 `caret` 패키지의 `dummyVars`을 사용할 수 있다. 

후에 다루겠지만, `train`와 [`recipes`](https://recipes.tidymodels.org/)를 사용해서 전처리 과정에서 더욱 다양하고 사용자의 입맛대로 설정 가능한 옵션들을 어떻게 다룰 수 있는지 알려주도록 하겠다. 

## 3.1 가변수(Dummy Variables) 만들기  
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
