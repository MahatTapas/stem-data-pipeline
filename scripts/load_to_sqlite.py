import sqlite3
import pandas as pd

DB_PATH = "db/steam.db"
CSV_PATH = "data/processed/steam_processed.csv"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(CSV_PATH)
    df.to_sql("raw_games", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    load_data()
    print("Data has been loaded into SQLite successfully.")