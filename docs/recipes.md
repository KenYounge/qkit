# Recipes for Common Tasks


## Google Compute

#### Select a VM image

  - An all-around image for machine learning:

        common-cpu

  - Tensorflow Images:
    
        tf2-latest-gpu
        tf2-latest-cpu
        tf-latest-gpu
        tf-latest-cpu
    
  - XGBoot images:
    
        xgboost-latest-gpu-experimental
        xgboost-latest-cpu-experimental

#### Create a VM

  - Instructions assume that the VM should be named `vm`

  - When using Google Dev Console, setup a new VM as follows:

        name:           vm
        zone:           europe-west1-d
        machine type:   n1-highcpu-8
        boot disk:      OS image = Debian GNU/Linux 10
        boot type:      SSD
        boot size:      500 GB
        svc acct:       enable default service account
        scopes:         enable all scopes
        restart:        disable auto restart
        maintenance:    migrate

  - Command-line for the above for a new VM called "vm"  (PASTE SPECIAL without newlines)

        gcloud compute instances create "vm"
            --boot-disk-device-name "vm"
            --project NAME-OF-PROJECT
            --zone "europe-west1-d"
            --machine-type "n1-highcpu-16"
            --subnet "default"
            --no-restart-on-failure
            --maintenance-policy "MIGRATE"
            --scopes default="https://www.googleapis.com/auth/cloud-platform"
            --image "common-cpu"
            --boot-disk-size "500"
            --boot-disk-type "pd-ssd"

  - Standard Machine Types:

        n1-standard-1 , 2, 4, 8, 16, 32
        n1-highmem-2  ,    4, 8, 16, 32
        n1-highcpu-2  ,    4, 8, 16, 32

#### Run Jupyter Server on VM

  - Start the VM with `Allow HTTP and HTTPS traffic` enabled

  - Set IP addresses to static and assign to VM

  - SSH into the VM

        gcloud compute ssh vm --project NAME-OF-PROJECT --zone europe-west1-d
        sudo -s
        
        cd ~ , 
        screen
    
        git clone https://github.com/KenYounge/qkit.git
        jupyter lab --allow-root


#### Configure UNIX

  - Login with ssh

        gcloud compute ssh vm --project NAME-OF-PROJECT --zone europe-west1-d
        sudo -s

  - Setup GCP 

        gcloud config set project NAME-OF-PROJECT
        gcloud config set compute/zone europe-west1-d

  - Setup git

        apt-get install -y git
        git config --global credential.helper cache
        git config --global user.name "GITHUB-USERNAME"
        git config --global user.email "GITHUB-EMAIL-ADDRESS"
        echo "machine github.com login GITHUB-EMAIL-ADDRESS password THEPASSWRD" >> ~/.netrc
        echo "machine github.com login GITHUB-EMAIL-ADDRESS password THEPASSWRD" >> /.netrc

  - Clone qkit  

        cd /
        git clone https://github.com/KenYounge/qkit.git

  - Setup UNIX

        bash /qkit/setup_unix.sh
        export PATH="/anaconda/bin:$PATH"     # may need to run manually


#### Update UNIX

  - Start VM

        gcloud compute instances start vm --project NAME-OF-PROJECT --zone europe-west1-d

  - Log into VM

        gcloud compute ssh vm --project NAME-OF-PROJECT --zone "europe-west1-d"
        sudo -s
        cd /

  - Install Ubuntu packages

        apt-get install -y  _______        # enter the package name
    
  - Install or upgrade pip packages
    
        pip install --upgrade _______      # enter the package name

