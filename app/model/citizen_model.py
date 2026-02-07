import re
from tinydb import TinyDB, Query

db = TinyDB('db.json', encoding='utf-8')
citizen_table = db.table('citizens')

class CitizenModel:
    @staticmethod
    def get_all():
        return citizen_table.all()

    @staticmethod
    def add_citizen(data):
        if not citizen_table.search(Query().id == data['id']):
            citizen_table.insert(data)
            return True
        return False
    
    @staticmethod
    def get_next_id():
        all_citizens = citizen_table.all()
        if not all_citizens:
            return "C001"
        
        
        ids = []
        for c in all_citizens:
            
            match = re.search(r'\d+', c['id'])
            if match:
                ids.append(int(match.group()))
        
        if not ids:
            return "C001"
            
        next_number = max(ids) + 1
        return f"C{next_number:03d}"
    
    @staticmethod
    def get_prioritized_citizens():
        citizens = citizen_table.all()
        
        def priority_score(c):
            # กฎ: เด็ก (<=12) และผู้สูงอายุ (>=60) มาก่อน
            if c['age'] <= 12 or c['age'] >= 60: return 0
            if c['type'] == 'VIP': return 1
            if c['type'] == 'RiskGroup': return 2
            return 3

        return sorted(citizens, key=priority_score)
    