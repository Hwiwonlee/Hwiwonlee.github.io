log 목록을 따로 떼어놓을까 고민 중. 

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
### **[Laying out multiple plots on a page](https://cran.r-project.org/web/packages/egg/vignettes/Ecosystem.html)**  

# ggplot, aes, order를 주는 방법
### **[How do you order the fill-colours within ggplot2 geom_bar](https://stackoverflow.com/questions/15251816/how-do-you-order-the-fill-colours-within-ggplot2-geom-bar)**  

# ggplot, aes, alpha, group에 따라 투명도 조정
### **[R ggplot transparency - alpha values conditional on other variable](https://stackoverflow.com/questions/24800626/r-ggplot-transparency-alpha-values-conditional-on-other-variable)**  

# ggplot, line graph, row 순서에 맞게 그리기
## **[Make a ggplot line plot where lines follow row order](https://stackoverflow.com/questions/20526618/make-a-ggplot-line-plot-where-lines-follow-row-order)**  

# ggplot, plot 안에 value 넣기 
[How to add X and Y point coordinates in ggplot2?](https://stackoverflow.com/questions/49945120/how-to-add-x-and-y-point-coordinates-in-ggplot2/49949059)  
[Label points in geom_point](https://stackoverflow.com/questions/15624656/label-points-in-geom-point)

# ggplot, color
[R - ggplot2 - colors/ palette](http://blog.naver.com/PostView.nhn?blogId=coder1252&logNo=220945693871&parentCategoryNo=&categoryNo=1&viewDate=&isShowPopularPosts=true&from=search)  



# Formula 선언에서 자주 보는 문자 정리
#### [R에서 모델적합에 사용되는 formula 인자식 사용부분에 대한 고찰](https://lovetoken.github.io/r/2016/12/06/formula_usage.html)  

# row-wise dataset
[Row_wise dataset](https://statkclee.github.io/r-novice-gapminder/14-tidyr-kr.html)  

# applys 
[apply function 정리 ](https://3months.tistory.com/389)  

# Heatmap.2 function
[heatmap.2() 그림을 그릴때 성가신 것 바로잡기](http://blog.genoglobe.com/2018/05/r-heatmap2.html)
[heatmap.2 그림을 조정해 보자](http://blog.genoglobe.com/2015/08/r-heatmap2.html)
[Tutorial by Examples: 히트맵](https://thebook.io/006723/ch09/02/01/)
[efg’s R Notes: gplots: heatmap.2](http://earlglynn.github.io/RNotes/package/gplots/heatmap2.html)
[heatmap.2 from R doucuments](https://www.rdocumentation.org/packages/gplots/versions/3.0.1.1/topics/heatmap.2)

### 못 읽은 것들
[Conditional ggplot2 geoms in functions (QTL plots)](https://shiring.github.io/ggplot2/2017/02/12/qtl_plots)  
[Data Visualization in R](https://rpubs.com/JohnBernau/datavizr4)  
[R Tip: How to Pass a formula to lm](http://www.win-vector.com/blog/2018/09/r-tip-how-to-pass-a-formula-to-lm/)  
[Tweaking R colours with the shades package](http://hughjonesd.github.io/tweaking-colours-with-the-shades-package.html)

[1](https://stackoverflow.com/questions/22915337/if-else-condition-in-ggplot-to-add-an-extra-layer)  
[2](https://stackoverflow.com/questions/41666078/ggplot-for-loop-outputs-all-the-same-graph)  
[3](https://stackoverflow.com/questions/31321734/ggplot-line-or-point-plotting-conditionally)  
[4](https://stackoverflow.com/questions/46570609/iteratively-apply-ggplot-function-within-a-map-function)  



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
```

```r
#### 1. NEW - Draw ROC curve using identified positive polar metabolites ####
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
## Q. lr.eta가 크면 AUC가 큰가? lr.eta가 크면 좋은가? AUC가 크면 좋은가? 


roc.metabolites <- roc(group1 ~ . - (group+ID+group1), data = data1)

ggroc(roc.metabolites[1], legacy.axes = TRUE) +
  theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") +
  scale_colour_hue(c = 45, l = 95)

ggroc(roc.metabolites, legacy.axes = TRUE) +
  theme_minimal() + ggtitle("Positive polar") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") + 
  geom_line(colour = ifelse("AUC" > 0,"green",
                            ifelse("AUC" > 0.5, "orange", "red")))

y <- sapply(roc.metabolites[,1:4], function(x) {x > 3})


lapply(roc.metabolites, summary)


roc.metabolites[[1]]$auc

auc_print(roc.metabolites)
c(rep(NA, length(roc.metabolites)))


a <- conditional_ggplot(roc.metabolites)

a[[1]] + a[[2]]



#### TRY ####
conditional_ggplot = function(roc_result){
  
  plots <- list()
  position_1st <- c(rep(NA, length(roc_result)))
  position_2nd <- c(rep(NA, length(roc_result)))
  position_3nd <- c(rep(NA, length(roc_result)))
  position_4th <- c(rep(NA, length(roc_result)))
  x <- NULL
  for (i in 1:length(roc_result)) {
    
    # base ggroc call
    p <- ggroc(roc_result[i], legacy.axes = TRUE) +
      theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
      geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") 
    
    # add geom layer based on content of argument:
    ## AUC가 0.3 미만이면 drop
    ## AUC가 0.3 이상, 0.5미만이면 흐리게
    ## AUC가 0.5 이상, 0.7미만이면 기본
    ## AUC가 0.7 이상이면 진하게 
    if(as.numeric(roc_result[[i]]$auc) < 0.3){
      p <- p + scale_colour_hue(l = 100)
      position_1st[i] <- i
    }
    if(as.numeric(roc_result[[i]]$auc) < 0.5){
      p <- p + scale_colour_hue(l = 80)
      position_2nd[i] <- i
    }
    if(as.numeric(roc_result[[i]]$auc) < 0.7){
      p <- p + scale_colour_hue(l = 65)
      position_3nd[i] <- i
    }
    if(as.numeric(roc_result[[i]]$auc) < 1){
      p <- p + scale_colour_hue(l = 45)
      position_4th[i] <- i
    }
    
    
    
    # 'plus'로 plot이 합쳐지진 않네
    # IDEA. 그럼 roc result dataframe으로 합쳐서 그냥 그리는 건 어떨까? 
    # plots[[i]] <- p
    # if(i == 1){
    #   x <- p} else
    #     x <- x + p
    
    #...
  }
  return(x)
  # ...
}


#### Wiggling problem ####
# sensitivity와 1-spectificity로 그려서 ggroc와 같은지 확인해보자. 
plot(y = roc.metabolites[[1]]$sensitivities, x = 1-roc.metabolites[[1]]$specificities, type = "l")
# plot()으로 그렸더니 대충 비슷한 것 같은데? 

# ggplot + geom_line()으로 그려서 확인해보자. 
fafa = as.data.frame(cbind(1-roc.metabolites[[1]]$specificities, roc.metabolites[[1]]$sensitivities))

plot(y = fafa$V2, x = fafa$V1, type = "l")

c <- ggplot(data = fafa, aes(x = V1, y = V2)) +
  geom_line() + 
  # geom_point() +  
  theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed")

b <- ggroc(roc.metabolites[1], legacy.axes = TRUE) +
  theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed")

# c : result를 그대로 이용, b : ggroc을 이용함. 
grid.arrange(c, b, nrow = 1, ncol = 2)


# Q. 왜 plot에서는 안보이던 wiggling이 ggplot에서는 보이지?
## 이걸로 2시간 날림. 더 날릴 수도? 

# V1 : 1-spec에서 이전 값보다 커지는 경우가 있는가? 
t <- c()
for(i in 1:nrow(fafa)){
  if(fafa$V1[i+1] > fafa$V1[i]){
    t[i] <- i
  } else t[i] <- NA
}

length(na.omit(t)) # 없음 

# V2 : sens에서 이전 값보다 커지는 경우가 있는가? 
r <- c()
for(i in 1:nrow(fafa)){
  if(fafa$V2[i+1] > fafa$V2[i]){
    r[i] <- i
  } else r[i] <- NA
}

length(na.omit(r)) # 없음

## 중간 CONCLUSION : dataset을 잘못 넣은게 아니라 ggplot 상의 문제이다. 
## 사실, plot()을 이용한 그림에서는 정상적으로 나오는데 ggplot()을 이용한 그림에선 흔들림이 생기는 것이 문제. 

# 그럼 ggplot이 어떻게 그려지는 거야? 
ggplot(data = fafa[1:10, ], aes(x = V1, y = V2)) +
  geom_line() +
  geom_point() + geom_text(aes(V1, V2, label=paste(round(V1, 2), round(V2, 2), sep=",")), hjust=0, vjust=0)

round(fafa[1:10, ], 2)

# SOLVE!
# ggplot이 row 순서대로 그려지지 않고 있었다. 
# 가령 4th (0.98, 1) 후 5th (0,97, 1)로 line이 이어져야하는데 7th(0.97, 0.98)로 이어지고 있다. 

# Q. 그래서 이걸 어떻게 풀어야하나? 
# geom_path를 이용해보라는 SOF의 답변을 참고
ggplot(data = fafa, aes(x = V1, y = V2)) +
  geom_path() 
#### SOLVE. 근데 이거 왜 되냐. 아깐 안됐는데...? 억울하다..........#####

ggplot(data = fafa, aes(x = V1, y = V2)) +
  geom_path() 



rs_1 <- as.tbl(as.data.frame(matrix(0, nrow = length(roc.metabolites[[1]]$sensitivities), ncol = 2)))
rs_2 <- as.tbl(as.data.frame(matrix(0, nrow = length(roc.metabolites[[1]]$sensitivities), ncol = length(roc.metabolites)*2)))
for(i in 1:length(roc.metabolites)){
  rs_1[, 1] <- 1-roc.metabolites[[i]]$specificities
  rs_1[, 2] <- roc.metabolites[[i]]$sensitivities
  rs_2[, ((2*i)-1) : (2*i)] <- rs_1
}
# 이것보단 그냥 concat해서 index단위로 붙이는 게 나을 것 같은데. 


#### prefaring Function ####
group_auc_rs <- c(NA, length(roc.metabolites))

rs_1 <- as.tbl(as.data.frame(matrix(0, nrow = length(roc.metabolites[[1]]$sensitivities), ncol = 5)))
rs_2 <- as.tbl(as.data.frame(matrix(0, nrow = 0, ncol = 5)))

for(i in 1:length(roc.metabolites)){
  rs_1[, 1] <- names(roc.metabolites)[i]
  rs_1[, 2] <- 1-roc.metabolites[[i]]$specificities
  rs_1[, 3] <- roc.metabolites[[i]]$sensitivities
  rs_1[, 4] <- as.numeric(roc.metabolites[[i]]$auc)
  
  # auc에 따른 group을 만들기 
  rs_1[, 5] <- if(rs_1[, 4] < 0.3){
    "less than 0.3"
  } else if(rs_1[, 4] < 0.5) {
    "less than 0.5"
  } else if(rs_1[, 4] < 0.6) {
    "less than 0.6"
  } else if(rs_1[, 4] < 0.7){
    "less than 0.7"
  } else {
    "more than 0.7"
  }
  
  # row-wise dataset 저장 
  rs_2 <- rbind(rs_2, rs_1)
  
}

0 < rs_2[, 4] & rs_2[, 4] <= 0.584

rs_2 %>% 
  rename(Var = V1, 
         Spec = V2, 
         Sens = V3,
         AUC = V4, 
         Group = V5) -> rs_2

rs_2 %>% arrange(desc(AUC)) -> rs_2

ggplot(rs_2, aes(x=Spec, y=Sens, col = Var)) + 
  geom_path() # 까지 성공 


# 이제 auc에 따라 투명도를 조절해보자. 
ggplot(rs_2, aes(x=Spec, y=Sens, col = Var, alpha = Group, order=AUC)) + 
  geom_path() # Group 별로 alpha를 다르게 줌. 


# 하나의 공간에 모든 그래프, group별로 나뉜 그래프를 그려보자. 
t1 <- ggplot(rs_2, aes(x=Spec, y=Sens, alpha = Group)) + 
  geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") 


t2 <- ggplot(rs_2 %>% 
               dplyr::filter(Group == "less than 0.6"),
             aes(x=Spec, y=Sens, col = Var, order=AUC)) + 
  geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") +
  scale_color_brewer(palette = "RdYlBu")

t3 <- ggplot(rs_2 %>% 
               dplyr::filter(Group == "less than 0.7"),
             aes(x=Spec, y=Sens, col = Var, order=AUC)) + 
  geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") +
  scale_color_brewer(palette = "RdYlBu")

t4 <- ggplot(rs_2 %>% 
               dplyr::filter(Group == "more than 0.7"),
             aes(x=Spec, y=Sens, col = Var, order=AUC)) + 
  geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
  geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") +
  scale_color_brewer(palette = "RdYlBu")


# grid.arrange를 이용한 공간분할 
grid.arrange(
  grobs = list(t1, t2, t3, t4),
  layout_matrix = rbind(c(1,1,1),
                        c(2,3,4))
)

## 일단 완성. 이제 Function으로 바꿔보자. 
proto_roc_curve_HW <- function(roc.result){
  ## pROC::roc의 결과를 이용해 ROC curve를 AUC에 근거한 "group"으로 나눠 그려주는 함수 ##
  ## Function that draws ROC curve seperating with group based on AUC ##
  
  # 1. Generate result space 
  plots <- list()
  rs_1 <- as.tbl(as.data.frame(matrix(0, nrow = length(roc.result[[1]]$sensitivities), ncol = 5)))
  rs_2 <- as.tbl(as.data.frame(matrix(0, nrow = 0, ncol = 5)))
  
  
  # 2. Generate tbl with storing values 
  for(i in 1:length(roc.result)){
    rs_1[, 1] <- names(roc.result)[i] # Variable name 
    rs_1[, 2] <- 1-roc.result[[i]]$specificities # 1-specificy
    rs_1[, 3] <- roc.result[[i]]$sensitivities # sencsitivity
    rs_1[, 4] <- as.numeric(roc.result[[i]]$auc) # AUC 
    
    # Grouping based on AUC
    rs_1[, 5] <- if(rs_1[, 4] < 0.3){
      "less than 0.3"
    } else if(rs_1[, 4] < 0.5) {
      "less than 0.5"
    } else if(rs_1[, 4] < 0.6) {
      "less than 0.6"
    } else if(rs_1[, 4] < 0.7){
      "less than 0.7"
    } else {
      "more than 0.7"
    }
    
    # Store row-wise dataset 
    rs_2 <- rbind(rs_2, rs_1)
    
  }
  
  # Renaming 
  rs_2 %>% 
    rename(Var = V1, 
           Spec = V2, 
           Sens = V3,
           AUC = V4, 
           Group = V5) -> rs_2
  
  
  
  # 3. Plotting one space with using whole variables and each group's variables 
  plots[[1]] <- ggplot(rs_2, aes(x=Spec, y=Sens, alpha = Group)) + 
    geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
    geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") 
  
  
  for(j in 1:length(unique(rs_2$Group))){
    plots[[j+1]] <- ggplot(rs_2 %>% 
                             dplyr::filter(Group == unique(Group)[j]),
                           aes(x=Spec, y=Sens, col = Var, order=AUC)) + 
      geom_path() + theme_minimal() + ggtitle("ROC curves of Positive polar metabolites") + 
      geom_segment(aes(x = 0, xend = 1, y = 0, yend = 1), color="red", linetype="dashed") +
      scale_color_brewer(palette = "RdYlBu")
  }
  ## "RdYlBu"의 색깔 조합이 너무 혼란스러운 것 같다.
  ## palette를 사용하면 한 plot의 Varaible의 순서대로 진하게 -> 옅게로 바뀌는게 싫음.
  ## Q. 그럼 어떻게 바꿔줘야할까? 
  
  # grid.arrange를 이용한 공간분할 
  result <- grid.arrange(
    grobs = plots,
    layout_matrix = rbind(rep(1, length(unique(rs_2$Group))),
                          seq(2, length(unique(rs_2$Group))+1))
  )
  
  return(result)
}


# Q. 아래 두 개가 똑같은데 왜 2번은 실행이 안되는걸까? 
grid.arrange(
  grobs = proto_roc_curve_HW(roc.metabolites),
  layout_matrix = rbind(c(1,1,1),
                        c(2,3,4))
)  
grid.arrange(
  grobs = proto_roc_curve_HW(roc.metabolites),
  layout_matrix = rbind(rep(1, length(unique(rs_2$Group))),
                        seq(2, length(unique(rs_2$Group)))+1)
)
# SOLVE! 
# seq(2, length(unique(rs_2$Group)))+1) != seq(2, length(unique(rs_2$Group))+1)


#### END : Function, proto_roc_curve_HW ####
proto_roc_curve_HW(roc.metabolites) # 결과 확인 



#### ####


#### AUC check function ####
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




#### ####
```

```r
#### 2. OLD Draw ROC curve using identified negative polar metabolites ####
#### Part 1. ####
# This Part use the identified metabolites. So, actually this part should move to behind part 2 in "2. OLD section".
# But i don't want to mess this "OLD" legacy. Therefore I do not handle this.

data <- read.csv(".../negative_polar.csv")

data1 <- subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1 <- ifelse(data1$group=="CX CAN",1,0)

## CINs vs CX CAN ROC

data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

## Normal +CIN1 vs CIN2/3 + CX CAN ROC

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN"|data1$group=="CIN2/3",1,0)



ROC(form=group1~Lactate,data=data1,plot="ROC")
ROC(form=group1~Dimethylglycine,data=data1,plot="ROC")
ROC(form=group1~X3.Hydroxybutyric.acid,data=data1,plot="ROC")
ROC(form=group1~Malate,data=data1,plot="ROC")
#### ####

#### Part 2. ####
# This Part use the un-identified metabolites. That means, this is the real first step on the 3. OLD using rawdataset.
# But as I wrote before, I don't take this sequence for preserve original legacy

options(java.parameters = "-Xmx4g")
polar_negative<-read.csv(".../polar_negative.csv")


x<-c()
p<-c()

for( i in 3:2565){
  x[i]<-colnames(polar_negative[i])
  p[i]<-round(kruskal.test(polar_negative[,i]~polar_negative$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,".../polar_negative_kw.csv")

polar_positive<-read.csv(".../polar_positive.csv")

x<-c()
p<-c()
for( i in 3:1928){
  x[i]<-colnames(polar_positive[i])
  p[i]<-round(kruskal.test(polar_positive[,i]~polar_positive$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,".../polar_positive_kw.csv")


lipid_positive<-read.csv(".../lipid_positive.csv")

x<-c()
p<-c()
for( i in 3:4357){
  x[i]<-colnames(lipid_positive[i])
  p[i]<-round(kruskal.test(lipid_positive[,i]~lipid_positive$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,".../lipid_positive_kw.csv")

lipid_negative<-read.csv(".../lipid_negative.csv")

x<-c()
p<-c()
for( i in 3:3840){
  x[i]<-colnames(lipid_negative[i])
  p[i]<-round(kruskal.test(lipid_negative[,i]~lipid_negative$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,".../llipid_negative_kw.csv")

#### ####
```

```r
#### 2. New Draw ROC curve using identified negative polar metabolites #####
#### Part 1. #### 
# load csv file and store to 'data'
data <- as.tibble(read.csv(".../negative_polar.csv"))

# OLD version would be some comparison rearch using grouping 
## 1) Normal vs CX CAN / 2) CIN1 + CIN2/2 vs CX CAN / 3) Normal + CIN1 vs CIN2/3 + CX CAN 

# exercise about filtering
## value of group column equals to "Normal" or "CX CAN"
data %>% 
  dplyr::filter(group == "Normal" | group == "CX CAN") %>% # -> data1_NEW, data1 totally equals to data1_NEW
  mutate(group1 = ifelse(group == "CX CAN", 1, 0)) -> data1_NEW # data1 totally equals to data1_NEW

## check the equality data1 and data1_NEW
sum(data1 != data1_NEW)

# Actually, I do not have to make some different versions like OLD. 
data %>% 
  ### 1) Normal vs CX CAN
  dplyr::filter(group == "Normal" | group == "CX CAN") %>%
  mutate(group1 = ifelse(group == "CX CAN", 1, 0)) %>% 
  
  
  ### 2) CIN1 + CIN2/2 vs CX CAN
  dplyr::filter(group=="CIN1"|group=="CIN2/3"|group=="CX CAN") %>% 
  mutate(group1 = ifelse(group == "CX CAN", 1, 0)) %>% 
  
  
  ### 3) Normal + CIN1 vs CIN2/3 + CX CAN
  mutate(group1 = ifelse(group=="CX CAN"|group=="CIN2/3",1,0)) %>% 
  
  ### Drawing ROC curve
  ROC(form = group1~Lactate, data=., plot="ROC") %>% 
  ROC(form = group1 ~ Dimethylglycine , data = ., plot="ROC") %>% 
  ROC(form=group1~X3.Hydroxybutyric.acid,data=data1,plot="ROC") %>% 
  ROC(form=group1~Malate,data=data1,plot="ROC")

# <TO DO> Covert more convenient

#### ####

#### Part 2. ####
# options(java.parameters = "-Xmx4g") remove

# Load rawdata and store to 'polar_negative'
polar_negative <- read.csv(".../polar_negative.csv")
## I forced to use 'data.frame' format, non-tibble. beacause of kruskal.test function 

# Generatign function for sum up part 2
## In this Part 2, acutually, just repeat iteration code using kruskal.test over and over again
## So the thing is only changed input dataset for  using kruskal.test

kruskal_test <- function(df, start, end){
  ### function that kruskal test  ###
  ### df : input dataset ###
  ### start, end : points of variables start and end 
  
  # store space 
  x <- c()
  p <- c()
  
  # iteration part for kruskal.test
  for (i in start:end){
    x[i] <- colnames(df[i])
    p[i] <- round(kruskal.test(df[,i] ~ df$group)$p.value, 5)
    result <- tibble(x, p)
  }
  # return result 
  return(result)
}

# Just comparison New and Old

x<-c()
p<-c()

for( i in 3:2565){
  x[i]<-colnames(polar_negative[i])
  p[i]<-round(kruskal.test(polar_negative[,i]~polar_negative$group)$p.value,5)
  data<-data.frame(x,p)
}

# check the same result 
head(kruskal_test(polar_negative, 3, length(polar_negative)), 10)

# To save the result to new csv file 
write.csv(kruskal_test(polar_negative, 3, length(polar_negative)),".../polar_negative_kw.csv")

# This is the process of making a function and checking the results
# In now, use the function for more smart

# polar_positive dataset 
polar_positive <- read.csv(".../polar_positive.csv")
write.csv(kruskal_test(polar_positive, 3, length(polar_positive)),".../polar_positive_kw.csv")

# lipid_positive dataset
lipid_positive <- read.csv(".../lipid_positive.csv")
write.csv(kruskal_test(lipid_positive, 3, length(lipid_positive)),".../lipid_positive_kw.csv")

# lipid_negative dataset
lipid_negative <- read.csv(".../lipid_negative.csv")
write.csv(kruskal_test(lipid_negative, 3, length(lipid_negative)),".../llipid_negative_kw.csv")

# It seems like newbie's coding but very intuitive style
# However it needs to commit more efficient using 'user def function' to reduce repeatation code 

# <TO DO> def function and test 
# <END> I create function, kruskal_test. The messy code was neatly organized with a kruskal_test function
#### ####
```

```r
#### 3. OLD Heatmap plot and HCA using identified negative polar metabolites ####
# HCA means 'Hierarchical cluster analysis'

#### Part 1. Draw heatmap plot #### 
rm(list=ls())

data<-read.csv(".../polar_negative_for_heatmap.csv")
rownames(data)<-data[,1]
data<-data[,-1]

install.packages("gplots")
library(gplots)


heatmap1<-as.matrix(scale(data)) #?젙洹쒗솕
heatmap1<-as.matrix(scale(log(data))) #?젙洹쒗솕

for(i in 1:202){data[,i]<-ifelse(data[,i]<0,0,data[,i])}
for(i in 1:202){data[,i]<-log10(as.numeric(data[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))


heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)

#### ####

#### Part 2. Hierarchical cluster analysis ####
hc.rows <- hclust(dist(heatmap1))
plot(hc.rows)
table(cutree(hc.rows,k=5))

hc.cols <- hclust(dist(t(heatmap1)))
plot(hc.cols)
table(cutree(hc.cols,k=3))
#### ####
```

```r
#### 3. NEW Heatmap plot and HCA using identified negative polar metabolites ####
# HCA means 'Hierarchical cluster analysis'

#### Part 1. Draw heatmap plot #### 

# polar_negative_for_heatmap.csv과 polar_negative의 차이?
# kruskal test 후 0.03 이하의 p-value를 갖는 X만을 take한 것
# 그렇다면 .csv file을 따로 만들지 않고 polar_negative를 편집해서 하는게 더 나을 것. 

data <- read.csv(".../polar_negative.csv")
colnames(data)
rownames(data)

# kruskal_test 후 결과를 re_krus에 저장 
kruskal_test(data, 3, length(data)) %>% 
  mutate(sig = ifelse(p <= 0.03, 1, 0)) -> re_krus

# tanspose re_krus
t_re_krus <- as_tibble(cbind(nms = names(re_krus[, -1]), t(re_krus[, -1])))[, -1]

# change t_re_krus's column names same as data's things
names(t_re_krus) <- names(data)

rbind(data, t_re_krus) %>% # data와 kruscal test 결과 bind
  as_tibble() %>% 
  # kruscal test에서 p value가 0.03 이하인 것만 select
  select(group, id, which(.[nrow(.),] == 1)) %>% # 205 x 1004
  ## <TO DO> column name을 각 group_N으로 바꾸고 1st row 삭제
  ## <TO DO> add column about variable index(left out the alphabet in X1, X2, X17,...)
  ## <TO DO> Transpose dataset 
  cbind(cnames = names(.), t(.))


rbind(data, t_re_krus) %>% # data와 kruscal test 결과 bind
  as_tibble() %>% 
  # kruscal test에서 p value가 0.03 이하인 것만 select
  select(group, id, which(.[nrow(.),] == 1)) -> filter_result # 205 x 1006

filter_result %>%
  rownames_to_column %>% 
  gather(var, value, -rowname) %>%
  # dplyr::filter(rowname == 1) # 1st_obs 선택
  pivot_wider(names_from = "rowname", values_from = "value") -> test_res
# spread(rowname, value) -> test_res # 1006 x 206
## <PROBLEM> spread를 사용하면 X, id, variable의 indexing이 모두 꼬여버림.
## <SOLVE> spread가 아니라 pivot_wider를 사용했더니 제대로 나옴. 

# test_res의 column name 바꾸기 
# <GOAL> test_res의 column name을 group+id의 꼴로 바꿔보자. 
names(test_res) # 현재 column name 
data[50:70, 1:2] # dataset의 group과 id 확인

coln <- c()
for(i in 1:nrow(data)) {
  coln[i] <- paste0(data[i, 1],"_", data[i, 2])
}
length(coln)

names(test_res)[2:204] <- coln
names(test_res)[205:206] <- c("p_kruscal" ,"<=0.03")

last_res <- test_res[-1, ]

#### 일단 last_res로 결과 저장함. ####

#### <HERE!!> 확인해볼 것 ####
# heat_map용으로 편집된 data_c와 last_res의 결과 확인 
data_c <- read.csv(".../polar_negative_for_heatmap.csv")
dim(data_c) # 1004 x 205, X를 제대로 뽑아낸 것 확인  

dim(last_res[2:nrow(last_res), 2:ncol(last_res)-2])

# group별 몇 개씩 있는 지 확인 
data %>% as_tibble() %>% group_by(group) %>% summarise(n = n())

sum(last_res[2:nrow(last_res), 2:69] != data_c[, 2:69])
sum(last_res[2:nrow(last_res), 70:122] != data_c[, 70:122])
sum(last_res[2:nrow(last_res), 123:149] != data_c[, 123:149])
sum(last_res[2:nrow(last_res), 150:203] != data_c[, 150:203]) 
# <CLEAR>
# <NOTE> data_c에는 VIP가 없음. 딱 obs만큼의 data만 존재




# <RROLBEM> rownames이 바뀌지 않음. 
# rownames(last_res_2) <- last_res_2[, 1]
# <SOLVE> last_res_2[, 1]를 쓰면 return이 matrix형태로 옴
# rownames에 넣으려면 vector여야하므로 $ indexing을 해야함
rownames(last_res_2) <- last_res_2$var

last_res_2 <- last_res_2[, -1]
last_res_2


# 이제 heatmap을 만들어보자.
library(gplots)
# legacy에서 사용했던 형태대로 하려면 뒤의 3개의 열을 빼야한다. 
last_res_2[, 200:205]
heatmap_data <- last_res_2[, -(203:205)]


#### legacy code ####
#### Part 1. Draw heatmap plot #### 
rm(list=ls())

data<-read.csv(".../polar_negative_for_heatmap.csv")
rownames(data)<-data[,1]
data<-data[,-1]

install.packages("gplots")
library(gplots)


heatmap1 <- as.matrix(scale(data)) #?젙洹쒗솕
heatmap1 <- as.matrix(scale(log(data))) #?젙洹쒗솕

for(i in 1:202){data[,i]<-ifelse(data[,i]<0,0,data[,i])}
for(i in 1:202){data[,i]<-log10(as.numeric(data[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))


heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)

#### ####

# scaleing을 위한 obs의 type convert 
heatmap_data %>% 
  type_convert(cols(Normal_1 = col_double())) -> heatmap_data

# heatmap_data obs 중 음수를 0으로 바꿔줌. 음수가 정의되지 않나봄 

for(i in 1:ncol(heatmap_data)){
  for(j in 1:nrow(heatmap_data)){
    heatmap_data[j, i] <- ifelse(heatmap_data[j, i] <= 0, 0.0000001, heatmap_data[j, i])
  }
}



heatmap_scale <- as.matrix(scale(heatmap_data)) # 평균-표준편차를 이용한 scaling
heatmap_scale_log <- as.matrix(scale(log(heatmap_data))) # log를 이용한 scaling 

colCols <- ifelse(grepl("Normal",colnames(heatmap_scale)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap_scale)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap_scale)),"red","black")))))


heatmap.2(heatmap_scale, scale='none',
          trace="none", cexRow=1, keysize=0.75, ColSideColors=colCols, labCol=NA, margins = c(10, 20))

heatmap.2(heatmap_scale_log, scale='none',
          trace="none", cexRow=1, keysize=0.75, ColSideColors=colCols, labCol=NA, margins = c(10, 20))


# To solve the error in plot.new() : figure margins too large
# 그러나 효과는 미비했다. 
par("mar")
par(mar = c(0.1,0.1,0.1,0.1))

# legend를 붙이기 위한 cdoe 
par(lend = 1)
legend("topright", legend = c("Normal", "CIN1", "CIN2/3","Cancer"), col = c("purple", "lightblue","red", "black"),
       lty=1, lwd =2, border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)

# <CHECK> 이 로직이 맞나? heatmap.2에 대한 공부가 필요하다. 일단 계속해보자. 
#### ####

#### Part 2. Hierarchical cluster analysis ####
hc.rows <- hclust(dist(heatmap_scale_log))
plot(hc.rows)
table(cutree(hc.rows,k=5))

hc.cols <- hclust(dist(t(heatmap_scale_log)))
plot(hc.cols)
table(cutree(hc.cols,k=3))

# 그려지긴 하는데 이게 의미가 있나? 
#### ####
```

```r
#### 4. OLD ROC, AUC, on the number of all cases using polar negative metabolites ####
data<-read.csv(".../polar_negative.csv")

# Normal vs CX cAN
data1<-subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

library(Epi)

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal_CXCAN_auc.csv")

# Normal vs CIN1
data1<-subset(data,data$group=="Normal"|data$group=="CIN1")
data1$group1<-ifelse(data1$group=="CIN1",1,0)

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal_CIN1.csv")


# Normal vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal_CIN2.3.csv")

# Normal,C1 vs CIN2/3,cx can
data1<-data
data1$group1<-ifelse(data1$group=="CIN2/3"|data1$group=="CX CAN",1,0)
x<-c()
auc<-c()

library(Epi)
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal c1_CIN2.3 cx.csv")

# CIN1 vs CIN2/3
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_CIN1_CIN2.3.csv")

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

install.packages("MASS")
library(Epi)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X2767,data=data1,plot="ROC")
ROC(form=group1~X57+X938+X2767,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_CIN1_CXCAN.csv")


# CIN2/3 vs CX CAN
data1<-subset(data,data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN2.3_CXCAN.csv")



# Normal vs CIN1,2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal vs abnormal.csv")



# Normal , CIN1 vs  CIN 2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


# Normal , CIN1   CIN 2,3, vs Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal,CIN1,2,3 vs Cx cAN.csv")

# C1,2,3 vs Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN1.2.3 vs CXCAN.csv")


# C1 vs C2,3 Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CIN1",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")



ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X2767,data=data1,plot="ROC")
ROC(form=group1~X57+X938+X2767,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN1 vs CIN 2.3 CXCAN.csv")


# Normal, CIn1 vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal,c1 vs C2.3.csv")


# Normal vs CIM1/2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal vs CIM123.csv")

# Normal,C1 vs Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal,C1 vs Cx cAN.csv")


# Normal vs CIN2/3 Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="Normal",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")



x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal vs CIN2.3 Cx cAN.csv")
#### ####
```

```r
#### 4. NEW ROC, AUC, on the number of all cases using negative polar metabolites ####
#### Part 1. drawing ROC curve using candidated metapolites under Normal vs CX CAN ####
data <- read.csv(".../polar_negative.csv")

# categorical value, "group" check 
data %>% 
  as_tibble() %>%
  group_by(group) %>% summarise(n=n())

# filtering dataset, Noraml vs CX CAN
#### CONTENT ####

data %>% 
  as_tibble() %>% 
  dplyr::filter(group == "Normal"|group == "CX CAN") %>% 
  mutate(group1 = ifelse(group == "Normal", 0, 1)) %>% 
  select(group, group1, id, everything()) %>% 
  select(group1, cm) -> data_1 

# some candidated metabolites 
cm <- c("X57", "X51", "X938", "X928", "X957", "X318")

# set names for saving plots 
folder_name <- "..."
file_name <- "testplot"


# for iteration with candidated metabolites for drawing ROC curve
for( i in 1:length(cm) ) {
  if(i != length(cm)){
    numbering <- i
    png_name <- paste0(folder_name, file_name, "_" , numbering, ".png") 
    
    png(png_name, width = 2000, height = 1500)
    
    ROC(form = as.formula(paste(colnames(data_1)[1], "~", cm[i])), data = data_1, plot="ROC")
    # by https://www.r-bloggers.com/changing-the-variable-inside-an-r-formula/
    dev.off()
  } else {
    numbering <- i
    png_name <- paste0(folder_name, file_name, "_" , numbering, ".png") 
    png(png_name, width = 2000, height = 1500)
    ROC(form = as.formula(paste(colnames(data_1)[1], "~", cm[i])), data = data_1, plot="ROC")
    dev.off()
  }
  
}
#### <TO DO> add plot name ####
#### ####

#### <QUSTION> How to commit all combinations of multiple variables to model in just one step ####
require(MuMIn)
data(iris)

# To solve the Error in dredge(globalmodel) : 
#   'global.model''s 'na.action' argument is not set and options('na.action') is "na.omit"
options(na.action = "na.omit") 
# But it is not perfect because of changing global options, na.action. 
# Therefore Mox suggests that change the lm function's options, na.action = "na.fail"
# https://stackoverflow.com/questions/28606549/how-to-run-lm-models-using-all-possible-combinations-of-several-variables-and-a

globalmodel <- lm(Sepal.Length ~ Petal.Length + Petal.Width + Species, data = iris, na.action = "na.fail")

combinations <- dredge(globalmodel)

print(combinations)
#### This way can't fit on my question ####
#### ####

#### Part 2. Compute the AUC of a metabolite according to the number of cases between all groups and add the result ####
#### <Question> How can i filtering dataset on the number of cases using group values ####
# by https://stackoverflow.com/questions/53212822/how-to-count-all-common-occurrences-of-one-factor-between-pairwise-combinations

fruit_basket <- data.frame("fruit" = c("apple", "grapes", "banana", "grapes", "mangoes", "apple", "mangoes", "banana"),
                           "basket" = c("one", "one", "two", "two", "three", "three", "four", "four"))
library(magrittr)
library(dplyr)

# Convert words to numbers -- there has to be a better way!!!
fruit_basket %<>%
  mutate(basket = case_when(
    basket == "one" ~ 1,
    basket == "two" ~ 2,
    basket == "three" ~ 3,
    basket =="four" ~ 4
  ))

res <- crossprod(table(fruit_basket))
res[lower.tri(res, diag=T)] <- NA
fruit_basket
res



# Using rolldie https://rdrr.io/github/GabauerDavid/WVPU/man/rolldie.html
group_value = c("Normal", "CIN1", "CIN2/3", "CX CAN") # 4
group_value = c("Red", "Blue", "Yellow","Green","Black") # 5
group_value = c("apple", "grapes", "banana", "mangoes","ananas","mandarin") # 6 
group_value = c("A", "B", "C", "D","E","F", "G", "H", "I", "J") # 10 
group_value = c("A", "B", "C", "D","E","F", "G", "H", "I", "J", "K") # 11 





#### description ####
# n개의 group_value를 갖고 있다고 가정하면 
# 1 vs 1, 2 vs 1, 3 vs 1, ...., n-1 vs 1 (rep, n-1)
# 2 vs 2, 3 vs 2, 4 vs 2, ...., n-2 vs 2 (rep, n-2)
# 3 vs 3, 4 vs 3, 5 vs 3, ...., n-3 vs 3 (rep, n-3)
# ....
# round(n/2)-1 vs drop(n/2)+1 (rep, 1, this is last step in case of odd n)
# n/2 vs n/2 (rep, 1, this is last step in case of even n)
# 를 반복하고 위의 과정에서 '중복'이 없어야 함. 



#### Step 1. (rep, n-1) inner pairing하고 저장하기 ####
# a vs b, b = 1의 경우

### 1 vs 1, 4C2
combn(x = group_value, m = 2)

#### TEST k vs 1 nCk * (n-k) (k goes 1 to n-1) ####
### 2 vs 1, 4C2 * 2
h1 <- combn(x = group_value, m = 2) # 4C2
h2 <- do.call(paste, c(as.data.frame(t(h1)), sep=" plus ")) # 2개씩 뽑은 것을 하나의 string으로 합침 
h3 <- str_split(h2, pattern = " plus ", n = 2, simplify = TRUE) # 하나의 obs로 다시 분리 

filter2_1 <- matrix(sapply(h3, function(x) {which(x == group_value)}), nrow(h3), 2) # 2 equal to m in line 1360
filter2_2 = matrix(0, nrow(filter2_1), length(group_value)-2) # 2 equal to m in line 160

for(i in 1:nrow(filter2_1)){
  # for(j in 1:ncol(h3)){
  #   filter2[i, j] = which(h3[i, j] == group_value) 
  #   
  # }
    filter2_2[i, ] = combn(x = group_value[-filter2_1[i,]], m = 1)
}

filter2_2 = matrix(sapply(filter2_2, function(x) {which(x == group_value)}), nrow(filter2_1), length(group_value)-2)



# 제대로 됐는지 check 
unique(cbind(filter2_1, filter2_2)) == cbind(filter2_1, filter2_2) # 확인


### 3 vs 1 nC3 * (n-3)
g1 <- combn(x = group_value, m = 3) # 4C2
g2 <- do.call(paste, c(as.data.frame(t(g1)), sep=" plus ")) # 2개씩 뽑은 것을 하나의 string으로 합침 
g3 <- str_split(g2, pattern = " plus ", n = 3, simplify = TRUE) # 하나의 obs로 다시 분리 

filter3_1 <- matrix(sapply(g3, function(x) {which(x == group_value)}), nrow(g3), 3) # 2 equal to m in line 1360
filter3_2 = matrix(0, nrow(filter3_1), length(group_value)-3) # 2 equal to m in line 160

for(i in 1:nrow(filter3_1)){
  # for(j in 1:ncol(h3)){
  #   filter2[i, j] = which(h3[i, j] == group_value) 
  #   
  # }
  filter3_2[i, ] = combn(x = group_value[-filter3_1[i,]], m = 1)
}

filter3_2 = matrix(sapply(filter3_2, function(x) {which(x == group_value)}), nrow(filter3_1), length(group_value)-3)

filter3_2

# 제대로 됐는지 check 
unique(cbind(filter3_1, filter3_2)) == cbind(filter3_1, filter3_2) # 확인

#### TEST 끝 ####

#### k vs 1 nCk * (n-k) (k goes 1 to n-1) ####
result_list_1 <- list()
result_list_2 <- list()
for (q in 1:length(group_value)-1) {
  
  if (q == 1) { 
    h1 <- combn(x = group_value, m = 2)
    filter2_1 <- matrix(sapply(t(h1), function(x) {which(x == group_value)}), nrow(t(h1)), ncol(t(h1))) 
    
    result_list_1[[q]] <- filter2_1
    result_list_2[[q]] <- 0
    } else { 
      
      for (k in 2:(length(group_value)-1)) {
        ### n개의 category에서 묶을 k개를 선택한 후 따로 저장하기 ### 
        # n개의 category에서 묶을 k개를 선택
        h1 <- combn(x = group_value, m = k)
        # k개를 뽑은 것을 하나의 string으로 합침 
        h2 <- do.call(paste, c(as.data.frame(t(h1)), sep=" plus "))
        # k개의 obs로 다시 분리 
        h3 <- str_split(h2, pattern = " plus ", n = k, simplify = TRUE)
        # h3의 value를 group_value의 index value로 다시 저장
        filter2_1 <- matrix(sapply(h3, function(x) {which(x == group_value)}), nrow(h3), k) 
        
        ### n개의 category에서 묶인 k개를 제외한 n-k개 중에서 하나씩 선택 ###
        filter2_2 = matrix(0, nrow(filter2_1), length(group_value)-k) # length(group_value)-k mean 'n-k'
        
        # for iteration, k개를 제외한 n-k개 중에서 하나씩 선택
        for(i in 1:nrow(filter2_1)){
          # k개를 제외 : -filter2_1[i,]]
          # 1개씩 선택 : combn(,...m = 1)
          filter2_2[i, ] = combn(x = group_value[-filter2_1[i,]], m = 1)
        }
        
        # 하나씩 선택된 값들을 group_value의 index value로 다시 저장 
        filter2_2 = matrix(sapply(filter2_2, function(x) {which(x == group_value)}), nrow(filter2_1), length(group_value)-k)
        
        # iteration이 제대로 되고 있는지 확인 + k개 선택된 값과 n-k개 남은 값이 중복되고 있는지 확인 
        # print(paste(k, sum(unique(cbind(filter2_1, filter2_2)) != cbind(filter2_1, filter2_2))))
        
        result_list_1[[k]] <- filter2_1
        result_list_2[[k]] <- filter2_2
    
    }
  }
}

# 결과 정리
# (1) k개 선택 
# (2) n-k에서 l개 선택 결과를 l개 선택 당 1행으로 분배해서 넣는게 더 나은 것 같음. 
#     이렇게 되면 '결과' 수 만큼 result_matrix를 만들어야 함. 
#     for문이 여러개 들어가겠는데? 일단 만들어보고 편집하자. 


result_list_3 = list()
result_list_3[[1]] <- result_list_1[[1]]

for(w in 2:(length(group_value)-1)){
  result_vec = c()
  for(e in 1:nrow(result_list_2[[w]])){
    if(e == 1) { 
      result_vec[ 1 : (ncol(result_list_2[[w]])*e) ] <- result_list_2[[w]][e, ]
    } else {
      result_vec[ (1+(ncol(result_list_2[[w]])*(e-1))) : (ncol(result_list_2[[w]])*e) ] <- result_list_2[[w]][e, ]
    }
  }
  result_list_3[[w]] <- result_vec
}


# 제대로 펼쳐졌는지 확인 
(nrow(result_list_2[[2]]) * ncol(result_list_2[[2]])) == length(result_list_3[[2]])
(nrow(result_list_2[[3]]) * ncol(result_list_2[[3]])) == length(result_list_3[[3]])
(nrow(result_list_2[[4]]) * ncol(result_list_2[[4]])) == length(result_list_3[[4]])
(nrow(result_list_2[[5]]) * ncol(result_list_2[[5]])) == length(result_list_3[[5]])

# result_list_1
# result_list_2[[t]]의 row만큼 result_list_1[[t]]의 row를 반복시켜야 함


# 결과는 result_list_4로 저장하고 result_list_1과 같은지 확인 후 result_list_3의 vector들과 결합할 예정 

result_list_4 <- list()
result_list_4[[1]] <- result_list_3[[1]]

for(t in 2:(length(group_value)-1)){
  
  for(y in 1:nrow(result_list_1[[t]])){
    
    if (y == 1){
      a <- matrix(rep(result_list_1[[t]][y, ], ncol(result_list_2[[t]])), ncol(result_list_2[[t]]), byrow = T) # 4는 뭐지? 
    } else {
      b <- matrix(rep(result_list_1[[t]][y, ], ncol(result_list_2[[t]])), ncol(result_list_2[[t]]), byrow = T) # 4는 뭐지? 
      a <- rbind(a, b)
      result_list_4[[t]] <- a 
      
    }
  }
}

result_list_4

result_list_5 <- list()
result_list_5[[1]] <- result_list_3[[1]]
for (u in 2:(length(group_value)-1)){
  result_list_5[[u]] <- cbind(result_list_4[[u]], result_list_3[[u]])
}

#### k vs 1 nCk * (n-k) (k goes 1 to n-1) 최종 결과 ####
result_list_5  # 경우의 수 체크까지 완료, 개수 맞음. 




#### k vs m nCk * (n-k)Cm (m goes 2 to n/2, k goes m to n-m) ####
# m이 2 이상일 때를 한번에 만들 수 있지 않을까? 

result_list_f1 <- list(0)
result_list_f2 <- list(0)
result_list_f3 <- list(0)
for (m in 2 : floor(length(group_value)/2)) { # floor : 버림 
  result_list_6 <- list(0)
  result_list_7 <- list(0)
  result_list_8 <- list(0)
  

  for ( k in m : (length(group_value)-m) ) {
    h1 <- combn(x = group_value, m = k)
    # k개를 뽑은 것을 하나의 string으로 합침 
    h2 <- do.call(paste, c(as.data.frame(t(h1)), sep=" plus "))
    # k개의 obs로 다시 분리 
    h3 <- str_split(h2, pattern = " plus ", n = k, simplify = TRUE)
    
    
    # h3의 value를 group_value의 index value로 다시 저장
    filter2_1 <- matrix(sapply(h3, function(x) {which(x == group_value)}), nrow(h3), k) 
    
    ### n개의 category에서 묶인 k개를 제외한 n-k개 중에서 하나씩 선택 ###
    filter2_2 = matrix(0, nrow(filter2_1)*choose(length(group_value)-k, m), m)
    
    # for iteration, k개를 제외한 n-k개 중에서 하나씩 선택
    for( i in 1 : nrow(filter2_1) ){
      # k개를 제외 : -filter2_1[i,]]
      # 1개씩 선택 : combn(,...m = 1)
      if ( i == 1 ) {
        filter2_2[i:nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), ] = t(combn(x = group_value[-filter2_1[i,]], m = m))
        
        a <- matrix(rep(filter2_1[i, ], nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), byrow = T)
        
      } else {
        filter2_2[ ((1+(i-1)*nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))))) : (i*nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), ] = t(combn(x = group_value[-filter2_1[i,]], m = m))  
        b <- matrix(rep(filter2_1[i, ], nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), byrow = T)
        a <- rbind(a, b)
        filter2_3 <- a
      } 
      
    }
    
    # 하나씩 선택된 값들을 group_value의 index value로 다시 저장 
    filter2_2 = matrix(sapply(filter2_2, function(x) {which(x == group_value)}), nrow(filter2_1)*choose(length(group_value)-k, m), nrow(combn(x = group_value[-filter2_1[i, ]], m = m)))
    
    
    # filter2_2의 row와 filter2_1의 row를 맞춰주기 위한 과정
    ## filter2_1의 row를 filter2_2의 한 경우의 반복 수 만큼 복사할 것
    
    
    result_list_6[[k]] <- filter2_3
    result_list_7[[k]] <- filter2_2
    
    if ((sum(filter2_3 == 0) + is.null(filter2_3) + sum(filter2_2 == 0)  +is.null(filter2_3)) > 0) {
      result_list_8[[k]] <- 0
    } else {
      result_list_8[[k]] <- cbind(filter2_3, filter2_2)
    }
    
  }
  
  result_list_f1[[m]] <- result_list_6
  result_list_f2[[m]] <- result_list_7
  result_list_f3[[m]] <- result_list_8
}

#### k vs m nCk * (n-k)Cm (m goes 2 to n/2, k goes m to n-m) 최종결과 ####
result_list_f3 # 최종 결과 


# function of all combination with comparison, proto type 
# <TO DO> 1.12. 줄 맞추기, 현재 줄이 꼬인 상태라 알아보기 힘듦 
all_comb_comparison <- function(group_value){
  result_list_1 <- list() # m == 1일 때의 결과 저장 
  result_list_2 <- list() # m == 1일 때의 결과 저장 
  
  result_list_f1 <- list(0) # != 1일 때의 결과 저장 
  result_list_f2 <- list(0) # != 1일 때의 결과 저장 
  result_list_f3 <- list(0) # != 1일 때의 결과 저장 
  
  for (m in 1 : floor(length(group_value)/2)) {
    
    if (m == 1){
      for (q in 1:length(group_value)-1) {
        
        if (q == 1) { 
          h1 <- combn(x = group_value, m = 2)
          filter2_1 <- matrix(sapply(t(h1), function(x) {which(x == group_value)}), nrow(t(h1)), ncol(t(h1))) 
          
          result_list_1[[q]] <- filter2_1
          result_list_2[[q]] <- 0
        } else { 
          
          for (k in 2:(length(group_value)-1)) {
            ### n개의 category에서 묶을 k개를 선택한 후 따로 저장하기 ### 
            # n개의 category에서 묶을 k개를 선택
            h1 <- combn(x = group_value, m = k)
            # k개를 뽑은 것을 하나의 string으로 합침 
            h2 <- do.call(paste, c(as.data.frame(t(h1)), sep=" plus "))
            # k개의 obs로 다시 분리 
            h3 <- str_split(h2, pattern = " plus ", n = k, simplify = TRUE)
            # h3의 value를 group_value의 index value로 다시 저장
            filter2_1 <- matrix(sapply(h3, function(x) {which(x == group_value)}), nrow(h3), k) 
            
            ### n개의 category에서 묶인 k개를 제외한 n-k개 중에서 하나씩 선택 ###
            filter2_2 = matrix(0, nrow(filter2_1), length(group_value)-k) # length(group_value)-k mean 'n-k'
            
            # for iteration, k개를 제외한 n-k개 중에서 하나씩 선택
            for(i in 1:nrow(filter2_1)){
              # k개를 제외 : -filter2_1[i,]]
              # 1개씩 선택 : combn(,...m = 1)
              filter2_2[i, ] = combn(x = group_value[-filter2_1[i,]], m = 1)
            }
            
            # 하나씩 선택된 값들을 group_value의 index value로 다시 저장 
            filter2_2 = matrix(sapply(filter2_2, function(x) {which(x == group_value)}), nrow(filter2_1), length(group_value)-k)
            
            # iteration이 제대로 되고 있는지 확인 + k개 선택된 값과 n-k개 남은 값이 중복되고 있는지 확인 
            # print(paste(k, sum(unique(cbind(filter2_1, filter2_2)) != cbind(filter2_1, filter2_2))))
            
            result_list_1[[k]] <- filter2_1
            result_list_2[[k]] <- filter2_2
            
          }
        }
      }
  
      result_list_3 = list()
      result_list_3[[1]] <- result_list_1[[1]]
      
      for(w in 2:(length(group_value)-1)){
        result_vec = c()
        for(e in 1:nrow(result_list_2[[w]])){
          if(e == 1) { 
            result_vec[ 1 : (ncol(result_list_2[[w]])*e) ] <- result_list_2[[w]][e, ]
          } else {
            result_vec[ (1+(ncol(result_list_2[[w]])*(e-1))) : (ncol(result_list_2[[w]])*e) ] <- result_list_2[[w]][e, ]
          }
        }
        result_list_3[[w]] <- result_vec
      }
      
      
      result_list_4 <- list()
      result_list_4[[1]] <- result_list_3[[1]]
      
      for(t in 2:(length(group_value)-1)){
        
        for(y in 1:nrow(result_list_1[[t]])){
          
          if (y == 1){
            a <- matrix(rep(result_list_1[[t]][y, ], ncol(result_list_2[[t]])), ncol(result_list_2[[t]]), byrow = T) # 4는 뭐지? 
          } else {
            b <- matrix(rep(result_list_1[[t]][y, ], ncol(result_list_2[[t]])), ncol(result_list_2[[t]]), byrow = T) # 4는 뭐지? 
            a <- rbind(a, b)
            result_list_4[[t]] <- a 
            
          }
        }
      }
      
      result_list_4
      
      result_list_5 <- list()
      result_list_5[[1]] <- result_list_3[[1]]
      for (u in 2:(length(group_value)-1)){
        result_list_5[[u]] <- cbind(result_list_4[[u]], result_list_3[[u]])
      }
      
    } else {
      result_list_6 <- list(0)
      result_list_7 <- list(0)
      result_list_8 <- list(0)
      
      for ( k in m : (length(group_value)-m) ) {
      h1 <- combn(x = group_value, m = k)
      # k개를 뽑은 것을 하나의 string으로 합침 
      h2 <- do.call(paste, c(as.data.frame(t(h1)), sep=" plus "))
      # k개의 obs로 다시 분리 
      h3 <- str_split(h2, pattern = " plus ", n = k, simplify = TRUE)
      
      
      # h3의 value를 group_value의 index value로 다시 저장
      filter2_1 <- matrix(sapply(h3, function(x) {which(x == group_value)}), nrow(h3), k) 
      
      ### n개의 category에서 묶인 k개를 제외한 n-k개 중에서 하나씩 선택 ###
      filter2_2 = matrix(0, nrow(filter2_1)*choose(length(group_value)-k, m), m)
      
      # for iteration, k개를 제외한 n-k개 중에서 하나씩 선택
      for( i in 1 : nrow(filter2_1) ){
        # k개를 제외 : -filter2_1[i,]]
        # 1개씩 선택 : combn(,...m = 1)
        if ( i == 1 ) {
          filter2_2[i:nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), ] = t(combn(x = group_value[-filter2_1[i,]], m = m))
          
          a <- matrix(rep(filter2_1[i, ], nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), byrow = T)
          
        } else {
          filter2_2[ ((1+(i-1)*nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))))) : (i*nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), ] = t(combn(x = group_value[-filter2_1[i,]], m = m))  
          b <- matrix(rep(filter2_1[i, ], nrow(t(combn(x = group_value[-filter2_1[i,]], m = m)))), nrow(t(combn(x = group_value[-filter2_1[i,]], m = m))), byrow = T)
          a <- rbind(a, b)
          filter2_3 <- a
        } 
        
      }
      
      # 하나씩 선택된 값들을 group_value의 index value로 다시 저장 
      filter2_2 = matrix(sapply(filter2_2, function(x) {which(x == group_value)}), nrow(filter2_1)*choose(length(group_value)-k, m), nrow(combn(x = group_value[-filter2_1[i, ]], m = m)))
      
      
      # filter2_2의 row와 filter2_1의 row를 맞춰주기 위한 과정
      ## filter2_1의 row를 filter2_2의 한 경우의 반복 수 만큼 복사할 것
      
      
      result_list_6[[k]] <- filter2_3
      result_list_7[[k]] <- filter2_2
      
      if ((sum(filter2_3 == 0) + is.null(filter2_3) + sum(filter2_2 == 0)  +is.null(filter2_3)) > 0) {
        result_list_8[[k]] <- 0
      } else {
        result_list_8[[k]] <- cbind(filter2_3, filter2_2)
      }
      
      }
    
    result_list_f1[[m]] <- result_list_6
    result_list_f2[[m]] <- result_list_7
    result_list_f3[[m]] <- result_list_8
    }
  }
  
  result_list_f3[[1]] <- result_list_5
  result_list_final <- result_list_f3
  
  return(result_list_final)  
}

  
all_comb_comparison(group_value) # 확인. 1.12 문제없이 돌아감. 



#### ####





x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal_CXCAN_auc.csv")

# Normal vs CIN1
data1<-subset(data,data$group=="Normal"|data$group=="CIN1")
data1$group1<-ifelse(data1$group=="CIN1",1,0)

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal_CIN1.csv")


# Normal vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal_CIN2.3.csv")

# Normal,C1 vs CIN2/3,cx can
data1<-data
data1$group1<-ifelse(data1$group=="CIN2/3"|data1$group=="CX CAN",1,0)
x<-c()
auc<-c()

library(Epi)
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_Normal c1_CIN2.3 cx.csv")

# CIN1 vs CIN2/3
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_CIN1_CIN2.3.csv")

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

install.packages("MASS")
library(Epi)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X2767,data=data1,plot="ROC")
ROC(form=group1~X57+X938+X2767,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_negative_CIN1_CXCAN.csv")


# CIN2/3 vs CX CAN
data1<-subset(data,data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN2.3_CXCAN.csv")



# Normal vs CIN1,2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal vs abnormal.csv")



# Normal , CIN1 vs  CIN 2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


# Normal , CIN1   CIN 2,3, vs Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_Normal,CIN1,2,3 vs Cx cAN.csv")

# C1,2,3 vs Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN1.2.3 vs CXCAN.csv")


# C1 vs C2,3 Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CIN1",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")



ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X2767,data=data1,plot="ROC")
ROC(form=group1~X57+X938+X2767,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_negative_CIN1 vs CIN 2.3 CXCAN.csv")


# Normal, CIn1 vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal,c1 vs C2.3.csv")


# Normal vs CIM1/2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal vs CIM123.csv")

# Normal,C1 vs Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal,C1 vs Cx cAN.csv")


# Normal vs CIN2/3 Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="Normal",0,1)

ROC(form=group1~X57,data=data1,plot="ROC")
ROC(form=group1~X51,data=data1,plot="ROC")
ROC(form=group1~X938,data=data1,plot="ROC")
ROC(form=group1~X928,data=data1,plot="ROC")
ROC(form=group1~X957,data=data1,plot="ROC")
ROC(form=group1~X318,data=data1,plot="ROC")
ROC(form=group1~X57+X51+X938+X928+X957+X318,data=data1,plot="ROC")



x<-c()
auc<-c()
for( i in 3:2565){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_ne_Normal vs CIN2.3 Cx cAN.csv")
#### ####
```


```r
#### 5. OLD ROC, AUC, on the number of all cases using polar positive metabolites ####
rm(list=ls())

data<-read.csv(".../polar_positive.csv")

# Normal vs CX cAN
data1<-subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

library(Epi)

x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_positive_Normal_CXCAN_auc.csv")

# Normal vs CIN1
data1<-subset(data,data$group=="Normal"|data$group=="CIN1")
data1$group1<-ifelse(data1$group=="CIN1",1,0)

x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal_CIN1.csv")


# Normal vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)

ROC(form=group1~X1538,data=data1,plot="ROC")
ROC(form=group1~X1923,data=data1,plot="ROC")
ROC(form=group1~X1696,data=data1,plot="ROC")
ROC(form=group1~X1619,data=data1,plot="ROC")
ROC(form=group1~X1538+X1923+X1696+X1619,data=data1,plot="ROC")

library(Epi)

ROC(form=group1~X770,data=data1,plot="ROC")
ROC(form=group1~X2020,data=data1,plot="ROC")
ROC(form=group1~X1723,data=data1,plot="ROC")
ROC(form=group1~X770+X2020+X1723,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_positive_Normal_CIN2.3.csv")

# CIN1 vs CIN2/3
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)

ROC(form=group1~X1538,data=data1,plot="ROC")
ROC(form=group1~X1923,data=data1,plot="ROC")
ROC(form=group1~X1696,data=data1,plot="ROC")
ROC(form=group1~X1619,data=data1,plot="ROC")
ROC(form=group1~X1538+X1923+X1696+X1619,data=data1,plot="ROC")

ROC(form=group1~X770,data=data1,plot="ROC")
ROC(form=group1~X2020,data=data1,plot="ROC")
ROC(form=group1~X1723,data=data1,plot="ROC")
ROC(form=group1~X770+X2020+X1723,data=data1,plot="ROC")



x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_positive_CIN1_CIN2.3.csv")

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,".../polar_positive_CIN1_CXCAN.csv")


# CIN2/3 vs CX CAN
data1<-subset(data,data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_CIN2.3_CXCAN.csv")



# Normal vs CIN1,2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal vs abnormal.csv")



# Normal , CIN1 vs  CIN 2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)


x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


# Normal , CIN1   CIN 2,3, vs Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal,CIN1,2,3 vs Cx cAN.csv")

# C1,2,3 vs Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_CIN1.2.3 vs CXCAN.csv")


# C1 vs C2,3 Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CIN1",0,1)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_CIN1 vs CIN 2.3 CXCAN.csv")

options(java.parameters = "-Xmx4g")
polar_negative<-read.csv(".../polar_negative.csv")



# Normal, CIn1 vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)


ROC(form=group1~X1538,data=data1,plot="ROC")
ROC(form=group1~X1923,data=data1,plot="ROC")
ROC(form=group1~X1696,data=data1,plot="ROC")
ROC(form=group1~X1619,data=data1,plot="ROC")
ROC(form=group1~X1538+X1923+X1696+X1619,data=data1,plot="ROC")


ROC(form=group1~X770,data=data1,plot="ROC")
ROC(form=group1~X2020,data=data1,plot="ROC")
ROC(form=group1~X1723,data=data1,plot="ROC")
ROC(form=group1~X770+X2020+X1723,data=data1,plot="ROC")

x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal,c1 vs C2.3.csv")


# Normal vs CIM1/2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal vs CIM123.csv")

# Normal,C1 vs Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal,C1 vs Cx cAN.csv")


# Normal vs CIN2/3 Cx cAN

data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="Normal",0,1)


ROC(form=group1~X1538,data=data1,plot="ROC")
ROC(form=group1~X1923,data=data1,plot="ROC")
ROC(form=group1~X1696,data=data1,plot="ROC")
ROC(form=group1~X1619,data=data1,plot="ROC")
ROC(form=group1~X1538+X1923+X1696+X1619,data=data1,plot="ROC")

ROC(form=group1~X770,data=data1,plot="ROC")
ROC(form=group1~X2020,data=data1,plot="ROC")
ROC(form=group1~X1723,data=data1,plot="ROC")
ROC(form=group1~X770+X2020+X1723,data=data1,plot="ROC")


x<-c()
auc<-c()
for( i in 3:1928){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,".../polar_positive_Normal vs CIN2.3 Cx cAN.csv")
#### ####
```

```r
#### 6. OLD mutate VIP value with negative and positive polar ####

polar_negative<-read.csv(".../polar_negative.csv")

polar_negative1<-polar_negative[-203,]

x<-c()
p<-c()
vip<-c()

for( i in 3:2565){
  x[i]<-colnames(polar_negative1[i])
  p[i]<-round(kruskal.test(polar_negative1[,i]~polar_negative1$group)$p.value,5)
  vip[i]<-polar_negative[203,i]
  data<-data.frame(x,p,vip)
}

write.csv(data,".../polar_negative_kw_VIP.csv")

polar_positive<-read.csv(".../polar_positive.csv")

polar_positive1<-polar_positive[-206,]

x<-c()
p<-c()
vip<-c()

for( i in 3:1928){
  x[i]<-colnames(polar_positive1[i])
  p[i]<-round(kruskal.test(polar_positive1[,i]~polar_positive1$group)$p.value,5)
  vip[i]<-polar_positive[206,i]
  data<-data.frame(x,p,vip)
}

write.csv(data,".../polar_positive_kw_VIP.csv")
#### ####
```
