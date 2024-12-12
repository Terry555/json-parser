#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Installing Python..."
    # For Ubuntu/Debian systems, install python3 and pip
    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    # For Red Hat/CentOS systems, install python3 and pip
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y python3 python3-pip
    else
        echo "Unsupported system for automatic Python installation. Please install Python manually."
        exit 1
    fi
else
    echo "Python is already installed."
fi

# Check if pip is installed
if ! command -v pip3 &>/dev/null; then
    echo "pip is not installed. Installing pip..."
    sudo apt install -y python3-pip
fi

# Ensure the program's requirements are installed (if any)
# If you have any Python dependencies, this is where you'd list them
# Example: If you have a `requirements.txt`, you can install dependencies like so:
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
fi

# Check if the user provided a .json file as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <json-file>"
    exit 1
fi

# Ensure the provided .json file exists
if [ ! -f "$1" ]; then
    echo "File '$1' not found!"
    exit 1
fi

# Run your program (assuming it's located in the same directory)
echo "Running the JSON parser on '$1'..."
python3 semantic_analyzer.py "$1"