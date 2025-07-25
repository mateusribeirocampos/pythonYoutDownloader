# Complete Guide: Local Python Environment Setup

This guide explains how to set up a local Python environment using pyenv, virtual environments, and package management with pip and uv.

## 1. pyenv Installation and Configuration

### macOS

```bash
# Install pyenv via Homebrew
brew install pyenv

# Add to shell profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

### Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev python3-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc or ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload
source ~/.bashrc
```

### Essential pyenv Commands

```bash
# List available versions
pyenv install --list

# Install a specific version
pyenv install 3.12.6

# List installed versions
pyenv versions

# Set global version (system-wide)
pyenv global 3.12.6

# Set local version (current project)
pyenv local 3.12.6

# View current version
pyenv version
```

## 2. Virtual Environment Management

### Creating and Activating Virtual Environments

```bash
# Navigate to project directory
cd /path/to/your/project

# Set local Python version (optional)
pyenv local 3.12.6

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Verify it's active (should show (venv) in prompt)
which python
python --version
```

### Deactivating and Removing Environments

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment (delete folder)
rm -rf venv
```

## 3. Recommended Project Structure

```bash
my-project/
├── .python-version    # Python version (pyenv local)
├── venv/             # Virtual environment
├── requirements.txt  # pip dependencies
├── pyproject.toml   # uv/poetry configuration
├── src/             # Source code
├── tests/           # Tests
├── README.md        # Documentation
└── .gitignore       # Ignore venv/ and others
```

## 4. Recommended .gitignore File

```gitignore
# Virtual environments
venv/
env/
ENV/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 5. Verification Commands

### Check Current Configuration

```bash
# Active Python version
python --version

# Python location
which python

# Available pyenv versions
pyenv versions

# Packages installed in current environment
pip list

# Environment information
pip show pip
```

### Automatic Verification Script

```bash
#!/bin/bash
echo "=== Python Environment Verification ==="
echo "Python version: $(python --version)"
echo "Python location: $(which python)"
echo "pip version: $(pip --version)"
echo "Active virtual environment: $VIRTUAL_ENV"
echo "pyenv version: $(pyenv version)"
echo "Installed packages: $(pip list | wc -l) packages"
```

## 6. Best Practices

### Project Isolation

```bash
# For each new project:
mkdir new-project
cd new-project
pyenv local 3.12.6
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Dependencies Management

```bash
# Create requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Install development dependencies only
pip install -r requirements-dev.txt
```

### Example requirements.txt

```txt
# requirements.txt
yt-dlp==2025.7.21
requests>=2.31.0

# requirements-dev.txt (development)
-r requirements.txt
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
```

## 7. Common Problem Solutions

### Python not found after installing pyenv

```bash
# Check if PATH is correct
echo $PATH | grep pyenv

# Reload shell configurations
source ~/.zshrc  # or ~/.bashrc
```

### Virtual environment won't activate

```bash
# Check if script exists
ls venv/bin/activate

# Give execution permission
chmod +x venv/bin/activate

# Activate with full path
source ./venv/bin/activate
```

### SSL/certificate problems

```bash
# macOS - install certificates
/Applications/Python\ 3.12/Install\ Certificates.command

# Linux - install ca-certificates
sudo apt-get update && sudo apt-get install ca-certificates
```

## 8. Backup and Restore Commands

### Configuration Backup

```bash
# Save list of installed Python versions
pyenv versions > pyenv-versions.txt

# Save dependencies
pip freeze > requirements.txt

# Save project configuration
echo "$(pyenv local)" > .python-version
```

### Restore on New Machine

```bash
# Install pyenv (follow previous steps)

# Install necessary Python versions
cat pyenv-versions.txt | grep -v system | xargs -I {} pyenv install {}

# Configure project
cd project
pyenv local $(cat .python-version)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This guide provides a solid foundation for managing Python environments professionally and in isolation.