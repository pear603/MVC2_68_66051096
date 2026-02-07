from tinydb import TinyDB, Query

db = TinyDB('db.json')
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

    