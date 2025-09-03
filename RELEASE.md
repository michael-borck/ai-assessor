# Release Guide

This document describes how to create releases for AI Assessor with automatic builds for Windows and Linux.

## Release Process

### 1. Prepare for Release

1. Ensure all changes are committed and pushed to `main`
2. Run tests and quality checks:
   ```bash
   pytest
   black .
   flake8 .
   mypy ai_assessor
   ```
3. Update version numbers if needed in relevant files
4. Update CHANGELOG.md with release notes

### 2. Create a Release

Releases are created through GitHub's web interface and trigger automatic builds:

1. Go to your repository on GitHub
2. Click "Releases" in the right sidebar
3. Click "Create a new release"
4. Create a new tag (e.g., `v1.0.0`, `v1.1.0`)
5. Fill in the release title and description
6. Click "Publish release"

### 3. Automatic Builds

When you create a release, GitHub Actions will automatically:

**Windows Build:**
- Build a Windows executable using PyInstaller
- Package it as a ZIP file
- Upload `AI_Assessor_Windows_vX.X.X.zip` to the release

**Linux Build:**
- Build a Linux executable using PyInstaller
- Package it as an AppImage
- Upload `AI_Assessor_Linux_vX.X.X.AppImage` to the release

### 4. Manual Local Builds (Optional)

You can also build locally for testing:

**Windows:**
```bash
python build_windows.py
```

**Linux:**
```bash
python build_linux.py
```

## Release Triggers

The build workflow is triggered by:
- **Push to main**: Creates artifacts for testing (not attached to releases)
- **Pull requests**: Creates artifacts for testing
- **Release creation**: Creates artifacts AND uploads them to the release

## Distribution

After a release is created:

**Windows Users:**
1. Download `AI_Assessor_Windows_vX.X.X.zip`
2. Extract the ZIP file
3. Run `AI_Assessor.exe`

**Linux Users:**
1. Download `AI_Assessor_Linux_vX.X.X.AppImage`
2. Make it executable: `chmod +x AI_Assessor_Linux_vX.X.X.AppImage`
3. Run it: `./AI_Assessor_Linux_vX.X.X.AppImage`

## Version Numbering

Use semantic versioning (semver): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Examples: `v1.0.0`, `v1.1.0`, `v1.1.1`

## Troubleshooting

**Build Failures:**
- Check the Actions tab in GitHub for detailed logs
- Ensure all dependencies are properly specified in requirements.txt
- Test builds locally first

**Release Assets Missing:**
- Ensure the release was created (not just a tag)
- Check that the workflow completed successfully
- Assets are uploaded only on successful builds
