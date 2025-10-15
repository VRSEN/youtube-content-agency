from agency_swarm.tools import BaseTool
from datetime import datetime, timezone


class GetCurrentTime(BaseTool):
    """
    Gets the current date and time in ISO 8601 format with timezone information.
    Use this tool to determine the current date before calculating time periods for fetching news.
    """
    
    # No input fields needed - this tool just returns current time
    
    def run(self):
        """
        Returns the current date and time in ISO 8601 format.
        """
        # Get current time in UTC
        current_time = datetime.now(timezone.utc)
        
        # Format as ISO 8601 string
        iso_time = current_time.isoformat()
        
        # Also provide human-readable format
        readable_time = current_time.strftime("%B %d, %Y at %H:%M:%S UTC")
        
        return f"Current time: {readable_time}\nISO 8601 format: {iso_time}\n\nUse this timestamp to calculate relative time periods (e.g., 'last 7 days', 'last 30 days') when fetching documents."


if __name__ == "__main__":
    tool = GetCurrentTime()
    print(tool.run())

