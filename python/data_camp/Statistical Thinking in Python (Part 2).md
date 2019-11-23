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

    ## Initialize array of replicates: 
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

# 4. Hypothesis test examples
## 4.1 A/B testing

```python
# The vote for the Civil Rights Act in 1964
## Construct arrays of data: dems, reps
dems = np.array([True] * 153 + [False] * 91)
reps = np.array([True] * 136  + [False] * 35)

def frac_yea_dems(dems, reps):
    """Compute fraction of Democrat yea votes."""
    frac = np.sum(dems) / len(dems)
    return frac
    
perm_replicates = draw_perm_reps(dems, reps, frac_yea_dems, 10000) ## Acquire permutation samples: perm_replicates

## Compute and print p-value: p
p = np.sum(perm_replicates <= 153/244) / len(perm_replicates)
print('p-value =', p)
```
```python
# A time-on-website analog
nht_diff_obs = diff_of_means(nht_dead, nht_live) ## Compute the observed difference in mean inter-no-hitter times: nht_diff_obs
perm_replicates = draw_perm_reps(nht_dead, nht_live, diff_of_means, 10000) ## Acquire 10,000 permutation replicates of difference in mean no-hitter time: perm_replicates

p = np.sum(perm_replicates <= nht_diff_obs) / len(perm_replicates) ## Compute and print the p-value: p
print('p-val =', p)
```
## 4.2 Test of correlation

```python
# Hypothesis test on Pearson correlation
r_obs = pearson_r(illiteracy, fertility) ## Compute observed correlation: r_obs

perm_replicates = np.empty(10000) ## Initialize permutation replicates: perm_replicates

## Draw replicates
for i in range(10000):
    ## Permute illiteracy measurments: illiteracy_permuted
    illiteracy_permuted = np.random.permutation(illiteracy)

    ## Compute Pearson correlation
    perm_replicates[i] = pearson_r(illiteracy_permuted, fertility)

p = np.sum(perm_replicates >= r_obs) / len(perm_replicates) ## Compute p-value: p
print('p-val =', p)
```

```python
# Do neonicotinoid insecticides have unintended consequences?
## Compute x,y values for ECDFs
x_control, y_control = ecdf(control)
x_treated, y_treated = ecdf(treated)

## Plot the ECDFs
plt.plot(x_control, y_control, marker='.', linestyle='none')
plt.plot(x_treated, y_treated, marker='.', linestyle='none')

plt.margins(0.02)
plt.legend(('control', 'treated'), loc='lower right')
plt.xlabel('millions of alive sperm per mL')
plt.ylabel('ECDF')
plt.show()
```

```python
# Bootstrap hypothesis test on bee sperm counts
diff_means = diff_of_means(control, treated) ## Compute the difference in mean sperm count: diff_means

mean_count = np.concatenate([control, treated]).mean() ## Compute mean of pooled data: mean_count

## Generate shifted data sets
control_shifted = control - np.mean(control) + mean_count
treated_shifted = treated - np.mean(treated) + mean_count

## Generate bootstrap replicates
bs_reps_control = draw_bs_reps(control_shifted,
                       np.mean, size=10000)
bs_reps_treated = draw_bs_reps(treated_shifted,
                       np.mean, size=10000)

bs_replicates = bs_reps_control-bs_reps_treated ## Get replicates of difference of means: bs_replicates

## Compute and print p-value: p
p = np.sum(bs_replicates >= np.mean(control) - np.mean(treated)) \
            / len(bs_replicates)
print('p-value =', p)

```

# 5. Putting it all together

```python
# EDA of beak depths of Darwin's finches
_ = sns.swarmplot(x='year', y='beak_depth', data=df) ## Create bee swarm plot

_ = plt.xlabel('year')
_ = plt.ylabel('beak depth (mm)')
plt.show()
```

```python
# ECDFs of beak depths
## Compute ECDFs
x_1975, y_1975 = ecdf(bd_1975)
x_2012, y_2012 = ecdf(bd_2012)

## Plot the ECDFs
_ = plt.plot(x_1975, y_1975, marker='.', linestyle='none')
_ = plt.plot(x_2012, y_2012, marker='.', linestyle='none')

plt.margins(0.02)
_ = plt.xlabel('beak depth (mm)')
_ = plt.ylabel('ECDF')
_ = plt.legend(('1975', '2012'), loc='lower right')
plt.show()
```

