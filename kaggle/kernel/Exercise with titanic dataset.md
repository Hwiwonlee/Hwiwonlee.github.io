## 들어가기 전에
남들 다 하는 Kaggle을 시작하기 위해 그나마 가장 익숙한 [titanic dataset](https://www.kaggle.com/c/titanic)을 골랐다. Python을 이용해 작성하는 첫 kaggle kernel이라 많이 버벅이겠지만, 그 맛에 공부 하는 거지.

# 1. Introduction of competiton
titanic dataset은 'isis dataset'과 더불어 굉장히 많이 쓰이는 example dataset이다. titanic dataset을 이용한 kaggle competition의 목적은 **주어진 dataset을 이용해 타이타닉이 가라앉은 상황에서 승객들의 생존여부를 예측하는 것**이다. 생존 혹은 사망의 binary classification이므로 평가 기준은 다음의 [accuracy score](https://en.wikipedia.org/wiki/Accuracy_and_precision#In_binary_classification)이다. kaggle에서 제공하는 raw dataset은 'train'과 'test'으로 실제로 data analysis에 사용되는 raw dataset처럼 missing value 및 outlier도 존재한다. 따라서 competition에 참가하는 참가자들은 preprocessing부터 model fitting까지 차근차근 연습해볼 수 있다.

# 2. Datasets overview
어떻게 나눌지는 모르겠지만 일단, 쭉쭉 써보자. 
Train dataset과 Test dataset을 간단하게 살펴보자. 정말 간단하게만.

```python
# Load datasets
train = pd.read_csv('/kaggle/input/titanic/train.csv')
test = pd.read_csv('/kaggle/input/titanic/test.csv')

# train dataset overview using .shape and .info()
print(train.shape)
print(train.info())
print(train.head())

# test dataset overview using .shape and .info()
print(test.shape)
print(test.info())
print(test.head())
```

train과 test을 알아보기 위해 overview에 쓰이는 대표적인 attrtibute 및 fucntion인 .shape, .info(), .head()를 이용했다. 눈에 쉽게 보이는 특징 몇 개를 아래에 정리해두었다. 
* train은 891x12, test는 418x11의 dataset이다.
  * train과 test의 column 개수의 차이가 나는 건, test의 'survived' column을 제거했기 때문으로 보인다. 
  * 사실, 하나의 dataset을 train dataset과 test dataset으로 미리 나눠놓는 건 그렇게 흔한 일은 아니다. 아마 example dataset이기 떄문에 미리 나눈 것으로 보인다. 보통은 analyst가 나누는 method를 정한다. 
* missing value는 train에는 Cabin > Age > Embarked 순으로 많고 test에는 Cabin > Age > Fare 순으로 많다. 
  * 아마 뒤에서 다루겠지만 missing value를 처리하는 일은 정말 중요하다. 

> 여기까지 쓰는데 kernel이 두 번 다운됐다. 이거 써도 되는건가? github로 쓰고 옮기는게 낫겠다는 생각이 들었다. 괜히 competition high-position들이 결과만 sharing하고 github 주소를 다는 게 아닌 것 같다. 꽤 불편하다.

* 가령, Name이나 Ticket 같은 다루기 어려운 변수들이 몇 개 보인다. 꽤 고민을 해봐야할 것 같다. 
  * Name이나 Ticket의 obs가 갖는 의미를 찾는다면 사용방법을 찾는데 많은 도움이 될 것이다. 
* Age나 Fare는 변수를 구간화시켜 명목변수로 바꿔(binning)도 좋을 것 같다. 
  * Age는 10대 이하, 10대, 20대, 30대...로 Fare는 10미만, 20미만, 30미만 등으로 나눠 변수를 새로 정의해줄 수 있다.
  * Binning의 유의사항으로는 너무 많은 구간으로 나누지 않는 것이다. 지나치게 좁은 구간으로 나눠버리면 변수 개수가 늘어나는 것과 마찬가지라 말도 안되게 많은 문제가 생긴다.  
* **Sibsp**는 # of siblings / spouses aboard the Titanic, **Parch**는 # of parents / children aboard the Titanic이다. kaggle의 [data dictionary](https://www.kaggle.com/c/titanic/data)에서 찾았다.
  * 해석 안되는 변수 명들은 보통 이렇게 설명이 되어 있다. 혼자 고생하지 말고 꼼꼼히 살펴보자. 
  * 누군가의 자식이면 누군가의 부모도 있다는 것 아닌가? 예를 들어 A와 B가 부모 자식 사이면 Parch는 같은 값을 갖을 것이다. Name으로 이걸 구분할 수 있을까? 
