```r
`Caret` 패키지는 예측변수로 이뤄진 데이터셋(Predictor data) 전처리(Pre-precess)를 위한 여러 함수를 포함하고 있다. 이 함수들은 예측변수 데이터가 모두 숫자형(Numeric data)으로 이뤄져 있음을 가정하고 있기 때문에 사용하기 전에 숫자형 자료로 바꿔줘야 한다. 흔히 "더미 변수화"로 불리는 작업이 위와 같은 과정이며 `model.matrix`나 곧장 설명할 `caret` 패키지의 `dummyVars`을 사용할 수 있다. 

후에 다루겠지만, `train`의 [`recipes`](https://recipes.tidymodels.org/)


```
