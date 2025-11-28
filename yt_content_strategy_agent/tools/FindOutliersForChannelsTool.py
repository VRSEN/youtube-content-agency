from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import datetime
import sys
import os
from typing import Dict

# Add parent directory to path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(agent_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from yt_content_strategy_agent.tools.FindChannelOutliersTool import FindChannelOutliersTool


class FindOutliersForChannelsTool(BaseTool):
    """
    Analyzes multiple YouTube channels to find outlier high-performing videos across all of them.
    
    This tool is useful for competitive analysis, identifying trending topics across multiple channels,
    and discovering content strategies that are working well in your niche. It runs the outlier 
    detection for each channel and aggregates the results.
    """
    
    competitors: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping channel IDs to channel names. Example: {'UC123...': 'Channel Name 1', 'UC456...': 'Channel Name 2'}"
    )
    
    max_results: int = Field(
        30,
        description="Maximum number of recent videos to fetch per channel (default: 30)"
    )
    
    days_window: int = Field(
        90,
        description="Only analyze videos published within this many days (default: 90)"
    )
    
    min_duration_seconds: int = Field(
        240,
        description="Minimum video duration in seconds to be considered long-form (default: 240, i.e., 4 minutes)"
    )

    def run(self):
        """
        Execute outlier detection across all specified competitor channels.
        
        Returns a JSON string containing:
        - Timestamp of analysis
        - List of results for each channel (each with outliers, median VPD, etc.)
        """
        # Step 1: Set the analysis timestamp
        today = datetime.datetime.now(tz=datetime.timezone.utc)
        
        # Step 2: Run outlier detection for each channel
        results = []
        for channel_id, channel_name in self.competitors.items():
            # Create a tool instance for this channel
            channel_tool = FindChannelOutliersTool(
                channel_id=channel_id,
                channel_name=channel_name,
                max_results=self.max_results,
                days_window=self.days_window,
                min_duration_seconds=self.min_duration_seconds
            )
            
            # Run the analysis
            channel_result_json = channel_tool.run()
            channel_result = json.loads(channel_result_json)
            results.append(channel_result)
        
        # Step 3: Aggregate results
        output = {
            'today': today.isoformat(),
            'competitors': results,
        }
        
        return json.dumps(output, indent=2)


if __name__ == "__main__":
    # Test case - tech channels
    competitors_dict = {
        "UCXuqSBlHAE6Xw-yeJA0Tunw": "Linus Tech Tips",
        "UCBJycsmduvYEL83R_U4JriQ": "MKBHD",
    }
    
    tool = FindOutliersForChannelsTool(
        competitors=competitors_dict,
        max_results=20,
        days_window=90
    )
    
    result = tool.run()
    print(result)
