#!/usr/bin/env python3
"""
Test submission processing without GUI to debug the API issue
"""

import os
import sys
from dotenv import load_dotenv
from ai_assessor.config import ConfigManager
from ai_assessor.core import Assessor, OpenAIClient
from ai_assessor.utils import ErrorHandler

# Set up logging
ErrorHandler.setup_logging()

def main():
    # Load environment variables
    load_dotenv()

    # Initialize configuration
    config_manager = ConfigManager("config.ini")

    # For testing, let's set the values directly
    # You can modify these values for your setup

    print("=== AI Assessor Submission Test ===")
    print("This will test submission processing without the GUI")

    # Get API settings
    if len(sys.argv) >= 4:
        api_key = sys.argv[1]
        base_url = sys.argv[2] if sys.argv[2] != "none" else None
        model = sys.argv[3]
    else:
        print("\nUsage: python test_submission.py <api_key> <base_url_or_none> <model>")
        print("Example: python test_submission.py sk-xxx none gpt-3.5-turbo")
        print("Example: python test_submission.py sk-xxx http://localhost:11434 llama2")
        return

    # Initialize API client
    ssl_verify = True
    if base_url and "localhost" in base_url:
        ssl_verify = False

    api_client = OpenAIClient(api_key, base_url, ssl_verify)

    # Test connection first
    print(f"\n=== Testing Connection ===")
    print(f"Base URL: {base_url or 'OpenAI default'}")
    print(f"Model: {model}")
    print(f"SSL Verify: {ssl_verify}")

    try:
        models = api_client.list_models()
        model_ids = [m.id for m in models.data]
        print(f"✓ Connection successful! Found {len(model_ids)} models")

        if model not in model_ids:
            print(f"⚠ Warning: Model '{model}' not found in available models")
            print(f"Available models: {model_ids[:10]}...")  # Show first 10
        else:
            print(f"✓ Model '{model}' is available")

    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return

    # Initialize assessor
    assessor = Assessor(api_client, config_manager)

    # Check for actual submissions
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        print(f"\n✗ Submissions folder '{submissions_folder}' not found")
        return

    from ai_assessor.utils.file_utils import FileUtils
    docx_files = FileUtils.get_docx_files(submissions_folder)

    if not docx_files:
        print(f"\n✗ No .docx files found in '{submissions_folder}'")
        return

    print(f"\n=== Found Submissions ===")
    for i, file in enumerate(docx_files):
        print(f"{i+1}. {file}")

    # Test with first submission
    submission_file = os.path.join(submissions_folder, docx_files[0])
    print(f"\n=== Testing Submission: {docx_files[0]} ===")

    # Use simple prompts for testing
    system_prompt = "You are a helpful teaching assistant. Please grade this student submission and provide brief feedback."
    user_prompt = "Please review and grade the following student work:"

    try:
        # Test the full pipeline
        success, feedback = assessor.grade_submission(
            submission_file=submission_file,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            support_files=None,  # Skip support files for initial test
            output_folder=None,  # Don't save output for test
            model=model,
            temperature=0.7
        )

        if success:
            print(f"✓ SUCCESS! Submission processed")
            print(f"Feedback length: {len(feedback)} characters")
            print(f"First 300 chars:\n{feedback[:300]}...")
        else:
            print(f"✗ FAILED: {feedback}")

    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")

    # Check log file for additional details
    log_file = os.path.expanduser("~/aiassessor.log")
    if os.path.exists(log_file):
        print(f"\n=== Recent Log Entries ===")
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:  # Show last 10 lines
                print(line.strip())

if __name__ == "__main__":
    main()