# Python Package Management: pip vs uv (Local vs Global)

Complete guide on Python package management, differences between local and global installation, and how to use pip and uv efficiently.

## 1. Fundamental Concepts

### Global vs Local Installation

**Global (System):**

- Packages installed for all projects
- Located at: `/Users/user/.pyenv/versions/3.12.6/lib/python3.12/site-packages/`
- Problems: version conflicts, conflicting dependencies

**Local (Virtual Environment):**

- Packages isolated by project
- Located at: `venv/lib/python3.12/site-packages/`
- Advantages: isolation, specific versions, no conflicts

## 2. pip - Traditional Package Manager

### Basic Commands

```bash
# Check version
pip --version

# Install package
pip install package-name

# Install specific version
pip install package-name==1.2.3

# Install with version constraint
pip install 'package-name>=1.0,<2.0'

# List installed packages
pip list

# Show package information
pip show package-name

# Update package
pip install --upgrade package-name

# Uninstall package
pip uninstall package-name
```

### Dependency Management

```bash
# Create dependencies file
pip freeze > requirements.txt

# Install from dependencies file
pip install -r requirements.txt

# Install in development mode (editable)
pip install -e .
```

### Example requirements.txt

```txt
# Main dependencies
yt-dlp==2025.7.21
requests>=2.31.0,<3.0.0
pydantic>=2.0.0

# Development dependencies
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

## 3. uv - Modern Package Manager (Fast)

### Installing uv

```bash
# Install uv
pip install uv

# Or via curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Basic uv Commands

```bash
# Install package
uv pip install package-name

# Install from requirements.txt
uv pip install -r requirements.txt

# List packages
uv pip list

# Uninstall package
uv pip uninstall package-name

# Create virtual environment
uv venv

# Activate environment (same command as python -m venv)
source .venv/bin/activate  # Linux/macOS
```

### uv Advantages

- **Speed**: 10-100x faster than pip
- **Compatibility**: pip-compatible API
- **Smart cache**: reuses downloads
- **Better resolution**: resolves dependencies more efficiently

## 4. pip vs uv Comparison

| Aspect | pip | uv |
|--------|-----|----|
| Speed | Standard | 10-100x faster |
| Compatibility | Native Python | pip-compatible |
| Cache | Basic | Advanced |
| Dependency resolution | Slow | Fast and intelligent |
| Binary size | Included in Python | ~15MB |
| Maturity | Stable | In development |

## 5. Usage Strategies

### Local Development

```bash
# Create new project
mkdir my-project
cd my-project

# Configure Python
pyenv local 3.12.6

# Create virtual environment
python -m venv venv
# OR using uv (faster)
uv venv

# Activate environment
source venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
# OR pip install -r requirements.txt
```

### Recommended Workflow

```bash
# 1. Always use virtual environment
python -m venv venv && source venv/bin/activate

# 2. Update pip/uv
pip install --upgrade pip uv

# 3. Install dependencies with uv (faster)
uv pip install package-name

# 4. Save dependencies
pip freeze > requirements.txt

# 5. For development, separate dependencies
echo "pytest>=7.0.0" >> requirements-dev.txt
```

## 6. Version Management

### Version Specification

```txt
# requirements.txt - Version specification examples

# Exact version
yt-dlp==2025.7.21

# Minimum version
requests>=2.31.0

# Version with upper limit
numpy>=1.20.0,<2.0.0

# Compatible version (semver)
fastapi~=0.100.0  # Equivalent to >=0.100.0,<0.101.0

# Development version
git+https://github.com/user/repo.git@branch

# Local editable package
-e .
```

### Dependency Updates

```bash
# See outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all (be careful!)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
```

## 7. Environments for Different Use Cases

### Development

```bash
# requirements-dev.txt
-r requirements.txt
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
pre-commit>=3.0.0
```

### Production

```bash
# requirements-prod.txt (fixed versions)
yt-dlp==2025.7.21
requests==2.31.0
pydantic==2.5.3
```

### Testing

```bash
# requirements-test.txt
-r requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

## 8. Complementary Tools

### pip-tools (Advanced Management)

```bash
# Install pip-tools
pip install pip-tools

# Create requirements.in
echo "yt-dlp" > requirements.in
echo "requests>=2.31.0" >> requirements.in

# Generate requirements.txt with fixed versions
pip-compile requirements.in

# Update dependencies
pip-compile --upgrade requirements.in
```

### pyproject.toml (Modern)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "youtube-downloader"
version = "1.0.0"
dependencies = [
    "yt-dlp>=2025.7.21",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
]
```

## 9. Automation Scripts

### Quick Setup Script

```bash
#!/bin/bash
# setup.sh

echo "Setting up Python environment..."

# Check if pyenv exists
if ! command -v pyenv &> /dev/null; then
    echo "pyenv not found. Please install it first."
    exit 1
fi

# Configure local Python
pyenv local 3.12.6

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate

# Update pip and install uv
pip install --upgrade pip uv

# Install dependencies
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
    echo "Dependencies installed successfully!"
else
    echo "requirements.txt file not found."
fi

echo "Environment configured! Use 'source venv/bin/activate' to activate."
```

## 10. Best Practices

### Project Checklist

- [ ] Always use virtual environment
- [ ] Fix Python version with pyenv local
- [ ] Specify versions in requirements.txt
- [ ] Separate dependencies (dev, prod, test)
- [ ] Use uv for speed (when available)
- [ ] Keep requirements.txt updated
- [ ] Don't commit venv/ folder
- [ ] Document setup in README.md

### Verification Commands

```bash
# Check current environment
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"
echo "Environment: $VIRTUAL_ENV"
echo "Packages: $(pip list | wc -l)"

# Check consistency
pip check

# Security audit
pip-audit  # Install with: pip install pip-audit
```

This guide provides a solid foundation for managing Python packages efficiently and securely.
