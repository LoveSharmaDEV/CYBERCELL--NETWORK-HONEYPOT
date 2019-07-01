import numpy as np
import threading
from keras.models import model_from_json
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import tensorflow as tf
import time


def end_game():
  try:
    fileHandle = open ( '/root/HONEYPOT/logs/log.txt',"r" )
    lineList = fileHandle.readlines()
    Last_l = lineList[len(lineList)-1]
    file = open('last_command.txt' , "w")  
    file.write(lineList[len(lineList)-1])
    print("involved")




   
    list = []
    list.append(Last_l)
    
    cv = CountVectorizer()
    # importing dataset
    dataset = pd.read_csv('data.csv')  
    
    # cleaning the texts
    corpus = []
    for i in range(0 ,561):
        review = dataset['COMMANDS'][i] 
        corpus.append(review)
        
    cv.fit(corpus)
    cmmd = cv.transform(list)
    
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
    y_pred = loaded_model.predict(cmmd)
    
    if y_pred > 0.5:
        mal_file = open("/root/HONEYPOT/Malicious.txt" , 'a')
        mal_file.write(Last_l)
    
    with open('graph1.txt', 'a') as abc:
        np.savetxt(abc, y_pred)
  except :
      pass
   
    
 
while True:
  end_game()
  time.sleep(3)
