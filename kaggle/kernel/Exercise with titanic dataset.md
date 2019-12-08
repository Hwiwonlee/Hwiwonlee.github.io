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
* Name이나 Ticket 같은 다루기 어려운 변수들이 몇 개 보인다. 꽤 고민을 해봐야할 것 같다. 
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
&nbsp;&nbsp;&nbsp;&nbsp;마찬가지로 관측값의 종류, 개수, 성질, 분포에 대한 이해는 데이터 분석의 기초이다. 특별히 이 과정에서 관측값의 분포를 확인하고 missing value의 개수와 속한 변수를 찾는 일이 핵심이다. 먼저 .describe()를 이용해 summary stat을 살펴보자. 

```python
print(train.describe())
print(test.describe())
```

&nbsp;&nbsp;&nbsp;&nbsp;.describe()는 dataframe의 변수 기준으로 numerical value를 갖는 observation들의 summary statistics을 보여주는 method다. .describe()로도 많은 정보를 알 수 있고 이를 통해 다음 단계에서 해야할 일의 순서를 정할 수 있다. 내가 .describe()로 알아낸 것은 아래와 같다.

* train과 test 모두 Age에 missing value가 있으며 test에는 Fare에도 하나의 missing value가 존재한다.
* Pclass의 사분위수가 정수로 떨어지는 것으로 보아 Pclass는 categorical variable로 정리하는 것이 옳다고 보이므로 이후로는 Pclass를 categorical variable로 다루겠다. 
* train과 test 모두 Sibsp의 max 값이 8이다. 이전의 사분위 값과 큰 차이를 보이므로 Sibsp를 대상으로 한 이상치 판별이 필요하다. 
* Parch의 경우 train의 max는 6, test의 max는 9로 이전의 사분위수와 큰 차이를 보인다. 따라서 Parch를 대상으로 한 이상치 판별이 필요하다. 
* Age, Fare 모두 사분위수와 min, max값이 큰 차이를 보인다. 구간 값으로 나눠서 두 변수를 정리하는 것이 분석에 좀 더 도움이 될 것으로 보인다. 

사분위수(qualtile)과 min, max는 numerical variable의 분포를 알 수 있는 중요한 단서이며 이상치를 판별에도 도움을 주니 .describe()를 통한 분석을 하는 것이 전체적인 분석 과정에서도 도움이 된다. 사분위수(qualtile)과 min, max을 이용한 시긱화인 box plot을 이용할 수도 있다. 

```python
# Multiple box plots on one Axes
fig, ax = plt.subplots(figsize = (10,5))
ax.boxplot([train['Age'].dropna(), train['SibSp'], train['Parch'], train['Fare'],
           test['Age'].dropna(), test['SibSp'], test['Parch'], test['Fare'].dropna()],
           sym="r*")
## plot function의 대상에 na가 있으면 plot이 그려지지 않는다. 따라서 train['Age'].dropna()로 na를 일단 제외하고 plot을 그렸다. 
plt.title('Multiple box plots of dataset on one Axes')
plt.xticks([1,2,3,4,5,6,7,8],
           ['train.Age', 'train.SibSp', 'train.Parch', 'train.Fare',
            'test.Age', 'test.SibSp', 'test.Parch', 'test.Fare'],
          rotation = 45)

plt.show()
```

```python
# Draw boxplot with features in train set using subplot()
fig = plt.figure(figsize=(8, 8)) 
age = plt.subplot(2,2,1)
sibsp = plt.subplot(2,2,2)
parch = plt.subplot(2,2,3)
fare = plt.subplot(2,2,4)
age.boxplot(train['Age'].dropna(), sym='r*')
sibsp.boxplot(train['SibSp'], sym='r*')
parch.boxplot(train['Parch'], sym='r*')
fare.boxplot(train['Fare'], sym='r*')
age.set_xticklabels(['Age'])
sibsp.set_xticklabels(['SibSp'])
parch.set_xticklabels(['Parch'])
fare.set_xticklabels(['Fare'])

fig.suptitle('boxplot with features in train set', fontsize=16)

plt.show()
```

```python

fig = plt.figure(figsize=(8, 8)) 
age = plt.subplot(2,2,1)
sibsp = plt.subplot(2,2,2)
parch = plt.subplot(2,2,3)
fare = plt.subplot(2,2,4)
age.boxplot(test['Age'].dropna(), sym='r*')
sibsp.boxplot(test['SibSp'], sym='r*')
parch.boxplot(test['Parch'], sym='r*')
fare.boxplot(test['Fare'].dropna(), sym='r*')
age.set_xticklabels(['Age'])
sibsp.set_xticklabels(['SibSp'])
parch.set_xticklabels(['Parch'])
fare.set_xticklabels(['Fare'])

fig.suptitle('boxplot with features in test set', fontsize=16)

plt.show()
```

