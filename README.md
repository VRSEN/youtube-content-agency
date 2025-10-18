# YouTube Content Agency

A production-ready [Agency Swarm](https://github.com/VRSEN/agency-swarm) implementation for YouTube content strategy, featuring AI-powered news analysis, trend detection, competitor analysis, and content ideation.

---

## 🎯 What This Agency Does

- **📰 Discover Trending Topics**: Analyzes news from multiple sources (Readwise Reader + X/Twitter)
- **🔍 Analyze Competitors**: Tracks competitor videos and identifies successful strategies
- **💡 Generate Video Ideas**: Creates data-driven content ideas based on trends and gaps
- **✨ Optimize Titles**: Generates high-performing video titles using proven frameworks
- **📊 Track Performance**: Analyzes channel metrics, comments, and transcripts
- **⏱️ Create Timestamps**: Automatically generates engaging video timestamps

---

## 🚀 Quick Start on Agencii Platform (Recommended)

1. **Fork this repository** to your own GitHub account
2. **Sign up** at [agencii.ai](https://agencii.ai/)
3. **Connect your repository** and click deploy
4. **Add API keys** when prompted during deployment

That's it! Your agency will be deployed and ready to use.

## 🤖 Agency Architecture

```
YouTubeContentStrategyAgent (Entry Point)
├── NewsletterAgent (Readwise Reader articles)
├── GrokNewsAgent (X/Twitter trends)
├── TitleGenerationAgent (Title optimization)
│   └── BuilderTomAgent (ICP feedback)
└── BuilderTomAgent (ICP feedback)
```

**Agents**:

- **YouTube Content Strategy Agent**: Main orchestrator for content strategy and analysis
- **Newsletter Agent**: Fetches and analyzes news from Readwise Reader
- **Grok News Agent**: Discovers viral AI content from X/Twitter
- **Title Generation Agent**: Generates optimized titles using Notion frameworks (optional)
- **Builder Tom Agent**: ICP persona providing audience feedback on titles and content ideas

---

## 💡 Usage Examples

Copy and paste these prompts to try the agency:

```
Generate video ideas based on the latest AI news
```

```
Analyze competitor performance this week
```

```
What should I make a video about next?
```

```
Generate titles for a video about [topic]
```

```
Analyze the performance of my latest video
```

```
Generate timestamps for video [URL or ID]
```

---

## 🔧 Customization

### Configure Your Channel

**File**: `channel_description.md`

Edit this file to customize for your channel:

- Channel details (name, description, subscriber count)
- Content focus and topics
- Target audience demographics
- Mission, values, and goals

### Update Competitor List

**File**: `yt_content_strategy_agent/instructions.md`

Find the "Primary Competitors" section and update with your competitors:

```markdown
#### Primary Competitors

1. Competitor Name: `UCxxxxxxxxxxxxxxxxxx`
2. Another Channel: `UCxxxxxxxxxxxxxxxxxx`
```

The agent will automatically track these channels.

### Configure News Sources

**Readwise Reader**:

- Save AI-related articles, blogs, and documentation
- Tag articles with relevant topics (e.g., "AI", "agents", "tools")
- The agent will analyze articles from your reading list

**X/Twitter via Grok**:

- Automatically monitors viral AI content
- No manual setup needed

### Title Frameworks (Optional)

**File**: `title_generation_agent/tools/NotionTitleFrameworksTool.py`

If using Notion for title frameworks:

1. Create a Notion database with your title templates
2. Add your Notion database ID to the tool
3. Set `NOTION_API_KEY` in your `.env` file

**Note**: The Notion API key is optional. You can skip title generation if you don't need it.

---

## 🏗️ Project Structure

```
youtube-content-agency/
├── agency.py                           # Main agency entry point
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Container configuration
├── .env                                # Environment variables (create this)
├── channel_description.md              # Your channel configuration
│
├── yt_content_strategy_agent/          # Main orchestrator
├── newsletter_agent/                   # Readwise Reader integration
├── grok_news_agent/                    # X/Twitter trends
├── title_generation_agent/             # Title optimization
├── builder_tom_agent/                  # ICP feedback persona
│
├── py-mcp-youtube-toolbox/             # YouTube MCP server
└── readwise-reader-mcp/                # Readwise MCP server
```

---

## 💻 Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-content-agency.git
cd youtube-content-agency
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# News Sources
READWISE_TOKEN=your_readwise_token_here
XAI_API_KEY=your_xai_api_key_here

# YouTube Integration
YOUTUBE_API_KEY=your_youtube_api_key_here

# Optional - for title generation
NOTION_API_KEY=your_notion_api_key_here
```

**Get your Readwise token**: [https://readwise.io/access_token](https://readwise.io/access_token)  
**Sign up for Readwise Reader**: [https://readwise.io/read](https://readwise.io/read) (I use this to check newsletters)

#### 4. Test the Agency

```bash
python agency.py
```

---

## 🛠️ Troubleshooting

If you encounter any issues, please [open an issue on GitHub](https://github.com/vrsen/youtube-content-agency/issues).

---

## 📖 Learn More

- **[Agency Swarm Documentation](https://agency-swarm.ai/)**
- **[Agency Swarm GitHub](https://github.com/VRSEN/agency-swarm)**
- **[Readwise Reader MCP](https://github.com/edricgsh/readwise-reader-mcp)**
- **[MCP Integration Guide](https://agency-swarm.ai/core-framework/tools/mcp-integration)**

---

Built with ❤️ using [Agency Swarm](https://agency-swarm.ai/)
