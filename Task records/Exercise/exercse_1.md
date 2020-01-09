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
ANCHOR 
PLEASE ADD CODE FOR INSTALL "MetaboAnalystR"
```


```r

#### 2. OLD Draw ROC curve using identified negative polar metabolites ####
#### Part 1. ####
# This Part use the identified metabolites. So, actually this part should move to behind part 2 in "2. OLD section".
# But i don't want to mess this "OLD" legacy. Therefore I do not handle this.

data <- read.csv("...negative_polar.csv")

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
polar_negative<-read.csv("...polar_negative.csv")


x<-c()
p<-c()

for( i in 3:2565){
  x[i]<-colnames(polar_negative[i])
  p[i]<-round(kruskal.test(polar_negative[,i]~polar_negative$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,"...polar_negative_kw.csv")

polar_positive<-read.csv("...polar_positive.csv")

x<-c()
p<-c()
for( i in 3:1928){
  x[i]<-colnames(polar_positive[i])
  p[i]<-round(kruskal.test(polar_positive[,i]~polar_positive$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,"...polar_positive_kw.csv")


lipid_positive<-read.csv("...lipid_positive.csv")

x<-c()
p<-c()
for( i in 3:4357){
  x[i]<-colnames(lipid_positive[i])
  p[i]<-round(kruskal.test(lipid_positive[,i]~lipid_positive$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,"...lipid_positive_kw.csv")

lipid_negative<-read.csv("...lipid_negative.csv")

x<-c()
p<-c()
for( i in 3:3840){
  x[i]<-colnames(lipid_negative[i])
  p[i]<-round(kruskal.test(lipid_negative[,i]~lipid_negative$group)$p.value,5)
  data<-data.frame(x,p)
}

write.csv(data,"...llipid_negative_kw.csv")

#### ####

#### 2. New Draw ROC curve using identified negative polar metabolites #####
#### Part 1. #### 
# load csv file and store to 'data'
data <- as.tibble(read.csv("...negative_polar.csv"))

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
polar_negative <- read.csv("...polar_negative.csv")
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
write.csv(kruskal_test(polar_negative, 3, length(polar_negative)),"...polar_negative_kw.csv")

# This is the process of making a function and checking the results
# In now, use the function for more smart

# polar_positive dataset 
polar_positive <- read.csv("...polar_positive.csv")
write.csv(kruskal_test(polar_positive, 3, length(polar_positive)),"...polar_positive_kw.csv")

# lipid_positive dataset
lipid_positive <- read.csv("...lipid_positive.csv")
write.csv(kruskal_test(lipid_positive, 3, length(lipid_positive)),"C:...lipid_positive_kw.csv")

# lipid_negative dataset
lipid_negative <- read.csv("...lipid_negative.csv")
write.csv(kruskal_test(lipid_negative, 3, length(lipid_negative)),"...llipid_negative_kw.csv")

# It seems like newbie's coding but very intuitive style
# However it needs to commit more efficient using 'user def function' to reduce repeatation code 

# <TO DO> def function and test 
# <END> I create function, kruskal_test. The messy code was neatly organized with a kruskal_test function
#### ####

  


#### 3. OLD Heatmap plot and HCA using identified negative polar metabolites ####
# HCA means 'Hierarchical cluster analysis'

#### Part 1. Draw heatmap plot #### 
rm(list=ls())

data<-read.csv("...polar_negative_for_heatmap.csv")
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


#### 3. NEW Heatmap plot and HCA using identified negative polar metabolites ####
# HCA means 'Hierarchical cluster analysis'

#### Part 1. Draw heatmap plot #### 

# polar_negative_for_heatmap.csv과 polar_negative의 차이?
# kruskal test 후 0.03 이하의 p-value를 갖는 X만을 take한 것
# 그렇다면 .csv file을 따로 만들지 않고 polar_negative를 편집해서 하는게 더 나을 것. 

data <- read.csv("...polar_negative.csv")
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

# 일단 last_res로 결과 저장함.
# <HERE!!> 확인해볼 것
# heat_map용으로 편집된 data_c와 last_res의 결과 확인 
data_c <- read.csv("...polar_negative_for_heatmap.csv")
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


# legacy code 
#### Part 1. Draw heatmap plot #### 
rm(list=ls())

data<-read.csv("...polar_negative_for_heatmap.csv")
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






#################################################################################################################

# AUC 洹몃━湲?

rm(list=ls())

data<-read.csv("...polar_negative.csv")

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

write.csv(data2,"...polar_negative_Normal_CXCAN_auc.csv")

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
write.csv(data2,"...polar_negative_Normal_CIN1.csv")


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

write.csv(data2,"...polar_negative_Normal_CIN2.3.csv")

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

write.csv(data2,"...polar_negative_Normal c1_CIN2.3 cx.csv")

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

write.csv(data2,"...polar_negative_CIN1_CIN2.3.csv")

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

write.csv(data2,"...polar_negative_CIN1_CXCAN.csv")


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
write.csv(data2,"...polar_negative_CIN2.3_CXCAN.csv")



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
write.csv(data2,"...polar_negative_Normal vs abnormal.csv")



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
write.csv(data2,"...polar_negative_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


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
write.csv(data2,"...polar_negative_Normal,CIN1,2,3 vs Cx cAN.csv")

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
write.csv(data2,"...polar_negative_CIN1.2.3 vs CXCAN.csv")


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
write.csv(data2,"...polar_negative_CIN1 vs CIN 2.3 CXCAN.csv")


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
write.csv(data2,"...polar_ne_Normal,c1 vs C2.3.csv")


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
write.csv(data2,"...polar_ne_Normal vs CIM123.csv")

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
write.csv(data2,"...polar_ne_Normal,C1 vs Cx cAN.csv")


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
write.csv(data2,"...polar_ne_Normal vs CIN2.3 Cx cAN.csv")

###################################################

rm(list=ls())

data<-read.csv("...polar_positive.csv")

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

write.csv(data2,"...polar_positive_Normal_CXCAN_auc.csv")

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
write.csv(data2,"...polar_positive_Normal_CIN1.csv")


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

write.csv(data2,"...polar_positive_Normal_CIN2.3.csv")

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

write.csv(data2,"...polar_positive_CIN1_CIN2.3.csv")

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

write.csv(data2,"...polar_positive_CIN1_CXCAN.csv")


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
write.csv(data2,"...polar_positive_CIN2.3_CXCAN.csv")



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
write.csv(data2,"...polar_positive_Normal vs abnormal.csv")



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
write.csv(data2,"...polar_positive_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


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
write.csv(data2,"...polar_positive_Normal,CIN1,2,3 vs Cx cAN.csv")

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
write.csv(data2,"...polar_positive_CIN1.2.3 vs CXCAN.csv")


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
write.csv(data2,"...polar_positive_CIN1 vs CIN 2.3 CXCAN.csv")

options(java.parameters = "-Xmx4g")
polar_negative<-read.csv("...polar_negative.csv")




library(Epi)

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
write.csv(data2,"...polar_positive_Normal,c1 vs C2.3.csv")


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
write.csv(data2,"...polar_positive_Normal vs CIM123.csv")

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
write.csv(data2,"...polar_positive_Normal,C1 vs Cx cAN.csv")


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
write.csv(data2,"...polar_positive_Normal vs CIN2.3 Cx cAN.csv")




############################################# with VIP


polar_negative<-read.csv("...polar_negative.csv")

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

write.csv(data,"...polar_negative_kw_VIP.csv")

polar_positive<-read.csv("...polar_positive.csv")

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

write.csv(data,"...polar_positive_kw_VIP.csv")



##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


rm(list=ls())


data<-read.csv("...polar_negative_for_heatmap_se1.csv")


rownames(data)<-data[,1]
data<-data[,-1]

library(gplots)


heatmap2<-data[c("51","57","284","318","327","399","792","928","938","957","967","1311","1312","1588","1602","2767","3047","3053","3368","3803","3829","4026"),]
heatmap2<-data[c("51","57","93","278","284","318","327","392","399","436","486","504","792","850","897","906","925","928","938","957","967","1047","1068","1074","1084","1092","1118","1250","1276","1311","1312","1354","1434","1454","1555","1588","1602","1610","1611","1685","1760","1841","1937","1947","2031","2092","2103","2111","2145","2204","2251","2320","2331","2382","2387","2429","2436","2443","2451","2491","2652","2663","2671","2710","2713","2716","2729","2738","2754","2767","2791","2799","2904","2930","2931","2947","2965","2988","2995","3000","3002","3008","3009","3021","3028","3047","3052","3053","3057","3061","3072","3102","3129","3142","3217","3218","3271","3292","3293","3302","3338","3347","3349","3350","3353","3354","3364","3368","3386","3417","3418","3423","3468","3470","3499","3501","3505","3506","3510","3531","3532","3578","3582","3589","3600","3601","3609","3618","3627","3642","3648","3650","3697","3700","3707","3724","3727","3744","3759","3763","3771","3803","3810","3818","3828","3829","3843","3852","3857","3872","3882","3885","3900","3946","3956","3971","3972","3974","3975","3991","4005","4007","4013","4026","4028","4037","4041","4064","4068","4072","4073","4076","4094","4102","4114","4128","4136","4148","4153","4154","4158","4169","4172","4179","4181","4183","4195","4202"),]
heatmap2<-data[c("51","57","64","65","66","198","221","268","276","278","284","307","308","318","327","348","392","399","412","659","745","749","777","778","792","821","860","877","888","897","928","938","957","967","995","1030","1047","1068","1074","1084","1118","1141","1154","1230","1311","1312","1354","1401","1419","1434","1454","1483","1537","1555","1588","1602","1635","1636","1748","1760","1820","1841","1855","1886","1914","1918","1937","1947","1989","2012","2111","2145","2159","2179","2214","2274","2286","2300","2320","2330","2331","2337","2359","2375","2382","2387","2432","2451","2491","2606","2619","2635","2652","2663","2671","2699","2713","2716","2717","2729","2767","2785","2799","2892","2904","2914","2930","2931","2947","2988","3000","3008","3009","3021","3072","3081","3082","3088","3102","3129","3142","3188","3199","3207","3216","3217","3218","3225","3257","3259","3263","3271","3286","3292","3293","3302","3307","3338","3347","3348","3349","3350","3353","3354","3364","3368","3378","3386","3417","3423","3429","3462","3468","3470","3475","3499","3501","3502","3505","3506","3510","3531","3532","3578","3582","3589","3600","3601","3609","3618","3620","3621","3627","3638","3639","3642","3648","3650","3697","3707","3724","3727","3741","3744","3759","3763","3771","3788","3803","3810","3818","3828","3829","3843","3847","3852","3857","3872","3882","3885","3889","3894","3900","3921","3930","3940","3946","3948","3956","3971","3972","3974","3975","3991","4005","4007","4013","4026","4028","4037","4041","4058","4064","4068","4070","4072","4073","4076","4086","4102","4106","4108","4114","4126","4128","4136","4140","4147","4148","4153","4154","4158","4166","4169","4172","4176","4179","4181","4183","4184","4195","4202"),]
heatmap2<-data[c("51","57","278","284","318","327","392","399","792","897","928","938","957","967","1047","1068","1074","1084","1118","1311","1312","1354","1434","1454","1555","1588","1602","1760","1841","1937","1947","2111","2145","2320","2331","2382","2387","2451","2491","2652","2663","2671","2713","2716","2729","2767","2799","2904","2930","2931","2947","2988","3000","3008","3009","3021","3072","3102","3129","3142","3217","3218","3271","3292","3293","3302","3338","3347","3349","3350","3353","3354","3364","3368","3386","3417","3423","3468","3470","3499","3501","3505","3506","3510","3531","3532","3578","3582","3589","3600","3601","3609","3618","3627","3642","3648","3650","3697","3707","3724","3727","3744","3759","3763","3771","3803","3810","3818","3828","3829","3843","3852","3857","3872","3882","3885","3900","3946","3956","3971","3972","3974","3975","3991","4005","4007","4013","4026","4028","4037","4041","4064","4068","4072","4073","4076","4102","4114","4128","4136","4148","4153","4154","4158","4169","4172","4179","4181","4183","4195","4202"),]
heatmap2<-data[c("51","57","284","318","327","399","792","928","938","957","967","1311","1312","1588","1602","2767","3368","3803","3829","4026"),]

wssplot <- function(data, nc=205, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}

wssplot(heatmap2, nc=14)

d <- dist(heatmap2, method = "euclidean") # Euclidean distance matrix.
H.fit <- hclust(d)
plot(H.fit)
rect.hclust(H.fit, k=3, border="red") 



heatmap2<-as.matrix(scale(log(heatmap2))) #?젙洹쒗솕
for(i in 1:202){heatmap2[,i]<-ifelse(heatmap2[,i]<0,0,as.numeric(heatmap2[,i]))}

colCols <- ifelse(grepl("Normal",colnames(heatmap2)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap2)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap2)),"red","black")))))
heatmap.2(heatmap2, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))
par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)



