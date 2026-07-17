import os
import urllib.request

# This points to a massive open-source dataset of fragrances from Parfumo
DATASET_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2024/2024-12-10/parfumo_data_clean.csv"
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "legacy_scripts", "dataset")

def download_dataset():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        
    file_path = os.path.join(DATASET_DIR, "fragrances.csv")
    print("Downloading massive public fragrance dataset (no API keys required)...")
    
    try:
        urllib.request.urlretrieve(DATASET_URL, file_path)
        print(f"Dataset successfully downloaded! You can now search for millions of fragrances in the app.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_dataset()
