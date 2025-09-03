# Development Setup

This document explains how to set up a development environment for AI Assessor.

## Prerequisites

- Python 3.8 or higher
- Git

## Setup Development Environment

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd ai-assessor
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install development dependencies (includes production deps)
pip install -r requirements-dev.txt
```

### 4. Install Pre-commit Hooks
```bash
pre-commit install
```

## Development Workflow

### Running the Application
```bash
# Make sure venv is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run GUI
python ai_assessor_main.py

# Run CLI
python -m ai_assessor.cli.cli --help
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_assessor

# Run specific test file
pytest tests/test_config.py
```

### Code Formatting and Linting
```bash
# Format code with Black
black .

# Check formatting without changing files
black --check .

# Run linting
flake8 .

# Sort imports
isort .
```

### Pre-commit Checks
```bash
# Run all pre-commit hooks manually
pre-commit run --all-files
```

## Building Windows Executable

### Local Build (Windows only)
```bash
# Make sure venv is activated and dependencies installed
python build_windows.py
```

### CI Build
The Windows executable is automatically built via GitHub Actions on:
- Every push to main
- Pull requests
- New releases

## Virtual Environment Best Practices

- **Always activate the virtual environment** before working on the project
- **Never commit the `venv/` directory** (it's in .gitignore)
- **Recreate the venv if you have issues:**
  ```bash
  deactivate  # if currently in venv
  rm -rf venv  # or rmdir /s venv on Windows
  python -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate
  pip install -r requirements-dev.txt
  ```

## Troubleshooting

### "Command not found" errors
- Make sure virtual environment is activated
- Check that dependencies are installed: `pip list`

### Import errors
- Ensure you're in the project root directory
- Virtual environment is activated
- Dependencies are installed

### Pre-commit hook failures
- Run `black .` to fix formatting issues
- Run `flake8 .` to see linting issues
- Fix issues and try committing again
