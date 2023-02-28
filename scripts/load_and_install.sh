#!/bin/bash

# Loads and installs all the required packages needed for python 3.10
pip3.10 freeze > ../requirements.txt && echo "Successfully loaded python libraries" || echo "Failed to load required python libraries"
pip3.10 install -r ../requirements.txt && echo "Successfully installed python libraries" || echo "Failed to install required python libraries"