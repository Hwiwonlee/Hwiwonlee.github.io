# Reporting with R Markdown

## Getting Started with R Markdown

<pre>
---
title: "Investment Report"
output: html_document
---

```{r data, include = FALSE}
library(readr)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
```

```{r}
investment_annual_summary
```
</pre>

<pre>
---
title: "Investment Report"
output: html_document
---

```{r data, include = FALSE}
library(readr)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/78b002735b6f620df7f2767e63b76aaca317bf8d/investment_services_projects.csv")
```


```{r}
investment_annual_summary
investment_services_projects
```
</pre>

<pre>
---
title: "Investment Report"
output: html_document
---

```{r data, include = FALSE}
library(readr)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/78b002735b6f620df7f2767e63b76aaca317bf8d/investment_services_projects.csv")
```


## Datasets

### Investment Annual Summary

The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.

```{r}
investment_annual_summary
```
### Investment Services Projects

The `investment_services_projects` dataset provides information about each investment project from the 2012 to 2018 fiscal years. Information listed includes the project name, company name, sector, project status, and investment amounts.

```{r}
investment_services_projects 
```
</pre>


### The YAML header

<pre>
---
title: "Investment Report"
output: html_document
author : "Lukas"
date : "`r Sys.Date()`"
---
```

</pre>

<pre>
---
title: "Investment Report"
author: "Add your name"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---
</pre>

## Adding Analyses and Visualizations
### Analyzing the data

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r data, include = FALSE}
library(readr)
library(dplyr)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary

The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
investment_annual_summary
```

### Investment Projects in Brazil

The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.
```{r brazil-investment-projects}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil")

brazil_investment_projects
```

### Investment Projects in Brazil in 2018

```{r brazil-investment-projects-2018}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

brazil_investment_projects_2018

brazil_investment_projects_2018_total <- brazil_investment_projects_2018 %>%
  summarize(sum_total_investment = sum(total_investment, na.rm = TRUE)) 
```

The total investment amount for all projects in Brazil in the 2018 fiscal year was `r brazil_investment_projects_2018_total` million dollars.
</pre>

### Adding plots

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary

The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in Brazil

The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.
```{r brazil-investment-projects}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 
  
ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018

```{r brazil-investment-projects-2018}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30")
         
ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Plot options

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', out.width = '80%', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary

The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in Brazil

The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.
```{r brazil-investment-projects}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018

```{r brazil-investment-projects-2018}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary

The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary, out.width = '85%', fig.cap = 'Figure 1.1 The Investment Annual Summary for each region for 2012 to 2018'}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in Brazil

The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.
```{r brazil-investment-projects, out.width = '95%', fig.cap = 'Figure 1.2 The Investment Services Projects in Brazil from 2012 to 2018'}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018

```{r brazil-investment-projects-2018, out.width = '95%', fig.cap = 'Figure 1.3 The Investment Services Projects in Brazil in 2018'}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Organizing the report

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_region_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/52f5414f6504e0503e86eb1043afa9b3d157fab2/investment_region_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 
### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each of the following regions for each fiscal year, from 2012 to 2018:

- East Asia and the Pacific
- Europe and Central Asia
- Latin America and the Caribbean
- Middle East and North Africa
- South Asia
- Sub-Saharan Africa.


```{r investment-annual-summary, out.width = '85%', fig.cap = 'Figure 1.1 The Investment Annual Summary for each region for 2012 to 2018.'}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

```{r tables}
kable(investment_region_summary, col.names = c("Region", "Dollars in Millions"), align = "cc", caption = "Table 1.1 The total investment summary for each region for the 2012 to 2018 fiscal years.")
```


### Investment Projects in Brazil
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.

```{r brazil-investment-projects, out.width = '95%', fig.cap = 'Figure 1.2 The Investment Services Projects in Brazil from 2012 to 2018.'}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `brazil_investment_projects_2018`. 

```{r brazil-investment-projects-2018, out.width = '95%', fig.cap = 'Figure 1.3 The Investment Services Projects in Brazil in 2018.'}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Code chunk options

<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = FALSE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)
library(knitr)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_region_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/52f5414f6504e0503e86eb1043afa9b3d157fab2/investment_region_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 
### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each of the following regions for each fiscal year, from 2012 to 2018:

1. East Asia and the Pacific      
2. Europe and Central Asia        
3. Latin America and the Caribbean
4. Middle East and North Africa   
5. South Asia                     
6. Sub-Saharan Africa

```{r investment-annual-summary, out.width = '85%', fig.cap = 'Figure 1.1 The Investment Annual Summary for each region for 2012 to 2018.', collapse = TRUE}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

