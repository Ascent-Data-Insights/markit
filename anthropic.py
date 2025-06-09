import os
import anthropic


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
    
    def create_message(self, messages, **kwargs):
        """Create a message using the client with the system prompt."""
        return self.client.messages.create(
            system=self.system_prompt,
            messages=messages,
            **kwargs
        )
