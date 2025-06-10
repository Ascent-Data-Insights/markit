import os
import time
import anthropic
from anthropic._exceptions import OverloadedError


class AnthropicClient:
    """A wrapper around the Anthropic client with a shared system prompt."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.system_prompt = """
        You are a very helpful assistant to a small consulting startup called Ascent Data Insights.
        Ascent is based in Cincinnati, OH, and is a data science consulting company with two employees.
        Our mission is to help small-to-medium sized businesses get the most value out of their data by 
        helping them capture data and improve existing processes. You are going to help us find and research
        potential clients in the Greater Cincinnati Area. 

        Use citations to back up your answer to all research questions.
        """
        # self.model = "claude-3-5-haiku-latest"
        self.model = "claude-3-5-sonnet-latest"
        # self.model = "claude-3-7-sonnet-20250219"

    def create_message(self, prompt, **kwargs):
        """Create a message using the client with the system prompt."""
        max_retries = 5
        base_delay = 1  # Start with 1 second

        for attempt in range(max_retries + 1):
            try:
                return self.client.messages.create(
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
