# Running the Interconnect Demo

Note this is almost identical to what you did when you ran this all in ROSA in the earlier demo [Running the inference demo](https://github.com/odh-labs/predictive-maint/blob/main/docs/image-detection-2-inference-demo.md)












================================================================================================================================

You should already have opened this page while [setting up the inference demo](https://github.com/odh-labs/predictive-maint/blob/main/docs/image-detection-1-inference-demo-setup.md). You should see yourself on the screen. 

**Click start** 

Keep yourself in the webcam frame. The page will begin capturing images and sending them to Kafka.
![images/2-setup/image20.png](images/2-setup/image20.png) 


## 2 - Start your Dashboard web page
Now it's time to start your Dashboard web page - to detect what the AI model is detecting in real time


You should already have opened this page while [setting up the inference demo](https://github.com/odh-labs/predictive-maint/blob/main/docs/image-detection-1-inference-demo-setup.md).

**Click Start** 


![images/2-setup/image29.png](images/2-setup/image29.png) 

The page will begin polling S3 object storage for what the AI is detecting. As you are being captured, ***Person*** will start incrementing every second. 

Put your hand in front of your webcam - so it's not seeing you. ***Background*** will start incrementing.

