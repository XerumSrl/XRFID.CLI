# 🚀 Installation Guide

Complete installation instructions for Zebra RFID CLI on all supported platforms.

## System Requirements

- **Python 3.9 or higher** (check with `python --version`)
- **Git** for cloning the repository
- **Network access** to your Zebra RFID reader
- **Supported Readers**: Zebra FX9600, FXR90, ATR7000

## Platform-Specific Installation

### Windows (PowerShell)

#### Prerequisites
```powershell
# Check Python version (must be 3.9+)
python --version

# Check if Git is installed
git --version

# If Git is not installed, download from: https://git-scm.com/download/win
```

#### Installation Steps
```powershell
# 1. Clone the repository
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Verify installation
python xrcli_entrypoint.py --help
```

#### Automated Setup Script (Windows)
Create a file called `setup.ps1`:

```powershell
#!/usr/bin/env pwsh
# XRFID CLI Setup Script for Windows
# Usage: .\setup.ps1

Write-Host "🏷️ Zebra RFID CLI Setup" -ForegroundColor Cyan
Write-Host "Developed by Xerum Srl" -ForegroundColor Green

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.9+ from https://python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host "`n🎉 Setup complete!" -ForegroundColor Green
Write-Host "Start the CLI with:" -ForegroundColor Cyan
Write-Host "python xrcli_entrypoint.py --ip YOUR_READER_IP -u admin -p change" -ForegroundColor White
```

Then run:
```powershell
.\setup.ps1
```

### Linux/macOS (Bash)

#### Prerequisites
```bash
# Check Python version (must be 3.9+)
python3 --version

# Check if Git is installed
git --version

# Ubuntu/Debian: Install prerequisites if needed
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# macOS: Install prerequisites if needed (with Homebrew)
brew install python3 git
```

#### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/XerumSrl/XRFID.CLI.git
cd XRFID.CLI

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Verify installation
python xrcli_entrypoint.py --help
```

#### Automated Setup Script (Linux/macOS)
Create a file called `setup.sh`:

```bash
#!/bin/bash
# XRFID CLI Setup Script for Linux/macOS
# Usage: chmod +x setup.sh && ./setup.sh

echo "🏷️ Zebra RFID CLI Setup"
echo "Developed by Xerum Srl"

# Check Python version
echo -e "\nChecking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Create virtual environment
echo -e "\nCreating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo -e "\n🎉 Setup complete!"
echo "Start the CLI with:"
echo "python xrcli_entrypoint.py --ip YOUR_READER_IP -u admin -p change"
```

Then run:
```bash
chmod +x setup.sh
./setup.sh
```

## Verification

After installation, verify everything works:

```bash
# Test CLI help
python xrcli_entrypoint.py --help

# Test with a reader (replace with your reader's IP)
```bash
# Test with a reader (replace with your reader's IP)
python xrcli_entrypoint.py --ip 192.168.1.100 -u admin -p change
```
```

## Common Installation Issues

### Python Version Issues
- **Issue**: `python: command not found`
- **Solution**: Use `python3` instead of `python`, or add Python to PATH

### Virtual Environment Issues
- **Issue**: `cannot import name '_ssl' from '_socket'`
- **Solution**: Reinstall Python with SSL support

### Permission Issues (Linux/macOS)
- **Issue**: Permission denied errors
- **Solution**: Don't use `sudo` with pip in virtual environment

### Network Issues
- **Issue**: Package download failures
- **Solution**: Check internet connection, try with `--trusted-host pypi.org`

## Next Steps

After successful installation:

1. [Quick Start Guide](quick-start.md) - Get started in 5 minutes
2. [Configuration](configuration.md) - Set up persistent settings
3. [Basic Operations](user-guide/basic-operations.md) - Learn essential commands

---

**Developed by [Xerum Srl](https://xerum.it)** | Licensed under MIT License