```{r tables}
kable(investment_region_summary, col.names = c("Region", "Dollars in Millions"), align = "cc", caption = "Table 1.1 The total investment summary for each region for the 2012 to 2018 fiscal years.")
```

### Investment Projects in Brazil
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.

```{r brazil-investment-projects, out.width = '95%', fig.cap = 'Figure 1.2 The Investment Services Projects in Brazil from 2012 to 2018.', collapse = TRUE}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `brazil_investment_projects_2018`. 

```{r brazil-investment-projects-2018, out.width = '95%', fig.cap = 'Figure 1.3 The Investment Services Projects in Brazil in 2018.', collapse = TRUE}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Warnings, messages, and errors
<pre>
---
title: "Investment Report"
date: "`r format(Sys.time(), '%d %B %Y')`"
output: html_document
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, message = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 
### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary, out.width = '85%', fig.cap = 'Figure 1.1 The Investment Annual Summary for each region for 2012 to 2018.', warning = FALSE}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in Brazil
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts.

```{r brazil-investment-projects, out.width = '95%', fig.cap = 'Figure 1.2 The Investment Services Projects in Brazil from 2012 to 2018.', warning = FALSE}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `brazil_investment_projects_2018`. 

```{r brazil-investment-projects-2018, out.width = '95%', fig.cap = 'Figure 1.3 The Investment Services Projects in Brazil in 2018.' , warning = FALSE}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>


## Customizing the Report
### Adding a table of contents
<pre>
---
title: "Investment Report"
output: 
  html_document:
    toc: true
    toc_float:
      collapsed: false
      smooth_scroll: false
    toc_depth: 3
