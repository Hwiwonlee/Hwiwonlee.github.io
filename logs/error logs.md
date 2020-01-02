# 1. Install MetaboAnalystR
&nbsp;&nbsp;&nbsp;&nbsp;MetaboAnalystR를 설치하기 위해 [개발자의 github](https://github.com/xia-lab/MetaboAnalystR)을 참고했지만 MetaboAnalystR의 dependencies를 설치하는데 애를 먹었다. 에러 메세지로 보아 package repository에 문제가 있는 것 같았는데, 비슷한 문제를 겪은 [stackoverflow](https://stackoverflow.com/questions/45108484/warning-unable-to-access-index-for-repository-https-www-stats-ox-ac-uk-pub-rw)의 글도 참고해보았지만 문제가 해결되지 않았다. 
&nbsp;&nbsp;&nbsp;&nbsp;Solution은 개발자가 제시한 방법 중 R 3.5.1 미만 버전을 위한 설치 방법을 사용하니 문제가 해결되었다. 난 R 3.6.1을 이용 중인데, 왜 구버전을 위한 설치 방법으로 문제없이 설치되었는지 잘 모르겠다. 

```r
# First step on installing MetaboAnalyst
install.packages("pacman")
library(pacman)
pacman::p_load(Rserve, ellipse, scatterplot3d, Cairo, randomForest, caTools, e1071, som, impute, pcaMethods, RJSONIO, ROCR, globaltest, GlobalAncova, Rgraphviz, preprocessCore, genefilter, pheatmap, SSPA, sva, Rcpp, pROC, data.table, limma, car, fitdistrplus, lars, Hmisc, magrittr, methods, xtable, pls, caret, lattice, igraph, gplots, KEGGgraph, reshape, RColorBrewer, tibble, siggenes, plotly, xcms, CAMERA, fgsea, MSnbase, BiocParallel, metap, reshape2, scales)

## Error occured
## Warning: unable to access index for repository https://www.stats.ox.ac.uk/

# Solution 1. from the stackoverflow
options(repos = "https://cran.rstudio.com")
getOption("repos")
options(repos = getOption("repos")["CRAN"])

## Using different way that install MetaboAnalystR from the dev's github
metanr_packages <- function(){
  
  metr_pkgs <- c("Rserve", "ellipse", "scatterplot3d", "Cairo", "randomForest", "caTools", "e1071", "som", "impute", "pcaMethods", "RJSONIO", "ROCR", "globaltest", "GlobalAncova", "Rgraphviz", "preprocessCore", "genefilter", "pheatmap", "SSPA", "sva", "Rcpp", "pROC", "data.table", "limma", "car", "fitdistrplus", "lars", "Hmisc", "magrittr", "methods", "xtable", "pls", "caret", "lattice", "igraph", "gplots", "KEGGgraph", "reshape", "RColorBrewer", "tibble", "siggenes", "plotly", "xcms", "CAMERA", "fgsea", "MSnbase", "BiocParallel", "metap", "reshape2", "scales")
  
  list_installed <- installed.packages()
  
  new_pkgs <- subset(metr_pkgs, !(metr_pkgs %in% list_installed[, "Package"]))
  
  if(length(new_pkgs)!=0){
    
    if (!requireNamespace("BiocManager", quietly = TRUE))
      install.packages("BiocManager")
    BiocManager::install(new_pkgs)
    print(c(new_pkgs, " packages added..."))
  }
  
  if((length(new_pkgs)<1)){
    print("No new packages added...")
  }
}
metanr_packages()
```