&nbsp;&nbsp;&nbsp;&nbsp;Box plot([boxplot 그리기](https://rfriend.tistory.com/410), [set_xticklabels](https://nittaku.tistory.com/117), [subtitle](https://matplotlib.org/3.1.1/gallery/subplots_axes_and_figures/figure_title.html), [figsize](https://financedata.github.io/posts/faq_matplotlib_default_chart_size.html))을 통해 알아본 결과, 몇 가지 사실을 추가로 알 수 있었다. 지금 단계에서의 plot은 missing value에 대한 imputation이 이뤄지지 않았으므로 결측치를 제외하고 그린 값이므로 dataset을 정확히 표현하지 못함을 명심하자. 

* 60대 중반 이후의 Age가 이상치로 보인다. 즉, 대부분의 탑승객들은 60대 중반 이하이다. 
* SibSp는 3 이상부터 이상치로 보인다. 즉, 대부분의 탑승객들은 2 이하의 값을 갖는다.
* Parch는 0이 정상치다. 즉, 1이상의 값은 모두 이상치로 보인다.
* Fare의 경우 탑승객의 대다수가 100미만의 돈을 지불했음을 알 수 있다. 따라서 100이상의 요금은 모두 이상치로 판정보인다. 

이상치로 보이는 값들을 찾아냈지만 이상치(outlier)가 모두 error는 아니라는 것에 주의하자. 어느 수준의 이상치를 error로 볼 것인지, 이상치와 error를 대체할 것인지, 변수 변환을 통해 이상치와 error를 다룰 것인지는 지금 단계에서 결정할 수 없다. numerical variable 중 continous variable에 한하여 분포를 알아보기 위한 시각화 방법으로 histogram을 이용할 수도 있다. Titanic dataset에서 continous variable은 Fare와 Age, 단 두 개이다. 

```python
f, axes = plt.subplots(1, 2, figsize=(12, 6))
tr_age = sns.distplot(train['Age'].dropna(), color="blue", label='Train.age', ax=axes[0])
te_age = sns.distplot(test['Age'].dropna(), color="red", label='Test.age', ax=axes[0])

tr_fare = sns.distplot(train['Fare'].dropna(), color="blue", label='Train.fare', ax=axes[1])
te_fare = sns.distplot(test['Fare'].dropna(), color="red", label='Test.fare', ax=axes[1])

f.suptitle("Histogram with Age and Fare in dataset", fontsize = 16)

axes[0].set_title("Histogram with Age and Fare in train set")
axes[1].set_title("Histogram with Age and Fare in test set")

axes[0].legend(loc='upper right', frameon=False)
axes[1].legend(loc='upper right', frameon=False)

plt.show()

"""Old version 
# Draw histogram with Age and Fare in train set
fig = plt.figure(figsize=(10,4))
age = plt.subplot(2,1,1)
fare = plt.subplot(2,1,2)
age.hist(train['Age'], bins = 20)
fare.hist(train['Fare'], bins = 20)
plt.show()

# Draw histogram with Age and Fare in test set
fig = plt.figure(figsize=(10,4))
age = plt.subplot(2,1,1)
fare = plt.subplot(2,1,2)
age.hist(test['Age'], bins = 20)
fare.hist(test['Fare'], bins = 20)
plt.show()"""
```

&nbsp;&nbsp;&nbsp;&nbsp;Histogram([hist 그리기](https://rfriend.tistory.com/408), [hist 그리기 2](https://rfriend.tistory.com/409), [hist 그리기 3](https://stackoverflow.com/questions/41384040/subplot-for-seaborn-boxplot), [범례 편집](https://jakevdp.github.io/PythonDataScienceHandbook/04.06-customizing-legends.html))으로 확인해본 결과 train과 test의 Age, Fare는 유사한 분포를 갖고 있는 것으로 보인다. Fare가 normal dist를 가정할 수 없는 비대칭형 분포를 띄고, Age 또한 normal dist을 가정하는 경우 추가적인 error를 갖게 될 것이므로 다른 분포를 가정하는 등의 방법을 찾아야 할 것으로 보인다.  

&nbsp;&nbsp;&nbsp;&nbsp;이제 categorical variable의 분포에 대해 알아보자. categorical variable은 연속형 공간을 갖지 못하므로 빈도수로만 분포를 알아볼 수 있으므로 각 항목에 대한 빈도 수를 시각화하는 것이 좋다. Titanic dataset에서 categorical variable은 Survived, Pclass, Sex, Embarked로 총 4개이다.

```python
plt.clf()
freq_sur = pd.value_counts(train['Survived'].values, sort=False)
freq_sex = pd.value_counts(train['Sex'].values, sort=False)
freq_pcl = pd.value_counts(train['Pclass'].values, sort=False)
freq_emb = pd.value_counts(train['Embarked'].values, sort=False)

f, axes = plt.subplots(1, 4, figsize=(16, 8))
tr_sur = sns.barplot(x=freq_sur.index, y=freq_sur, label='Train.survived', ax=axes[0])
tr_sex = sns.barplot(x=freq_sex.index, y=freq_sex, label='Train.sex', ax=axes[1])
tr_pcl = sns.barplot(x=freq_pcl.index, y=freq_pcl, label='Train.pclass', ax=axes[2])
tr_emb = sns.barplot(x=freq_emb.index, y=freq_emb, label='Train.embarked', ax=axes[3])

f.suptitle("Barplot with categorical variables in train set", fontsize = 16)

axes[0].set_title("Frequency of Survieved's value")
axes[1].set_title("Frequency of Sex's value")
axes[2].set_title("Frequency of Pclass's value")
axes[3].set_title("Frequency of Embarked's value")

plt.show()
```
```python
plt.clf()
freq_sex = pd.value_counts(test['Sex'].values, sort=False)
freq_pcl = pd.value_counts(test['Pclass'].values, sort=False)
freq_emb = pd.value_counts(test['Embarked'].values, sort=False)

f, axes = plt.subplots(1, 3, figsize=(12, 6))
te_sex = sns.barplot(x=freq_sex.index, y=freq_sex, label='Train.sex', ax=axes[0])
te_pcl = sns.barplot(x=freq_pcl.index, y=freq_pcl, label='Train.pclass', ax=axes[1])
te_emb = sns.barplot(x=freq_emb.index, y=freq_emb, label='Train.embarked', ax=axes[2])

f.suptitle("Barplot with categorical variables in test set", fontsize = 16)

axes[0].set_title("Frequency of Sex's value")
axes[1].set_title("Frequency of Pclass's value")
axes[2].set_title("Frequency of Embarked's value")

plt.show()
```
> To do. plt.subplots(2,2)로 주면 error가 나는데, (1,4)로 주면 에러가 나지 않는다. 왜 그럴까? 

> To do. plot안에 value값을 표시할 수는 없을까? 

Survived variable이 없는 것을 제외한다면 categorical variable의 빈도수 또한 train set과 test set이 유사한 경향을 보임을 볼 수 있다. 
* train set의 Survived로 생존자보단 사망자가 많음을 알 수 있다.
* train set과 test set에 근거해 titanic엔 여성보다 남성이 많이 탑승했다고 말할 수 있다.
* train set과 test set에 근거해 titanic의 탑승객들의 사용 객실을 규모로 정리해보면 3등석 > 1등석 > 2등석 순이다.
* train set과 test set에 근거해 titanic의 탑승객들이 승선한 항구를 승선규모로 정리해보면 S > C > Q이다. 

&nbsp;&nbsp;&nbsp;&nbsp;이제 missing value의 규모와 어느 변수에 missing value가 많은지 알아보자. 

```python
# List comprehension을 이용한 filtering 
print(train.isna().sum()[[n for n in range(len(train.isna().sum())) if train.isna().sum()[n] != 0]].sort_values())
print(test.isna().sum()[[n for n in range(len(test.isna().sum())) if test.isna().sum()[n] != 0]].sort_values())
```
```python
plt.clf()
tr_NaN = train.isna().sum()[[n for n in range(len(train.isna().sum())) if train.isna().sum()[n] != 0]].sort_values()
te_NaN = test.isna().sum()[[n for n in range(len(test.isna().sum())) if test.isna().sum()[n] != 0]].sort_values()

f, axes = plt.subplots(1, 2, figsize=(12, 6))
tr_NaN_bar = sns.barplot(x=tr_NaN.index, y=tr_NaN, label='Train.NaN', ax=axes[0])
te_NaN_bar = sns.barplot(x=te_NaN.index, y=te_NaN, label='Test.NaN', ax=axes[1])

f.suptitle("Barplot with missing values in dataset", fontsize = 16)

axes[0].set_title("Missing values in train set")
axes[1].set_title("Missing values in test set")

plt.show()
```
List comprehension과 barplot를 이용해 train set과 test set에 있는 missing value에 대해 다음과 같은 사실들을 알 수 있었다.
* train set과 test set 모두 Age과 Cabin variable에 적지 않은 수의 missing value가 있다.
    * 특히, Cabin은 과반수 이상의 observation을 missing value로 갖고 있어 imputation이 쉽지 않아 보인다.
* train set은 Embarked에서 2개의 missing value가, test set은 Fare에서 1개의 missing value가 발견되었다. 

&nbsp;&nbsp;&nbsp;&nbsp;variable부터 observation까지 간단하게 살펴보았다. 이제 test set을 중심으로 Survived와 관련이 있는 변수가 있는지 알아보도록 하자. 

## 2.4 Exploratory Data Analysis (1) : 기초적 분석
&nbsp;&nbsp;&nbsp;&nbsp;EDA, Exploratory Data Analysis, 는 데이터 분석이라는 과정 안에서 굉장히 넓게 사용할 수 있는 말이다. 흔히 쓰는 Preprocessing이나 data wragling조차도 EDA의 하나의 과정일수도 아닐수도 있다. 그래서 되도록이면 EDA라는 단어를 쓰고 싶지 않았는데, 많이 쓰는데는 그 이유가 있나보다. 마땅한 단어가 없다. overview 단계에서의 EDA는 test set에 포함된 예측 대상이 되는 변수, 즉 Survived와 다른 변수들 사이에 어떤 관계가 있는지 알아보는데 중심을 둔다. 현재로써는 imputation이나 변수변환같은 변수에 대한 직접적인 조작을 하지 않은 상태이므로 지금 알아보는 이 관계가 최선의 관계는 아니다. 그럼에도 불구하고 이 과정이 권장되는 것은 다음의 이유들 때문이다. 

* Data analysis의 목적이 되는 변수와 다른 변수 사이의 대략적인 관계를 알아볼 수 있다. 
* variable handling, 그러니까 Preprocessing 이전에 handling이 필요한 변수를 찾아낼 수 있다.

이제 Survived와 Pclass, Sex, Age, SibSp, Parch, Fare, Embarked 사이의 관계를 수치와 시각화로 알아보자. 

```python
train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
train[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
```
```python
plt.clf()
rel_pcl = train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
rel_sex = train[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)
rel_sib = train[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
rel_par = train[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
rel_emb = train[["Embarked", "Survived"]].dropna().groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)

f, axes = plt.subplots(1, 5, figsize=(16, 8))
rel_pcl_bar = sns.barplot(x=rel_pcl['Pclass'], y=rel_pcl['Survived'], label='Rel.pclass', ax=axes[0])
rel_sex_bar = sns.barplot(x=rel_sex['Sex'], y=rel_sex['Survived'], label='Rel.Sex', ax=axes[1])
rel_sib_bar = sns.barplot(x=rel_sib['SibSp'], y=rel_sib['Survived'], label='Rel.SibSp', ax=axes[2])
rel_par_bar = sns.barplot(x=rel_par['Parch'], y=rel_par['Survived'], label='Rel.Parch', ax=axes[3])
rel_emb_bar = sns.barplot(x=rel_emb['Embarked'], y=rel_emb['Survived'], label='Rel.Parch', ax=axes[4])

f.suptitle("Barplot with relation between Survived and categorical variables in train set", fontsize = 16)

axes[0].set_title("Relation between Survived and Pclass")
axes[1].set_title("Relation between Survived and Sex")
axes[2].set_title("Relation between Survived and SibSp")
axes[3].set_title("Relation between Survived and Parch")
axes[4].set_title("Relation between Survived and Embarked")

plt.show()
```

```python
f, axes = plt.subplots(1, 2, figsize=(20, 8))
sns.distplot(train[train['Survived'] == 0]['Age'], color = 'red', bins = 20, ax=axes[0])
sns.distplot(train[train['Survived'] == 1]['Age'], color = 'blue', bins = 20, ax=axes[1])

axes[0].set_xlim(train[train['Survived'] == 0]['Age'].min()-3, train[train['Survived'] == 0]['Age'].max()+3)
axes[1].set_xlim(train[train['Survived'] == 1]['Age'].min()-3, train[train['Survived'] == 1]['Age'].max()+3)

f.suptitle("Histogram with relation between Survived and Age in train set", fontsize = 16)
axes[0].set_title("Relation between Survived = 0 and Age")
axes[1].set_title("Relation between Survived = 1 and Age")
```

```python
f, axes = plt.subplots(1, 2, figsize=(20, 8))
sns.distplot(train[train['Survived'] == 0]['Fare'], color = 'red', bins = 20, ax=axes[0])
sns.distplot(train[train['Survived'] == 1]['Fare'], color = 'blue', bins = 20, ax=axes[1])

axes[0].set_xlim(train[train['Survived'] == 0]['Fare'].min()-10, train[train['Survived'] == 0]['Fare'].max()+10)
axes[1].set_xlim(train[train['Survived'] == 1]['Fare'].min()-10, train[train['Survived'] == 1]['Fare'].max()+10)

f.suptitle("Histogram with relation between Survived and Fare in train set", fontsize = 16)
axes[0].set_title("Relation between Survived = 0 and Fare")
axes[1].set_title("Relation between Survived = 1 and Fare")
```

Survived와 categorical variable들은 barplot으로 Survived와 numerical variable들은 histogram으로 시각화해보았다. 말 그대로 raw data인 상태의 분석 결과라 뚜렷한 경향성을 찾기는 어렵지만 그래도 성과가 없지는 않다.
* 1등석에 탑승한 승객의 생존률은 무려 60%가 넘는다. 3등석에 탑승한 승객의 생존률이 30%가 되지 않는 것으로 볼 때 상당히 큰 차이로 보인다. 
* 남성의 생존률이 20%가 되지 않는 반면, 여성의 생존률은 70%가 넘는다.
* 형제, 자매나 가족간의 탑승 여부 및 숫자는 survived와 큰 상관이 없는 것으로 보인다. 변수 변환으로 의미있게 만들어볼 수 있을까?
* 탑승한 항구가 'C'인 경우 생존률이 50% 이상이다. 탑승한 항구가 특별한 의미가 있는 것일까?
* Age나 Fare와 Survived 사이에 전체적인 경향은 찾아보기 힘들었다.
* 다만 Age의 경우 10대 미만의 영유아의 생존률이 유의미하게 높아보인다. 

&nbsp;&nbsp;&nbsp;&nbsp;지금까지 data analysis의 overview 단계를 진행해보았다. 내가 진행한 overview를 크게 두 단계로 나누면 dataset의 구성 분석 + EDA : 기초분석 정도 될 것이다. 앞서도 말했지만 변수변환과 같은 변수조작이 이뤄지지 않은 상태의 dataset을 대상으로 한 분석이라 그 결과가 만족스럽지 않을 수 있지만 향후 data handling에 있어 꼭 필요한 단계들이었다고 생각한다. 마지막으로 2장에서 본 내용들을 간단히 되짚어보고 3장으로 넘어가자. 

* numerical variable과 categorical variable을 구분해 정의했다. 
* string variable인 name과 ticket은 아직 분석하지 않았다.
* numerical variable과 categorical variable의 분포를 보아 test set과 train set은 비교적 잘 나눠진 것 같다. 
* 변수가 가진 missing value의 개수를 알아보았다. 
* EDA : 기초분석으로 Survived와 변수 간 관계를 알아보았다. 




# 3. Preprocessing(Data wrangling, Data munging or Data handling)
&nbsp;&nbsp;&nbsp;&nbsp;Preprocessing, 전처리는 model fitting 전 dataset을 model에 적절하게 만들어주는 모든 작업을 아우른다. model에 따라 필요한 dataset의 형태가 다를 수 있기 때문에, 혹은 prediction의 성능을 높히기 위해 전처리는 여러 번 반복될 수 있다. 이 과정을 prepocessing이라는 말 외에도 data wrangling, munging, handling이라고 하는데 변수를 포함한 dataset을 조작한다는 큰 틀은 벗어나지 않으며 아래의 과정이 대표적인 전처리 과정들이다.

* dataset의 통합
* Missing values를 찾고 해결 방법 결정 후, 시행하기 
* Outliers찾고 처리 방법 결정 후, 시행하기

이제 하나 하나씩 처리해보자.

> To do. 생각해보니 '전처리'는 handling 이전의 단계를 말하는 것 아닐까? 전처리는 최소한의 handling이 가능하게끔 만들어주는 단계이고. fitting을 하고 다시 전처리를 한다고 써놓고 보니 좀 이상하네. 


## 3.1 Combine dataset
&nbsp;&nbsp;&nbsp;&nbsp;dataset의 용량이 커지는 추세에 따라 모든 정보를 포함한 대용량의 단일 dataset을 가지고 데이터 분석을 하는 경우는 많이 없어졌다. 더욱이 SQL DB가 보편화 되며 DB에서 조건에 따라 filtering된 data를 추출, 이들을 합친 dataset을 만들어 분석하는 일이 잦아졌고 자연스럽게 dataset을 합치는 일 또한 많아졌다. 
&nbsp;&nbsp;&nbsp;&nbsp;Pandas module에서 dataset을 합치는 대표적인 방법은 (1) pandas.concat() (2) pandas.merge() 다. arg와 dataset에 따라 방법에 상관없이 같은 결과를 낼 수도 있지만 기본적으로 pandas.concat()은 **동일한 index나 column에 따른 연속적 연결에 의한 병합**을, pandas.merge()는 **공통된 열이나 행을 기준(key)으로 설정한 후, 기준 안에서 중복되는 값을 중심으로한 병합**을 시행한다. 따라서 pandas.concat()은 dataset의 비교적 단순한 통합을, pandas.merge()는 기준으로 선언된 key안에 존재하는 중복값을 통한 통합을 하고자 할 때 사용된다. 자세한 내용은 [pandas document](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html)를 참고하자.
&nbsp;&nbsp;&nbsp;&nbsp;Titanic competition에서 제공하는 train & test dataset은 survived column의 유무를 제외한다면 모든 column의 이름과 data type이 같기 때문에 index에 따라 '이어 붙여주기'만 하면 되는 것으로 보인다. 따라서 train set에서 Survived column을 제외한 후 test set과 병합하기 위해 pandas.concat()을 사용했다.

```python
# pandas.concat을 이용한 dataset combination
com_df = pd.concat([train.drop(['Survived'], 1), test], ignore_index=True, sort = True)
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
com_df = com_df[['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
       'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']]
print(com_df.info()) ## train dataset과 같은 column 순서임을 확인
```

## 3.2 Variable handling
&nbsp;&nbsp;&nbsp;&nbsp;Variable handling, machine 혹은 Deep learning 분야에서는 Feature engineering이라 부르는 이 과정은 dataset의 변수를 분석하고 model에 적합하게 변환하고 조작하는 과정이다. Variable handling의 과정은 data analysis의 핵심이라고 볼 수 있는데, variable이 갖고 있는 정보를 최대한 보존시키며 분석에 적절한 형태로 변환한 variable를 이용한 fitting & prediction과 그렇지 않은 variable을 이용한 fitting & prediction의 accuracy차이가 상당하기 때문이다. Variable handling의 범위는 작게는 변수 안의 data type을 바꾸는 것부터 크게는 n개의 변수를 r개의 변수로 합치거나 변수를 dataset에서 삭제하는 것까지 다양하다. variable handling의 방법이 다양한 만큼 analyst의 올바른 의사결정이나 variable에 대한 insight에 크게 의존하므로 analyst, 본인의 역량을 드러낼 수 있는 좋은 기회다. 

&nbsp;&nbsp;&nbsp;&nbsp;Tatinic dataset에서는 12개의 변수가 주어졌으며 이 중 Survived는 test에서 제외된 상태이므로 11개의 변수를 handling하는 것이 이번 단계에서의 주된 과제다. 11개의 변수 중 numerical variable은 PassengerId, Age, SibSp. Parch, Fare 등 총 5개이며 categorical variable은 Pclass, Sex, Embarked 등 총 3개이고 String variable은 Name, Ticket, Cabin 등 총 3개이다. 이제 하나하나씩 변수를 자세히 살펴보고 적절한 변환을 해보자. 

### 3.2.1 PassengerId
&nbsp;&nbsp;&nbsp;&nbsp;PassengerId는 변수명 그대로 인식을 위해 임의로 부여한 numerical variable이다. dataframe의 row에는 # of observation만큼의 index가 이미 존재하므로 index와 PassengerId는 완벽히 같다. 따라서 **PassengerId는 dataframe에서 삭제하도록 하겠다.**

```python
# index와 PassengerId colum가 같음을 확인하기
com_df.index #RangeIndex(start=0, stop=1309, step=1)
com_df['PassengerId'] # 1:1309

# PassengerId column 삭제 
com_df = com_df.drop(['PassengerId'], 1)
com_df.head() 
```

### 3.2.2 Name
&nbsp;&nbsp;&nbsp;&nbsp;Name은 체계를 갖고 있으므로 자연어보단 분석하기 편한 편이라고 한다. 실제로 Titanic의 Name column을 보면 '.', ',', ' ' 등으로 나눠져 있음을 볼 수 있다. 그렇다면 가장 많은 빈도를 가진 단어는 무엇일까? 

> To do. 띄어쓰기를 기준으로 같은 문자열을 찾는 방법이 있을까? 중복도 검사하기. 해결! 

> To do. re module을 이용할 수도 있을까? 


```python
# com_df에 '문자열'을 포함한 observation을 대상으로한 describe 결과
com_df.describe(include=['O'])

# Name을 기호를 제외하고 공백 기준으로 나눈 새로운 column New_name 추가
com_df['New_name'] = com_df['Name'].str.replace('[^\w\s]','') # https://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas

# New_name으로 string의 빈도수 파악 : 공백을 기준으로 중복 문자열 알아보기
Name_list = list(com_df["New_name"]) ## List로 변환
Name_list = ' '.join(Name_list).split(' ') ## 공백기준, value을 하나의 list로 합친 후 다시 공백 기준 나누기
"""이렇게 하는 이유는 위에서 쓴 split()이 str만 사용가능한 method이기 때문(https://www.geeksforgeeks.org/python-string-split/)이다.
1) ' '.join(Name_list)로 하나의 str object로 합치고
2) str.split(' ')로 str를 공백 기준으로 나눈 하나의 list로 저장"""
type(' '.join(Name_list)) ## str 확인

# Name_list에서 가장 많은 빈도수를 가진 단어는?
import collections
collections.Counter(Name_list) # https://excelsior-cjh.tistory.com/94
collections.Counter(Name_list).most_common(20) # 상위 20개의 중복 빈도를 가진 단어 출력
```

원래의 Name column을 [공백 기준으로 나누고](https://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas), [collections 모듈을 이용한 방법](https://excelsior-cjh.tistory.com/94)으로 빈도수가 많은 단어만 추려내보았다. Last name으로 보이는 것들을 제외하면 성별을 나타내는 'Mr', 'Miss', 'Mrs'과 알 수 없는 칭호인 'Master'가 눈에 띈다. 'Master'에 대해 알아보니 청소년 미만의 '남자 아이'를 뜻하는 말이라고 한다. 추가적으로 성별을 나타내는 칭호과 직위를 나타내는 칭호까지 추가한 결과가 아래에 나와있다. 

> To do. Dr은 'Dr'로 찾으니 'Dr'로 시작하는 이름들이 나와서 ' Dr'로 찾았다. '완벽히 일치하는 문자열'을 찾을 수 있는 방법은 없을까?  
> 정규표현식에 대해 더 알아보자 [(1)](https://greeksharifa.github.io/blog/tags/#re), [(2)](https://wikidocs.net/4308#match), [(3)](https://wikidocs.net/4309)


```python
# 성별을 의미하는 칭호 추가 : Ms
com_df[com_df['New_name'].str.contains('Ms')] # 2개 
```
```python
# 직위를 나타내는 칭호 찾기. 
com_df[com_df['New_name'].str.contains(r'\bDr\b')] # 11개
com_df[com_df['New_name'].str.contains(r'\bSir\b')] # 1개
com_df[com_df['New_name'].str.contains('Prof')] # 0개 
```

아래의 코드는 pd.crosstab()을 이용해 '칭호'과 생존여부 사이에 관계가 있는지 알아보기 위해 작성한 코드다. Survived가 포함되어야만 했기에 dataset은 train set으로 한정지었다. 2장에서 보았듯, 여성의 생존률이 높기 때문에 여성을 의미하는 칭호를 가진 사람의 생존률이 더 높은 것을 확인할 수 있었다. 그렇다면 '칭호'과 생존여부 사이에는 적절한 관계가 있다고 생각해도 될 것이다. [정규표현식](https://whatisthenext.tistory.com/116)

```python
pd.crosstab(train.Name.str.extract(' ([A-Za-z]+)\.', expand=False), train['Survived']) # train['Title'] = train.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
# ' ([A-Za-z]+)\.' : ([A-Za-z]+), 대소문자를 가리지 않는 알파벳(A-Za-z)을 대상으로 하며 반복이 존재하는(+, 즉, 글자수 제한이 없음) 문자열([])을 대상으로 함.
# + \. : 메타 문자인 .(dot)을 일반문자로 인식하게 해(\) [some words].의 형태를 추출할 수 있도록 한다. 
```

&nbsp;&nbsp;&nbsp;&nbsp;앞서 칭호와 생존률에 관련이 있음을 확인했으니 Name에서 칭호를 추출, '칭호'의 여부와 종류에 따른 새로운 variable을 만들어 dataset에 추가해보자. 칭호 변수, 이후로는 Title이라 부를 이 변수는 성격상 categorical variable로 정의되어야 옳으므로 너무 많은 수준의 category를 포함하지 않는 것이 좋다. 따라서 [Title의 수준은 총 5개로 빈도수에 따라 Mr, Miss, Mrs, Master, Rare를 각각 1,2,3,4,5에 대응시킬 것](https://www.kaggle.com/startupsci/titanic-data-science-solutions/notebook#Titanic-Data-Science-Solutions)이다. 

> 여기까지 하다가 느낀 건데, Titanic Data Science Solutions에서 combine = [train, test]로 합친 것은 굉장히 깔끔하게 합친 것 같다. 이렇게 합치면 for문으로 train, test를 쉽게 바꿔줄 수 있기 때문에 코드가 좀 더 간편해지는 장점이 있다. 

```python
title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
com_df['Title'] = com_df.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
com_df['Title'] = com_df['Title'].map(title_mapping)
com_df['Title'] = com_df['Title'].fillna(0)

com_df.head()
```

### 3.2.3 Sex
&nbsp;&nbsp;&nbsp;&nbsp;Sex와 같은 categorical variable을 string 형태로 둬도 크게 상관없긴 하지만 분석의 편의성을 위해 integer로 변환하는 것이 보통이다. 따라서 남성을 0으로, 여성을 1로 바꿔보자. 

```python
com_df['Sex_int'] = com_df['Sex'].map( {'female': 1, 'male': 0} ).astype(int)
```

### 3.2.4 Age
&nbsp;&nbsp;&nbsp;&nbsp;Age는 numerical variable 중 interger를 갖는 descrete variable로 정의되는 것이 보통이지만 Tatinic dataset은 float를 갖는 continuous variable로 정의되었다. 더불어 2장에서 살펴본 것과 같이 Age의 구간이 n개월의 영아부터 80세의 노인까지 굉장히 넓게 분포하고 있다. 따라서 continuous variable로 유지하는 것이 아닌 categorical variable로 바꾸는 것이 분석을 위해 바람직해보이며 나이의 scale과 나이 차이의 성격을 유지하기 위해 Ordinal로 정의할 것이다. 따라서 [Age는 'Age_band'로 총 다섯 등분해 저장하겠다.](https://www.kaggle.com/startupsci/titanic-data-science-solutions/notebook#Titanic-Data-Science-Solutions)

```python
# Age를 float value로 갖는 obs 출력
com_df[((com_df["Age"] / np.trunc(com_df["Age"])) > 1)]
com_df[((com_df["Age"] / np.trunc(com_df["Age"])) > 1)].shape[0]
```
```python
sns.boxplot(com_df["Age"].dropna())
```
```python
com_df['Age_band'] = pd.cut(com_df['Age'], 5)

## Age band를 숫자형 범주로 바꿔 'Age'로 대체시키기 
com_df.loc[com_df['Age'] <= 16, 'Age'] = 0
com_df.loc[(com_df['Age'] > 16) & (com_df['Age'] <= 32), 'Age'] = 1
com_df.loc[(com_df['Age'] > 32) & (com_df['Age'] <= 48), 'Age'] = 2
com_df.loc[(com_df['Age'] > 48) & (com_df['Age'] <= 64), 'Age'] = 3
com_df.loc[ com_df['Age'] > 64, 'Age']
com_df.head()
```

사실 굳이 '다섯 등분'일 필요는 없다. 물론 이 부분에 대한 방법론(=countinuous variable을 bining하는 방법론)이 존재하는 것으로 알고 있지만 '적절한 수준'으로 쪼개 뭉쳐주기만 하면 되는 일이다. '적절한 수준'이라는 말이 조금 어려운데, 하나의 bin이 너무나 큰 대푯값을 갖지 않도록 하는 동시에 구간 안에 너무 많은 값을 갖지 않도록 하는 것이 중요하다. 가령, Titanic dataset에서는 생존률을 대푯값으로 보면 10대 이전의 생존률이 높고 분포의 밀도는 20-40대에서 높다. 따라서, 10대와 20대를 적절히 섞어줄 수 있는 bining을 시행하면 얼추 맞는다. 이 때 5,6,7개의 구간으로 나눠주는 선에서 선택할 수 있는데 categorical variable 내의 수준이 많아지는 것을 지양하는 것이 바람직하므로 5개의 수준으로 선택한 것으로 보인다. 

```python
# n등분에 대한 approach
# 5등분 
train['Age_band'] = pd.cut(train['Age'], 5)
train[['Age_band', 'Survived']].groupby(['Age_band'], as_index=False).mean().sort_values(by='Age_band', ascending=True)

# 6등분 
train['Age_band'] = pd.cut(train['Age'], 6)
train[['Age_band', 'Survived']].groupby(['Age_band'], as_index=False).mean().sort_values(by='Age_band', ascending=True)

# 7등분 
train['Age_band'] = pd.cut(train['Age'], 7)
train[['Age_band', 'Survived']].groupby(['Age_band'], as_index=False).mean().sort_values(by='Age_band', ascending=True)
```

이제 Age variable에 missing value를 채우는 일이 남았다. 그러나 당장은 다른 variable handling을 계속 진행하도록 하자. imputation은 3절에서 시행하겠다. 

### 3.2.5 Fare
&nbsp;&nbsp;&nbsp;&nbsp;Fare는 Age와 같은 numerical variable, continuous varaible이다. 따라서 Age에서와 마찬가지로 구간을 나눠 ordinal로 만들어주면 된다. 단, 2장에서 이미 살펴보았듯 Fare는 상당히 치우친 분포를 갖고 있으므로 Age에서 처럼 pd.cut()을 사용할 수 없으므로 전체 obs를 동일한 개수로 나누는 pd.qcut()를 이용하는 것이 좀 더 바람직할 것이다. 이제 Fare를 정확히 4등분해서 각 구간에 따라 0, 1,2,3의 ordinal로 다시 정의해보자. 이 과정에서 Fare에 포함된 하나의 missing value에 대해서는 median으로 대체하겠다. 

```python
# 'Fare'에 있는 하나의 Na를 median으로 채워줌. 
com_df['Fare'].fillna(com_df['Fare'].dropna().median(), inplace=True)

com_df['Fare_band'] = pd.qcut(com_df['Fare'], q=4)
com_df.loc[com_df['Fare'] <= 7.896, 'Fare'] = 0
com_df.loc[(com_df['Fare'] > 7.896) & (com_df['Fare'] <= 14.454), 'Fare'] = 1
com_df.loc[(com_df['Fare'] > 14.454) & (com_df['Fare'] <= 31.275), 'Fare']   = 2
com_df.loc[com_df['Fare'] > 31.275, 'Fare'] = 3
com_df['Fare'] = com_df['Fare'].dropna().astype(int)
com_df.head()
```
```python
# FareBand와 Survived의 관계 
train['Fare_band'] = pd.qcut(train_df['Fare'], 4)
train[['Fare_band', 'Survived']].groupby(['Fare_band'], as_index=False).mean().sort_values(by='Fare_band', ascending=True)
```
### 3.2.6 SibSp + Parch = New variable, Alone
&nbsp;&nbsp;&nbsp;&nbsp;SibSp는 Titanic에 동승한 형제 및 자매의 숫자를, Parch는 Titanic에 동승한 부모 및 자녀의 숫자를 의미하는 변수들이며 numerical, descrete variable이다. Titanic dataset에서 이 두 변수는 과반수 이상의 obs에서 SibSp = 0, Parch = 0를 갖으므로 동승자가 있다 혹은 없다의 categorical variable로 재정의하는 것이 더 좋아보인다. 따라서, SibSp나 Parch 혹은 SibSp와 Parch를 0이상으로 갖는 obs를 '동승자가 있다'로, SibSp=Parch=0인 obs를 '동승자가 없다'로 정의한 Alone을 추가해 SibSp와 Parch를 대체할 것이다. 


```python
print(len(com_df[com_df['SibSp']<1])) # 형제 자매와 함께 타지 않은 사람이 891명
print(len(com_df[com_df['Parch']<1])) # 부모와 함께 타지 않은 사람이 1002명
print(len(com_df[(com_df['Parch']<1) & (com_df['SibSp']<1)])) # 가족과 함께 타지 않은 사람이 790명
print(len(com_df)) # 전체 1309명
```
```python
com_df['Family'] = com_df['SibSp'] + com_df['Parch']
com_df['Alone'] = 0 # 0 : 가족없이 홀로 탑승
com_df.loc[com_df['Family'] != 0, 'Alone'] = 1 # 가족과 함께 탑승
com_df[(com_df['Family']!=0) & (com_df['Alone']==0)] # 제대로 Alone이 추가되었는지 확인 
```

### 3.2.7 Embarked
&nbsp;&nbsp;&nbsp;&nbsp;Embarked는 Titanic이 정박한 항구에 관한 변수로 3개의 수준, S, C, Q를 갖는 categorical variable이다. 앞서 Sex에서 male:0, female:1으로 처리했던 것처럼 string type의 obs를 integer로 바꿀 것이다. 빈도수에 따라 S:0, C:1, Q:2로 재정의할 것이며 combined set에 포함된 2개의 missing value는 최빈값인 S:0으로 대체할 것이다. 

```python
print(com_df["Embarked"].value_counts())
print(len(com_df["Embarked"].dropna()))
print(len(com_df["Embarked"]))
```
```python
com_df['Embarked'] = com_df['Embarked'].fillna('S')
com_df["Embarked_int"] = com_df['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2 } ).astype(int)
com_df["Embarked_int"].value_counts() # check
```
### 3.2.8 Ticket
&nbsp;&nbsp;&nbsp;&nbsp;Ticket은 문자열+숫자의 mixed variable이나 obs에 따라 숫자로만 이뤄진 obs가 있고 mixed type의 obs가 있다. 따라서 side story로 남겨두고 이번 분석에서는 삭제하도록 하겠다. 

```python
com_df = com_df.drop(['Ticket'], 1)
```

### 3.2.9 Cleaning the dataset
&nbsp;&nbsp;&nbsp;&nbsp;지금까지 Titanic dataset에 있는 변수들을 다뤄보았다. 몇 개의 변수들이 다른 type의 obs로 대체되면서 쓸모가 없어졌고 아예 새로운 변수로 대체되는 변수들도 있었다. 이제 dataset에서 의미없어진 변수들을 지워보자. 

```python
com_df.head()
com_df = com_df.drop(['Name', 'Sex', 'SibSp', 'Parch', 'Embarked', 'New_name', 'Age_band', 'Fare_band', 'Family'], 1)
com_df.head()
com_df.info()
```

이제 3장에서 남은 일은 Cabin의 처리와 Cabin과 Age의 missing value를 채우는 일이다. 다음 절에서 cabin과 age의 imputation을 해보자. 


## 3.3 Dealing with missing values 
&nbsp;&nbsp;&nbsp;&nbsp;Missing value, 결측값은 전처리 과정에서 반드시 짚고 넘어가야할 중요한 문제다. 결측값이 존재하기만 해도 modeling 과정에서 algorithm이 실행되지 않는 경우가 대부분이고 설사 실행된다한들 full-filled dataset보다 accuracy가 떨어지는 경우가 부기지수다. 그러므로 결측값을 어떻게든 채워넣어야 하는데 그 방법 또한 여러 개라 가장 적절한 방법이 무엇인지 판단하고 해당 방법을 통해 imputation을 거쳐 dataset에 채워넣어야 한다. 이제 우리가 갖고 있는 combined dataset으로 missing values를 다루는 방법들을 천천히 알아보자.

### 3.3.1 Are there missing values?
&nbsp;&nbsp;&nbsp;&nbsp;사실 위의 과정을 성실히 거쳐왔다면 이미 missing values가 포함된 columns을 알고 있을 것이다.

```python
print(com_df.info())
print("\n","혹은 이 방법으로도 알 수 있다","\n",com_df.isnull().sum())
print("\n","좀 더 깔끔하게","\n",com_df.isna().sum()[[n for n in range(len(com_df.isna().sum())) if com_df.isna().sum()[n] != 0]].sort_values())
```
.info()를 overview에 유용하게 사용할 수 있는 이유 중 하나는 위와 같이 null value(=missing value)를 보여주기 때문이다. missing value의 개수만 알고 싶다면 bulit-in function인 .isnull()과 .sum()을 이용해 column 단위의 missing value 개수를 볼 수도 있다. 위의 결과로 총 5개의 column에 missing values가 있음을 알 수 있으며 missing value의 크기 순으로 보면 Cabin > Survived > Age > Embarked > Fare이다. 이 중, 418개의 missing values를 갖고 있는 Survived는 test dataset으로 나눠지며 삭제된 값으로 우리가 model fitting 및 prediction으로 채워야할 것들이므로 채워넣어야할 대상으로 고려하지 않을 것이다.

```python
missing_values = pd.DataFrame(com_df.isnull().sum(), columns = ['The number of missing values'])
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

### 3.3.2. Fill missing values with imputation method
&nbsp;&nbsp;&nbsp;&nbsp;Imputation이라고도 하는 이 작업은 missing value로 비어있는 observation을 특정 방법론으로 추정해 채워넣는 과정이다. 앞서도 얘기했지만 imputation 자체가 연구 분야가 되어 있을 정도로 이 작업이 갖는 의미가 크다. imputation을 하기 위해선 두 가지 정도의 의사결정을 해야 하며 결과에 따라 접근 방법이 조금씩 달라진다. 의사결정이 필요한 내용은 아래와 같다.

1. 어떤 변수가 missing value를 갖고 있는가? 
1. missing value가 어떻게 생긴 것인가? 

첫 번째 내용은 변수의 성질에 관한 것이다. '변수'(Variable, or Feature)라고 통칭되는 이것은 크게 숫자형 변수와 명목형 변수로 나눠지고 그 안에서도 구체적인 성질에 따라 나뉘기 때문에 '어떤 변수'에 missing value가 있는지 알아야 어떤 식의 imputation method를 쓸 지 결정할 수 있다. 이 부분은 2장에서 이미 한 번 다뤘으며 두 번째 내용은 missing value의 구분에 대한 것이다. missing value는 크게 [3가지로 구분](https://en.wikipedia.org/wiki/Missing_data#Types)되며 구분에 따라 사용할 수 있는 방법들에 차이가 있으므로 갖고 있는 data의 missing value가 어디에 속하는지 판단해야 한다.

 imputation에 대한 다양한 방법은 다음 번에 알아보고, 이번에는 가장 쉽게 쓰이는 세 가지 방법 중 하나를 택해 사용하겠다. 세가지 방법은 다음과 같다.
* missing value가 속한 변수에서 missing value를 제외한 값으로 분포를 구한 후 평균과 표준편차에 맞춰 missing value를 채우는 방법
* missing value가 속한 변수와 관련있는 다른 변수들을 이용해 다른 변수들의 조건과 관련성을 고려하여 중앙값으로 missing value를 채우는 방법
* 첫 번째와 두 번째를 혼합해 missing value가 속한 변수와 관련있는 다른 변수들을 이용해 다른 변수들의 조건과 관련성을 고려하여 평균과 표준편차에 맞춰 missing value를 채우는 방법
첫 번째와 세 번째 방법은 변수에 대한 분포가정이 필요하다는 점과 분포를 기준으로한 random sampling을 이용하기 때문에 생기는 오차 가능성을 한계로 갖고 두 번째 방법은 변수 간 관계성을 먼저 증명해야한다는 점과 변수들이 분포를 갖고 있을 경우 중앙값을 사용함으로써 생기는 오차 가능성을 한계로 갖는다. 변수 간의 관계만 밝혀낸다면 두 번째 방법이 좀 더 리스크가 적은 방법이므로 관련성이 존재한다면 두 번째 방법을, 관련성이 존재하지 않거나 밝혀낼 수 없다면 첫 번째 방법을 추천한다. 이제 imputation 이전에 missing value를 갖고 있는 변수에 대해서, 또한 해당 변수와 다른 변수들의 관계를 먼저 알아봐자.


#### 3.3.2.1 [Cabin](https://www.kaggle.com/ccastleberry/titanic-cabin-features)
&nbsp;&nbsp;&nbsp;&nbsp;Cabin은 객실의 번호에 관한 변수로 문자와 숫자가 결합된 mixed variable이다. Cabin은 Titanic dataset에서 가장 많은 1014개의 missing value를 가지고 있으며 이는 Cabin의 77%가 missing value라는 말과 같다. 사실, obs의 수가 굉장히 많은 상황이 아니라면 이 정도 비율을 가진 missing value를 imputation하기 매우 어렵다. imputation을 진행한다고 하더라도 그 방법이 잘못되었다면 오히려 prediction accuracy에 악영향을 미치게 되기 때문에 오히려 imputation을 하지 않는 것을 권장할 수도 있다. 때문에 Cabin을 제외하고 분석한 commit이 대부분이며 그 결과가 나쁜 수준도 아니라 Cabin을 dataset에서 삭제해도 괜찮아보인다. 이제 스스로 선택할 시간이다. Cabin을 버릴 것인가, 아니면 Cabin을 이용해 분석해볼 것인가? Cabin을 이용해 분석해볼 것이라면 상단의 하이퍼링크를 추천한다. 해당 링크는 Cabin만을 이용해 0.68의 점수를 받았다.

```python
print(len(com_df['Cabin'].dropna()))
print(len(com_df['Cabin']))

print(train.iloc[train['Cabin'].dropna().index, :].Survived.value_counts())
print(train.loc[train['Cabin'].isna(), :].Survived.value_counts())
print(136/(136+68))
print(206/(481+206))
```

Cabin을 imputation 하지 않고 Missing vs Non-missing 사이의 생존률 차이만 살펴봐도 0.3 vs 0.66로 Cabin에 value를 갖는 obs가 value를 갖지 않는 obs보다 생존률이 36% 높은 것으로 나타난다. 따라서 무리하게 imputation을 하는 것보다 Cabin을 value : 1, missing value : 0으로 정의된 categorical variable로 바꾸는 것이 더 좋아보인다. 

```python
com_df['Cabin_cate'] = 0

# Cabin이 Non-null인 obs만 Cabin_cate = 1로 바꿔줌
com_df.loc[com_df['Cabin'].dropna().index, 'Cabin_cate'] = 1
com_df.drop(['Cabin'], axis = 1)
com_df.head()
```

> To do. loc, iloc에 대한 이해가 부족한 것 같다. 왜 loc, iloc를 써야하고 어떻게 작동하는지 알아보자. 

#### 3.3.2.2 Age
&nbsp;&nbsp;&nbsp;&nbsp;Age는 생존률과 관련이 있는 중요 변수로 Combine dataset 기준, 263개의 missing value를 갖고 있으며 이는 전체 obs 중 약 20%정도 되는 양이다. 이미 80%의 Age obs가 존재하며 Age와의 관계를 알아볼 수 있는 8개의 변수(Pclass, Fare, Title, Sex_in, Alone, Embarked_int, Cabin_cate, Survived)를 갖고 있으므로 무리없이 imputation을 해볼 수 있을 것이다. 

```python
com_df['Age'].isna().sum() # missing value의 토탈
com_df['Age'].isna().sum()/len(com_df) # 전체 obs 대비 missing value의 비율
com_df[com_df['Age'].isna()] # 'Age'를 missing value로 갖는 obs 
com_df.iloc[com_df['Age'].dropna().index, :] # Age를 value로 갖는 obs
```
```python
sns.countplot(x="Age", hue="Pclass", data=com_df) # Age와 Pclass의 관계를 표현하기 위한 Countplot 
```

