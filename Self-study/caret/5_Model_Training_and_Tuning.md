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

## 5.5.1 전처리 옵션 (Pre-Processing Options)  
전에 말한 것과 같이, [`train` 함수 안의 `preProcess` arg](https://www.rdocumentation.org/packages/caret/versions/6.0-86/topics/train)에 적절한 값을 넣어 주기만 하면 `train` 함수로 모델 fitting 앞서, dataset에 전처리를 할 수 있다. 적절한 값이란 앞에서 보았듯, centering과 scaling, 결측값 채워넣기(아래에서 자세히 다루겠다), spatial sign 변환을 적용하거나 PCA나 ICA를 위한 변수 변환 등을 의미하는 값들을 의미한다. 이 값들은 "문자형"으로 들어가야하며 [`preProcess` 함수](https://topepo.github.io/caret/pre-processing.html)에서 `method`에 사용되는 값과 같다. `trainControl` 함수를 통해 `preProcess`에 대한 추가적인 옵션을 사용할 수 있다.  
이러한 전처리 과정은 `predict.train`, `extractPrediction` 혹은 `extractProbs`(이 두 함수는 이 장의 뒤에서 알아보도록 하자) 등의 함수를 이용한 예측 변수 처리 과정동안 똑같이 사용할 수 있다. `preProcess`를 사용한 전처리는 `object$finalModel` 객체를 직접적으로 이용한 예측에는 **사용할 수 없다**.  
결측값을 채워넣는 방법에 한해, 사용할 수 있는 다음의 세 가지 방법이 있다.  
  - k-nearest neighbors 방법은 결측치가 포함된 샘플을 가지고 training set에서 가장 가까운 k개의 샘플을 구한다. 해당 예측 변수에 대한 결측값을 채우기 위해 k개의 training set의 값을 평균내어 결측값을 대체한다. training set 샘플의 거리를 계산할 때, 계산 과정에서 사용된 예측 변수는 해당 표본에서 결측치가 없고 training set에서도 결측치가 없는 변수이다. 
  - 또 다른 방법은 training set을 이용해 각 예측 변수에 대한 bagged tree model을 적합시키는 것이다. bagged tree model은 일반적으로 꽤 정확한 모델이며 결측치를 다루기에도 좋은 방법이다. 표본에서 예측 변수에 결측치를 채워넣을 때, 다른 예측 변수들의 값들이 bagged tree를 통해 모델을 계산해내고 새로운 값을 예측하여 내놓는다. 이 방법은 상당한 양의 계산 과정이 필요하므로 충분한 시간을 갖고 실행하거나 높은 수준의 계산 능력을 갖춘 장비로 실행하길 권한다. 
  - 매우 간단한 방법으로, 결측치가 포함된 예측 변수의 중앙값으로 결측치를 채우는 방법이 있다.  

training set 안에 결측치가 있다면 PCA와 ICA 모델은 결측치가 없는 예측 변수들만으로 구성된 training set을 사용하여 fitting된다.  

## 5.5.2 tuning grid 설정 (Alternate Tuning Grids)  
`train`에서 tuning paramter grid가 만족스럽지 못하다면(사용자에 따라 혹은 경우에 따라 너무 촘촘하다고 생각할 수도 혹은 너무 넉넉하다고 생각할 수도 있다) grid를 따로 설정할 수 있다. `tuneGrid` arg에 각 tuning parameter를 열로 갖는 데이터 프레임을 넣어 grid를 설정할 수 있다. 앞서 본 RDA 예제에서, `gamma`와 `lambda`의 tuning parameter grid를 설정해보자. `expand.grid`로 정의한 grid를 `train`에 넣으면 설정된 grid를 사용해 parameter tuning이 실행된다. 
boosted tree model을 사용한다면, learning rate를 고정할 수 있고 3개 이상의 `n.trees`를 평가할 수 있다.  
```r
gbmGrid <-  expand.grid(interaction.depth = c(1, 5, 9), 
                        n.trees = (1:30)*50, 
                        shrinkage = 0.1,
                        n.minobsinnode = 20)
                        
nrow(gbmGrid)

set.seed(825)
gbmFit2 <- train(Class ~ ., data = training, 
                 method = "gbm", 
                 trControl = fitControl, 
                 verbose = FALSE, 
                 ## Now specify the exact models 
                 ## to evaluate:
                 tuneGrid = gbmGrid)
gbmFit2
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
##   interaction.depth  n.trees  Accuracy  Kappa
##   1                    50     0.78      0.56 
##   1                   100     0.81      0.61 
##   1                   150     0.82      0.63 
##   1                   200     0.83      0.65 
##   1                   250     0.82      0.65 
##   1                   300     0.83      0.65 
##   :                   :        :         : 
##   9                  1350     0.85      0.69 
##   9                  1400     0.85      0.69 
##   9                  1450     0.85      0.69 
##   9                  1500     0.85      0.69 
## 
## Tuning parameter 'shrinkage' was held constant at a value of 0.1
## 
## Tuning parameter 'n.minobsinnode' was held constant at a value of 20
## Accuracy was used to select the optimal model using the largest value.
## The final values used for the model were n.trees = 1200,
##  interaction.depth = 9, shrinkage = 0.1 and n.minobsinnode = 20.
```
"random search"([pdf](http://www.jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf)), 즉 가능한 tuning parameter 조합에서 무작위 추출을 이용한 parameter tuning 방법도 사용할 수 있다. 이 방법에 대한 내용은 [이 페이지](https://topepo.github.io/caret/random-hyperparameter-search.html)를 참고하자.  
random search를 사용하기 위해서는 `trainControl`에서 search = "random"을 입력해주어야 한다. 이 경우, `tuneLength` parameter는 parameter 조합의 전체 개수로 정의된다.  

### 5.5.3 그림을 이용해 Resampling들의 성능 지표 표현하기 (Plotting the Resampling Profile)  
`plot` 함수를 이용하면 계산된 성능 지표와 tuning parameter들의 관계를 한 눈에 알아볼 수 있다. 가령, `plot`에 아무런 arg로 설정하지 않은 채로 `train`의 결과만을 넣으면 첫 번째의 성능 지표를 기준으로 그림을 그려준다. 
```r
trellis.par.set(caretTheme())
plot(gbmFit2)  
```
<img src = "https://topepo.github.io/caret/basic/train_plot1-1.svg">
다른 성능 지표를 기준으로 그림을 그려보고 싶다면 `metric`에서 지정해주면 된다.  
```r
trellis.par.set(caretTheme())
plot(gbmFit2, metric = "Kappa")
```
<img src = "https://topepo.github.io/caret/basic/train_plot2-1.svg">
다른 형태의 그림도 그릴 수 있다. [?plot.train](https://rdrr.io/cran/caret/man/plot.train.html)에 더욱 자세한 내용이 있으니 참고하자. 한 가지 예로 아래의 코드를 이용하면 `plot`으로 hitmap을 그릴 수 있다.  
```r
trellis.par.set(caretTheme())
plot(gbmFit2, metric = "Kappa", plotType = "level",
     scales = list(x = list(rot = 90)))
```
<img src = "https://topepo.github.io/caret/basic/train_plot3-1.svg">
더불어, 흔히 사용하는 `ggplot`으로도 그릴 수 있다.   

```r
ggplot(gbmFit2) 
```

<img src = "https://topepo.github.io/caret/basic/train_ggplot1-1.svg">

`caret` 패키지는 `plot`이외에도 resampling들로부터 계산된 성능 지표를 좀 더 자세히 그릴 수 있는 `xyplot.train`([histogram.train](https://rdrr.io/cran/caret/man/histogram.train.html), [xyplot.resamples](https://rdrr.io/cran/caret/man/xyplot.resamples.html)) 함수를 지원한다.  
> ?xyplot.train으로 검색해보면 `histogram.train`이 나오고 rdrr에서 검색해보면 xyplot.resamples가 나온다. 좀 더 이상한 건 실제 R에서 사용할 때는 둘 다 나오지 않고 `xyplot`이 그 자체로 존재한다. 아마, [`lattice`](https://rdrr.io/cran/lattice/man/Lattice.html) 패키지로부터 참조해서 사용하는 구조 같은데, 그럼 `lattice` 패키지 안의 [`xyplot`의 도움말](https://rdrr.io/cran/lattice/man/xyplot.html)을 보는 게 더 낫지 않을까?   

위와 같은 그림을 유지한 상태에서 다른 tuning parameters들을 표현하고 싶은 경우도 있을 것이다. [`update.train`](https://rdrr.io/cran/caret/man/update.train.html)을 사용하면 처음부터 전체 과정을 반복할 필요없이 최종 모델에 재적합 시켜 결과값만 바꿀 수 있다.  

