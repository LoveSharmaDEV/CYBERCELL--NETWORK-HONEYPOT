import numpy as np
import threading
from keras.models import model_from_json
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import tensorflow as tf

class End_game :
    
    def mal_done(self ,statement):
        list = []
        list.append(statement)
        
        cv = CountVectorizer()
        # importing dataset
        dataset = pd.read_csv('data.csv')  
        
        # cleaning the texts
        corpus = []
        for i in range(0 ,144):
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
        graph = tf.get_default_graph() 
        
        #evaluate loaded model on test data
        loaded_model.compile(loss = 'binary_crossentropy' , optimizer = 'rmsprop' , metrics = ['accuracy'])
        y_pred = loaded_model.predict_classes(cmmd)
        
        with open('graph.txt', 'a') as abc:
            np.savetxt(abc, y_pred)
        abc.close()    