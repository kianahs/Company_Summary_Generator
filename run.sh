#!/bin/bash

REPO_URL="https://github.com/kianahs/Company_Summary_Generator.git"
PROJECT_DIR="CompanySummaryGenerator"
VENV_NAME="venv"
CONFIG_FILE="config.json"


echo "Cloning repository..."
git clone "$REPO_URL" "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit 1


echo "Creating virtual environment..."
python -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"


echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt


echo "Running main.py with config..."
python main.py --config "$CONFIG_FILE"
