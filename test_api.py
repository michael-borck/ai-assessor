#!/usr/bin/env python3
"""
Test script to debug API submission issues without GUI
"""

import os
from unittest.mock import patch
from dotenv import load_dotenv
from ai_assessor.config import ConfigManager
from ai_assessor.core import Assessor, OpenAIClient
from ai_assessor.utils import ErrorHandler
from docx import Document

# Set up logging
ErrorHandler.setup_logging()


@patch("ai_assessor.core.api_client.OpenAI")
def test_api(mock_openai):
    # Create a dummy config.ini file
    with open("config.ini", "w") as f:
        f.write("[Paths]\n")
        f.write("SystemPromptPath = prompts/system_prompt.txt\n")
        f.write("UserPromptPath = prompts/user_prompt.txt\n")
        f.write("SupportFolder = support/\n")
        f.write("SubmissionsFolder = submissions/\n")
        f.write("OutputFolder = output/\n")
        f.write("[API]\n")
        f.write("Key = test_api_key\n")
        f.write("BaseURL = https://api.openai.com\n")
        f.write("DefaultModel = gpt-3.5-turbo\n")
        f.write("Temperature = 0.7\n")
        f.write("SSLVerify = True\n")
        f.write("[Models]\n")
        f.write("gpt-3.5-turbo = gpt-3.5-turbo\n")

    # Load environment variables
    load_dotenv()

    # Mock the OpenAI client
    mock_client = mock_openai.return_value
    mock_client.models.list.return_value.data = [
        type("model", (object,), {"id": "gpt-3.5-turbo"})()
    ]
    mock_client.chat.completions.create.return_value.choices = [
        type(
            "choice",
            (object,),
            {"message": type("message", (object,), {"content": "Test feedback"})()},
        )()
    ]

    # Initialize configuration
    config_manager = ConfigManager("config.ini")

    # Explicitly set config_manager.config for testing purposes
    import configparser
    temp_config = configparser.ConfigParser()
    temp_config.read("config.ini")
    config_manager.config = temp_config

    # Get API settings
    api_key = "test_api_key"
    base_url = "https://api.openai.com"
    model = "gpt-3.5-turbo"

    # Initialize API client
    api_client = OpenAIClient(api_key, base_url)

    # Test connection first
    models = api_client.list_models()
    assert len(models.data) > 0

    # Initialize assessor
    assessor = Assessor(api_client, config_manager)

    # Test submission processing
    system_prompt = (
        "You are a helpful teacher. Grade this submission and provide brief feedback."
    )
    user_prompt = "Please grade the following student work:"

    # Create a dummy submission file
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        os.makedirs(submissions_folder)
    submission_file = os.path.join(submissions_folder, "test_submission.docx")
    document = Document()
    document.add_paragraph("This is a test submission.")
    document.save(submission_file)

    # Test with real submission
    success, feedback = assessor.grade_submission(
        submission_file=submission_file,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=0.7,
    )
    assert success is True
    assert feedback == "Test feedback"

    # Clean up the dummy config file
    os.remove("config.ini")
