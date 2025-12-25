from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning
from agency_swarm.tools import WebSearchTool


planner_agent = Agent(
    name="Planner",
    description="Expert video planner for YouTube content using GPT-5.2 model.",
    instructions="./instructions.md",
    files_folder="./files",
    tools_folder="./tools",
    tools=[WebSearchTool()],
    model="anthropic/claude-sonnet-4.5",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="high", summary="auto"),
    ),
)
