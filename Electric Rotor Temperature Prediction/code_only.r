library(tidyr)
library(dplyr)
library(leaps)
library(car) #scatterplot matrix
library(glmnet) # ridge and lasso
library(mgcv) # gam
library(randomForest)

# read dataset
data = read.csv(file = "./pmsm_temperature_data.csv")

# inspect the dataset and display the dimensions
cat("The dataset has", dim(data)[1], "records, each with", dim(data)[2],
    "attributes. The structure is:\n\n")

# inspect the structure of data
str(data)

cat("\n Inspect the first few rows and columns in the dataset:")
# Inspect the first few records
head(data)

cat("\n The statistical summary for each attribute:")
# Statistical summary 
summary(data)


# plot each attribuite on histogram
par(mfrow = c(2,2))
for (i in colnames(data)[1:9]){
    hist(data[,i], main = paste0("Histogram of"," ", i))
}

# add min value to each of variables so they can be transformed
data$pm_n = data$pm + 5
data$ambient_n = data$ambient + 5
data$coolant_n = data$coolant + 5
data$u_d_n = data$u_d + 5
data$u_q_n = data$u_q + 5
data$motor_speed_n = data$motor_speed + 5
data$torque_n = data$torque + 5
data$i_d_n = data$i_d + 5
data$i_q_n = data$i_q + 5

# apply log transformation to deal with skewed data
par(mfrow=c(2,2))
hist(log(data$coolant_n))
hist(log(data$u_q_n))
hist(log(data$motor_speed_n))
hist(log(data$i_d_n))

# apply square root transformation
par(mfrow = c(2,2))
hist(sqrt(data$coolant_n))
hist(sqrt(data$u_q_n))
hist(sqrt(data$motor_speed_n))
hist(sqrt(data$i_d_n))

# apply cube root transformation
par(mfrow = c(2,2))
hist((data$coolant_n)^(1/3))
hist((data$u_q_n)^(1/3))
hist((data$motor_speed_n)^(1/3))
hist((data$i_d_n)^(1/3))


# plot each pairs of variables
scatterplotMatrix(~ambient+coolant+u_d+u_q+i_d+i_q+motor_speed+torque+pm, data = data, main = "Scatterplot matrix")

# Correlation Coefficients of each pair
cor(data[1:9])

# plot u_d vs i_q and torque
plot(data$u_d, data$i_q)
plot(data$u_d, data$torque)

par(mfrow = c(2,2))
for (i in colnames(data[1:8])){
    plot(data$pm, data[,i], main = paste0("pm vs", " ", i))
}


# subset data into train and test set
train = data %>% filter(profile_id != 72 & profile_id != 81)
test = data %>% filter(profile_id == 72 | profile_id == 81)

# perform best subset selection
reg_fit = regsubsets(pm~ ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q, data = train)
reg_summary = summary(reg_fit)

par(mfrow = c(1,2))

# Find the maximum adj_r2
adj_r2_max = which.max(reg_summary$adjr2)
# Find the minimum Cp and BIC
cp_min = which.min(reg_summary$cp)
bic_min = which.min(reg_summary$bic) 

# plot the measurements for each number of variables and 
# show the maximum and minmum on the plots as red points
# RSS
plot(reg_summary$rss, xlab = "Number of Variables", ylab = "RSS", type = "l")

# adjusted R2
plot(reg_summary$adjr2, xlab = "Number of Variables", ylab = "Adjusted RSq", type = "l")
points(adj_r2_max, reg_summary$adjr2[adj_r2_max], col ="red", cex = 2, pch = 20)

# Cp
plot(reg_summary$cp, xlab = "Number of Variables", ylab = "Cp", type = "l")
points(cp_min, reg_summary$cp[cp_min], col = "red", cex = 2, pch = 20)

# BIC
plot(reg_summary$bic, xlab = "Number of Variables", ylab = "BIC", type = "l")
points(bic_min, reg_summary$bic[bic_min], col = "red", cex = 2, pch = 20)


# create model
fit1 = lm(pm~ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q, data = train)
# check for statistics and residual plots
summary(fit1)
plot(fit1)

# adding interaction terms that are highly coorelated
fit2 = lm(pm~ ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q + i_q:torque + u_d:torque + u_d:i_q
               + u_q:motor_speed + motor_speed:i_d, data = train) 
# check for statistics and residual plots
summary(fit2)
plot(fit2)

# check the influencial points
train[c(4192,4162,4172),]

# exclude the three rows and include other interactions see if it improves the model 
fit3 = lm(pm~ ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q + i_q:torque + u_d:torque + u_d:i_q
               + u_q:motor_speed + motor_speed:i_d, data = train[-c(116,4162,4172,4192,4221,4201),])
# check for statistics and residual plots
summary(fit3)
plot(fit3)

