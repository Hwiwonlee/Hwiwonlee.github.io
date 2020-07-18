## 4.1 종속 변수를 이용해 간단히 자르기 (Simple Splitting Based on the Outcome)  
`createDataPartition` 함수는 데이터셋을 정해진 인수값에 따라 균형있게 나눈다. 종속 변수, y가 명목형 변수라면 y의 각 클래스에 따라 random sampling을 시행해 원래의 데이터셋이 가진 클래스 분포를 보존한다. 예를 들어, 붓꽃(iris) 데이터셋의 품종(Species)를 기준으로 80/20%의 비율로 나눠보자.  
```r
library(caret)
set.seed(3456)
trainIndex <- createDataPartition(iris$Species, p = .8, 
                                  list = FALSE, 
                                  times = 1)
head(trainIndex)
```
```r
##      Resample1
## [1,]         1
## [2,]         2
## [3,]         3
## [4,]         5
## [5,]         6
## [6,]         7
```
```r
irisTrain <- iris[ trainIndex,]
irisTest  <- iris[-trainIndex,]
```
`list = FALSE`는 데이터셋을 list로 받지 않기 위한 arg이다. 또한 한 번에 몇 덩이로 나눌 것인지에 대한 arg, `times`를 볼 수 있다. `createDataPartition`의 결과로 정수 벡터의 리스트를 얻을 수 있다. 비슷하게, `createResample`은 부트스트랩(Bootstrp)을 위한 간단한 샘플링을, `createResample`는 균형잡힌 교차검증(Balanced Cross-Validation)을 위한 샘플링을 지원한다. 

