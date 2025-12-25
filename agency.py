from dotenv import load_dotenv
from agency_swarm import Agency
from agents import set_default_openai_client, set_tracing_export_api_key
from openai import AsyncOpenAI
import os
from yt_content_strategy_agent import yt_content_strategy_agent
from title_generation_agent import title_generation_agent
from grok_news_agent import grok_news_agent
from newsletter_agent import newsletter_agent
from agency_swarm.tools.send_message import SendMessageHandoff
from curious_ai_explorer_agent import curious_ai_explorer_agent
from script_writer_agent import script_writer_agent
from thumbnail_generator_agent import thumbnail_generator_agent
from planner_agent import planner_agent

load_dotenv()

# Patch MultiProvider to support anthropic prefix with OpenRouter
from agents.models.multi_provider import MultiProvider

def patched_get_fallback_provider(self, prefix):
    if prefix is None or prefix == "openai" or prefix == "anthropic":
        return self.openai_provider
    elif prefix in self._fallback_providers:
        return self._fallback_providers[prefix]
    else:
        self._fallback_providers[prefix] = self._create_fallback_provider(prefix)
        return self._fallback_providers[prefix]

def patched_get_model(self, model_name):
    """Keep full model name for anthropic models when using OpenRouter"""
    prefix, stripped_model_name = self._get_prefix_and_model_name(model_name)
    
    # For anthropic models, keep the full model name with prefix
    if prefix == "anthropic":
        return self.openai_provider.get_model(model_name)
    
    # For other models, use original behavior
    if prefix and self.provider_map and (provider := self.provider_map.get_provider(prefix)):
        return provider.get_model(stripped_model_name)
    else:
        return self._get_fallback_provider(prefix).get_model(stripped_model_name)

MultiProvider._get_fallback_provider = patched_get_fallback_provider
MultiProvider.get_model = patched_get_model

openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)
set_default_openai_client(openrouter_client)
set_tracing_export_api_key(os.environ.get("OPENAI_API_KEY"))

# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    agency = Agency(
        yt_content_strategy_agent, title_generation_agent, thumbnail_generator_agent, script_writer_agent, planner_agent, curious_ai_explorer_agent,
        communication_flows=[
            (yt_content_strategy_agent, title_generation_agent, SendMessageHandoff),
            (yt_content_strategy_agent, grok_news_agent),
            (yt_content_strategy_agent, script_writer_agent, SendMessageHandoff),
            (yt_content_strategy_agent, planner_agent, SendMessageHandoff),
            (yt_content_strategy_agent, newsletter_agent),
            (yt_content_strategy_agent, curious_ai_explorer_agent),
            (yt_content_strategy_agent, thumbnail_generator_agent, SendMessageHandoff),
            (title_generation_agent, curious_ai_explorer_agent),
            (title_generation_agent, thumbnail_generator_agent, SendMessageHandoff),
            (title_generation_agent, planner_agent, SendMessageHandoff),
            (thumbnail_generator_agent, curious_ai_explorer_agent),
            (script_writer_agent, curious_ai_explorer_agent),
            (planner_agent, curious_ai_explorer_agent),
            (planner_agent, script_writer_agent, SendMessageHandoff),
        ],
        name="YouTubeContentAgency", # don't forget to rename your agency!
        shared_instructions="channel_description.md",
        load_threads_callback=load_threads_callback,
    )

    return agency

if __name__ == "__main__":
    agency = create_agency()

    # test 1 message
    # async def main():
    #     response = await agency.get_response("Hello, how are you?")
    #     print(response)
    # asyncio.run(main())

    # run in terminal
    agency.terminal_demo()