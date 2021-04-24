--------------------------------------------------------------------------------

# Help file to setup a new Mac OSX M1 Computer  

--------------------------------------------------------------------------------

The following document sets forth a bare-metal process for completely installing a new Mac OSX Big Sur 11.2.3 M1 computer to return to operation as quickly as possible.

## Xcode

#### Download and install Xcode from the Apple store

Do this first, before anything else! Other dev apps require Xcode to be installed first. 

Be sure to run Xcode at least one time and accept license agreement. If you do not, then it will hang when other apps try to call XCODE and it waits for license to validate!

From time to time, upgrade to the latest version of XCODE. But then be sure to run Xcode again and accept the license again, or programs may hang while waiting for the XCODE license to validate. 

#### Install XCODE command-line tools

	xcode-select --install
	
The above step is required on MacOS to set up local development utilities, including "many commonly used tools, utilities, and compilers, including make, GCC, clang, perl, svn, git, size, strip, strings, libtool, cpp, what, and many other useful commands that are usually found in default Linux installations,"

If the above commandline instructions fails, then you can also directly sign into Apple Developer and download the tools installation DMG from:

	https://developer.apple.com/download/more/


## Rosetta 2

Mac uses "Rosetta 2" to translate legacy code for Intel CPUs over to M1 (or "Apple Silicon"). When you install Xcode, and then run Xcode, it should automatically prompt you to install Rosetta. But if it does not, then you can do it directly by running this:

	softwareupdate --install-rosetta


## Enable Mac OSX System Extensions

If you use Google Drive for Desktop (or other kernel extensions) then (as of Big Sur) you need to enable "OSX System Extensions." To do that, shut down your system. Then press and hold the Touch ID or power button to launch Startup Security Utility. In Startup Security Utility, enable kernel extensions from the Security Policy button.


## Homebrew 

Install **Homebrew** so you can use `brew` to install Mac versions of Unix utilities.

	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	
		brew update

Add brew to profile

	echo 'eval $(/opt/homebrew/bin/brew shellenv)' >> /Users/younge/.zprofile
	eval $(/opt/homebrew/bin/brew shellenv)

Turn off analytics tracking 

	brew analytics off

Install specific Unix utilities & apps for Mac OS X:

	brew install curl
	brew upgrade curl
	brew install wget
	brew install xquartz
	brew install poppler 
	brew install antiword 
	brew install unrtf 
	brew install tesseract 
	brew install swig
	brew install qlmarkdown
	brew install mysql-connector-c
	brew install coreutils            # GNU version of UNIX tools start with g
	brew install graphviz             # Must install XCODE before this
	brew install ffmpeg
	brew install youtube-dl           # YouTube Downloader application

Keep `brew` (and apps installed by `brew`) up-to-date:

  `brew update && brew upgrade`  
  
Brew cask can have problems, so:

    brew update
    brew install cask
    brew reinstall cask
    
Occasionally run **brew doctor** to find and fix problems

	brew doctor


## First-Round apps   (these help to complete later steps)

  * Google Chrome  		 
  * 1Password      		 
  * Pathfinder     	
  * iTerm2  	 				    https://iterm2.com/
  * Cisco AnyConnect VPN	  	 connect to vpn.epfl.ch


## Configure ZSH  

Install Oh My Zsh   https://github.com/ohmyzsh/ohmyzsh

	sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

Install Autosuggestions

	git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

Add the plugin to the list of plugins for Oh My Zsh to load (inside ~/.zshrc)

	nano ~/.zshrc
	
	plugins=(git zsh-autosuggestions)

	... Start a new terminal session.

Install zsh-syntax-highlighting using Oh-my-zsh

	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

	nano ~/.zshrc

	plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

	... Start a new terminal session.

Install Powerlevel10k:

	git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
	
Then edit your ~/.zshrc and set ZSH_THEME="powerlevel10k/powerlevel10k"

	nano ~/.zshrc
	
	ZSH_THEME="powerlevel10k/powerlevel10k"

Once you do so, when you start a new terminal session, the Powerlevel10 configure wizard will be launched to set your prompt and config.

If you install Oh-my-zsh later, you may drop sections from the `.zshrc` file
(for eaxmple, the `>>> conda initialize >>>` block within the resource file)
Look for `.zshrc.pre-oh-my-zsh` and add sections back into the `.zshrc` file


