#!/bin/sh

sudo apt-get update
sudo apt-get install -y puredata pisound-ctl amidiauto pisound-ctl-scripts-puredata python3-pip python3-setuptools
sudo pip3 install python-osc Adafruit-Blinka pygame pillow adafruit-circuitpython-ssd1306

echo "Done! Thank you!"
