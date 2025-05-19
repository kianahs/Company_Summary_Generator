#!/bin/bash

VENV_NAME="venv"
CONFIG_FILE="config.json"


echo "Creating virtual environment..."
python -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"


echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt


echo "Running main.py with config..."
python main.py --config "$CONFIG_FILE"
