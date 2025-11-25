from agency_swarm import Agent
import litellm
from agents import ModelSettings
from openai.types.shared import Reasoning

script_writer_agent = Agent(
    name="ScriptWriter",
    description="Expert script writer for YouTube content using GPT-5.1 model.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5.1",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="low",
            summary="auto"
        ),
    ),
)

