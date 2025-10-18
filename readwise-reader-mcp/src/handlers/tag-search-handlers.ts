import { initializeClient } from '../utils/client-init.js';

export async function handleListTags(args: any) {
  const client = initializeClient();
  const response = await client.listTags();
  const tagsText = response.data.map((tag: any) => `- ${tag.name}`).join('\n');

  let responseText = `Available tags:\n${tagsText}`;
  
  if (response.messages && response.messages.length > 0) {
    responseText += '\n\nMessages:\n' + response.messages.map(msg => `${msg.type.toUpperCase()}: ${msg.content}`).join('\n');
  }

  return {
    content: [
      {
        type: 'text',
        text: responseText,
      },
    ],
  };
}

export async function handleTopicSearch(args: any) {
  const client = initializeClient();
  const { searchTerms } = args as { searchTerms: string[] };
  
  const response = await client.searchDocumentsByTopic(searchTerms);
  
  const searchResults = {
    searchTerms,
    totalMatches: response.data.length,
    documents: response.data.map((doc: any) => ({
      id: doc.id,
      url: doc.url,
      title: doc.title,
      author: doc.author,
      source: doc.source,
      category: doc.category,
      location: doc.location,
      tags: doc.tags,
      site_name: doc.site_name,
      word_count: doc.word_count,
      created_at: doc.created_at,
      updated_at: doc.updated_at,
      published_date: doc.published_date,
      summary: doc.summary,
      image_url: doc.image_url,
      source_url: doc.source_url,
      notes: doc.notes,
      reading_progress: doc.reading_progress,
      first_opened_at: doc.first_opened_at,
      last_opened_at: doc.last_opened_at,
      saved_at: doc.saved_at,
      last_moved_at: doc.last_moved_at,
    }))
  };

  let responseText = JSON.stringify(searchResults, null, 2);
  
  if (response.messages && response.messages.length > 0) {
    responseText += '\n\nMessages:\n' + response.messages.map(msg => `${msg.type.toUpperCase()}: ${msg.content}`).join('\n');
  }

  return {
    content: [
      {
        type: 'text',
        text: responseText,
      },
    ],
  };
} 