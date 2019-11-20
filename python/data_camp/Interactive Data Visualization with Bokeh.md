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

```python
# Using the current document
## Perform necessary imports
from bokeh.io import curdoc
from bokeh.plotting import figure

plot = figure() ## Create a new plot: plot
plot.line(x=[1,2,3,4,5], y=[2,5,4,6,7]) ## Add a line to the plot

curdoc().add_root(plot) ## Add the plot to the current document
```
curdoc란 'current document'를 의미한다. curdoc()에는 만든 plot들이나 설정, 레이아웃 등을 'current document'에 추가시킬 수 있는 함수들이 속해있다. 

```python
# Add a single slider
## Perform the necessary imports
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models import Slider

slider = Slider(title='my slider', start=0, end=10, step=0.1, value=2) ## Create a slider: slider
layout = widgetbox(slider) ## Create a widgetbox layout: layout

curdoc().add_root(layout) ## Add the layout to the current document

```

```python
# Multiple sliders in one document
## Perform necessary imports
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models import Slider

slider1 = Slider(title='slider1', start=0, end=10, step=0.1, value=2) ## Create first slider: slider1

# Create second slider: slider2
slider2 = Slider(title='slider2', start=10, end=100, step=1, value=20)

# Add slider1 and slider2 to a widgetbox
layout = widgetbox(slider1, slider2)

# Add the layout to the current document
curdoc().add_root(layout)
```

## 3.2 Connecting sliders to plots

```python
# How to combine Bokeh models into layouts
source = ColumnDataSource({'x': x, 'y': y}) ## Create ColumnDataSource: source

plot.line(x='x', y='y', source=source) ## Add a line to the plot
layout = column(widgetbox(slider), plot) ## Create a column layout: layout

curdoc().add_root(layout) ## Add the layout to the current document
```

```python
# Learn about widget callbacks
## Define a callback function: callback
def callback(attr, old, new):

    ## Read the current value of the slider: scale
    scale = slider.value

    ## Compute the updated y using np.sin(scale/x): new_y
    new_y = np.sin(scale/x)

    ## Update source with the new data values
    source.data = {'x': x, 'y': new_y}

slider.on_change('value', callback) ## Attach the callback to the 'value' property of slider

layout = column(widgetbox(slider), plot) ## Create layout and add to current document
curdoc().add_root(layout)

```

## 3.3 Updating plots from dropdowns
```python
# Updating data sources from dropdown callbacks
from bokeh.models import ColumnDataSource, Select ## Perform necessary imports

## Create ColumnDataSource: source
source = ColumnDataSource(data={
    'x' : fertility,
    'y' : female_literacy
})

plot = figure() ## Create a new plot: plot
plot.circle('x', 'y', source=source) ## Add circles to the plot

## Define a callback function: update_plot
def update_plot(attr, old, new):
    ## If the new Selection is 'female_literacy', update 'y' to female_literacy
    if new == 'female_literacy': 
        source.data = {
            'x' : fertility,
            'y' : female_literacy
        }
    ## Else, update 'y' to population
    else:
        source.data = {
            'x' : fertility,
            'y' : population
        }
select = Select(title="distribution", options=['female_literacy', 'population'], value = 'female_literacy') ## Create a dropdown Select widget: select    
select.on_change('value', update_plot) ## Attach the update_plot callback to the 'value' property of select

layout = row(select, plot) 
curdoc().add_root(layout) ## Create layout and add to current document
```

```python
# Synchronize two dropdowns
## Create two dropdown Select widgets: select1, select2
select1 = Select(title='First', options=['A', 'B'], value='A')
select2 = Select(title='Second', options=['1', '2', '3'], value='1')

## Define a callback function: callback
def callback(attr, old, new):
    ## If select1 is 'A' 
    if select1.value == 'A':
        ## Set select2 options to ['1', '2', '3']
        select2.options = ['1', '2', '3']

        ## Set select2 value to '1'
        select2.value = '1'
    else:
        ## Set select2 options to ['100', '200', '300']
        select2.options = ['100', '200', '300']

        ## Set select2 value to '100'
        select2.value = '100'

select1.on_change('value', callback) ## Attach the callback to the 'value' property of select1

layout = widgetbox(select1, select2)
curdoc().add_root(layout) ## Create layout and add to current document
```
## 3.4 Buttons

```python
# Button widgets
button = Button(label = 'Update Data') ## Create a Button with label 'Update Data'

## Define an update callback with no arguments: update
def update():

    ## Compute new y values: y
    y = np.sin(x) + np.random.random(N)

    ## Update the ColumnDataSource data dictionary
    source.data = {'x': x, 'y': y}

button.on_click(update) ## Add the update callback to the button

layout = column(widgetbox(button), plot)
curdoc().add_root(layout) ## Create layout and add to current document
```

```python
# Button styles
from bokeh.models import CheckboxGroup, RadioGroup, Toggle ## Import CheckboxGroup, RadioGroup, Toggle from bokeh.models

toggle = Toggle(button_type = 'success', label = 'Toggle button') ## Add a Toggle: toggle
checkbox = CheckboxGroup(labels=['Option 1', 'Option 2', 'Option 3']) ## Add a CheckboxGroup: checkbox
radio = RadioGroup(labels=['Option 1', 'Option 2', 'Option 3']) ## Add a RadioGroup: radio

curdoc().add_root(widgetbox(toggle, checkbox, radio)) ## Add widgetbox(toggle, checkbox, radio) to the current document
```

