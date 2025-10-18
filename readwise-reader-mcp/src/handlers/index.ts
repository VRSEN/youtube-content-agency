import { 
  handleSaveDocument, 
  handleListDocuments, 
  handleUpdateDocument, 
  handleDeleteDocument 
} from './document-handlers.js';
import { handleListTags, handleTopicSearch } from './tag-search-handlers.js';

export async function handleToolCall(name: string, args: any) {
  switch (name) {
    case 'readwise_save_document':
      return handleSaveDocument(args);
      
    case 'readwise_list_documents':
      return handleListDocuments(args);
      
    case 'readwise_update_document':
      return handleUpdateDocument(args);
      
    case 'readwise_delete_document':
      return handleDeleteDocument(args);
      
    case 'readwise_list_tags':
      return handleListTags(args);
      
    case 'readwise_topic_search':
      return handleTopicSearch(args);
      
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
} 