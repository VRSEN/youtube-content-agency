from agents import ModelSettings
from agency_swarm import Agent
from dotenv import load_dotenv
import datetime

load_dotenv()

grok_news_agent = Agent(
    name="GrokNewsAgent", 
    description="A specialized news research agent that uses Grok AI to fetch the most recent AI news and viral tweets, providing trend analysis and content opportunities for YouTube content strategy.",
    instructions="./instructions.md",
    model="litellm/xai/grok-4",
    model_settings=ModelSettings(
        max_tokens=25000,
        extra_body={
            "search_parameters": {
                "mode": "on",
                "from_date": (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
                "returnCitations": True,
                "sources": [
                    {"type": "x", "post_view_count": 100000},
                    # {"type": "news", "country": "US"}
                ],
                "max_search_results": 30,
            },
            "reasoning": {
                "effort": "high",
                "summary": "auto"
            }
        }
    ),
)

if __name__ == "__main__":
    print("Grok News Agent initialized successfully")
    print(f"Model: {grok_news_agent.model}")
    print(f"Tools available: {grok_news_agent.tools}")
