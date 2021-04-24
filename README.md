# The `qkit` Toolkit

Copyright (c) 2020 by Kenneth A. Younge.
( https://kenneth.younge.net/  and https://github.com/KenYounge/ )  
  
Access to this code is provided under an MIT License.

This repository provides tools and utilities in Python 3 to use in other projects. the Readme also documents common "recipes" that I use (but frequently forget) with respect to how to work with Google Cloud, UNIX, etc. 


#### Installation

  - Clone from GitHub into a directory in your project.

        git clone https://github.com/KenYounge/tools.git

  - Install the requirements:

        pip install -r tools/requirements.txt

#### Usage

  - Import the module `tools` (or alternatively select and import the individual modules you want to use):

        import tools

  - or 

        from tools import ui


## Recipes for Google Compute

#### Create a VM

  - Instructions assume that the VM should be named `vm`

  - Use Google Dev Console to setup a new VM as follows:

        name:           vm
        zone:           europe-west1-d
        machine type:   n1-highcpu-8
        boot disk:      tis-boot-disk
                        or start fresh with OS image = debian (NOT backports)
        boot type:      SSD
        boot size:      500 GB
        svc acct:       enable default service account
        scopes:         enable all scopes
        restart:        disable auto restart
        maintenance:    migrate

  - Command-line for the above for VM "tis-vm"  (PASTE SPECIAL without newlines)

        gcloud compute instances create "vm"
            --boot-disk-device-name "vm"
            --project "epfl-cdm-tis"
            --zone "europe-west1-d"
            --machine-type "n1-highcpu-16"
            --subnet "default"
            --no-restart-on-failure
            --maintenance-policy "MIGRATE"
            --scopes default="https://www.googleapis.com/auth/cloud-platform"
            --image "/epfl-cdm-tis/tis-boot-disk"
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

        gcloud compute ssh vm --project epfl-cdm-tis --zone europe-west1-d
        sudo -s
        
        cd ~ , 
        screen
        git clone https://github.com/KenYounge/tools.git
        jupyter lab --allow-root




#### Configure Ubuntu on a new VM

  - Login with ssh

        gcloud compute ssh tis-vm --project epfl-cdm-tis --zone europe-west1-d
        sudo -s
        cd /

  - Set GCP defaults

        gcloud config set project epfl-cdm-tis
        gcloud config set compute/zone europe-west1-d

  - Setup git

        apt-get install -y git
        git config --global credential.helper cache
        git config --global user.name "tislab"
        git config --global user.email "epfl.tis.lab@gmail.com"
        echo "machine github.com login epfl.tis.lab@gmail.com password THEPASSWRD" >> ~/.netrc
        echo "machine github.com login epfl.tis.lab@gmail.com password THEPASSWRD" >> /.netrc

  - Clone pytis git repo

        git clone https://github.com/epfl-tis/pytis.git

  - Install libraries

        bash /pytis/vm_config.sh
        export PATH="/anaconda/bin:$PATH"     # may need to run manually

#### Update Ubuntu OS on a VM

  - Start VM

        gcloud compute instances start tis-vm --project epfl-cdm-tis --zone europe-west1-d

  - Log into VM

        gcloud compute ssh tis-vm --project "epfl-cdm-tis" --zone "europe-west1-d"
        sudo -s
        cd /

  - Install and/or upgrade changes to OS

        apt-get install -y  ????      do what you want to update or add to OS
        pip install --upgrade ????    do what you want to update or add to OS

#### Save a disk image

  - Delete VM instance, but leave boot disk

        gcloud compute instances delete tis-vm --keep-disks boot --project epfl-cdm-tis --zone europe-west1-d

  - Copy boot disk into image

        gcloud compute images delete tis-boot-disk --project epfl-cdm-tis
        gcloud compute images create tis-boot-disk --source-disk tis-vm --project epfl-cdm-tis --source-disk-zone europe-west1-d

  - Archive a versioned copy of image (increment tis-boot-disk-### ... )

        gcloud compute images create tis-boot-disk-003 --source-disk tis-vm --project epfl-cdm-tis --source-disk-zone europe-west1-d

  - Delete old boot disk

        gcloud compute disks delete tis-vm --project epfl-cdm-tis --zone europe-west1-d

#### Manually run a python program on a VM

  - Start VM

    Use PASTE SPECIAL (without newlines) to start a VM called "vm"

        gcloud compute instances create "vm"
            --boot-disk-device-name "vm"
            --project "epfl-cdm-tis"
            --zone "europe-west1-d"
            --machine-type "n1-highmem-16"
            --subnet "default"
            --no-restart-on-failure
            --maintenance-policy "MIGRATE"
            --scopes default="https://www.googleapis.com/auth/cloud-platform"
            --image "/epfl-cdm-tis/tis-boot-disk"
            --boot-disk-size "20"
            --boot-disk-type "pd-ssd"

  - Connect to VM  
  
        gcloud compute ssh tis-vm --project epfl-cdm-tis --zone europe-west1-d  
        sudo -s  
        screen  

  - Update the `tools` repo

        cd /tools/
        git pull

  - Execute your program

        export PATH="/anaconda/bin:$PATH"
        python PROGRAM.py

  - Copy output to a Google Cloud Storage bucket

        gsutil -m cp ~* gs://BUCKETNAME

### gcloud

  - view serial output:     
  
        gcloud compute instances get-serial-port-output INSTANCENAME --zone "europe-west1-d"
    
  - set metadata:          
   
        gcloud compute  ....somestuf....  --metadata "codeno=1234567890123456"
    
  - send files to VM:       
  
        gcloud compute copy-files ~/local-dir/file-1 VMNAME:~/remote-destination
    
  - copy files from VM:     
  
        gcloud compute copy-files VMNAME:/gce/FILENAME ~/LOCALDIR

  - re-run startup       
  
        sudo /usr/share/google/run-startup-scripts

  - attach disks in compute engine
                                
        mkdir /mnt/MOUNTNAME
        /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/sdb /mnt/MOUNTNAME
        chmod a+w /mnt/MOUNTNAME


### gsutils

  - copy local to cloud   
    
        gsutil -m cp . gs://bucketname   this runs in parallel and copys everything in cur dir
    
  - copy cloud to cloud    
   
        gsutil -m cp gs://bucketname/* gs://bucketname
    
  - move local to cloud     
  
        gsutil -m mv . gs://bucketname   this runs in parallel and copys everything in cur dir
    
  - remove all in bucket    
  
        gsutil -m rm -R gs://bucketname/
    
  - synch s3 and google     
  
        gsutil rsync -d -r s3://my-s3-bucket gs://my-gcs-bucket


## Recipes for UNIX

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


### Other Misc UNIX Commands

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
    
### `venv` Virtual Environments

    python -m venv myenv

    source myenv/bin/activate
   
    
## Recipes for Jupyter


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
   

## Recipe for MySQL

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


## Distributing packages through PyPI.org

Instructions: https://packaging.python.org/tutorials/packaging-projects/


#### Install utilities

    pip install --upgrade setuptools    
    pip install --upgrade build
    pip install --upgrade twine          


#### Link raw code (in a github repo) to a build directory

For example, for the project "passcode" we execute:

    ln -s /Users/USERHOME/projects/passcode/github/passcode/__init__.py /Users/USERHOME/projects/passcode/passcode/__init__.py


#### Build

  Run this in the directory with `setup.py`

    python setup.py sdist bdist_wheel

This should output a lot of text and then generate two files in the dist directory:

    dist/
      passcode-0.1.2-py3-none-any.whl
      passcode-0.1.2.tar.gz


#### Publish

    python -m twine upload dist/*