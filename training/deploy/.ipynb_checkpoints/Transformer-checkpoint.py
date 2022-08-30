import numpy as np
import joblib
import pandas as pd

class Transformer(object):
    
    def __init__(self):
        self.scaler = joblib.load('scaler.pkl')

    def transform_input(self, X, feature_names =None , meta=None ):
        print(X)
        print('*'*50)

        print(feature_names)
        print('+'*50)
        print(meta)
        print('-'*50)
        df = pd.DataFrame(X, columns=feature_names)
        print('x'*50)
        print(df)
        print('y'*50)
        
        transformed_data = self.scaler.transform(df)
        
        print(transformed_data)
        print('z'*50)

        return transformed_data