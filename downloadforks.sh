#!/bin/bash
rm -rf all_merged_into_original
# Define the owner and repo variables
owner="JesusFreke"
repo="smalidea"
token="GITHUB_TOKEN"

# Activate the virtual environment
source venv/bin/activate

pip install -r requirements.txt
#python downloadforks.py -owner $owner -repo $repo -onlyactive -token $token
python downloadforks.py -owner $owner -repo $repo -token $token
python mergeforks.py $repo # pass the repo name as an argument