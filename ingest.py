import pandas as pd
from sqlalchemy import create_engine

DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"

def ingest():
    print("📥 Loading CSV into PostgreSQL...")

    df = pd.read_csv("./data/Dataset.csv")

    engine = create_engine(DB_URI)

    df.to_sql(
        "kaggle_raw",
        engine,
        schema="raw_data",
        if_exists="replace",
        index=False
    )

    print("✅ Ingest Completed.")

if __name__ == "__main__":
    ingest()
