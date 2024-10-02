# Python Camera Script

## Description
This project provides a Python script for capturing and analyzing images using a camera. It leverages various libraries to facilitate image processing and data analysis.

## Requirements
- Python 3.x
- Virtual environment tools (included in Python)
- Necessary libraries listed in `requirements.txt`

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/CodeBluDev/Pyton-Camara-Script
    cd Pyton-Camara-Script
    ```

2. **Install Python and Git**:
    ### For Windows Users:
    1. **Install Chocolatey** (if not installed):
        Open PowerShell as Administrator and run:
        ```powershell
        Set-ExecutionPolicy Bypass -Scope Process -Force; `
        [System.Net.ServicePointManager]::SecurityProtocol = `
        [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        ```

    2. **Install Python**:
        ```powershell
        choco install python
        ```

    3. **Install Git**:
        ```powershell
        choco install git
        ```

    4. **Verify Installations**:
        ```bash
        python --version
        git --version
        ```

    ### For macOS Users:
    1. **Install Homebrew** (if not installed):
        Open Terminal and run:
        ```bash
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```

    2. **Install Python and Git**:
        ```bash
        brew install python git
        ```

    3. **Verify Installations**:
        ```bash
        python3 --version
        git --version
        ```

3. **Run the Setup Script**: This script will create a virtual environment and install the necessary dependencies.
    ```bash
    ./setup.sh
    ```

4. **Activate the Virtual Environment**: If the virtual environment isn't activated automatically, activate it with:
    ```bash
    source venv/bin/activate
    ```

5. **Check Installed Packages**: Verify that the required packages are installed by running:
    ```bash
    pip list
    ```

## Usage
To run the camera capture and analysis script, execute the following command while the virtual environment is activated:
```bash
python capture_and_analyze.py