```python
# Parameter estimates of beak depths
mean_diff = np.mean(bd_2012)-np.mean(bd_1975) ## Compute the difference of the sample means: mean_diff

## Get bootstrap replicates of means
bs_replicates_1975 = draw_bs_reps(bd_1975, np.mean, 10000)
bs_replicates_2012 = draw_bs_reps(bd_2012, np.mean, 10000)

bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975 ## Compute samples of difference of means: bs_diff_replicates

conf_int = np.percentile(bs_diff_replicates, [2.5, 97.5]) ## Compute 95% confidence interval: conf_int

print('difference of means =', mean_diff, 'mm')
print('95% confidence interval =', conf_int, 'mm')
```

```python
# Hypothesis test: Are beaks deeper in 2012?
combined_mean = np.mean(np.concatenate((bd_1975, bd_2012))) ## Compute mean of combined data set: combined_mean

## Shift the samples
bd_1975_shifted = bd_1975 - np.mean(bd_1975)+ combined_mean
bd_2012_shifted = bd_2012 - np.mean(bd_2012)+ combined_mean

## Get bootstrap replicates of shifted data sets
bs_replicates_1975 = draw_bs_reps(bd_1975_shifted, np.mean, 10000)
bs_replicates_2012 = draw_bs_reps(bd_2012_shifted, np.mean, 10000)

bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975 ## Compute replicates of difference of means: bs_diff_replicates

p = np.sum(bs_diff_replicates >= mean_diff) / len(bs_diff_replicates)

# Print p-value
print('p =', p)
```

```python
# EDA of beak length and depth
## Make scatter plot of 1975 data
_ = plt.plot(bl_1975, bd_1975, marker='.',
             linestyle='None', color='blue', alpha=0.5)

## Make scatter plot of 2012 data
_ = plt.plot(bl_2012, bd_2012, marker='.',
             linestyle='None', color='red', alpha=0.5)

_ = plt.xlabel('beak length (mm)')
_ = plt.ylabel('beak depth (mm)')
_ = plt.legend(('1975', '2012'), loc='upper left')
plt.show()
```

```python
# Linear regressions
## Compute the linear regressions
slope_1975, intercept_1975 = np.polyfit(bl_1975, bd_1975, deg=1)
slope_2012, intercept_2012 = np.polyfit(bl_2012, bd_2012, deg=1)

## Perform pairs bootstrap for the linear regressions
bs_slope_reps_1975, bs_intercept_reps_1975 = \
        draw_bs_pairs_linreg(bl_1975, bd_1975, 1000)
bs_slope_reps_2012, bs_intercept_reps_2012 = \
        draw_bs_pairs_linreg(bl_2012, bd_2012, 1000)

## Compute confidence intervals of slopes
slope_conf_int_1975 = np.percentile(bs_slope_reps_1975, [2.5, 97.5])
slope_conf_int_2012 = np.percentile(bs_slope_reps_2012, [2.5, 97.5])
intercept_conf_int_1975 = np.percentile(bs_intercept_reps_1975, [2.5, 97.5])
intercept_conf_int_2012 = np.percentile(bs_intercept_reps_2012, [2.5, 97.5])


print('1975: slope =', slope_1975,
      'conf int =', slope_conf_int_1975)
print('1975: intercept =', intercept_1975,
      'conf int =', intercept_conf_int_1975)
print('2012: slope =', slope_2012,
      'conf int =', slope_conf_int_2012)
print('2012: intercept =', intercept_2012,
      'conf int =', intercept_conf_int_2012)
```

```python
# Displaying the linear regression results
## Make scatter plot of 1975 data
_ = plt.plot(bl_1975, bd_1975, marker='.',
             linestyle='none', color='blue', alpha=0.5)

## Make scatter plot of 2012 data
_ = plt.plot(bl_2012, bd_2012, marker='.',
             linestyle='none', color='red', alpha=0.5)

_ = plt.xlabel('beak length (mm)')
_ = plt.ylabel('beak depth (mm)')
_ = plt.legend(('1975', '2012'), loc='upper left')

## Generate x-values for bootstrap lines: x
x = np.array([10, 17])

## Plot the bootstrap lines
for i in range(100):
    plt.plot(x, bs_slope_reps_1975[i]*x+bs_intercept_reps_1975[i],
             linewidth=0.5, alpha=0.2, color='blue')
    plt.plot(x, bs_slope_reps_2012[i]*x+bs_intercept_reps_2012[i],
             linewidth=0.5, alpha=0.2, color='red')
plt.show()
```

