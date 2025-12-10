from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning


planner_agent = Agent(
    name="Planner",
    description="Expert video planner for YouTube content using GPT-5.1 model.",
    instructions="./instructions.md",
    files_folder="./files",
    tools_folder="./tools",
    model="gpt-5.1",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="high", summary="auto"),
    ),
)
