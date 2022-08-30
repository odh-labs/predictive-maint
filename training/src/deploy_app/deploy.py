import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import sys
class deployApplication():
    '''
    Deploy application
    ----------

    Returns
    -------
    an APP
    
    '''
    def __init__(self ):

        
        self.current_path = None
        self.inference_path = None

    ## Read data from csv File
    def deployApp(self):
        '''
        Deploy the application
        ----------
        
        Returns
        -------
        Dataframe 
        '''

        sys.path.append(os.path.dirname(os.getcwd()))
        sys.path.append(os.environ['SAVE_PATH'])
        print(os.path.dirname(os.getcwd()))
        print(os.environ['SAVE_PATH'])
        
#         self.current_path= os.path.dirname(os.getcwd())
#         self.inference_path = self.current_path.replace('Workshop','Inference')
        
#          print(self.current_path)
#         print(self.inference_path)
#         # sys.path.append(inference_path+"/deploy/")
# #         os.system('python ' +self.inference_path+"/deploy/" +'ocp_deploy.py' )
        os.system('python ' +os.environ['SAVE_PATH'] +'ocp_deploy.py' )

