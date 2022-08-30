import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa
import matplotlib.pyplot as plt
import sys
sys.path.append("..")

class buildModel():
    '''
    The model being used here is a modified U-Net. A U-Net consists of an encoder (downsampler) and decoder (upsampler). In-order to learn robust features and reduce the number of trainable parameters, you will use a pretrained model - EfficientNetV2B0 - as the encoder. For the decoder, you will use the upsample block, which is already implemented in the pix2pix example in the TensorFlow Examples repo. (Check out the pix2pix: Image-to-image translation with a conditional GAN tutorial in a notebook.)
    ----------

    Returns
    -------
    self.model:
        Deep learning based Model
    
    '''
    def __init__(self,dataAugmentation = None, inputShape=None, numClasses=None, topDropoutRate=None):
        self.input_shape = inputShape
        self.num_classes = numClasses
        self.top_dropout_rate = topDropoutRate
        self.data_augmentation = dataAugmentation
        
        
        
        ##self.base_model, self.layers, self.layer_names
        
    
    def dlModel(self):
        

        """
        ## Build a model
        We'll build a small version of the Xception network. We haven't particularly tried to
        optimize the architecture; if you want to do a systematic search for the best model
         configuration, consider using
        [KerasTuner](https://github.com/keras-team/keras-tuner).
        Note that:
        - We start the model with the `data_augmentation` preprocessor, followed by a
         `Rescaling` layer.
        - We include a `Dropout` layer before the final classification layer.
        """


        self.inputs = keras.Input(shape=self.input_shape)
        # Image augmentation block
        x = self.data_augmentation(self.inputs)

        model = EfficientNetB0(include_top=False, input_tensor=x, weights="imagenet")
        # Freeze the pretrained weights
        model.trainable = True

        # Rebuild top
        x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
        x = layers.BatchNormalization()(x)

        
        x = layers.Dropout(self.top_dropout_rate, name="top_dropout")(x)
        self.outputs = layers.Dense(self.num_classes, activation="softmax", name="pred")(x)

        self.model = keras.Model(self.inputs, self.outputs)




# keras.utils.plot_model(model, show_shapes=True)

    def defineModel(self):

        self.dlModel()
        self.compileModel()
            # self.clf.summary()
                
        
    def compileModel(self):
        '''
        Compile the model
        ----------
        
        Returns
        -------
        
        '''
        
        self.model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), loss='categorical_crossentropy',metrics=["accuracy"],
#               metrics=[
#                          # tf.keras.metrics.TrueNegatives(name='True_Negatives'),
#               # tf.keras.metrics.FalseNegatives(name='False_Negatives'),
#               # tf.keras.metrics.TruePositives(name='True_Positives'),
#               # tf.keras.metrics.FalsePositives(name='False_Positives'),
#               tf.keras.metrics.Precision(name='Precision'),
#               tf.keras.metrics.Recall(name='Recall'),
#               tfa.metrics.F1Score(self.num_classes, name='F1Score', average="micro")]
                          
                          )    
    

    
    def setupModel(self):
        '''
        Build the model
        ----------
        
        Returns
        -------
        
        '''
        self.defineModel()

        return self.model