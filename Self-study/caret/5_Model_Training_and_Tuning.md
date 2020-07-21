## 5.1 모델 트레이닝과 파라매터 조정 (Model Training and Parameter Tuning)  
[`caret`](https://cran.r-project.org/web/packages/caret/index.html) 패키지에는 모델 수립과 평가 과정을 효율적으로 처리할 수 있도록 돕는 여러 함수들이 있다.  
그 중 하나인 `train` 함수는 다음과 같이 사용할 수 있다. 
  - resampling의으로 여러 모델 튜닝 파라메터들을 비교하면서 평가지표에 따른 성능평가를 할 때
  - 최적의 모델 튜닝 파라메터를 선택할 때
  - 트레이닝 셋으로부터 모델 성능을 추정하고 싶을 때  

`train`함수를 사용하기 이전에 먼저, 사용하고자 하는 모델을 선택해야 한다. 현재, [`caret`](https://cran.r-project.org/web/packages/caret/index.html)에서 238개의 모델을 사용할 수 있으며 [`train` Model List](https://topepo.github.io/caret/available-models.html)나 [`train`Models By Tag](https://topepo.github.io/caret/train-models-by-tag.html)를 통해 모델들에 대한 자세한 사항을 확인할 수 있다. 이번 장에서는 최적화 대상이 되는 파라메터들을 알아보고 실제로 최적화 작업을 해보겠다. 또한 [Using Your Own Model in train](https://topepo.github.io/caret/using-your-own-model-in-train.html)도 다뤄보겠다.  

모델을 조정하는 첫 번째 단계(아래의 알고리즘의 첫 줄이다.)는 조정의 대상이 되는 파라메터들을 선택하는 것이다. 예를 들어, Partial Least Squares(PLS)에 적합시키고 싶다면 PLS components들의 개수를 조정하고자 하는(혹은 성능을 비교해보고자 하는) 파라메터로 특정할 수 있다.  
<img src= "https://topepo.github.io/caret/premade/TrainAlgo.png">  

사용할 모델과 조정할 파라메터 값을 설정했다면, resampling의 유형 또한 결정해야 한다. 현재, k-fold cross-validation (한번 혹은 n번 반복해 시행하는), leave-one-out cross-validation(LOOCV), bootstrap(기본적인 방법 혹은 632 rule을 이용한 방법) 등의 resampling 방법들을 `train`에서 사용할 수 있다. resampling 후에, 조정 과정에서의 성능 측정 프로필을 생성해 사용자가 어떤 튜닝 파라메터 값을 선택해야 하는지 확인할 수 있다. 기본적으로 `train`은 다른 알고리즘을 사용하기보다는 해당 알고리즘에서의 가장 좋은 값을 갖는 튜닝 파라메터를 선택하도록 되어 있다.(자세한 내용은 차차 나올 것이다.)

## 5.2 예제 (An Example)  
Sonar data는 [`mlbench`](https://cran.r-project.org/web/packages/mlbench/index.html) 패키지에서 불러올 수 있다.  
```r
library(mlbench)
data(Sonar)
str(Sonar[, 1:10])
```
```r
## 'data.frame':    208 obs. of  10 variables:
##  $ V1 : num  0.02 0.0453 0.0262 0.01 0.0762 0.0286 0.0317 0.0519 0.0223 0.0164 ...
##  $ V2 : num  0.0371 0.0523 0.0582 0.0171 0.0666 0.0453 0.0956 0.0548 0.0375 0.0173 ...
##  $ V3 : num  0.0428 0.0843 0.1099 0.0623 0.0481 ...
##  $ V4 : num  0.0207 0.0689 0.1083 0.0205 0.0394 ...
##  $ V5 : num  0.0954 0.1183 0.0974 0.0205 0.059 ...
##  $ V6 : num  0.0986 0.2583 0.228 0.0368 0.0649 ...
##  $ V7 : num  0.154 0.216 0.243 0.11 0.121 ...
##  $ V8 : num  0.16 0.348 0.377 0.128 0.247 ...
##  $ V9 : num  0.3109 0.3337 0.5598 0.0598 0.3564 ...
##  $ V10: num  0.211 0.287 0.619 0.126 0.446 ...
```
`createDataPartition` 함수를 사용하면 데이터셋의 균형을 유지한 상태(stratified random sampling)로 데이터셋을 트레이닝 셋과 테스트 셋으로 나눌 수 있다.  
```r
library(caret)
set.seed(998)
inTraining <- createDataPartition(Sonar$Class, p = .75, list = FALSE)
training <- Sonar[ inTraining,]
testing  <- Sonar[-inTraining,]
```

## 5.3 파라메터 튜닝의 기초 (Basic Parameter Tuning)   
기본적으로, 별 다른 설정을 하지 않은 상태의 bootstrap resampling은 위의 알고리즘 3과 같다. 물론 repeated K-fold CV나 LOOCV 등과 같은 resampling 방법도 같은 알고리즘을 사용한다. `trainControl`에서 resampling 방법을 선택할 수 있다. 
```r
fitControl <- trainControl(## 10-fold CV
                           method = "repeatedcv",
                           number = 10,
                           ## repeated ten times
                           repeats = 10)
```

`trainControl`에 대한 자세한 내용을 [여기](https://topepo.github.io/caret/model-training-and-tuning.html#custom)를 참고하자.
트레이닝을 위한 처음 두 개의 arg는 예측 변수와 결과 변수의 관계와 이들을 불러올 데이터셋이다. 세 번째 arg는 사용할 모델의 유형을 의미한다. (사용할 수 있는 모델들과 그에 대한 자세한 내용은 [`train` Model List](https://topepo.github.io/caret/available-models.html)나 [`train`Models By Tag](https://topepo.github.io/caret/train-models-by-tag.html)를 참고하자.) 실습을 위해 [`gbm`](https://cran.r-project.org/web/packages/gbm/index.html)(Gradient Boosting Machine) 패키지를 이용해 bootsed tree model에 적합시켜볼 것이다. 이를 위한 기본적인 코드는 아래와 같다. resampling 방법으로는 repeated cross-validation를 사용했다. 
```r
set.seed(825)
gbmFit1 <- train(Class ~ ., data = training, 
                 method = "gbm", 
                 trControl = fitControl,
                 ## This last option is actually one
                 ## for gbm() that passes through
                 verbose = FALSE)
gbmFit1
```
```r
## Stochastic Gradient Boosting 
## 
## 157 samples
##  60 predictor
##   2 classes: 'M', 'R' 
## 
## No pre-processing
## Resampling: Cross-Validated (10 fold, repeated 10 times) 
## Summary of sample sizes: 141, 142, 141, 142, 141, 142, ... 
## Resampling results across tuning parameters:
## 
##   interaction.depth  n.trees  Accuracy   Kappa    
##   1                   50      0.7935784  0.5797839
##   1                  100      0.8171078  0.6290208
##   1                  150      0.8219608  0.6386184
##   2                   50      0.8041912  0.6027771
##   2                  100      0.8302059  0.6556940
##   2                  150      0.8283627  0.6520181
##   3                   50      0.8110343  0.6170317
##   3                  100      0.8301275  0.6551379
##   3                  150      0.8310343  0.6577252
## 
## Tuning parameter 'shrinkage' was held constant at a value of 0.1
## 
## Tuning parameter 'n.minobsinnode' was held constant at a value of 10
## Accuracy was used to select the optimal model using the largest value.
## The final values used for the model were n.trees = 150,
##  interaction.depth = 3, shrinkage = 0.1 and n.minobsinnode = 10.
```
gradient boosting machine (GBM) model의 대표적인 튜닝 파라메터들을 다음과 같다. 
  - 반복 수, 즉 trees의 개수(n.trees)
  - tree의 복잡도(interaction.depth)
  - learning rate, 얼마나 빠르게 알고리즘을 습득할 것인지를 결정하는 파라메터(shrinkage)
  - training set을 이용해 node를 나눌 때 기준이 될 최소 샘플 갯수(n.minobsinnode)

위 모델의 tuning parameter의 테스트 결과는 처음 두 열에 표시된다.(후보 모델의 grid set가 모두 이러한 tuning parameter에 대해 단일 값을 사용하기 때문에 shrinkage와 n.minobsinnode는 표시되지 않는다.) 정확도(Accuracy)는 여러차례 반복된 CV의 결과로 구한 평균 정확도이다. 표준편차 또한 반복된 CV의 결과를 평균내어 구할 수 있다. Kappa([wiki](https://en.wikipedia.org/wiki/Cohen%27s_kappa), [추가 설명](https://thedatascientist.com/performance-measures-cohens-kappa-statistic/))는 Cohen's(unweighted) Kappa 통계량을 의미하며 여기서는 각 resampling 결과들의 kappa를 평균하여 구한 값이다. 이와 같이 `train`을 사용해 특정 모델을 설정하여 훈련 시킬 수 있다. `train`에서 사용할 모델을 설정하면, 자동적으로 grid 디자인의 tuning paramters 테스트를 진행하고 결과를 저장한다. 기본적으로 p가 tuning parameter의 개수라면 grid의 크기는 3^p가 된다. 또 다른 예로 Regularized Discriminant Analysis(RDA) 모델은 2개의 parameter(`gamma`와 `lambda`)를 갖는데, 두 parameter 모두 0과 1사이에 존재한다. 따라서 트레이닝 grid는 2차원 공간의 3^2 = 9개의 조합으로 구성된다.  

## 5.4 재현성에 대하여 (Notes on Reproducibility)  
많은 모델들이 parameter를 추정하는데 난수를 사용한다. 또한 resampling index도 난수를 사용한다. 재현가능한 결과를 위해 무작위성을 조정하는 대표적인 두 가지 방법을 알아보자.   
  - `train`에서 재현성을 갖도록 항상 같은 resample들을 사용하도록 하는 두 가지 방법이 있다. 첫 번째는 `train`을 실행하기 전에 `set.seed`에서 seed number를 설정하는 것이다. 이 방법을 사용하면 난수들이 고정되어 resampling에 대한 정보가 남고 같은 resampling을 재현할 수 있게 된다. 데이터셋을 나누기 위해 설정한 방법이 있다면, `trainControl`의 `index` arg를 사용할 수 있다. 이 부분은 위에서 간단히 설명했었으니 참고하길 바란다.   
  - resampling 안에서 모델을 만들고자 할 때 재현성을 갖추려면 seed들 또한 설정해야 한다. `train`을 실행하기 전에 seed를 설정하면 항상 같은 난수를 생성해 재현성을 갖도록 하지만 [병렬처리 환경](https://topepo.github.io/caret/parallel-processing.html)에서는 재현성을 갖지 못하게 될 수도 있다(이 부분은 병렬 처리에 대한 기술적 문제이다.). 모델 fitting seeds를 설정하기 위해 `trainControl`의 `seeds` arg를 사용할 수 있다. `set.seeds`의 사용법과 마찬가지로 `seeds`에 seeds로 사용할 정수 벡터의 리스트를 넣어 사용한다. `trainControl`의 도움말에서 `seeds` arg의 적절한 사용 방법을 볼 수 있으니 참고하길 바란다.  

패키지가 어떤 언어를 기반으로 하느냐에 따라 난수의 재현성 확보 여부가 불가능한 경우가 있다(물론 대부분 가능하다. 재현성은 굉장히 중요한 문제다.). 특별히 C 언어로 계산 과정이 실행되는 경우, 난수에 대한 seed를 설정할 수 없는 경우는 정말 드물다. 또한 일부 패키지는 load되는 순간에 난수도 함께 load되어(직접적으로 혹은 namespace를 통해서) 재현성에 영향을 미치기도 하니 주의해야 할 것이다. 

## 5.5 파라메터 튜닝을 해보자 (Customizing the Tuning Process)  
Tuning/complexity parameters를 선택하고 최종 모델을 만드는 과정을 알아보자. 


 
