# Original start
# # chmod +x /MacroReplace/ReplaceMacro.sh
# # bash /MacroReplace/ReplaceMacro.sh '/app/files/config_auth.ini' 'files'
# python -c 'import nltk; nltk.download("all")'
# # python -c 'from Handler.Config import Config; Config.encrypt()'
# # python /app/App.py
# # python -m pytest
# cd ./src && python -c 'from Handler.Config import Config; Config.encrypt()'
# python App.py
# Original end
# New script start
# Check if Git is installed and install if not  
if ! command -v git &> /dev/null  
then  
    echo "Git could not be found. Attempting to install Git..."  
    apt-get update  
    apt-get install git -y  
else  
    echo "Git is already installed."  
fi  

# Check if cron is installed and install if not  
if ! command -v cron &> /dev/null  
then  
    echo "Cron could not be found. Attempting to install Cron..."  
    apt-get update
    apt-get install cron -y
else  
    echo "Cron is already installed."  
fi 

# Check if jq is installed and install if not  
if ! command -v jq &> /dev/null  
then  
    echo "jq could not be found. Attempting to install jq..."  
    apt-get update
    apt-get install jq -y
else  
    echo "jq is already installed."  
fi 

# Check if Git LFS is installed and install if not  
if ! command -v git-lfs &> /dev/null  
then  
    echo "Git LFS could not be found. Attempting to install Git LFS..."  
    # On some systems, you need to add a new package source for git-lfs  
    # Here's how you would do it on a Debian/Ubuntu system:  
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash  
    apt-get install git-lfs -y  
    # Initialize Git LFS  
    git lfs install  
else  
    echo "Git LFS is already installed."  
fi  

# AZcopy setup
if command -v azcopy >/dev/null 2>&1; 
then
    echo "azcopy is already installed."
else
    echo "azcopy is not installed."
    echo "Installing azcopy..."
    # Download azcopy
    wget https://aka.ms/downloadazcopy-v10-linux
    # Extract azcopy from the tarball
    tar -xvf downloadazcopy-v10-linux
    # Path service setup
    rm -f /usr/bin/azcopy
    cp ./azcopy_linux_amd64_*/azcopy /usr/bin
    chmod 755 /usr/bin/azcopy
    # Cleanup
    rm -f downloadazcopy-v10-linux
    rm -rf ./azcopy_linux_amd64_*/
    echo "azcopy has been installed successfully."
fi
echo "Setting environment variables for managed identity"
# export AZCOPY_AUTO_LOGIN_TYPE=MSI
# export AZCOPY_MSI_CLIENT_ID="57df4c19-99cd-4437-931a-bf20d8e5fb5f"
# export GOOGLE_APPLICATION_CREDENTIALS="/mnt/semanticstructured/gs_milvus_tls_keys/sa-cami-extracts-prod-access-key.json"

# Add the safe directory to the Git configuration  
echo "Configuring safe directory for Git"  
git config --global --add safe.directory /mnt/semanticstructured/File_movement/automation/OAAAKGGenAIFileShare  

echo "Current Working Directory: " $(pwd)
echo "Installing requirements.txt"
python -m pip install --upgrade pip && pip --no-cache-dir install -r ./requirements.txt && echo "Installed requirements.txt"
echo "Starting nltk download"
python -c 'import nltk; nltk.download("all")'
echo "Finished nltk download"
echo "Starting Spacy download en_core_web_sm"
# python -m spacy download en_core_web_sm
echo "Finished Spacy download en_core_web_sm"
echo "Current Working Directory: " $(pwd)
echo "Listing Files" && ls && echo "Listing ends"
echo "Listing files of directories" && ls */ && echo "Listing files of directories ends"
# echo "Installing requirements.txt"
# python -m pip install --upgrade pip && pip --no-cache-dir install -r ./requirements.txt && echo "Installed requirements.txt"
# echo "Starting nltk download"
# python -c 'import nltk; nltk.download("all")'
# echo "Finished nltk download"
echo "Checking before encrypting"
cd ./src && echo "Current Working Directory before checking: " $(pwd) && python -c 'from Handler.Config import Config; Config.check_encrypt()'
echo "Checking after encrypting"
cd .. && echo "Current Working Directory after changing to root directory: " $(pwd)
echo "Starting Encryption"
# [ -f temp.txt ] && echo "file exists" || { echo "File does not exist"; > temp.txt; cd ./src; echo "Echo cmd before. Current Working Directory: " $(pwd); python -c 'from Config import Config; Config.encrypt()' && echo "Encryption is Completed"; } && echo "Check complete"
cd ./src && echo "Echo cmd before. Current Working Directory: " $(pwd)
# python -c 'from Config import Config; Config.check_config()' && echo "Config check completed"
FILEPATH="../files/.key.key"
new_variable=$(head -1 "../files/config_auth.ini")
echo "step2";
if [[ "$new_variable" == *"azure"* ]] && [ -f "$FILEPATH" ]; then echo "step5"; rm -f "$FILEPATH"; fi;
python -c 'from Handler.Config import Config; Config.encrypt()' && echo "Encryption is Completed"
# python -c 'from Encryption import Encryption; Encryption.check_encryption()' && echo "Encryption check completed"
echo "All checks complete"
echo "Current Working Directory: " $(pwd)
# echo "Starting nltk download"
# python -c 'import nltk; nltk.download("all")'
# echo "Finished nltk download"
echo "Current Working Directory before Compiling: " $(pwd)
echo "Compiling .py files"
cd .. && echo "Current Working Directory after changing to root directory: " $(pwd)
python compile_files.py && echo "Finished Compiling .py files"
echo "Current Working Directory: " $(pwd)

# Add a new cron job to schedule trigger
service cron restart
crontab -l | { cat; echo "30 7 * * 4 /home/site/wwwroot/files/schedule.sh  > /var/log/cron.log 2>&1"; } | crontab -
crontab -l | { cat; echo "0 7 * * 4 >/mnt/semanticstructured/final_metrics.json  > /var/log/cron.log 2>&1"; } | crontab -

# ODBC dependency installation
curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
apt-get update

# .pyc deploy
cd ./src && echo "Current Working Directory after changing to src: " $(pwd)
# ## Installing azcopy
# echo "Copying the installation file from fileshare"
# cp /mnt/semanticstructured/azcopy_install/azcopy_v10.tar.gz .
# tar -xvf azcopy_v10.tar.gz
# rm -f /usr/bin/azcopy
# cp ./azcopy_linux_amd64_*/azcopy /usr/bin/
# chmod 755 /usr/bin/azcopy
# echo "Installation of azcopy completed Completed"


echo "Starting the Flask app from App.pyc"
python3 App.pyc && echo "Current Working Directory: " $(pwd)
echo "Finished the Flask app from App.pyc"

# New script end