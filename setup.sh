#!/bin/bash
# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Reminder to activate the environment manually
echo "To activate the virtual environment, run 'source venv/bin/activate' if it isn't already activated."
