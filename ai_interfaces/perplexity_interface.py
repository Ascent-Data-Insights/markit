import os
from ai_interfaces.base_interface import BaseInterface
from openai import OpenAI


class PerplexityInterface(BaseInterface):
    """Perplexity client."""

    def __init__(self):
        super().__init__(api_key=os.environ["PERPLEXITY_API_KEY"])
        self.model = "sonar"

    def create_message(self, prompt, **kwargs) -> str:
        """Create a message using the client with the system prompt."""
        client = OpenAI(api_key=self.api_key, base_url="https://api.perplexity.ai")

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {   
                "role": "user",
                "content": prompt,
            },
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        message = response.choices[0].message.content

        # Strip the message of code block notation if it exists
        message = message.strip('```').strip('json')

        return message
