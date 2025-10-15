from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()

class YouTubeTranscriptTool(BaseTool):
    """
    A tool for fetching transcripts from YouTube videos.
    This tool can extract transcripts from YouTube videos using their URL or video ID,
    and returns the full transcript text for content analysis and strategy development.
    """
    
    video_url: str = Field(
        ...,
        description="The YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID) or just the video ID.",
    )
    
    language: str = Field(
        default="en",
        description="The language code for the transcript (e.g., 'en' for English, 'es' for Spanish). Defaults to 'en'.",
    )
    
    include_timestamps: bool = Field(
        default=False,
        description="Whether to include timestamps in the transcript output. Defaults to True.",
    )

    def run(self):
        """
        Fetches the transcript from a YouTube video.
        """
        try:
            # Step 1: Extract video ID from URL if a full URL is provided
            video_id = self._extract_video_id(self.video_url)
            
            if not video_id:
                return f"Error: Could not extract video ID from URL: {self.video_url}"
            
            # Step 2: Configure proxy if credentials are available
            proxy_username = os.getenv("WEBSHARE_PROXY_USERNAME")
            proxy_password = os.getenv("WEBSHARE_PROXY_PASSWORD")
            
            if proxy_username and proxy_password:
                # Create proxy configuration
                proxy_config = WebshareProxyConfig(
                    proxy_username=proxy_username,
                    proxy_password=proxy_password,
                    filter_ip_locations=["us"]
                )
                api = YouTubeTranscriptApi(proxy_config=proxy_config)
                print("Using Webshare proxy configuration for YouTube API requests")
            else:
                # Use API without proxy
                api = YouTubeTranscriptApi()
                print("No proxy credentials found. Using direct connection to YouTube API")
            
            # Step 3: Fetch the transcript
            try:
                # First try to get transcript in the specified language
                fetched_transcript = api.fetch(video_id, languages=[self.language])
            except Exception:
                # If the specified language is not available, try to get any available transcript
                try:
                    fetched_transcript = api.fetch(video_id)
                    print(f"Warning: Transcript in '{self.language}' not available. Using available transcript.")
                except Exception as inner_e:
                    return f"Error: Could not fetch transcript for video ID {video_id}. Error: {str(inner_e)}"
            
            # Step 4: Format the transcript
            transcript_snippets = fetched_transcript.snippets
            
            if self.include_timestamps:
                formatted_transcript = "\n".join([
                    f"[{self._format_timestamp(snippet.start)}] {snippet.text}"
                    for snippet in transcript_snippets
                ])
            else:
                formatted_transcript = " ".join([snippet.text for snippet in transcript_snippets])
            
            # Step 5: Return the formatted transcript with metadata
            result = f"YouTube Video Transcript (Video ID: {video_id})\n"
            result += f"Language: {fetched_transcript.language_code}\n"
            result += f"Total segments: {len(transcript_snippets)}\n"
            result += "=" * 50 + "\n\n"
            result += formatted_transcript
            
            return result
            
        except Exception as e:
            return f"Unexpected error occurred: {str(e)}"
    
    def _extract_video_id(self, url_or_id):
        """
        Extract video ID from YouTube URL or return the ID if it's already a video ID.
        """
        # If it's already a video ID (11 characters, alphanumeric and dashes/underscores)
        if len(url_or_id) == 11 and re.match(r'^[a-zA-Z0-9_-]+$', url_or_id):
            return url_or_id
        
        # Extract from various YouTube URL formats
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)
        
        return None
    
    def _format_timestamp(self, seconds):
        """
        Convert seconds to MM:SS or HH:MM:SS format.
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    # Test the tool with the provided video URL
    tool = YouTubeTranscriptTool(
        video_url="https://www.youtube.com/watch?v=BG9hXrMoZEU",
        language="en",
        include_timestamps=False
    )
    
    print("Testing YouTube Transcript Tool...")
    result = tool.run()
    print(result[:500] + "..." if len(result) > 500 else result)
