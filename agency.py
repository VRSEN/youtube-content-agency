from dotenv import load_dotenv
from agency_swarm import Agency

from yt_content_strategy_agent import yt_content_strategy_agent
from title_generation_agent import title_generation_agent
from grok_news_agent import grok_news_agent
from newsletter_agent import newsletter_agent
from agency_swarm.tools.send_message import SendMessageHandoff
from curious_ai_explorer_agent import curious_ai_explorer_agent
from script_writer_agent import script_writer_agent
from thumbnail_generator_agent import thumbnail_generator_agent

# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    agency = Agency(
        yt_content_strategy_agent, title_generation_agent, thumbnail_generator_agent, script_writer_agent, curious_ai_explorer_agent,
        communication_flows=[
            (yt_content_strategy_agent, title_generation_agent, SendMessageHandoff),
            (yt_content_strategy_agent, grok_news_agent),
            (yt_content_strategy_agent, script_writer_agent, SendMessageHandoff),
            (yt_content_strategy_agent, newsletter_agent),
            (yt_content_strategy_agent, curious_ai_explorer_agent),
            (yt_content_strategy_agent, thumbnail_generator_agent, SendMessageHandoff),
            (title_generation_agent, curious_ai_explorer_agent),
            (title_generation_agent, thumbnail_generator_agent, SendMessageHandoff),
            (thumbnail_generator_agent, curious_ai_explorer_agent),
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