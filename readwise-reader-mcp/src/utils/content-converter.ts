import { parse } from 'node-html-parser';

// Convert URL content using jina.ai
export async function convertWithJina(url: string): Promise<string> {
  const jinaUrl = `https://r.jina.ai/${url}`;
  
  const response = await fetch(jinaUrl, {
    headers: {
      'Accept': 'text/plain',
      'User-Agent': 'Readwise-MCP-Server/1.0.0'
    }
  });
  
  if (!response.ok) {
    throw new Error(`Jina conversion failed: ${response.status}`);
  }
  
  return response.text();
}

// Extract text content from HTML string
export function extractTextFromHtml(htmlContent: string): string {
  if (!htmlContent?.trim()) {
    return '';
  }
  
  const root = parse(htmlContent);
  
  // Remove non-content elements
  root.querySelectorAll('script, style, nav, header, footer').forEach(el => el.remove());
  
  // Get title and body text
  const title = root.querySelector('title')?.text?.trim() || '';
  const bodyText = root.querySelector('body')?.text || root.text || '';
  
  // Clean up whitespace
  const cleanText = bodyText.replace(/\s+/g, ' ').trim();
  
  return title ? `${title}\n\n${cleanText}` : cleanText;
}

// Convert URL content to LLM-friendly text
export async function convertUrlToText(url: string, category?: string): Promise<string> {
  if (!url?.trim()) {
    return '';
  }
  
  try {
    // Use jina for articles and PDFs, lightweight HTML parsing for others
    const shouldUseJina = !category || category === 'article' || category === 'pdf';
    
    if (shouldUseJina) {
      return await convertWithJina(url);
    } else {
      // For non-article/pdf content, we'll rely on HTML content from Readwise
      // This function is now mainly used as a fallback
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Readwise-MCP-Server/1.0.0',
          'Accept': 'text/html,application/xhtml+xml'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTML fetch failed: ${response.status}`);
      }
      
      const html = await response.text();
      return extractTextFromHtml(html);
    }
  } catch (error) {
    console.warn('Error converting URL to text:', error);
    return '[Content unavailable - conversion error]';
  }
} 