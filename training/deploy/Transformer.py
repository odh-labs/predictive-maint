import numpy as np
import joblib
import pandas as pd

class Transformer(object):
    
    def __init__(self):
        print("Transformer")

    def transform_input(self, X, feature_names =None , meta=None ):
        print(X)
        print('*'*50)

        print(feature_names)
        
        print('z'*50)

        return X