#this script is to transform the raw data into meaningful data

import json
import pandas as pd

RAW_PATH = "data/raw/steam_raw.json"
PROCESSED_PATH = "data/processed/steam_processed.csv"

def load_raw_data():
    with open(RAW_PATH,'r') as f:
        raw_data = json.load(f)
        return raw_data 
    
def transform_data(data):
        featured = data.get('data', {}).get('featured_win', {})
        games = []
        for item in featured.get("items", []):
            games.append({
                "game_id": item.get("id"),
                "name": item.get("name"),
                "price": item.get("final_price"),
                "discount": item.get("discount_percent"),
                "platform": "steam",
                "fetched_at": data["fetched_at"],
            })
        return pd.DataFrame(games)
        


def t_main():
        raw = load_raw_data()
        df = transform_data(raw)
        print(df.head())
        df.to_csv(PROCESSED_PATH, index=False)

        
if __name__ == "__main__":
    t_main()
    print("Data has been transformed and saved successfully.")