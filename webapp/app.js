const App = () => {
  const [docs, setDocs] = React.useState([]); // {path, title, content}
  const [currentDoc, setCurrentDoc] = React.useState(null);
  const [searchResults, setSearchResults] = React.useState([]);
  const searchIndexRef = React.useRef(null);

  React.useEffect(() => {
    fetch('file_list.json')
      .then(res => res.json())
      .then(paths => loadDocs(paths));
  }, []);

  const loadDocs = async (paths) => {
    const loaded = [];
    for (const p of paths) {
      const res = await fetch('../' + p);
      const text = await res.text();
      const title = p.split('/').pop();
      loaded.push({ path: p, title, content: text });
    }
    setDocs(loaded);
    buildIndex(loaded);
  };

  const buildIndex = (docs) => {
    const idx = lunr(function () {
      this.ref('path');
      this.field('title');
      this.field('content');
      docs.forEach(d => this.add(d));
    });
    searchIndexRef.current = idx;
  };

  const handleSearch = (e) => {
    const query = e.target.value;
    if (!query) {
      setSearchResults([]);
      return;
    }
    const res = searchIndexRef.current.search(query);
    const mapped = res.map(r => docs.find(d => d.path === r.ref));
    setSearchResults(mapped);
  };

  const renderDocList = () => (
    <ul>
      {docs.map(doc => (
        <li key={doc.path} className="link" onClick={() => setCurrentDoc(doc)}>
          {doc.title}
        </li>
      ))}
    </ul>
  );

  const renderSearchResults = () => (
    searchResults.length > 0 && (
      <ul>
        {searchResults.map(doc => (
          <li key={doc.path} className="link" onClick={() => setCurrentDoc(doc)}>
            {doc.title}
          </li>
        ))}
      </ul>
    )
  );

  return (
    <div style={{display:'flex', width:'100%'}}>
      <div id="sidebar">
        <input className="search-input" type="text" placeholder="Search" onChange={handleSearch} />
        {renderSearchResults()}
        {renderDocList()}
      </div>
      <div id="content">
        {currentDoc ? (
          <div dangerouslySetInnerHTML={{ __html: marked.parse(currentDoc.content) }} />
        ) : (
          <h1>Select a document</h1>
        )}
      </div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('app')).render(<App />);
