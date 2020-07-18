
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

## 3.4 선형 종속과 선형 독립(Linear Dependencies)  
함수 `findLinearCombos`는 QR 분해(QR decomposition)을 사용해 행렬의 선형 조합들의 집합들(sets of linear combinations)을 보여준다.(만약, 존재한다면) 예를 들어, less-than-full-rank parameterizations에 의해 만들어진 것으로 보이는 아래의 행렬을 살펴보자. 

```r
ltfrDesign <- matrix(0, nrow=6, ncol=6)
ltfrDesign[,1] <- c(1, 1, 1, 1, 1, 1)
ltfrDesign[,2] <- c(1, 1, 1, 0, 0, 0)
ltfrDesign[,3] <- c(0, 0, 0, 1, 1, 1)
ltfrDesign[,4] <- c(1, 0, 0, 1, 0, 0)
ltfrDesign[,5] <- c(0, 1, 0, 0, 1, 0)
ltfrDesign[,6] <- c(0, 0, 1, 0, 0, 1)
```

2열과 3열을 합치면 1열이 됨을 볼 수 있다. 비슷하게, 4,5,6열을 합치면 1열이 된다. `findLinearCombos`를 사용한다면 이러한 "종속성"을 볼 수 있을 것이다. 각각의 선형 조합에 대해 점진적으로 열을 제거하고 종속성이 제거되었는지 여부를 테스트한다. `findLinearCombos`는 선형 종속에 의해 삭제된 열 벡터의 위치 또한 알려줄 것이다. 

```r
comboInfo <- findLinearCombos(ltfrDesign)
comboInfo
```

```r
ltfrDesign[, -comboInfo$remove]
```
이러한 유형의 종속성들은 분자구조를 설명하기 위해 많은 수의 이진 케미컬 fingerprint들을 사용할 때 발생할 수 있다.  

## 3.5 `preProcess` 함수(The `preProcess` Function)  
`preProcess` 클래스는 중심화와 척도 표준화(centering and scaling)을 포함하여, 예측 변수에 대한 많은 연산에 사용할 수 있다. 함수 `preProcess`는 각각의 연산에 필요한 매개변수들을(parameters) 추정하고 `predict.preProcess`는 특정한 데이터 셋에 추정된 값을 적용할 때 사용할 수 있다. 이 함수는 `train` 함수를 사용할 때 인터페이스로도 사용할 수 있다.  

다음 몇 개의 섹션에서 사용 방법의 여러 유형을 알려주고 어떻게 여러 방법들로 사용되는지에 대한 예시들 또한 보여주겠다. 모든 경우에 있어서, `preProcess` 함수는 필요한 값이 무엇이든 특정한 데이터 셋(가령, 트레이닝 셋)으로부터 추정한 후 다시 계산하지 않고 모든 데이터 셋에 그 값을 적용한다는 것을 꼭 알아두길 바란다.  

## 3.6 중심화와 척도 표준화(Centering and Scaling)  
아래의 예에서와 같이, MDRR dataset의 절반을 이용해 예측 변수의 위치와 척도(the location and scale)를 추정하고자 한다. 이 예제에서 함수 `preProcess`는 이름과 다르게 전처리에 사용되지 않았다. 이 예제나 다른 데이터 셋을 이용한 전처리에 함수 `predict.preProcess`가 사용되었다.  
```r
set.seed(96)
inTrain <- sample(seq(along = mdrrClass), length(mdrrClass)/2)

training <- filteredDescr[inTrain,]
test <- filteredDescr[-inTrain,]
trainMDRR <- mdrrClass[inTrain]
testMDRR <- mdrrClass[-inTrain]

preProcValues <- preProcess(training, method = c("center", "scale"))

trainTransformed <- predict(preProcValues, training)
testTransformed <- predict(preProcValues, test)
```
`preProcess`의 옵션 중 "range"를 설정하면 척도 표준화를 0과 1사이로 해준다.  

