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