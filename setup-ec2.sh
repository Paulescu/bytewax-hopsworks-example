# remove this package to avoid the following error:
#   pip cannot uninstall : "It is a distutils installed project"
apt autoremove -y python3-pyasn1-modules/focal
apt autoremove -y python3-pexpect/focal
apt autoremove -y python3-entrypoints/focal

# set third-party API keys to connect to Feature Store
export HOPSWORKS_PROJECT_NAME=???
export HOPSWORKS_API_KEY=???

# # add src library to PYTHONPATH, so we can write absolute imports
# # like "from src.config import FEATURE_GROUP_METADATA"
# export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/bytewax"
# export PYTHONPATH="${PYTHONPATH}:/home/ubuntu/bytewax/src"