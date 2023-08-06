import os
import joblib
import numpy as np
import logging

#Percpetron Class
class Perceptron:
    def __init__(self,eta:float=None,epochs:int=None):
        self.weights = np.random.randn(3)*1e-4 # initialize the weights with small random values 
        training = (eta is not None) and (epochs is not None)
        if training:
            logging.info(f"initial weights before training: \n {self.weights}")
        self.eta = eta
        self.epochs = epochs

    #calculate Z values     
    def _z_outcome(self,input,weights):
        return np.dot(input,weights)

    #calculate the activation
    def activation_function(self,z):
        return np.where(z>0,1,0)

    # function for fitting/training the model(perceptron)
    def fit(self,X,y):
        self.X = X
        self.y = y

        # adding bias to the input data so that it becomes a learnable variable
        X_with_bias= np.c_[self.X,-np.ones((len(self.X),1))]
        logging.info(f"X with bias :\n{X_with_bias}")

        # iterating through the epochs  
        for epoch in range(self.epochs):
            logging.info("--"*10)
            logging.info(f"for epoch >> {epoch}")
            logging.info("--"*10)

            z= self._z_outcome(X_with_bias,self.weights)
            y_hat = self.activation_function(z)
            logging.info(f"Predicted values after forward pass \n{y_hat}")

            self.error = self.y-y_hat# calulate the error
            logging.info(f"Error:\n{self.error}")  

            self.weights += self.eta * np.dot(X_with_bias.T,self.error) # weigths updation rule (increase the weights from gradually from small values)
            logging.info(f"Updated weights after epoch:\n {epoch+1}/{self.epochs} :\n {self.weights}")
            logging.info("##"*10)

    def predict(self,X):
        X_with_bias= np.c_[X,-np.ones((len(X),1))]
        z = self._z_outcome(X_with_bias,self.weights)
        return self.activation_function(z)

    def total_loss(self):
        total_loss = np.sum(self.error)
        logging.info(f"\ntotal loss: {total_loss}\n")

    def _create_dir_return_path(self,model_dir,filename):
        os.makedirs(model_dir,exist_ok=True)
        return os.path.join(model_dir,filename)

    def save(self,filename,model_dir= None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir,filename)
            joblib.dump(self,model_file_path)
        else:
            model_file_path = self._create_dir_return_path("model",filename)
            joblib.dump(self,model_file_path)
        logging.info(f">>>>Model is saved at {model_file_path}>>>>>")

    def load(self,filepath):
        return joblib.load(filepath)
        
        
    