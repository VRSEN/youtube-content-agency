from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

# Define constants at module level
account_id = "MY_ACCOUNT_ID"
api_key = os.getenv("MY_API_KEY")  # or access_token = os.getenv("MY_ACCESS_TOKEN")


class ExampleTool(BaseTool):
    """
    A brief description of what the custom tool does.
    The docstring should clearly explain the tool's purpose and functionality.
    It will be used by the agent to determine when to use this tool.
    """

    # Define the fields with descriptions using Pydantic Field
    example_field: str = Field(
        ..., description="Description of the example field, explaining its purpose and usage for the Agent."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        # Your custom tool logic goes here
        # Example:
        # do_something(self.example_field, api_key, account_id)

        # Return the result of the tool's operation as a string
        return f"Result of ExampleTool operation with {self.example_field}"


if __name__ == "__main__":
    tool = ExampleTool(example_field="test value")
    print(tool.run())
