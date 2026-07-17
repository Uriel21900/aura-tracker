import React, { useState, useEffect } from 'react';
import { Search, Star, Clock, Wind, DollarSign, Plus } from 'lucide-react';
import './App.css';

function App() {
  const [collection, setCollection] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    fetchCollection();
  }, []);

  const fetchCollection = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/collection');
      const data = await res.json();
      setCollection(data);
    } catch (err) {
      console.error("Error fetching collection", err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery) return;
    setIsSearching(true);
    try {
      const res = await fetch(`http://localhost:8000/api/search?query=${searchQuery}`);
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch (err) {
      console.error("Search error", err);
    }
    setIsSearching(false);
  };

  const addFragrance = async (fragrance) => {
    try {
      await fetch('http://localhost:8000/api/collection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          brand: fragrance.brand,
          name: fragrance.name,
          season: fragrance.season,
          rating: fragrance.rating,
          longevity: fragrance.longevity,
          projection: fragrance.projection,
          price_tier: fragrance.price_tier,
          inspiration: "Original"
        })
      });
      fetchCollection();
      setSearchResults([]);
      setSearchQuery('');
    } catch (err) {
      console.error("Add error", err);
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">Aura Tracker</h1>
      </header>

      <main className="main-content">
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
      </main>
    </div>
  );
}

export default App;
