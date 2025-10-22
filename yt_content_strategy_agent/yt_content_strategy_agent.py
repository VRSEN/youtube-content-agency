from agents import ModelSettings
from openai.types.shared import Reasoning
from agency_swarm import Agent
from agents.mcp import MCPServerStdio
from agents.tool import WebSearchTool
import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

path_to_stdio_mcp_server = os.path.join(os.path.dirname(__file__), "../py-mcp-youtube-toolbox")

youtube_toolbox_server = MCPServerStdio(
    name="YouTube Toolbox",
    params={
        "command": "uv",
        "args": [
            "--directory",
            path_to_stdio_mcp_server,
            "run",
            "server.py"
        ],
        "env": {
            "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY", "your_youtube_api_key")
        }
    },
    cache_tools_list=True,
	  client_session_timeout_seconds=10,
    tool_filter={
        "blocked_tool_names": ["get_video_transcript", "get_video_enhanced_transcript"]
    }
)

yt_content_strategy_agent = Agent(
    name="YouTubeContentStrategyAgent",
    description="A specialized agent for developing YouTube content strategies, optimizing video, channel, and trend performance, and analyzing audience engagement to maximize channel growth.",
    instructions="./instructions.md",
    tools_folder="./tools",
    tools=[WebSearchTool()],
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="medium",
            summary="auto"
        ),
    ),
    mcp_servers=[youtube_toolbox_server],
)

if __name__ == "__main__":
    async def main():
        await youtube_toolbox_server.connect()
        tools = await youtube_toolbox_server.list_tools()
        print(tools)

    asyncio.run(main())
