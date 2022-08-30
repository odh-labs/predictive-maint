import os
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import subprocess
import joblib
import mlflow
class MLflow():
    '''
    Define a class for MLflow configuration
    ----------

    Returns
    -------
    self.model:
        Deep learning based Model  
    
    '''
    def __init__(self, MLFLOW):
        self.mlflow = MLFLOW
        self.host = os.environ['HOST']
        self.experiment_name = os.environ['EXPERIMENT_NAME']
        

    def SetUp_Mlflow(self):
        '''
        Setup MLflow
        ----------
        
        Returns
        -------
        
        '''       

        # Connect to local MLflow tracking server
        self.mlflow.set_tracking_uri(self.host)

        # Set the experiment name...
        self.mlflow.set_experiment(self.experiment_name)

        self.mlflow.tensorflow.autolog()
        return self.mlflow

    


    def mlflow_grid_search(methodtoexecute, methodarguments):
        with mlflow.start_run(tags= {
            "mlflow.docker.image.name": os.getenv("JUPYTER_IMAGE", "LOCAL"),
            "mlflow.source.type": "NOTEBOOK",
        }) as run:
            methodtoexecute(**methodarguments)
            record_details(mlflow)

        return run
    
    
    
class trainModel():
    '''
    Build Lstm model for tensorflow
    ----------

    Returns
    -------
    self.model:
        Deep learning based Model
    
    '''
    
    def __init__(self, model = None, trainDs = None, valDs = None, batchSize=64,epochs=10,outputFeatureName = None,mlflow = None):
        self.model_checkpoint_callback = []
        
        self.model = model
        self.history = []
        
        
        self.batch_size = batchSize
        self.epochs = epochs
        
        self.mlflow = mlflow
        
        self.out_fe_name = outputFeatureName
        self.train_ds = trainDs
        self.val_ds = valDs
        
        


    def get_pip_freeze(self):
        return subprocess.check_output(['pip', 'freeze']).splitlines()


    def record_details(self):
        """
        This method is the anchor poijt and more activiteis will go in it
        :param mlflow:
        :return:
        """
        with open(os.environ['SAVE_PATH']+"pip_freeze.txt", "wb") as file:
            for line in self.get_pip_freeze():
                file.write(line)
                file.write(bytes("\n", "UTF-8"))
        self.mlflow.log_artifact(os.environ['SAVE_PATH']+"pip_freeze.txt")
        file.close()
        self.mlflow.log_artifact(os.environ['MODEL_PATH'], artifact_path="model")
        self.mlflow.log_artifact(os.environ['SAVE_PATH']+"requirements.txt", artifact_path="model")
        
#         self.mlflow.log_artifact(os.environ['SAVE_PATH']+"tokenizer.pkl", artifact_path="model")
#         self.mlflow.log_artifact(os.environ['SAVE_PATH']+"doc1.txt", artifact_path="model")


        # os.remove("pip_freeze.txt")
        # os.remove("model.h5")
        # os.remove("tokenizer.pkl")
        # os.remove("labelencoder.pkl")

    def DefineCheckPoint(self):
        '''
        Define the model
        ----------
        
        Returns
        -------
        
        '''
        #Bidirectional LSTM
        checkpoint_filepath = os.environ['MODEL_PATH']
        self.model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            monitor=os.environ['CHECK_METRICS'],
            mode=os.environ['CHECK_METRICS_MAX_OR_MIN'],
            save_best_only=True)

    def ModelTraining(self):
        '''
        Define the model
        ----------
        
        Returns
        -------
        
        '''

            
        self.DefineCheckPoint()
        
            
        self.mlflow = MLflow(self.mlflow).SetUp_Mlflow()
        with self.mlflow.start_run(tags= {

                "mlflow.docker.image.name": os.getenv("JUPYTER_IMAGE", "LOCAL"),
                "mlflow.source.type": "NOTEBOOK",
        #         "mlflow.source.name": ipynbname.name()
            }) as run:

                # Fit the model
                self.history = self.model.fit(
                    self.train_ds,
                    epochs=self.epochs,
                    callbacks=[self.model_checkpoint_callback],
                    validation_data=self.val_ds,
                    
                    workers=-1)
                
                
                self.record_details()
        
#         cuda.select_device(0)
#         cuda.close()
        return self.model,self.history