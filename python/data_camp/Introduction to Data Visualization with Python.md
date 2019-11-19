# 1. Customizing plots
## 1.1 Plotting multiple graphs


```python
# Multiple plots on single axis
## 미리 load된 numpy array dataset. 아마 전에 봤던 여성 학위 수여 관련 data 같다. 
import matplotlib.pyplot as plt
plt.plot(year, physical_sciences, color = 'blue') ## Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(year, computer_science, color ='red') ## Plot in red the % of degrees awarded to women in Computer Science

plt.show()

# Using axes()
plt.axes([0.05, 0.05, 0.425, 0.9]) ## Create plot axes for the first line plot
plt.plot(year, physical_sciences, color='blue')

plt.axes([0.525, 0.05, 0.425, 0.9]) ## Create plot axes for the second line plot
plt.plot(year, computer_science, color='red')

## plt.axes([xlo, ylo, width, height]) :  a set of axes is created and made active with lower corner at coordinates (xlo, ylo) of the specified width and height

plt.show()

# Using subplot() (1)
plt.subplot(1, 2, 1) ## Create a figure with 1x2 subplot and make the left subplot active

plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

plt.subplot(1, 2, 2) ## Make the right subplot active in the current 1x2 subplot grid
## plt.subplot(m, n, k) to make the subplot grid of dimensions 'm' by 'n' and to make the 'k'th subplot active

plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

plt.tight_layout() ## Use plt.tight_layout() to improve the spacing between subplots
plt.show()

# Using subplot() (2)
plt.subplot(2,2,1) ## Create a figure with 2x2 subplot layout and make the top left subplot active
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

plt.subplot(2,2,2) ## Make the top right subplot active in the current 2x2 subplot grid 
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

plt.subplot(2,2,3) ## Make the bottom left subplot active in the current 2x2 subplot grid
plt.plot(year, health, color='green')
plt.title('Health Professions')

plt.subplot(2,2,4) ## Make the bottom right subplot active in the current 2x2 subplot grid
plt.plot(year, education, color='yellow')
plt.title('Education')

plt.tight_layout() ## Improve the spacing between subplots and display them
plt.show()
```

plt.subplot는 row-wise로 plot의 순서를 매긴다. 쉽게 말해 2x2 matrix를 상상하면 되는데, (1,1) = 1st, (1,2) = 2nd, (2,1) = 3nd, (2,2) 4th로 정의된다. 따라서 # Using subplot() (2)에서 보이는 것처럼 top left가 1, right가 2, bottom left가 3, right가 4로 정의되는 것이다.

## 1.2 Customizing axes

```python
# Using xlim(), ylim()
plt.plot(year,computer_science, color='red') 
plt.plot(year, physical_sciences, color='blue')

plt.xlabel('Year')
plt.ylabel('Degrees awarded to women (%)')

plt.xlim((1990, 2010)) ## Set the x-axis range
plt.ylim((0, 50)) ## Set the y-axis range
## plt.xlim((xmin, xmax))로 사용한다. 

plt.title('Degrees awarded to women (1990-2010)\nComputer Science (red)\nPhysical Sciences (blue)')
plt.show()

plt.savefig('xlim_and_ylim.png') ## Save the image as 'xlim_and_ylim.png'

# Using axis()
plt.plot(year,computer_science, color='blue')
plt.plot(year, physical_sciences,color='red')

plt.axis([1990, 2010, 0, 50]) ## Set the x-axis and y-axis limits
## plt.axis([xmin, xmax, ymin, ymax])
## .xlim, .ylim을 한 줄로 정의할 수 있다.

plt.show()

plt.savefig('axis_limits.png')
```

## 1.3 Legends, annotations, and styles
```python
# Using legend()
plt.plot(year, computer_science, color='red', label='Computer Science') ## Specify the label 'Computer Science'
plt.plot(year, physical_sciences, color='blue', label='Physical Sciences') ## Specify the label 'Physical Sciences' 

plt.legend(loc='lower center') ## Add a legend at the lower center

plt.xlabel('Year')
plt.ylabel('Enrollment (%)')
plt.title('Undergraduate enrollment of women')
plt.show()
```

