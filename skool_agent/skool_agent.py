from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent

skool_agent = Agent(
    name="SkoolAgent",
    description="Template agent for Skool operations. Fill in tools and instructions as needed.",
    instructions="./instructions.md",
    tools_folder="./tools",
    files_folder="./files",
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="low",
            summary="auto"
        ),
    ),
)
