from tinydb import TinyDB, Query

db = TinyDB('db.json', encoding='utf-8')
shelter_table = db.table('shelters')

class ShelterModel:
    @staticmethod
    def get_all():
        return shelter_table.all()

    @staticmethod
    def get_by_id(s_id):
        return shelter_table.get(cond=Query().id == s_id)

    @staticmethod
    def update_occupancy(s_id, current_count):
        shelter_table.update({'current_occupancy': current_count}, Query().id == s_id)

    @staticmethod
    def reset_all_occupancy():
       
        for s in shelter_table.all():
            shelter_table.update({'current_occupancy': 0}, Query().id == s['id'])

    @staticmethod
    def find_suitable_shelter(citizen, shelters):
        # 1. กรองเฉพาะศูนย์ที่ยังมีที่ว่าง (เต็มแล้วห้ามรับเพิ่มเด็ดขาด)
        available = [s for s in shelters if s['current_occupancy'] < s['capacity']]
        
        # 2. กฎด้านสุขภาพ: กลุ่มเสี่ยงต้องอยู่ศูนย์ความเสี่ยงต่ำเท่านั้น
        if citizen['health_status'] == 'At Risk':
            suitable = [s for s in available if s['risk_level'] == 'Low']
        else:
            # กลุ่มปกติ: ให้พยายามใช้ศูนย์ Medium/High ก่อนเพื่อกักศูนย์ Low ไว้ให้กลุ่มเสี่ยง
            suitable = [s for s in available if s['risk_level'] != 'Low']
            if not suitable: # ถ้าศูนย์อื่นเต็มหมดแล้วจริงๆ ถึงจะยอมให้เข้าศูนย์ Low
                suitable = [s for s in available if s['risk_level'] == 'Low']
                
        return suitable[0] if suitable else None # ถ้าไม่เจอศูนย์ที่ว่าง/เหมาะสม จะคืนค่า None