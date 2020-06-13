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
Factor score란 EFA로 추정된 item-factor의 관계를 토대로 각 observation들이 factor에 대해 갖는 계산된 값이다. 사실 명확하게 이해가 안돼서 위키피디아의 내용을 인용하겠다.   
> Factor scores (also called component scores in PCA): are the scores of each case (row) on each factor (column). To compute the factor score for a given case for a given factor, one takes the case's standardized score on each variable, multiplies by the corresponding loadings of the variable for the given factor, and sums these products. Computing factor scores allows one to look for factor outliers. Also, factor scores may be used as variables in subsequent modeling.   

추가로 [Factor analysis 에 대한 강의노트](https://stats.idre.ucla.edu/wp-content/uploads/2016/02/part2-1.pdf)를 더 인용하겠다.  
> Factor scores is estimate of the factor value for each individual based on the model and the individual’s observed scores  

위키피디아의 내용을 보면 각 factor에 대한 score를 계산할 수 있는 모양이지만 예제는 minimum residual로부터 계산한 MR1의 factor score만을 다루고 있다. 
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

### Overview of the Measure Development Process
Factor analysis의 Measure Development Process는 아래와 같다.  
 1. Develop items for your measure  
 2. Collect pilot data from a representative sample  
 3. Check out what that dataset looks like  
 4. Consider whether you want to use EFA, CFA, or both  
 5. If both, split your sample into random halves  
 6. Compare the two samples to make sure they are similar  

이 때, CFA는 Confirmatory Factor Analysis를 의미한다. [EFA와 CFA의 정의](https://en.wikipedia.org/wiki/Factor_analysis)로 둘의 차이점을 알아보자.  
> Exploratory factor analysis (EFA) is used to identify complex interrelationships among items and group items that are part of unified concepts. **The researcher makes no a priori assumptions about relationships among factors.**  

> Confirmatory factor analysis (CFA) is a more complex approach that **tests the hypothesis that the items are associated with specific factors.** CFA uses structural equation modeling to test a measurement model whereby loading on the factors allows for evaluation of relationships between observed variables and unobserved variables. Structural equation modeling approaches can accommodate measurement error, and are less restrictive than least-squares estimation. Hypothesized models are tested against actual data, and the analysis would demonstrate loadings of observed variables on the latent variables (factors), as well as the correlation between the latent variables.

> EFA와 CFA의 차이점은 factors에 가설을 가정하느냐 하지 않느냐에서 온다. EFA는 **탐색적**이기 떄문에 factor가 갖는 관계성에 아무런 가정을 부여하지 않지만 CFA는 가설을 **확인하는** 방법이기 떄문에 factor 사이의 연구자가 설정한 가설이 붙는다고 이해하면 조금 편할 것이다. 

#### Descriptive statistics of your dataset
```r
# Basic descriptive statistics
describe(gcbs)

# Graphical representation of error
error.dots(gcbs)

# Graphical representation of error
error.bars(gcbs)
```

#### Splitting your dataset 
```r
# Establish two sets of indices to split the dataset
N <- nrow(gcbs)
indices <- seq(1, N)
indices_EFA <- sample(indices, floor((.5*N)))
indices_CFA <- indices[!(indices %in% indices_EFA)]

# Use those indices to split the dataset into halves for your EFA and CFA
gcbs_EFA <- gcbs[indices_EFA, ]
gcbs_CFA <- gcbs[indices_CFA, ]
```

#### Comparing the halves of your dataset
```r
# Use the indices from the previous exercise to create a grouping variable
group_var <- vector("numeric", nrow(gcbs))
group_var[indices_EFA] <- 1
group_var[indices_CFA] <- 2

# Bind that grouping variable onto the gcbs dataset
gcbs_grouped <- cbind(gcbs, group_var)

# Compare stats across groups
describeBy(gcbs_grouped, group = group_var)
statsBy(gcbs_grouped, group = "group_var")
```
같은 함수형식인 것 같은데 argument type을 다르게 갖는 게 조금 이상하다.


#### Internal reliability
```r
# Estimate coefficient alpha
alpha(gcbs)

# Calculate split-half reliability
splitHalf(gcbs)
```
크론바흐 알파(Cronbach's alpha) 혹은 tau-equivalent reliability는 단일 실행 신뢰도 계수로 고정된 시간에서 여러 항목에 대한 응답자의 신뢰도를 나타낸다. FA에서 크론바흐 알파는 다양한 항목(item)들이 같은 개념을 측정하는지 확인하고자 하는 목적으로 사용된다. 따라서 높은 alpha는 여러 item(혹은 factor)들이 측정하고자 하는 factor를 일관되게 측정하고 있음을 의미한다. 크론바흐 알파는 factor들끼리 상관관계가 클수록, 그리고  factor별 분산들의 차이가 작을수록 크게 계산되며 이는 크론바흐 알파가 factor들의 측정 일관성을 나타낸다는 점에서 직관적으로 이해할 수 있다. 

