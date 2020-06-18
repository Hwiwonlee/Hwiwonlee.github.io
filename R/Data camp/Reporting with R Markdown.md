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

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>

<pre>

</pre>