plt.legend(loc)를 이용해 legend를 추가하는 개념이 아니라 .plot에서 'label'을 선언하고 이를 .legend로 call해서 위치를 잡아주는 형태인 듯하다. 

```python
# Using annotate()  
cs_max = computer_science.max() ## Compute the maximum enrollment of women in Computer Science: cs_max
yr_max = year[computer_science.argmax()] ## Calculate the year in which there was maximum enrollment of women in Computer Science: yr_max

plt.plot(year, computer_science, color='red', label='Computer Science') 
plt.plot(year, physical_sciences, color='blue', label='Physical Sciences')
plt.legend(loc='lower right') ## Plot with legend as before

plt.annotate('Maximum', xy = (yr_max, cs_max), xytext = (yr_max+5, cs_max+5), arrowprops=dict(facecolor='black')) ## Add a black arrow annotation
## plt.annotate('str', xy, xytext, arrowprops)
## 'str' : 주석에 붙을 text; xy : tuple, 주석의 대상에 해당하는 plot 상의 obs; xytext : tuple, '주석'의 입력이 시작될 자리, arrowprops : 화살표의 성질 

plt.xlabel('Year')
plt.ylabel('Enrollment (%)')
plt.title('Undergraduate enrollment of women') ## Add axis labels and title
plt.show()

# Modifying styles
import matplotlib.pyplot as plt
plt.style.use('ggplot') ## Set the style to 'ggplot'

plt.subplot(2, 2, 1) 
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

plt.subplot(2, 2, 2)
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

## Add annotation
cs_max = computer_science.max()
yr_max = year[computer_science.argmax()]
plt.annotate('Maximum', xy=(yr_max, cs_max), xytext=(yr_max-1, cs_max-10), arrowprops=dict(facecolor='black'))


plt.subplot(2, 2, 3)
plt.plot(year, health, color='green')
plt.title('Health Professions')

plt.subplot(2, 2, 4)
plt.plot(year, education, color='yellow')
plt.title('Education')

plt.tight_layout() ## Improve spacing between subplots and display them
plt.show()
```

# 2. Plotting 2D arrays
## 2.1 Working with 2D arrays

```python
# Generating meshes
import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(-2, 2, 41) 
v = np.linspace(-1, 1, 21) ## Generate two 1-D arrays: u, v

X,Y = np.meshgrid(u, v) ## Generate 2-D arrays from u and v: X, Y
## np.meshgrid() : 선언된 arg로 구성된 grid를 만듦. 좀 신기하다

Z = np.sin(3*np.sqrt(X**2 + Y**2)) ## Compute Z based on X and Y

plt.pcolor(Z)
plt.show() ## Display the resulting image with pcolor()

plt.savefig('sine_mesh.png') ## Save the figure to 'sine_mesh.png'
```

## 2.2 Visualizing bivariate functions

```python
# Contour & filled contour plots
plt.subplot(2,2,1)
plt.contour(X, Y, Z) ## Generate a default contour map of the array Z

plt.subplot(2,2,2)
plt.contour(X, Y, Z, 20) ## Generate a contour map with 20 contours

plt.subplot(2,2,3)
plt.contourf(X, Y, Z) ## Generate a default filled contour map of the array Z

plt.subplot(2,2,4)
plt.contourf(X, Y, Z, 20) ## Generate a default filled contour map with 20 contours

plt.tight_layout() ## Improve the spacing between subplots
plt.show()
```
.contour()와 contourf()는 등고선 사이를 색으로 채우지 않느냐, 채우느냐의 차이다. 선언된 X, Y를 meshgrid로 갖는 Z를 이용해 contour plot을 그린다. 

