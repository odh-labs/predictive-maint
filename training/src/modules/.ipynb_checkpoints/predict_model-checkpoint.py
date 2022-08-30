import sys
import os
import tensorflow as tf
import numpy as np
from pathlib import Path
from sklearn.metrics import confusion_matrix
from ..visualization.visualize import visualizeData
import matplotlib.pyplot as plt
class predictor(object):
    
    def __init__(self, clf=None,data=None,modelType = 'ml'):
        self.clf = clf
        self.data_x = data[0]
        self.data_y = data[1]
        self.model_type = modelType
    



    def predict(self):
        if self.model_type == 'ml':
                 y_pred1 = self.clf.predict(self.data_x.values)
                 y_pred = self.clf.predict_proba(self.data_x)[:, 1]
                 cnf_matrix = confusion_matrix(self.data_y,y_pred1)
                
                
                 vD = visualizeData(cm_data=cnf_matrix,y_true = self.data_y, y_pred = y_pred,modelType=self.model_type)
                 vD.precisionRecallDisplay()
                 
                 vD.confusionMatrixPlot()

        else:
                
                 y_pred=self.clf.predict(self.data_x.values) 
                 y_pred1=np.round(y_pred)

                 cnf_matrix = confusion_matrix(self.data_y,y_pred1)
                 vD = visualizeData(cm_data=cnf_matrix,y_true = self.data_y, y_pred = y_pred,modelType=self.model_type)
                 vD.precisionRecallDisplay()
                 
                 vD.confusionMatrixPlot()