hc.rows <- hclust(dist(heatmap2))
plot(hc.rows)
table(cutree(hc.rows,k=5))

hc.cols <- hclust(dist(t(heatmap1)))
plot(hc.cols)
table(cutree(hc.cols,k=3))


















rm(list=ls())

data<-read.csv("...polar_positive_for_heatmap_se1.csv")
data<-read.csv("...positive_polar.csv")

summary(data)
dat<-data[,-1:-2]


rownames(data)<-data[,1]
data<-data[,-1]

library(gplots)
head(data)

heatmap2<-dat[,c("X522","X781","X1213","X1227","X1538","X1593","X1605","X1619","X1696","X1741","X1769","X1792","X1886","X1888","X1923","X1939","X1981","X1992","X2474")]
heatmap2<-data[,c("X522","X665","X781","X895","X1149","X1168","X1209","X1213","X1215","X1225","X1227","X1308","X1315","X1322","X1349","X1383","X1458","X1527","X1538","X1593","X1605","X1606","X1619","X1679","X1696","X1735","X1741","X1742","X1769","X1784","X1792","X1866","X1886","X1888","X1923","X1928","X1939","X1974","X1981","X1992","X2020","X2063","X2182","X2400","X2442","X2474","X2608")]
heatmap2<-data[,c("X317","X741","X769","X770","X771","X895","X965","X1215","X1225","X1227","X1349","X1383","X1527","X1538","X1605","X1606","X1619","X1664","X1666","X1696","X1712","X1718","X1723","X1730","X1735","X1741","X1742","X1789","X1792","X1793","X1853","X1888","X1904","X1923","X1939","X1974","X1980","X1981","X1992","X2020","X2033","X2053","X2109","X2166","X2384","X2400","X2442","X2524","X2588","X2713","X2776","X2799","X2847","X2868","X2915","X2925","X3083","X3185","X3204","X3424","X3425","X3456","X3458")]
heatmap2<-data[,c("X895","X1215","X1225","X1227","X1349","X1383","X1527","X1538","X1605","X1606","X1619","X1696","X1735","X1741","X1742","X1792","X1888","X1923","X1939","X1974","X1981","X1992","X2020","X2400","X2442")]
heatmap2<-data[,c("X1227","X1538","X1605","X1619","X1696","X1741","X1792","X1888","X1923","X1939","X1981","X1992")]

