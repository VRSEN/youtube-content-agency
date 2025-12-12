from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import datetime
import sys
import os
from typing import Any, Dict, Iterable, Mapping

# Add parent directory to path for standalone execution
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(agent_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from yt_content_strategy_agent.tools.FindChannelOutliersTool import FindChannelOutliersTool


def _split_channel_ids(raw: str) -> list[str]:
    # Accept comma-separated values and whitespace/newlines.
    parts = [p.strip() for p in raw.replace("\n", ",").split(",")]
    return [p for p in parts if p]


def _normalize_competitors(value: Any) -> Dict[str, str]:
    """
    Normalize 'competitors' into a dict[channel_id] = channel_name.

    Supported inputs (agent-friendly):
    - {"UC...": "Name", "UC...": "Name"}  (dict)
    - [{"channel_id": "UC...", "channel_name": "Name"}, ...] (list of objects)
    - "UC1,UC2,UC3" (comma-separated string)
    - {"channels": <any of the above>} (common agent mis-shape)
    """
    if value is None:
        raise ValueError("competitors is required")

    # Common agent wrapper shape: { "channels": ... }
    if isinstance(value, Mapping) and "channels" in value and len(value) == 1:
        return _normalize_competitors(value["channels"])

    # Dict mapping channel_id -> channel_name
    if isinstance(value, Mapping):
        # If values are strings, treat as the canonical mapping.
        if all(isinstance(k, str) for k in value.keys()) and all(
            isinstance(v, str) for v in value.values()
        ):
            normalized: Dict[str, str] = {}
            for cid, cname in value.items():
                cid = cid.strip()
                cname = cname.strip()
                if not cid:
                    continue
                normalized[cid] = cname or cid
            if not normalized:
                raise ValueError("competitors mapping was empty")
            return normalized

        # Some agents attempt: {"channels": "..."} or {"channels": [...]}, handled above.
        raise ValueError(
            "Unsupported competitors mapping shape. Expected a dict of channel_id -> channel_name."
        )

    # Comma-separated string (or whitespace/newline separated)
    if isinstance(value, str):
        ids = _split_channel_ids(value)
        if not ids:
            raise ValueError("competitors string was empty")
        return {cid: cid for cid in ids}

    # Iterable/list input
    if isinstance(value, Iterable):
        normalized = {}
        for item in value:
            if isinstance(item, str):
                cid = item.strip()
                if cid:
                    normalized[cid] = cid
                continue

            if isinstance(item, Mapping):
                cid = (
                    item.get("channel_id")
                    or item.get("channelId")
                    or item.get("id")
                    or item.get("channel")
                )
                cname = item.get("channel_name") or item.get("channelName") or item.get(
                    "name"
                )
                if isinstance(cid, str):
                    cid = cid.strip()
                if isinstance(cname, str):
                    cname = cname.strip()
                if cid:
                    normalized[cid] = cname or cid
                continue

            raise ValueError(
                "Unsupported competitors list item. Expected str or object with channel_id."
            )

        if not normalized:
            raise ValueError("competitors list was empty")
        return normalized

    raise ValueError(
        "Unsupported competitors type. Use dict, list, or comma-separated string."
    )


class FindOutliersForChannelsTool(BaseTool):
    """
    Analyzes multiple YouTube channels to find outlier high-performing videos across all of them.
    
    This tool is useful for competitive analysis, identifying trending topics across multiple channels,
    and discovering content strategies that are working well in your niche. It runs the outlier 
    detection for each channel and aggregates the results.
    """
    
    competitors: Any = Field(
        ...,
        description=(
            "Competitor channels to analyze. Recommended format is a dict mapping channel IDs to channel names, "
            "e.g. {'UC123...': 'Channel Name 1', 'UC456...': 'Channel Name 2'}. "
            "Agent-friendly alternatives also accepted: "
            "- list of objects [{'channel_id': 'UC...', 'channel_name': '...'}, ...] "
            "- comma-separated string 'UC1,UC2,UC3' "
            "- wrapper object {'channels': <any of the above>}"
        ),
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
        try:
            competitors = _normalize_competitors(self.competitors)
        except Exception as e:
            return json.dumps(
                {
                    "error": "Invalid competitors input",
                    "details": f"{type(e).__name__}: {e}",
                },
                indent=2,
            )

        results = []
        for channel_id, channel_name in competitors.items():
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
