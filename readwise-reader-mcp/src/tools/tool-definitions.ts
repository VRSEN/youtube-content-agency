import { Tool } from '@modelcontextprotocol/sdk/types.js';

export const tools: Tool[] = [
  {
    name: 'readwise_save_document',
    description: 'Save a document (URL or HTML content) to Readwise Reader',
    inputSchema: {
      type: 'object',
      properties: {
        url: {
          type: 'string',
          description: 'URL of the document to save',
        },
        html: {
          type: 'string',
          description: 'HTML content of the document (optional)',
        },
        tags: {
          type: 'array',
          items: { type: 'string' },
          description: 'Tags to add to the document',
        },
        location: {
          type: 'string',
          enum: ['new', 'later', 'shortlist', 'archive', 'feed'],
          description: 'Location to save the document (default: new)',
        },
        category: {
          type: 'string',
          enum: ['article', 'book', 'tweet', 'pdf', 'email', 'youtube', 'podcast'],
          description: 'Category of the document (auto-detected if not specified)',
        },
      },
      required: ['url'],
      additionalProperties: false,
    },
  },
  {
    name: 'readwise_list_documents',
    description: 'List documents from Readwise Reader with optional filtering',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'string',
          description: 'Filter by specific document ID',
        },
        updatedAfter: {
          type: 'string',
          description: 'Filter documents updated after this date (ISO 8601)',
        },
        addedAfter: {
          type: 'string',
          description: 'Filter documents added after this date (ISO 8601). Note: This will fetch all documents first and then filter client-side.',
        },
        location: {
          type: 'string',
          enum: ['new', 'later', 'shortlist', 'archive', 'feed'],
          description: 'Filter by document location',
        },
        category: {
          type: 'string',
          enum: ['article', 'book', 'tweet', 'pdf', 'email', 'youtube', 'podcast'],
          description: 'Filter by document category',
        },
        tag: {
          type: 'string',
          description: 'Filter by tag name',
        },
        pageCursor: {
          type: 'string',
          description: 'Page cursor for pagination',
        },
        withHtmlContent: {
          type: 'boolean',
          description: '⚠️ PERFORMANCE WARNING: Include HTML content in the response. This significantly slows down the API. Only use when explicitly requested by the user or when raw HTML is specifically needed for the task.',
        },
        withFullContent: {
          type: 'boolean',
          description: '⚠️ PERFORMANCE WARNING: Include full converted text content in the response. This significantly slows down the API as it fetches and processes each document\'s content. Only use when explicitly requested by the user or when document content is specifically needed for analysis/reading. Default: false for performance.',
        },
      },
      additionalProperties: false,
    },
  },
  {
    name: 'readwise_update_document',
    description: 'Update a document in Readwise Reader',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'string',
          description: 'Document ID to update',
        },
        title: {
          type: 'string',
          description: 'New title for the document',
        },
        author: {
          type: 'string',
          description: 'New author for the document',
        },
        summary: {
          type: 'string',
          description: 'New summary for the document',
        },
        published_date: {
          type: 'string',
          description: 'New published date (ISO 8601)',
        },
        image_url: {
          type: 'string',
          description: 'New image URL for the document',
        },
        location: {
          type: 'string',
          enum: ['new', 'later', 'shortlist', 'archive', 'feed'],
          description: 'New location for the document',
        },
        category: {
          type: 'string',
          enum: ['article', 'book', 'tweet', 'pdf', 'email', 'youtube', 'podcast'],
          description: 'New category for the document',
        },
      },
      required: ['id'],
      additionalProperties: false,
    },
  },
  {
    name: 'readwise_delete_document',
    description: 'Delete a document from Readwise Reader',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'string',
          description: 'Document ID to delete',
        },
      },
      required: ['id'],
      additionalProperties: false,
    },
  },
  {
    name: 'readwise_list_tags',
    description: 'List all tags from Readwise Reader',
    inputSchema: {
      type: 'object',
      properties: {},
      additionalProperties: false,
    },
  },
  {
    name: 'readwise_topic_search',
    description: 'Search documents in Readwise Reader by topic using regex matching on title, summary, notes, and tags',
    inputSchema: {
      type: 'object',
      properties: {
        searchTerms: {
          type: 'array',
          items: { type: 'string' },
          description: 'List of search terms to match against document content (case-insensitive regex matching)',
          minItems: 1,
        },
      },
      required: ['searchTerms'],
      additionalProperties: false,
    },
  },
]; 