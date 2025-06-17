import os
import time
import anthropic
from ai_interfaces.base_interface import BaseInterface
from anthropic._exceptions import OverloadedError


class AnthropicInterface(BaseInterface):
    """A wrapper around the Anthropic interface with a shared system prompt."""

    def __init__(self):
        super().__init__(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.interface = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-haiku-latest"
        # self.model = "claude-3-5-sonnet-latest"
        # self.model = "claude-3-7-sonnet-20250219"

    def create_message(self, prompt, **kwargs) -> str:
        """Create a message using the interface with the system prompt."""
        max_retries = 5
        base_delay = 1  # Start with 1 second

        for attempt in range(max_retries + 1):
            try:
                response = self.interface.messages.create(
                    system=self.system_prompt,
                    max_tokens=6000,
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    tools=[
                        {
                            "type": "web_search_20250305",
                            "name": "web_search",
                            "max_uses": 5,
                        },
                    ],
                    # thinking={"type": "enabled", "budget_tokens": 2000},
                    **kwargs,
                )
                return response.content[-1].text
            except OverloadedError as e:
                if attempt == max_retries:
                    # Last attempt failed, re-raise the exception
                    raise e

                # Calculate exponential backoff delay (1, 2, 4, 8, 16, 32 seconds max)
                delay = min(base_delay * (2**attempt), 32)
                print(
                    f"API overloaded, retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries + 1})"
                )
                time.sleep(delay)
