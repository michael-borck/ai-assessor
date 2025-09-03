"""
Basic tests for file utility functions.
"""

import os
import tempfile

from ai_assessor.utils.file_utils import FileUtils


class TestFileUtils:
    """Test cases for FileUtils."""

    def test_get_docx_files_empty_directory(self):
        """Test getting docx files from empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            files = FileUtils.get_docx_files(temp_dir)
            assert files == []

    def test_get_docx_files_with_docx(self):
        """Test getting docx files from directory with docx files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            docx_file = os.path.join(temp_dir, "test.docx")
            txt_file = os.path.join(temp_dir, "test.txt")

            # Create empty files
            with open(docx_file, "w") as f:
                f.write("")
            with open(txt_file, "w") as f:
                f.write("")

            files = FileUtils.get_docx_files(temp_dir)
            assert "test.docx" in files
            assert "test.txt" not in files

    def test_get_docx_files_nonexistent_directory(self):
        """Test handling of non-existent directory."""
        files = FileUtils.get_docx_files("/nonexistent/directory")
        assert files == []
