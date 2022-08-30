import os
import zipfile
def get_hyper_paras():

    # dataPath = "../data/raw/creditcard.csv"
    # with zipfile.ZipFile('../data/raw/data.zip', 'r') as zip_ref:
    #     zip_ref.extractall('../data/raw/')


    ### Data Info
    SPLITE_RATE = .2
    
#     OUTPUT_FEATURE_NAME = ["Blocked","Blured","Changed_View","Normal", "Others"]
    OUTPUT_FEATURE_NAME = ["Background","Person","Finger"]
#     LOSS_WEIGHTS = [10,2,1]
    ### Model Related info
    BATCH_SIZE  = 32
    IMAGE_SIZE = (256, 256)
    
    INPUT_SHAPE =IMAGE_SIZE + (3,)
    DROP_OUT_RATE = .2
    EPOCHS = 3
    SEED = 100
    TRAIN_DATA_FLAG = True
    FINE_TUNE_FLAG = False
    
    
    os.environ["MODEL_NAME"] = 'abn-det-demo'
    os.environ["MODEL_VERSION"] = "1"
    base, sourceRepoName = os.path.split(os.getcwd())
    
    

    print (base +"----"+ sourceRepoName)


    base = os.environ['REPO_PATH']
    
    os.environ['SAVE_PATH'] = base +'/training/deploy/'
    os.environ['DATA_PATH'] = base +'/training/data/raw/data/'

    os.environ['MODEL_PATH'] = base+'/training/deploy/model.h5'
    
    
    
    os.environ['HOST'] = "http://mlflow:5500"
    os.environ['PROJECT_NAME'] = "AbnormalityDetection"
    os.environ['EXPERIMENT_NAME'] = "ImageClassification"
    os.environ['MLFLOW_S3_ENDPOINT']='minio-ml-workshop:9000'
    os.environ['MLFLOW_S3_ENDPOINT_URL']='http://minio-ml-workshop:9000'
    os.environ['AWS_ACCESS_KEY_ID']='minio'
    os.environ['AWS_SECRET_ACCESS_KEY']='minio123'
    os.environ['AWS_REGION']='us-east-1'
    os.environ['AWS_BUCKET_NAME']='pred-maintianance-data'
    os.environ['OPENSHIFT_CLIENT_PYTHON_DEFAULT_OC_PATH']= '/tmp/oc'
    
    os.environ['CHECK_METRICS']  = 'val_loss'
    os.environ['CHECK_METRICS_MAX_OR_MIN']  = 'min'
    

    return SPLITE_RATE, OUTPUT_FEATURE_NAME, BATCH_SIZE, IMAGE_SIZE, INPUT_SHAPE,DROP_OUT_RATE, EPOCHS, SEED, TRAIN_DATA_FLAG, FINE_TUNE_FLAG
