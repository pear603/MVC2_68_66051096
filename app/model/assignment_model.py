from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from datetime import datetime


db = TinyDB('db.json', storage=JSONStorage, ensure_ascii=False, encoding='utf-8')
assignment_table = db.table('assignments')

class AssignmentModel:
    @staticmethod
    def get_all():
        
        return assignment_table.all()

    @staticmethod
    def clear_all():
        
        assignment_table.truncate()

    @staticmethod
    def create(citizen_id, shelter_id, status):
        assignment_table.insert({
            'citizen_id': citizen_id,
            'shelter_id': shelter_id,
            'status': status
        })

    @staticmethod
    def assign_single(citizen):
        from app.model.shelter_model import ShelterModel
        
        # 1. ดึงข้อมูลศูนย์ทั้งหมดมาดูที่ว่างปัจจุบัน
        shelters = ShelterModel.get_all()
        
        # 2. กรองศูนย์ที่ยังไม่เต็ม (Rule: เต็มแล้วห้ามรับเพิ่ม)
        available = [s for s in shelters if s['current_occupancy'] < s['capacity']]
        
        # 3. กรองตามเงื่อนไขสุขภาพ (Rule: กลุ่มเสี่ยงต้องอยู่ศูนย์ Low Risk เท่านั้น)
        if citizen['health_status'] == 'At Risk':
            suitable = [s for s in available if s['risk_level'] == 'Low']
        else:
            # Smart Logic: คนปกติให้ไป High/Medium ก่อนเพื่อเก็บที่ Low ไว้ให้คนป่วย
            suitable = [s for s in available if s['risk_level'] != 'Low']
            if not suitable: # ถ้าศูนย์อื่นเต็มจริงๆ ถึงจะยอมให้คนปกติเข้าศูนย์ Low
                suitable = [s for s in available if s['risk_level'] == 'Low']
        
        if suitable:
            target = suitable[0]
            # บันทึกการจัดสรร
            assignment_table.insert({
                'citizen_id': citizen['id'],
                'shelter_id': target['id'],
                'status': 'ได้ที่พัก'
            })
            # อัปเดตจำนวนคนในศูนย์ (Database)
            ShelterModel.update_occupancy(target['id'], target['current_occupancy'] + 1)
            return f"ได้รับที่พักที่ศูนย์ {target['id']}"
        else:
            # กรณีไม่มีศูนย์ที่ว่างหรือตรงเงื่อนไข: ตกค้างทันที
            assignment_table.insert({
                'citizen_id': citizen['id'],
                'shelter_id': None,
                'status': 'ตกค้าง'
            })
            return "ไม่สามารถจัดสรรได้ (ศูนย์เต็มหรือเงื่อนไขไม่ตรง) - สถานะ: ตกค้าง"