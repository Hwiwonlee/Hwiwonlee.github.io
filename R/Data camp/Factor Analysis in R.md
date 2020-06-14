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

## Multidimensional EFA
### Determining dimensionality
Factor analysis의 대표적인 예시인 PCA가 reduction dimensionality의 효과가 있는 것처럼 EFA 또한 차원 감소의 목적으로 사용된다. 이론적으로 봐도  PCA, EFA 모두 eigen value & eigen vector를 사용하기 때문에 전개가 거의 비슷하다. 따라서 이 절에서는 eigen value를 구하는 법을 배우는데...정작 eigen value와 eigen vector로 어떻게 차원감소가 이뤄지는지까지는 나오지 않는다. 나중에 따로 정리해봐야겠다. 

```r
# Establish two sets of indices to split the dataset
N <- nrow(bfi)
indices <- seq(1, N)
indices_EFA <- sample(indices, floor((.5*N)))
indices_CFA <- indices[!(indices %in% indices_EFA)]

# Use those indices to split the dataset into halves for your EFA and CFA
bfi_EFA <- bfi[indices_EFA, ]
bfi_CFA <- bfi[indices_CFA, ]

# Calculate the correlation matrix first
bfi_EFA_cor <- cor(bfi_EFA, use = "pairwise.complete.obs")

# Then use that correlation matrix to calculate eigenvalues
eigenvals <- eigen(bfi_EFA_cor)

# Look at the eigenvalues returned
eigenvals$values

# Calculate the correlation matrix first
bfi_EFA_cor <- cor(bfi_EFA, use = "pairwise.complete.obs")

# Then use that correlation matrix to create the scree plot
scree(bfi_EFA_cor, factors = FALSE)
```

### Understanding multidimensional data
factor와 item을 혼용해서 사용하는데 명확한 구분이 있는 걸까? loading과 factor score에 대해서도 모호하게 설명하고 넘어가는데 좀 아쉽다. 

```r
# Run the EFA with six factors (as indicated by your scree plot)
EFA_model <- fa(bfi_EFA, nfactors = 6)

# View results from the model object
EFA_model

# Run the EFA with six factors (as indicated by your scree plot)
EFA_model <- fa(bfi_EFA, nfactors = 6)

# View items' factor loadings
EFA_model$loadings

# View the first few lines of examinees' factor scores
head(EFA_model$scores)
```
그래도 나중에 설명해준다. 
An item's loadings represent the amount of information it provides for each factor. Items’ meaningful loadings will be displayed in the output. You’ll notice that many items load onto more than one factor, which means they provide information about multiple factors. This may not be desirable for measure development, so some researchers consider **only** the strongest loading for each item.

Each examinee will have a factor score for each factor, so that the matrix won't include blanks. However, examinees with missing data will receive NA scores on all factors.

## Investigating model fit
EFA는 absolute fit test과 relative fit test의 두 가지 방법으로 model fitting test를 한다. 두 fit test의 차이점을 쉽게 설명하면, absolute fit test는 model 자체의 fitting test고 relative fit test는 유의한 model에서 optimal number of factors를 결정하기 위한 방법이다.  relative fit test에서 BIC가 되는 걸 보면 AIC와 같은 다른 값들도 사용가능하지 않을까 추측해본다. 

Absolute fit statistics have intrinsic meaning and suggested cutoff values.  
 1) Chi-square test : model 자체의 유의성만 판단, N이 커지면 보통 유의하다는 결과를 줌.  
 2) Tucker-Lewis Index (TLI) : 0.9보다 크면 well fitting    
 3) Root Mean Square Error of Approximation (RMSEA) : 0.05보다 작으면 well fitting   
Relative fit statistics only have meaning when comparing models.  
 1) Bayesian Information Criterion (BIC)  


```r
# Run each theorized EFA on your dataset
bfi_theory <- fa(bfi_EFA, nfactors = 5)
bfi_eigen <- fa(bfi_EFA, nfactors = 6)

# Compare the BIC values
bfi_theory$BIC
bfi_eigen$BIC
```

## Confirmatory Factor Analysis
### Setting up a CFA
CFA(Confirmatory Factor Analysis)와 EFA의 차이로 factor와 item 사이의 이론적 가설이나 가정의 존재를 말한 적이 있다. CFA는 factor와 item 사이에 밝혀진 이론이나 연구자의 가설이 설정된 상태에서 이뤄지는 분석이다. 따라서 factor와 item 사이의 관계를 먼저 설정하는 것이 첫 단계이다.  
Benefits of a confirmatory analysis:  
 1) Explicitly specified variable/factor relationships
 2) Testing a theory that you know in advance
 3) This is the right thing to publish when you are developing a new measure!

