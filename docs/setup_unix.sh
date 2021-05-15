#! /bin/bash

#=======================================================================================================================
#
#   SETUP A UBUNTU VM
#
#=======================================================================================================================


#---------------------------------------------------------
#  UBUNTU PACKAGES
#---------------------------------------------------------

    apt-get update
    apt-get install -y build-essential
    apt-get install -y sysstat
    apt-get install -y git
    apt-get install -y zip
    apt-get install -y unzip
    apt-get install -y python-pip
    apt-get install -y python-dev
    apt-get install -y libmysqlclient-dev
    apt-get install -y mysql-client
    apt-get install -y python-setuptools
    apt-get install -y screen
    apt-get install -y python-html5lib
    apt-get install -y python-lxml
    apt-get install -y python-beautifulsoup
    apt-get install -y python-numpy
    apt-get install -y python-scipy
    apt-get install -y python-matplotlib
    apt-get install -y ipython
    apt-get install -y ipython-notebook
    apt-get install -y python-pandas
    apt-get install -y python-sympy
    apt-get install -y python-nose
    apt-get install -y python-service-identity     # for gcloud support of .p12 keys
    apt-get install -y wkhtmltopdf
    apt-get install -y xfonts-75dpi
    apt-get install -y fonts-cmu
    apt-get install -y libjpeg-dev
    apt-get install -y libfreetype6
    apt-get install -y libfreetype6-dev
    apt-get install -y libatlas-dev
    apt-get install -y libatlas3gf-base
    apt-get install -y parallel
    apt-get install -y python3-tk
    apt-get install -y libhdf5-serial-dev
    apt-get install -y libatlas-dev
    apt-get install -y libatlas3gf-base
    apt-get install -y fonts-cmu
    apt-get install -y cm-super
    apt-get install -y graphviz
    apt-get install -y enchant


#---------------------------------------------------------
#  EASY INSTALL PACKAGES
#---------------------------------------------------------

    easy_install -U distribute
    apt-get remove -y python-pip
    easy_install pip


#---------------------------------------------------------
#  PIP PACKAGES
#---------------------------------------------------------

    pip install --upgrade pip
    pip install --upgrade google-cloud
    pip install --upgrade google-api-python-client
    pip install --upgrade gcsfs
    pip install --upgrade googledatastore
    pip install --upgrade mysql-connector-python
    pip install --upgrade MySQL-python
    pip install --upgrade sendgrid
    pip install --upgrade psutil
    pip install --upgrade requests
    pip install --upgrade crcmod
    pip install --upgrade httplib2
    pip install --upgrade httplib2.ca_certs_locater
    pip install --upgrade beautifulsoup4
    pip install --upgrade cython
    pip install --upgrade line_profiler
    pip install --upgrade numexpr
    pip install --upgrade tables
    pip install --upgrade pandas
    pip install --upgrade statsmodels
    pip install --upgrade xgboost
    pip install --upgrade pdfkit jinja2
    pip install --upgrade futures
    pip install --upgrade wordcloud
    pip install --upgrade rpy2
    pip install --upgrade pandas
    pip install --upgrade numexpr
    pip install --upgrade pandas
    pip install --upgrade statsmodels
    pip install --upgrade cvxopt
    pip install --upgrade python-Levenshtein
    pip install --upgrade pyxDamerauLevenshtein
    pip install --upgrade tqdm
    pip install --upgrade pyenchant
    pip install --upgrade ystockquote
    pip install --upgrade pydataset
    pip install --upgrade mlxtend
    pip install --upgrade streamlit
    pip install --upgrade certifi
    pip install --upgrade tabulate
    pip install --upgrade u8darts
    pip install --upgrade pystan
    pip install --upgrade gluonts
    pip install --upgrade fbprophet
    pip install --upgrade mxnet
    pip install --upgrade pygame


#-------------------------------------------------------------------------------
#  GOOGLE CLOUD
#-------------------------------------------------------------------------------

    curl https://sdk.cloud.google.com | bash
    source ~/.bashrc         # the gcloud installer modifies the PATH
    source ~/.bash_profile   # the gcloud installer modifies the PATH


#-------------------------------------------------------------------------------
#  ANACONDA
#-------------------------------------------------------------------------------

    cd /tmp
    wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh
    bash Anaconda3-5.3.0-Linux-x86_64.sh
    conda create --name python3 python=3
    export PATH="/anaconda3/bin:$PATH"
    export PYTHONPATH="/anaconda3/bin:PYTHONPATH"
    source ~/.bashrc


#-------------------------------------------------------------------------------
#  CONDA LIBRARIES
#-------------------------------------------------------------------------------

    conda update -y -n base conda
    conda install -y pandasql
    conda install -y -f python-levenshtein

#-------------------------------------------------------------------------------
#  CONDA-FORGE LIBRARIES
#-------------------------------------------------------------------------------

    conda config --add channels conda-forge
    conda install -y -c conda-forge scikit-optimize
    conda install -y -c conda-forge scikit-image
    conda install -y -c conda-forge statsmodels
    conda install -y -c conda-forge PyMySQL
    conda install -y -c conda-forge gensim
    conda install -y -c conda-forge tensorflow
    conda install -y -c conda-forge keras
    conda install -y -c conda-forge xgboost
    conda install -y -c conda-forge plotly
    conda install -y -c conda-forge networkx
    conda install -y -c conda-forge lightgbm
    conda install -y -c conda-forge textblob
    conda install -y -c conda-forge scrapy
    conda install -y -c conda-forge nodejs
    conda install -y -c conda-forge pydot
    conda install -y -c conda-forge basemap
    conda install -y -c conda-forge folium
    conda install -y -c conda-forge spacy
    conda install -y -c conda-forge emcee
    conda install -y -c conda-forge tika
    conda install -y -c conda-forge nltk
    conda install -y -c conda-forge psutil


#-------------------------------------------------------------------------------
#  FINAL CONFIGURATION
#-------------------------------------------------------------------------------

    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales
    source ~/.bashrc         # the gcloud installer modifies the PATH
    source ~/.bash_profile   # the gcloud installer modifies the PATH

