export interface ReadwiseDocument {
  id: string;
  url: string;
  source_url?: string;
  title?: string;
  author?: string;
  source?: string;
  summary?: string;
  published_date?: string | number;
  image_url?: string;
  location: 'new' | 'later' | 'shortlist' | 'archive' | 'feed';
  category?: 'article' | 'book' | 'tweet' | 'pdf' | 'email' | 'youtube' | 'podcast' | 'video';
  tags?: string[] | object;
  site_name?: string;
  word_count?: number | null;
  created_at: string;
  updated_at: string;
  notes?: string;
  parent_id?: string | null;
  reading_progress?: number;
  first_opened_at?: string | null;
  last_opened_at?: string | null;
  saved_at?: string;
  last_moved_at?: string;
  html_content?: string;
}

export interface CreateDocumentRequest {
  url: string;
  html?: string;
  tags?: string[];
  location?: 'new' | 'later' | 'shortlist' | 'archive' | 'feed';
  category?: 'article' | 'book' | 'tweet' | 'pdf' | 'email' | 'youtube' | 'podcast';
}

export interface UpdateDocumentRequest {
  title?: string;
  author?: string;
  summary?: string;
  published_date?: string;
  image_url?: string;
  location?: 'new' | 'later' | 'shortlist' | 'archive' | 'feed';
  category?: 'article' | 'book' | 'tweet' | 'pdf' | 'email' | 'youtube' | 'podcast';
}

export interface ListDocumentsParams {
  id?: string;
  updatedAfter?: string;
  addedAfter?: string;
  location?: 'new' | 'later' | 'shortlist' | 'archive' | 'feed';
  category?: 'article' | 'book' | 'tweet' | 'pdf' | 'email' | 'youtube' | 'podcast';
  tag?: string;
  pageCursor?: string;
  withHtmlContent?: boolean;
  withFullContent?: boolean;
  limit?: number;
}

export interface ListDocumentsResponse {
  count: number;
  nextPageCursor?: string;
  results: ReadwiseDocument[];
}

export interface ReadwiseTag {
  id: string;
  name: string;
}

export interface ReadwiseConfig {
  token: string;
}

export interface APIMessage {
  type: 'info' | 'warning' | 'error';
  content: string;
}

export interface APIResponse<T> {
  data: T;
  messages?: APIMessage[];
}