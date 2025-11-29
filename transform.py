import pandas as pd
from sqlalchemy import create_engine, text

DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"


def transform():
    print("🔧 Transforming Data...")

    engine = create_engine(DB_URI)

    # 1) ดึงข้อมูลดิบจาก raw_data.kaggle_raw
    df = pd.read_sql_table(
        "kaggle_raw",
        con=engine,
        schema="raw_data"
    )
    print(f"📥 Loaded raw_data.kaggle_raw: {len(df):,} rows")

    # 2) ลบแถวที่ข้อมูลสำคัญหาย
    df = df.dropna(
        subset=[
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
        ]
    )

    # 3) ตัดแถวที่จำนวนหรือราคาติดลบ / เป็นศูนย์
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    # 4) แปลง InvoiceDate ให้เป็น datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # 5) ลบแถวซ้ำ
    df = df.drop_duplicates()

    # 6) สร้างคอลัมน์ใหม่สำหรับใช้ทำ Dashboard / KPI
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["InvoiceYear"] = df["InvoiceDate"].dt.year
    df["InvoiceMonth"] = df["InvoiceDate"].dt.month
    df["InvoiceDay"] = df["InvoiceDate"].dt.day
    df["InvoiceHour"] = df["InvoiceDate"].dt.hour

    print(f"✅ After cleaning: {len(df):,} rows")

    # 7) เขียนลง production.fact_sales
    #    ลบตารางเดิมทิ้งไปเลย (ถ้ามี) พร้อม view ที่ผูกอยู่ (CASCADE)
    with engine.begin() as conn:
        print("⚠️ DROP TABLE production.fact_sales CASCADE (if exists) ...")
        conn.execute(text("DROP TABLE IF EXISTS production.fact_sales CASCADE;"))

        print("💾 Creating & writing production.fact_sales from DataFrame ...")
        df.to_sql(
            "fact_sales",
            con=conn,
            schema="production",
            if_exists="append",  # ถ้าไม่มีตาราง → pandas จะสร้างให้เอง
            index=False,
            chunksize=5000,      # แบ่ง insert ทีละ 5000 แถว ลดโอกาสค้าง
        )

    print("✅ Transform Completed! Data saved to production.fact_sales")


if __name__ == "__main__":
    transform()