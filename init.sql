-- สร้าง Schema ชื่อ raw_data ถ้ายังไม่มี
CREATE SCHEMA IF NOT EXISTS raw_data;

-- ลบตารางเดิมออกก่อน (ถ้ามี)
DROP TABLE IF EXISTS raw_data.kaggle_raw;

-- สร้างตารางว่าง เพื่อรอรับข้อมูลจาก ingest.py
-- pandas จะเติมคอลัมน์ให้อัตโนมัติ (if_exists='replace')
CREATE TABLE raw_data.kaggle_raw (
    id SERIAL PRIMARY KEY
);