#### Save a disk image

  - Delete the VM instance, but LEAVE the boot disk soit can be re-used...

        gcloud compute instances delete vm --keep-disks boot --project NAME-OF-PROJECT --zone europe-west1-d

  - Copy boot disk into image

        gcloud compute images delete boot-disk --project NAME-OF-PROJECT
        gcloud compute images create boot-disk --source-disk vm --project NAME-OF-PROJECT --source-disk-zone europe-west1-d

  - Archive a versioned copy of image (increment boot-disk-### ... )

        gcloud compute images create boot-disk-003 --source-disk vm --project NAME-OF-PROJECT --source-disk-zone europe-west1-d

  - Delete old boot disk

        gcloud compute disks delete vm --project NAME-OF-PROJECT --zone europe-west1-d

#### A typical workflow to run a python program on a VM

  - Start VM

    Use PASTE SPECIAL (without newlines) to start a VM called "vm"

        gcloud compute instances create "vm"
            --boot-disk-device-name "vm"
            --project NAME-OF-PROJECT
            --zone "europe-west1-d"
            --machine-type "n1-highmem-16"
            --subnet "default"
            --no-restart-on-failure
            --maintenance-policy "MIGRATE"
            --scopes default="https://www.googleapis.com/auth/cloud-platform"
            --image "/NAME-OF-PROJECT/boot-disk"
            --boot-disk-size "20"
            --boot-disk-type "pd-ssd"

  - Connect to VM  
  
        gcloud compute ssh vm --project NAME-OF-PROJECT --zone europe-west1-d  
        sudo -s  
    
  - Start a screen session so you can reconnect later
    
        screen  

  - Clone your project

        cd /
        git clone https://github.com/KenYounge/REPO-PROJECT.git
        cd /REPO-PROJECT

  - Execute your program

        export PATH="/anaconda/bin:$PATH"
        python PROGRAM.py

  - Copy output to a Google Cloud Storage bucket so you can get to it later

        gsutil -m cp ~* gs://BUCKETNAME

### gcloud

  - View serial output:     
  
        gcloud compute instances get-serial-port-output INSTANCENAME --zone "europe-west1-d"
    
  - Set metadata:          
   
        gcloud compute  ....somestuf....  --metadata "codeno=1234567890123456"
    
  - Send file(s) to VM:       
  
        gcloud compute copy-files ~/local-dir/file-1 VMNAME:~/remote-destination
    
  - copy file(s) from VM:     
  
        gcloud compute copy-files VMNAME:/gce/FILENAME ~/LOCALDIR

  - re-run the startup script (the one that ran when you booted the VM)     
  
        sudo /usr/share/google/run-startup-scripts

  - attach another disk to a Google Compute VM 
                                
        mkdir /mnt/MOUNTNAME
        /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/sdb /mnt/MOUNTNAME
        chmod a+w /mnt/MOUNTNAME


### gsutils

  - Copy local to cloud   
    
        gsutil -m cp . gs://bucketname   this runs in parallel and copys everything in cur dir
    
  - Copy cloud to cloud    
   
        gsutil -m cp gs://bucketname/* gs://bucketname
    
  - Move local to cloud     
  
        gsutil -m mv . gs://bucketname   this runs in parallel and copys everything in cur dir
    
  - Remove all in bucket    
  
        gsutil -m rm -R gs://bucketname/
    
  - Synch s3 and google     
  
        gsutil rsync -d -r s3://my-s3-bucket gs://my-gcs-bucket


## UNIX

  - `nano`                a simple text editor in terminal

  - `head -n 1000`        to list begining of a file (or cat <file> | head -n 1000)  
  
  - `tail -n 1000`        to list tail of a file (or cat <file> | tail -n 1000)  
    
  - `rm -rf`              to force remove the entire directory 
  
        rm -rf tools/
    
  - `apt-get`             to manually remove locks if if apt-get hangs...
                                
        sudo rm /var/lib/dpkg/lock
        sudo rm /var/cache/apt/archives/lock
    
  - `curl`                to use curl in bash scripts:  
  
        VALUE_OF_FOO=$(curl http://metadata/computeMetadata/v1/instance/attributes/foo -H "Metadata-Flavor: Google")
        number of arguments are in the special variable $ and variables $@ and $* return all arguments

  - `screen` - keep bash and ssh sessions alive and then reconnect    
  
        screen -list      to list out running screen sessions  
        
        screen -R         to resume  the  youngest  (by creation time) session
                                  if necessary detach and logout remotely first.
                                  if it was not running create it and notify the user.
        
        screen -r [pid]   to reconnect to a specific session
        
        ctrl-a d          to detatch within screen (Hold ctrl press a, let go ctrl, press d)

  - `git config --global credential.helper store` to store your git credentials 


### Misc UNIX Commands

    which python
	
    which python3
	
    python --version
	
    python3 --version

    source myenv/bin/activate   # Activate an environment

### conda

List conda environments

    conda info --envs

List conda environments  

    conda env list
    
Create a new conda environment

    conda create -n myenv
    
    conda create -n myenv python=3.6
    
Activate a conda environment
    
    conda activate myenv

Delete an entire conda environment

    conda remove --name ENVNAME --all
    
Deactive (the currently active) conda environment  

    conda deactivate   # will probably activate Python 2.7 from Apple Mac OS
    
### Virtual Environments

Python works better when every project has its own `venv` virtual environment.
To use one, you first have to start it (often just inside the local project directory).

    python -m venv myenv

After it is constructed, you then need to tell UNIX that is is active.

    source myenv/bin/activate
   
    
## Jupyter

Install the ipython kernel package so you can manage kernels and environments
    
    pip install --user ipykernel
    
Install a virtual environment in Jupyter

    python -m ipykernel install --user --name= myenv
    
The above results in this environment being available in Jupyter

    Installed kernelspec myenv in /Users/younge/Library/Jupyter/kernels/myenv
    
    
#### Remove an environment from Jupyter

List environments in Jupyter with:

    jupyter kernelspec list

This should return something like:

	Available kernels:
	  myenv      /home/user/.local/share/jupyter/kernels/myenv
	  python3    /usr/local/share/jupyter/kernels/python3

To uninstall the kernel, you can type:

    jupyter kernelspec uninstall myenv
   

## MySQL

  - Documentation  
  
     - User Guide:    http://mysql-python.sourceforge.net/MySQLdb.html
     - API doc:       http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
     - Manual:        http://dev.mysql.com/doc/refman/5.5/en/index.html
     - SQL Syntax:    http://dev.mysql.com/doc/refman/5.5/en/sql-syntax.html

  - Installation on Mac           
  
        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        brew install mysql
        export PATH=$PATH:/usr/local/mysql/bin
        pip install MySQL-Python

  - Command-line 
  
        mysql --host=173.194.226.164 --user=root --password

