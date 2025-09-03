"""
Basic tests for document processing functionality.
"""

import os
import tempfile

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

        # Should handle non-existent files gracefully
        result = processor.read_word_document("/nonexistent/file.docx")
        assert result == "" or result is None

    def test_write_text_document(self):
        """Test writing text content to a document."""
        processor = DocumentProcessor()

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            output_path = tmp.name

        try:
            # Test basic text writing
            test_content = "This is a test document content."
            processor.write_word_document(output_path, test_content)

            # Verify file was created
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0

        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
