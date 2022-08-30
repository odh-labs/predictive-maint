# On Virtual Box
1. Install Virtualbox guest additions for linux. 
- [Outside VM] In VM toolbar, go to Devices->'Insert Guest Addition CD image'. 
- [Inside VM] Open Files and go to mounted CD. Open it in terminal and run `sudo ./VBoxLinuxAdditions.run`
2. Install extension pack from https://www.virtualbox.org/wiki/Downloads. You need this to access webcam. Make sure on Mac that VirtualBox can access the Camera


# Set up the Fedora VM
CPU: 4 cores. 
RAM: 4Gb. 
Storage: 15 Gb. 

During OS installation create account with following:   
username: redhat  
password: redhat  

# Update and install packages
```sh
sudo dnf update
```

```sh
sudo dnf install vim golang opencv* make automake gcc gcc-c++ kernel-devel  
```

# Get repo
```sh
git clone https://github.com/odh-labs/predictive-maint.git  
cd ~
cd predictive-maint  
```

## Setting up Rhoas cli
```sh
curl -o- https://raw.githubusercontent.com/redhat-developer/app-services-cli/main/scripts/install.sh | bash 
``` 
Open file by running `sudo vim ~/.bash_profile` and add `/home/redhat/.local/bin` at the end of the file    

Test rhoas cli. 
``` sh
rhoas version  
```

## Setting up oc cli
Download `Openshift v4.10 Linux Client ` from `https://access.redhat.com/downloads/content/290/ver=4.10/rhel---8/4.10.26/x86_64/product-software`  

```sh
cd ~/Downloads/  
tar xvzf oc-4.10.26-linux.tar.gz  
cp oc  /home/redhat/.local/bin/  
```

Test oc cli
```sh
oc status
```

## Create Kafka instance and update variables in 'consumer-deployment.yaml' file
```sh
cd ~/predictive-maint/deploy/  
./kafka.sh  
```

## Deployments on Openshift
> login to oc cluster  
```sh
export USER=<user2>  
oc new-project a-predictive-maint-$USER  
oc delete limits a-predictive-maint-$USER-core-resource-limits  

cd ~/predictive-maint/deploy/  
oc apply -f minio-full.yaml  
oc apply -f Seldon-Deployment.yaml  
oc apply -f consumer-deployment.yaml  
```

## Start capturing camera feed
Load env variables  
```sh
cd ~/predictive-maint/deploy/
export CLIENT_ID=$(cat credentials.json | jq  --raw-output '.clientID')
export CLIENT_SECRET=$(cat credentials.json | jq  --raw-output '.clientSecret')
export KAFKA_BROKER_URL=$(rhoas status -o json  | jq --raw-output '.kafka.bootstrap_server_host')
```
Start Capturing camera feed.  

- [Outside VM] In VM toolbar, go to Devices->Webcams and check the Camera ('FaceTime HD Camera' in case of MacOs). 
```sh
cd ~/predictive-maint/event-producer 
go run -v .
```
  
