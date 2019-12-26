# LOG
# ROC와 AUC의 개념 
### **[ROC와 AUC의 기본 컨셉](https://nittaku.tistory.com/297)**  
### **[ROC curve analysis](https://rpubs.com/cardiomoon/64987)**  
#### [ROC Curve and AUC](https://m.cafe.daum.net/biometrika/P8TH/31)
### **[ggroc: Plot a ROC curve with ggplot2](https://rdrr.io/cran/pROC/man/ggroc.html)**  
### **[roc: Build a ROC curve](https://rdrr.io/cran/pROC/man/roc.html)**    
[Package, pROC](https://cran.r-project.org/web/packages/pROC/pROC.pdf)  


# ROC, optimal cut-off value에 대해
[ROC and multiROC analysis: how to calculate optimal cutpoint?](https://stats.stackexchange.com/questions/67560/roc-and-multiroc-analysis-how-to-calculate-optimal-cutpoint)  
[How are the threshold or cutoff points in {Epi} R package selected?](https://stackoverflow.com/questions/38529914/how-are-the-threshold-or-cutoff-points-in-epi-r-package-selected/38532555#38532555)  
[How can I get The optimal cutoff point of the ROC in logistic regression as a number](https://stackoverflow.com/questions/23131897/how-can-i-get-the-optimal-cutoff-point-of-the-roc-in-logistic-regression-as-a-nu)  





# ggplot에서 condition에 따라 color를 다르게 주는 방법
### [ggplot with conditions](https://community.rstudio.com/t/ggplot-with-conditions/17352)  
[ggplot2: doughnuts, how to conditional color fill with if_else](https://stackoverflow.com/questions/45490075/ggplot2-doughnuts-how-to-conditional-color-fill-with-if-else)  


# ggplot에서 그래프 여러개 그리기
#### [동시에 여러 개의 ggplot2 그래프 패널 보여주기](https://m.blog.naver.com/PostView.nhn?blogId=definitice&logNo=221165151283&proxyReferer=https%3A%2F%2Fwww.google.com%2F) : 맨날 까먹음  


# Formula 선언에서 자주 보는 문자 정리
#### [R에서 모델적합에 사용되는 formula 인자식 사용부분에 대한 고찰](https://lovetoken.github.io/r/2016/12/06/formula_usage.html)  





### 못 읽은 것들
[Conditional ggplot2 geoms in functions (QTL plots)](https://shiring.github.io/ggplot2/2017/02/12/qtl_plots)  
[Data Visualization in R](https://rpubs.com/JohnBernau/datavizr4)  
[R Tip: How to Pass a formula to lm](http://www.win-vector.com/blog/2018/09/r-tip-how-to-pass-a-formula-to-lm/)  
[Tweaking R colours with the shades package](http://hughjonesd.github.io/tweaking-colours-with-the-shades-package.html)


```r
#### 1. OLD - Draw ROC curve using identified positive polar metabolites ####
rm(list=ls())


data<-read.csv(".../positive_polar.csv")

## Normal vs CX CAN ROC

data1<-subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


## CINs vs CX CAN ROC

data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

## Normal +CIN1 vs CIN2/3 + CX CAN ROC

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN"|data1$group=="CIN2/3",1,0)


require(Epi)

ROC(form=group1~Alanine,data=data1,plot="ROC")
ROC(form=group1~Creatinine,data=data1,plot="ROC")
ROC(form=group1~Proline,data=data1,plot="ROC")
ROC(form=group1~Pyroglutamic.acid,data=data1,plot="ROC")
ROC(form=group1~Creatine,data=data1,plot="ROC")
ROC(form=group1~Isoleucine,data=data1,plot="ROC")
ROC(form=group1~Hypoxanhine,data=data1,plot="ROC")
ROC(form=group1~Trigonelline,data=data1,plot="ROC")
ROC(form=group1~Glutamate,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine,data=data1,plot="ROC")
ROC(form=group1~Hippuric.acid,data=data1,plot="ROC")
ROC(form=group1~X3.Indolepropionic.acid,data=data1,plot="ROC")
ROC(form=group1~Caffeine,data=data1,plot="ROC")
ROC(form=group1~sn.glycero.3.Phosphocholine,data=data1,plot="ROC")
ROC(form=group1~Inosine,data=data1,plot="ROC")
ROC(form=group1~Nonanoylcarnitine,data=data1,plot="ROC")
ROC(form=group1~AMP,data=data1,plot="ROC")
#### ####

#### 2. NEW - Draw ROC curve using identified positive polar metabolites ####
# Be smart and skillful

## example of "ggroc"
data(aSAH)

rocobj <- roc(aSAH$outcome, aSAH$s100b)
rocobj2 <- roc(aSAH$outcome, aSAH$wfns)



g <- ggroc(rocobj); g

# with additional aesthetics:
ggroc(rocobj, alpha = 0.5, colour = "red", linetype = 2, size = 2)

# You can then your own theme, etc.
g + theme_minimal() + ggtitle("My ROC curve") + 
  geom_segment(aes(x = 1, xend = 0, y = 0, yend = 1), color="grey", linetype="dashed")

# 이전, column을 직접 입력하는 방식으로 해봄. 
ggroc(roc(data1$group1, data1$Alanine),  legacy.axes = TRUE) +
  theme_minimal() + ggtitle("Alanine") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed")
# 근데 좀 비효율적인데. 

# Q. formula를 꼭 column으로 쪼개서 해야 하나?
# TEST 
ggroc(roc(group1~Alanine, data=data1),  legacy.axes = TRUE) +
  theme_minimal() + ggtitle("Alanine") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed")
# formula로 commit해도 됨. formula로 해보자. 


### Drow mutiple ROC line 
g2 <- ggroc(list(s100b=rocobj, wfns=rocobj2, ndka=roc(aSAH$outcome, aSAH$ndka)))
g2 # 방법 1)
roc.list <- roc(outcome ~ s100b + ndka + wfns, data = aSAH)
g.list <- ggroc(roc.list) # 방법 2)

grid.arrange(g2, g.list, nrow=1, ncol=2) # 차이가 있는지 확인, 없음. 

# 모든 Positive polar에 대한 ROC curve를 한번에 그려보자. 
roc.metabolites <- roc(group1 ~ . - (group+ID+group1), data = data1)
ggroc(roc.metabolites, legacy.axes = TRUE) +
  theme_minimal() + ggtitle("Positive polar") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed")

# 조건에 따른 line color setting 
## 가령, AUC가 0.5 미만이면 옅은 색깔, lr.eta가 특정 조건을 만족하지 않으면 옅은 색깔. 등등
### lr.eta : predicted values 중 optimum cut-off value 

ggroc(roc.metabolites, legacy.axes = TRUE) +
  theme_minimal() + ggtitle("Positive polar") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") + 
  geom_col(fill = ifelse(perf.project.tdy$perf>0,"green",
                        ifelse(perf.project.tdy$perf<=-4,"red","orange")),
          width = barwidth)


## AUC check function 
auc_print <- function(roc_result){
  data <- roc_result
  result <- c()
  for (i in 1:length(roc_result)){
    result[i] <- as.numeric(data[[i]]$auc)
  }
  result[length(roc_result)+1] <- mean(result)
  
  return(result)
}

# pROC::roc에서 optimal cut-off value를 어떻게 만들어낼까?
### TRY 사실 Epi::ROC를 쓰면 바로 나오긴 하는데, Epi::ROC에서 ggplot 연동이 안되는 것 같아서 일단 try 
optimal_lr.eta=function(x){
  no = which.max(x$res$sens+x$res$spec)[1]
  result=x$res$lr.eta[no]
  result
}
optimal_lr.eta(a1) 

optimal_lr.eta=function(rec_result){
  no = which.max(rec_result[[1]]$sensitivities + rec_result[[1]]$specificities)[1]
  # result=x$res$lr.eta[no]
  # result
}
print(optimal_lr.eta(roc.metabolites))


```
