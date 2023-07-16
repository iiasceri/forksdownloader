#!/bin/bash
pip install requests
python downloadforks.py -owner $1 -repo $2
