.PHONY: help install install-dev test lint format clean run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting (flake8)"
	@echo "  format      - Format code (black)"
	@echo "  type-check  - Run type checking (mypy)"
	@echo "  clean       - Clean build artifacts"
	@echo "  run         - Run the YouTube downloader"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run tests
test:
	python -m pytest tests/ -v

# Run linting
lint:
	flake8 src/ tests/

# Format code
format:
	black src/ tests/

# Type checking
type-check:
	mypy src/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the application
run:
	python src/youtube_downloader.py

# Build package
build:
	python -m build

# Install in editable mode
install-editable:
	pip install -e .