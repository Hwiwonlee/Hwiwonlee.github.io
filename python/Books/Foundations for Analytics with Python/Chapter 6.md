```python
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
mu1, mu2, sigma = 100, 130, 15
x1 = mu1 + sigma * np.random.randn(10000)
x2 = mu2 + sigma * np.random.randn(10000)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
n, bins, patches = ax1.hist(x1, bins = 50, normed = False, color = 'darkgreen')
n, bins, patches = ax1.hist(x2, bins = 50, normed = False, color = 'orange', alpha = 0.5)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
plt.xlabel('Bins')
plt.ylabel('Number of Values in Bin')
fig.suptitle('Histograms', fontsize = 14, fontweight = 'bold')
ax1.set_title('Two Frequency Distributions')
plt.savefig('histogram.png', dpi = 400, bbox_inches = 'tight')
plt.show()
```

```python
from numpy.random import randn
import matplotlib.pyplot as plt
plt.style.use('ggplot')

plot_data1 = randn(50).cumsum()
plot_data2 = randn(50).cumsum()
plot_data3 = randn(50).cumsum()
plot_data4 = randn(50).cumsum()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(plot_data1, marker = r'o', color = u'blue', linestyle = '-', label = 'Blue Solid')
ax1.plot(plot_data2, marker = r'+', color = u'red', linestyle = '--', label = 'Red Dashed')
ax1.plot(plot_data3, marker = r'*', color = u'green', linestyle = '-.', label = 'Green Dash Dot')
ax1.plot(plot_data4, marker = r's', color = u'orange', linestyle = ':', label = 'Orange Dotted')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Line Plots : Markers, Colors, and Linestyles')
plt.xlabel('Draw')
plt.ylabel('Random Number')
plt.legend(loc='best')
plt.savefig('Line_plot.png', dpi = 400, bbox_inches = 'tight')
plt.show()
```
```python
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
x = np.arange(start = 1., stop = 15., step = 1.)
y_linear = x + 5. * np.random.randn(14)
y_quadratic = x**2 + 10. * np.random.randn(14)
fn_linear = np.poly1d(np.polyfit(x, y_linear, deg = 1))
fn_quadratic = np.poly1d(np.polyfit(x, y_quadratic, deg = 2))
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(x, y_linear, 'bo', x, y_quadratic, 'go', x, fn_linear(x), 'b-', x, fn_quadratic(x), 'g-', linewidth = 2)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Scatter Plots with Best Fit Lines')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.xlim((min(x)-1, max(x)+1))
plt.ylim((min(y_quadratic)-10, max(y_quadratic)+10))
plt.savefig('scatter_plot.png', dpi = 400, bbox_inches = 'tight')
plt.show()
```
```python
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

N = 500
normal = np.random.normal(loc = 0, scale = 1, size = N)
lognormal = np.random.lognormal(mean = 0, sigma = 1, size = N)
index_value = np.random.random_integers(low = 0, high = N-1, size = N)
normal_sample = normal[index_value]
lognormal_sample = lognormal[index_value]
box_plot_data = [normal, normal_sample, lognormal, lognormal_sample]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
box_labels = ['normal', 'normal_sample', 'lognormal', 'lognormal_sample']

ax1.boxplot(box_plot_data, notch = False, sym = '.', vert = True, whis = 1.5, showmeans = True, labels = box_labels)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Box Plots : Resampling of Two Ditsributions')
ax1.set_xlabel('Ditsribution')
ax1.set_ylabel('Value')
plt.savefig('box_plot.png', dpi = 400, bbox_inches = 'tight')
plt.show()
```

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig, axes = plt.subplots(nrows=1, ncols =2)
ax1, ax2 = axes.ravel()
data_frame = pd.DataFrame(np.random.rand(5,3), 
              index = ['Customer 1', 'Customer 2', 'Customer 3', 'Customer 4', 'Customer 5'],
              columns = pd.Index(['Metric 1','Metric 2', 'Metric 3'], name = 'Metrics'))