```python
# Modifying colormaps
plt.subplot(2,2,1)
plt.contourf(X,Y,Z,20, cmap='viridis') ## Create a filled contour plot with a color map of 'viridis'
plt.colorbar()
plt.title('Viridis')

plt.subplot(2,2,2)
plt.contourf(X,Y,Z,20, cmap='gray') ## Create a filled contour plot with a color map of 'gray'
plt.colorbar()
plt.title('Gray')

plt.subplot(2,2,3)
plt.contourf(X,Y,Z,20, cmap='autumn') ## Create a filled contour plot with a color map of 'autumn'
plt.colorbar()
plt.title('Autumn')

plt.subplot(2,2,4)
plt.contourf(X,Y,Z,20, cmap='winter') ## Create a filled contour plot with a color map of 'winter'
plt.colorbar()
plt.title('Winter')

plt.tight_layout()
plt.show()

```

## 2.3 Visualizing bivariate distributions

```python
# Using hist2d()
plt.hist2d(hp, mpg, bins=(20, 20), range =((40, 235),(8, 48))) ## Generate a 2-D histogram
plt.colorbar() ## Add a color bar to the histogram

plt.xlabel('Horse power [hp]')
plt.ylabel('Miles per gallon [mpg]')
plt.title('hist2d() plot')
plt.show()

# Using hexbin()
plt.hexbin(hp, mpg, gridsize = (15, 12), extent = (40, 235, 8, 48)) ## Generate a 2d histogram with hexagonal bins
plt.colorbar() ## Add a color bar to the histogram

plt.xlabel('Horse power [hp]')
plt.ylabel('Miles per gallon [mpg]')
plt.title('hexbin() plot')
plt.show()
```

## 2.4 Working with images

```python
# Loading, examining images
## 사용된 img는 https://en.wikipedia.org/wiki/File:Bruce_McCandless_II_during_EVA_in_1984.jpg이다. 
img = plt.imread('480px-Astronaut-EVA.jpg') ## Load the image into an array: img
print(img.shape) ## Print the shape of the image

plt.imshow(img) ## Display the image
plt.axis('off') ## Hide the axes
plt.show()

# Pseudocolor plot from image data
img = plt.imread('480px-Astronaut-EVA.jpg')
print(img.shape)

intensity = img.sum(axis=2) ## Compute the sum of the red, green and blue channels: intensity
print(intensity.shape) ## Print the shape of the intensity

plt.imshow(intensity, cmap = 'gray') ## Display the intensity with a colormap of 'gray'

plt.colorbar()

# Hide the axes and show the figure
plt.axis('off')
plt.show()
```
사람이 보기 편한 image와 분석을 하기 쉬운 image가 조금 다른데, #Pseudocolor plot from image data는 그 사실을 보여주기 위한 예제이다. 이 예제에서 중요한 부분은 `intensity = img.sum(axis=2)`와 `plt.imshow(intensity, cmap = 'gray')`이다. `intensity = img.sum(axis=2)`는 색의 삼원색(RGB)의 강도를 계산해주기 위한 것으로 이 과정을 거치면 '그림'으로써의 의미는 크게 떨어지지만 여전히 분석할 수 있는 형태이므로 data의 형태로 보관하기 용이해진다. 한번 더 효율성을 높인 것이 `plt.imshow(intensity, cmap = 'gray')`인데, 이 과정을 거치면 그림은 RGB의 강도(intensity)에 의한 흑백으로 변하고 사람이 식별하기에도, data로 보관하기에도 훨씬 쉬워지는 장점이 있다. 

