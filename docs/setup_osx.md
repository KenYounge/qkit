
# Help file to setup a new Mac OSX M1 Computer  

The following document sets forth a bare-metal process for completely installing a new Mac OSX Big Sur 11.2.3 M1 computer to return to operation as quickly as possible.



<br>

--------------------------------------------------------------------------------------------------------------------
## OS X


### Xcode

##### Install Xcode from the Apple store

Do this first, before anything else! Other dev apps require Xcode to be installed first.

Be sure to run Xcode at least one time and accept license agreement. If you do not, then it will hang when other apps try to call XCODE and it waits for license to validate!

From time to time, upgrade to the latest version of XCODE. But then be sure to run Xcode again and accept the license again, or programs may hang while waiting for the XCODE license to validate.

##### Install Xcode command-line tools

    xcode-select --install

The above step is required on MacOS to set up local development utilities, including "many commonly used tools, utilities, and compilers, including make, GCC, clang, perl, svn, git, size, strip, strings, libtool, cpp, what, and many other useful commands that are usually found in default Linux installations,"

If the above command line instructions fails, then you can also directly sign into Apple Developer and download the tools installation DMG from:

    https://developer.apple.com/download/more/


### Rosetta 2

Mac uses "Rosetta 2" to translate legacy code for Intel CPUs over to M1 (or "Apple Silicon"). When you install Xcode, and then run Xcode, it should automatically prompt you to install Rosetta. But if it does not, then you can do it directly by running this:

    softwareupdate --install-rosetta


### System Extensions

If you use Google Drive for Desktop (or other kernel extensions) then (as of Big Sur) you need to enable "OSX System Extensions." To do that, shut down your system. Then press and hold the Touch ID or power button to launch Startup Security Utility. In Startup Security Utility, enable kernel extensions from the Security Policy button.


### Key Apps

We need to install these early in the process to help with other steps.

  * Google Chrome  		 
  * 1Password      		 
  * Pathfinder     	
  * iTerm2  	 				    https://iterm2.com/
  * Cisco AnyConnect VPN	  	 connect to vpn.epfl.ch

### Start a `~/scratch/` directory

We can use this to stage temporary git repos and other installs

    mkdir ~/scratch



<br>

--------------------------------------------------------------------------------------------------------------------
## Homebrew


Install **Homebrew** to use `brew` to install software

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
		brew update
	  echo 'eval $(/opt/homebrew/bin/brew shellenv)' >> /Users/younge/.zprofile
	  eval $(/opt/homebrew/bin/brew shellenv)
	  brew analytics off  # Turn off analytics tracking

Install Unix utilities for OS X:

	brew install curl
	brew upgrade curl
	brew install wget
	brew install xquartz
	brew install poppler
	brew install unrtf
	brew install swig
	brew install mysql-connector-c
	brew install coreutils            # GNU version of UNIX tools start with g
	brew install graphviz             # Must install XCODE before this
	brew install ffmpeg
	brew install tesseract            # OCR engine
	brew install youtube-dl           # Youtube downloader utility

Keep `brew` and `cask` up-to-date

	brew update
	brew upgrade
	brew install cask
	brew reinstall cask
	brew doctor                       # run `doctor` to find and fix problems




<br>

--------------------------------------------------------------------------------------------------------------------
## ZSH  

Install Oh My Zsh   https://github.com/ohmyzsh/ohmyzsh

    sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

    # Add plugin to `.zshrc` and restart terminal

    nano ~/.zshrc
    plugins=(git zsh-autosuggestions)

Install zsh-syntax-highlighting

    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

    # Add plugin to `.zshrc` and restart terminal

    nano ~/.zshrc
    plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

nstall Powerlevel10k:

	git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k

    # Add ZSH_THEME to `.zshrc` and restart terminal

    nano ~/.zshrc
    ZSH_THEME="powerlevel10k/powerlevel10k"

When you restart terminal it will take you through the Powerlevel10 config.
Reconfigure `powerlevel10k` by running:  

    p10k configure

If you install Oh-my-zsh later, you may drop sections from the `.zshrc` file
(for eaxmple, the `>>> conda initialize >>>` block within the resource file)
Look for `.zshrc.pre-oh-my-zsh` and add sections back into the `.zshrc` file




<br>

--------------------------------------------------------------------------------------------------------------------
##  Python


### Anaconda

Install 64-bit Anaconda Python 3.x

	https://www.continuum.io/downloads

Check path variables in `.zshrc` to make sure Anaconda is on paths.


### PyCharm   

Download the Apple Silicon M1 version of the DMG installer.
Install PyCharm before running pip install requirements.


### Jupyter Lab

Install jupyter lab

    pip install jupyterlab

Install stand-alone app helper

    git clone https://github.com/telamonian/jupyter-app.git
    cd jupyter-app
    ./install

Set Python3 for the jupyter/ipython kernel

    python3 -m pip install ipykernel  # install the python kernel (ipykernel) globally
    python3 -m ipykernel install      # install python kernel into nteract's available kernel list


