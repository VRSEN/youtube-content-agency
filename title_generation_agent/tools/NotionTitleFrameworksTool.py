# NotionTitleFrameworksTool.py
from agency_swarm.tools import BaseTool
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# YouTube Title Frameworks Database ID from the provided URL
DATABASE_ID = "2065bd4b16a680dfb365ed6f0e3fbd79"

class NotionTitleFrameworksTool(BaseTool):
    """
    Fetches YouTube title frameworks from the Notion database and returns them in a clean, formatted string.
    This tool retrieves all proven high-performing title frameworks that can be used to create compelling YouTube titles.
    """
    

    def run(self):
        """
        Fetch title frameworks from the Notion database and return them formatted for easy use.
        """
        try:
            # Step 1: Initialize Notion client
            notion_api_key = os.getenv("NOTION_API_KEY")
            if not notion_api_key:
                return "❌ Error: NOTION_API_KEY environment variable not found. Please set your Notion API key."
            
            notion = Client(auth=notion_api_key)
            
            # Step 2: Retrieve database to get data source ID (required for querying in newer API)
            database = notion.databases.retrieve(DATABASE_ID)
            data_sources = database.get("data_sources", [])
            
            if not data_sources:
                return "❌ Error: Database has no data sources. Cannot query database."
            
            # Use the first data source (most databases have one)
            data_source_id = data_sources[0]["id"]
            
            # Step 3: Query the data source to get ALL frameworks (handle pagination)
            all_results = []
            start_cursor = None
            
            while True:
                query_params = {
                    "page_size": 100,  # Maximum per page
                }
                
                if start_cursor:
                    query_params["start_cursor"] = start_cursor
                
                # Query through data source (newer API requirement)
                response = notion.data_sources.query(data_source_id, **query_params)
                all_results.extend(response.get("results", []))
                
                # Check if there are more pages
                if not response.get("has_more", False):
                    break
                    
                start_cursor = response.get("next_cursor")
            
            # Step 4: Format the results
            if not all_results:
                return "📝 No title frameworks found in the database."
            
            formatted_frameworks = []
            formatted_frameworks.append("🎯 **YouTube Title Frameworks from Notion Database**\n")
            formatted_frameworks.append("=" * 60)
            
            for idx, page in enumerate(all_results, 1):
                properties = page.get("properties", {})
                
                # Helper function to extract text from various property types
                def extract_text(prop):
                    if not prop:
                        return ""
                    
                    prop_type = prop.get("type", "")
                    
                    if prop_type == "title" and prop.get("title"):
                        return " ".join([t["text"]["content"] for t in prop["title"] if t.get("text")])
                    elif prop_type == "rich_text" and prop.get("rich_text"):
                        return " ".join([t["text"]["content"] for t in prop["rich_text"] if t.get("text")])
                    elif prop_type == "select" and prop.get("select"):
                        return prop["select"]["name"]
                    elif prop_type == "multi_select" and prop.get("multi_select"):
                        return ", ".join([s["name"] for s in prop["multi_select"]])
                    
                    return ""
                
                # Extract the actual properties from your database
                title_framework = extract_text(properties.get("Title Framework"))
                example_title_1 = extract_text(properties.get("Example Title 1"))
                example_title_2 = extract_text(properties.get("Example Title 2"))
                og_title = extract_text(properties.get("OG title"))
                
                # Get view count and other metrics if available
                outlier = properties.get("Outlier", {}).get("number", "")
                yt_link = extract_text(properties.get("YT video link"))
                
                title = title_framework if title_framework else f"Framework #{idx}"
                
                # Format the framework entry
                formatted_frameworks.append(f"\n📌 **{idx}. {title}**")
                
                if og_title:
                    formatted_frameworks.append(f"   Original Title: {og_title}")
                
                if example_title_1:
                    formatted_frameworks.append(f"   Example 1: {example_title_1}")
                
                if example_title_2:
                    formatted_frameworks.append(f"   Example 2: {example_title_2}")
                
                
                if outlier:
                    formatted_frameworks.append(f"   Outlier Score: {outlier}")
                
                if yt_link:
                    formatted_frameworks.append(f"   Video Link: {yt_link}")
                
                formatted_frameworks.append("-" * 50)
            
            # Step 5: Add usage guidance
            formatted_frameworks.append("\n💡 **Usage Guidelines:**")
            formatted_frameworks.append("• Select frameworks that naturally fit your video content")
            formatted_frameworks.append("• Adapt frameworks to match your specific topic and keywords")
            formatted_frameworks.append("• Don't force frameworks that don't suit the video")
            formatted_frameworks.append("• Combine multiple frameworks for creative variations")
            formatted_frameworks.append(f"• Total frameworks fetched: {len(all_results)}")
            
            return "\n".join(formatted_frameworks)
            
        except Exception as e:
            return f"❌ Error fetching title frameworks: {str(e)}\n\nPlease check:\n1. NOTION_API_KEY is set correctly\n2. Database is shared with your integration\n3. Database ID is correct: {DATABASE_ID}"

if __name__ == "__main__":
    # Test the tool
    print("🧪 Testing NotionTitleFrameworksTool:")
    print("-" * 50)
    tool = NotionTitleFrameworksTool()
    result = tool.run()
    print(result)