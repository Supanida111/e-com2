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
CREDENTIALS_FILE = "credentials.json"   # ต้องวางไฟล์นี้ในโฟลเดอร์ e-com2
#SPREADSHEET_ID = "19vEFyHbJnMK7Sto8n9KWG0lGmOHHR_emUkoxU40SKjI"  # แก้เป็นของคุณได้
#WORKSHEET_NAME = "fact_sales"  # ชื่อชีตใน Spreadsheet
SPREADSHEET_ID = "1zC5TVxUS3krUJ3aBOWswP7aTdjbwAdPvVAfdv2o7Hlw"
WORKSHEET_NAME = "fact_sales"


def publish():
    print("📤 Publishing data from PostgreSQL → Google Sheets...")

    # 1) อ่านข้อมูลจาก production.fact_sales
    engine = create_engine(DB_URI)
    query = "SELECT * FROM production.fact_sales"
    df = pd.read_sql(query, engine)

    # 2) เตรียม Credentials ของ Service Account
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        scopes,
    )

    client = gspread.authorize(creds)

    # 3) เปิด Spreadsheet
    sh = client.open_by_key(SPREADSHEET_ID)

    # 4) เปิด/สร้าง Worksheet
    try:
        worksheet = sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(
            title=WORKSHEET_NAME,
            rows=str(len(df) + 10),
            cols=str(len(df.columns) + 10),
        )

    # 5) ล้างข้อมูลเก่า
    worksheet.clear()

    # 6) เขียน DataFrame ลง Google Sheets
    set_with_dataframe(worksheet, df)

    print("✅ Upload Completed! Google Sheets is ready.")


if __name__ == "__main__":
    publish()