date: "`r format(Sys.time(), '%d %B %Y')`"
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```

# Datasets 

## Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

## Investment Projects in Brazil
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r brazil-investment-projects}
brazil_investment_projects <- investment_services_projects %>%
  filter(country == "Brazil") 

ggplot(brazil_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

## Investment Projects in Brazil in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `brazil_investment_projects_2018`. Projects that do not have an associated investment amount are excluded from the plot.

```{r brazil-investment-projects-2018}
brazil_investment_projects_2018 <- investment_services_projects %>%
  filter(country == "Brazil",
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(brazil_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in Brazil in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Creating a report with a parameter


<pre>
---
title: "Investment Report"
output: 
  html_document:
    toc: true
    toc_float: true
date: "`r format(Sys.time(), '%d %B %Y')`"
params: 
  country: "Brazil"
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```

## Datasets 

### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in Brazil
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects}
country_investment_projects <- investment_services_projects %>%
  filter(country == params$country) 

ggplot(country_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in Brazil in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `brazil_investment_projects_2018`. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects-2018}
country_investment_projects_2018 <- investment_services_projects %>%
  filter(country == params$country,
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30") 

ggplot(country_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

<pre>
---
title: "Investment Report for Projects in `r params$country`"
output: 
  html_document:
    toc: true
    toc_float: true
date: "`r format(Sys.time(), '%d %B %Y')`"
params:
  country: Bangladesh 
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```

## Datasets 

### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in `r params$country`
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects}
country_investment_projects <- investment_services_projects %>%
  filter(country == params$country) 

ggplot(country_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in `r params$country` in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `country_investment_projects_2018`. Projects that do not have an associated investment amount are excluded from the plot.
```{r country-investment-projects-2018}
country_investment_projects_2018 <- investment_services_projects %>%
  filter(country == params$country,
         date_disclosed >= "2017-07-01",
         date_disclosed <= "2018-06-30")

ggplot(country_investment_projects_2018, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects in 2018",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>


### Multiple parameters

<pre>
---
title: "Investment Report for Projects in `r params$country`"
output: 
  html_document:
    toc: true
    toc_float: true
date: "`r format(Sys.time(), '%d %B %Y')`"
params:
  country: Brazil
  fy: 2018
  year_start: 2017-07-01
  year_end: 2018-06-30
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in `r params$country`
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects}
country_investment_projects <- investment_services_projects %>%
  filter(country == params$country) 

ggplot(country_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in `r params$country` in 2018
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the 2018 fiscal year, and is referred to as `country_annual_investment_projects`. Projects that do not have an associated investment amount are excluded from the plot.
```{r country-annual-investment-projects}
country_annual_investment_projects <- investment_services_projects %>%
  filter(country == params$country,
         date_disclosed >= params$year_start,
         date_disclosed <= params$year_end) 

ggplot(country_annual_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>

### Customizing the report
<pre>
---
title: "Investment Report for Projects in `r params$country`"
output: 
  html_document:
    toc: true
    toc_float: true
date: "`r format(Sys.time(), '%d %B %Y')`"
params:
  country: Bangladesh
  year_start: 2013-07-01
  year_end: 2014-06-30
  fy: 2014
---

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in `r params$country`
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects}
country_investment_projects <- investment_services_projects %>%
  filter(country == params$country) 

ggplot(country_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in `r params$country` in `r params$fy`
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the `r params$fy` fiscal year, and is referred to as `country_annual_investment_projects`. Projects that do not have an associated investment amount are excluded from the plot.
```{r country-annual-investment-projects}
country_annual_investment_projects <- investment_services_projects %>%
  filter(country == params$country,
         date_disclosed >= params$year_start,
         date_disclosed <= params$year_end) 

ggplot(country_annual_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>



<pre>
---
title: "Investment Report for Projects in `r params$country`"
output: 
  html_document:
    toc: true
    toc_float: true
date: "`r format(Sys.time(), '%d %B %Y')`"
params:
  country: Brazil
  year_start: 2017-07-01
  year_end: 2018-06-30
  fy: 2018
---

<style>
h1.title {
  color: #F08080;
  background-color: #F5F5F5;
  opacity: 0.6;
  font-family: Calibri;
  font-size: 20px;
}
h4.author{ 
  color: #708090;
  background-color: #F5F5F5;
  font-family: Calibri;
}
h4.date{
  color: #708090;
  background-color: #F5F5F5;
  font-family: Calibri;
}
#TOC { 
  color: #708090;
  font-family: Calibri;
  font-size: 16px;
  border-color: #708090;
}
body{ 
  color: #708090;
  font-family: Calibri;
  background-color: #F5F5F5;
}
pre{
  color: #708090;
  background-color: #F8F8FF;
}
</style>

```{r setup, include = FALSE}
knitr::opts_chunk$set(fig.align = 'center', echo = TRUE)
```

```{r data, include = FALSE}
library(readr)
library(dplyr)
library(ggplot2)

investment_annual_summary <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/d0251f26117bbcf0ea96ac276555b9003f4f7372/investment_annual_summary.csv")
investment_services_projects <- read_csv("https://assets.datacamp.com/production/repositories/5756/datasets/bcb2e39ecbe521f4b414a21e35f7b8b5c50aec64/investment_services_projects.csv")
```


## Datasets 

### Investment Annual Summary
The `investment_annual_summary` dataset provides a summary of the dollars in millions provided to each region for each fiscal year, from 2012 to 2018.
```{r investment-annual-summary}
ggplot(investment_annual_summary, aes(x = fiscal_year, y = dollars_in_millions, color = region)) +
  geom_line() +
  labs(
    title = "Investment Annual Summary",
    x = "Fiscal Year",
    y = "Dollars in Millions"
  )
```

### Investment Projects in `r params$country`
The `investment_services_projects` dataset provides information about each investment project from 2012 to 2018. Information listed includes the project name, company name, sector, project status, and investment amounts. Projects that do not have an associated investment amount are excluded from the plot.

```{r country-investment-projects}
country_investment_projects <- investment_services_projects %>%
  filter(country == params$country) 

ggplot(country_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  )
```

### Investment Projects in `r params$country` in `r params$fy`
The `investment_services_projects` dataset was filtered below to focus on information about each investment project from the `r params$fy` fiscal year, and is referred to as `country_annual_investment_projects`. Projects that do not have an associated investment amount are excluded from the plot.
```{r country-annual-investment-projects}
country_annual_investment_projects <- investment_services_projects %>%
  filter(country == params$country,
         date_disclosed >= params$year_start,
         date_disclosed <= params$year_end) 

ggplot(country_annual_investment_projects, aes(x = date_disclosed, y = total_investment, color = status)) +
  geom_point() +
  labs(
    title = "Investment Services Projects",
    x = "Date Disclosed",
    y = "Total IFC Investment in Dollars in Millions"
  ) 
```
</pre>