```python
# Extent and aspect
## Extent는 x축과 y축의 길이, aspect는 그림의 너비와 높이로 계산한 비율이다. 높이/너비로 계산한다. 
img = plt.imread('480px-Astronaut-EVA.jpg')

plt.subplot(2,2,1)
plt.title('extent=(-1,1,-1,1),\naspect=0.5') 
plt.xticks([-1,0,1])
plt.yticks([-1,0,1])
plt.imshow(img, extent=(-1,1,-1,1), aspect=0.5)

plt.subplot(2,2,2)
plt.title('extent=(-1,1,-1,1),\naspect=1')
plt.xticks([-1,0,1])
plt.yticks([-1,0,1])
plt.imshow(img, extent=(-1,1,-1,1), aspect=1)

plt.subplot(2,2,3)
plt.title('extent=(-1,1,-1,1),\naspect=2')
plt.xticks([-1,0,1])
plt.yticks([-1,0,1])
plt.imshow(img, extent=(-1,1,-1,1), aspect=2)

plt.subplot(2,2,4)
plt.title('extent=(-2,2,-1,1),\naspect=2')
plt.xticks([-2,-1,0,1,2])
plt.yticks([-1,0,1])
plt.imshow(img, extent=(-2,2,-1,1), aspect=2)

plt.tight_layout()
plt.show()

# Rescaling pixel intensities
image = plt.imread('640px-Unequalized_Hawkes_Bay_NZ.jpg') ## Load the image into an array: image

pmin, pmax = image.min(), image.max() ## Extract minimum and maximum values from the image: pmin, pmax
print("The smallest & largest pixel intensities are %d & %d." % (pmin, pmax))

rescaled_image = 256*(image - pmin) / (pmax - pmin) ## Rescale the pixels: rescaled_image
print("The rescaled smallest & largest pixel intensities are %.1f & %.1f." % 
      (rescaled_image.min(), rescaled_image.max()))

plt.title('rescaled image')
plt.axis('off')
plt.imshow(rescaled_image)

plt.show()
```

# 3. Statistical plots with Seaborn
## 3.1 Visualizing regressions

```python
# Simple linear regressions
import matplotlib.pyplot as plt
import seaborn as sns

sns.lmplot(x='weight', y='hp', data=auto) ## Plot a linear regression between 'weight' and 'hp'
plt.show()

# Plotting residuals of a regression
import matplotlib.pyplot as plt
import seaborn as sns

sns.residplot(x='hp', y='mpg', data=auto, color='green') ## Generate a green residual plot of the regression between 'hp' and 'mpg'
plt.show()

# Higher-order regressions
plt.scatter(auto['weight'], auto['mpg'], label='data', color='red', marker='o') ## Generate a scatter plot of 'weight' and 'mpg' using red circles
sns.regplot(x='weight', y='mpg', data=auto, color='blue', scatter=None, label='First Order') ## Plot in blue a linear regression of order 1 between 'weight' and 'mpg'
sns.regplot(x='weight', y='mpg', data=auto, color='green', scatter = None, label='Second Order', order = 2) ## Plot in green a linear regression of order 2 between 'weight' and 'mpg'

plt.legend(loc = 'upper right') ## Add a legend and display the plot
plt.show()

# Grouping linear regressions by hue
sns.lmplot(x='weight', y='hp',data = auto, hue='origin', palette='Set1') ## Plot a linear regression between 'weight' and 'hp', with a hue of 'origin' and palette of 'Set1'

plt.show()

# Grouping linear regressions by row or column
sns.lmplot(x='weight', y='hp',data = auto, row='origin', palette='Set1') ## Plot linear regressions between 'weight' and 'hp' grouped row-wise by 'origin'
## col-wise하게 잡고 싶다면 col=str로 arg를 잡아주면 된다. 

plt.show()
```

## 3.2 Visualizing univariate distributions

