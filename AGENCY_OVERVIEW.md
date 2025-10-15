# YouTube Content Agency

A specialized Agency Swarm implementation for YouTube content strategy, featuring AI-powered news analysis, trend detection, and content ideation.

## Agency Structure

### Agents

#### 1. **YouTube Content Strategy Agent** (Entry Point)

- **Role**: Main orchestrator for YouTube content strategy and analysis
- **Capabilities**:
  - Generates video ideas based on trends and news
  - Analyzes competitor videos and channel performance
  - Performs individual video analysis
  - Generates timestamps for videos
  - Coordinates with other agents for comprehensive insights
- **MCP Integration**: YouTube Toolbox MCP server
- **Tools**:
  - YouTubeTranscriptTool
  - YouTube API tools (via MCP)

#### 2. **Newsletter Agent** (NEW)

- **Role**: Fetches and analyzes news from Readwise Reader
- **Capabilities**:
  - Fetches articles within specified time periods
  - Identifies significant AI releases and updates
  - Detects repeated topics across multiple sources
  - Filters for video-relevant content
  - Provides structured news summaries
- **MCP Integration**: Readwise Reader MCP server
- **Key Features**:
  - Time-based filtering (default: 7 days)
  - Topic search across saved articles
  - Tag-based organization
  - Performance-optimized content fetching
- **Setup**: See `newsletter_agent/README.md`

#### 3. **Grok News Agent**

- **Role**: Discovers viral AI content from X/Twitter
- **Capabilities**:
  - Monitors X (Twitter) for viral AI tweets and threads
  - Identifies trending GitHub repositories
  - Tracks major AI company announcements
  - Analyzes engagement metrics
  - Focuses on actionable business applications
- **Key Features**:
  - Real-time social media trend detection
  - GitHub repository discovery
  - Tutorial potential assessment
  - Business impact analysis

#### 4. **Title Generation Agent**

- **Role**: Generates optimized titles and thumbnail text
- **Capabilities**:
  - Creates compelling video titles
  - Generates thumbnail text
  - Uses Notion frameworks for optimization
  - Applies proven title patterns
- **Tools**: NotionTitleFrameworksTool

#### 5. **Skool Agent**

- **Role**: Manages Skool community interactions
- **Capabilities**:
  - Posts updates to Skool community
  - Manages community engagement
  - Shares video content

## Communication Flows

```
YouTubeContentStrategyAgent (Entry Point)
├── NewsletterAgent (Readwise Reader articles)
├── GrokNewsAgent (X/Twitter trends)
├── TitleGenerationAgent (Title/thumbnail generation) [Handoff]
└── SkoolAgent (Community management) [Handoff]
```

### News Gathering Strategy

When generating video ideas, the Content Strategy Agent contacts both news agents **simultaneously**:

1. **NewsletterAgent**: Provides structured news from Readwise Reader

   - Saved articles, blog posts, official announcements
   - In-depth analysis and documentation
   - Historical context (up to weeks)

2. **GrokNewsAgent**: Provides viral content from X/Twitter
   - Real-time social media trends
   - Community reactions and engagement
   - Emerging topics and discussions

**Strongest Signals**: Topics that appear in BOTH sources are prioritized for video content.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js (for MCP servers)
- OpenAI API key
- Readwise account and token
- X.ai API key (for Grok)
- YouTube API key
- Notion API key

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd content-agency-1
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
READWISE_TOKEN=your_readwise_token
XAI_API_KEY=your_xai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
NOTION_API_KEY=your_notion_api_key

# Optional
ANTHROPIC_API_KEY=your_anthropic_key
```

4. **Set up Readwise Reader MCP**

See detailed instructions in `newsletter_agent/README.md`

Quick setup:

```bash
# Get your token from https://readwise.io/access_token
# Add it to .env as READWISE_TOKEN
```

5. **Test the agency**

```bash
python agency.py
```

## Usage Examples

### Generating Video Ideas

```
User: "Generate video ideas based on the latest AI news"

The Content Strategy Agent will:
1. Contact NewsletterAgent and GrokNewsAgent simultaneously
2. Gather news from both Readwise Reader and X/Twitter
3. Analyze competitor videos
4. Identify trending topics
5. Generate video ideas with:
   - Potential titles
   - Why they should perform now
   - Key points to discuss
   - Relevance to channel
   - Differentiators
```

### Analyzing Competitors

```
User: "Analyze competitor performance"

The agent will:
1. Fetch latest videos from competitor channels
2. Identify outliers (high-performing videos)
3. Analyze transcripts and comments
4. Provide strategic recommendations
```

### Generating Titles

```
User: "Generate titles for a video about [topic]"

The agent will:
1. Fetch latest videos for reference
2. Hand off to TitleGenerationAgent
3. Return optimized titles and thumbnail text
```

## MCP Servers

### YouTube Toolbox MCP

- **Location**: `py-mcp-youtube-toolbox/`
- **Command**: `uv run server.py`
- **Environment**: `YOUTUBE_API_KEY`

### Readwise Reader MCP

- **Package**: `readwise-reader-mcp` (npm)
- **Command**: `npx -y readwise-reader-mcp`
- **Environment**: `READWISE_TOKEN`
- **Documentation**: https://github.com/edricgsh/readwise-reader-mcp

## Best Practices

### News Analysis

1. **Always use both news agents** when generating ideas
2. **Prioritize repeated topics** across multiple sources
3. **Focus on actionable content** that can be demonstrated
4. **Consider timeliness** - prioritize recent developments

### Content Strategy

1. **Analyze competitors regularly** to identify gaps
2. **Track outlier videos** for trend signals
3. **Align with channel themes** - ensure natural progression
4. **Focus on AI agents** and development tools

### Performance

1. **Avoid full content fetching** unless specifically needed
2. **Use time filters** to limit data volume
3. **Batch operations** when possible
4. **Monitor API rate limits**

## API Rate Limits

- **Readwise Reader**: 20 req/min (default), 50 req/min (create/update)
- **YouTube API**: Varies by quota
- **OpenAI API**: Varies by plan

## Troubleshooting

### Newsletter Agent Issues

See `newsletter_agent/README.md` for detailed troubleshooting

### Common Issues

**"No news found"**

- Check that articles are saved in Readwise Reader
- Verify time period covers saved articles
- Ensure READWISE_TOKEN is valid

**"MCP server connection failed"**

- Verify Node.js is installed
- Check internet connectivity
- Test MCP server manually: `npx -y readwise-reader-mcp`

**"API key invalid"**

- Verify all API keys in `.env` are correct
- Check for extra spaces or newlines
- Regenerate tokens if needed

## Contributing

When adding new agents or tools:

1. Follow Agency Swarm v1.0.0 patterns
2. Use MCP servers when available
3. Document setup requirements
4. Test thoroughly before committing
5. Update this documentation

## References

- [Agency Swarm Documentation](https://agency-swarm.ai/)
- [Readwise Reader MCP](https://github.com/edricgsh/readwise-reader-mcp)
- [MCP Integration Guide](https://agency-swarm.ai/core-framework/tools/mcp-integration)
