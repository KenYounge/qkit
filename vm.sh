#!/bin/bash
#-----------------------------------------------------------------------------------------------------------------------
#  Start one or more VMs at Google to run a Jupyter Server. Output list of VMs and URLs to _urls.txt
#-----------------------------------------------------------------------------------------------------------------------
#
#  BEFORE YOU RUN THIS PROGRAM:
#
#      1. Open a Firewall in Google Cloud and allow HTTP incoming traffic
#
#         Go to VPC Network Console and select Firewall ( https://console.cloud.google.com/networking)

#         Create firewall rule to allow ingress on tcp:5000
#            Name:              jupyter
#            Network:           Default
#            Priority:          1000
#            Direction:         Ingress
#            Targets:           All instances in network
#            Filters:           IP ranges: 0.0.0.0/0
#            Protocols/ports:   Allow specified protocols and ports
#             ... then set:     tcp:5000
#
#      2. Add the lines below to the Jupyter config file on the disk image used by the vm,
#         so that the Jupyter Lab Server will listen on port 5000
#
#         The Jupyter config file is called  jupyter_notebook_config.py
#         and it is located in    ~/.jupyter/
#
#         c = get_config()
#         c.NotebookApp.ip = '*'
#         c.NotebookApp.open_browser = False
#         c.NotebookApp.port = 5000
#
#      3. Review the settings below for the Google Cloud project, image, etc.
#
#  USAGE:
#
#      Feed one email addresses to the script to start one Jupyter VM :
#
#         sh vm.sh bob.smith@company.com mary_jones@gmail.com      # feed individual entries
#
#      To feed a file of email addresses to start a Jupyter VMs for each one:
#
#         sh vm.sh "$(cat emails.txt)"
#
#      To record all activity into a log file:
#
#         sh vm.sh "$(cat emails.txt)" | tee log.txt


#-----------------------------------------------------------------------------------------------------
# Google Cloud Settings
#-----------------------------------------------------------------------------------------------------
project=dsfm-epfl
image=dsfm-latest-cpu
machine=n1-standard-4
region=europe-west1
zone=europe-west1-b
serviceaccount=387468781741-compute@developer.gserviceaccount.com

for email in "$@"
do

  vm_name=$(echo $email | tr '.' '-' | tr '_' '-' | tr '@' '-')  # Clean VM name of disallowed chars

  echo ' '
  echo ' '
  echo '------------------------------------------------------------------------------------------------------------------------------'
  echo 'STARTING VM for '$email
  echo '------------------------------------------------------------------------------------------------------------------------------'


  # Check if VM exists
  #-----------------------------------------------------------------------------------------------------
  vms=$(gcloud compute instances list --project=$project)
  if [[ "$vms" == *"$vm_name"* ]]; then
    echo ' '
    echo 'WARNING: A VM for '$vm_name' already exists. This will delete it and erase everything within the next 15 seconds !'
    echo ' '
    sleep 15
    gcloud compute instances delete --project=$project --zone=$zone --quiet $vm_name &
    sleep 60  # wait a bit for it to release
    gcloud compute addresses delete --project=$project --quiet $vm_name &
    sleep 60  # wait a bit for it to release
  fi


  # Reserve an "External IP Address" for that vm (so we can track it)
  #-----------------------------------------------------------------------------------------------------
  echo 'Reserving IP for ['$vm_name']...'
  gcloud compute addresses create $vm_name --project=$project --region=$region --network-tier=PREMIUM
  vm_ip=$(gcloud compute addresses list | grep -m 1 "RESERVED" | awk -v N=$N '{print $2}')
  echo 'Reserved IP ['$vm_ip'].'


  # Launch VM at that IP
  #-----------------------------------------------------------------------------------------------------
  echo 'Starting VM ['$vm_name']...'
  gcloud compute \
          instances create $vm_name \
          --project=$project \
          --zone=$zone \
          --service-account=$serviceaccount \
          --machine-type=$machine \
          --subnet=default \
          --network-tier=PREMIUM \
          --maintenance-policy=MIGRATE \
          --scopes=https://www.googleapis.com/auth/cloud-platform \
          --tags=http-server,https-server \
          --image=$image \
          --image-project=$project \
          --boot-disk-size=200GB \
          --boot-disk-type=pd-standard \
          --boot-disk-device-name=$vm_name \
          --address=$vm_ip
  sleep 60
  echo 'Created VM ['$vm_name'] at [http://'$vm_ip'].'


  # SSH to VM, create directories, give jupyter root access
  #-----------------------------------------------------------------------------------------------------
  echo 'Starting Jupyter...'
  nohup gcloud compute ssh $vm_name \
          --project $project \
          --zone $zone \
          --command "cd .. && sudo mkdir -p dsfm && cd dsfm && sudo /root/anaconda3/bin/jupyter lab --allow-root" \
     | tee "temp.tmp" &
  pid=$!
  sleep 60
  kill $pid


  # Get TOKEN
  #-----------------------------------------------------------------------------------------------------
  token=$(grep 'http://' "temp.tmp" | sed -e 's/^[ \t]*//' | awk 'NR==1 {print substr($0,length-47,48)}')
  if [ -e "nohup.out" ]; then
	  rm "temp.tmp"
  fi


  # Print Results
  #-----------------------------------------------------------------------------------------------------
  echo ' '
  echo 'Started Jupter !'
  echo ' '
  echo '    EMAIL:  '$email
  echo '    URL:    http://'$vm_ip':5000/?token='$token
  echo ' '
  echo '------------------------------------------------------------------------------------------------------------------------------'
  echo ' '
  echo ' '


  # Record URL in a file for later lookup
  #-----------------------------------------------------------------------------------------------------
  echo $email', http://'$vm_ip':5000/?token='$token >> "vm_list.txt"


done

exit