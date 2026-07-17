from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import csv
import glob

app = FastAPI()

# Allow CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collection.db")
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "legacy_scripts", "dataset")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            name TEXT,
            season TEXT,
            strength TEXT,
            rating TEXT,
            longevity TEXT,
            projection TEXT,
            price_tier TEXT,
            inspiration TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Fragrance(BaseModel):
    brand: str
    name: str
    season: str = "All Season"
    strength: str = "Moderate"
    rating: str = "8.0"
    longevity: str = "Moderate"
    projection: str = "Moderate"
    price_tier: str = "Budget"
    inspiration: str = "Original"

@app.get("/api/collection")
def get_collection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection ORDER BY brand, name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(ix) for ix in rows]

@app.post("/api/collection")
def add_to_collection(f: Fragrance):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO collection (brand, name, season, strength, rating, longevity, projection, price_tier, inspiration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (f.brand, f.name, f.season, f.strength, f.rating, f.longevity, f.projection, f.price_tier, f.inspiration))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/api/search")
def search_dataset(query: str):
    # This reads the kaggle dataset to find matches
    results = []
    if not os.path.exists(DATASET_PATH):
        return {"error": "Dataset folder not found. Please run update_database.py first.", "results": []}
        
    csv_files = glob.glob(os.path.join(DATASET_PATH, "*.csv"))
    if not csv_files:
        return {"error": "No CSV files found in dataset.", "results": []}
        
    try:
        with open(csv_files[0], mode='r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                brand_col = next((c for c in row.keys() if c and 'brand' in c.lower()), None)
                name_col = next((c for c in row.keys() if c and ('name' in c.lower() or 'perfume' in c.lower())), None)
                
                if brand_col and name_col:
                    brand = str(row[brand_col])
                    name = str(row[name_col])
                    
                    if query.lower() in brand.lower() or query.lower() in name.lower():
                        results.append({
                            "brand": brand,
                            "name": name,
                            "season": row.get('Season', row.get('season', "All Season")),
                            "rating": row.get('Rating', row.get('rating', "8.0")),
                            "longevity": row.get('Longevity', row.get('longevity', "Moderate")),
                            "projection": row.get('Sillage', row.get('sillage', "Moderate")),
                            "price_tier": row.get('Price', row.get('price', "Budget"))
                        })
                        count += 1
                        if count > 20: # Limit to 20 results for speed
                            break
    except Exception as e:
        return {"error": str(e), "results": []}
        
    return {"results": results}
