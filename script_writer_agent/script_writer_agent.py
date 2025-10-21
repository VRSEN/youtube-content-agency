from agency_swarm import Agent
import litellm

litellm.modify_params = True

script_writer_agent = Agent(
    name="ScriptWriter",
    description="Expert script writer for YouTube content using Claude Sonnet 4.5 model.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-4o",
)

