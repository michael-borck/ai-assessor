import httpx
import logging
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
        # Validate required parameters
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.base_url or self.base_url.strip() == "":
            raise ValueError(
                "Base URL is required. Examples: https://api.openai.com (OpenAI) or http://localhost:11434 (Ollama)"
            )

        logging.debug(f"OpenAIClient.initialize - Original base_url: '{self.base_url}'")
        url = self.base_url.strip()
        logging.debug(f"OpenAIClient.initialize - Stripped base_url: '{url}'")
        if not url.endswith("/v1"):
            url = url.rstrip("/") + "/v1"
            logging.debug(f"OpenAIClient.initialize - Modified base_url: '{url}'")
        else:
            logging.debug(
                f"OpenAIClient.initialize - Base_url already ends with /v1: '{url}'"
            )

        http_client = httpx.Client(verify=self.ssl_verify)
        self.client = OpenAI(
            api_key=self.api_key, base_url=url, http_client=http_client
        )

    def update(self, api_key, base_url, ssl_verify):
        """
        Update the API client with new settings.
        This is useful if the user changes settings in the UI.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.ssl_verify = ssl_verify
        logging.debug(
            f"OpenAIClient.update: api_key={api_key}, base_url={base_url}, ssl_verify={ssl_verify}"
        )
        self.initialize()

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
            logging.info("API Call Details:")
            logging.info(f"  Model: {model}")
            logging.info(f"  Temperature: {temperature}")
            logging.info(f"  Max tokens: {max_tokens}")
            logging.info(f"  Base URL: {self.base_url}")
            logging.info(f"  SSL Verify: {self.ssl_verify}")
            logging.info(f"  System content length: {len(system_content)} chars")
            logging.info(f"  User content length: {len(user_content)} chars")

            # Build base parameters
            params = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                ],
            }

            # Check if this is a GPT-5 or reasoning model (o1, o3, o4, etc.)
            # These models require max_completion_tokens instead of max_tokens
            # and don't support the temperature parameter
            model_lower = model.lower()
            is_reasoning_model = (
                "gpt-5" in model_lower
                or "o1" in model_lower
                or "o3" in model_lower
                or "o4" in model_lower
            )

            if is_reasoning_model:
                # GPT-5 and reasoning models use max_completion_tokens
                # and don't support temperature
                params["max_completion_tokens"] = max_tokens
                logging.info(
                    f"Using max_completion_tokens for reasoning model: {model}"
                )
            else:
                # Standard models use max_tokens and temperature
                params["max_tokens"] = max_tokens
                params["temperature"] = temperature

            # Use the new API format
            response = self.client.chat.completions.create(**params)

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