## 3.7 결측값 채워넣기(Imputation)  
`preProcess`를 학습 데이터 셋의 정보에만 기반하여 결측값을 채워넣는데 사용할 수 있다. K-근접 이웃 방법이 그 중 하나이다. 임의의 샘플에 대하여, K-최근접 이웃 방법은 학습 데이터 셋과 그에 포함된 예측변수들을 이용해 결측값을 대체한다.(보통 평균이나 중간값과 같은 요약 통계량이 쓰인다.) 이 접근법을 사용하면 메서드 인수에 있는 내용에 관계없이 데이터를 중심화하고 척도표준화를 시키는 `preProcess`가 자동으로 설정된다. 결측값 대체를 위한 다른 방법으로, bagged tree 방법을 들 수 있다. 데이터의 각각의 예측 변수에 대하여, 학습 데이터 셋의 다른 모든 변수를 사용해 bagged tree(혹은 bagged 모형)가 만들어진다. 새로운 샘플이 결측값이 포함된 예측 변수를 갖는다면, bagged 모형을 사용해 그 값을 예측해낼 수 있다. 이론 상으로는 이 방법이 결측값 대체에 가장 강력한 방법이지만 계산량은 그 이상으로, 최근접 이웃 방법보다 압도적으로 많다. 

## 3.8 예측 변수 변환 (Transforming Predictors)  
종종, 주성분 분석(Principal Component Analysis, PCA)을 위해 데이터셋을 예측 변수간 상관관계가 없거나 극히 작도록 만들어야 한다. 이렇게 만들어진 데이터셋은 이전 예측 변수와는 다른 예측 변수를 갖고 차원 수 또한 매우 줄어든 상태가 된다. `preProcess` 클래스는 `"pca"`를 포함한 예측 변수 변환을 지원하며 이를 위한 인자(argument)를 갖는다. 예측 변수 변환에는 예측 변수 사이의 척도 표준화가 강제된다. 주성분 분석이 예측 변수 변환을 위한 방법 인자(method argument)로 들어간 경우, `predict.preProcess`는 열 이름을 `PC1`(Principal Component 1, 첫 번째 주성분), `PC2` 등으로 바꾼다.  
이와 유사하게, 독립 성분 분석(Independent Component Analysis, ICA)은 원래 데이터 셋에서 선형 독립인 예측변수와 같이 선형 조합을 갖는 새로운 예측 변수를 찾는다.(상관관계가 없도록 만드는 PCA와는 반대이다.) 새로운 변수는 `IC1`(Independent Component 1, 첫 번째 독립성분), `IC2` 등으로 이름이 붙는다.  
“spatial sign” transformation (Serneels et al, 2006)는 데이터셋의 예측 변수를 p 차원을 갖는 unit circle로 투영시키는 방법이다. 이 때의 p는 예측 변수의 숫자를 의미한다. [근본적으로, 데이터 셋의 벡터는 그 노름(norm)에 의해 나뉘어질 수 있다.](http://pages.cs.wisc.edu/~matthewb/pages/notes/pdf/linearalgebra/NormedVectorSpaces.pdf) 아래의 두 그림은 spatial sign transformation의 전과 후를 비교하기 위해 중심화, 척도 표준화된 MDRR 데이터셋으로 그린 것이다. spatial sign transformation를 사용하기 전에, 대상이 되는 예측변수들은 모두 중심화, 척도 표준화가 이뤄져야 한다.  

```r
library(AppliedPredictiveModeling)
transparentTheme(trans = .4)
```
```r
plotSubset <- data.frame(scale(mdrrDescr[, c("nC", "X4v")])) 
xyplot(nC ~ X4v,
       data = plotSubset,
       groups = mdrrClass, 
       auto.key = list(columns = 2))  
```
spatial sign transformation 후의 그림이다.  
```r
transformed <- spatialSign(plotSubset)
transformed <- as.data.frame(transformed)
xyplot(nC ~ X4v, 
       data = transformed, 
       groups = mdrrClass, 
       auto.key = list(columns = 2)) 
```
또 다른 옵션으로, 데이터셋이 0보다 큰 경우 사용할 수 있는 Box–Cox transformation를 위한 `"BoxCox"`가 있다.  
```r
preProcValues2 <- preProcess(training, method = "BoxCox")
trainBC <- predict(preProcValues2, training)
testBC <- predict(preProcValues2, test)
preProcValues2
```

```r
## Created from 264 samples and 31 variables
## 
## Pre-processing:
##   - Box-Cox transformation (31)
##   - ignored (0)
## 
## Lambda estimates for Box-Cox transformation:
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
## -2.0000 -0.2500  0.5000  0.4387  2.0000  2.0000
```
`NA`는 Box–Cox transformation로 변환할 수 없는 예측 변수들과 관련있는 결측값이다. 이 변환은 대상이 되는 데이터셋의 값이 0보다 커야만 한다. 이와 유사한 예측 변수 변환 방법으로 Yeo-Johnson과 Manly의 지수 변환(1976) 등도 `preProcess`에서 사용 가능하다.  

## 3.9 총 정리(Putting It All Together)  
책, [Applied Predictive Modeling](http://appliedpredictivemodeling.com/)에서 고성능 컴퓨팅 환경에서 작업 실행 시간을 예측하는 사례연구를 보자. 데이터는 다음과 같다.  

```r
library(AppliedPredictiveModeling)
data(schedulingData)
str(schedulingData)
```
```
## 'data.frame':    4331 obs. of  8 variables:
##  $ Protocol   : Factor w/ 14 levels "A","C","D","E",..: 4 4 4 4 4 4 4 4 4 4 ...
##  $ Compounds  : num  997 97 101 93 100 100 105 98 101 95 ...
##  $ InputFields: num  137 103 75 76 82 82 88 95 91 92 ...
##  $ Iterations : num  20 20 10 20 20 20 20 20 20 20 ...
##  $ NumPending : num  0 0 0 0 0 0 0 0 0 0 ...
##  $ Hour       : num  14 13.8 13.8 10.1 10.4 ...
##  $ Day        : Factor w/ 7 levels "Mon","Tue","Wed",..: 2 2 4 5 5 3 5 5 5 3 ...
##  $ Class      : Factor w/ 4 levels "VF","F","M","L": 2 1 1 1 1 1 1 1 1 1 ...
```
데이터는 숫자형 예측 변수들과 명목형 예측 변수들로 이뤄져 있다. 이제 우리가 연속형 예측 변수들에 중심화와 척도 표준화를 시킨 뒤 Yeo-Johnson 변환의 작업을 한다고 가정해보자. 또한 나무 기반 모형(Tree-based model)을 사용할 것으로 가정하여 명목형 예측 변수들의 더미변수화를 하지 않을 것이다. 마지막 예측 변수, Class를 제외한 예측 변수로 위의 과정을 실행한 뒤 결과를 확인해보자.  
```r
pp_hpc <- preProcess(schedulingData[, -8], 
                     method = c("center", "scale", "YeoJohnson"))
pp_hpc
```
```r
## Created from 4331 samples and 7 variables
## 
## Pre-processing:
##   - centered (5)
##   - ignored (2)
##   - scaled (5)
##   - Yeo-Johnson transformation (5)
## 
## Lambda estimates for Yeo-Johnson transformation:
## -0.08, -0.03, -1.05, -1.1, 1.44
```
```r
transformed <- predict(pp_hpc, newdata = schedulingData[, -8])
head(transformed)
```
```r
##   Protocol  Compounds InputFields Iterations NumPending         Hour Day
## 1        E  1.2289592  -0.6324580 -0.0615593  -0.554123  0.004586516 Tue
## 2        E -0.6065826  -0.8120473 -0.0615593  -0.554123 -0.043733201 Tue
## 3        E -0.5719534  -1.0131504 -2.7894869  -0.554123 -0.034967177 Thu
## 4        E -0.6427737  -1.0047277 -0.0615593  -0.554123 -0.964170752 Fri
## 5        E -0.5804713  -0.9564504 -0.0615593  -0.554123 -0.902085020 Fri
## 6        E -0.5804713  -0.9564504 -0.0615593  -0.554123  0.698108782 Wed
```
두 개의 예측변수가 "무시됨"(ignored)으로 표시된 것은 7개의 예측 변수 중 중심화가 불가능한 명목형 예측 변수가 2개 있기 때문이다. 그러나 숫자형으로 저장되어 있어 걸러내지 못한 NumPending 예측 변수는 매우 희박하고 불균형한 분포를 갖는다. 
```r
mean(schedulingData$NumPending == 0)
```
```r
## [1] 0.7561764
```
다른 일부 모형에서 이러한 불균형한 분포를 갖는 예측 변수는 문제가 될 수 있다. (특별히, 재표집(resample)이나 [down-sample](https://en.wikipedia.org/wiki/Downsampling_(signal_processing)을 하는 경우가 그렇다.) 0 혹은 0에 가까운 분산을 갖는 예측 변수가 있는지 확인하고 걸러내는 작업을 `preProcess`에 추가해보자. 
```r
pp_no_nzv <- preProcess(schedulingData[, -8], 
                        method = c("center", "scale", "YeoJohnson", "nzv"))
pp_no_nzv
```
```r
## Created from 4331 samples and 7 variables
## 
## Pre-processing:
##   - centered (4)
##   - ignored (2)
##   - removed (1)
##   - scaled (4)
##   - Yeo-Johnson transformation (4)
## 
## Lambda estimates for Yeo-Johnson transformation:
## -0.08, -0.03, -1.05, 1.44
```
```r
predict(pp_no_nzv, newdata = schedulingData[1:6, -8])
```
```r
##   Protocol  Compounds InputFields Iterations         Hour Day
## 1        E  1.2289592  -0.6324580 -0.0615593  0.004586516 Tue
## 2        E -0.6065826  -0.8120473 -0.0615593 -0.043733201 Tue
## 3        E -0.5719534  -1.0131504 -2.7894869 -0.034967177 Thu
## 4        E -0.6427737  -1.0047277 -0.0615593 -0.964170752 Fri
## 5        E -0.5804713  -0.9564504 -0.0615593 -0.902085020 Fri
## 6        E -0.5804713  -0.9564504 -0.0615593  0.698108782 Wed
````
"삭제됨"(removed)로 표시된 예측 변수가 추가 되었음에 주목해보자. 우리가 추가한 인수에 의해 0이나 0에 가까운 분산을 갖는 예측 변수가 삭제되었음을 의미한다. 

## 3.10 클래스 간 거리 계산(Class Distance Calculations)  
[caret](https://cran.r-project.org/web/packages/caret/index.html) 패키지에는 class 중심으로부터의 거리에 근거해 새로운 예측 변수를 만드는(선형 판별 분석에서 사용하는 것과 비슷한 방법으로) 함수들이 포함되어 있다. 명목형 변수들의 각 수준에 대하여 class 중심과 공분산 행렬을 계산해낼 수 있다. 새로운 표본을 이용해, 각 class 중심으로부터 마할라노비스 거리([Mahalanobis distance](https://en.wikipedia.org/wiki/Mahalanobis_distance))를 계산한 후 거리 계산을 기반으로 새로운 예측 변수를 추가했다. 이는 의사 결정 경계(decision boundary)가 선형인 경우, 비 선형 모델에 유용할 수 있다. (This can be helpful for non-linear models when the true decision boundary is actually linear.)  
> 이게 정확히 무슨 의미인 지 모르겠다.  

한 class 내에서 표본보다 많은 예측 변수가 있는 경우, `classDist` 함수에서 사용 가능한 `pca`와 `keep`인자를 사용하면 주성분 분석 중, 특이 공분산 행렬(singular covariance matrix)에 발생할 수 있는 문제를 피할 수 있다. (이 부분은 선형대수의 기초 지식이 필요한 부분이다. stackoverflow에서 괜찮은 Q&A를 찾았다. [(1)](https://stats.stackexchange.com/questions/60622/why-is-a-sample-covariance-matrix-singular-when-sample-size-is-less-than-number), [(2)](https://stats.stackexchange.com/questions/108065/singular-covariance-matrix-in-exploratory-factor-analysis), [(3)](https://stats.stackexchange.com/questions/70899/what-correlation-makes-a-matrix-singular-and-what-are-implications-of-singularit))   

그 후, `predict.classDist`는 클래스 거리에 대한 예측 변수를 만들 수 있다. 초기 설정에 의하여, 클래스 거리는 남아있겠지만 `trans` 인자에 따라 바뀔 수 있다.  

예를 들어, MDRR dataset을 다시 사용해보자. 
```r
centroids <- classDist(trainBC, trainMDRR)
distances <- predict(centroids, testBC)
distances <- as.data.frame(distances)
head(distances)
```
```r
##                dist.Active dist.Inactive
## ACEPROMAZINE      3.787139      3.941234
## ACEPROMETAZINE    4.306137      3.992772
## MESORIDAZINE      3.707296      4.324115
## PERIMETAZINE      4.079938      4.117170
## PROPERICIAZINE    4.174101      4.430957
## DUOPERONE         4.355328      6.000025
```
아래의 이미지는 위의 예제에서 만들어진 클래스의 거리 변수를 이용해 그린 산점도이다. 
```r
xyplot(dist.Active ~ dist.Inactive,
       data = distances, 
       groups = testMDRR, 
       auto.key = list(columns = 2))
```