#### PIP

Upgrade to the latest version of pip

    pip install --upgrade pip

Review REQUIREMENTS.txt and select packages for the base environment

    more REQUIREMENTS.txt

To install everything in the REQUIREMENTS.txt, run:

    pip install --upgrade REQUIREMENTS.txt

To generate your own pip & PyPI distributions, install PyPA’s `build` utility:

    pip install --upgrade build

To upload packages directly to PyPI.org, install the `twine` utility:

    pip install --user --upgrade twine




<br>

--------------------------------------------------------------------------------------------------------------------
## GitHub


### SSH Credentials for GitHub

It is safer and faster to use Two-Factor Authentication with GitHub.
Generate an SSH Key, install it in the Apple Keychain, link it to GitHub.

#### Generate an SSH key

The following command will create a new ssh key, using provided email as a label.  

    ssh-keygen -t ed25519 -C "<<YOUREMAIL>>"

When prompted to "Enter a file in which to save the key," press Enter.
This accepts the default file location.
At prompt, type a passphrase.  

#### Add SSH Key to Apple's ssh-agent

Use the default macOS ssh-add command, and **not** an application installed by
`macports`, `homebrew`, or some other external source.

Start the ssh-agent in the background.  

    eval "$(ssh-agent -s)"
    > Agent pid 5133

If you're using macOS Sierra 10.12.2 or later, you will need to modify your
`~/.ssh/config` file to automatically load keys into the ssh-agent and store
your passphrases in your keychain.

First, check to see if your ~/.ssh/config file exists in the default location.

    open ~/.ssh/config  
	  > The file /Users/you/.ssh/config does not exist.

If the file doesn't exist, create the file.

    touch ~/.ssh/config

Open your ~/.ssh/config file, then modify the file to contain the following lines. If your SSH key file has a different name or path than the example code, modify the filename or path to match your current setup.
Note: If you chose not to add a passphrase to your key, you should omit the UseKeychain line.

    Host *
      AddKeysToAgent yes
      UseKeychain yes
      IdentityFile ~/.ssh/id_ed25519

Add your SSH private key to the ssh-agent and store your passphrase in the keychain. If you created your key with a different name, or if you are adding an existing key that has a different name, replace id_ed25519 in the command with the name of your private key file.

    ssh-add -K ~/.ssh/id_ed25519

#### Add SSH key to GitHub account

Copy the SSH public key to your clipboard.

If your SSH public key file has a different name than the example code,
modify the filename to match your current setup. When copying your key,
don't add any newlines or whitespace.

    pbcopy < ~/.ssh/id_ed25519.pub

In the upper-right corner of a GitHub webpage, click your profile photo,
then click Settings, then "SSH and GPG Keys", then "New Key".
Enter a title for the key (such as the name of the computer it is on) and
then paste in the SSH keytext from the clipboard. Save. Confirm add.

You are done setting up the SSH channel for github communications...

#### Using `https` with `github` under 2-Factor Authorization (2FA)

Even though you now have ssh enabled, you may still want to use `https` style
commands for push, pull, cloning, etc with `github`	- but if you have 2FA
enabled, you will have to use "Personal Tokens" from the commandline, instead
of your password. For instructions, see:

    https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

In upper-right corner of GitHub, click your profile photo.
Then click Settings.
In the left sidebar, click Developer settings.
In the left sidebar, click Personal access tokens.
Click Generate new token.
Generate new token button - and give your token a descriptive name.
Select the scopes, or permissions, you'd like to grant this token.
Click Generate token.
Copy the token to your clipboard. You cannot see the token after you navigate off the page.

To use token on the command line, enter it instead of your password:

    Username: your_username
    Password: your_token

Personal access tokens can only be used for HTTPS Git operations.
If your repository uses an SSH remote URL, you will need to switch the remote from SSH to HTTPS.

#### Other `git` settings

    git config --global core.editor "nano"  
    git config --global core.autocrlf input  




<br>

--------------------------------------------------------------------------------------------------------------------
## Google Cloud


#### Google Cloud SDK

Instructions:  

    https://cloud.google.com/sdk/
    https://cloud.google.com/sdk/docs/quickstart


Unzip the downloaded file (something like the following)

    google-cloud-sdk-328.0.0-darwin-x86_64.tar.gz

Move to user home directory - so it will be located at:  

    ~/google-cloud-sdk/

Install google cloud:

    cd ~/google-cloud-sdk/
    bash install.sh

Restart terminal so google command lLine tools are now on path

Initialize `gcloud`

    gcloud init
		gcloud config set compute/project epfl-cdm-tis
		gcloud config set compute/region europe-west1
		gcloud config set compute/zone europe-west1-d

Authorize `gcloud`  

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

#### Google Cloud Client

  https://github.com/GoogleCloudPlatform/google-cloud-python

    pip install --upgrade google-cloud
    pip install --upgrade google-cloud-storage
    pip install --upgrade google-cloud-datastore
    pip install --upgrade google-cloud-logging
    pip install --upgrade google-auth-oauthlib

