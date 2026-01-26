from agents import ModelSettings
from agency_swarm import Agent

curious_ai_explorer_agent = Agent(
    name="PragmaticAIExplorerAgent",
    description="A YouTube viewer persona representing the top-of-funnel audience for Arseny's channel. When interacting with this agent, you must provide unbaised context closely matching it with what the viewer would see. No second opinions.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="litellm/xai/grok-4",
    model_settings=ModelSettings(
        # reasoning=Reasoning(
        #     effort="medium",
        #     summary="auto"
        # ),
    ),
)

