
#### 1. dataset 만들기
```r
# Load the readr, ggplot2, and dplyr packages
library(readr)
library(ggplot2)
library(dplyr)

# Read datasets/confirmed_cases_worldwide.csv into confirmed_cases_worldwide
confirmed_cases_worldwide <- read_csv("datasets/confirmed_cases_worldwide.csv", 
                                     col_types = cols(date = col_date(format = ""), cum_cases= col_double()))

# See the result
confirmed_cases_worldwide
```
read_csv가 아닌 read.csv를 사용해서 다음 단계로 넘어가질 못했다. 사실 read.csv를 사용해도 dataset을 불러오는데는 문제 없지만 column의 데이터 형태를 세부설정하기가 어렵고 실제로 위의 단계에서 read.csv를 사용한다면 date는 string or factor로 cum_cases는 integer로 저장된다. read_csv를 사용하면 column의 type을 설정하기 훨씬 편리하므로 분석에 적절한 형태로 바꿔주기 좋다. 

#### 2. 시간이 지남에 따라 발생한 누적환자에 대한 선 그래프 그리기
```r
# Draw a line plot of cumulative cases vs. date
# Label the y-axis
ggplot(data = confirmed_cases_worldwide, aes(x = date, y = cum_cases)) +
  geom_line() +
  ylab("Cumulative confirmed cases")
```

#### 3. 중국 내 누적 환자와 중국 외 누적 환자의 비교
```r
# Read in datasets/confirmed_cases_china_vs_world.csv
confirmed_cases_china_vs_world <- read_csv("datasets/confirmed_cases_china_vs_world.csv")

# See the result
glimpse(confirmed_cases_china_vs_world)
str(confirmed_cases_china_vs_world)

# Draw a line plot of cumulative cases vs. date, grouped and colored by is_china
# Define aesthetics within the line geom
plt_cum_confirmed_cases_china_vs_world <- ggplot(data = confirmed_cases_china_vs_world) +
  geom_line(aes(x = date, y = cum_cases, , color = is_china, group = is_china)) +
  ylab("Cumulative confirmed cases")

# See the plot
plt_cum_confirmed_cases_china_vs_world
```
이 부분에서도 좀 막혔다. 아래 코드를 이용해도 똑같은 그래프가 그려지지만 quo_name에 대한 불일치로 clear 판정을 받지 못했다. 결과가 같아도 코드 상에서나 object 상에서 다른 정의가 이뤄졌을 수도 있으니까 그럴 수 있겠다고 생각은 하는데 그럼, 3번에서도 x, y를 geom_line 안으로 넣어야 하는 거 아닌가? 제대로 된 설명이 없어서 납득은 안된다. 
```r
# another way
ggplot(data = confirmed_cases_china_vs_world, x = date, y = cum_cases, color = is_china) +
  geom_line(aes(group = is_china)) +
  ylab("Cumulative confirmed cases")

# warning message 1. quo_name(layer$mapping$x) not equal to "date".
# warning message 2. quo_name(layer$mapping$x) not equal to "cum_cases".
```

