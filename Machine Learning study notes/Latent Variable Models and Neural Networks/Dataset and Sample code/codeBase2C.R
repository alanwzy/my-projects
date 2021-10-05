####################### GENERAL AUXILIARY FUNCTIONS #######################
## The following structure helps us to have functions with multiple outputs
### credit: https://stat.ethz.ch/pipermail/r-help/2004-June/053343.html

error.rate <- function(Y1, T1){
  if (nrow(Y1)!=nrow(T1)){
    stop('error.rate: size of true lables and predicted labels mismatch')
  }
  return (sum(T1!=Y1)/nrow(T1))
}

##########################
options(warn=-1)
library(h2o)
#If there is a proxy: proxy.old <- Sys.getenv('http_proxy'); Sys.setenv('http_proxy'='');
localH2O =  h2o.init(nthreads = -1, port = 54321, max_mem_size = '6G', startH2O = TRUE)


# Students: Use the "absolute" path to the datasets on your machine (important)
labeled.frame <- h2o.importFile(path = '/Users/gholamrh/Google\ Drive/teaching/FIT5201/2016\ -\ TP4/Task3C_labeled.csv' ,sep=',') 
unlabeled.frame <- h2o.importFile(path = '/Users/gholamrh/Google\ Drive/teaching/FIT5201/2016\ -\ TP4/Task3C_unlabeled.csv' ,sep=',') 
test.frame <- h2o.importFile(path = '/Users/gholamrh/Google\ Drive/teaching/FIT5201/2016\ -\ TP4/Task3C_test.csv' ,sep=',') 

labeled.frame[,1] <- as.factor(labeled.frame$label)
unlabeled.frame[,1] <- NA
train.frame <- h2o.rbind(labeled.frame[,-1], unlabeled.frame[,-1])
test.frame[,1] <- as.factor(test.frame$label)

# build a neural network classifier based on the labeled training data
NN.model <- h2o.deeplearning(    
  x = 2:ncol(labeled.frame), # select all pixels + extra features
  y = 1,
  training_frame = labeled.frame, # specify the frame (imported file)    
  hidden = c(100), # number of layers and their units
  epochs = 50, # maximum number of epoches  
  activation = 'Tanh', # activation function 
  autoencoder = FALSE, # is it an autoencoder? Yes!
  l2 = 0.1
)

labeled.predict <- h2o.predict(NN.model, labeled.frame)$predict
error.rate(labeled.frame$label, labeled.predict)

test.predict <- h2o.predict(NN.model, test.frame)$predict
error.rate(test.frame$label, test.predict)


reconstruction.train.error <- matrix(NA, nrow=20, ncol=1)
classification.labeled.error <- matrix(NA, nrow=20, ncol=1)

reconstruction.test.error <- matrix(NA, nrow=20, ncol=1)
classification.test.error <- matrix(NA, nrow=20, ncol=1)


for (k in seq(20, 500, 20)){
  # Students: need to write up code here
  # XXXXXX 
}

# Produce the needed plots.
#XXXXX

