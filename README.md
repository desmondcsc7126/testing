#!/bin/bash
sudo yum update -y
sudo yum install git -y
git clone https://github.com/desmondcsc7126/testing.git
cd testing
sudo pip3 install flask
sudo pip3 install pymysql
sudo pip3 install boto3
sudo python3 application.py
