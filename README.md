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

🚀 วิธีรันโปรเจกต์บน GitHub (How to Run This Project)
1️⃣ Clone โปรเจกต์จาก GitHub
git clone https://github.com/Supanida111/e-com2.git
cd e-com2

2️⃣ สร้างและเปิดใช้งาน Virtual Environment

Windows

python -m venv .venv
.\.venv\Scripts\activate


Mac / Linux

python3 -m venv .venv
source .venv/bin/activate

3️⃣ ติดตั้ง Dependencies ทั้งหมด
pip install -r requirements.txt


ถ้าไม่มีไฟล์ requirements.txt ให้สร้างโดยคัดลอกสิ่งนี้ใส่ไฟล์ใหม่:

pandas
sqlalchemy
psycopg2-binary
gspread
gspread-dataframe
oauth2client
python-dotenv

4️⃣ ตั้งค่าการเชื่อมต่อ Database และ Google Sheets

ตรวจสอบไฟล์เหล่านี้:

📌 ingest.py, transform.py, publish.py

ต้องมีค่า DB_URI แบบนี้:

DB_URI = "postgresql://admin:admin123@localhost:5432/kaggle_db"


ตรวจไฟล์ publish.py ต้องกำหนด:

CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
WORKSHEET_NAME = "fact_sales"


นำไฟล์ credentials.json จาก Google Cloud Service Account
ไปวางในโฟลเดอร์เดียวกับ publish.py.

แชร์ Google Sheet ให้ Service Account ด้วยสิทธิ์ Editor.

5️⃣ รัน Pipeline ทีละขั้นตอน
5.1 Ingest → โหลด CSV ลง PostgreSQL
python ingest.py

5.2 Transform → ทำความสะอาดข้อมูล → fact_sales
python transform.py

5.3 Publish → ส่งข้อมูลขึ้น Google Sheets
python publish.py

6️⃣ รันแบบรวดเดียว (All-in-One)
python run_pipeline.py

7️⃣ ดูผลลัพธ์บน Dashboard
✔ Google Sheets

ข้อมูลจะถูกส่งไปที่ Worksheet: fact_sales

✔ Looker Studio

เชื่อม Google Sheets → แล้ว Refresh Dashboard ได้ทันที