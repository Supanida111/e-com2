# 🟦 E-Commerce ETL Pipeline  
Kaggle Online Retail → PostgreSQL → Google Sheets → Looker Studio

โปรเจ็กต์นี้เป็นตัวอย่างการทำ **Data Pipeline แบบครบวงจร** สำหรับชุดข้อมูล E-Commerce จาก Kaggle  
เป้าหมายคือแปลงข้อมูลดิบจากไฟล์ CSV ให้กลายเป็นตาราง Fact ที่สะอาด แล้วนำไปสร้าง Dashboard บน Google Looker Studio

---

## 1. สถาปัตยกรรม (Architecture)

Flow การทำงานของระบบ

1. **Kaggle CSV (Online Retail Dataset)**  
2. **Ingest:** `ingest.py`  
   - โหลดไฟล์ `Dataset.csv` ด้วย `pandas`  
   - เขียนข้อมูลลง PostgreSQL → `raw_data.kaggle_raw`  

3. **Transform:** `transform.py`  
   - ดึงข้อมูลจาก `raw_data.kaggle_raw`  
   - ทำ Data Cleaning + สร้างฟิลด์ใหม่  
   - เขียนผลลัพธ์ลง `production.fact_sales`  

4. **Publish:** `publish.py`  
   - ดึงข้อมูลจาก `production.fact_sales`  
   - ใช้ Google Service Account เขียนลง Google Sheets (worksheet `fact_sales`)  

5. **Dashboard:**  
   - นำ Google Sheets เชื่อมกับ **Looker Studio** เพื่อทำ Report / Dashboard  

---

## 2. เทคโนโลยีที่ใช้ (Tech Stack)

- **ภาษา:** Python 3.x  
- **ฐานข้อมูล:** PostgreSQL  
- **ไลบรารีหลัก (Python):**
  - `pandas`
  - `sqlalchemy`
  - `psycopg2-binary`
  - `gspread`
  - `gspread-dataframe`
  - `oauth2client`
- **บริการของ Google:**
  - Google Sheets
  - Google Cloud Service Account + Google Sheets API + Google Drive API
  - Google Looker Studio

---

## 3. โครงสร้างโปรเจ็กต์ (Project Structure)

```text
e-com2/
├─ ingest.py          # ดึง CSV → เข้าฐานข้อมูล (raw_data.kaggle_raw)
├─ transform.py       # ทำความสะอาด/แปลงข้อมูล → production.fact_sales
├─ publish.py         # ดึง fact_sales → เขียนลง Google Sheets
├─ run_pipeline.py    # รันทุก step: Ingest → Transform → Publish
├─ credentials.json   # (ไม่ควร push ขึ้น Git) Google Service Account key
├─ Dataset.csv        # ไฟล์ CSV จาก Kaggle (Online Retail)
├─ README.md          # คู่มือโปรเจ็กต์ (ไฟล์นี้)
└─ .venv/             # virtual environment (แนะนำให้ใช้)

---

 ## วิธีรันโปรเจค 
1) เปิดโฟลเดอร์โปรเจค

เปิด VS Code และเลือกเมนู File → Open Folder…
จากนั้นเลือกโฟลเดอร์โปรเจค e-com2

2) เปิด Terminal และเปิดใช้งาน Virtual Environment

เปิด Terminal ใน VS Code:

Terminal → New Terminal


จากนั้นรันคำสั่งต่อไปนี้:

cd "C:\Users\user\OneDrive\leaning\3.1\e-com2"
.\.venv\Scripts\Activate.ps1


ถ้าสำเร็จจะเห็น (.venv) ขึ้นหน้าบรรทัด Terminal

3) ติดตั้ง Dependencies (ทำครั้งแรกครั้งเดียว)
python -m pip install --upgrade pip
python -m pip install pandas sqlalchemy psycopg2-binary gspread gspread-dataframe oauth2client

4) ตั้งค่าการเชื่อมต่อฐานข้อมูลและ Google Sheets

ตรวจไฟล์เหล่านี้:

ingest.py, transform.py, publish.py

ตรวจ DB_URI ต้องเป็น:

DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"


ตรวจไฟล์ publish.py:

CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "ใส่ Spreadsheet ID ที่นี่"
WORKSHEET_NAME = "fact_sales"


ตรวจว่าไฟล์ credentials.json ถูกวางในโฟลเดอร์โปรเจคเดียวกับ publish.py

แชร์ Google Sheets ให้ Service Account:

เปิด Google Sheets

กด Share

ใส่อีเมลของ service account

ตั้งเป็น Editor

5) รัน Pipeline ทีละขั้น
5.1 Ingest – โหลดข้อมูล CSV ลง PostgreSQL
python ingest.py

5.2 Transform – ทำความสะอาดข้อมูล + สร้าง Fact Table
python transform.py

5.3 Publish – ส่งข้อมูลขึ้น Google Sheets
python publish.py

6) รันแบบรวดเดียว (Ingest → Transform → Publish)

ถ้าต้องการรันทุกขั้นตอนอัตโนมัติ:

python run_pipeline.py

7) ดูผลลัพธ์บน Dashboard

เปิด Google Sheets → เช็กว่าชีต fact_sales ถูกอัปเดต

เปิด Looker Studio → เชื่อมข้อมูลกับชีตนี้

Dashboard จะอัปเดตอัตโนมัติทุกครั้งที่รัน publish.py