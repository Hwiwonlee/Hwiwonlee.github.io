# 1. Graphical exploratory data analysis
## 1.1 Plotting a histogram

```python
# Plotting a histogram of iris data
import matplotlib.pyplot as plt
import seaborn as sns

sns.set() ## Set default Seaborn style
plt.hist(versicolor_petal_length) ## Plot histogram of versicolor petal lengths

plt.show() ## Show histogram
```
> Q. seaborn style의 차이?
> A.

```python
# Axis labels!
_= plt.hist(versicolor_petal_length) ## Plot histogram of versicolor petal lengths
plt.xlabel('petal length (cm)') ## Label axes
plt.ylabel('count')

plt.show()
```
> Q. '_=' 이렇게 해도 돌아가네?  
> A. 'under score'를 사용하는 경우가 종종 있는데, 이 경우는 '마지막 값을 저장하기 위해' 사용하는 것 같다. [출처](https://mingrammer.com/underscore-in-python/)

```python
# Adjusting the number of bins in a histogram
import numpy as np

n_data = len(versicolor_petal_length) ## Compute number of data points: n_data
n_bins = np.sqrt(n_data) ## Number of bins is the square root of number of data points: n_bins
n_bins = int(n_bins) ## Convert number of bins to integer: n_bins

plt.hist(versicolor_petal_length, bins = n_bins) ## Plot the histogram

_ = plt.xlabel('petal length (cm)')
_ = plt.ylabel('count') ## Label axes

plt.show() ## Show histogram
```

## 1.2 Plot all of your data: Bee swarm plots

```python
# Bee swarm plot
sns.swarmplot(x='species', y='petal length (cm)', data = df) ## Create bee swarm plot with Seaborn's default settings

plt.xlabel('species')
plt.ylabel('petal length (cm)')
plt.show()
```

## 1.3 Plot all of your data: ECDFs(Empirical Cummulative Density Functions)
```python
# Computing the ECDF
def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y
```

```python
# Plotting the ECDF
x_vers, y_vers = ecdf(versicolor_petal_length) ## Compute ECDF for versicolor data: x_vers, y_vers

plt.plot(x_vers, y_vers, marker = '.', linestyle = 'none') ## Generate plot

plt.xlabel('length')
plt.ylabel('ECDF')
plt.show()
```

```python
# Comparison of ECDFs
## Compute ECDFs
x_set, y_set = ecdf(setosa_petal_length)
x_vers, y_vers = ecdf(versicolor_petal_length)
x_virg, y_virg = ecdf(virginica_petal_length)

## Plot all ECDFs on the same plot
plt.plot(x_set, y_set, marker='.', linestyle='none')
plt.plot(x_vers, y_vers, marker='.', linestyle='none')
plt.plot(x_virg, y_virg, marker='.', linestyle='none')


plt.legend(('setosa', 'versicolor', 'virginica'), loc='lower right')
_ = plt.xlabel('petal length (cm)')
_ = plt.ylabel('ECDF')

plt.show()
```

# 2. Quantitative exploratory data analysis
## 2.1 Introduction to summary statistics: The sample mean and median

```python
# Computing means
mean_length_vers = np.mean(versicolor_petal_length) ## Compute the mean: mean_length_vers
print('I. versicolor:', mean_length_vers, 'cm') ## Print the result with some nice formatting
```

## 2.2 Percentiles, outliers, and box plots

```python
# Computing percentiles
percentiles = np.array([2.5, 25, 50, 75, 97.5]) ## Specify array of percentiles: percentiles
ptiles_vers = np.percentile(versicolor_petal_length, percentiles) ## Compute percentiles: ptiles_vers

print(ptiles_vers)
```

```python
# Comparing percentiles to ECDF
_ = plt.plot(x_vers, y_vers, '.')
_ = plt.xlabel('petal length (cm)')
_ = plt.ylabel('ECDF') ## Plot the ECDF

_ = plt.plot(ptiles_vers, percentiles/100, marker='D', color='red',
         linestyle='none') ## Overlay percentiles as red diamonds.
plt.show()
```
> 해당 percentiles만 'Red diamond'로 표시됨. 신기하고 예쁘네. 

```python
# Box-and-whisker plot
_ = sns.boxplot(x='species', y='petal length (cm)', data = df) ## Create box plot with Seaborn's default settings

_ = plt.xlabel('species')
_ = plt.ylabel('petal length') 
plt.show()
```

## 2.3 Variance and std

```python
# Computing thre variance 
differences = versicolor_petal_length - np.mean(versicolor_petal_length) ## Array of differences to mean: differences
diff_sq = differences ** 2 ## Square the differences: diff_sq

variance_explicit = np.mean(diff_sq) ## Compute the mean square difference: variance_explicit
variance_np = np.var(versicolor_petal_length) ## Compute the variance using NumPy: variance_np

print(variance_explicit,variance_np)

# The standard deviation and the variance
variance = np.var(versicolor_petal_length)

print(np.sqrt(variance))
print(np.std(versicolor_petal_length))
```

## 2.4 Covariance and the Pearson correlation coefficient

```python
# Scatter plots
plt.plot(versicolor_petal_length, versicolor_petal_width, marker = '.', linestyle = 'none')

_=plt.xlabel('length')
_=plt.ylabel('width')
plt.show()
```

```python
# Computing the covariance
covariance_matrix = np.cov(versicolor_petal_length, versicolor_petal_width) ## Compute the covariance matrix: covariance_matrix
print(covariance_matrix)

petal_cov = covariance_matrix[0,1] ## Extract covariance of length and width of petals: petal_cov
print(petal_cov)

# Computing the Pearson correlation coefficient
def pearson_r(x, y):
    """Compute Pearson correlation coefficient between two arrays."""
    ## Compute correlation matrix: corr_mat
    corr_mat = np.corrcoef(x, y)

    ## Return entry [0,1]
    return corr_mat[0,1]

r = pearson_r(versicolor_petal_length, versicolor_petal_width) ## Compute Pearson correlation coefficient for I. versicolor: r
print(r)
```

# 3. Thinking probabilistically-- Discrete variables
## 3.1 Random number generators and hacker statistics

```python
# Generating random numbers using the np.random module
np.random.seed(42) ## Seed the random number generator

random_numbers = np.empty(100000) ## Initialize random numbers: random_numbers

##Generate random numbers by looping over range(100000)
for i in range(100000):
    random_numbers[i] = np.random.random()

_ = plt.hist(random_numbers)
plt.show()

```

```python
# The np.random module and Bernoulli trials
def perform_bernoulli_trials(n, p):
    """Perform n Bernoulli trials with success probability p
    and return number of successes."""
    ## Initialize number of successes: n_success
    n_success = 0

    ## Perform trials
    for i in range(n):
        ## Choose random number between zero and one: random_number
        random_number = np.random.random(0, 1)

        ## If less than p, it's a success so add one to n_success
        if random_number < p:
            n_success += 1

    return n_success
```

```python
# How many defaults might we expect?
np.random.seed(42)
n_defaults = np.empty(1000)

## Compute the number of defaults
for i in range(1000):
    n_defaults[i] = perform_bernoulli_trials(100, 0.05)

_ = plt.hist(n_defaults, normed = True)
_ = plt.xlabel('number of defaults out of 100 loans')
_ = plt.ylabel('probability')
plt.show()
```

```python
# Will the bank fail?
x, y = ecdf(n_defaults) ## Compute ECDF: x, y

## Plot the ECDF with labeled axes
_=plt.plot(x, y, marker = '.', linestyle = 'none')
_=plt.xlabel('number of defaults out of 100 loans')
_=plt.ylabel('CDF')
plt.show()

n_lose_money = np.sum(n_defaults >= 10) ## Compute the number of 100-loan simulations with 10 or more defaults: n_lose_money
print('Probability of losing money =', n_lose_money / len(n_defaults))
```

## 3.2 Probability distributions and stories: The Binomial distribution
```python
# Sampling out of the Binomial distribution
n_defaults = np.random.binomial(100, 0.05, 10000) ## Take 10,000 samples out of the binomial distribution: n_defaults

x, y = ecdf(n_defaults)

_=plt.plot(x, y, marker = '.', linestyle = 'none')
_=plt.xlabel('number of defaults out of 100 loans')
_=plt.ylabel('CDF')
plt.show()
```

```python
Plotting the Binomial PMF
bins = np.arange(min(n_defaults), max(n_defaults)+1.5) - 0.5 ## Compute bin edges: bins

_=plt.hist(n_defaults, normed=True, bins=bins)
_=plt.xlabel('number of defaults out of 100 loans')
_=plt.ylabel('PMF')
plt.show()
```
> pmf(probability mass function)라는 단어 되게 오랜만에 본다. pmf, pdf 구분하는 게 맞긴 한데, 정말 많은 경우(경험상 95% 이상) pdf로 퉁쳐서 부른다. 


## 3.3 Poisson processes and the Poisson distribution
```python
# Relationship between Binomial and Poisson distributions
samples_poisson = np.random.poisson(10, 10000) ## Draw 10,000 samples out of Poisson distribution: samples_poisson

## Print the mean and standard deviation
print('Poisson:     ', np.mean(samples_poisson),
                       np.std(samples_poisson))

## Specify values of n and p to consider for Binomial: n, p
n = [20, 100, 1000]
p = [0.5, 0.1, 0.01]


## Draw 10,000 samples for each n,p pair: samples_binomial
for i in range(3):
    samples_binomial = np.random.binomial(n[i], p[i], size=10000)

    print('n =', n[i], 'Binom:', np.mean(samples_binomial),
                                 np.std(samples_binomial))
```

```python
# Was 2015 anomalous?
n_nohitters = np.random.poisson(251/115, 10000) ## Draw 10,000 samples out of Poisson distribution: n_nohitters

n_large = np.sum(n_nohitters >= 7) ## Compute number of samples that are seven or greater: n_large
p_large = n_large/10000 ## Compute probability of getting seven or more: p_large

print('Probability of seven or more no-hitters:', p_large)
```

# 4. Thinking probabilistically-- Continuous variables
## 4.1 Introduction to the Normal distribution


```python
# The Normal PDF
## Draw 100000 samples from Normal distribution with stds of interest: samples_std1, samples_std3, samples_std10
samples_std1 = np.random.normal(20, 1, 100000)
samples_std3 = np.random.normal(20, 3, 100000)
samples_std10 = np.random.normal(20, 10, 100000)

## Make histograms
plt.hist(samples_std1, normed = True, histtype='step', bins=100)
plt.hist(samples_std3, normed = True, histtype='step', bins=100)
plt.hist(samples_std10, normed = True, histtype='step', bins=100)



## Make a legend, set limits and show plot
_ = plt.legend(('std = 1', 'std = 3', 'std = 10'))
plt.ylim(-0.01, 0.42)
plt.show()
```

```python
# The Normal CDF
x_std1, y_std1 = ecdf(samples_std1)
x_std3, y_std3 = ecdf(samples_std3)
x_std10, y_std10 = ecdf(samples_std10)

_=plt.plot(x_std1, y_std1, marker ='.', linestyle='none')
_=plt.plot(x_std3, y_std3, marker ='.', linestyle='none')
_=plt.plot(x_std10, y_std10, marker ='.', linestyle='none')

_ = plt.legend(('std = 1', 'std = 3', 'std = 10'), loc='lower right')
plt.show()
```

## 4.2 The Normal distribution: Properties and warnings

```python
# Are the Belmont Stakes results Normally distributed?
## Compute mean and standard deviation: mu, sigma
mu = np.mean(belmont_no_outliers)
sigma = np.std(belmont_no_outliers)

samples = np.random.normal(mu, sigma, 10000) ## Sample out of a normal distribution with this mu and sigma: samples

## Get the CDF of the samples and of the data
x, y = ecdf(belmont_no_outliers)
x_theor, y_theor = ecdf(samples)

## Plot the CDFs and show the plot
_ = plt.plot(x_theor, y_theor)
_ = plt.plot(x, y, marker='.', linestyle='none')
_ = plt.xlabel('Belmont winning time (sec.)')
_ = plt.ylabel('CDF')
plt.show()
```

```python
# What are the chances of a horse matching or beating Secretariat's record?
samples = np.random.normal(mu, sigma, 1000000) ## Take a million samples out of the Normal distribution: samples

prob = np.sum(samples <= 144) / 1000000 ## Compute the fraction that are faster than 144 seconds: prob

print('Probability of besting Secretariat:', prob) ## Print the result
```

## 4.3 The Exponential distribution
```python
# If you have a story, you can simulate it!
def successive_poisson(tau1, tau2, size=1):
    """Compute time for arrival of 2 successive Poisson processes."""
    ## Draw samples out of first exponential distribution: t1
    t1 = np.random.exponential(tau1, size)

    ## Draw samples out of second exponential distribution: t2
    t2 = np.random.exponential(tau2, size)

    return t1 + t2

# Distribution of no-hitters and cycles
"""Now, you'll use your sampling function to compute the waiting time to observe a no-hitter and hitting of the cycle. The mean waiting time for a no-hitter is 764 games, and the mean waiting time for hitting the cycle is 715 games."""

waiting_times = successive_poisson(764, 715, 100000) ## Draw samples of waiting times: waiting_times

plt.hist(waiting_times, bins = 100, normed = True, histtype='step') ## Make the histogram

plt.xlabel('the waiting time') 
plt.ylabel('PDF')
plt.show()
```
