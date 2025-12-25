from agency_swarm import Agent
from agents import ModelSettings
from openai.types.shared import Reasoning

script_writer_agent = Agent(
    name="ScriptWriter",
    description="Expert script writer for YouTube content using GPT-5.2 model.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="anthropic/claude-sonnet-4.5",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="low",
            summary="auto"
        ),
    ),
)

