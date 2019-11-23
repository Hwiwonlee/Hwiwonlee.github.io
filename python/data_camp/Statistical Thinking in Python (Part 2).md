# 1. Parameter estimation by optimization
## 1.1 Optimal parameters

```python
# How often do we get no-hitters?
np.random.seed(42) ## Seed random number generator
tau = nohitter_times.mean() ## Compute mean no-hitter time: tau

inter_nohitter_time = np.random.exponential(tau, 100000) ## Draw out of an exponential distribution with parameter tau

## Plot the PDF and label axes
_ = plt.hist(inter_nohitter_time,
             bins=50, normed=True, histtype='step')
_ = plt.xlabel('Games between no-hitters')
_ = plt.ylabel('PDF')
plt.show()
```

```python
# Do the data follow our story?
x, y = ecdf(nohitter_times) ## Create an ECDF from real data: x, y
x_theor, y_theor = ecdf(inter_nohitter_time) ## Create a CDF from theoretical samples: x_theor, y_theor

## Overlay the plots
plt.plot(x_theor, y_theor)
plt.plot(x, y, marker='.', linestyle='none')

## Margins and axis labels
plt.margins(0.02)
plt.xlabel('Games between no-hitters')
plt.ylabel('CDF')

plt.show()
```

```python
# How is this parameter optimal?
## Plot the theoretical CDFs
plt.plot(x_theor, y_theor)
plt.plot(x, y, marker='.', linestyle='none')
plt.margins(0.02)
plt.xlabel('Games between no-hitters')
plt.ylabel('CDF')

samples_half = np.random.exponential(tau/2, 10000) ## Take samples with half tau: samples_half
samples_double = np.random.exponential(tau*2, 10000) ## Take samples with double tau: samples_double

## Generate CDFs from these samples
x_half, y_half = ecdf(samples_half)
x_double, y_double = ecdf(samples_double)

## Plot these CDFs as lines
_ = plt.plot(x_half, y_half)
_ = plt.plot(x_double, y_double)
plt.show()
```

## 1.2 Linear regression by least squares

```python
# EDA of literacy/fertility data
_ = plt.plot(illiteracy, fertility, marker='.', linestyle='none') ## Plot the illiteracy rate versus fertility

## Set the margins and label axes
plt.margins(0.02)
_ = plt.xlabel('percent illiterate')
_ = plt.ylabel('fertility')
plt.show()

print(pearson_r(illiteracy, fertility)) ## Show the Pearson correlation coefficient
```

```python
# Linear regression
## Plot the illiteracy rate versus fertility
_ = plt.plot(illiteracy, fertility, marker='.', linestyle='none')
plt.margins(0.02)
_ = plt.xlabel('percent illiterate')
_ = plt.ylabel('fertility')

a, b = np.polyfit(illiteracy, fertility, deg = 1) ## Perform a linear regression using np.polyfit(): a, b
## np.polyfit(x, y, deg) : deg = n차식에 대한 parameter

## Print the results to the screen
print('slope =', a, 'children per woman / percent illiterate')
print('intercept =', b, 'children per woman')

## Make theoretical line to plot
x = np.array([0, 100])
y = a * x + b
## 난 0부터 100까지의 sequence인 줄 알았는데 그냥 0, 100이었음.
## 이걸 theoretical하다고 볼 수 있나? 오히려 두 점으로 이뤄진 직선이라 theoretical하다고 볼 수도 있겠네. 

_ = plt.plot(x, y) ## Add regression line to your plot
plt.show()
```

```python
# How is it optimal?
a_vals = np.linspace(0, 0.1, 200) ## Specify slopes to consider: a_vals
rss = np.empty_like(a_vals) ## Initialize sum of square of residuals: rss
## The empty_like() function returns a new array with the same shape and type as a given array

## Compute sum of square of residuals for each value of a_vals : SSE or RSS
for i, a in enumerate(a_vals):
    rss[i] = np.sum((fertility - a*illiteracy - b)**2)

## Plot the RSS
plt.plot(a_vals, rss, '-')
plt.xlabel('slope (children per woman / percent illiterate)')
plt.ylabel('sum of square of residuals')
plt.show()
```

## 1.3 The importance of EDA: Anscombe's quartet
```python
# Linear regression on appropriate Anscombe data
a, b = np.polyfit(x, y, deg = 1) ## Perform linear regression: a, b
print(a, b) ## Print the slope and intercept

## Generate theoretical x and y data: x_theor, y_theor
x_theor = np.array([3, 15])
y_theor = a * x_theor + b

## Plot the Anscombe data and theoretical line
_ = plt.plot(x, y, marker='.', linestyle = 'none')
_ = plt.plot(x_theor, y_theor)

plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

```python
# Linear regression on all Anscombe data
## Iterate through x,y pairs
for x, y in zip(anscombe_x , anscombe_y ):
    # Compute the slope and intercept: a, b
    a, b = np.polyfit(x, y, deg = 1)

    # Print the result
    print('slope:', a, 'intercept:', b)
