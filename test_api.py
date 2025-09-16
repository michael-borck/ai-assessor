#!/usr/bin/env python3
"""
Test script to debug API submission issues without GUI
"""

import os
from dotenv import load_dotenv
from ai_assessor.config import ConfigManager
from ai_assessor.core import Assessor, OpenAIClient
from ai_assessor.utils import ErrorHandler

# Set up logging
ErrorHandler.setup_logging()

def test_api():
    # Load environment variables
    load_dotenv()

    # Initialize configuration
    config_manager = ConfigManager("config.ini")

    # Get API settings - you'll need to set these
    api_key = input("Enter your API key: ").strip()
    base_url = input("Enter base URL (leave empty for OpenAI): ").strip()
    model = input("Enter model name (e.g., gpt-3.5-turbo): ").strip()

    if not api_key:
        print("API key is required!")
        return

    if not model:
        model = "gpt-3.5-turbo"

    # Initialize API client
    ssl_verify = True
    if base_url and "localhost" in base_url:
        ssl_verify = False

    api_client = OpenAIClient(api_key, base_url, ssl_verify)

    # Test connection first
    print("\n=== Testing Connection ===")
    try:
        models = api_client.list_models()
        print(f"✓ Connection successful! Found {len(models.data)} models")
        for m in models.data[:5]:  # Show first 5 models
            print(f"  - {m.id}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return

    # Initialize assessor
    assessor = Assessor(api_client, config_manager)

    # Test submission processing
    print("\n=== Testing Submission Processing ===")

    # Simple test content
    system_prompt = "You are a helpful teacher. Grade this submission and provide brief feedback."
    user_prompt = "Please grade the following student work:"

    # Check if there are actual submissions
    submissions_folder = "submissions"
    if os.path.exists(submissions_folder):
        from ai_assessor.utils.file_utils import FileUtils
        docx_files = FileUtils.get_docx_files(submissions_folder)
        if docx_files:
            submission_file = os.path.join(submissions_folder, docx_files[0])
            print(f"Testing with submission: {submission_file}")
        else:
            print("No .docx files found in submissions folder, creating test submission...")
            submission_file = None
    else:
        print("No submissions folder found, creating test submission...")
        submission_file = None

    # If no real submission, create a simple test
    if not submission_file:
        test_submission = "This is a test student submission. The student wrote: 'Hello, this is my assignment about Python programming.'"
        try:
            result = api_client.generate_assessment(
                system_content=system_prompt,
                user_content=f"{user_prompt}\n\nStudent Submission:\n{test_submission}",
                model=model,
                temperature=0.7
            )
            print(f"✓ Test submission processed successfully!")
            print(f"Response length: {len(result)} characters")
            print(f"First 200 chars: {result[:200]}...")
        except Exception as e:
            print(f"✗ Test submission failed: {e}")
    else:
        # Test with real submission
        try:
            success, feedback = assessor.grade_submission(
                submission_file=submission_file,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=model,
                temperature=0.7
            )
            if success:
                print(f"✓ Real submission processed successfully!")
                print(f"Feedback length: {len(feedback)} characters")
                print(f"First 200 chars: {feedback[:200]}...")
            else:
                print(f"✗ Real submission failed: {feedback}")
        except Exception as e:
            print(f"✗ Real submission failed with exception: {e}")

if __name__ == "__main__":
    test_api()