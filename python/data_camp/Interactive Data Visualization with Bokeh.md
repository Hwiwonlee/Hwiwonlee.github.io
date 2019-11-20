# 1. Basic plotting with Bokeh
## 1.1 Plotting with glyphs

```python
# A simple scatter plot
from bokeh.plotting import figure ## Import figure from bokeh.plotting
from bokeh.io import show, output_file ## Import output_file and show from bokeh.io

p = figure(x_axis_label='fertility (children per woman)', y_axis_label='female_literacy (% population)') ## Create the figure: p
p.circle(fertility, female_literacy) ## Add a circle glyph to the figure p

output_file('fert_lit.html') ## Call the output_file() function and specify the name of the file
show(p) ## Display the plot

```

```python
# A scatter plot with different shapes
p = figure(x_axis_label='fertility (children per woman)', y_axis_label='female_literacy (% population)') ## Create the figure: p

p.circle(fertility_latinamerica, female_literacy_latinamerica) ## Add a circle glyph to the figure p
p.x(fertility_africa, female_literacy_africa) ## Add an x glyph to the figure p

output_file('fert_lit_separate.html') ## Specify the name of the file
show(p) ## Display the plot

```

```python
# Customizing your scatter plots
p = figure(x_axis_label='fertility (children per woman)', y_axis_label='female_literacy (% population)') ## Create the figure: p

p.circle(fertility_latinamerica, female_literacy_latinamerica, color='blue', size=10, alpha=0.8) ## Add a blue circle glyph to the figure p
p.circle(fertility_africa, female_literacy_africa, color='red', size=10, alpha=0.8) ## Add a red circle glyph to the figure p

output_file('fert_lit_separate_colors.html') ## Specify the name of the file
show(p) ## Display the plot

```

## 1.2 Additional glyphs

```python
# Lines
from bokeh.plotting import figure ## Import figure from bokeh.plotting

p = figure(x_axis_type = 'datetime', x_axis_label='Date', y_axis_label='US Dollars') ## Create a figure with x_axis_type="datetime": p

p.line(date, price) ## Plot date along the x axis and price along the y axis
output_file('line.html') ## Specify the name of the output file and show the result
show(p)
```

```python
# Lines and markers
from bokeh.plotting import figure ## Import figure from bokeh.plotting

p = figure(x_axis_type='datetime', x_axis_label='Date', y_axis_label='US Dollars') ## Create a figure with x_axis_type='datetime': p

p.line(date, price) ## Plot date along the x-axis and price along the y-axis
p.circle(date, price, fill_color='white', size=4) ## With date on the x-axis and price on the y-axis, add a white circle glyph of size 4

output_file('line.html') ## Specify the name of the output file and show the result
show(p)
```

```python
# Patches
x = [az_lons, co_lons, nm_lons, ut_lons] ## Create a list of az_lons, co_lons, nm_lons and ut_lons: x
y = [az_lats, co_lats, nm_lats, ut_lats] ## Create a list of az_lats, co_lats, nm_lats and ut_lats: y

p.patches(x, y, line_color = 'white') ## Add patches to figure p with line_color=white for x and y

output_file('four_corners.html') ## Specify the name of the output file and show the result
show(p)
```
.patches()가 좀 특이한 것 같다. list로 선언된 x,y를 이어서 'patch'로 만들어버리는 듯. 

## 1.3 Data formats
```python
# Plotting data from NumPy arrays
import numpy as np

x = np.linspace(0, 5, 100) ## Create array using np.linspace: x
y = np.cos(x) ## Create array using np.cos: y

p.circle(x, y) ## Add circles at x and y

output_file('numpy.html')
show(p)
```

```python
# Plotting data from Pandas DataFrames
import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv('auto.csv') ## Read in the CSV file: df

p = figure(x_axis_label='HP', y_axis_label='MPG') ## Create the figure: p
p.circle(df.hp, df.mpg, color = df['color'], size = 10) ## Plot mpg vs hp by color

output_file('auto-df.html')
show(p)
```

```python
# The Bokeh ColumnDataSource (continued)
from bokeh.plotting import ColumnDataSource ## Import the ColumnDataSource class from bokeh.plotting

source = ColumnDataSource(df) ## Create a ColumnDataSource from df: source
source.data

p.circle(x='Year', y='Time', size = 8, color = 'color', source=source) ## Add circle glyphs to the figure p
output_file('sprint.html')
show(p)

```

## 1.4 Customizing glyphs

```python
# Selection and non-selection glyphs
p = figure(x_axis_label='Year', y_axis_label='Time', tools='box_select') ## Create a figure with the "box_select" tool: p

p.circle(x='Year', y='Time', selection_color='red', nonselection_alpha=0.1, source=source) ## Add circle glyphs to the figure p with the selected and non-selected properties

output_file('selection_glyph.html')
show(p)
```

```python
# Hover glyphs
from bokeh.models import HoverTool ## import the HoverTool

## Add circle glyphs to figure p
p.circle(x, y, size=10,
         fill_color='grey', alpha=0.1, line_color=None,
         hover_fill_color='firebrick', hover_alpha=0.5,
         hover_line_color='white')

hover = HoverTool(tooltips=None, mode='vline') ## Create a HoverTool: hover
p.add_tools(hover) ## Add the hover tool to the figure p

output_file('hover_glyph.html')
show(p)
```
오- 이거 되게 신기하다.

```python
# Colormapping
from bokeh.models import CategoricalColorMapper ##Import CategoricalColorMapper from bokeh.models
source = ColumnDataSource(df) ## Convert df to a ColumnDataSource: source

## Make a CategoricalColorMapper object: color_mapper
color_mapper = CategoricalColorMapper(factors=['Europe', 'Asia', 'US'],
                                      palette=['red', 'green', 'blue'])

## Add a circle glyph to the figure p
p.circle('weight', 'mpg', source=source,
            color=dict(field='origin', transform=color_mapper),
            legend='origin')

output_file('colormap.html')
show(p)

```

