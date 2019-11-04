# 2. CSV 파일 
Pandas를 이용한다면 복잡한 코드를 짜지 않아도 함수 몇 개로 csv 파일을 효과적으로 다룰 수 있기 때문에 Pandas module을 이용하는 것이 효율 측면에서 훨씬 좋다.
더불어 Pandas 제공하는 DataFrame class가 갖는 이점까지 생각해보면 Pandas를 사용하지 않을 이유가 전혀 없다. 따라서 Pandas를 이용한 cvs file handling에 집중하겠다. 

```python
import pandas as pd
# read_csv()를 이용한 csv파일 읽기
df = pd.read_csv(csv_0_directory) ## kaggle, 타이타닉 data set의 test.csv를 이용했다. 
df.head() ## load된 data의 head check
print(type(df)) ## class DataFrame

# 특정 행과 열을 필터링하기
## loc[[row], [col]] : label based
## iloc[[row], [col]] : integer based 참고 : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html

df_Survived_loc = df.loc[:, ['PassengerId','Survived']] ## 'label'
df_Survived_iloc = df.iloc[:, [0,1]] ## integer
print(df_Survived_loc)
print(df_Survived_iloc)

## df_Survived_iloc2 = df.iloc[:, [0:2]] ## error, 콜론을 이용한 방법은 interger based가 아님. 

# 조건에 맞는 자료만 뽑아내기
## goal : 2등 객실 이하 + 30대 이상 + 살아남은 승객만 추출
df_goal = df.loc[(df['Pclass'] >= 2) & (df['Age'] >= 30) & (df['Survived'] == 1), :]
# df_goal_error = df.loc[:,(df['Pclass'] >= 2) & (df['Age'] >= 30) & (df['Survived'] == 1)]
## https://nittaku.tistory.com/111 참고
## https://dandyrilla.github.io/2017-08-12/pandas-10min/#ch3 참고
print(df_goal.head())
print(len(df_goal.index)) ## 53개의 data 추출
```
이 부분이 조금 헷갈렸다. 사실 별 거 아니었는데... 헷갈린 부분은 이렇다.

- 왜 'row'의 arg를 조건식으로 선언했을때만 돌아갈까? 왜 col의 arg로 넣으면 에러가 날까?

사실, 위의 조건 _2등 객실 이하 + 30대 이상 + 살아남은 승객만 추출_ 은 '관측값'을 선택하는 것이므로 'row'기준에서 필터링을 하는 게 맞다. col의 arg로 위의 arg를 넣으면 안돌아가는 이유도 당연한데, 선언된 조건이 이미 col 기준으로 작성되었기 때문에 .loc()에 조건식을 또 넣는다는 것 자체가 불가능하다. 
```python
# 특정 조건을 만족하는 열만 추출하기
## '열'이름에서 'a'가 들어가는 열만 추출하기
df_col_in_a = df.filter(regex='a|A')
print(df_col_in_a) 
## https://stackoverflow.com/questions/21285380/find-column-whose-name-contains-a-specific-string
```
