"""
Basic tests for configuration management.
"""

import os
import tempfile

from ai_assessor.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""

    def test_config_manager_initialization(self):
        """Test that ConfigManager can be initialized."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("[API]\nKey = test_key\n")
            config_file = f.name

        try:
            config = ConfigManager(config_file)
            assert config is not None
        finally:
            os.unlink(config_file)

    def test_get_value_with_default(self):
        """Test getting configuration values with defaults."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("[API]\nKey = test_key\nDefaultModel = gpt-4-turbo\n")
            config_file = f.name

        try:
            config = ConfigManager(config_file)

            # Test existing value
            assert config.get_value("API", "Key", "") == "test_key"

            # Test default value
            assert config.get_value("API", "NonExistentKey", "default") == "default"
        finally:
            os.unlink(config_file)

    def test_set_value(self):
        """Test setting configuration values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
            f.write("[API]\nKey = old_key\n")
            config_file = f.name

        try:
            config = ConfigManager(config_file)
            config.set_value("API", "Key", "new_key")

            assert config.get_value("API", "Key", "") == "new_key"
        finally:
            os.unlink(config_file)