```python
# Beak length to depth ratio
## Compute length-to-depth ratios
ratio_1975 = bl_1975/bd_1975
ratio_2012 = bl_2012/bd_2012

## Compute means
mean_ratio_1975 = np.mean(ratio_1975)
mean_ratio_2012 = np.mean(ratio_2012)

## Generate bootstrap replicates of the means
bs_replicates_1975 = draw_bs_reps(ratio_1975, np.mean, 10000)
bs_replicates_2012 = draw_bs_reps(ratio_2012, np.mean, 10000)

## Compute the 99% confidence intervals
conf_int_1975 = np.percentile(bs_replicates_1975, [0.5, 99.5])
conf_int_2012 = np.percentile(bs_replicates_2012, [0.5, 99.5])

print('1975: mean ratio =', mean_ratio_1975,
      'conf int =', conf_int_1975)
print('2012: mean ratio =', mean_ratio_2012,
      'conf int =', conf_int_2012)
```

```python
# Calculation of heritability
## Make scatter plots
_ = plt.plot(bd_parent_fortis, bd_offspring_fortis,
             marker='.', linestyle='none', color='blue', alpha=0.5)
_ = plt.plot(bd_parent_scandens, bd_offspring_scandens,
             marker='.', linestyle='none', color='red', alpha=0.5)

_ = plt.xlabel('parental beak depth (mm)')
_ = plt.ylabel('offspring beak depth (mm)')
_ = plt.legend(('G. fortis', 'G. scandens'), loc='lower right')
plt.show()

```

```python
# Correlation of offspring and parental data
def draw_bs_pairs(x, y, func, size=1):
    """Perform pairs bootstrap for a single statistic."""

    ## Set up array of indices to sample from: inds
    inds = np.arange(len(x))

    ## Initialize replicates: bs_replicates
    bs_replicates = np.empty(size)

    ## Generate replicates
    for i in range(size):
        bs_inds = np.random.choice(inds, size=len(inds))
        bs_x, bs_y = x[bs_inds], y[bs_inds]
        bs_replicates[i] = func(bs_x, bs_y)

    return bs_replicates
```

```python
# Pearson correlation of offspring and parental data
## Compute the Pearson correlation coefficients
r_scandens = pearson_r(bd_parent_scandens, bd_offspring_scandens)
r_fortis = pearson_r(bd_parent_fortis, bd_offspring_fortis)

## Acquire 1000 bootstrap replicates of Pearson r
bs_replicates_scandens = draw_bs_pairs(bd_parent_scandens, bd_offspring_scandens, pearson_r, 1000)
bs_replicates_fortis = draw_bs_pairs(bd_parent_fortis, bd_offspring_fortis, pearson_r, 1000)


## Compute 95% confidence intervals
conf_int_scandens = np.percentile(bs_replicates_scandens, [2.5, 97.5])
conf_int_fortis = np.percentile(bs_replicates_fortis, [2.5, 97.5])

print('G. scandens:', r_scandens, conf_int_scandens)
print('G. fortis:', r_fortis, conf_int_fortis)
```

```python
# Measuring heritability
def heritability(parents, offspring):
    """Compute the heritability from parent and offspring samples."""
    covariance_matrix = np.cov(parents, offspring)
    return covariance_matrix[0,1] / covariance_matrix[0,0]

## Compute the heritability
heritability_scandens = heritability(bd_parent_scandens, bd_offspring_scandens)
heritability_fortis = heritability(bd_parent_fortis, bd_offspring_fortis)

## Acquire 1000 bootstrap replicates of heritability
replicates_scandens = draw_bs_pairs(
        bd_parent_scandens, bd_offspring_scandens, heritability, size=1000)       
replicates_fortis = draw_bs_pairs(
        bd_parent_fortis, bd_offspring_fortis, heritability, size=1000)
        
## Compute 95% confidence intervals
conf_int_scandens = np.percentile(replicates_scandens, [2.5, 97.5])
conf_int_fortis = np.percentile(replicates_fortis, [2.5, 97.5])

print('G. scandens:', heritability_scandens, conf_int_scandens)
print('G. fortis:', heritability_fortis, conf_int_fortis)
```

```python
# Is beak depth heritable at all in G. scandens?
perm_replicates = np.empty(10000) ## Initialize array of replicates: perm_replicates

## Draw replicates
for i in range(10000):
    # Permute parent beak depths
    bd_parent_permuted = np.random.permutation(bd_parent_scandens)
    perm_replicates[i] = heritability(bd_parent_permuted, bd_offspring_scandens)


p = np.sum(perm_replicates >= heritability_scandens) / len(perm_replicates) ## Compute p-value: p
print('p-val =', p)

```
