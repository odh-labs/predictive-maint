import os
import tensorflow as tf

import joblib
import numpy as np
import json
import traceback
import sys


class Predictor(object):
    
    def __init__(self):
        self.loaded = False
        self.labels = ["Background","Person","Finger"]#["Blocked","Blured","Changed_View","Normal", "Others"]
    def load(self):

        print("Loading model",os.getpid())
        self.model = tf.keras.models.load_model( 'model.h5', compile=False)
        print("Model Loaded!")
        self.loaded = True
        print("Loaded model")

    def predict_raw(self, request):
        data = request.get("data", {}).get("ndarray")
        print('step 00')
#         print(data)
        if data:
            float_array = np.array(data, dtype=np.float64)
            float_array = tf.expand_dims(float_array, 0)
            print('step 01')
#             print(float_array)

        print ('step1......')
#         print(X['image'])
        try:
            print(float_array)
        except Exception as e:
            print(traceback.format_exception(*sys.exc_info()))
      
        if not self.loaded:
            self.load()
        try:
            result = self.model.predict(float_array) 
        except Exception as e:
            print(traceback.format_exception(*sys.exc_info()))
        
        ######
        print ('step 2......')
#         print(tf.math.argmax(result,axis=0))
        json_results = {}
        arg_max_result = tf.math.argmax(result,axis=1)
        print("1"*50)
        json_results["Predicted Class: "] = str(self.labels[int(arg_max_result)])
        print("2"*50)
        json_results["Predicted Label: "] = json.dumps(arg_max_result.numpy(), cls=JsonSerializer)
        print("3"*50)
        json_results["Predicted Class Prob: "] = json.dumps(str(np.max(result, axis=1)), cls=JsonSerializer)
        print("4"*50)
        json_results["All Probs: "] = json.dumps(result, cls=JsonSerializer)
        print("5"*50)
    
        print(json_results)
        return json.dumps(json_results)
        # return json.dumps(result.numpy(), cls=JsonSerializer)

class JsonSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (
        np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)