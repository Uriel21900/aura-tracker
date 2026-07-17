import React, { useState, useEffect } from 'react';
import { Search, Star, Clock, Wind, DollarSign, Plus, Database, LayoutDashboard } from 'lucide-react';
import './App.css';

function App() {
  const [collection, setCollection] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [clonesDb, setClonesDb] = useState([]);

  useEffect(() => {
    fetchCollection();
    fetchClonesDb();
  }, []);

  const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;

  const fetchCollection = async () => {
    try {
      const res = await fetch(`${API_URL}/api/collection`);
      const data = await res.json();
      setCollection(data);
    } catch (err) {
      console.error("Error fetching collection", err);
    }
  };

  const fetchClonesDb = async () => {
    try {
      const res = await fetch(`${API_URL}/api/dupes`);
      const data = await res.json();
      setClonesDb(data.dupes || []);
    } catch (err) {
      console.error("Error fetching dupes", err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery) return;
    setIsSearching(true);
    try {
      const res = await fetch(`${API_URL}/api/search?query=${searchQuery}`);
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch (err) {
      console.error("Search error", err);
    }
    setIsSearching(false);
  };

  const addFragrance = async (fragrance) => {
    try {
      await fetch(`${API_URL}/api/collection`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          brand: fragrance.brand || "Unknown",
          name: fragrance.name,
          season: fragrance.season || "All Season",
          rating: fragrance.rating || "8.0",
          longevity: fragrance.longevity || "Moderate",
          projection: fragrance.projection || "Moderate",
          price_tier: fragrance.price_tier || "Budget",
          inspiration: fragrance.inspiration || "Original"
        })
      });
      fetchCollection();
      setSearchResults([]);
      setSearchQuery('');
      setActiveTab('dashboard');
    } catch (err) {
      console.error("Add error", err);
    }
  };

  const addFromCloneDb = (cloneObj) => {
    addFragrance({
      name: cloneObj.clone,
      inspiration: `Dupe of ${cloneObj.original}`
    });
  };

  return (
    <div className="app-container">
      <header className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <h1 className="title">Aura Tracker</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            className={`btn-secondary ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
            style={{ padding: '0.5rem 1rem', display: 'flex', gap: '0.5rem', alignItems: 'center', border: activeTab === 'dashboard' ? '1px solid #a78bfa' : '' }}
          >
            <LayoutDashboard size={18} /> Dashboard
          </button>
          <button 
            className={`btn-secondary ${activeTab === 'clones' ? 'active' : ''}`}
            onClick={() => setActiveTab('clones')}
            style={{ padding: '0.5rem 1rem', display: 'flex', gap: '0.5rem', alignItems: 'center', border: activeTab === 'clones' ? '1px solid #a78bfa' : '' }}
          >
            <Database size={18} /> Clones Database
          </button>
        </div>
      </header>

      <main className="main-content">
        {activeTab === 'dashboard' ? (
          <>
            <section className="glass-panel search-section">
              <div className="gradient-bar"></div>
              <h2 className="section-title">
                <Search className="icon-purple" /> Discover New Fragrances
              </h2>
              <form onSubmit={handleSearch} className="search-form">
                <input 
                  type="text" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search millions of fragrances..." 
                  className="search-input"
                />
                <button type="submit" className="btn-primary">
                  {isSearching ? 'Searching...' : 'Search'}
                </button>
              </form>

              {searchResults.length > 0 && (
                <div className="search-results">
                  {searchResults.map((res, i) => (
                    <div key={i} className="result-card">
                      <h3 className="result-name">{res.name}</h3>
                      <p className="result-brand">{res.brand}</p>
                      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
                        <input 
                          type="text" 
                          placeholder="Inspiration / Dupe of..." 
                          className="search-input"
                          style={{ flex: 1, padding: '0.75rem', fontSize: '0.9rem' }}
                          value={res.inspiration || ""}
                          onChange={(e) => {
                            const newResults = [...searchResults];
                            newResults[i].inspiration = e.target.value;
                            setSearchResults(newResults);
                          }}
                        />
                        <button 
                          className="btn-secondary" 
                          style={{ padding: '0.75rem' }}
                          onClick={async () => {
                            const newResults = [...searchResults];
                            newResults[i].inspiration = "Searching online...";
                            setSearchResults(newResults);
                            try {
                              const ddgRes = await fetch(`${API_URL}/api/search-dupe-online?name=${encodeURIComponent(res.name)}`);
                              const data = await ddgRes.json();
                              const finalResults = [...searchResults];
                              finalResults[i].inspiration = data.inspiration;
                              setSearchResults(finalResults);
                            } catch (e) {
                              const finalResults = [...searchResults];
                              finalResults[i].inspiration = "Failed to search online";
                              setSearchResults(finalResults);
                            }
                          }}
                          title="Search the live internet for dupes"
                        >
                          🌐 Search
                        </button>
                      </div>
                      <button onClick={() => addFragrance(res)} className="btn-secondary">
                        <Plus size={18} /> Add to Collection
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section className="collection-section">
              <h2 className="section-title-large">My Collection</h2>
              <div className="collection-grid">
                {collection.map((item) => (
                  <div key={item.id} className="glass-panel card">
                    <div className="card-header">
                      <div>
                        <h3 className="card-name">{item.name}</h3>
                        <p className="card-brand">{item.brand}</p>
                      </div>
                      <span className="badge">{item.season}</span>
                    </div>
                    
                    <div className="card-stats">
                      <div className="stat"><Star size={16} className="icon-yellow"/> {item.rating}/10</div>
                      <div className="stat"><Clock size={16} className="icon-blue"/> {item.longevity}</div>
                      <div className="stat"><Wind size={16} className="icon-green"/> {item.projection}</div>
                      <div className="stat"><DollarSign size={16} className="icon-emerald"/> {item.price_tier}</div>
                    </div>

                    <div className="card-footer">
                      <p className="inspiration">
                        <span>Inspiration:</span> {item.inspiration}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        ) : (
          <section className="glass-panel">
            <div className="gradient-bar"></div>
            <h2 className="section-title">
              <Database className="icon-purple" /> Clones Database
            </h2>
            <p style={{ color: '#8b949e', marginBottom: '2rem' }}>
              Browse our massive built-in dictionary of known clones and instantly add them to your collection!
            </p>
            
            <div className="collection-grid">
              {clonesDb.map((item, idx) => (
                <div key={idx} className="glass-panel card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '150px' }}>
                  <div>
                    <h3 className="card-name" style={{ color: '#e2e8f0', fontSize: '1.2rem', marginBottom: '0.5rem' }}>{item.clone}</h3>
                    <p className="inspiration" style={{ fontSize: '0.95rem' }}>
                      <span style={{ color: '#a78bfa' }}>Dupe of:</span> {item.original}
                    </p>
                  </div>
                  <button onClick={() => addFromCloneDb(item)} className="btn-secondary" style={{ width: '100%', marginTop: '1.5rem' }}>
                    <Plus size={18} /> Add to Collection
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
