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
