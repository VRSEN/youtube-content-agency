from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import math
import datetime
import re
import os
from typing import Optional
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


def _parse_duration_to_seconds(dur: str) -> int:
    """Parse ISO8601 YouTube duration (e.g. PT16M4S) into seconds."""
    if not isinstance(dur, str) or not dur.startswith('PT'):
        return 0
    hours = minutes = seconds = 0
    for val, unit in re.findall(r"(\d+)([HMS])", dur):
        if unit == 'H':
            hours = int(val)
        elif unit == 'M':
            minutes = int(val)
        elif unit == 'S':
            seconds = int(val)
    return hours * 3600 + minutes * 60 + seconds


class FindChannelOutliersTool(BaseTool):
    """
    Finds outlier long-form videos for a single YouTube channel based on views-per-day (VPD) performance.
    
    Outliers are defined as videos in the top 20% of 28-day VPD among the last 12 eligible 
    long-form uploads in the specified time window. This helps identify which video topics 
    and formats are performing exceptionally well for a channel.
    """
    
    channel_id: str = Field(
        ..., 
        description="The YouTube channel ID to analyze (e.g., 'UC...')"
    )
    
    channel_name: Optional[str] = Field(
        None,
        description="Optional: Human-readable channel name for reporting purposes"
    )
    
    max_results: int = Field(
        30,
        description="Maximum number of recent videos to fetch from the channel (default: 30)"
    )
    
    days_window: int = Field(
        90,
        description="Only analyze videos published within this many days (default: 90)"
    )
    
    min_duration_seconds: int = Field(
        240,
        description="Minimum video duration in seconds to be considered long-form (default: 240, i.e., 4 minutes). This filters out Shorts."
    )

    def run(self):
        """
        Execute the outlier detection analysis for the specified channel.
        
        Returns a JSON string containing:
        - Channel information
        - Median and 80th percentile VPD values
        - List of all analyzed videos
        - List of outlier videos (top 20% performers)
        """
        # Step 1: Initialize YouTube API client
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return json.dumps({"error": "YOUTUBE_API_KEY not found in environment variables"}, indent=2)
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        today = datetime.datetime.now(tz=datetime.timezone.utc)
        
        # Step 2: Search for recent uploads from the channel
        try:
            search_response = youtube.search().list(
                part='snippet',
                channelId=self.channel_id,
                order='date',
                maxResults=self.max_results,
                type='video'
            ).execute()
        except Exception as e:
            return json.dumps({"error": f"Failed to search videos: {str(e)}"}, indent=2)
        
        videos = []
        
        # Step 3: Process each video found
        for item in search_response.get('items', []):
            vid_id = item['id'].get('videoId')
            if not vid_id:
                continue
            
            snippet = item.get('snippet', {})
            title = snippet.get('title')
            published_at_str = snippet.get('publishedAt')
            
            if not published_at_str:
                continue
            
            try:
                published_at = datetime.datetime.fromisoformat(
                    published_at_str.replace('Z', '+00:00')
                )
            except Exception:
                continue
            
            age_days = (today - published_at).days
            if age_days > self.days_window:
                continue
            
            days_since = max(age_days, 1)
            
            # Step 4: Fetch detailed stats for each video
            try:
                video_response = youtube.videos().list(
                    part='contentDetails,statistics',
                    id=vid_id
                ).execute()
            except Exception as e:
                continue
            
            if not video_response.get('items'):
                continue
            
            video_data = video_response['items'][0]
            content_details = video_data.get('contentDetails', {})
            statistics = video_data.get('statistics', {})
            
            duration_seconds = _parse_duration_to_seconds(content_details.get('duration', 'PT0S'))
            if duration_seconds < self.min_duration_seconds:
                # Skip shorts / very short videos
                continue
            
            try:
                views = int(statistics.get('viewCount', 0))
            except Exception:
                views = 0
            
            # Calculate views per day for different windows
            vpd_28 = views / max(1, min(days_since, 28))
            vpd_7 = views / max(1, min(days_since, 7))
            
            videos.append(
                {
                    'channel_id': self.channel_id,
                    'channel_name': self.channel_name,
                    'video_id': vid_id,
                    'title': title,
                    'published_at': published_at_str,
                    'days_since': days_since,
                    'views': views,
                    'duration_seconds': duration_seconds,
                    'duration_min': round(duration_seconds / 60, 1),
                    'vpd_28': round(vpd_28, 2),
                    'vpd_7': round(vpd_7, 2),
                    'url': f'https://www.youtube.com/watch?v={vid_id}',
                }
            )
        
        # Step 5: Use the 12 most recent eligible long-form videos
        videos_sorted = sorted(videos, key=lambda x: x['published_at'], reverse=True)[:12]
        
        if not videos_sorted:
            result = {
                'channel_id': self.channel_id,
                'channel_name': self.channel_name,
                'median_vpd_28': 0.0,
                'p80_vpd_28': 0.0,
                'videos': [],
                'outliers': [],
            }
            return json.dumps(result, indent=2)
        
        # Step 6: Calculate statistics and identify outliers
        vpd_values = [v['vpd_28'] for v in videos_sorted]
        vpd_values_sorted = sorted(vpd_values)
        
        median = vpd_values_sorted[len(vpd_values_sorted) // 2]
        idx_80 = max(0, math.floor(0.8 * (len(vpd_values_sorted) - 1)))
        p80 = vpd_values_sorted[idx_80]
        
        outliers = [v for v in videos_sorted if v['vpd_28'] >= p80]
        
        result = {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            'median_vpd_28': round(median, 2),
            'p80_vpd_28': round(p80, 2),
            'videos': videos_sorted,
            'outliers': outliers,
        }
        
        return json.dumps(result, indent=2)


if __name__ == "__main__":
    # Test case - Linus Tech Tips channel
    tool = FindChannelOutliersTool(
        channel_id="UCXuqSBlHAE6Xw-yeJA0Tunw",
        channel_name="Linus Tech Tips",
        max_results=30,
        days_window=90
    )
    
    result = tool.run()
    print(result)
