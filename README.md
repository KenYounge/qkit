# `qkit` - Quant AI Toolkit

Copyright (c) 2021 by Kenneth A. Younge.  

This repository provides python code and utilities used in our research.  

	AUTHOR:  Kenneth A. Younge  
	SOURCE:  https://github.com/KenYounge/qkit/  
	LICENSE: Access to this code is provided under an MIT License.  


## Install

### Install with `pip`

        pip install qkit

### Or include into your project

  - Clone from GitHub

        git clone https://github.com/KenYounge/qkit.git
        cd qkit    
    
  - Create and activate a virtual environment
            
        python3 -m venev venev
        . venv/bin/activate

  - Install supporting packages  
            
        pip install -r requirements.txt

## Usage

  - Import `qkit`

        import qkit

  - Or import individual modules that you want to use
    
        from qkit import fio
        from qkit.passcode import passcode


## `/docs/`

The `/docs/` directory contains aditional documentation for: 

  * [recipes.md](recipes.md) Instructions for tasks that are easy to forget.

  * [requirements_extra.txt](requirements_extra.txt) List of all pip packages used across Quant AI. 

  * [setup_osx.md](setup_osx.md) Instructions to setup and configure a new Macbook M1 (for fast recovery).

  * [setup_unix.sh](setup_unix.sh) Bash script to setup and configure a Ubuntu LINUX server.


