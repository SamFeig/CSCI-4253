# Update the package list and install SDK
sudo apt-get update
sudo apt-get install -y python3 python3-pip git google-cloud-sdk
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

sudo -i #needed for permision issues
mkdir -p /srv
cd /srv
#get files from metadata
curl http://metadata/computeMetadata/v1/instance/attributes/startup-script-remote -H "Metadata-Flavor: Google" > startup_script_remote.sh
curl http://metadata/computeMetadata/v1/instance/attributes/service-credentials -H "Metadata-Flavor: Google" > service-credentials.json
curl http://metadata/computeMetadata/v1/instance/attributes/part3 -H "Metadata-Flavor: Google" > part3.py

#launch second vm
python3 ./part3.py csci-4253 csci5253bucket