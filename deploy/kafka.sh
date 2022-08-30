# Prior to running this script, you need to do the following
# 1) Run this to download the Red Hat OpenShift Application Services (RHOAS) Command Line Interface (CLI)
#    curl -o- https://raw.githubusercontent.com/redhat-developer/app-services-cli/main/scripts/install.sh | bash
# 2) Export the location of the RHOAS CLI to your system PATH, 
#    e.g. on mac that's done as follows:
#    export PATH=%PATH%:/Users/<INSERT YOUR USERNAME HERE>/bin
# 3) Create a Red Hat Account - where the SaaS service, Red Hat OpenShift Service for Apache Kafka is located
#    Do that here:
#    http://console.redhat.com



KAFKA_NAME='kafka-rocks'
TOPIC_NAME='video-stream'



export RHOAS_TELEMETRY=true

rhoas login

rhoas --version

rhoas kafka create --name ${KAFKA_NAME}

rhoas context set-kafka --name ${KAFKA_NAME}

while true
do
  STATUS=$(rhoas status)
  PROV='provisioning'
  READY='ready'

  if [[ "$STATUS" == *"$PROV"* ]]; then
    echo "Provisioing"
  elif [[ "$STATUS" == *"$READY"* ]]; then
    echo "Ready"
    break
  fi
  sleep 5
done

rhoas kafka topic create --name ${TOPIC_NAME}

rhoas service-account create --file-format json --short-description="${KAFKA_NAME}-service-account" --overwrite

sleep 10


export CLIENT_ID=$(cat credentials.json | jq  --raw-output '.clientID')
export CLIENT_SECRET=$(cat credentials.json | jq  --raw-output '.clientSecret')

echo "$CLIENT_ID"
echo "$CLIENT_SECRET"

#validate service account is created
rhoas service-account list | grep "${KAFKA_NAME}-service-account"

#rhoas kafka acl grant-access --consumer --producer --service-account "${CLIENT_ID}" --topic-prefix '*'  --group all  -y
#rhoas kafka acl grant-access --consumer --producer --service-account "${CLIENT_ID}" --topic-prefix 'video-stream'  --group all  -y
rhoas kafka acl grant-access --consumer --producer --service-account "${CLIENT_ID}" --topic-prefix  "${TOPIC_NAME}" --group all  -y

#print the status
rhoas status -o json

export KAFKA_BROKER_URL=$(rhoas status -o json  | jq --raw-output '.kafka.bootstrap_server_host')
echo "$KAFKA_BROKER_URL"

#change the consumer deployment yaml file

sed -i "s/SASL_USERNAME_VALUE/${CLIENT_ID}/g" consumer-deployment.yaml
sed -i "s/SASL_PASSWORD_VALUE/${CLIENT_SECRET}/g" consumer-deployment.yaml
sed -i "s/KAFKA_BROKER_VALUE/${KAFKA_BROKER_URL}/g" consumer-deployment.yaml

# Mac (sed has peculiarities - use gnu-sed)
# run: brew install gnu-sed 
# see: https://blog.birost.com/a?ID=00900-c6ae76a9-d665-4d1a-9fa8-0f962b6385e6 
# gsed -i "s/SASL_USERNAME_VALUE/${CLIENT_ID}/g" consumer-deployment.yaml
# gsed -i "s/SASL_PASSWORD_VALUE/${CLIENT_SECRET}/g" consumer-deployment.yaml
# gsed -i "s/KAFKA_BROKER_VALUE/${KAFKA_BROKER_URL}/g" consumer-deployment.yaml

