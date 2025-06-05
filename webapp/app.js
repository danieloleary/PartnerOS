import React from "react";
import ReactDOM from "react-dom/client";
const App = () => {
  const [docs, setDocs] = React.useState([]);
  const [currentDoc, setCurrentDoc] = React.useState(null);
  const [searchResults, setSearchResults] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [searchQuery, setSearchQuery] = React.useState('');
  const searchIndexRef = React.useRef(null);

  // Section configuration with icons and descriptions
  const sections = {
    'partner_blueprint': {
      icon: '📚',
      title: 'Partner Blueprint',
      description: 'Core documentation and guides'
    },
    'I_Partner_Strategy_Templates': {
      icon: '🎯',
      title: 'Strategy Templates',
      description: 'Strategic planning and evaluation'
    },
    'II_Partner_Recruitment_Templates': {
      icon: '🤝',
      title: 'Recruitment Templates',
      description: 'Partner recruitment and onboarding'
    },
    'III_Partner_Enablement_Templates': {
      icon: '🚀',
      title: 'Enablement Templates',
      description: 'Partner training and support'
    }
  };

  React.useEffect(() => {
    console.log('Starting to load file list...');
    fetch('file_list.json')
      .then(res => {
        if (!res.ok) {
          throw new Error(`Failed to load file_list.json: ${res.status} ${res.statusText}`);
        }
        return res.json();
      })
      .then(paths => {
        console.log('Successfully loaded file_list.json:', {
          pathCount: paths.length,
          paths: paths
        });
        return loadDocs(paths);
      })
      .catch(err => {
        console.error('Error loading file list:', err);
        setIsLoading(false);
      });
  }, []);

  const loadDocs = async (paths) => {
    console.log('Starting to load documents from paths:', paths);
    const loaded = [];
    const errors = [];

    for (const p of paths) {
      try {
        // Ensure the path starts with a slash to be relative to the server root
        const documentPath = p.startsWith('/') ? p : '/' + p;
        console.log('Attempting to fetch document from server root:', documentPath);
        
        const res = await fetch(documentPath);
        if (!res.ok) {
          const error = `Failed to load ${documentPath}: ${res.status} ${res.statusText}`;
          console.error(error);
          errors.push(error);
          continue;
        }

        const text = await res.text();
        if (!text) {
          const error = `Empty content for ${documentPath}`;
          console.error(error);
          errors.push(error);
          continue;
        }

        // --- Frontmatter Parsing ---
        let frontmatter = {};
        let markdownContent = text;
        const lines = text.split('\n');
        let i = 0;
        // Simple detection: look for lines starting with key: value at the beginning
        while (i < lines.length && lines[i].match(/^\s*[a-zA-Z0-9_]+\s*:\s*.*/)) {
          const line = lines[i];
          const colonIndex = line.indexOf(':');
          if (colonIndex > -1) {
            const key = line.substring(0, colonIndex).trim();
            const value = line.substring(colonIndex + 1).trim();
            frontmatter[key] = value;
          }
          i++;
        }
        // The rest of the lines are markdown content
        markdownContent = lines.slice(i).join('\n').trim();
        // --- End Frontmatter Parsing ---

        // Extract section and title from the original path (p) for correct display/categorization
        const pathPartsOriginal = p.split('/');
        const title = frontmatter.title || pathPartsOriginal[pathPartsOriginal.length - 1].replace('.md', '');
        // Use section from frontmatter if available, otherwise from path
        const section = frontmatter.section || pathPartsOriginal.find(part => part !== '..' && part !== '') || 'Unknown';
        
        // Use description from frontmatter if available, otherwise extract first paragraph
        const description = frontmatter.description || text.split('\n\n')[0].replace(/^#+\s*/, '');
        
        const doc = { 
          path: documentPath, // Store the root-relative path
          title, 
          content: markdownContent, // Store only the markdown content
          section, 
          description,
          url: documentPath, // Use the root-relative path for URL as well
          frontmatter // Store the extracted frontmatter
        };
        
        console.log('Successfully loaded document:', {
          path: doc.path,
          title: doc.title,
          section: doc.section,
          contentLength: doc.content.length,
          description: doc.description,
          frontmatter: doc.frontmatter
        });
        
        loaded.push(doc);
      } catch (err) {
        const error = `Error loading ${p}: ${err.message}`;
        console.error(error);
        errors.push(error);
      }
    }

    console.log('Document loading summary:', {
      total: paths.length,
      loaded: loaded.length,
      errors: errors.length,
      errorList: errors
    });

    if (loaded.length === 0) {
      console.error('No documents were loaded successfully!');
    }

    setDocs(loaded);
    buildIndex(loaded);
    setIsLoading(false);
  };

  const buildIndex = (docs) => {
    console.log('Building search index with docs:', docs);
    const idx = lunr(function() {
      this.field('title', { boost: 10 });
      this.field('description', { boost: 5 });
      this.field('content');
      this.ref('path');

      docs.forEach(doc => {
        this.add({
          path: doc.path,
          title: doc.title,
          description: doc.description,
          content: doc.content
        });
      });
    });
    searchIndexRef.current = idx;
    console.log('Search index built successfully');
  };

  const highlightText = (text, query) => {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  };

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      console.log('Searching for:', query);
      const results = searchIndexRef.current.search(query);
      console.log('Search results:', results);
      
      // Map search results to full document data
      const searchResultsWithData = results.map(result => {
        const doc = docs.find(d => d.path === result.ref);
        return {
          ...result,
          title: doc.title,
          description: doc.description,
          section: doc.section
        };
      });
      
      setSearchResults(searchResultsWithData);
    } catch (err) {
      console.error('Search error:', err);
      setSearchResults([]);
    }
  };

  const renderDocList = () => {
    console.log('renderDocList called.');
    console.log('Current docs state:', docs);
    console.log('Configured sections:', sections);

    const docsBySection = {};
    docs.forEach(doc => {
      console.log(`Processing document: ${doc.title}, section: ${doc.section}`);
      if (!docsBySection[doc.section]) {
        docsBySection[doc.section] = [];
        console.log(`Created new section array for: ${doc.section}`);
      }
      docsBySection[doc.section].push(doc);
    });
    console.log('Documents grouped by section:', docsBySection);

    const renderedSections = Object.entries(sections).map(([sectionKey, sectionInfo]) => {
      const sectionDocs = docsBySection[sectionKey] || [];
      console.log(`Attempting to render section: ${sectionKey}, Info: `, sectionInfo, `Documents found: ${sectionDocs.length}`);
      
      // Only render section if there are documents in it
      if (sectionDocs.length === 0) {
        console.log(`Section ${sectionKey} has no documents, skipping render.`);
        return null;
      }

      console.log(`Rendering section ${sectionKey} with ${sectionDocs.length} documents:`, sectionDocs);

      return (
        <div key={sectionKey} className="section">
          <div className="section-header">
            <span className="section-icon">{sectionInfo.icon}</span>
            <div className="section-title-info">
              <h3>{sectionInfo.title}</h3>
              <p className="section-description">{sectionInfo.description}</p>
            </div>
          </div>
          <ul>
            {sectionDocs.map(doc => (
              <li key={doc.path}>
                <a 
                  href="#" 
                  className="link" 
                  onClick={(e) => {
                    e.preventDefault();
                    console.log('Sidebar link clicked, setting currentDoc to:', doc.path);
                    setCurrentDoc(doc);
                  }}
                >
                  {doc.title}
                </a>
                <div className="doc-description">{doc.description}</div>
              </li>
            ))}
          </ul>
        </div>
      );
    });
    
    console.log('Finished renderDocList. Rendered sections array:', renderedSections);
    
    // Filter out nulls from sections with no documents before returning
    return renderedSections.filter(section => section !== null);
  };

  const renderSearchResults = () => {
    if (!searchQuery) return null;
    
    return (
      <div className="search-results">
        <h3>Search Results {searchResults.length > 0 ? `(${searchResults.length})` : ''}</h3>
        {searchResults.length === 0 ? (
          <div className="no-results">No results found for "{searchQuery}"</div>
        ) : (
          searchResults.map(result => (
            <div key={result.ref} className="search-result">
              <a 
                href="#" 
                className="link" 
                onClick={(e) => {
                  e.preventDefault();
                  console.log('Search result link clicked, finding and setting currentDoc for path:', result.ref);
                  const doc = docs.find(d => d.path === result.ref);
                  if (doc) setCurrentDoc(doc);
                  else console.error('Document not found for search result:', result.ref);
                }}
              >
                {result.title}
              </a>
              <div className="result-meta">
                <span className="result-section">
                  {sections[result.section]?.icon} {sections[result.section]?.title}
                </span>
                <span className="result-score">Match: {Math.round(result.score * 100)}%</span>
              </div>
              <div className="result-description">{result.description}</div>
            </div>
          ))
        )}
      </div>
    );
  };

  // Configure marked with highlight.js, security, and custom renderer
  const renderer = new marked.Renderer();

  renderer.link = function(href, title, text) {
    // Check if it's an internal relative link (not starting with #, /, http, etc.)
    if (href && !href.startsWith('#') && !href.startsWith('/') && !href.startsWith('http') && !href.startsWith('mailto')) {
      // Get the directory of the current document
      const currentDocPath = currentDoc ? currentDoc.path : '';
      const currentDocDir = currentDocPath.substring(0, currentDocPath.lastIndexOf('/') + 1);
      
      // Resolve the relative href against the current document's directory
      // We need a simple way to resolve ../ and ./ paths
      // A robust path resolution function might be needed for complex cases, 
      // but for simple relative paths, we can try basic handling.
      let resolvedHref = currentDocDir + href;
      
      // Simple path normalization (handling ../ and ./) - might need more robust logic
      const parts = resolvedHref.split('/');
      const newParts = [];
      for (const part of parts) {
        if (part === '.' || part === '') continue;
        if (part === '..') newParts.pop();
        else newParts.push(part);
      }
      resolvedHref = '/' + newParts.join('/');
      
      console.log(`Resolving link: ${href} from ${currentDocPath} -> ${resolvedHref}`);
      href = resolvedHref;
    }
    
    // For external links, open in a new tab for better UX
    const target = href.startsWith('http') ? '_blank' : '_self';

    return `<a href="${href}" ${title ? `title="${title}"` : ''} target="${target}">${text}</a>`;
  };

  marked.setOptions({
    renderer: renderer,
    highlight: function(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
    langPrefix: 'hljs language-',
    breaks: true,
    gfm: true,
    // baseUrl is less relevant now with custom renderer, but keep for potential fallback
    baseUrl: '/'
  });

  // Function to sanitize and render markdown
  const renderMarkdown = (content) => {
    console.log('Original markdown content (first 500 chars):', content.substring(0, 500) + '...');
    
    const html = marked.parse(content);
    console.log('HTML generated by marked (first 500 chars):', html.substring(0, 500) + '...');

    // DOMPurify.sanitize(html, {
    //   ALLOWED_TAGS: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'code', 'pre', 'blockquote', 'strong', 'em', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'br', 'span', 'div'], // Added span and div
    //   ALLOWED_ATTR: ['href', 'src', 'alt', 'class', 'target', 'style'] // Added style attribute for potential future use
    // });
    // Temporarily disable DOMPurify to see if it's causing issues
    const sanitizedHtml = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'code', 'pre', 'blockquote', 'strong', 'em', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'br', 'span', 'div'],
      ALLOWED_ATTR: ['href', 'src', 'alt', 'class', 'target', 'style']
    });
    console.log('HTML after DOMPurify (first 500 chars):', sanitizedHtml.substring(0, 500) + '...');

    // After rendering and sanitizing, highlight code blocks
    // This needs to happen *after* the HTML is in the DOM, but for debugging, 
    // we can at least see the HTML structure here.
    // The actual highlighting is triggered by highlight.js after the DOM is updated.

    return sanitizedHtml;
  };

  // Update the document content rendering
  const renderDocContent = (doc) => {
    if (!doc) return null;
    
    // Use the title from the document object (extracted from frontmatter or filename)
    const displayTitle = doc.title;

    return (
      <div className="document-content">
        <div className="document-header">
          <h1>{displayTitle}</h1>
          <div className="document-meta">
            <span className="document-section">
              {sections[doc.section]?.icon} {sections[doc.section]?.title}
            </span>
            <span className="document-path">{doc.path}</span>
            {/* Optional: Display other frontmatter here if needed */}
            {/* {doc.frontmatter.template_number && <span>Template #: {doc.frontmatter.template_number}</span>} */}
            {/* {doc.frontmatter.last_updated && <span>Last Updated: {doc.frontmatter.last_updated}</span>} */}
          </div>
        </div>
        <div dangerouslySetInnerHTML={{ __html: renderMarkdown(doc.content) }} />
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <div>Loading documents...</div>
      </div>
    );
  }

  return (
    <div style={{display:'flex', width:'100%'}}>
      <div id="sidebar" tabindex="0">
        <div className="logo-container">
          <img src="assets/partneros-logo.svg" alt="PartnerOS Logo" className="logo" />
        </div>
        <div className="search-container">
          <input 
              className="search-input" aria-label="Search documents"
            type="text" 
            placeholder="Search documents..." 
            value={searchQuery}
            onChange={handleSearch} 
          />
          {searchQuery && !searchResults.length && (
            <div className="no-results">No results found</div>
          )}
        </div>
        {renderSearchResults()}
        {!searchQuery && renderDocList()}
      </div>
      <div id="content">
        {currentDoc ? renderDocContent(currentDoc) : (
          <div className="welcome">
            <div className="welcome-header">
              <img src="assets/partneros-logo.svg" alt="PartnerOS Logo" className="welcome-logo" />
              <h1>Partner Ecosystem Blueprint</h1>
            </div>
            <p>Select a document from the sidebar to begin exploring the blueprint.</p>
            <div className="welcome-features">
              <div className="feature">
                <h3>📚 Comprehensive Templates</h3>
                <p>Access a complete set of templates for partner strategy, recruitment, and enablement.</p>
              </div>
              <div className="feature">
                <h3>🔍 Smart Search</h3>
                <p>Quickly find relevant content with our enhanced search functionality.</p>
              </div>
              <div className="feature">
                <h3>📝 Markdown Support</h3>
                <p>All documents support rich markdown formatting for better readability.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
ReactDOM.createRoot(document.getElementById('app')).render(<App />);
