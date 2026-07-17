from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import csv
import glob

# Known dupe mappings for auto-population
DUPE_MAPPING = {
    "9 PM Night Out": "Dupe of JPG Ultra Male",
    "9pm": "Dupe of JPG Ultra Male",
    "Historic Olmeda": "Dupe of Bleu de Chanel",
    "Supremacy Collector's Edition Pour Homme": "Dupe of Creed Aventus",
    "Supremacy Not Only Intense": "Dupe of Nishane Hacivat / Aventus",
    "Ruthless Vanilla": "Dupe of YSL Babycat / Vanilla",
    "Vault Men": "Dupe of Armani Code Profumo",
    "Victorioso Victory": "Dupe of Paco Rabanne Invictus Victory",
    "376 (Imagination)": "Dupe of Louis Vuitton Imagination",
    "358 (Meteore)": "Dupe of Louis Vuitton Météore",
    "737 (Sicily)": "Dupe of Mancera Sicily",
    "677 (Afternoon Swim)": "Dupe of Louis Vuitton Afternoon Swim",
    "230 (One Million Prive)": "Dupe of Paco Rabanne 1 Million Privé",
    "240 (Wanted)": "Dupe of Azzaro Wanted",
    "330 (Red Tabacco)": "Dupe of Mancera Red Tobacco",
    "Magnetic Scent For Him": "Dupe of Escada Magnetism for Men",
    "Prada Luna Rossa Ocean": "Dupe of Prada Luna Rossa Ocean",
    "Imperialism": "Dupe of Creed Millésime Impérial",
    "Warrior": "Dupe of Creed Viking",
    "Secret Garden": "Dupe of Tom Ford Noir de Noir",
    "Tuxedo": "Dupe of YSL Tuxedo",
    "Adventure": "Dupe of Creed Aventus",
    "Craze": "Dupe of Parfums de Marly Pegasus",
    "Dynasty": "Dupe of PDM Haltane / Oud for Greatness",
    "Tresador Mystique": "Dupe of Lancome Tresor Midnight Rose",
    "Rifaaqat": "Dupe of YSL Babycat",
    "Milano Privé": "Dupe of Paco Rabanne 1 Million Privé",
    "Furtune Lucky Man": "Dupe of Paco Rabanne 1 Million Lucky",
    "Mashair Indigo": "Dupe of Dior Sauvage",
    "Royal Noir Absolu": "Dupe of Tom Ford Noir Extreme",
    "F Le Parfum": "Dupe of YSL Y Le Parfum",
    "Factory Campfire": "Dupe of Maison Margiela By the Fireplace",
    "Apple Orchard": "Dupe of Kilian Apple Brandy",
    "Citrus Ginger": "Dupe of Bleu de Chanel",
    "9th Avenue New York": "Dupe of Bond No 9",
    "Bamboo Reflection": "Dupe of Amouage Reflection Man",
    "You Are My Fire Rouge": "Dupe of MFK Baccarat Rouge 540",
    "Dunescape": "Dupe of Maison Margiela Beach Walk",
    "Kaaf Noir": "Dupe of Abercrombie & Fitch Fierce",
    "Tres Nuit Lyric": "Dupe of Armani Acqua di Gio Profondo",
    "Tres Nuit": "Dupe of Creed Green Irish Tweed",
    "Summer Swim": "Dupe of Louis Vuitton Afternoon Swim",
    "MegaMarine": "Dupe of Orto Parisi Megamare",
    "Symphony 33": "Dupe of Le Labo Santal 33",
    "The Pride Of Armaf": "Dupe of Dior Sauvage",
    "Shades Blue": "Dupe of Bleu de Chanel",
    "Z25": "Dupe of Le Labo Tonka 25",
    "Legend Pour Homme": "Dupe of Montblanc Legend",
    "Mocha Wood": "Dupe of Franck Boclet Tobacco",
    "Red Cherry": "Dupe of Tom Ford Lost Cherry",
    "Al Raiee": "Dupe of D&G The One Luminous Night",
    "Calabria Cerulean": "Dupe of Acqua di Parma Mirto di Panarea",
    "Club De Nuit Intense Edt": "Dupe of Creed Aventus",
    "Club De Nuit Intense Edp": "Dupe of Creed Aventus",
    "Club De Nuit Limited Edition Parfum": "Dupe of Creed Aventus",
    "Club De Nuit Urban Man Elixir": "Dupe of Dior Sauvage / Aventus",
    "Club De Nuit Sillage": "Dupe of Creed Silver Mountain Water",
    "Club De Nuit Milestone": "Dupe of Creed Millésime Impérial",
    "Club De Nuit Precieux": "Dupe of Creed Aventus Absolu",
}

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
                        # Try to auto-populate from known dupes
                        auto_inspiration = ""
                        for known_name, known_insp in DUPE_MAPPING.items():
                            if known_name.lower() == name.lower():
                                auto_inspiration = known_insp
                                break
                                
                        results.append({
                            "brand": brand,
                            "name": name,
                            "season": row.get('Season', row.get('season', "All Season")),
                            "rating": row.get('Rating', row.get('rating', "8.0")),
                            "longevity": row.get('Longevity', row.get('longevity', "Moderate")),
                            "projection": row.get('Sillage', row.get('sillage', "Moderate")),
                            "price_tier": row.get('Price', row.get('price', "Budget")),
                            "inspiration": auto_inspiration
                        })
                        count += 1
                        if count > 20: # Limit to 20 results for speed
                            break
    except Exception as e:
        return {"error": str(e), "results": []}
        
    return {"results": results}
