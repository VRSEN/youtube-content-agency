import { ReadwiseClient } from '../readwise-client.js';

let readwiseClient: ReadwiseClient | null = null;

// Initialize the client with token from environment or config
export function initializeClient(): ReadwiseClient {
  if (readwiseClient) {
    return readwiseClient;
  }
  
  const token = process.env.READWISE_TOKEN;
  if (!token) {
    throw new Error('Readwise access token not provided. Please set READWISE_TOKEN in your MCP configuration or environment variables. You can get your token from https://readwise.io/access_token');
  }
  
  readwiseClient = new ReadwiseClient({ token });
  return readwiseClient;
} 