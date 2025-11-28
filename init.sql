-- init.sql
-- รันอัตโนมัติครั้งแรกตอน docker-compose สร้าง container postgres

-- 1) Schema เก็บข้อมูลดิบจาก Kaggle
CREATE SCHEMA IF NOT EXISTS raw_data;

-- 2) Schema เก็บข้อมูลที่แปลงแล้ว สำหรับ Dashboard
CREATE SCHEMA IF NOT EXISTS production;
