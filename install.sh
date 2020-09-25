#!/bin/sh
sudo apt-get update --assume-yes
sudo apt-get upgrade --assume-yes
sudo apt-get install --assume-yes python
sudo apt-get install --assume-yes python3-pip
sudo apt-get install --assume-yes git
sudo apt-get install --assume-yes pipenv
mkdir ~/Programs
cd ~/Programs
git pull https://github.com/GabrielSCabrera/MasterThesis/
cd ~/Programs/MasterThesis
make install
