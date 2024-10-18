#!/bin/bash

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "Python is already installed."
else
    echo "Python is not installed. Installing Python..."

    # Update package lists
    sudo apt update

    # Install Python (This works for Debian-based systems; adjust as necessary)
    sudo apt install -y python3 python3-pip

    # Verify installation
    if command -v python3 &>/dev/null; then
        echo "Python installation completed successfully."
    else
        echo "Python installation failed. Please install it manually."
        exit 1
    fi
fi

# Run Docker `my-parser-app`
docker run --rm -v "$(pwd):/app" my-parser-app python3 /app/lexical_analyzer.py

# Run the lexical_analyzer.py script using Docker with the JSON test files as arguments
echo "Running lexical_analyzer.py with test files..."

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "lexical_analyzer.py executed successfully."
else
    echo "An error occurred while executing lexical_analyzer.py."
    exit 1
fi
