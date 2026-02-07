# สร้าง venv
python -m venv venv

# เปิดใช้งาน (Windows)
venv\Scripts\activate

# เปิดใช้งาน (Mac/Linux)
source venv/bin/activate

ติดตั้ง Library ที่จำเป็น
pip install flask tinydb

-------------------------------
ใน git มี db.json หากรันแล้วไม่มีข้อมูลให้รันด้วย python seed.py ก่อนเพื่อสร้างข้อมูล

รันโปรแกรม
python app.py
