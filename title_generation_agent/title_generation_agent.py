from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent

title_generation_agent = Agent(
    name="TitleGenerationAgent",
    description="A specialized agent focused on creating compelling, high-converting YouTube video titles and thumbnail text based on video content, trends, and performance data. Has access to Notion database with proven title frameworks.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="litellm/openai/gpt-5",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
)
