import pandas as pd
from sqlalchemy import create_engine
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------------------------------------
# 1) DATABASE CONNECTION
# -----------------------------------------------------------
DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"

# -----------------------------------------------------------
# 2) GOOGLE SHEETS CONFIG
# -----------------------------------------------------------
CREDENTIALS_FILE = "credentials.json"   # ต้องวางไฟล์ไว้ในโฟลเดอร์ e-com2
SPREADSHEET_ID = "19vEFyHbJnMK7Sto8n9KWG0lGmOHHR_emUkoxU40SKjI"
  # ของคุณ

# -----------------------------------------------------------
# 3) FUNCTION: UPLOAD TO GOOGLE SHEETS
# -----------------------------------------------------------
def publish():
    print("📤 Uploading Data to Google Sheets...")

    # 1) Connect PostgreSQL
    engine = create_engine(DB_URI)

    # 2) Load fact_sales
    df = pd.read_sql("SELECT * FROM production.fact_sales", engine)
    print(f"📦 Loaded {len(df):,} rows from production.fact_sales")

    # 3) Google Sheets Auth
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scope
    )
    client = gspread.authorize(creds)

    # ⭐ 4) เปิด Google Sheet ด้วย SPREADSHEET_ID (ไม่สร้างใหม่)
    sh = client.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1  # ใช้ Sheet แรก

    # 5) ล้างข้อมูลเก่าเพื่อป้องกันทับซ้อน
    worksheet.clear()

    # 6) อัปโหลดแบบ DataFrame
    set_with_dataframe(worksheet, df)

    print("✅ Upload Completed!")

# -----------------------------------------------------------
# RUN
# -----------------------------------------------------------
if __name__ == "__main__":
    publish()
