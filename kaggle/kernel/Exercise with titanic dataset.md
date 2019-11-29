## 들어가기 전에
&nbsp;&nbsp;&nbsp;&nbsp;남들 다 하는 Kaggle을 시작하기 위해 그나마 가장 익숙한 [titanic dataset](https://www.kaggle.com/c/titanic)을 골랐다. Python을 이용해 작성하는 첫 kaggle kernel이라 많이 버벅이겠지만, 그 맛에 공부 하는 거지.

# 1. Introduction of competiton
&nbsp;&nbsp;&nbsp;&nbsp;titanic dataset은 'isis dataset'과 더불어 굉장히 많이 쓰이는 example dataset이다. titanic dataset을 이용한 kaggle competition의 목적은 **주어진 dataset을 이용해 타이타닉이 가라앉은 상황에서 승객들의 생존여부를 예측하는 것**이다. 생존 혹은 사망의 binary classification이므로 평가 기준은 다음의 [accuracy score](https://en.wikipedia.org/wiki/Accuracy_and_precision#In_binary_classification)이다. kaggle에서 제공하는 raw dataset은 'train'과 'test'으로 실제로 data analysis에 사용되는 raw dataset처럼 missing value 및 outlier도 존재한다. 따라서 competition에 참가하는 참가자들은 preprocessing부터 model fitting까지 차근차근 연습해볼 수 있다.

# 2. Overview of Datasets
&nbsp;&nbsp;&nbsp;&nbsp;Train dataset과 Test dataset을 간단하게 살펴보는 단계다. 이 과정이 분석에 필요한 이유는 다음과 같다. 
* 변수의 종류, 개수, 성질을 알아보기 위함
* 관측값의 종류, 개수, 성질, 분포를 알아보기 위함
* Missing value 혹은 Null의 유무, 규모와 어떤 변수에 속해있는지 파악하기 위함

&nbsp;&nbsp;&nbsp;&nbsp;이 과정은 가장 기초적이면서 필수적인 과정인 동시에 여러 번 수행하게 될 수도 있는 과정이다. 따라서 과정의 흐름을 분명히 파악하고 실습해보자. 

## 2.1 Just overview using .info()
&nbsp;&nbsp;&nbsp;&nbsp;Dataset이 갖고 있는 변수와 관측값에 대한 개략적인 정보를 확인할 수 있는 function이나 method는 많지만 보통 .info() method를 이용한 방법을 많이 사용한다. 물론, 변수의 개수가 많을수록 한 눈에 dataset의 정보를 파악하기 어렵다는 단점이 존재하기는 하지만, Titanic dataset의 경우 변수의 개수가 비교적 적은 케이스이므로 사용해도 무방하다. 

```python
# Load datasets
train = pd.read_csv('/kaggle/input/titanic/train.csv')
test = pd.read_csv('/kaggle/input/titanic/test.csv')

# train dataset overview using .shape, .info(), .head() and .tail()
print(train.shape)
print(train.info())
print(train.head())
print(train.tail())

# test dataset overview using .shape and .info(), .head() and .tail()
print(test.shape)
print(test.info())
print(test.head())
print(test.tail())
```

&nbsp;&nbsp;&nbsp;&nbsp;train과 test을 알아보기 위해 overview에 쓰이는 대표적인 attrtibute 및 fucntion인 .shape, [.info()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.info.html), .head(), tail()을 이용했다. 눈에 쉽게 보이는 특징 몇 개를 아래에 정리해두었다. 
* train은 891x12, test는 418x11의 dataset이다.
   * train과 test의 column 개수의 차이가 나는 건, test의 'survived' column을 제거했기 때문으로 보인다. 
   * 사실, 하나의 dataset을 train dataset과 test dataset으로 미리 나눠놓는 건 그렇게 흔한 일은 아니다. 아마 example dataset이기 떄문에 미리 나눈 것으로 보인다. 보통은 analyst가 나누는 method를 정한다. 
* missing value는 train에는 Cabin > Age > Embarked 순으로 많고 test에는 Cabin > Age > Fare 순으로 많다. 
   * 아마 뒤에서 다루겠지만 missing value를 처리하는 일은 정말 중요하다.  
 * 가령, Name이나 Ticket 같은 다루기 어려운 변수들이 몇 개 보인다. 꽤 고민을 해봐야할 것 같다. 
   * Name이나 Ticket의 obs가 갖는 의미를 찾는다면 사용방법을 찾는데 많은 도움이 될 것이다. 
 * Age나 Fare는 변수를 구간화시켜 명목변수로 바꿔(binning)도 좋을 것 같다. 
   * Age는 10대 이하, 10대, 20대, 30대...로 Fare는 10미만, 20미만, 30미만 등으로 나눠 변수를 새로 정의해줄 수 있다.
   * Binning의 유의사항으로는 너무 많은 구간으로 나누지 않는 것이다. 지나치게 좁은 구간으로 나눠버리면 변수 개수가 늘어나는 것과 마찬가지라 말도 안되게 많은 문제가 생긴다.  
 * **Sibsp**는 # of siblings / spouses aboard the Titanic, **Parch**는 # of parents / children aboard the Titanic이다. kaggle의 [data dictionary](https://www.kaggle.com/c/titanic/data)에서 찾았다.
   * 해석 안되는 변수 명들은 보통 이렇게 설명이 되어 있다. 혼자 고생하지 말고 꼼꼼히 살펴보자. 
   * 누군가의 자식이면 누군가의 부모도 있다는 것 아닌가? 예를 들어 A와 B가 부모 자식 사이면 Parch는 같은 값을 갖을 것이다. Name으로 이걸 구분할 수 있을까?
   
## 2.2 Overview of variables 
&nbsp;&nbsp;&nbsp;&nbsp;변수의 종류, 개수, 성질에 대한 이해는 데이터 분석의 기초이다. 위의 2.1에서 봤던 내용을 기반으로 변수에 대해 정리해보자. 
* 변수의 개수는 총 12개이다. 
* 12개의 변수 중 numerical variable은 int64 type의 PassengerId, Pclass, SibSp, Parch와 float64 type의 Age, Fare로 총 6개다. 
* 12개의 변수 중 categorical variable은 Survived, Sex, Embarked로 총 3개다. 
* 12개의 변수 중 mixed variable은 Ticket과 Cabin이다. 
* 12개의 변수 중 Name은 string variable이다. 
* 12개의 변수 중 PassengerId는 indexing을 위한 변수이다. 
&nbsp;&nbsp;&nbsp;&nbsp;'변수'에 대해 알고 있다면 위의 내용이 틀렸다는 사실을 금방 눈치챌 수 있을 것이다. 사실 Pclass, SibSp, Parch의 세 변수는 categorical variable이며 특별히 Pclass는 서열형 명목 변수(Ordinal)이다. 그럼에도 위 처럼 정리한 것은 Dataset에 대해 아무것도 모르는 상태에서 매우 큰 dataset을 다루고 있음을 가정했기 때문이다. 변수의 숫자가 많아지면 하나하나 변수의 성질을 살피기 어렵게 되고 결국 Overview 단계에서는 .info()의 결과에 의해 출력되는 'dtypes'에 의존할 수 밖에 없게 된다. 잘 못 정리된 변수들은 뒤에서 올바르게 고칠 것이다. 

> dtypes 별로 column name을 return하는 함수가 있나? 있겠지? 찾아보자. 

## 2.3 Overview of observations
&nbsp;&nbsp;&nbsp;&nbsp;마찬가지로 관측값의 종류, 개수, 성질, 분포에 대한 이해는 데이터 분석의 기초이다. 특별히 관측값의 분포를 확인하는 일은 이 과정의 핵심이다.


  
# 3. Preprocessing(1) : data transformation
&nbsp;&nbsp;&nbsp;&nbsp;Preprocessing, 전처리의 첫 번째 단계는 dataset의 형태를 바꾸는 것이다. data transformation는 아래의 과정을 포함하고 있다. 
* dataset의 통합
* Missing values를 찾고 해결 방법 결정 후, 시행하기 
* Outliers찾고 처리 방법 결정 후, 시행하기

이제 하나 하나씩 처리해보자.

## 3.1 Combine dataset
&nbsp;&nbsp;&nbsp;&nbsp;dataset의 용량이 커지는 추세에 따라 모든 정보를 포함한 대용량의 단일 dataset을 가지고 데이터 분석을 하는 경우는 많이 없어졌다. 더욱이 SQL DB가 보편화 되며 DB에서 조건에 따라 filtering된 data를 추출, 이들을 합친 dataset을 만들어 분석하는 일이 잦아졌고 자연스럽게 dataset을 합치는 일 또한 많아졌다. 
&nbsp;&nbsp;&nbsp;&nbsp;Pandas module에서 dataset을 합치는 대표적인 방법은 (1) pandas.concat() (2) pandas.merge() 다. arg와 dataset에 따라 방법에 상관없이 같은 결과를 낼 수도 있지만 기본적으로 pandas.concat()은 **동일한 index나 column에 따른 연속적 연결에 의한 병합**을, pandas.merge()는 **공통된 열이나 행을 기준(key)으로 설정한 후, 기준 안에서 중복되는 값을 중심으로한 병합**을 시행한다. 따라서 pandas.concat()은 dataset의 비교적 단순한 통합을, pandas.merge()는 기준으로 선언된 key안에 존재하는 중복값을 통한 통합을 하고자 할 때 사용된다. 자세한 내용은 [pandas document](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html)를 참고하자.
&nbsp;&nbsp;&nbsp;&nbsp;Titanic competition에서 제공하는 train & test dataset은 survived column의 유무를 제외한다면 모든 column의 이름과 data type이 같기 때문에 index에 따라 '이어 붙여주기'만 하면 되는 것으로 보인다. 따라서 dataset을 병합하기 위한 방법으로 pandas.concat()을 사용했다.

```python
# pandas.concat을 이용한 dataset combination
com_df = pd.concat([train, test], ignore_index=True, sort = True)
print(com_df.info()) ## column순서가 바뀜

"""
제대로 combination 됐나 확인
missing values of Age col : 1309 - 1046 = 263 = 177 + 86
missing values of Cabin col : 1309 - 295 = 1014 = 687 + 327
missing values of Embarked col : 1309 - 1307 = 2 = 2 + 0
missing values of Fare col : 1309 - 1308 = 1 = 0 + 1
missing values of Survived col : 1309 - 891 = 418 = 0 + 418

print(com_df.isnull().sum())
print(train.isnull().sum())
print(test.isnull().sum())
"""
train.columns ## columns 순서 및 이름 확인
com_df = com_df[['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
       'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']]
print(com_df.info()) ## train dataset과 같은 column 순서임을 확인
```
## 3.2 Dealing with missing values 
&nbsp;&nbsp;&nbsp;&nbsp;Missing value, 결측값은 전처리 과정에서 반드시 짚고 넘어가야할 중요한 문제다. 결측값이 존재하기만 해도 modeling 과정에서 algorithm이 실행되지 않는 경우가 대부분이고 설사 실행된다한들 full-filled dataset보다 accuracy가 떨어지는 경우가 부기지수다. 그러므로 결측값을 어떻게든 채워넣어야 하는데 그 방법 또한 여러 개라 가장 적절한 방법이 무엇인지 판단하고 해당 방법을 통해 pseudo-observation을 만들어 dataset에 넣어야 한다. 이제 우리가 갖고 있는 combined dataset으로 missing values를 다루는 방법들을 천천히 알아보자.

### 3.2.1 Are there missing values?
&nbsp;&nbsp;&nbsp;&nbsp;사실 위의 과정을 성실히 거쳐왔다면 이미 missing values가 포함된 columns을 알고 있을 것이다.

```python
print(com_df.info())
print("\n","혹은 이 방법으로도 알 수 있다","\n",com_df.isnull().sum())
```
.info()를 overview에 유용하게 사용할 수 있는 이유 중 하나는 위와 같이 null value(=missing value)를 보여주기 때문이다. missing value의 개수만 알고 싶다면 bulit-in function인 .isnull()과 .sum()을 이용해 column 단위의 missing value 개수를 볼 수도 있다. 위의 결과로 총 5개의 column에 missing values가 있음을 알 수 있으며 missing value의 크기 순으로 보면 Cabin > Survived > Age > Embarked > Fare이다. 이 중, 418개의 missing values를 갖고 있는 Survived는 test dataset으로 나눠지며 삭제된 값으로 우리가 model fitting 및 prediction으로 채워야할 것들이므로 채워넣어야할 대상으로 고려하지 않을 것이다.

```python
missing_values = pd.DataFrame(com_df.isnull().sum(), columns = ['The number of missing values'])
# print(missing_values.iloc[:, 0]) # .iloc를 이용해 1열만 print
# print(missing_values[missing_values.iloc[:, 0] != 0]) ## masking을 이용해 non-zero만 print
missing_values[missing_values.iloc[:, 0] != 0].sort_values('The number of missing values', ascending=False).plot(kind = 'bar')
plt.xticks(rotation=45)
plt.show()
# Q. 이 상태의 plot에 value를 표시할 수 있는 방법은 없을까?
```
[.sort_values()에 대한 내용](https://eunguru.tistory.com/226)  
[pd.DataFrame()에 대한 내용](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)  
[.loc(), .iloc()와 같은 indexer에 대한 내용](https://datascienceschool.net/view-notebook/704731b41f794b8ea00768f5b0904512/) 
> To do. plot에 value를 추가할 수 있는 방법 찾기 <br> 

&nbsp;&nbsp;&nbsp;&nbsp;시각화를 이용해서 각 feature에 있는 null-value를 표시할 수도 있다. 

### 3.2.2. Fill missing values with pseudo-observations


