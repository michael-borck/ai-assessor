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

# Set up logging
ErrorHandler.setup_logging()

@patch('ai_assessor.core.api_client.OpenAI')
def test_api(mock_openai):
    # Load environment variables
    load_dotenv()

    # Mock the OpenAI client
    mock_client = mock_openai.return_value
    mock_client.models.list.return_value.data = [
        type('model', (object,), {'id': 'gpt-3.5-turbo'})()
    ]
    mock_client.chat.completions.create.return_value.choices = [
        type('choice', (object,), {'message': type('message', (object,), {'content': 'Test feedback'})()})()
    ]

    # Initialize configuration
    config_manager = ConfigManager("config.ini")

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
    system_prompt = "You are a helpful teacher. Grade this submission and provide brief feedback."
    user_prompt = "Please grade the following student work:"
    
    # Create a dummy submission file
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        os.makedirs(submissions_folder)
    submission_file = os.path.join(submissions_folder, "test_submission.docx")
    with open(submission_file, "w") as f:
        f.write("This is a test submission.")

    # Test with real submission
    success, feedback = assessor.grade_submission(
        submission_file=submission_file,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=0.7
    )
    assert success is True
    assert feedback == "Test feedback"
