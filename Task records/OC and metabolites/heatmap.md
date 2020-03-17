```r
# data set 
install.packages("pheatmap")
library(pheatmap)
raw_info_add_set_log[, c("Group", all_metabolites)] 

# metabolite를 row로, sample을 column으로 
t(raw_info_add_set_log[, c("Group", all_metabolites)])[1:3, 1:3] # check 


raw_info_add_set_log[, c("Group", all_metabolites)] %>% 
  arrange(Group) -> heatmap_test

heatmap_test <- as.data.frame(t(heatmap_test)) # data set 선언 
colnames(heatmap_test) <- paste0("Sample", seq(1, ncol(heatmap_test), 1)) # column name을 sample로 바꿔주기 
heatmap_test[1:3, 1:3] # cehck 

pheatmap(heatmap_test)
heatmap_test[1, 1:5]


annotation_col_test <- data.frame(
  Group = factor(c(rep("Control", ((ncol(heatmap_test))/3)*2), rep("Case", (ncol(heatmap_test))/3)))
)

rownames(annotation_col_test) <- paste0("Sample", seq(1, ncol(heatmap_test), 1))


pheatmap(heatmap_test[-1, ], annotation_col = annotation_col_test, scale = "none", 
         clustering_method = "ward", cluster_cols = F, color = colorRampPalette(c("navy", "white", "firebrick3"))(50))
# cluster_cols = F로 해서 아예 column의 유사성을 비교하지 않도록 설정
# 일단 해결...? 색깔만 좀 어떻게 해볼까

```
