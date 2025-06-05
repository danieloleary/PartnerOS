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
      // ONLY process files within the /partner_blueprint/ directory
      if (!p.startsWith('/partner_blueprint/')) {
        console.log(`Skipping non-blueprint file: ${p}`);
        continue;
      }

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

        // Clean up the raw text from potential leading HTML boilerplate
        const cleanHtmlRegex = /^\s*<!DOCTYPE html>.*?<html.*?<head>.*?<script.*?<\/script>.*?<\/head>.*?<body.*?\/?>/is;
        const cleanedText = text.replace(cleanHtmlRegex, '').trim();

        // --- Frontmatter Parsing ---
        let frontmatter = {};
        let markdownContent = cleanedText;
        const lines = cleanedText.split('\n');
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
        const description = frontmatter.description || cleanedText.split('\n\n')[0].replace(/^#+\s*/, '');
        
        const doc = { 
          path: documentPath, // Store the root-relative path
          title, // Use the original extracted title, now based on cleaned text
          content: markdownContent, // Store only the markdown content
          section, 
          description, // Use the original extracted description, now based on cleaned text
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
          ...doc,
          score: result.score
        };
      });
      
      setSearchResults(searchResultsWithData);
    } catch (err) {
      console.error('Search error:', err);
      setSearchResults([]);
    }
  };

  const renderDocList = () => {
    if (isLoading) {
      return <div className="loading">Loading documents...</div>;
    }

    return (
      <div className="doc-list">
        {Object.entries(sections).map(([key, section]) => {
          const sectionDocs = docs.filter(doc => doc.section === key);
          if (sectionDocs.length === 0) return null;

          return (
            <div key={key} className="section">
              <h2>{section.icon} {section.title}</h2>
              <p>{section.description}</p>
              <ul>
                {sectionDocs.map(doc => (
                  <li key={doc.path}>
                    <a
                      href="#"
                      onClick={(e) => {
                        e.preventDefault();
                        setCurrentDoc(doc);
                      }}
                    >
                      {doc.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    );
  };

  const renderSearchResults = () => {
    if (!searchQuery) return null;

    return (
      <div className="search-results">
        <h2>Search Results</h2>
        {searchResults.length === 0 ? (
          <p>No results found</p>
        ) : (
          <ul>
            {searchResults.map(result => (
              <li key={result.path}>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    setCurrentDoc(result);
                  }}
                >
                  {highlightText(result.title, searchQuery)}
                </a>
                <p>{highlightText(result.description, searchQuery)}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  };

  const renderMarkdown = (content) => {
    console.log('renderMarkdown called with content (first 100 chars):', content ? content.substring(0, 100) : 'null');
    if (!content) return null;

    try {
      // Use marked to convert markdown to HTML
      const html = marked.parse(content);
      
      // Sanitize the HTML to prevent XSS
      const sanitized = DOMPurify.sanitize(html);
      
      console.log('renderMarkdown successfully processed content.');

      return (
        <div 
          className="markdown-content"
          dangerouslySetInnerHTML={{ __html: sanitized }}
        />
      );
    } catch (err) {
      console.error('Error rendering markdown:', err);
      return null;
    }
  };

  const renderDocContent = (doc) => {
    console.log('renderDocContent called with doc:', doc);
    if (!doc) return null;

    return (
      <div className="doc-content">
        <h1>{doc.title}</h1>
        {renderMarkdown(doc.content)}
      </div>
    );
  };

  return (
    <div className="app">
      <header>
        <h1>Partner Ecosystem Blueprint</h1>
        <div className="search">
          <input
            type="text"
            placeholder="Search documentation..."
            value={searchQuery}
            onChange={handleSearch}
          />
        </div>
      </header>
      <main>
        <nav>
          {renderDocList()}
          {renderSearchResults()}
        </nav>
        <article>
          {renderDocContent(currentDoc)}
        </article>
      </main>
    </div>
  );
};

export default App; 