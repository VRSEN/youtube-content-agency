# NotionScriptExamplesTool.py
from agency_swarm.tools import BaseTool
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Notion Database ID for script examples (formatted with dashes)
DATABASE_ID = "fa2a7c11-17aa-4366-bdca-049568653c14"

class NotionScriptExamplesTool(BaseTool):
    """
    Fetches script examples from the Notion database that have "Script" in their title.
    Returns them in markdown format to help understand Arseny Shatokhin's writing style and structure.
    Use this tool before writing scripts to learn from previous examples.
    """

    def run(self):
        """
        Fetch script examples from Notion database and return them in markdown format.
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
            
            # Step 3: Query the data source with filter for "Script" in title
            # Fetch more than needed and filter client-side to ensure quality
            # Sort by last edited time to get the most recent scripts first
            query_params = {
                "page_size": 50,  # Fetch 50 to filter down to 10 good ones
                "filter": {
                    "property": "Name",
                    "title": {
                        "contains": "Script"
                    }
                },
                "sorts": [
                    {
                        "timestamp": "last_edited_time",
                        "direction": "descending"
                    }
                ]
            }
            
            # Query through data source (newer API requirement)
            response = notion.data_sources.query(data_source_id, **query_params)
            all_results = response.get("results", [])
            
            # Step 4: Filter results to only include actual script pages
            # Exclude pages with "Description", "Thumbnail", etc. in the title
            filtered_results = []
            exclude_keywords = ["description", "thumbnail", "idea", "tags"]
            
            for page in all_results:
                properties = page.get("properties", {})
                title_prop = properties.get("Name", {})
                
                # Extract title safely
                page_title = ""
                try:
                    if title_prop.get("title"):
                        page_title = " ".join([
                            t.get("text", {}).get("content", "").lower()
                            for t in title_prop["title"] 
                            if t.get("type") == "text" and t.get("text", {}).get("content")
                        ])
                except Exception:
                    continue
                
                # Check if title contains "script" but NOT any excluded keywords
                if "script" in page_title:
                    is_excluded = any(keyword in page_title for keyword in exclude_keywords)
                    if not is_excluded:
                        filtered_results.append(page)
                        
                        # Stop once we have 10 good scripts
                        if len(filtered_results) >= 10:
                            break
            
            all_results = filtered_results
            
            # Step 5: For each filtered page, fetch the full content
            if not all_results:
                return "📝 No script examples found in the database with 'Script' in the title."
            
            formatted_scripts = []
            formatted_scripts.append("# 📜 Script Examples from Arseny Shatokhin\n")
            formatted_scripts.append("=" * 80)
            formatted_scripts.append("\n")
            
            for idx, page in enumerate(all_results, 1):
                page_id = page.get("id")
                properties = page.get("properties", {})
                
                # Extract title (with safe error handling)
                title_prop = properties.get("Name", {})
                page_title = f"Script {idx}"  # Default title
                try:
                    if title_prop.get("title"):
                        page_title = " ".join([
                            t.get("text", {}).get("content", "") 
                            for t in title_prop["title"] 
                            if t.get("type") == "text" and t.get("text", {}).get("content")
                        ]) or f"Script {idx}"
                except Exception:
                    page_title = f"Script {idx}"
                
                formatted_scripts.append(f"## {idx}. {page_title}\n")
                
                # Step 6: Fetch the page content (blocks)
                try:
                    blocks = []
                    block_cursor = None
                    
                    while True:
                        block_params = {"block_id": page_id, "page_size": 100}
                        if block_cursor:
                            block_params["start_cursor"] = block_cursor
                        
                        block_response = notion.blocks.children.list(**block_params)
                        blocks.extend(block_response.get("results", []))
                        
                        if not block_response.get("has_more", False):
                            break
                        block_cursor = block_response.get("next_cursor")
                    
                    # Step 7: Convert blocks to markdown
                    content_markdown = self._blocks_to_markdown(blocks)
                    formatted_scripts.append(content_markdown)
                    
                except Exception as e:
                    formatted_scripts.append(f"⚠️ Could not fetch content for this page: {str(e)}\n")
                
                formatted_scripts.append("\n" + "-" * 80 + "\n\n")
            
            # Step 8: Add usage guidance
            formatted_scripts.append("\n💡 **How to Use These Examples:**\n")
            formatted_scripts.append("• Study the tone, pacing, and structure of Arseny's scripts")
            formatted_scripts.append("• Notice how he introduces concepts and builds engagement")
            formatted_scripts.append("• Pay attention to his conversational style and technical explanations")
            formatted_scripts.append("• Adapt these patterns while maintaining authenticity")
            formatted_scripts.append(f"• Total script examples fetched: {len(all_results)}\n")
            
            return "\n".join(formatted_scripts)
            
        except Exception as e:
            return f"❌ Error fetching script examples: {str(e)}\n\nPlease check:\n1. NOTION_API_KEY is set correctly\n2. Database is shared with your integration\n3. Database ID is correct: {DATABASE_ID}"
    
    def _blocks_to_markdown(self, blocks):
        """
        Convert Notion blocks to markdown format.
        """
        markdown_lines = []
        
        for block in blocks:
            block_type = block.get("type")
            
            if block_type == "paragraph":
                text = self._extract_rich_text(block.get("paragraph", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(text + "\n")
            
            elif block_type == "heading_1":
                text = self._extract_rich_text(block.get("heading_1", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"# {text}\n")
            
            elif block_type == "heading_2":
                text = self._extract_rich_text(block.get("heading_2", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"## {text}\n")
            
            elif block_type == "heading_3":
                text = self._extract_rich_text(block.get("heading_3", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"### {text}\n")
            
            elif block_type == "bulleted_list_item":
                text = self._extract_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"- {text}\n")
            
            elif block_type == "numbered_list_item":
                text = self._extract_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"1. {text}\n")
            
            elif block_type == "code":
                code_block = block.get("code", {})
                text = self._extract_rich_text(code_block.get("rich_text", []))
                language = code_block.get("language", "")
                if text:
                    markdown_lines.append(f"```{language}\n{text}\n```\n")
            
            elif block_type == "quote":
                text = self._extract_rich_text(block.get("quote", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"> {text}\n")
            
            elif block_type == "callout":
                text = self._extract_rich_text(block.get("callout", {}).get("rich_text", []))
                if text:
                    markdown_lines.append(f"💡 {text}\n")
            
            elif block_type == "divider":
                markdown_lines.append("---\n")
        
        return "\n".join(markdown_lines)
    
    def _extract_rich_text(self, rich_text_array):
        """
        Extract plain text from Notion rich text array, preserving formatting.
        """
        if not rich_text_array:
            return ""
        
        text_parts = []
        for text_obj in rich_text_array:
            if text_obj.get("type") == "text":
                content = text_obj.get("text", {}).get("content", "")
                annotations = text_obj.get("annotations", {})
                
                # Apply markdown formatting based on annotations
                if annotations.get("bold"):
                    content = f"**{content}**"
                if annotations.get("italic"):
                    content = f"*{content}*"
                if annotations.get("code"):
                    content = f"`{content}`"
                if annotations.get("strikethrough"):
                    content = f"~~{content}~~"
                
                text_parts.append(content)
        
        return "".join(text_parts)

if __name__ == "__main__":
    # Test the tool
    print("🧪 Testing NotionScriptExamplesTool:")
    print("-" * 80)
    tool = NotionScriptExamplesTool()
    result = tool.run()
    print(result)

