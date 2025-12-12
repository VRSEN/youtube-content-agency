from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent

curious_ai_explorer_agent = Agent(
    name="CuriousAIExplorerAgent",
    description="A YouTube viewer persona representing the top-of-funnel audience for Arseny's channel. When interacting with this agent, you must provide unbaised context closely matching it with what the viewer would see. No second opinions.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
)

