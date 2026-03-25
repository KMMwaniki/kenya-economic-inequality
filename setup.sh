#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install packages one by one
pip install numpy
pip install pandas
pip install plotly
pip install streamlit

# Create database
python run_database.py

echo "Build completed!"