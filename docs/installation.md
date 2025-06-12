Installation Guide
System Requirements
Supported Operating Systems

Windows 10/11
macOS 10.14+
Linux (Ubuntu 18.04+, CentOS 7+, etc.)

Python Requirements

Python 3.8 or higher
pip package manager

Account Requirements

Active easytoyou.eu account with valid subscription

Installation Methods
Method 1: Standard Installation (Recommended)
bash# Clone the repository
git clone https://github.com/rbwtech/easy-to-you-automation.git
cd easy-to-you-automation

# Install dependencies

pip install -r requirements.txt
Method 2: Virtual Environment (Best Practice)
bash# Clone repository
git clone https://github.com/rbwtech/easy-to-you-automation.git
cd easy-to-you-automation

# Create virtual environment

python -m venv venv

# Activate virtual environment

# Windows:

venv\Scripts\activate

# macOS/Linux:

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt
Method 3: Development Installation
bash# Clone repository
git clone https://github.com/rbwtech/easy-to-you-automation.git
cd easy-to-you-automation

# Create virtual environment

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install development dependencies

pip install -r requirements-dev.txt

# Install in editable mode

pip install -e .
Verification
Test Installation
bash# Test v2 (recommended)
python scripts/main.py --help

# Test v1 (legacy)

python scripts/easy4us.py --help

# Test package import

python -c "from easytoyou import IonicubeDecoder; print('✅ Installation successful!')"
Test Basic Functionality
bash# Run a quick test (replace with your credentials)
python scripts/main.py -u USERNAME -p PASSWORD -s ./test_directory -v

Troubleshooting
Common Issues
Python Version Issues
bash# Check Python version
python --version

# Use specific Python version if needed

python3.8 -m pip install -r requirements.txt
Permission Errors (Linux/macOS)
bash# Use --user flag
pip install --user -r requirements.txt

# Or use sudo (not recommended)

sudo pip install -r requirements.txt
Windows PATH Issues
bash# Add Python to PATH or use full path
C:\Python38\python.exe -m pip install -r requirements.txt
SSL Certificate Errors
bash# Upgrade certificates
pip install --upgrade certifi

# Or use trusted hosts

pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
Next Steps

Read the Usage Guide for detailed usage instructions
Check Troubleshooting for common issues
Review API Documentation for advanced usage