#### Google API Client Libraries

    https://developers.google.com/api-client-library/

The Google APIs Python Client is a client library for using the broad set of Google APIs. google-cloud is built specifically for the Google Cloud Platform and is the recommended way to integrate Google Cloud APIs into your Python applications. If your application requires both Google Cloud Platform and other Google APIs, the 2 libraries may be used by your application.

    pip install --upgrade google-api-python-client
    pip install --upgrade GoogleAppEngineCloudStorageClient




<br>

--------------------------------------------------------------------------------------------------------------------
## Mac OSX Applications  


Members of the lab often use the following applications:

	1Password
	Android File Transfer
	Atom                              https://atom.io/
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

#### Scrivener

For technical books, use the Scrivener+MultiMarkDown workflow — see Chapter 22 of the Scrivener manual (Scrivener's own manual is created in Scrivener+MMD-->LaTeX).

Inline code and code blocks can be created with automatic syntax highlighting by providing the language name on compile. MultiMarkDown does the final conversion to Word or HTML, and because you compile to plain text, you can use `Pandoc` for more markup formatting (e.g. custom inline and block styles that you can use for INFO, WARNING boxes etc.). You can pass custom templates to `Pandoc` during compile, so you make a Word doc with the styling as you want, and when converting your Scrivener markdown file it applies the template and the Word document is fully styled (and `Pandoc` generates good semantic docx files (unlike Scrivener), figures, headings, captions, code blocks, block quotes etc all have attached style).

#### MS Office

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

#### Adobe Creative Suite CC


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




<br>

-------------------------------------------------------------------------------------------------------------------
## OS X Continued...


	#### Re-install XCode Command Line Tools

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

	#### Quicklook utilities

	Utilities for document conversions - especially `pandoc` to go markdown to pdf

	    brew install qlmarkdown                              # Quicklook for markdown
	    brew install quicklook-json                          # Quicklook for JSON
	    brew install qlvideo                                 # Quicklook for video
	    brew install antiword                                # Quicklook for Word docx
	    xattr -r ~/Library/QuickLook                         # remove quarantine block
	    xattr -d -r com.apple.quarantine ~/Library/QuickLook # remove quarantine block
	    qlmanage -r                                          # reset so utilities run

	QuickLook doesn't allow selecting text by default. If you want to select the text in the markdown preview, you will need to enable text selection in QuickLook by running the following command in Terminal:

	    defaults write com.apple.finder QLEnableTextSelection -bool TRUE; killall Finder

	#### `youtube-dl` utility

			youtube-dl is critical for easy access to content on YouTube.
			Homebrew should install it in the section above:

				brew install youtube-dl

			But if it gets pulled from homebrew, you can also install it from source:

				sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
				sudo chmod a+rx /usr/local/bin/youtube-dl
				youtube-dl -h                              # Execute to read the help file

	#### `pandoc` utility

	`pandoc` is a utility to convert docs between formats, especially markdown to pdf

	    brew install pandoc

	If `brew` fails, then use the MacOS installer from

	    https://pandoc.org/installing.html

	Install scripts to use `pandoc` from BBEdit

	    https://github.com/jrgcmu/BBpandoc

	Unzip and copy the folder to

	    ~/Library/Application Support/BBEdit/Scripts

	Copy pandoc-preview.sh to (create directory if it doesn't exist)

	    ~/Library/Application Support/BBEdit/Preview Filters

	Download `github` markdown css

	    https://gist.github.com/andyferra/2554919

	Copy `github` markdown css (or any other custom CSS files) to:

	    ~/Library/Application Support/BBEdit/Preview CSS

#### Fonts

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

Install Powerline fonts

    pip install powerline-status

    cd ~/scratch
    git clone https://github.com/powerline/fonts.git --depth=1
    cd fonts
    ./install.sh
    cd ..
    rm -rf fonts

Install Cascadia Code fonts
  
  https://github.com/microsoft/cascadia-code/blob/main/sources/vtt_data/CascadiaCode_VTT.ttf
  
  Double click the `CascadiaCode_VTT.ttf ` file - that will open the font installer



<br>

--------------------------------------------------------------------------------------------------------------------

## UNIX Apps & Docker


**Gunicorn** - a simple Python WSGI HTTP Server for UNIX in Docker

    pip install gunicorn


**consolemd** - a utility to display markdown files in a console

    pip install consolemd




<br>

--------------------------------------------------------------------------------------------------------------------

## Maintenance


#### Update core components

    xcode-select --install
    brew update
    brew upgrade
    brew reinstall cask
    brew doctor
    brew analytics off
    pip install --upgrade pip
    gcloud components update

#### Update `zsh`:  

    p10k configure    

#### SSL

If `libssh` breaks then you may get SSL errors when using `curl`.
If that happens, use `conda` to install `libssh2` to fix the problem:

    conda install libssh2
    HOMEBREW_CURLRC=1 brew reinstall openssl curl

If the above does not fix the problem -- reinstall Anaconda.
