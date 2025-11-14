from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent
from agents.mcp import MCPServerStdio
import os
from dotenv import load_dotenv

load_dotenv()

# Readwise Reader MCP Server Configuration
# GitHub: https://github.com/edricgsh/readwise-reader-mcp

path_to_readwise_mcp = os.path.join(os.path.dirname(__file__), "../readwise-reader-mcp")

readwise_reader_server = MCPServerStdio(
    name="Readwise_Reader",
    params={
        "command": "node",
        "args": [
            os.path.join(path_to_readwise_mcp, "dist/index.js")
        ],
        "env": {
            "READWISE_TOKEN": os.getenv("READWISE_TOKEN", "your_readwise_token")
        }
    },
    cache_tools_list=True,
    client_session_timeout_seconds=30,
    tool_filter={
        "allowed_tool_names": ["readwise_list_documents"]
    }
)

newsletter_agent = Agent(
    name="NewsletterAgent",
    description="A specialized agent for fetching and summarizing news from Readwise Reader, identifying significant releases, updates, and recurring topics relevant for video content.",
    instructions="./instructions.md",
    tools_folder="./tools",
    model="gpt-5.1",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
    mcp_servers=[readwise_reader_server],
)

if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("Testing Newsletter Agent...")
        print("-" * 50)
        
        # Test query to fetch latest news
        response = await newsletter_agent.get_response(
            "Fetch the latest AI news from the last 7 days and provide a summary of the most significant topics."
        )
        
        print("\nAgent Response:")
        print(response)
    
    asyncio.run(main())


