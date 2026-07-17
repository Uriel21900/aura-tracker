import os

main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

with open(main_py_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the DUPE_MAPPING section
import re

new_dupe_logic = """from duckduckgo_search import DDGS

# Two-way smart mappings
CLONE_TO_ORIGINAL = {
    "Club De Nuit Intense": "Dupe of Creed Aventus",
    "Club De Nuit Sillage": "Dupe of Creed Silver Mountain Water",
    "Club De Nuit Milestone": "Dupe of Creed Millésime Impérial",
    "Club De Nuit Untold": "Dupe of Baccarat Rouge 540",
    "Club De Nuit Iconic": "Dupe of Bleu de Chanel",
    "Game of Spades Rouge": "Dupe of Baccarat Rouge 540",
    "Zara Red Temptation": "Dupe of Baccarat Rouge 540",
    "Amber Oud Gold Edition": "Dupe of Xerjoff Erba Pura",
    "Khamrah": "Dupe of Kilian Angels' Share",
    "Asad": "Dupe of Dior Sauvage Elixir",
    "Supremacy Not Only Intense": "Dupe of Nishane Hacivat",
    "Fakhar Black": "Dupe of YSL Y EDP",
    "Hawas": "Dupe of Paco Rabanne Invictus Aqua",
    "9pm": "Dupe of JPG Ultra Male",
    "9 PM Night Out": "Dupe of JPG Ultra Male",
    "Craze": "Dupe of Parfums de Marly Pegasus",
    "Amber Oud Tobacco Edition": "Dupe of Tom Ford Tobacco Vanille",
    "Woody Oud": "Dupe of Tom Ford Oud Wood",
    "Toscano Leather": "Dupe of Tom Ford Tuscan Leather",
    "Porto Neroli": "Dupe of Tom Ford Neroli Portofino",
    "Bright Peach": "Dupe of Tom Ford Bitter Peach",
    "Fabulo Intense": "Dupe of Tom Ford Fucking Fabulous",
    "Liam Grey": "Dupe of BDK Gris Charnel",
    "Kismet Angel": "Dupe of Kilian Angels' Share",
    "Jean Lowe Immortal": "Dupe of Louis Vuitton L'Immensité",
    "Jean Lowe Ombre": "Dupe of Louis Vuitton Ombre Nomade",
    "Salvo Intense": "Dupe of Dior Sauvage EDP",
    "Turathi Blue": "Dupe of Bvlgari Tygar",
    "Al Qiam Silver": "Dupe of Bvlgari Tygar",
    "Historic Olmeda": "Dupe of Bleu de Chanel",
    "Supremacy Collector's Edition Pour Homme": "Dupe of Creed Aventus",
    "Ruthless Vanilla": "Dupe of YSL Babycat",
    "Vault Men": "Dupe of Armani Code Profumo",
    "Victorioso Victory": "Dupe of Paco Rabanne Invictus Victory",
    "376 (Imagination)": "Dupe of Louis Vuitton Imagination",
    "358 (Meteore)": "Dupe of Louis Vuitton Météore",
    "737 (Sicily)": "Dupe of Mancera Sicily",
    "677 (Afternoon Swim)": "Dupe of Louis Vuitton Afternoon Swim",
}

ORIGINAL_TO_CLONES = {
    "Baccarat Rouge 540": "Known Dupes: CDN Untold, Game of Spades Rouge, Zara Red Temptation, Al Haramain Amber Oud Ruby",
    "Creed Aventus": "Known Dupes: CDNIM, Supremacy NOI, Montblanc Explorer, L'Aventure",
    "Bleu de Chanel": "Known Dupes: CDN Iconic, Historic Olmeda, Missoni Parfum Pour Homme",
    "Dior Sauvage": "Known Dupes: Afnan Modest Une, Prada Luna Rossa Carbon, Ventana",
    "Dior Sauvage Elixir": "Known Dupes: Lattafa Asad, Salvo Elixir",
    "Kilian Angels' Share": "Known Dupes: Lattafa Khamrah, Kismet Angel, Sharaf Blend",
    "Tom Ford Tobacco Vanille": "Known Dupes: Amber Oud Tobacco Edition, Charuto Tobacco Vanille",
    "Tom Ford Oud Wood": "Known Dupes: Maison Alhambra Woody Oud",
    "Tom Ford Lost Cherry": "Known Dupes: Maison Alhambra Lovely Cherie",
    "YSL Y EDP": "Known Dupes: Lattafa Fakhar Black, Sheikh Shuyukh Final Edition",
    "Parfums de Marly Layton": "Known Dupes: Detour Noir, Lalique White in Black",
    "Parfums de Marly Pegasus": "Known Dupes: Armaf Craze",
    "Creed Silver Mountain Water": "Known Dupes: CDN Sillage, Afnan Supremacy In Heaven",
    "Creed Millésime Impérial": "Known Dupes: CDN Milestone, Sean John Unforgivable",
    "Xerjoff Erba Pura": "Known Dupes: Amber Oud Gold Edition, Ana Abiyedh White",
    "Bvlgari Tygar": "Known Dupes: Afnan Turathi Blue, Lattafa Al Qiam Silver",
    "Louis Vuitton Imagination": "Known Dupes: Zara Sunrise on the Red Sand Dunes",
    "Louis Vuitton L'Immensité": "Known Dupes: Jean Lowe Immortal",
    "Louis Vuitton Ombre Nomade": "Known Dupes: Jean Lowe Ombre",
    "JPG Ultra Male": "Known Dupes: Afnan 9pm",
    "Invictus Aqua": "Known Dupes: Rasasi Hawas, Montblanc Legend Spirit",
    "BDK Gris Charnel": "Known Dupes: Lattafa Liam Grey, Francique 63.55",
}

def check_smart_dupe(name):
    for clone, orig in CLONE_TO_ORIGINAL.items():
        if clone.lower() in name.lower() or name.lower() in clone.lower():
            return orig
    for orig, clones in ORIGINAL_TO_CLONES.items():
        if orig.lower() in name.lower() or name.lower() in orig.lower():
            return clones
    return ""

app = FastAPI()"""

# Replace DUPE_MAPPING up to app = FastAPI()
content = re.sub(r'# Known dupe mappings.*?\napp = FastAPI\(\)', new_dupe_logic, content, flags=re.DOTALL)

# Replace the inner loop logic
old_inner = """                        # Try to auto-populate from known dupes
                        auto_inspiration = ""
                        for known_name, known_insp in DUPE_MAPPING.items():
                            if known_name.lower() == name.lower():
                                auto_inspiration = known_insp
                                break"""

new_inner = """                        # Use Smart Dupe Engine
                        auto_inspiration = check_smart_dupe(name)"""

content = content.replace(old_inner, new_inner)

# Add the new endpoint
new_endpoint = """
@app.get("/api/search-dupe-online")
def search_dupe_online(name: str):
    try:
        results = DDGS().text(f'"{name}" perfume clone of OR dupe of', max_results=3)
        if not results:
            return {"inspiration": f"No online matches found."}
            
        snippets = " ".join([r['body'] for r in results]).lower()
        brands = ["Creed Aventus", "Baccarat Rouge 540", "Bleu de Chanel", "Dior Sauvage", "Tom Ford", "YSL", "Parfums de Marly", "Kilian", "Louis Vuitton", "Mancera", "Montale", "Roja", "Xerjoff", "Initio", "Nishane", "JPG Ultra Male", "Invictus"]
        
        found = []
        for b in brands:
            if b.lower() in snippets:
                found.append(b)
                
        if found:
            return {"inspiration": f"Online: Dupe of {', '.join(set(found))}"}
        else:
            return {"inspiration": "Online: Possible clone, but exact designer not detected."}
    except Exception as e:
        return {"inspiration": f"Error: {str(e)}"}
"""

content += new_endpoint

with open(main_py_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected Smart Dupe Engine into main.py!")
