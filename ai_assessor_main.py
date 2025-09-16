"""
#!/usr/bin/env python3
AI Assessor - An AI-powered tool for grading student submissions.
"""


import os
import tkinter as tk

# Attempt to initialize Xlib for multi-threaded mode
# This is a workaround for a bug in some Linux distributions where tkinter
# can crash in multi-threaded applications.
# See: https://stackoverflow.com/questions/323972/is-tkinter-thread-safe
# try:
# x11 = ctypes.cdll.LoadLibrary("libX11.so")
# x11.XInitThreads()
# except Exception:
# print("Warning: Could not initialize Xlib for multi-threaded mode.")

from dotenv import load_dotenv

from ai_assessor.config import ConfigManager

# Import core components
from ai_assessor.core import Assessor, OpenAIClient
from ai_assessor.utils import ErrorHandler

# Set up logging
ErrorHandler.setup_logging()


def main():
    """
    Main entry point for the application.
    """
    # Load environment variables for API key
    load_dotenv()

    # Initialize configuration
    config_manager = ConfigManager("config.ini")

    # Get API key from environment or config
    api_key = os.getenv("OPENAI_API_KEY") or config_manager.get_value("API", "Key", "")
    base_url = config_manager.get_value("API", "BaseURL", "")

    # Initialize API client (compatible with any OpenAI-compatible provider)
    api_client = OpenAIClient(api_key, base_url)

    # Initialize assessor
    assessor = Assessor(api_client, config_manager)

    # Start GUI
    # For now, we'll import the GUI here to avoid circular imports
    # In future, we can add CLI or web interface conditionally
    from ai_assessor.ui.gui import AIAssessorGUI

    # Initialize and run the GUI
    root = tk.Tk()
    root.title("AI Assessor")
    _ = AIAssessorGUI(root, assessor, config_manager)
    root.mainloop()


if __name__ == "__main__":
    main()
