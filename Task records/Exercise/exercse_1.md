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




#### ####


# MetaboAnalystR installation
## Step 1. 
install.packages("pacman")

library(pacman)

pacman::p_load(Rserve, ellipse, scatterplot3d, Cairo, randomForest, caTools, e1071, som, impute, pcaMethods, RJSONIO, ROCR, globaltest, GlobalAncova, Rgraphviz, preprocessCore, genefilter, pheatmap, SSPA, sva, Rcpp, pROC, data.table, limma, car, fitdistrplus, lars, Hmisc, magrittr, methods, xtable, pls, caret, lattice, igraph, gplots, KEGGgraph, reshape, RColorBrewer, tibble, siggenes, plotly, xcms, CAMERA, fgsea, MSnbase, BiocParallel, metap, reshape2, scales)


## Step 2.
# Step 1: Install devtools
install.packages("devtools")
library(devtools)

# Step 2: Install MetaboAnalystR without documentation
devtools::install_github("xia-lab/MetaboAnalystR", build = TRUE, build_opts = c("--no-resave-data", "--no-manual", "--no-build-vignettes"))

# 참고할 sites
https://academic.oup.com/bioinformatics/article/34/24/4313/5046255
https://github.com/xia-lab/MetaboAnalystR'
https://en.wikipedia.org/wiki/MetaboAnalyst
https://rdrr.io/github/xia-lab/MetaboAnalystR/


```
