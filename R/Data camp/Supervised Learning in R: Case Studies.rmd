```r
# Caret package의 이해
## https://www.rdocumentation.org/packages/caret/versions/6.0-86/topics/createDataPartition
## https://www.rdocumentation.org/packages/caret/versions/6.0-86/topics/trainControl
## https://www.rdocumentation.org/packages/caret/versions/4.47/topics/train

# yardstick package의 이해 


# Up sampling, Down sampling의 이해 
# https://www.rdocumentation.org/packages/caret/versions/6.0-86/topics/downSample

# CART, xgboost, gbm
## CART
sisters_cart <- train(age ~ ., method = "rpart"
, data = training)
## xgboost
sisters_rf <- train(age ~ ., method = "xgbLinear"
, data = training)
## gbm
sisters_gbm <- train(age ~ ., method = "gbm"
, data = training)

```