You can reconfigure the `powerlevel10k` setup by re-executing the setup script:  

    p10k configure
    

## Install Anaconda Python

Install 64-bit Python 3.x Anaconda from:

	https://www.continuum.io/downloads

Check paths in .zshrc and ensure that Anaconda code is there.

    
## Install PyCharm   

Download the Apple Silicon M1 version of the DMG installer.
Install PyCharm before running pip install requirements.


## Install PIP packages from PyPi.org

Install Anaconda and PyCharm first.

TRhen upgrade to the latest version of pip

	pip install --upgrade pip 

Then review the REQUIREMENTS.txt to see which packages you want to unstall in the base environment.

	more REQUIREMENTS.txt

To install everything in the REQUIREMENTS.txt file, run:

	pip install --upgrade REQUIREMENTS.txt

To generate your own pip & PyPI distributions, install PyPA’s `build` utility:

	pip install --upgrade build

To upload packages directly to PyPI.org, install the `twine` utility:

	pip install --user --upgrade twine


## Install Google Cloud SDK

See instructions:  https://cloud.google.com/sdk/


Download it:  

    https://cloud.google.com/sdk/docs/quickstart 


Unzip the downloaded file (something like the following) 

    google-cloud-sdk-328.0.0-darwin-x86_64.tar.gz
    
    
Move to user home directory - so it then be at:  

    ~/google-cloud-sdk/


Install it:

    cd ~/google-cloud-sdk/
    bash install.sh
    
    restart terminal (zsh) so Command Line Tools are now on path
    
    
Initialize it:

    gcloud init
    
    that will ask you to login and then set defaults, such as:
    
			Your current project has been set to: [epfl-cdm-tis].
	
			Your project default Compute Engine zone has been set to [europe-west1-d].
			You can change it by running [gcloud config set compute/zone NAME].
			
			Your project default Compute Engine region has been set to [europe-west1].
			You can change it by running [gcloud config set compute/region NAME].
	    
	    
