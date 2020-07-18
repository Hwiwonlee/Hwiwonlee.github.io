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