```python
# Constructing strip plots
plt.subplot(2,1,1)
sns.stripplot(x='cyl', y='hp', data=auto) ## Make a strip plot of 'hp' grouped by 'cyl'

plt.subplot(2,1,2)
sns.stripplot(x='cyl', y='hp', data=auto, jitter = True, size = 3) ## Make the strip plot again using jitter and a smaller point size

plt.show()

# Constructing swarm plots
plt.subplot(2,1,1)
sns.swarmplot(x='cyl', y='hp', data=auto) ## Generate a swarm plot of 'hp' grouped horizontally by 'cyl'  

plt.subplot(2,1,2)
sns.swarmplot(x='hp', y='cyl', data=auto, hue='origin', orient = 'h') ## Generate a swarm plot of 'hp' grouped vertically by 'cyl' with a hue of 'origin'
## default 상태에서는 세로로 길게 그려지는데 orient = 'h'(horizontal)를 이용하면 가로로 길게 늘어진다. 

plt.show()

# Constructing violin plots
plt.subplot(2,1,1)
sns.violinplot(x='cyl', y='hp', data=auto) ## Generate a violin plot of 'hp' grouped horizontally by 'cyl'

plt.subplot(2,1,2)
sns.violinplot(x='cyl', y='hp', data=auto, color = 'lightgray', inner=None) ## Generate the same violin plot again with a color of 'lightgray' and without inner annotations
sns.stripplot(x='cyl', y='hp', data=auto, size= 1.5, jitter = True) ## Overlay a strip plot on the violin plot
## 빈 violinplot에 stripplot을 추가한 형태다. 

# Display the plot
plt.show()
```

## 3.3 Visualizing multivariate distributions

```python
# Plotting joint distributions (1)
sns.jointplot(x='hp', y='mpg', data=auto) ## Generate a joint plot of 'hp' and 'mpg'
## scatter와 histogram이 같이 나온다. 신기하네.

plt.show()

# Plotting joint distributions (2)
sns.jointplot(kind='hex', x='hp',y='mpg',data=auto) ## Generate a joint plot of 'hp' and 'mpg' using a hexbin plot

plt.show()

# Plotting distributions pairwise (1)
print(auto.head()) ## Print the first 5 rows of the DataFrame
sns.pairplot(auto) ## Plot the pairwise joint distributions from the DataFrame 

plt.show()

# Plotting distributions pairwise (2)
print(auto.head()) ## Print the first 5 rows of the DataFrame
sns.pairplot(kind='reg', data=auto, hue='origin') ## Plot the pairwise joint distributions grouped by 'origin' along with regression lines

plt.show()

# Visualizing correlations with a heatmap
print(cov_matrix) ## Print the covariance matrix
sns.heatmap(cov_matrix) ## Visualize the covariance matrix using a heatmap

plt.show()
```

# 4. Analyzing time series and images
## 4.1 Visualizing time series

```python
# Multiple time series on common axes
import matplotlib.pyplot as plt

plt.plot(aapl, color='blue', label='AAPL')
plt.plot(ibm, color='green', label='IBM')
plt.plot(csco, color='red', label='CSCO')
plt.plot(msft, color='magenta', label='MSFT')

plt.legend(loc='upper left') ## Add a legend in the top left corner of the plot
plt.xticks(rotation = 60) ## Specify the orientation of the xticks

plt.show()

# Multiple time series slices (1)
plt.subplot(2,1,1)
plt.xticks(rotation=45)
plt.title('AAPL: 2001 to 2011')
plt.plot(aapl, color='blue') ## Plot the series in the top subplot in blue

view = aapl['2007':'2008'] ## Slice aapl from '2007' to '2008' inclusive: view

plt.subplot(2,1,2)
plt.xticks(rotation=45)
plt.title('AAPL: 2007 to 2008')
plt.plot(view, color='black') ## Plot the sliced data in the bottom subplot in black
plt.tight_layout()
plt.show()

# Multiple time series slices (2)
view_1 = aapl['2007-11':'2008-04'] ## Slice aapl from Nov. 2007 to Apr. 2008 inclusive: view

plt.subplot(2,1,1)
plt.plot(view_1, color='red')
plt.xticks(rotation = 45)
plt.title('AAPL: Nov. 2007 to Apr. 2008') ## Plot the sliced series in the top subplot in red

view_2 = aapl['2008-01'] ## Reassign the series by slicing the month January 2008

plt.subplot(2,1,2)
plt.plot(view_2, color='green')
plt.xticks(rotation = 45)
plt.title('AAPL: Jan. 2008') ## Plot the sliced series in the bottom subplot in green

plt.tight_layout()
plt.show()

# Plotting an inset view
view = aapl['2007-11':'2008-04'] ## Slice aapl from Nov. 2007 to Apr. 2008 inclusive: view

plt.plot(aapl)
plt.xticks(rotation=45)
plt.title('AAPL: 2001-2011') ## Plot the entire series 

plt.axes([0.25, 0.5, 0.35, 0.35]) ## Specify the axes

plt.plot(view, color = 'red')
plt.xticks(rotation=45)
plt.title('2007/11-2008/04') ## Plot the sliced series in red using the current axes
plt.show()
```

