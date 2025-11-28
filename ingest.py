import pandas as pd
from sqlalchemy import create_engine

# ใช้ค่าเดียวกับ docker-compose.yml
DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"

# ไฟล์ CSV จาก Kaggle (อยู่ในโฟลเดอร์ data)
CSV_PATH = "./data/Dataset.csv"


def ingest():
    print("📥 Loading CSV into PostgreSQL...")

    # 1) อ่านไฟล์ CSV จาก Kaggle
    df = pd.read_csv(CSV_PATH)

    # 2) ต่อ PostgreSQL
    engine = create_engine(DB_URI)

    # 3) เขียนเข้า schema raw_data, table = kaggle_raw
    # if_exists="replace" = ลบทิ้งแล้วสร้างใหม่ทุกครั้ง → rerun กี่ครั้งก็ไม่พัง
    df.to_sql(
        "kaggle_raw",
        engine,
        schema="raw_data",
        if_exists="replace",
        index=False,
    )

    print("✅ Ingest Completed.")


if __name__ == "__main__":
    ingest()

