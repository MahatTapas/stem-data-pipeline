import json
import pandas as pd
import os

# 1. SETUP PATHS (Absolute paths to prevent Airflow discovery errors)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data/raw/steam_raw.json")
PROCESSED_PATH = os.path.join(BASE_DIR, "data/processed/steam_processed.csv")

def load_raw_data():
    """Load JSON data from the raw storage file."""
    if not os.path.exists(RAW_PATH):
        print(f"Error: Raw file not found at {RAW_PATH}")
        return None
        
    with open(RAW_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error: Could not decode JSON. The file might be corrupted.")
            return None

def transform_data(data):
    """Extract game info from 'specials', 'top_sellers', and numeric keys."""
    if not data or 'data' not in data:
        return pd.DataFrame()

    inner_data = data.get('data', {})
    
    # These are the keys we confirmed exist in your specific JSON
    categories = ['specials', 'top_sellers', 'new_releases', 'coming_soon']
    
    # We also saw numeric keys ('0', '1', etc.) in your 'Inside Data' list. 
    # Let's add those just in case they contain more games.
    numeric_keys = [str(i) for i in range(10)] 
    all_target_keys = categories + numeric_keys
    
    games = []
    
    for key in all_target_keys:
        # Check if the key exists and has an 'items' list
        category_block = inner_data.get(key, {})
        if isinstance(category_block, dict):
            items = category_block.get("items", [])
            
            for item in items:
                games.append({
                    "game_id": item.get("id"),
                    "name": item.get("name"),
                    "price": item.get("final_price"),
                    "discount": item.get("discount_percent"),
                    "platform": "steam",
                    "source_category": key,
                    "fetched_at": data.get("fetched_at"),
                })
            
    df = pd.DataFrame(games)
    
    # Cleanup: Remove duplicates if a game appeared in multiple categories
    if not df.empty:
        return df.drop_duplicates(subset=['game_id'])
    return df

def t_main():
    """Main execution logic for the transformation step."""
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    
    raw_data = load_raw_data()
    if raw_data is None:
        return

    df = transform_data(raw_data)
    
    if not df.empty:
        print(f"--- SUCCESS: Found {len(df)} games ---")
        print(df[['name', 'price', 'source_category']].head())
        
        df.to_csv(PROCESSED_PATH, index=False)
        print(f"Data saved to: {PROCESSED_PATH}")
    else:
        print("Warning: No games were extracted. Check if the raw JSON has 'items' lists.")

if __name__ == "__main__":
    t_main()
