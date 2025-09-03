# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Assessor is a Python application that automates grading of student submissions using OpenAI's API. It features both GUI and CLI interfaces for different use cases.

## Development Commands

### Running the Application
- **GUI**: `python ai_assessor_main.py`
- **CLI**: `python -m ai_assessor.cli.cli [command] [options]`

### Environment Setup
- **Create virtual environment**: `python -m venv venv`
- **Activate (Linux/macOS)**: `source venv/bin/activate`
- **Activate (Windows)**: `venv\Scripts\activate`
- **Install production dependencies**: `pip install -r requirements.txt`
- **Install development dependencies**: `pip install -r requirements-dev.txt`
- **Setup pre-commit hooks**: `pre-commit install`

### Testing and Code Quality
- **Run tests**: `pytest`
- **Format code**: `black .`
- **Check linting**: `flake8 .`
- **Run pre-commit checks**: `pre-commit run --all-files`

### Distribution Builds
- **Windows executable**: `python build_windows.py`
- **Linux AppImage**: `python build_linux.py`
- **Setup Windows build environment**: `setup_build_windows.bat`

### Automated Releases
- **GitHub Actions**: Automatically builds Windows and Linux executables on release
- **Release process**: Create a GitHub release with a version tag (e.g., `v1.0.0`)
- **Artifacts**: Windows ZIP and Linux AppImage automatically uploaded to release

## Architecture

### Core Structure
The application follows a modular architecture with clear separation of concerns:

```
ai_assessor/
├── core/           # Core business logic
│   ├── api_client.py     # OpenAI API client wrapper
│   └── assessor.py       # Main assessment functionality
├── config/         # Configuration management
├── ui/             # User interfaces
│   ├── gui.py           # Tkinter GUI implementation
│   └── views/           # GUI view components
├── cli/            # Command-line interface
├── utils/          # Utility modules
└── __init__.py
```

### Key Components

- **Assessor** (`ai_assessor.core.assessor`): Main business logic for processing submissions and generating feedback
- **OpenAIClient** (`ai_assessor.core.api_client`): Handles API communication with OpenAI services
- **ConfigManager** (`ai_assessor.config.config_manager`): Manages application configuration via INI files
- **DocumentProcessor** (`ai_assessor.utils.document_processor`): Handles Word document reading/writing
- **GUI** (`ai_assessor.ui.gui`): Tkinter-based graphical interface
- **CLI** (`ai_assessor.cli.cli`): Command-line interface with argument parsing

### Configuration
- Configuration stored in `config.ini` (template: `config.ini.template`)
- Environment variables supported via `.env` file
- API keys managed through environment variables or config file

### Document Processing
- Supports Word documents (.docx) for submissions and support files
- Uses `python-docx` library for document manipulation
- Handles both reading student submissions and writing feedback

### Multi-Interface Design
- **GUI Mode**: Full-featured Tkinter interface for interactive use
- **CLI Mode**: Command-line interface supporting batch operations and automation
- Both interfaces share the same core business logic through the Assessor class

## Dependencies
- `openai>=1.0.0` - OpenAI API client
- `python-docx>=0.8.11` - Word document processing
- `python-dotenv>=1.0.0` - Environment variable management
- `tqdm>=4.65.0` - Progress bars
- `pyinstaller>=5.9.0` - Windows executable building

## Directory Structure
- `prompts/` - System and user prompt templates
- `submissions/` - Student submission files
- `support/` - Reference materials and rubrics
- `output/` - Generated feedback and results
- `core/` - Additional core utilities (separate from ai_assessor/core/)
