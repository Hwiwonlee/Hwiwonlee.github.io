## Evaluating your measure with factor analysis
#### Starting out with a unidimensional EFA
single-factor explanatory factor analysis을 간단히 해보는 예제다. single-factor explanatory factor analysis는 여러 개의 factor, 그러니까 설문지 응답 같은 변수들이 하나의 factor와 연관이 있는지 알아보는 분석 방법이다. 간단히 예로 다수의 문항을 이용한 심리테스트로 피실험자의 심리상태를 추정하는 설문조사를 들 수 있다. 
```r
# Load the psych package
library(psych)
 
# Conduct a single-factor EFA
EFA_model <- fa(gcbs)

# View the results
EFA_model
```
결과가 꽤 복잡하게 나오는데 결과 중 MR1만 간단히 살펴보자. MR은 Minimum Residual의 약자로 MR1는 최소 잔차를 통해 구한 첫 번째 factor라는 의미다. 결과의 의미는 추가로 공부해야할 것 같다. 

#### Viewing and visualizing the factor loadings
-1부터 1 사이의 값을 갖는 factor loading은 item과 factor 간의 직접적인 연관성 정도를 보여주는 값이다. 
```r
# Set up the single-factor EFA
EFA_model <- fa(gcbs)

# View the factor loadings
EFA_model$loadings

# Create a path diagram of the items' factor loadings
fa.diagram(EFA_model)
```

#### Interpreting individuals' factor scores
Factor score란 EFA로 추정된 item-factor의 관계를 토대로 각 observation들이 factor에 대해 갖는 계산된 값이다. 
```r
# Take a look at the first few lines of the response data and their corresponding sum scores
head(gcbs)
rowSums(head(gcbs))

# Then look at the first few lines of individuals' factor scores
head(EFA_model$scores)

# To get a feel for how the factor scores are distributed, look at their summary statistics and density plot.
summary(EFA_model$scores)

plot(density(EFA_model$scores, na.rm = TRUE), 
    main = "Factor Scores")
```
