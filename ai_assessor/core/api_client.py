import httpx
from openai import OpenAI


class OpenAIClient:
    """Client for OpenAI-compatible API providers."""

    def __init__(self, api_key, base_url=None, ssl_verify=True):
        self.api_key = api_key
        self.base_url = base_url
        self.ssl_verify = ssl_verify
        self.client = None

    def initialize(self):
        """Initialize the API client for OpenAI-compatible providers."""
        url = self.base_url
        if url and not url.endswith("/v1"):
            url = url.rstrip("/") + "/v1"

        http_client = httpx.Client(verify=self.ssl_verify)
        self.client = OpenAI(
            api_key=self.api_key, base_url=url, http_client=http_client
        )

    def list_models(self):
        """
        List available models from the provider.

        Returns:
            list: A list of model IDs.

        Raises:
            Exception: If the API call fails.
        """
        if not self.client:
            self.initialize()
        try:
            return self.client.models.list()
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")

    def generate_assessment(
        self, system_content, user_content, model, temperature=0.7, max_tokens=3500
    ):
        """
        Generate an assessment using the LLM provider's API.

        Args:
            system_content (str): The system prompt with any support materials
            user_content (str): The user prompt with student submission
            model (str): The model to use
            temperature (float): The temperature setting (0-1)
            max_tokens (int): Maximum tokens in the response

        Returns:
            str: The generated feedback

        Raises:
            Exception: If API call fails
        """
        import logging

        try:
            # Initialize client if not already done
            if not self.client:
                self.initialize()

            # Debug logging to help diagnose submission failures
            logging.info(f"API Call Details:")
            logging.info(f"  Model: {model}")
            logging.info(f"  Temperature: {temperature}")
            logging.info(f"  Max tokens: {max_tokens}")
            logging.info(f"  Base URL: {self.base_url}")
            logging.info(f"  SSL Verify: {self.ssl_verify}")
            logging.info(f"  System content length: {len(system_content)} chars")
            logging.info(f"  User content length: {len(user_content)} chars")

            # Use the new API format
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract the response (new API format)
            result = response.choices[0].message.content.strip()
            logging.info(f"API call successful, response length: {len(result)} chars")
            return result
        except Exception as e:
            logging.error(f"API call failed with error: {str(e)}")
            logging.error(f"Error type: {type(e).__name__}")
            import traceback
            logging.error(f"Full traceback: {traceback.format_exc()}")
            raise Exception(f"API call failed: {str(e)}")
