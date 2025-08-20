# Project Structure

This project follows Python software architecture best practices:

## Directory Structure

```
pythonYoutDownloader/
├── README.md                   # Project documentation
├── pyproject.toml             # Modern Python packaging configuration
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── Makefile                   # Build automation
├── .gitignore                 # Git ignore patterns
├── __init__.py               # Root package marker
│
├── src/                      # Source code package
│   ├── __init__.py          # Package initialization
│   └── youtube_downloader.py # Main application code
│
├── tests/                   # Test package
│   ├── __init__.py         # Test package initialization
│   ├── test_downloader.py  # Unit tests
│   └── demo.py             # Demo/integration tests
│
├── docs/                   # Documentation
│   ├── ENVIRONMENT_SETUP.md
│   ├── ENVIRONMENT_SETUP_EN.md
│   ├── PACKAGE_MANAGEMENT.md
│   └── PACKAGE_MANAGEMENT_EN.md
│
├── assets/                 # Static assets
│   └── pythonYout.png
│
└── venv/                   # Virtual environment (gitignored)
```

## Architecture Principles

### 1. **Separation of Concerns**
- `src/`: Contains all application logic
- `tests/`: Contains all testing code
- `docs/`: Contains documentation
- `assets/`: Contains static resources

### 2. **Package Structure**
- Each directory has `__init__.py` for proper Python package recognition
- Clear module boundaries and imports

### 3. **Configuration Management**
- `pyproject.toml`: Modern Python packaging standard (PEP 518)
- `requirements.txt`: Production dependencies
- `requirements-dev.txt`: Development dependencies
- `Makefile`: Common development tasks automation

### 4. **Development Workflow**
- `make install`: Install production dependencies
- `make install-dev`: Install development dependencies
- `make test`: Run tests
- `make lint`: Run code linting
- `make format`: Format code
- `make run`: Run the application

### 5. **Testing Strategy**
- Unit tests in `tests/test_downloader.py`
- Integration demo in `tests/demo.py`
- Both pytest-compatible and standalone runnable

### 6. **Code Quality**
- Type hints throughout the codebase
- Comprehensive docstrings
- Error handling and validation
- Consistent code style (configurable with black/flake8)

## Usage

### Development Setup
```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Run the application
make run
```

### Production Usage
```bash
# Install production dependencies only
make install

# Run the application
python src/youtube_downloader.py
```

This structure follows Python packaging best practices and enables easy maintenance, testing, and distribution.