from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning


thumbnail_generator_agent = Agent(
    name="ThumbnailGeneratorAgent",
    description="Generates optimized thumbnail text concepts with problem, benefit, and curiosity angles for high CTR YouTube thumbnails",
    instructions="./instructions.md",
    files_folder="./files",
    tools_folder="./tools",
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
)
