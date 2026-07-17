import os
import subprocess
import zipfile
import glob
import sys

def ensure_kaggle_installed():
    try:
        import kaggle
    except ImportError:
        print("Kaggle library not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        print("Please run the script again after installation finishes.")
        sys.exit(0)

def main():
    ensure_kaggle_installed()
    from kaggle.api.kaggle_api_extended import KaggleApi

    # If you find a better dataset on Kaggle, you can change this slug.
    # Example: 'nandhini34/fragrantica-dataset' or 'someone/perfumes'
    DATASET_SLUG = "nandhini34/fragrantica-dataset" 
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(current_dir, "dataset")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print(f"Connecting to Kaggle to download {DATASET_SLUG}...")
    try:
        api = KaggleApi()
        api.authenticate()
        
        print("Downloading dataset...")
        api.dataset_download_files(DATASET_SLUG, path=download_path, unzip=True)
        
        csv_files = glob.glob(os.path.join(download_path, "*.csv"))
        if csv_files:
            print("Successfully downloaded and updated the following database files:")
            for f in csv_files:
                print(f" - {os.path.basename(f)}")
        else:
            print("Download completed but no CSV files were found.")
            
    except Exception as e:
        print("\n--- ERROR ---")
        print("Could not connect to Kaggle.")
        print(f"Details: {e}")
        print("\nMake sure you have placed your 'kaggle.json' file in the correct location:")
        print(" - On Windows: C:\\Users\\<YourUsername>\\.kaggle\\kaggle.json")
        print(" - On Mac/Linux: ~/.kaggle/kaggle.json")

if __name__ == "__main__":
    main()