data_frame.plot(kind = 'bar', ax = ax1, alpha = 0.75, title = 'Bar plot')
plt.setp(ax1.get_xticklabels(), rotation = 45, fontsize = 10)
plt.setp(ax1.get_yticklabels(), rotation = 0, fontsize = 10)
ax1.set_xlabel('Customer')
ax1.set_ylabel('Value')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

colors = dict(boxes = 'DarkBlue', whiskers = 'Gray', medians = 'Red', caps = 'Black')
data_frame.plot(kind = 'box', color = colors, sym = 'r', ax = ax2, title = 'Box Plot')
plt.setp(ax2.get_xticklabels(), rotation = 45, fontsize = 10)
plt.setp(ax2.get_yticklabels(), rotation = 0, fontsize = 10)
ax2.set_xlabel('Metric')
ax2.set_ylabel('Value')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

plt.savefig('pandas_plots.png', dpi = 400, bbox_inches = 'tight')
```

```python
import plotnine as p9
from pydataset import data
mtcars = data('mtcars')
print(mtcars.head())

plt1 = p9.ggplot(aes(x = 'mpg'), data = mtcars) + geom_histogram(fill = 'darkblue', binwidth = 2) + xlim(10, 35) + ylim(0, 10) + xlab('MPG') + ylab('Frequency') + ggtitle("Histogram of MPG")
print(plt1)

survival = data('survival')
print(survival.head())
plt2 = p9.ggplot(aes(x = 'dose', y = 'surv'), data = survival) \
        +geom_line(color = 'purple', size = 1.5, alpha = 0.75) \
        +xlab('Dose') + ylab('Survival') + ggtitle('Survival of Rats after Radiation Doses')
print(plt2)

diamonds = data('diamonds')
print(diamonds.head())
print(diamonds.values)
diamonds.dtypes

plt3 = p9.ggplot(aes(x = 'carat', y = 'price', colour = 'cut'), data = diamonds) \
        + geom_point(alpha = 0.5) \
        + xlim(0, 6) + ylim(0, 20000) + xlab("Carat") + ylab("Price") + ggtitle('Diamond Price by Carat adn Cut') + theme_gray()
print(plt3)
```
### plotnine과 ggplot
**문제 1** dataset을 불러오기 위한 from ggplot import * 가 안됨
**[해결 1](https://stackoverflow.com/questions/28417293/sample-datasets-in-pandas)** 차선책으로 pydataset 모듈을 이용해 data를 가져옴. 그러나 mtcars와 diamonds만 존재. meat data는 가져올 수 없었음. R에서 직접 가져오는 방법도 있긴 하지만 일단 pass

**문제 2** diamonds data를 이용한 plot이 print가 안됨. Error: Discrete value supplied to continuous scale
**해결 2** 아직 진행 중. (11.09). scale_color_gradient(low = '#05D9F6', high = '#5011D1')이 문제였음. 일단 빼보니까 문제없이 돌아감.  
p9.scales.scale_color_gradient()의 [help](https://plotnine.readthedocs.io/en/stable/generated/plotnine.scales.scale_color_gradient.html#plotnine.scales.scale_color_gradient) 를 봐도 문제가 없어보이는데 이유를 아직 모르겠음. 



```python
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sns.set(color_codes = True)

x = np.random.normal(size = 1000)
sns.distplot(x , bins = 20, kde = False, rug = True, label = "Histogram w/o Destiny")
sns.utils.axlabel("Value", "Frequency")
plt.title("Histogram of Random Sample of Normal Distribution")
plt.legend()
plt.show()

mean, cov = [5, 10], [(1, 0.5), (0.5, 1)]
data = np.random.multivariate_normal(mean, cov, 200)
data_frame = pd.DataFrame(data, columns = ["x", "y"])
sns.jointplot(x="x", y="y", data = data_frame, kind = "reg").set_axis_labels("x", "y")
plt.suptitle("Joint Plot of Two Variables with Bivariate and Univariate Graphs")
plt.show()

iris = sns.load_dataset("iris")
sns.pairplot(iris)
plt.show()

tips = sns.load_dataset("tips")

sns.factorplot(x = "time", y = "total_bill", hue = "smoker", col = "day", data = tips, kind = "box", size = 4, aspect = 0.5)
plt.show()
```