## 4.2 Time series with moving windows

```python
# Plotting moving averages
plt.subplot(2,2,1)
plt.plot(mean_30, color='green')
plt.plot(aapl, 'k-.')
plt.xticks(rotation=60)
plt.title('30d averages') ## Plot the 30-day moving average in the top left subplot in green

plt.subplot(2,2,2)
plt.plot(mean_75, 'red')
plt.plot(aapl, 'k-.')
plt.xticks(rotation=60)
plt.title('75d averages') ## Plot the 75-day moving average in the top right subplot in red

plt.subplot(2, 2, 3)
plt.plot(mean_125, color='magenta')
plt.plot(aapl, 'k-.')
plt.xticks(rotation=60)
plt.title('125d averages') ## Plot the 125-day moving average in the bottom left subplot in magenta

plt.subplot(2, 2, 4)
plt.plot(mean_250, color='cyan')
plt.plot(aapl, 'k-.')
plt.xticks(rotation=60)
plt.title('250d averages') ## Plot the 250-day moving average in the bottom right subplot in cyan

plt.show()

# Plotting moving std
plt.plot(std_30, color='red', label='30d') ## Plot std_30 in red
plt.plot(std_75, color='cyan', label='75d') ## Plot std_75 in cyan
plt.plot(std_125, color='green', label='125d') ## Plot std_125 in green
plt.plot(std_250, color='magenta', label='250d') ## Plot std_250 in magenta

plt.legend(loc='upper left') ## Add a legend to the upper left
plt.title('Moving standard deviations')
plt.show()
```

## 4.3 Histogram equalization in images

