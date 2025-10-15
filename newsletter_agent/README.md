# Newsletter Agent

The Newsletter Agent connects to Readwise Reader via MCP to fetch and analyze news articles, identifying significant AI releases, updates, and events relevant for video content creation.

## Features

- Fetches articles from Readwise Reader within specified time periods
- Identifies and summarizes significant AI news and updates
- Detects repeated topics across multiple sources (strong signals)
- Filters for content relevant to AI development and YouTube videos
- Works alongside GrokNewsAgent to provide comprehensive news coverage

## Setup Instructions

### 1. Install the Readwise Reader MCP Server

**For Local Development:**

The Readwise Reader MCP server is cloned locally in the `readwise-reader-mcp/` directory.

To set it up:

```bash
# Clone if not already present
git clone https://github.com/edricgsh/readwise-reader-mcp.git readwise-reader-mcp

# Install and build
cd readwise-reader-mcp
npm install
npm run build
```

**For Production:**

The Dockerfile automatically clones and builds the MCP server during Docker build. No manual setup needed - it's handled automatically in the deployment process.

### 2. Get Your Readwise Access Token

1. Visit: https://readwise.io/access_token
2. Log in to your Readwise account
3. Copy your access token

### 3. Configure Environment Variables

Add your Readwise token to the `.env` file in the root directory:

```bash
READWISE_TOKEN=your_readwise_token_here
```

Replace `your_readwise_token_here` with your actual Readwise access token.

### 4. Add Articles to Readwise Reader

Before testing, make sure you have some AI-related articles saved in your Readwise Reader:

1. Visit [Readwise Reader](https://readwise.io/read)
2. Use the browser extension or email forwarding to save articles
3. Tag articles with relevant topics (e.g., "AI", "agents", "tools")
4. Organize by location (new, later, shortlist)

### 5. Verify the Setup

Test the newsletter agent connection:

```bash
cd /path/to/content-agency-1
python -m newsletter_agent.newsletter_agent
```

This will fetch articles from the last 7 days and provide a summary. If you haven't saved any articles yet, the agent will let you know and suggest next steps.

## Available MCP Tools

The newsletter agent has access to the following Readwise Reader tool via MCP:

- **readwise_list_documents**: List and filter documents from Readwise Reader
  - Filter by time period (e.g., last 7 days)
  - Filter by location (new, later, shortlist, archive, feed)
  - Filter by category (article, tweet, pdf, etc.)
  - Filter by tags
  - Optionally fetch full content for deep analysis

**Note**: Only the `readwise_list_documents` tool is enabled for this agent to focus on news analysis rather than content management.

## Usage

The Newsletter Agent is designed to be used by the YouTube Content Strategy Agent. When the strategy agent needs news insights, it will automatically contact both:

1. **GrokNewsAgent**: For viral social media trends from X/Twitter
2. **NewsletterAgent**: For structured news articles from Readwise Reader

Topics that appear in both sources are considered the strongest signals for video content.

### Example Workflow

1. Content Strategy Agent requests news for video ideation
2. Newsletter Agent fetches articles from Readwise Reader (last 7 days by default)
3. Agent analyzes articles for:
   - Major product launches and updates
   - Repeated topics across multiple sources
   - Relevance to AI development and agents
   - Video content potential
4. Agent returns structured summary with recommendations

## Communication Flow

```
YouTubeContentStrategyAgent
├── NewsletterAgent (Readwise Reader news)
└── GrokNewsAgent (X/Twitter trends)
```

The strategy agent contacts both news agents simultaneously to maximize coverage and identify the strongest content signals.

## Readwise Reader Tips

To get the most out of the Newsletter Agent:

1. **Tag Your Content**: Tag AI-related articles in Readwise Reader for better filtering
2. **Use Locations**: Organize articles by priority (new, later, shortlist, archive)
3. **Save Regularly**: Add relevant AI news sources to your Readwise Reader feed
4. **Focus on Quality**: The agent prioritizes articles that appear across multiple sources

## Troubleshooting

### "READWISE_TOKEN not found"

- Make sure you've added `READWISE_TOKEN` to your `.env` file
- Verify the token is valid by visiting https://readwise.io/access_token

### "Failed to connect to MCP server"

- Ensure Node.js is installed on your system
- Try running `npx readwise-reader-mcp` manually to test
- Check that your internet connection is working

### "No documents found"

- Make sure you have articles saved in your Readwise Reader account
- Try adjusting the time period (default is 7 days)
- Check if the articles are in the expected locations (new, later, etc.)

## API Rate Limits

Readwise Reader API has the following rate limits:

- Default: 20 requests/minute
- Document CREATE/UPDATE: 50 requests/minute
- 429 responses include "Retry-After" header

The agent is designed to work within these limits.

## References

- [Readwise Reader MCP Server GitHub](https://github.com/edricgsh/readwise-reader-mcp)
- [Readwise Reader API Documentation](https://readwise.io/reader_api)
- [Agency Swarm MCP Integration](https://agency-swarm.ai/core-framework/tools/mcp-integration)
