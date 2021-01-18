#!/bin/sh
sudo apt-get update --assume-yes
sudo apt-get upgrade --assume-yes
sudo apt-get install --assume-yes python
sudo apt-get install --assume-yes python3-pip
sudo apt-get install --assume-yes git
sudo python3.8 -m pip install pipenv
cd $HOME
mkdir -p $HOME/Programs
cd $HOME/Programs
git clone https://github.com/GabrielSCabrera/MasterThesis.git
cd $HOME/Programs/MasterThesis
make install