```

# 2. Bootstrap confidence intervals
## 2.1 Generating bootstrap replicates
```python
# Visulizing bootstrap samples
for _ in range(50):
    ## Generate bootstrap sample: bs_sample
    bs_sample = np.random.choice(rainfall, size=len(rainfall))

    ## Compute and plot ECDF from bootstrap sample
    x, y = ecdf(bs_sample)
    _ = plt.plot(x, y, marker='.', linestyle='none',
                 color='gray', alpha=0.1)

## Compute and plot ECDF from original data
x, y = ecdf(rainfall)
_ = plt.plot(x, y, marker='.')

## Make margins and label axes
plt.margins(0.02)
_ = plt.xlabel('yearly rainfall (mm)')
_ = plt.ylabel('ECDF')
plt.show()
```

## 2.2 Bootstrap confidence interval
```python
# Generating many bootstrap replicates

def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""

    ## Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    ## Generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data, func)

    return bs_replicates
```
draw_bs_reps()은 'data'를 받아서 선언된 'func'에 따라 'size'개의 bootstrap replicates를 return하는 함수다. 

```python
# Bootstrap replicates of the mean and the SEM(Standard Error of the Mean)
bs_replicates = draw_bs_reps(data=rainfall, func=np.mean, size=10000) ## Take 10,000 bootstrap replicates of the mean: bs_replicates

sem = np.std(rainfall) / np.sqrt(len(rainfall)) ## Compute and print SEM
print(sem)

bs_std = np.std(bs_replicates) ## Compute and print standard deviation of bootstrap replicates
print(bs_std)

## Make a histogram of the results
_ = plt.hist(bs_replicates, bins=50, normed=True)
_ = plt.xlabel('mean annual rainfall (mm)')
_ = plt.ylabel('PDF')
plt.show()
```

```python
# Bootstrap replicates of other statistics
bs_replicates = draw_bs_reps(rainfall, np.var, 10000) ## Generate 10,000 bootstrap replicates of the variance: bs_replicates
bs_replicates = bs_replicates / 100 # # Put the variance in units of square centimeters for convenience 

## Make a histogram of the results
_ = plt.hist(bs_replicates, bins = 50, normed = True)
_ = plt.xlabel('variance of annual rainfall (sq. cm)')
_ = plt.ylabel('PDF')
plt.show()
```

```python
# Confidence interval on the rate of no-hitters
bs_replicates = draw_bs_reps(nohitter_times, np.mean, 10000) ## Draw bootstrap replicates of the mean no-hitter time (equal to tau): bs_replicates 
conf_int = np.percentile(bs_replicates, [2.5, 97.5]) ## Compute the 95% confidence interval: conf_int

print('95% confidence interval =', conf_int, 'games')

## Plot the histogram of the replicates
_ = plt.hist(bs_replicates, bins=50, normed=True)
_ = plt.xlabel(r'$\tau$ (games)')
_ = plt.ylabel('PDF')
plt.show()

```
## 2.3 Pairs bootstrap 

```python
# A function to do pairs bootstrap
## def draw_bs_pairs_linreg(x, y, size=1):
    """Perform pairs bootstrap for linear regression."""

    # Set up array of indices to sample from: inds
    inds = np.arange(len(x))

    # Initialize replicates: bs_slope_reps, bs_intercept_reps
    bs_slope_reps = np.empty(size)
    bs_intercept_reps = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_inds = np.random.choice(inds, size=len(inds))
        bs_x, bs_y = x[bs_inds], y[bs_inds]
        bs_slope_reps[i], bs_intercept_reps[i] = np.polyfit(bs_x, bs_y, deg = 1)

    return bs_slope_reps, bs_intercept_reps
```
```python
# Pairs bootstrap of literacy/fertility data
bs_slope_reps, bs_intercept_reps = draw_bs_pairs_linreg(illiteracy, fertility, 1000) ## Generate replicates of slope and intercept using pairs bootstrap
print(np.percentile(bs_slope_reps, [2.5, 97.5])) ## Compute and print 95% CI for slope

## Plot the histogram
_ = plt.hist(bs_slope_reps, bins=50, normed=True)
_ = plt.xlabel('slope')
_ = plt.ylabel('PDF')
plt.show()
```

```python
# Plotting bootstrap regressions
x = np.array([0, 100]) ### Generate array of x-values for bootstrap lines: x

## Plot the bootstrap lines
for i in range(100):
    _ = plt.plot(x, 
                 bs_slope_reps[i]*x + bs_intercept_reps[i],
                 linewidth=0.5, alpha=0.2, color='red')