```python
# Extracting a histogram from a grayscale image
## https://commons.wikimedia.org/wiki/File:Unequalized_Hawkes_Bay_NZ.jpg
image = plt.imread('640px-Unequalized_Hawkes_Bay_NZ.jpg') ## Load the image into an array: image

plt.subplot(2,1,1)
plt.title('Original image')
plt.axis('off')
plt.imshow(image, cmap = 'gray') ## Display image in top subplot using color map 'gray'

pixels = image.flatten() ## Flatten the image into 1 dimension: pixels

plt.subplot(2,1,2)
plt.xlim((0,255))
plt.title('Normalized histogram')
plt.hist(pixels, bins=64, range=(0,256), normed=True, color='red', alpha=0.4) ## Display a histogram of the pixels in the bottom subplot

plt.show()

# Cumulative Distribution Function from an image histogram
image = plt.imread('640px-Unequalized_Hawkes_Bay_NZ.jpg')

plt.subplot(2,1,1)
plt.imshow(image, cmap='gray')
plt.title('Original image')
plt.axis('off') ## Display image in top subplot using color map 'gray'

pixels = image.flatten() ## Flatten the image into 1 dimension: pixels

plt.subplot(2,1,2) 
pdf = plt.hist(pixels, bins=64, range=(0,256), normed=False,
               color='red', alpha=0.4)
plt.grid('off') ## Display a histogram of the pixels in the bottom subplot

plt.twinx() ## Use plt.twinx() to overlay the CDF in the bottom subplot

cdf = plt.hist(pixels, bins=64, range=(0,256),
               normed=True, cumulative=True,
               color='blue', alpha=0.4) ## Display a cumulative histogram of the pixels
               
plt.xlim((0,256))
plt.grid('off')
plt.title('PDF & CDF (original image)')
plt.show() ## Specify x-axis range, hide axes, add title and display plot

# Equalizing an image histogram
image = plt.imread('640px-Unequalized_Hawkes_Bay_NZ.jpg')

pixels = image.flatten() ## Flatten the image into 1 dimension: pixels

cdf, bins, patches = plt.hist(pixels, bins=256, range=(0,256), normed=True, cumulative=True) ## Generate a cumulative histogram
new_pixels = np.interp(pixels, bins[:-1], cdf*255)

new_image = new_pixels.reshape(image.shape) ## Reshape new_pixels as a 2-D array: new_image

plt.subplot(2,1,1)
plt.title('Equalized image')
plt.axis('off')
plt.imshow(new_image, cmap='gray') ## Display the new image with 'gray' color map

plt.subplot(2,1,2)
pdf = plt.hist(new_pixels, bins=64, range=(0,256), normed=False,
               color='red', alpha=0.4)
plt.grid('off') ## Generate a histogram of the new pixels

plt.twinx() ## Use plt.twinx() to overlay the CDF in the bottom subplot
plt.xlim((0,256))
plt.grid('off')

plt.title('PDF & CDF (equalized image)')

cdf = plt.hist(new_pixels, bins=64, range=(0,256),
               cumulative=True, normed=True,
               color='blue', alpha=0.4) ## Generate a cumulative histogram of the new pixels
plt.show()

# Extracting histograms from a color image
## https://imgsrc.hubblesite.org/hu/db/images/hs-2004-32-b-small_web.jpg
image = plt.imread('hs-2004-32-b-small_web.jpg')

plt.subplot(2,1,1)
plt.title('Original image')
plt.axis('off')
plt.imshow(image) ## Display image in top subplot

red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2] ## Extract 2-D arrays of the RGB channels: red, green, blue

red_pixels = red.flatten()
green_pixels = green.flatten()
blue_pixels = blue.flatten() ## Flatten the 2-D arrays of the RGB channels into 1-D

## Overlay histograms of the pixels of each color in the bottom subplot
plt.subplot(2,1,2)
plt.title('Histograms from color image')
plt.xlim((0,256))
plt.hist(red_pixels, bins=64, normed=True, color='red', alpha=0.2)
plt.hist(green_pixels, bins=64, normed=True, color='green', alpha=0.2)
plt.hist(blue_pixels, bins=64, normed=True, color='blue', alpha=0.2)

plt.show()

# Extracting bivariate histograms from a color image
# https://campus.datacamp.com/courses/introduction-to-data-visualization-with-python/analyzing-time-series-and-images?ex=15
image = plt.imread('hs-2004-32-b-small_web.jpg') 

## Extract RGB channels and flatten into 1-D array
red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
red_pixels = red.flatten()
green_pixels = green.flatten()
blue_pixels = blue.flatten()

plt.subplot(2,2,1)
plt.grid('off') 
plt.xticks(rotation=60)
plt.xlabel('red')
plt.ylabel('green')
plt.hist2d(red_pixels, green_pixels, bins=(32,32)) ## Generate a 2-D histogram of the red and green pixels

plt.subplot(2,2,2)
plt.grid('off')
plt.xticks(rotation=60)
plt.xlabel('green')
plt.ylabel('blue')
plt.hist2d(green_pixels, blue_pixels, bins=(32,32)) ## Generate a 2-D histogram of the green and blue pixels

plt.subplot(2,2,3)
plt.grid('off')
plt.xticks(rotation=60)
plt.xlabel('blue')
plt.ylabel('red')
plt.hist2d(blue_pixels, red_pixels, bins=(32,32)) ## Generate a 2-D histogram of the blue and red pixels

plt.show()
```