```r
# Conduct a five-factor EFA on the EFA half of the dataset
EFA_model <- fa(bfi_EFA, nfactors = 5)

# Use the wrapper function to create syntax for use with the sem() function
EFA_syn <- structure.sem(EFA_model)

# Set up syntax specifying which items load onto each factor
theory_syn_eq <- "
AGE: A1, A2, A3, A4, A5
CON: C1, C2, C3, C4, C5
EXT: E1, E2, E3, E4, E5
NEU: N1, N2, N3, N4, N5
OPE: O1, O2, O3, O4, O5
"

# Feed the syntax in to have variances and covariances automatically added
theory_syn <- cfa(text = theory_syn_eq, 
                  reference.indicators = FALSE)
```

### Understanding the sem() syntax
```r
# Use the sem() function to run a CFA
theory_CFA <- sem(theory_syn, data = bfi_CFA)

# Use the summary function to view fit information and parameter estimates
summary(theory_CFA)
```

### Investigating model fit
```r
# Set the options to include various fit indices so they will print
options(fit.indices = c("CFI", "GFI", "RMSEA", "BIC"))

# Use the summary function to view fit information and parameter estimates
summary(theory_CFA)

# Run a CFA using the EFA syntax you created earlier
EFA_CFA <- sem(EFA_syn, data = bfi_CFA)

# Locate the BIC in the fit statistics of the summary output
summary(EFA_CFA)$BIC

# Compare EFA_CFA BIC to the BIC from the CFA based on theory
summary(theory_CFA)$BIC
```

## Refining your measure and/or model  
### EFA vs. CFA revisited  
EFA:  
- Estimates all possible variable/factor relationships  
- Looking for patterns in the data  
- Use when you don't have a well-developed theory  
  
CFA:  
- Only specified variable/factor relationships  
- Testing a theory that you know in advance  
- This is the right thing to publish!  

```r
# View the first five rows of the EFA loadings
EFA_model$loadings[1:5,]

# View the first five loadings from the CFA estimated from the EFA results
summary(EFA_CFA)$coeff[1:5,]

# Extracting factor scores from the EFA model
EFA_scores <- EFA_model$scores

# Calculating factor scores by applying the CFA parameters to the EFA dataset
CFA_scores <- fscores(EFA_CFA, data = bfi_EFA)

# Comparing factor scores from the EFA and CFA results from the bfi_EFA dataset
plot(density(EFA_scores[,1], na.rm = TRUE), 
    xlim = c(-3, 3), ylim = c(0, 1), col = "blue")
lines(density(CFA_scores[,1], na.rm = TRUE), 
    xlim = c(-3, 3), ylim = c(0, 1), col = "red")
```

### Adding loadings to improve fit
Remember:  
- EFAs estimate all item/factor loadings  
- CFAs only estimate specified loadings  
- Poor model fit could be due to excluded loadings  

EFA는 모든 item을 사용하고 CFA는 가설에 속한 item과 factor와의 관계를 이용하기 때문에 특정 item과 factor만 사용한다. 따라서 loading을 추가하는 작업은 CFA에서만 가능하다. 
```r
# Add some plausible item/factor loadings to the syntax
theory_syn_add <- "
AGE: A1, A2, A3, A4, A5
CON: C1, C2, C3, C4, C5
EXT: E1, E2, E3, E4, E5, N4
NEU: N1, N2, N3, N4, N5, E3
OPE: O1, O2, O3, O4, O5
"

# Convert your equations to sem-compatible syntax
theory_syn2 <- cfa(text = theory_syn_add, reference.indicators = FALSE)

# Run a CFA with the revised syntax
theory_CFA_add <- sem(model = theory_syn2, data = bfi_CFA)

# Conduct a likelihood ratio test
anova(theory_CFA, theory_CFA_add)

# Compare the comparative fit indices - higher is better!
summary(theory_CFA)$CFI
summary(theory_CFA_add)$CFI

# Compare the RMSEA values - lower is better!
summary(theory_CFA)$RMSEA
summary(theory_CFA_add)$RMSEA

# Compare BIC values
summary(theory_CFA)$BIC
summary(theory_CFA_add)$BIC
```

### Improving fit by removing loadings

```r
# Remove the weakest factor loading from the syntax
theory_syn_del <- "
AGE: A1, A2, A3, A4, A5
CON: C1, C2, C3, C4, C5
EXT: E1, E2, E3, E4, E5
NEU: N1, N2, N3, N4, N5
OPE: O1, O2, O3, O5
"

# Convert your equations to sem-compatible syntax
theory_syn3 <- cfa(text = theory_syn_del, reference.indicators = FALSE)

# Run a CFA with the revised syntax
theory_CFA_del <- sem(model = theory_syn3, data = bfi_CFA)

# Compare the comparative fit indices - higher is better!
summary(theory_CFA)$CFI
summary(theory_CFA_del)$CFI

# Compare the RMSEA values - lower is better!
summary(theory_CFA)$RMSEA
summary(theory_CFA_del)$RMSEA

# Compare BIC values
summary(theory_CFA)$BIC
summary(theory_CFA_del)$BIC
```
