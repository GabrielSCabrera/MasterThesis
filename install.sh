#!/bin/sh
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python -y
sudo apt-get install python3-pip -y
sudo apt-get install git -y
sudo apt-get install pipenv -y
mkdir ~/Programs
cd ~/Programs
git pull https://github.com/GabrielSCabrera/MasterThesis/
cd ~/Programs/MasterThesis
make install
