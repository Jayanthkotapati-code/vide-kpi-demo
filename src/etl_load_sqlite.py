import pandas as pd
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CSV_DEFAULT = BASE / "data" / "raw" / "customers_raw.csv"
DB_DEFAULT = BASE / "data" / "db" / "analytics.db"


def load_csv_to_sqlite(csv_path=CSV_DEFAULT, db_path=DB_DEFAULT):
    csv_path = Path(csv_path)
    db_path = Path(db_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(str(db_path))
    df.to_sql("customers_raw", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    return db_path


if __name__ == "__main__":
    db = load_csv_to_sqlite()
    print(f"Loaded CSV into {db}")