heatmap2<-data[c("522","781","1213","1227","1538","1593","1605","1619","1696","1741","1769","1792","1886","1888","1923","1939","1981","1992","2474"),]
heatmap2<-data[c("522","665","781","895","1149","1168","1209","1213","1215","1225","1227","1308","1315","1322","1349","1383","1458","1527","1538","1593","1605","1606","1619","1679","1696","1735","1741","1742","1769","1784","1792","1866","1886","1888","1923","1928","1939","1974","1981","1992","2020","2063","2182","2400","2442","2474","2608"),]
heatmap2<-data[c("317","741","769","770","771","895","965","1215","1225","1227","1349","1383","1527","1538","1605","1606","1619","1664","1666","1696","1712","1718","1723","1730","1735","1741","1742","1789","1792","1793","1853","1888","1904","1923","1939","1974","1980","1981","1992","2020","2033","2053","2109","2166","2384","2400","2442","2524","2588","2713","2776","2799","2847","2868","2915","2925","3083","3185","3204","3424","3425","3456","3458"),]
heatmap2<-data[c("895","1215","1225","1227","1349","1383","1527","1538","1605","1606","1619","1696","1735","1741","1742","1792","1888","1923","1939","1974","1981","1992","2020","2400","2442"),]
heatmap2<-data[c("1227","1538","1605","1619","1696","1741","1792","1888","1923","1939","1981","1992"),]

