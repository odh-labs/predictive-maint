import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
from json import dumps,loads
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
class readData():
    '''
    Read data from csv file
    ----------

    Returns
    -------
    self.data:
        data: as a pandas dataframe
    
    '''
    def __init__(self, dataPath= None, imageSize = None, batchSize = None, seed = None ):

        
        
        self.data_path = dataPath
        self.batch_size = batchSize
        self.image_size = imageSize
        self.seed = seed
    


    ## Read data from csv File
    def generateData(self):
        '''
        Read data from folder
        ----------
        
        Returns
        -------
        Dataframe 
        '''
        """
        ## Generate a `Dataset`
        """



        self.train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path,
            validation_split=0.2,
            subset="training",
            seed=self.seed,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )
        self.val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path,
            validation_split=0.2,
            subset="validation",
            seed=self.seed,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        self.test_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path,
            validation_split=0.2,
            subset="validation",
            seed=self.seed,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        self.num_classes = len(self.test_ds.class_names)
        return self.train_ds,self.val_ds,self.test_ds ,self.num_classes
    
    ## Read data from csv File
    def generateImageData(self):
        '''
        Read data from folder
        ----------
        
        Returns
        -------
        Dataframe 
        '''
        """
        ## Generate a `Dataset`
        """
        self.train_datagen = ImageDataGenerator(
#             rescale=1./255,
                # rotation_range=20,
            horizontal_flip=True,
                vertical_flip=True,
            fill_mode='nearest'
            )

        # Note that the validation data should not be augmented!
        self.test_datagen = ImageDataGenerator()

        self.train_ds = self.train_datagen.flow_from_directory(
            # This is the target directory
            self.data_path+'train/',
            # All images will be resized to target height and width.
            target_size=self.image_size,
            batch_size=self.batch_size,
            # Since we use categorical_crossentropy loss, we need categorical labels
            class_mode='categorical',
            shuffle=True)

        self.val_ds = self.test_datagen.flow_from_directory(
                self.data_path+'val/',
                target_size=self.image_size,
                batch_size=self.batch_size,
                class_mode='categorical',
                shuffle=False)

        self.test_ds = self.test_datagen.flow_from_directory(
                self.data_path+'test/',
                target_size=self.image_size,
                batch_size=self.batch_size,
                class_mode='categorical',
                shuffle=False)
        

        self.num_classes = len(np.unique(self.train_ds.labels))
        return self.train_ds,self.val_ds,self.test_ds ,self.num_classes 

    
    
    def readTestData(self):
        '''
        Read test data to evaluate the app performance
        ----------
        
        Returns
        -------
        Json file
        '''
        self.headers = {"Content-Type" : "application/json"}
        self.testData = {"data":
          {
                "names":
                    ["Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
               "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
               "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"],
             "ndarray": [[77627,-7.139060068,2.773081604,-6.757845069,4.446455974,-5.464428185,-1.713401451,-6.485365409,3.409394799,-3.053492714,-6.260705515,2.394167666,-6.16353738,0.602850521,-5.606346429,0.206621734,-6.52508104,-11.40836754,-4.693977736,2.431274492,-0.616949301,1.303250309,-0.016118152,-0.876669888,0.382229801,-1.054623888,-0.614606037,-0.766848112,0.409423944,106.9]]

          }
        }
        self.testData = dumps(self.testData)
        return self.testData,self.headers
    
    