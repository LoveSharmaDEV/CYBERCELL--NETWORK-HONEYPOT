# ARTIFICIAL NUERAL NETWORK
# INSTALLING THEANO
#INSTALLING TENSORFLOW
# INSTALLING KERAS

# PART1 DATA PREPROCESSING

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing dataset
dataset = pd.read_csv('data.csv')  

# cleaning the texts
corpus = []
for i in range(0 ,561):
    review = dataset['COMMANDS'][i] 
    corpus.append(review)
     
# Creating bag of words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray() 
y = dataset.iloc[: ,1].values


'''
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
'''
# LETS MAKE ANN
# IMPORT KERAS LIBRARIES


# Evaluating And Improving Performance Of ANN

# Evaluating The ANN
 
# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 150, kernel_initializer = 'uniform', activation = 'relu', input_dim = 389))

# Adding the second hidden layer
classifier.add(Dense(units = 150, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X, y, batch_size = 10, epochs = 100)

# Part 3 - Making predictions and evaluating the model

cmmd = cv.transform([' groupadd'])

# Predicting the Test set results
y_pred = classifier.predict(cmmd)
y_pred = (y_pred > 0.5)

# Dropout Regularization to reduce overfitting

# serialize model to json
model_json = classifier.to_json()
with open("classifier.json" , "w") as json_file:
    json_file.write(model_json)
    
#serialize weights to HDF5
classifier.save_weights("classifier.h5")
print("Saved model to disk")

#load json and create model
json_file = open('classifier.json' , 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

#load weights into new model
loaded_model.load_weights("classifier.h5")
print("Loaded model from disk")

#evaluate loaded model on test data
loaded_model.compile(loss = 'binary_crossentropy' , optimizer = 'rmsprop' , metrics = ['accuracy'])
y_pred = loaded_model.predict_classes(cmmd)