## 4.2 예측 변수를 이용해 데이터셋 자르기 (Splitting Based on the Predictors)
또한, `maxDissim` 함수로 maximum dissimilarity approach([Willett, 1999](https://www.liebertpub.com/doi/abs/10.1089/106652799318382))을 이용해 sub-sample를 만들 수 있다. m개의 샘플을 가진 A 데이터셋과 m개 보다 많은 n개의 샘플을 가진 B 데이터셋이 있다고 하자. 이 때, A는 B의 sub-sample임을 가정하자. A가 이미 B의 sub-sample이지만 m < n의 관계를 갖고 있으므로 우리는 A보다 다양한 B의 sub-sample을 만들고 싶어할 수도 있다. 이를 위해, B의 각 샘플에 대해 A의 각각의 포인트 사이에 대한 m개의 상이성(dissimilarity)을 계산하고 가장 크게 다른 B의 포인트를 A에 추가한 후 반복한다. R에는 상이성을 계산할 많은 방법들이 있다. [`caret`](https://cran.r-project.org/web/packages/caret/index.html)은 [`proxy`](https://cran.r-project.org/web/packages/proxy/index.html) 패키지를 이용하고 있다. 또한 "가장 다른" 샘플을 계산하는 방법도 여러가지가 있다. `obj`는 어떤 수치(scalar measure)로 결과값을 받을지 특정하는 arg이다. [`caret`](https://cran.r-project.org/web/packages/caret/index.html)은 `minDiss`와 `sumDiss`, 두가지 함수를 지원하는데, 순서대로 최소값을 최대화하거나 전체 상이성을 이용하는 함수들이다.  

예를 들어, Cox2 data에 대한 2개의 chemical descriptor을 이용해 산점도를 그리는 경우를 생각해보자. 5개의 화합물(compound)의 초기 무작위 샘플을 이용해 20개 이상의 화합물을 데이터셋에서 더 선택하려고 한다. 이 때, 선택되는 새로운 화합물은 처음 선택된 5개의 화합물과 크게 달라야 한다. (그래야 비교의 의미가 생긴다.) 그림에서 볼 수 있는 각각의 panel은 여러가지 combinations of distance와 scoring function을 사용해 결과를 보여준다. 이 데이터에서 거리 값은 선택된 혼합물이 대부분 다르므로 scoring method 보다 적은 수준의 영향력을 갖는다. 
```r
library(mlbench)
data(BostonHousing)

testing <- scale(BostonHousing[, c("age", "nox")])
set.seed(5)
## A random sample of 5 data points
startSet <- sample(1:dim(testing)[1], 5)
samplePool <- testing[-startSet,]
start <- testing[startSet,]
newSamp <- maxDissim(start, samplePool, n = 20)
head(newSamp)
```
```r
## [1] 460 142 491 156 498  82
```
아래의 시각화된 플롯은 데이터셋(작은 점)과 선택된 샘플과 20개의 샘플이 추가되는 과정을 표현한 것이다.  
<img src = "https://topepo.github.io/caret/premade/MaxDissim.gif">  


## 4.3 시간에 따라 데이터셋 자르기 (Data Splitting for Time Series)
시계열 자료라고 해도 시간에 따라 데이터셋을 자르는 것은 최고의 방법이 아닐 것이다. [Hyndman and Athanasopoulos (2013)](https://www.otexts.org/fpp/2/5)는 시간에 따라 움직이는 트레이닝, 테스트 셋의 rolling forecasting origin에 대해 다뤘었다. `caret`은 이러한 데이터셋 자르기를 `createTimeSlices` 함수를 통해 지원한다.  
`createTimeSlices`에는 다음과 같은 3개의 매개변수가 존재한다. 
  - `initialWindow` : 각 트레이닝 셋 샘플의 크기. 이 때, 트레이닝 셋 샘플은 랜덤하게 뽑히는 것이 아닌 시간순서와 같이 연속적으로 뽑힌다. 
  - `horizon` : 테스트 셋 샘플의 크기, 트레이닝 셋과 마찬가지로 연속적인 순서에 따라 뽑히며 `horizon`에 설정된 크기를 초과하면 데이터셋 자르기는 종료된다.  
  - `fixedWindow` : 논리형. `FALSE`인 경우, 트레이닝 셋은 항상 첫 번째 샘플에서 시작하고 트레이닝 셋의 크기는 자르는 횟수에 따라 달라진다.  

예를 들어, 20개의 data points를 갖고 있는 시계열 자료를 갖고 있다고 해보자. `initialWindow = 5`을 설정하고 다른 두 agr에 따른 변화를 아래의 그림에서 살펴볼 수 있다. 아래 그림에서 행은 다르게 잘린 각각의 샘플이고 열은 다른 시점의 data point이다. 또한 붉은색은 트레이닝 셋을 의미하며 파란색은 테스트셋을 의미한다. 
<img src="https://topepo.github.io/caret/splitting/Split_time-1.svg">

## 4.4 중요한 그룹들이 포 데이터셋 자르기 (Simple Splitting with Important Groups)  
종종, 데이터 안에 중요한 명목형 변수가 있어 이를 샘플링 혹은 리샘플링 단계에서 고려해야 하는 경우가 있다. 예를 들어 :  
  - 임상시험에서 병원간 차이에 대한 변수  
  - 경시적 혹은 반복 측정 데이터처럼, 대상 (혹은 일반적인 독립적 실험 개체)이 데이터셋 안에서 여러 행을 가질 경우  
중요한 명목형 변수를 포함한 테스트셋은 모델의 성능을 다소 낙관적으로 보게 하는 편향을 갖기 때문에 이러한 그룹이 트레이닝 셋이나 테스트 셋에 포함되지 않도록 하는 것에 관심이 있을 수 있다. Also, when one or more specific groups are held out, the resampling might capture the “ruggedness” of the model. 여러 지점을 검사하여 기록한 임상실험 데이터셋을 가정해보면, 리샘플링 성능 추정치는 여러 검사 지점 사이에서 모델이 얼마나 확장 가능한지를 부분적으로 측정값이다.  

데이터셋을 그룹에 따라 나누려면 `groupKFold`를 사용하면 된다.
```r
set.seed(3527)
subjects <- sample(1:20, size = 80, replace = TRUE)
table(subjects)
```
```r
## subjects
##  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 
##  2  3  2  5  3  5  4  5  4  4  2  5  4  2  3  3  6  7  8  3
```
```r
folds <- groupKFold(subjects, k = 15) 
```
`folds`의 결과는 `trainControl`함수의 `index` arg에 사용될 수 있다.  
이 그림은 각 대상들이 모델링과 홀드아웃 사이에서 어떻게 분할되는지 보여준다. `folds`를 만들 때 `k`의 값을 20보다 작게 주었기 대문에, 홀드아웃 집합에 속하는 대상들이 하나 이상인 경우가 있게 되었다. 
<img src="https://topepo.github.io/caret/splitting/Split_group_plot-1.svg">