wssplot <- function(data, nc=205, seed=1234){
  wss <- (nrow(data)-1)*sum(apply(data,2,var))
  for (i in 2:nc){
    set.seed(seed)
    wss[i] <- sum(kmeans(data, centers=i)$withinss)}
  plot(1:nc, wss, type="b", xlab="Number of Clusters",
       ylab="Within groups sum of squares")}

wssplot(heatmap2, nc=14)

d <- dist(heatmap2, method = "euclidean") # Euclidean distance matrix.
H.fit <- hclust(d)
plot(H.fit)
rect.hclust(H.fit, k=3, border="red") 



head(heatmap2)

heatmap2<-as.matrix(scale(log(heatmap2))) #?젙洹쒗솕
for(i in 1:202){heatmap2[,i]<-ifelse(heatmap2[,i]<0,0,as.numeric(heatmap2[,i]))}

colCols <- ifelse(grepl("Normal",colnames(heatmap2)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap2)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap2)),"red","black")))))
heatmap.2(heatmap2, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))
par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)

hc.rows <- hclust(dist(heatmap2))
plot(hc.rows)
table(cutree(hc.rows,k=5))


#####################################################################################




install.packages("PMCMR")
require(PMCMR)


polar_negative<-read.csv("...polar_negative.csv")

