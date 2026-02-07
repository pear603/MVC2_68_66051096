from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from datetime import datetime

# ตั้งค่า Database ให้รองรับภาษาไทยและเก็บข้อมูลในไฟล์ JSON 
db = TinyDB('db.json', storage=JSONStorage, ensure_ascii=False, encoding='utf-8')
assignment_table = db.table('assignments')

class AssignmentModel:
    @staticmethod
    def create_assignment(citizen_id, shelter_id, status):
        """
        บันทึกข้อมูลการให้พักพิง 
        """
        data = {
            'citizen_id': citizen_id,     # รหัสประชาชน 
            'shelter_id': shelter_id,     # รหัสศูนย์พักพิง 
            'assignment_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # วันที่เข้าพักพิง 
            'status': status              # สถานะ (ได้ที่พัก / ตกค้าง) [cite: 160]
        }
        return assignment_table.insert(data)

    @staticmethod
    def get_all():
        """
        ดึงข้อมูลการจัดสรรทั้งหมดเพื่อแสดงในหน้า Report 
        """
        return assignment_table.all()

    @staticmethod
    def clear_all():
        """
        ล้างข้อมูลการจัดสรรเก่าเพื่อรันกระบวนการใหม่
        """
        assignment_table.truncate()