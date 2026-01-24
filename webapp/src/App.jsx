import React from "react";
import ReactDOM from "react-dom/client";
import html2pdf from "html2pdf.js";

const App = () => {
  const [docs, setDocs] = React.useState([]);
  const [currentDoc, setCurrentDoc] = React.useState(null);
  const [searchResults, setSearchResults] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [isExporting, setIsExporting] = React.useState(false);
  const [fillMode, setFillMode] = React.useState(false);
  const [fieldValues, setFieldValues] = React.useState({});
  const [savedDrafts, setSavedDrafts] = React.useState({});
  const searchIndexRef = React.useRef(null);
  const contentRef = React.useRef(null);

  // Placeholder patterns to detect in templates
  const PLACEHOLDER_PATTERNS = [
    /\[Your Company\]/g,
    /\[Your Company's\]/g,
    /\[Company Name\]/g,
    /\[Partner Name\]/g,
    /\[Partner Company\]/g,
    /\[Product Name\]/g,
    /\[Product\/Solution\]/g,
    /\[Date\]/g,
    /\[Target Market\]/g,
    /\[Industry\]/g,
    /\[Region\]/g,
    /\[Contact Name\]/g,
    /\[Email\]/g,
    /\[Phone\]/g,
    /\[Revenue Target\]/g,
    /\[Partner Manager\]/g,
    /\[Fiscal Year\]/g,
    /\$X+K?M?/g,
    /X%/g,
    /\[insert [^\]]+\]/gi,
    /\[add [^\]]+\]/gi,
    /\[specify [^\]]+\]/gi,
  ];

  // Extract unique placeholders from content
  const extractPlaceholders = (content) => {
    if (!content) return [];
    const found = new Set();

    PLACEHOLDER_PATTERNS.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        matches.forEach(match => found.add(match));
      }
    });

    return Array.from(found).sort();
  };

  // Load saved drafts from localStorage on mount
  React.useEffect(() => {
    try {
      const saved = localStorage.getItem('partnerOS_drafts');
      if (saved) {
        setSavedDrafts(JSON.parse(saved));
      }
    } catch (err) {
      console.error('Error loading saved drafts:', err);
    }
  }, []);

  // Load field values when document changes
  React.useEffect(() => {
    if (currentDoc && savedDrafts[currentDoc.path]) {
      setFieldValues(savedDrafts[currentDoc.path]);
    } else {
      setFieldValues({});
    }
    setFillMode(false);
  }, [currentDoc, savedDrafts]);

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

  const handleExportPDF = async () => {
    if (!currentDoc || !contentRef.current) return;

    setIsExporting(true);

    try {
      const element = contentRef.current;
      const filename = `${currentDoc.title.replace(/[^a-z0-9]/gi, '_')}.pdf`;

      const opt = {
        margin: [0.75, 0.75, 0.75, 0.75],
        filename: filename,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
      };

      await html2pdf().set(opt).from(element).save();
    } catch (err) {
      console.error('Error exporting PDF:', err);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  // Handle field value changes
  const handleFieldChange = (placeholder, value) => {
    setFieldValues(prev => ({
      ...prev,
      [placeholder]: value
    }));
  };

  // Save draft to localStorage
  const saveDraft = () => {
    if (!currentDoc) return;

    const newDrafts = {
      ...savedDrafts,
      [currentDoc.path]: fieldValues
    };

    try {
      localStorage.setItem('partnerOS_drafts', JSON.stringify(newDrafts));
      setSavedDrafts(newDrafts);
      alert('Draft saved successfully!');
    } catch (err) {
      console.error('Error saving draft:', err);
      alert('Failed to save draft. Please try again.');
    }
  };

  // Clear draft for current document
  const clearDraft = () => {
    if (!currentDoc) return;

    if (!confirm('Are you sure you want to clear this draft?')) return;

    const newDrafts = { ...savedDrafts };
    delete newDrafts[currentDoc.path];

    try {
      localStorage.setItem('partnerOS_drafts', JSON.stringify(newDrafts));
      setSavedDrafts(newDrafts);
      setFieldValues({});
    } catch (err) {
      console.error('Error clearing draft:', err);
    }
  };

  // Apply field values to content
  const applyFieldValues = (content) => {
    if (!content || Object.keys(fieldValues).length === 0) return content;

    let result = content;
    Object.entries(fieldValues).forEach(([placeholder, value]) => {
      if (value) {
        // Escape special regex characters in placeholder
        const escaped = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(escaped, 'g');
        result = result.replace(regex, value);
      }
    });

    return result;
  };

  // Check if current document has a saved draft
  const hasSavedDraft = currentDoc && savedDrafts[currentDoc.path] &&
    Object.keys(savedDrafts[currentDoc.path]).length > 0;

  // Get placeholders for current document
  const currentPlaceholders = currentDoc ? extractPlaceholders(currentDoc.content) : [];

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

  const renderMarkdown = (content, applyValues = false) => {
    console.log('renderMarkdown called with content (first 100 chars):', content ? content.substring(0, 100) : 'null');
    if (!content) return null;

    try {
      // Apply field values if requested
      const processedContent = applyValues ? applyFieldValues(content) : content;

      // Use marked to convert markdown to HTML
      let html = marked.parse(processedContent);

      // Highlight unfilled placeholders when in fill mode
      if (fillMode && !applyValues) {
        currentPlaceholders.forEach(placeholder => {
          if (!fieldValues[placeholder]) {
            const escaped = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(escaped, 'g');
            html = html.replace(regex, `<span class="unfilled-placeholder">${placeholder}</span>`);
          }
        });
      }

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

    const placeholders = extractPlaceholders(doc.content);
    const hasPlaceholders = placeholders.length > 0;
    const filledCount = Object.values(fieldValues).filter(v => v).length;

    return (
      <div className="doc-content">
        <div className="doc-header">
          <h1>{doc.title}</h1>
          <div className="export-buttons">
            {hasPlaceholders && (
              <button
                onClick={() => setFillMode(!fillMode)}
                className={`export-btn ${fillMode ? 'fill-active' : ''}`}
                title={fillMode ? 'View template' : 'Fill template'}
              >
                {fillMode ? 'View Mode' : 'Fill Template'}
              </button>
            )}
            <button
              onClick={handleExportPDF}
              disabled={isExporting}
              className="export-btn"
              title="Download as PDF"
            >
              {isExporting ? 'Exporting...' : 'Export PDF'}
            </button>
            <button
              onClick={handlePrint}
              className="export-btn print-btn"
              title="Print document"
            >
              Print
            </button>
          </div>
        </div>

        {fillMode && hasPlaceholders && (
          <div className="fill-panel">
            <div className="fill-panel-header">
              <h3>Fill Template Fields</h3>
              <span className="fill-progress">
                {filledCount} / {placeholders.length} filled
              </span>
            </div>
            <p className="fill-instructions">
              Enter values for each placeholder. Your changes are highlighted in the preview below.
            </p>
            <div className="fill-fields">
              {placeholders.map(placeholder => (
                <div key={placeholder} className="fill-field">
                  <label>{placeholder}</label>
                  <input
                    type="text"
                    value={fieldValues[placeholder] || ''}
                    onChange={(e) => handleFieldChange(placeholder, e.target.value)}
                    placeholder={`Enter value for ${placeholder}`}
                  />
                </div>
              ))}
            </div>
            <div className="fill-actions">
              <button onClick={saveDraft} className="fill-btn save-btn">
                Save Draft
              </button>
              {hasSavedDraft && (
                <button onClick={clearDraft} className="fill-btn clear-btn">
                  Clear Draft
                </button>
              )}
            </div>
          </div>
        )}

        <div ref={contentRef} className="doc-body">
          {renderMarkdown(doc.content, fillMode && filledCount > 0)}
        </div>
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