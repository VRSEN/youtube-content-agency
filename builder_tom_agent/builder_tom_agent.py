from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent

builder_tom_agent = Agent(
    name="BuilderTomAgent",
    description="An ICP (Ideal Customer Profile) persona agent representing the target audience for Arseny's YouTube channel. Provides authentic feedback on video titles, content ideas, and strategies from the perspective of the ideal viewer.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5.1",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
)

