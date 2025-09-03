"""
Basic tests for document processing functionality.
"""

import os
import tempfile

import pytest

from ai_assessor.utils.document_processor import DocumentProcessor


class TestDocumentProcessor:
    """Test cases for DocumentProcessor."""

    def test_document_processor_initialization(self):
        """Test that DocumentProcessor can be initialized."""
        processor = DocumentProcessor()
        assert processor is not None

    def test_read_nonexistent_file(self):
        """Test handling of non-existent files."""
        processor = DocumentProcessor()

        # Should raise FileNotFoundError for non-existent files
        with pytest.raises(FileNotFoundError):
            processor.read_word_document("/nonexistent/file.docx")

    def test_write_text_document(self):
        """Test writing text content to a document."""
        processor = DocumentProcessor()

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            output_path = tmp.name

        try:
            # Test basic text writing
            test_content = "This is a test document content."
            processor.write_text_file(output_path, test_content)

            # Verify file was created and has content
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0

            # Verify content is correct
            with open(output_path, "r") as f:
                written_content = f.read()
            assert written_content == test_content

        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
