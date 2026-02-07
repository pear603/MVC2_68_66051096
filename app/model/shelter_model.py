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
    def find_suitable_shelter(health_status, in_memory_shelters):
        
        available = [s for s in in_memory_shelters if s.get('current_occupancy', 0) < s['capacity']]
        

        if health_status == 'At Risk':
            available = [s for s in available if s.get('risk_level') == 'ต่ำ']
            
        return available[0] if available else None

    