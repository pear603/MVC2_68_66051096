import re
from tinydb import TinyDB, Query

db = TinyDB('db.json')
citizen_table = db.table('citizens')

class CitizenModel:
    @staticmethod
    def get_all():
        return citizen_table.all()

    @staticmethod
    def add_citizen(data):
        # ตรวจสอบการลงทะเบียนซ้ำ [cite: 167]
        if not citizen_table.search(Query().id == data['id']):
            citizen_table.insert(data)
            return True
        return False
    
    @staticmethod
    def get_next_id():
        all_citizens = citizen_table.all()
        if not all_citizens:
            return "C001"
        
        # ดึงตัวเลขออกมาจาก ID ทั้งหมด (เช่น จาก 'C030' เอาแค่ 30)
        ids = []
        for c in all_citizens:
            # ใช้ regex ดึงเฉพาะตัวเลขออกมา
            match = re.search(r'\d+', c['id'])
            if match:
                ids.append(int(match.group()))
        
        if not ids:
            return "C001"
            
        # หาค่าสูงสุดแล้ว +1
        next_number = max(ids) + 1
        return f"C{next_number:03d}" # จัดรูปแบบเป็น C001, C002