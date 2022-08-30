FROM quay.io/ml-aml-workshop/python:3.7-slimv2

WORKDIR /microservice
COPY requirements.txt /microservice/
RUN pip install -r requirements.txt
RUN pip install seldon-core
RUN pip install joblib
RUN pip install scikit-learn
RUN pip install tensorflow
RUN pip install pandas

COPY Predictor.py   model.h5  /microservice/

ENV PERSISTENCE 0
CMD seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --grpc-port ${GRPC_PORT} --metrics-port ${METRICS_PORT} --http-port ${HTTP_PORT}