# 2. Layouts, Interactions, and Annotations
## 2.1 Introduction to layouts

```python
# Creating rows of plots
from bokeh.layouts import row ## Import row from bokeh.layouts

p1 = figure(x_axis_label='fertility (children per woman)', y_axis_label='female_literacy (% population)') ## Create the first figure: p1
p1.circle('fertility', 'female_literacy', source=source) ## Add a circle glyph to p1

p2 = figure(x_axis_label='population', y_axis_label='female_literacy (% population)') ## Create the second figure: p2
p2.circle('population', 'female_literacy', source=source) ## Add a circle glyph to p2

layout = row(p1, p2) ## Put p1 and p2 into a horizontal row: layout

output_file('fert_row.html')
show(layout)

```

```python
# Creating columns of plots
from bokeh.layouts import column ## Import column from the bokeh.layouts module

p1 = figure(x_axis_label='fertility (children per woman)', y_axis_label='female_literacy (% population)') ## Create a blank figure: p1
p1.circle('fertility', 'female_literacy', source=source) ## Add circle scatter to the figure p1

p2 = figure(x_axis_label='population', y_axis_label='female_literacy (% population)') ## Create a new blank figure: p2
p2.circle('population', 'female_literacy', source=source) ## Add circle scatter to the figure p2

layout = column(p1, p2) ## Put plots p1 and p2 in a column: layout

output_file('fert_column.html')
show(layout)
```

```python
# Nesting rows and columns of plots
from bokeh.layouts import column, row ## Import column and row from bokeh.layouts

row2 = row([mpg_hp, mpg_weight], sizing_mode='scale_width') ## Make a row layout that will be used as the second row: row2
layout = column([avg_mpg, row2], sizing_mode='scale_width') ## Make a column layout that includes the above row layout: layout

output_file('layout_custom.html')
show(layout)
```

## 2.2 Advanced layouts

```python
# Creating gridded layouts
from bokeh.layouts import gridplot ## Import gridplot from bokeh.layouts

row1 = [p1, p2] ## Create a list containing plots p1 and p2: row1
row2 = [p3, p4] ## Create a list containing plots p3 and p4: row2

layout = gridplot([row1, row2]) ## Create a gridplot using row1 and row2: layout

output_file('grid.html')
show(layout)
```

```python
# Starting tabbed layouts
from bokeh.models.widgets import Panel ## Import Panel from bokeh.models.widgets

tab1 = Panel(child=p1, title='Latin America') ## Create tab1 from plot p1: tab1
tab2 = Panel(child=p2, title='Africa') ## Create tab2 from plot p2: tab2
tab3 = Panel(child=p3, title='Asia') ## Create tab3 from plot p3: tab3
tab4 = Panel(child=p4, title='Europe') ## Create tab4 from plot p4: tab4

```

```python
# Displaying tabbed layouts
from bokeh.models.widgets import Tabs ## Import Tabs from bokeh.models.widgets

layout = Tabs(tabs=[tab1, tab2, tab3,tab4]) ## Create a Tabs layout: layout

output_file('tabs.html')
show(layout)
```

## 2.3 Linking plots together

```python
# Linked axes
p2.x_range = p1.x_range ## Link the x_range of p2 to p1: p2.x_range
p2.y_range = p1.y_range ## Link the y_range of p2 to p1: p2.y_range
p3.x_range = p1.x_range ## Link the x_range of p3 to p1: p3.x_range
p4.y_range = p1.y_range ## Link the y_range of p4 to p1: p4.y_range

output_file('linked_range.html')
show(layout)
```

```python
# Linked brushing
source = ColumnDataSource(data) ## Create ColumnDataSource: source

## Create the first figure: p1
p1 = figure(x_axis_label='fertility (children per woman)', y_axis_label='female literacy (% population)',
            tools='box_select,lasso_select')

p1.circle('fertility', 'female literacy', source=source) ## Add a circle glyph to p1

## Create the second figure: p2
p2 = figure(x_axis_label='fertility (children per woman)', y_axis_label='population (millions)',
            tools='box_select,lasso_select')

p2.circle('fertility', 'population', source=source) ## Add a circle glyph to p2

layout = row(p1, p2) ## Create row layout of figures p1 and p2: layout

output_file('linked_brush.html')
show(layout)
```
> Q. tools에서 'lasso_select'이 그 Lasso인가? 어떤 식으로 selection이 된다는 거지? 
> A. 

```python
# How to create legends
p.circle('fertility', 'female_literacy', source=latin_america, size=10, color='red', legend='Latin America') ## Add the first circle glyph to the figure p

p.circle('fertility', 'female_literacy', source=africa, size=10, color='blue', legend='Africa') ## Add the second circle glyph to the figure p

output_file('fert_lit_groups.html')
show(p)
```

```python
# Positioning and styling legends
p.legend.location = 'bottom_left' ## Assign the legend to the bottom left: p.legend.location
p.legend.background_fill_color = 'lightgray' ## Fill the legend background with the color 'lightgray': p.legend.background_fill_color

output_file('fert_lit_groups.html')
show(p)
```

```python
# Adding a hover tooltip
from bokeh.models import HoverTool ## Import HoverTool from bokeh.models

hover = HoverTool(tooltips = [('Country','@Country')]) ## Create a HoverTool object: hover
p.add_tools(hover) ## Add the HoverTool object to figure p

output_file('hover.html')
show(p)
```

# 3. Building interactive apps with Bokeh
## 3.1 Introducing the Bokeh Server