#### 4. WHO의 대처를 labeling으로 추가하기
```r
who_events <- tribble(
  ~ date, ~ event,
  "2020-01-30", "Global health\nemergency declared",
  "2020-03-11", "Pandemic\ndeclared",
  "2020-02-13", "China reporting\nchange"
) %>%
  mutate(date = as.Date(date))

str(who_events)

# Using who_events, add vertical dashed lines with an xintercept at date
# and text at date, labeled by event, and at 100000 on the y-axis
plt_cum_confirmed_cases_china_vs_world +
  geom_vline(aes(xintercept = date), who_events, linetype = "dashed") +
  geom_text(data = who_events, aes(x = date,label = event), y = 1e5)
```
labeling이 들어갈 y축의 위치를 정해주는 과정에서 헤맸는데 이걸 내가 헤맨건지 datacamp에서 정답을 강요하는 건지 모르겠다. [geom_text()](https://www.rdocumentation.org/packages/ggplot2/versions/3.3.1/topics/geom_label)에 보면 x, y, label이 aesthetics part의 중요한 parameter라는데 그럼 y가 aes 안으로 들어가는 게 더 정석적이지 않나? 애초에 정답이라고 판정한 코드를 실행하던, 오답이라고 판정한 코드를 실행하던 결과는 같다. object를 정의하는데 이점이라도 있는 걸까?

```r
# another way
plt_cum_confirmed_cases_china_vs_world +
  geom_vline(aes(xintercept = date), who_events, linetype = "dashed") +
  geom_text(data = who_events, aes(x = date,label = event, y = 100000))

# warning message 1. text$aes_params$y not equal to 1e+05.
# target is NULL, current is numeric
# The y parameter used in the `geom_text()` is not `1e5`.
```

#### 5. 2월 14일 이후로 중국의 누적환자수의 선형추세 보기
```r
# Filter for China, from Feb 15
china_after_feb15 <- confirmed_cases_china_vs_world %>%
  filter(date >= "2020-02-15" & is_china == "China")

str(china_after_feb15)

# Using china_after_feb15, draw a line plot cum_cases vs. date
# Add a smooth trend line using linear regression, no error bars
ggplot(data = china_after_feb15, aes(x = date, y = cum_cases)) +
  geom_line() +
  geom_smooth(method = "lm", se = FALSE) +
  ylab("Cumulative confirmed cases")
```

#### 6. 중국을 제외한 나라들의 추세 보기
```r
# Filter confirmed_cases_china_vs_world for not China
not_china <- confirmed_cases_china_vs_world %>%
  filter(is_china != "China")

# Using not_china, draw a line plot cum_cases vs. date
# Add a smooth trend line using linear regression, no error bars
plt_not_china_trend_lin <- ggplot(data = not_china, aes(x = date, y = cum_cases)) +
  geom_line() +
  geom_smooth(method = "lm", se = FALSE) +
  ylab("Cumulative confirmed cases")

# See the result
plt_not_china_trend_lin 
```

#### 7. 6번 그래프의 누적환자에 로그를 취해 다시 그려보기
```r
# Modify the plot to use a logarithmic scale on the y-axis
plt_not_china_trend_lin + 
  scale_y_log10(aes(y = cum_cases))
```

#### 8. 중국을 제외한 다른 나라들 중, 심각한 피해를 입은 나라는 어디일까
```r
# Run this to get the data for each country
confirmed_cases_by_country <- read_csv("datasets/confirmed_cases_by_country.csv")
glimpse(confirmed_cases_by_country)

# Group by country, summarize to calculate total cases, find the top 7
top_countries_by_total_cases <- confirmed_cases_by_country %>%
  group_by(country) %>%
  summarize(total_cases = max(cum_cases)) %>%
  top_n(7, total_cases)

# See the result
top_countries_by_total_cases
```

#### 9. 중국을 제외하고 심각한 피해를 입은 나라들의 누적환자 추세
```r
# Run this to get the data for the top 7 countries
confirmed_cases_top7_outside_china <- read_csv("datasets/confirmed_cases_top7_outside_china.csv")

# 
glimpse(confirmed_cases_top7_outside_china)

# Using confirmed_cases_top7_outside_china, draw a line plot of
# cum_cases vs. date, grouped and colored by country
ggplot(data = confirmed_cases_top7_outside_china) + 
    geom_line(aes(x = date, y = cum_cases, color = country, group = country)) + 
    ylab("Cumulative confirmed cases")
```

### 후기  
내용은 기초적인데 이상한 부분에서 사람 짜증나게 하는 프로젝트였다. Datacamp의 course들은 어느정도의 유연성을 갖고 있던데 이 프로젝트는 1) 완벽히 들어맞아야 하는 정답이 존재하고 2) 이게 왜 정답인지 설명해주지 않으며 3) 결과는 같은 나의 오답에 어떤 문제가 있는지 알려주지 않았다. 아직 베타버전이라니 그럴 수 있다고 치고 넘어가는데 다른 프로젝트 몇 개 더 해보고 비슷한 형식이면 안하는 게 정신건강과 시간에 좋을 것 같다. 
