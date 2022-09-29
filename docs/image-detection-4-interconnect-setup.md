# Setting up the Interconnect Demo


## 1 - Create an OpenShift Cluster

## 2 - Install the dashboard in a new namespace on the new cluster
oc new-project frontend
oc new-app https://github.com/odh-labs/predictive-maint.git  --context-dir=dashboard  --name=dashboard -e MINIO_URL=http://minio-ml-workshop:9000
oc create route edge --service=dashboard

## 3 - Install Skupper on both OpenShift Clusters
Install Skupper in Openshift namespaces within each
https://skupper.io/start/index.html

curl https://skupper.io/install.sh | sh

oc login <cluster-1>
oc project <namespace>
skupper init

oc login <cluster-2>
oc project <namespace>
skupper init

## 4 - Link Skupper

Login to the skupper consoles on both namespaces
Link the namespaces by copying the token and pasting into the other

## 5 - Expose MINIO service

Expose the minio service with HTTP on port 9000.


## 6 - Check the dashboard connects

Now find the dashboard and check it connects to the minio service

## 7 - Scale down the old dashboard

You can now scale down the initial dashboard deployed in the first cluster.

