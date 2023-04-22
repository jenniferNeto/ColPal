#!/bin/bash

# Install the required packages
pip3.10 install -r ../backend/requirements.txt && echo "Successfully installed python libraries" || echo "Failed to install required python libraries"