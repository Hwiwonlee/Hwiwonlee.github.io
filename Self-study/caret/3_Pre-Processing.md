
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
`dummyVars`로 만든 결과를 보면 intercept 열(column)이 존재하지 않고 각 범주형 변수들의 수준대로 가변수가 만들어진 것을 볼 수 있다. 이런 특성 때문에 `dummyVars`의 결과는 `lm`과 같은 일부 모델 함수들에 적용하기에 적합하지 않을 수 있다.  
> n개의 수준을 갖는 범주형 변수는 n-1개의 가변수를 생성해 표현할 수 있지만 `dummyVars`는 n개의 가변수를 생성해 표현한다. 예를 들어 m개의 범주형 변수가 존재하는 자료형에 대해 `dummyVars`로 가변수화를 시키는 경우, m개의 가변수가 추가로 생기는 것과 같다. 변수의 개수가 늘어난다는 것은 곧 [차원의 저주](https://en.wikipedia.org/wiki/Curse_of_dimensionality)에 대한 부담이 증가한다는 것과 일맥상통하므로 모델 적합 및 예측에 적절하지 않을 수 있다는 것이다.  

## 3.2 0 그리고 0에 가까운 분산을 갖는 예측 변수(Zero- and Near Zero-Variance Predictors)  
종종 어떤 경우의 시뮬레이션에서는 데이터 생성 매커니즘이 오직 하나의 명목형 숫자값(Single unique value. 이 경우, "0의 분산을 갖는 예측변수", “zero-variance predictor”)을 갖는 예측변수를 생성할 수 있다. 이 상황에서 나무 기반 모델(Tree-based model)을 제외한 다수의 모델을 이용해 분석하면 적합 결과가 불안정하거나 적합 자체가 불가능할 수 있다.  
비슷하게, 예측변수가 매우 낮은 빈도를 갖는 적은 수의 명목형 숫자값으로 이뤄진 경우가 있다. 예를 들어, `mdrrDescr` 데이터셋의 `nR11`변수의 경우 굉장히 적은 숫자의 명목형 숫자값로 이뤄져 있으며 이마저도 상당히 불균형하다.  
```r
data(mdrr)
data.frame(table(mdrrDescr$nR11))
```
문제는 교차검증(Cross-validation)이나 부트스트랩 같이 데이터셋을 나누었을 때 분할된 표본 중 0의 분산을 갖는 예측변수가 생기거나 소수의 관측값이 모델에 지나치게 큰 영향을 미칠 수 있게 된다는 점이다. 이 "0에 가까운 분산"을 갖는 예측변수들은 모델링 전에 찾아내서 제거해야 할 필요성이 있다.   

아래의 두 값을 계산해보면 "0에 가까운 분산"을 갖는 예측변수들을 찾을 수 있다.   
* (가장 많이 등장하는 명목형 숫자값의 빈도 / 두번째로 많이 등장하는 명목형 숫자값의 빈도)를 계산(빈도수 비율, Frequency ratio) 해본다. 1에 가까우면 예측변수 안의 명목형 숫자값이 잘 분산되어 있는 것이고 값이 크면 클수록 높은 수준의 불균형을 갖고 있는 것이다.  
* "명목형 숫자값의 백분율"(Percent of unique values)란 명목형 숫자값의 개수를 전체 관측치 숫자로 나눠준 것에 100을 곱한 것(백분율이므로)으로 0에 가까울 수록 해당 예측변수가 잘게 세분화된 것이다.  

빈도수 비율이 미리 설정한 임계값(Threshold)보다 크고 명목형 숫자값의 백분율이 임계값보다 작으면 예측변수가 0에 가까운 분산을 같는 것으로 간주할 수 있다.  

하지만 우리는 명목형 숫자값이 여러 값을 갖진 않지만 균일하게 분포된 데이터를 0에 가까운 분산을 갖는다고 판단하길 원하지 않는다. 두 가지 기준을 모두 사용했다는 사실이 임의의 예측 변수가 0에 가까운 분산을 갖는다고 보증해주진 않으므로 잘못 판단하는 것을 주의해야할 것이다.  

`nearZeroVar` 함수를 이용해 MDRR 데이터셋에 "0에 가까운 분산"을 갖는 변수를 찾아볼 수 있다.(`saveMetrics`의 전달인자(Argument)를 통해서 각 변수에 대한 빈도수 비율과 명목형 숫자값의 백분율을 볼 것인지, 보지 않고 "0에 가까운 분산"을 갖는 변수의 자릿수만 받을 것인지 결정할 수 있다. 초기상태는 `FALSE`다.)

```r
nzv <- nearZeroVar(mdrrDescr, saveMetrics= TRUE)
nzv[nzv$nzv,][1:10,]
```
```r
dim(mdrrDescr)
```

```r
nzv <- nearZeroVar(mdrrDescr)
filteredDescr <- mdrrDescr[, -nzv]
dim(filteredDescr)
```
`saveMetrics=FALSE`에 의해 nearZeroVar는 "0에 가까운 분산"을 갖는 것으로 보이는 변수들의 위치를 반환한다.  

## 3.3 예측 변수들의 상관관계 확인하기(Identifying Correlated Predictors)  
상관관계가 있는 예측변수를 이용한 PLS(partial least squares) 등을 제외한 모델들에서는 상관관계가 있는 예측변수들의 상관성을 줄여야 한다.  
상관계수 행렬이 주어진 경우, `findCorrelation` 함수는 다음의 알고리즘을 따라 제거해야할, 즉 높은 수준의 상관관계를 갖고 있는 예측변수들을 지정한다.  

```r
descrCor <-  cor(filteredDescr)
highCorr <- sum(abs(descrCor[upper.tri(descrCor)]) > .999)
```
이전에 본 MDRR 데이터에서, 65개의 예측변수(원문에서는 descriptors)에 대해 거의 완벽한 상관관계(상관계수의 절대값이 0.999 이상인 경우)가 발견되었다. 가령, IAC(total information index of atomic composition)와 TIC0(total information content index (neighborhood symmetry of 0-order))는 1의 상관계수를 갖는다. 아래의 코드들은 상관계수의 절댓값이 0.75 이상인 예측변수를 제거했을 때의 상관계수의 요약통계량을 보여준다.

```r
# 제거 하지 않은 경우 
descrCor <- cor(filteredDescr)
summary(descrCor[upper.tri(descrCor)])
```
```r
# cutoff = 0.75의 값을 줘서 상관계수의 절댓값이 0.75를 넘는 예측변수를 제거한 경우
highlyCorDescr <- findCorrelation(descrCor, cutoff = .75)
filteredDescr <- filteredDescr[,-highlyCorDescr]
descrCor2 <- cor(filteredDescr)
summary(descrCor2[upper.tri(descrCor2)])
```