# calculate weighted least squares
weights = 1 / lm(abs(fit1$residuals) ~ fit1$fitted.values)$fitted.values^2
# add log and cube root transformation
fit4 = lm(pm~ ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q + i_q:torque + u_d:torque + u_d:i_q
               + u_q:motor_speed + motor_speed:i_d + log(motor_speed_n) + I((u_q)^(1/3)),
          data = train,
          weights = weights)
# check for statistics and residual plots
summary(fit4)
plot(fit4)

# removed torque and motor speed from fit 4
fit5 = lm(pm~ ambient + coolant + u_d + u_q + i_d + i_q + i_q:torque + u_d:torque + u_d:i_q
               + u_q:motor_speed + motor_speed:i_d + log(motor_speed_n) + I((u_q)^(1/3)),
          data = train,
          weights = weights)
# check for statistics and residual plots
summary(fit5)
plot(fit5)

# include all interactions in the model
fit6 = lm(pm ~ (ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q)^2, data = train)
# apply stepwise selection on fit5
fit6_step = step(fit6)
# print summary
summary(fit6_step)
plot(fit6_step)

# To perform Ridge regression, we need to split predictors and target
train_x = model.matrix(pm~ (ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q)^2, train)[,-1] 
train_y = train$pm
test_x = model.matrix(pm~ (ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q)^2, test)[,-1]
test_y = test$pm

# use cross validation to find lamda that minimize MSE 
cv_ridge = cv.glmnet(train_x, train_y, alpha = 0)
# plot to visualize MSE vs lamda
plot(cv_ridge)
# show the lamda that minimizes MSE
best_lamda = cv_ridge$lambda.min 
best_lamda


# fit a ridge regression model to train set
grid = 10^seq(10, -2, length = 100)
ridge_model = glmnet(train_x, train_y, alpha = 0, lambda = grid , thresh = 1e-12)
# predict on test set with best lamda
ridge_pred = predict(ridge_model, s = best_lamda, newx = test_x)

# use cross validation to find lamda that minimize MSE 
cv_lasso = cv.glmnet(train_x, train_y, alpha = 1)
# plot to visualize MSE vs lamda
plot(cv_lasso)
# show the lamda that minimizes MSE
best_lamda_la = cv_lasso$lambda.min 
best_lamda_la

# fit a lasso regression model to train set
lasso_model = glmnet(train_x, train_y, alpha =1, lambda = grid , thresh = 1e-12)
# predict on test set with best lamda
lasso_pred = predict(lasso_model, s = best_lamda_la, newx = test_x)

# show the coefficients that is not zero in this lasso regression (show the predictors used)
lasso_coef = predict(lasso_model, type = "coefficients", s = best_lamda)[1:14,]
lasso_coef[lasso_coef != 0]

# Generalized additive model
fit7_gam = gam(pm~ ambient + s(coolant) + s(u_d) + s(u_q) + s(motor_speed) + s(torque) + s(i_d) + s(i_q) + i_q:torque + 
              u_d:torque + u_d:i_q
               + u_q:motor_speed + motor_speed:i_d, data = train)
summary(fit7_gam)
plot.gam(fit7_gam)

# fit a randomforest tree 
fit_rf = randomForest(pm~ambient + coolant + u_d + u_q + motor_speed + torque + i_d + i_q, data = train, 
                      mtry = 1, importance = TRUE)
# show important variables
importance(fit_rf)

# use the RMSE function from the house_price example 
RMSE <- function(predicted, target) {
    se <- 0
    for (i in 1:length(predicted)) {
        se <- se + (predicted[i]-target[i])^2
    }
    return (sqrt(se/length(predicted)))
}

# function to produce measurements for model comparision
model.accuracy = function(model){
    pred = predict(get(model), test)
    RMSE = RMSE(pred, test$pm)
    AIC = AIC(get(model))
    R2 = summary(get(model))$r.sq
    Result = data.frame(RMSE,AIC,R2)
    return (Result)    
}

# dataframe to store measurements
model_comp = data.frame(RMSE = numeric(), 
                         AIC = numeric(),
                         R2 = numeric())
# names of models to compare
models = c("fit1", "fit2", "fit3","fit4","fit5", "fit6_step")

# compute RMSE for each linear model
for (i in models){
    model_comp = rbind(model_comp, model.accuracy(i))
    rownames(model_comp) = 1:nrow(model_comp)
}
model_comp

# compare fit6 with fit2 using anova
anova(fit2,fit6_step,test="F")

cat("RMSE of ridge regression:",RMSE(ridge_pred,test_y),"\n")
cat("RMSE of lasso regression:",RMSE(lasso_pred,test_y))

cat("RMSE of GAM:",RMSE(predict(fit7_gam,test),test$pm),"\n")
cat("AIC of GAM:",AIC(fit7_gam),"\n")
cat("R2 of GAM:",summary(fit7_gam)$r.sq,"\n")

rf_pred = predict(fit_rf, test)
RMSE(rf_pred, test$pm)