Authorize (not sure if this is really needed as init may do it .... but can't hurt)

    gcloud auth login
    
    gcloud beta auth login
    
    gcloud beta auth application-default login
    
    gcloud auth login  # May need to do this again at the end to make sure it goes back to basic auth ???)
    
    
Install optional components:
    
    gcloud components list
    
    gcloud components install datalab
    gcloud components install cloud-datastore-emulator
    gcloud components install docker-credential-gcr
    gcloud components install beta
    gcloud components install app-engine-python
    gcloud components install app-engine-python-extras
    gcloud components install kubectl
    gcloud components install pkg

    
Occasionally update Google cloud by running:  

    gcloud components update


## Install Google Cloud Client

  https://github.com/GoogleCloudPlatform/google-cloud-python

    pip install --upgrade google-cloud
    pip install --upgrade google-cloud-storage
    pip install --upgrade google-cloud-datastore
    pip install --upgrade google-cloud-logging
    pip install --upgrade google-auth-oauthlib
    

## Install Google API Client Libraries

  https://developers.google.com/api-client-library/

The Google APIs Python Client is a client library for using the broad set of Google APIs. google-cloud is built specifically for the Google Cloud Platform and is the recommended way to integrate Google Cloud APIs into your Python applications. If your application requires both Google Cloud Platform and other Google APIs, the 2 libraries may be used by your application.

    pip install --upgrade google-api-python-client
    pip install --upgrade GoogleAppEngineCloudStorageClient
     
	
## Configure Mac OS X


#### Re-install XCode Command Line Tools:

Even if you did this earlier (at the start), you might need to do it again (or perhaps re-accept licensing agreement). It is most reliable to just do it again, run it again, accept it again.

    xcode-select --install


#### Add aliases to `bash`

Add alias for `ll` 

	echo "alias ll='ls -ClGaf'" >> ~/.bash_profile
	

#### Turn off spelling, caps and double-spacing  

By default, Mac will replace two quickly typed spaces with a period. Turn that off! 

  1. Go to the  Apple menu and choose ‘System Preferences’
  2. Select the “Keyboard” preference pane and then choose the “Text” tab
  3. Find the setting for “Correct Spelling automatically” and set the check box to OFF
  4. Find the setting for “Capitalize words automatically” and set the check box to OFF
  5. Find the setting for “Add period with double space” and set the check box to OFF
  6. Remove the omw shortcut to "On My Way"


#### Install quicklook for Markdown

Brew's version of quick look for markdown (qlmarkdown) can have problems, so:

    brew install qlmarkdown
    
or  

    brew reinstall qlmarkdown
    
reset the qlmanager
    
    qlmanage -r
    
QuickLook doesn't allow selecting text by default. If you want to select the text in the markdown preview, you will need to enable text selection in QuickLook by running the following command in Terminal:

    defaults write com.apple.finder QLEnableTextSelection -bool TRUE; killall Finder


#### Configure SSH for GitHub

It is safer and faster to use Two-Factor Authentication with GitHub. The following instructions help you to generate an SSH Key, install it in your Apple Keychain, and then link it to GitHub.

**Generate a new SSH key**

	ssh-keygen -t ed25519 -C "<<YOUREMAIL>>"
	
This creates a new ssh key, using the provided email as a label.  

	> Generating public/private ed25519 key pair.
	
When you're prompted to "Enter a file in which to save the key," press Enter. This accepts the default file location.

	> Enter a file in which to save the key (/Users/you/.ssh/id_ed25519): [Press enter]
	
At the prompt, type a secure passphrase. For more information, see "Working with SSH key passphrases".

	> Enter passphrase (empty for no passphrase): [Type a passphrase]
	> Enter same passphrase again: [Type passphrase again]


**Add SSH Key to Apple's ssh-agent**

Use the default macOS ssh-add command, and not an application installed by macports, homebrew, or some other external source.

Start the ssh-agent in the background.

	eval "$(ssh-agent -s)"
	> Agent pid 5133

If you're using macOS Sierra 10.12.2 or later, you will need to modify your ~/.ssh/config file to automatically load keys into the ssh-agent and store passphrases in your keychain.

First, check to see if your ~/.ssh/config file exists in the default location.

	open ~/.ssh/config
	> The file /Users/you/.ssh/config does not exist.
	
If the file doesn't exist, create the file.

	touch ~/.ssh/config
	
Open your ~/.ssh/config file, then modify the file to contain the following lines. If your SSH key file has a different name or path than the example code, modify the filename or path to match your current setup.

	Host *
	  AddKeysToAgent yes
	  UseKeychain yes
	  IdentityFile ~/.ssh/id_ed25519
  
  Note: If you chose not to add a passphrase to your key, you should omit the UseKeychain line.

Add your SSH private key to the ssh-agent and store your passphrase in the keychain. If you created your key with a different name, or if you are adding an existing key that has a different name, replace id_ed25519 in the command with the name of your private key file.

	ssh-add -K ~/.ssh/id_ed25519

**Add SSH key to GitHub account**

Copy the SSH public key to your clipboard.

If your SSH public key file has a different name than the example code, modify the filename to match your current setup. When copying your key, don't add any newlines or whitespace.

	pbcopy < ~/.ssh/id_ed25519.pub

In the upper-right corner of a GitHub webpage, click your profile photo, then click Settings, then "SSH and GPG Keys", then "New Key". Enter a title for the key (such as the name of the computer it is on) and then paste in the SSH keytext from the clipboard. Save. Confirm add. You are done.


#### Configure other `git` settings

    git config --global core.editor "nano"  
    git config --global core.autocrlf input  
    



#### Install the `youtube-dl` utility

youtube-dl is critical for easy access to content on YouTube. Homebrew shold be able to install the "YouTube Downloader" app from brew:

	brew install youtube-dl

But you can also install the app directly from it's repository (in case GitHub drops it again). 

	sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
	sudo chmod a+rx /usr/local/bin/youtube-dl

Execute this for the `youtube-dl` help file.

	youtube-dl -h


## Install Developer Fonts

Run __Font Book__ to import fonts (Font Book | File | Add Fonts...). Or simply download ttf files and double click them (that will open a font installer).

  - Download & install CMU Latex fonts: 

    lm2.004otf.zip  
    cm-unicode-0.6.3a.zip
    
  - Download CMU TTF fonts

    https://www.fontsquirrel.com/fonts/computer-modern

  - Download & install Google Fonts

    https://github.com/google/fonts/archive/master.zip

  - Download & install Meslo Nerd fonts (see https://github.com/romkatv/powerlevel10k#meslo-nerd-font-patched-for-powerlevel10k)
	
    MesloLGS NF Regular.ttf  
	   https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
	
    MesloLGS NF Bold.ttf  
      https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
	
    MesloLGS NF Italic.ttf  
      https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
	
    MesloLGS NF Bold Italic.ttf  
      https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf


## MS Office

If your institution uses a Microsoft Volume License to deploy Microsoft Office 2019 for Mac:

  1. Download and install the Microsoft Office 2019 for Mac installation package from:

     https://go.microsoft.com/fwlink/?linkid=525133

  2. Copy locally and run the `Microsoft_Office_2019_VL_Serializer.pkg` package that you will find here:

     smb://olympe.intranet.epfl.ch/mac/cd0F/2019/MultiLanguage/SERIALIZER-10.2018/Microsoft_Office_2019_VL_Serializer.pkg

  Deployment tips:

    a. The VL Serializer must be installed on each Mac that you want to set up with a Volume License
    
    b. If desired, the VL Serializer can be installed prior to downloading and installing the Office 2019 applications
    
    c. All packages are compatible with MDM management servers such as Intune, Jamf Pro and FileWave
    
    d. If you wish to deploy individual Office 2019 apps rather than the suite, use the following download links:
	  	
	  	- Word 2019 for Mac - https://go.microsoft.com/fwlink/?linkid=525134
	  	- Excel 2019 for Mac - https://go.microsoft.com/fwlink/?linkid=525135
	  	- PowerPoint 2019 for Mac - https://go.microsoft.com/fwlink/?linkid=525136
	  	- Outlook 2019 for Mac - https://go.microsoft.com/fwlink/?linkid=525137

    For more information and updates, see the article at https://go.microsoft.com/fwlink/?linkid=2005887


## Adobe Creative Suite CC


  If your institution provides an Enterprise License to Adobe Creative Suite CC, you 
  
  First, make sure you setup an "Adobe Personal ID" to identify yourself personally - you need it later.

  Go to the Adobe website: https://accounts.adobe.com

    For my University, we go to the Adobe sign in page, and on the first line type "epfl.ch" and hit ENTER
    That will then automatically redirect you to an authentication server. But your institution
    might follow a different authentication process ...
 
  Once you have logged in, you will be taken to your personal Adobe CC Cloud page.
  
  In the "Adobe for Enterprise" area: Click "View plan details." Click on “Download” button. Finally, click on the "Download" button for the app.  
  Then follow the instructions displayed. It may take a long time to download everything.
  
  In addition to the Adobe CC applications you install, the installation process will also install the "Adobe Creative Cloud" application which will always run in the background. It manages your credentials with Adobe's servers. However, you may need to pass through your isntitutions authentication server (for ours, we always enter "epfl.ch" on the first line of the Adobe login dialog).


## Install Native Mac Applications  
	
	1Password
	Android File Transfer
	Audacity
	BBEdit
	Docker                            https://www.docker.com/products/docker-desktop
	Express VPN 
	Falcon                            https://plot.ly/free-sql-client-download/
	Firefox
	GitHub Desktop                    http://mac.github.com
	Google Chrome
	Google Backup and Synch
	Google Drive for Desktop
	iTerm2
	Keynote
	Logitech Options
	Logitech Presentation
	MacDown
	Mendeley                          https://www.mendeley.com/
	Path Finder
	PyCharm
	R 
	RStudio
	ScanSnap Home (Fujitsu iX1500)    https://scansnap.fujitsu.com/global/dl/mac-1100-ix1500.html
	ScanSnap ABBYY FineReader  
	Signal
	Skype
	Skype Meeting App
	Spotify
	Stata
	MacTeX                            http://www.tug.org/mactex/
	TOR Browser
	Zoom                              https://www.zoom.us 


## Install UNIX Applications (including apps in Docker containers)

	
- Gunicorn   

	pip install gunicorn)


- `consolemd`  (a utility to display markdown files in a console)	
	pip install consolemd
	


	
## Periodic Maintenance & Fixes

#### Update core components

    xcode-select --install
    brew update
    brew upgrade
    brew reinstall cask
    brew doctor
    brew analytics off
    pip install --upgrade pip
    gcloud components update
    
    
#### Update `zsh` configuration:  

    p10k configure    
    
    
## Bug-Fixs

#### SSL 

If the `libssh` system breaks then you may get some SSL errors when using `curl`. If that happens, use conda to install libssh2 to fix:

	conda install libssh2 
	HOMEBREW_CURLRC=1 brew reinstall openssl curl
	
If the above does not fix everything, then return to Anaconda and reinstall

