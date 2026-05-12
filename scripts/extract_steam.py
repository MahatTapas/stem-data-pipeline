#in this script we extract the api from twitter
import requests
import json
import os
from datetime import datetime, timezone, timedelta

URL="https://store.steampowered.com/api/featuredcategories/"
RAW_PATH = "data/raw/steam_raw.json"

def fetch_steam_data():
    response = requests.get(URL)
    response.raise_for_status() # instead of doint it manually where we do if response.status_code ==200 we use this, this automaticlly throws an exception and is much suitable for airflow, since the manual way executes either way the airflow takes it as it ran successfully but with this way it will fail if the status code is not 200
    return response.json()

def save_raw_data(data):
    os.makedirs("data/raw", exist_ok=True)
    with open(RAW_PATH,'w') as f:
        json.dump({
            "fetched_at":datetime.now(timezone(timedelta(hours=5, minutes=45))).isoformat(),"timezone":"GMT+5:45",
            "data": data
            }, f, indent=4)
        
        #the industry standard is:
        #def save_raw_data(data):
        #    os.makedirs("data/raw", exist_ok=True)
        #   payload = {
        #        "metadata":{
        #            "fetched_at": datetime.now(timezone(timedelta(hours=5, minutes=45))).isoformat(),
        #            "timezone": "GMT+5:45"}, 
        #        "data": data  
        #    }
        #    with open(RAW_PATH,'w', encoding='utf-8') as f:
        #        json.dump(payload, f, indent=4)

def main():
        data = fetch_steam_data()
        save_raw_data(data)


if __name__ == "__main__":
    main()
    print("Data has been fetched and saved successfully.")