## Plot the data
_ = plt.plot(illiteracy, fertility, marker = '.', linestyle='none')
_ = plt.xlabel('illiteracy')
_ = plt.ylabel('fertility')
plt.margins(0.02)
plt.show()
```

# 3. Introduction to hypothesis testing
## 3.1 Formulating and simulating a hypothesis

```python
# Generating a permutation sample
def permutation_sample(data1, data2):
    """Generate a permutation sample from two data sets."""

    ## Concatenate the data sets: data
    data = np.concatenate([data1, data2])

    ## Permute the concatenated array: permuted_data
    permuted_data = np.random.permutation(data)

    ## Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2
```

```python
# Visualizing permutation sampling
for i in range(50):
    ## Generate permutation samples
    perm_sample_1, perm_sample_2 = permutation_sample(rain_june, rain_november)


    ## Compute ECDFs
    x_1, y_1 = ecdf(perm_sample_1)
    x_2, y_2 = ecdf(perm_sample_2)

    ## Plot ECDFs of permutation sample
    _ = plt.plot(x_1, y_1, marker='.', linestyle='none',
                 color='red', alpha=0.02)
    _ = plt.plot(x_2, y_2, marker='.', linestyle='none',
                 color='blue', alpha=0.02)

## Create and plot ECDFs from original data
x_1, y_1 = ecdf(rain_june)
x_2, y_2 = ecdf(rain_november)
_ = plt.plot(x_1, y_1, marker='.', linestyle='none', color='red')
_ = plt.plot(x_2, y_2, marker='.', linestyle='none', color='blue')

## Label axes, set margin, and show plot
plt.margins(0.02)
_ = plt.xlabel('monthly rainfall (mm)')
_ = plt.ylabel('ECDF')
plt.show()
```

## 3.2 Test statistics and p-values

```python
# Generating permutation replicates
def draw_perm_reps(data_1, data_2, func, size=1):
    """Generate multiple permutation replicates."""

   ## Initialize array of replicates: perm_replicates
    perm_replicates = np.empty(size)

    for i in range(size):
        ## Generate permutation sample
        perm_sample_1, perm_sample_2 = permutation_sample(data_1, data_2)

        ## Compute the test statistic
        perm_replicates[i] = func(perm_sample_1, perm_sample_2)

    return perm_replicates
```

```python
# Look before you leap: EDA before hypothesis testing
_ = sns.swarmplot(x='ID', y='impact_force', data=df) ## Make bee swarm plot

_ = plt.xlabel('frog')
_ = plt.ylabel('impact force (N)')
plt.show()
```

```python
# Permutation test on frog data
def diff_of_means(data_1, data_2):
    """Difference in means of two arrays."""

    ## The difference of means of data_1, data_2: diff
    diff = np.mean(data_1) - np.mean(data_2)

    return diff

empirical_diff_means = np.mean(force_a) - np.mean(force_b) ## Compute difference of mean impact force from experiment: empirical_diff_means

## Draw 10,000 permutation replicates: perm_replicates
perm_replicates = draw_perm_reps(force_a, force_b,
                                 diff_of_means, size=10000)
p = np.sum(perm_replicates >= empirical_diff_means) / len(perm_replicates) ## Compute p-value: p
print('p-value =', p)
```

## 3.3 Bootstrap hypothesis tests

```python
# A one-sample bootstrap hypothesis test
translated_force_b = force_b - np.mean(force_b) + 0.55 ## Make an array of translated impact forces: translated_force_b
bs_replicates = draw_bs_reps(translated_force_b, np.mean, 10000) ## Take bootstrap replicates of Frog B's translated impact forces: bs_replicates

p = np.sum(bs_replicates <= np.mean(force_b)) / 10000 ## Compute fraction of replicates that are less than the observed Frog B force: p
print('p = ', p)
```
> Q. repeat <br> A. 

```python
# A two-sample bootstrap hypothesis test for difference of means
mean_force = np.mean(forces_concat) ## Compute mean of all forces: mean_force

## Generate shifted arrays
force_a_shifted = force_a - np.mean(force_a) + mean_force
force_b_shifted = force_b - np.mean(force_b) + mean_force

## Compute 10,000 bootstrap replicates from shifted arrays
bs_replicates_a = draw_bs_reps(force_a_shifted, np.mean, 10000)
bs_replicates_b = draw_bs_reps(force_b_shifted, np.mean, 10000)

bs_replicates = bs_replicates_a - bs_replicates_b ## Get replicates of difference of means: bs_replicates
p = np.sum(bs_replicates >= empirical_diff_means) / len(bs_replicates) ## Compute and print p-value: p
print('p-value =', p)
```

## 4. Hypothesis test examples