polar_negative<-polar_negative[-203,]

table(polar_negative$group)

posthoc.kruskal.dunn.test(polar_negative$X51, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X57, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X284, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X381, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X327, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X399, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X792, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X928, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X938, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X957, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X967, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X1311, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X1312, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X1588, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X1602, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X2767, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X3047, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X3053, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X3368, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X3803, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X3829, polar_negative$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_negative$X4026, polar_negative$group, p.adjust.method="bonferroni")

library(ggplot2)

ggplot(polar_negative, aes(x=group,y=X51,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_51.png"))

ggplot(polar_negative, aes(x=group,y=X57,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_57.png"))

ggplot(polar_negative, aes(x=group,y=X284,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_284.png"))

ggplot(polar_negative, aes(x=group,y=X318,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_318.png"))

ggplot(polar_negative, aes(x=group,y=X327,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_327.png"))

ggplot(polar_negative, aes(x=group,y=X399,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_399.png"))

ggplot(polar_negative, aes(x=group,y=X792,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_792.png"))

ggplot(polar_negative, aes(x=group,y=X928,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("..negative_928.png"))

ggplot(polar_negative, aes(x=group,y=X938,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_938.png"))

ggplot(polar_negative, aes(x=group,y=X957,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_957.png"))

ggplot(polar_negative, aes(x=group,y=X967,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_967.png"))

ggplot(polar_negative, aes(x=group,y=X1311,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_1311.png"))

ggplot(polar_negative, aes(x=group,y=X1312,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_1312.png"))

ggplot(polar_negative, aes(x=group,y=X1588,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_1588.png"))

ggplot(polar_negative, aes(x=group,y=X1602,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_1602.png"))

ggplot(polar_negative, aes(x=group,y=X2767,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_2767.png"))

ggplot(polar_negative, aes(x=group,y=X3047,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_3047.png"))

ggplot(polar_negative, aes(x=group,y=X3053,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_3053.png"))

ggplot(polar_negative, aes(x=group,y=X3368,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_3368.png"))

ggplot(polar_negative, aes(x=group,y=X3803,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_3803.png"))

ggplot(polar_negative, aes(x=group,y=X3829,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_3829.png"))

ggplot(polar_negative, aes(x=group,y=X4026,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...negative_4026.png"))



#####################################################################################




install.packages("PMCMR")
require(PMCMR)


polar_positive<-read.csv("...polar_positive.csv")

polar_positive<-polar_positive[-206,]

table(polar_positive$group)


posthoc.kruskal.dunn.test(polar_positive$X522, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X781, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1213, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1227, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1538, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1593, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1605, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1619, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1696, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1741, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1769, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1792, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1886, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1888, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1923, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1939, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1981, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X1992, polar_positive$group, p.adjust.method="bonferroni")
posthoc.kruskal.dunn.test(polar_positive$X2474, polar_positive$group, p.adjust.method="bonferroni")

library(ggplot2)

ggplot(polar_positive, aes(x=group,y=X522,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_522.png"))

ggplot(polar_positive, aes(x=group,y=X781,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_781.png"))

ggplot(polar_positive, aes(x=group,y=X1213,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1213.png"))

ggplot(polar_positive, aes(x=group,y=X1227,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1227.png"))


ggplot(polar_positive, aes(x=group,y=X1538,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1538.png"))


ggplot(polar_positive, aes(x=group,y=X1593,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1593.png"))


ggplot(polar_positive, aes(x=group,y=X1605,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1605.png"))


ggplot(polar_positive, aes(x=group,y=X1619,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1619.png"))


ggplot(polar_positive, aes(x=group,y=X1696,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1696.png"))


ggplot(polar_positive, aes(x=group,y=X1741,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1741.png"))


ggplot(polar_positive, aes(x=group,y=X1769,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1769.png"))


ggplot(polar_positive, aes(x=group,y=X1792,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1792.png"))


ggplot(polar_positive, aes(x=group,y=X1886,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1886.png"))


ggplot(polar_positive, aes(x=group,y=X1888,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1888.png"))


ggplot(polar_positive, aes(x=group,y=X1923,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1923.png"))


ggplot(polar_positive, aes(x=group,y=X1939,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1939.png"))


ggplot(polar_positive, aes(x=group,y=X1981,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1981.png"))


ggplot(polar_positive, aes(x=group,y=X1992,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_1992.png"))


ggplot(polar_positive, aes(x=group,y=X2474,fill=group))+geom_boxplot()+theme_bw()+
  theme(legend.position='none')+scale_x_discrete(limits=c("Normal","CIN1","CIN2/3","CX CAN"))+
  theme(text = element_text(size=20),axis.title.x=element_blank())
ggsave(sprintf("...positive_2474.png"))



#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################

# AUC 洹몃━湲?

rm(list=ls())

install.packages("Epi")
library(Epi)

data<-read.csv("...lipid_negative.csv")

# Normal vs CX cAN
data1<-subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_ne_Normal_CXCAN_auc.csv")

# Normal vs CIN1
data1<-subset(data,data$group=="Normal"|data$group=="CIN1")
data1$group1<-ifelse(data1$group=="CIN1",1,0)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal_CIN1.csv")


# Normal vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_ne_Normal_CIN2.3.csv")

# CIN1 vs CIN2/3
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)


x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_ne_CIN1_CIN2.3.csv")

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_ne_CIN1_CXCAN.csv")


# CIN2/3 vs CX CAN
data1<-subset(data,data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_CIN2.3_CXCAN.csv")



# Normal vs CIN1,2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal vs abnormal.csv")



# Normal , CIN1 vs  CIN 2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


# Normal , CIN1   CIN 2,3, vs Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal,CIN1,2,3 vs Cx cAN.csv")

# C1,2,3 vs Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_CIN1.2.3 vs CXCAN.csv")


# C1 vs C2,3 Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CIN1",0,1)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_CIN1 vs CIN 2.3 CXCAN.csv")


# Normal, CIn1 vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal,c1 vs C2.3.csv")


# Normal vs CIM1/2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal vs CIM123.csv")

# Normal,C1 vs Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal,C1 vs Cx cAN.csv")


# Normal vs CIN2/3 Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="Normal",0,1)

x<-c()
auc<-c()
for( i in 3:3840){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_ne_Normal vs CIN2.3 Cx cAN.csv")

###################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################

# AUC 洹몃━湲?

rm(list=ls())

install.packages("Epi")
library(Epi)

data<-read.csv("...lipid_positive.csv")

# Normal vs CX cAN
data1<-subset(data,data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_po_Normal_CXCAN_auc.csv")

# Normal vs CIN1
data1<-subset(data,data$group=="Normal"|data$group=="CIN1")
data1$group1<-ifelse(data1$group=="CIN1",1,0)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal_CIN1.csv")


# Normal vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_po_Normal_CIN2.3.csv")

# CIN1 vs CIN2/3
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)


x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_po_CIN1_CIN2.3.csv")

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)


x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}

write.csv(data2,"...lipid_po_CIN1_CXCAN.csv")


# CIN2/3 vs CX CAN
data1<-subset(data,data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)
x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_CIN2.3_CXCAN.csv")



# Normal vs CIN1,2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal vs abnormal.csv")



# Normal , CIN1 vs  CIN 2,3, Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="Normal"|data1$group=="CIN1",0,1)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal,CIN1 vs CIn2,3, Cx cAN.csv")


# Normal , CIN1   CIN 2,3, vs Cx CAN

data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal,CIN1,2,3 vs Cx cAN.csv")

# C1,2,3 vs Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_CIN1.2.3 vs CXCAN.csv")


# C1 vs C2,3 Cx CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CIN1",0,1)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_CIN1 vs CIN 2.3 CXCAN.csv")


# Normal, CIn1 vs CIN2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="CIN2/3",1,0)
x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal,c1 vs C2.3.csv")


# Normal vs CIM1/2/3
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CIN2/3")
data1$group1<-ifelse(data1$group=="Normal",0,1)
x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal vs CIM123.csv")

# Normal,C1 vs Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal,C1 vs Cx cAN.csv")


# Normal vs CIN2/3 Cx cAN
data1<-subset(data,data$group=="Normal"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="Normal",0,1)

x<-c()
auc<-c()
for( i in 3:4357){
  x[i]<-colnames(data1[i])
  auc[i]<-ROC(form=group1~data1[,i],data=data1,plot="ROC")$AUC
  data2<-data.frame(x,auc)
}
write.csv(data2,"...lipid_po_Normal vs CIN2.3 Cx cAN.csv")

###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################


rm(list=ls())

data<-read.csv("...20171214_polar positive name_ heatmap.csv")
rownames(data)<-data[,1]
data<-data[,-1]

install.packages("gplots")
library(gplots)

heatmap1<-as.matrix(scale(data)) #?젙洹쒗솕
heatmap1<-as.matrix(scale(log2(data))) #?젙洹쒗솕

for(i in 1:205){data[,i]<-ifelse(data[,i]<0,0,data[,i])}
#for(i in 1:205){data[,i]<-log10(as.numeric(data[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))


heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)




hc.rows <- hclust(dist(heatmap1))
plot(hc.rows)
table(cutree(hc.rows,k=3))
rect.hclust(hc.rows, k=3, border="red") 

####

rownames(data)

data_2<-data[c("3-Indolepropionic acid","Alanine","AMP","Aspartate","Caffeine","Carnitine (C5) 2","Fructose 6-phosphate","Glutamate","Hippuric acid","Hypoxanthine","Inosine","Isoleucine","Nonanoylcarnitine","Phenylalanine","Pipecolic acid","Proline","sn-glycero-3-Phosphocholine","Taurine","Creatine"),]

data_2<-data[c("3-Indolepropionic acid","Alanine","AMP","Aspartate","Caffeine","Carnitine (C5) 2","Fructose 6-phosphate","Glutamate","Hippuric acid","Hypoxanthine","Inosine","Isoleucine","Nonanoylcarnitine","Phenylalanine","Pipecolic acid","Proline","sn-glycero-3-Phosphocholine","Taurine"),]

data_2<-data[c("3-Indolepropionic acid","Alanine","AMP","Aspartate","Caffeine","Carnitine (C5) 2","Glutamate","Hippuric acid","Hypoxanthine","Inosine","Isoleucine","Nonanoylcarnitine","Phenylalanine","Pipecolic acid","Proline","sn-glycero-3-Phosphocholine","Taurine"),]

data_2<-data[c("3-Indolepropionic acid","Alanine","AMP","Aspartate","Caffeine","Glutamate","Hippuric acid","Hypoxanthine","Inosine","Nonanoylcarnitine","Pipecolic acid","sn-glycero-3-Phosphocholine","Taurine"),]


heatmap1<-as.matrix(scale(data_2)) #?젙洹쒗솕
heatmap1<-as.matrix(scale(log(data_2))) #?젙洹쒗솕

for(i in 1:205){heatmap1[,i]<-ifelse(heatmap1[,i]<0,0,heatmap1[,i])}
#for(i in 1:205){heatmap1[,i]<-log10(as.numeric(heatmap1[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))


heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)




hc.rows <- hclust(dist(heatmap1))
plot(hc.rows)
table(cutree(hc.rows,k=3))
rect.hclust(hc.rows, k=3, border="red") 

###


#######################################################################################

install.packages("Epi")
library(Epi)

data<-read.csv("...20171214_polar positive name.csv")


str(data)

# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~Phenylalanine,data=data1,plot="ROC")
ROC(form=group1~Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine+Proline,data=data1,plot="ROC")$AUC

ROC(form=group1~Hypoxanthine+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC


# No CAN vs CX CAN
data1<-data
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~Phenylalanine,data=data1,plot="ROC")
ROC(form=group1~Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine+Proline,data=data1,plot="ROC")$AUC

ROC(form=group1~Hypoxanthine+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC


# CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="CIN2/3"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~Phenylalanine,data=data1,plot="ROC")
ROC(form=group1~Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine+Proline,data=data1,plot="ROC")$AUC


ROC(form=group1~Hypoxanthine+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC



# Normal+CIN1 vs CX CAN
data1<-subset(data,data$group=="CIN1"|data$group=="Normal"|data$group=="CX CAN")
data1$group1<-ifelse(data1$group=="CX CAN",1,0)

ROC(form=group1~Phenylalanine,data=data1,plot="ROC")
ROC(form=group1~Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine,data=data1,plot="ROC")
ROC(form=group1~Phenylalanine+Hypoxanthine+Proline,data=data1,plot="ROC")$AUC


ROC(form=group1~Hypoxanthine+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP,data=data1,plot="ROC")$AUC
ROC(form=group1~Hypoxanthine+Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Aspartate+AMP+Glutamate,data=data1,plot="ROC")$AUC


###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################
###################################################


rm(list=ls())

data<-read.csv("...20171219_polar negative name heatmap.csv")
rownames(data)<-data[,1]
data<-data[,-1]

install.packages("gplots")
library(gplots)

heatmap1<-as.matrix(scale(data)) #?젙洹쒗솕
#heatmap1<-as.matrix(scale(log(data))) #?젙洹쒗솕

for(i in 1:205){data[,i]<-ifelse(data[,i]<0,0,data[,i])}
#for(i in 1:205){data[,i]<-log10(as.numeric(data[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))


heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)




hc.rows <- hclust(dist(heatmap1))
plot(hc.rows)
table(cutree(hc.rows,k=3))
rect.hclust(hc.rows, k=3, border="red") 

####

rownames(data)

data_2<-data[c("3-Hydroxybutyric acid","Hippuric acid","3-Indolepropionic acid","Inosine","Lactate","Dimethylglycine","Taurine","Pyroglutamic acid","Aspartate","Malate","Glutamate","Histidine","Phenylalanine","Gluconic acid","Tryptophan","Ribose 5-phosphate"),]

data_2<-data[c("Lactate","Dimethylglycine","Taurine","Pyroglutamic acid","Aspartate","Malate","Glutamate","Histidine","Phenylalanine","Gluconic acid","Tryptophan","Ribose 5-phosphate"),]

data_2<-data[c("3-Hydroxybutyric acid","Hippuric acid","Lactate","Dimethylglycine","Taurine","Pyroglutamic acid","Aspartate","Malate","Glutamate","Histidine","Phenylalanine","Gluconic acid","Tryptophan","Ribose 5-phosphate"),]

data_2<-data[c("3-Hydroxybutyric acid","Hippuric acid","3-Indolepropionic acid","Inosine","Lactate","Dimethylglycine","Taurine","Pyroglutamic acid","Aspartate","Malate","Glutamate","Phenylalanine","Gluconic acid","Ribose 5-phosphate"),]

data_2<-data[c("3-Hydroxybutyric acid","Hippuric acid","3-Indolepropionic acid","Inosine","Lactate","Dimethylglycine","Taurine","Pyroglutamic acid","Aspartate","Malate","Glutamate","Ribose 5-phosphate"),]

heatmap1<-as.matrix(scale(data_2)) #?젙洹쒗솕
#heatmap1<-as.matrix(scale(log(data_2))) #?젙洹쒗솕

for(i in 1:203){heatmap1[,i]<-ifelse(heatmap1[,i]<0,0,heatmap1[,i])}
#for(i in 1:205){heatmap1[,i]<-log10(as.numeric(heatmap1[,i])) }  

colCols <- ifelse(grepl("Normal",colnames(heatmap1)),"purple",
                  (ifelse(grepl("CIN1",colnames(heatmap1)),"lightblue",
                          (ifelse(grepl("CIN2",colnames(heatmap1)),"red","black")))))

library(gplots)
heatmap.2(heatmap1, scale='none',
          trace="none",cexRow=1,keysize=0.75,ColSideColors=colCols,labCol=NA, margins = c(10, 20))

par(lend = 1)
legend("topright",legend = c("Normal", "CIN1", "CIN2/3","Cancer"),col = c("purple", "lightblue","red", "black"),
       lty=1,lwd =2,border=FALSE, bty="n", y.intersp = 0.7, cex=0.7)




hc.rows <- hclust(dist(heatmap1))
plot(hc.rows)
table(cutree(hc.rows,k=2))
rect.hclust(hc.rows, k=3, border="red") 
###


#######################################################################################

install.packages("Epi")
library(Epi)

rm(list=ls())
data<-read.csv("...20171219_polar negative name.csv")


str(data)



# Normal vs CX CAN
data1<-subset(data,data$Metabolite=="Normal"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)

ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC







# CIN1 vs CX CAN
data1<-subset(data,data$Metabolite=="CIN1"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC






# CIN2/3 vs CX CAN
data1<-subset(data,data$Metabolite=="CIN2/3"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC





# N,C1 vs C2/3, CX CAN
data1<-data
data1$group1<-ifelse(data1$Metabolite=="CIN2/3"|data1$Metabolite=="CX CAN",1,0)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC



# No can vs CX CAN
data1<-data
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC





# CINs vs CX CAN
data1<-subset(data,data$Metabolite=="CIN1"|data$Metabolite=="CIN2/3"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC




# CIN1 vs CIN2/3, CX CAN
data1<-subset(data,data$Metabolite=="CIN1"|data$Metabolite=="CIN2/3"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CIN1",0,1)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC





# N, CIN1 vs CX CAN
data1<-subset(data,data$Metabolite=="CIN1"|data$Metabolite=="Normal"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="CX CAN",1,0)

ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC



# N vs C2/3, CX CAN
data1<-subset(data,data$Metabolite=="Normal"|data$Metabolite=="CIN2/3"|data$Metabolite=="CX CAN")
data1$group1<-ifelse(data1$Metabolite=="Normal",0,1)


ROC(form=group1~Lactate+Aspartate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC

ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
ROC(form=group1~Lactate+Aspartate+Pyroglutamic.acid+Glutamate+Ribose.5.phosphate,data=data1,plot="ROC")$AUC
```
