


import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from ..visualization.visualize import visualizeData
import tensorflow as tf
# preprocessData(trainDs = None,testDs = None,valDs = None,numClasses = None).dataPreProcessing()
class preprocessData():
    '''
    Turn raw data into features for modeling
    ----------

    Returns
    -------
    self.final_set:
        Features for modeling purpose
    self.labels:
        Output labels of the features
    enc: 
        Ordinal Encoder definition file
    ohe:
        One hot  Encoder definition file
    '''
    def __init__(self, trainDs = None,testDs = None,valDs = None,numClasses = None, augFlag= None,height=None,width=None, batchSize = None):
        self.train_ds = trainDs
        self.test_ds = testDs
        self.val_ds = valDs
        self.num_classes = numClasses
        self.aug_flag = augFlag
        self.height = height
        self.width = width
        self.batch_size = batchSize
        

    def dataAugmentation(self):
                self.data_augmentation = tf.keras.Sequential(
            [   ###tensorflow <2.5
                tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
                tf.keras.layers.experimental.preprocessing.RandomRotation(0.1),
                ###tensorflow >2.8
#                 tf.keras.layers.RandomFlip("horizontal"),  
#                 tf.keras.layers.RandomRotation(0.1),
            ]
        )
            
    
    def input_preprocess(self,image, label):
        '''
        # One-hot / categorical encoding
        
        '''
        label = tf.one_hot(label, self.num_classes)
        return image, label
    
    def preProcess(self):
        
        


        self.train_ds = self.train_ds.map(
            self.input_preprocess, num_parallel_calls=tf.data.AUTOTUNE
        )

        # train_ds = train_ds.batch(batch_size=batch_size, drop_remainder=True)
        self.train_ds = self.train_ds.prefetch(tf.data.AUTOTUNE)


        self.val_ds = self.val_ds.map(self.input_preprocess)
        # val_ds = val_ds.batch(batch_size=batch_size, drop_remainder=True)


        self.test_ds = self.test_ds.map(self.input_preprocess)
        # test_ds = test_ds.batch(batch_size=batch_size, drop_remainder=True)
    def make_generator_train(self):
        return self.train_ds

    def make_generator_test(self):
        return self.test_ds

    def make_generator_validation(self):

        return self.val_ds
    
    
    def preProcessTFData(self):
        self.train_ds = tf.data.Dataset.from_generator(self.make_generator_train,output_types=(tf.float32, tf.float32),output_shapes=([self.batch_size, self.height, self.width, 3], [self.batch_size, self.num_classes]))
        self.test_ds = tf.data.Dataset.from_generator(self.make_generator_test,output_types=(tf.float32, tf.float32),output_shapes=([self.batch_size, self.height, self.width, 3], [self.batch_size, self.num_classes]))
        self.val_ds = tf.data.Dataset.from_generator(self.make_generator_validation,output_types=(tf.float32, tf.float32),output_shapes=([self.batch_size, self.height, self.width, 3], [self.batch_size, self.num_classes]))

        
    def dataPreProcessing(self):
        visualizeData( data = self.train_ds).showImages()
        self.dataAugmentation()
        visualizeData( data = self.train_ds,dataAugmentation = self.data_augmentation,augFlag = self.aug_flag).showImages()
        self.preProcess()
#         self.preProcessTFData()
        
        
        return self.train_ds, self.val_ds, self.test_ds,self.data_augmentation
    
    
        
        
    
    
    