# TODO: choose a different wored from "client" since it is overloaded in this repo
class BaseInterface:
    """An interface class for all AI clients we may want to use.
    
    Simply wraps ai clients with a shared system prompt and standard create_message interface.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.system_prompt = """
        You are a very helpful assistant to a small consulting startup called Ascent Data Insights.
        Ascent is based in Cincinnati, OH, and is a data science consulting company with two employees.
        Our mission is to help small-to-medium sized businesses get the most value out of their data by 
        helping them capture data and improve existing processes. You are going to help us find and research
        potential clients in the Greater Cincinnati Area. 

        Use citations to back up your answer to all research questions.
        """

    def create_message(self, prompt, **kwargs) -> str:
        """Create a message using the client with the system prompt."""
        raise NotImplementedError("This method should be implemented by subclasses.")
