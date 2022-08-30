import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix,PrecisionRecallDisplay

# visualizeData( data = None,dataAugmentation = None,  cm_data = None, y_true = None, y_pred = None).showImages()
class visualizeData():
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
    def __init__(self, data = None, dataAugmentation = None,augFlag = False, cm_data = None, y_true = None, y_pred = None, modelType=None):
        
        self.data_augmentation = dataAugmentation
        self.aug_flag  = augFlag
        self.data = data
        self.cm= cm_data
        self.modelType = modelType
        self.y_pred = y_pred
        self.y_true = y_true
        
        
        
        
    def showImages(self):    
        """
        ## Visualize the data
        Here are the first 9 images in the training dataset. As you can see, label 1 is "dog"
         and label 0 is "cat".
        """


        plt.figure(figsize=(10, 10))
        for images, labels in self.data.take(1):
            for i in range(9):
                ax = plt.subplot(3, 3, i + 1)
                if self.aug_flag ==True:
                    
                    img = self.data_augmentation(images)
                    img = img[0]
                    
                else:
                     img = images[i] 
                plt.imshow(img.numpy().astype("uint8"))
                plt.title(int(labels[i]))
                plt.axis("off")
        plt.show()
            
            
            
    def confusionMatrixPlot(self):
        
        plt.figure(figsize=(8,6))
        sns.set(font_scale=1.2)
        sns.heatmap(self.cm, annot=True, fmt = 'g', cmap="Reds", cbar = False)
        plt.xlabel("Predicted Label", size = 18)
        plt.ylabel("True Label", size = 18)
        plt.title("Confusion Matrix Plotting for "+ self.modelType +"  model", size = 20)
        
        self.current_path= os.getcwd()
        self.inference_path = self.current_path.replace('notebooks','reports')+'/figures/'
        
        
        plt.savefig(self.inference_path+'confusionMatrixPlot'+'_'+self.modelType+'.png')
        plt.show()
        
    def precisionRecallDisplay(self):
        PrecisionRecallDisplay.from_predictions(self.y_true, self.y_pred)
        
        self.current_path= os.getcwd()
        self.inference_path = self.current_path.replace('notebooks','reports')+'/figures/'
        
        plt.savefig(self.inference_path+'PrecisionRecallDisplay'+'_'+self.modelType+'.png')
        plt.show()


  