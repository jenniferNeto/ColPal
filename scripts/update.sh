#!/bin/bash

# Update requirements with newly installed packages
pip3.10 freeze > ../requirements.txt && echo "Successfully updated python libraries" || echo "Failed to update python libraries"