# 4. Putting It All Together! A Case Study

```python
# Some exploratory plots of the data
## Perform necessary imports
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

## Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country' : data.loc[1970].Country,
})

## Create the figure: p
p = figure(title='1970', x_axis_label='Fertility (children per woman)', y_axis_label='Life Expectancy (years)',
           plot_height=400, plot_width=700,
           tools=[HoverTool(tooltips='@country')])

p.circle(x='x', y='y', source=source) ## Add a circle glyph to the figure p

output_file('gapminder.html') ## Output the file and show the figure
show(p)
```

```python
# Beginning with just a plot
## Import the necessary modules
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

## Make the ColumnDataSource: source
source = ColumnDataSource(data ={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country'      : data.loc[1970].Country,
    'pop'      : (data.loc[1970].population / 20000000) + 2,
    'region'      : data.loc[1970].region,
})

xmin, xmax = min(data.fertility), max(data.fertility) ## Save the minimum and maximum values of the fertility column: xmin, xmax
ymin, ymax = min(data.life), max(data.life) ## Save the minimum and maximum values of the life expectancy column: ymin, ymax

## Create the figure: plot
plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

plot.circle(x='x', y='y', fill_alpha=0.8, source=source) ## Add circle glyphs to the plot
plot.xaxis.axis_label ='Fertility (children per woman)' ## Set the x-axis label
plot.yaxis.axis_label = 'Life Expectancy (years)' ## Set the y-axis label

curdoc().add_root(plot)
curdoc().title = 'Gapminder' ## Add the plot to the current document and add a title
```
```python
# Enhancing the plot with some shading
regions_list = data.region.unique().tolist() ## Make a list of the unique values from the region column: regions_list

## Import CategoricalColorMapper from bokeh.models and the Spectral6 palette from bokeh.palettes
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6) ## Make a color mapper: color_mapper

## Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

plot.legend.location = 'top_right' ## Set the legend.location attribute of the plot to 'top_right'

curdoc().add_root(plot)
curdoc().title = 'Gapminder' ## Add the plot to the current document and add the title
```

```python
# Adding a slider to vary the year
from bokeh.layouts import widgetbox, row
from bokeh.models import Slider

## Define the callback function: update_plot
def update_plot(attr, old, new):
    ## Set the yr name to slider.value and new_data to source.data
    yr = slider.value
    new_data = {
        'x'       : data.loc[yr].fertility,
        'y'       : data.loc[yr].life,
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    source.data = new_data


slider = Slider(title = 'Year', start = 1970, end = 2010, step = 1, value = 1970) ## Make a slider object: slider
slider.on_change('value', update_plot) ## Attach the callback to the 'value' property of slider

layout = row(widgetbox(slider), plot)
curdoc().add_root(layout) ## Make a row layout of widgetbox(slider) and plot and add it to the current document
```

```python
# Customizing based on user input
## Define the callback function: update_plot
def update_plot(attr, old, new):
    ## Assign the value of the slider: yr
    yr = slider.value
    ## Set new_data
    new_data = {
        'x'       : data.loc[yr].fertility,
        'y'       : data.loc[yr].life,
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    ## Assign new_data to: source.data
    source.data = new_data

    ## Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % yr

slider = Slider(title = 'Year', start = 1970, end = 2010, step = 1, value = 1970) ## Make a slider object: slider 
slider.on_change('value', update_plot) ## Attach the callback to the 'value' property of slider

layout = row(widgetbox(slider), plot)
curdoc().add_root(layout) ## Make a row layout of widgetbox(slider) and plot and add it to the current document
```

```python
# Adding a hover tool
from bokeh.models import HoverTool ## Import HoverTool from bokeh.models

hover = HoverTool(tooltips=[('Country', '@country')]) ## Create a HoverTool: hover
plot.add_tools(hover) ## Add the HoverTool to the plot
layout = row(widgetbox(slider), plot) ## Create layout: layout
curdoc().add_root(layout) ## Add layout to current document
```

```python
# Adding dropdowns to the app
## Define the callback: update_plot
def update_plot(attr, old, new):
    ## Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    ## Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    ## Set new_data
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    ## Assign new_data to source.data
    source.data = new_data

    ## Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    ## Add title to plot
    plot.title.text = 'Gapminder data for %d' % yr

slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year') ## Create a dropdown slider widget: slider
slider.on_change('value', update_plot) ## Attach the callback to the 'value' property of slider

## Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)

x_select.on_change('value', update_plot) ## Attach the update_plot callback to the 'value' property of x_select

## Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)

y_select.on_change('value', update_plot) ## Attach the update_plot callback to the 'value' property of y_select

layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout) ## Create layout and add to current document
```

bokeh를 이용한 시각화도구들은 HTML로 plot의 결과를 제공하기 때문에 plot을 보는 사람이 변수 선택이나 slider를 조정해 결과를 볼 수 있다는 장점이 있다. 블로그 등의 웹을 통해 결과를 보여줄 때 유용하게 쓸 수 있을 것 같다. 다만 사용자의 조작에 따라 여러가지 결과를 보여줘야하므로 코딩 상의 진입장벽이 조금 있어 늘 그렇듯 따로 공부를 더 해봐야할 것 같다.

> TO DO. bokeh 파트 공부하기

