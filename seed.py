from tinydb import TinyDB
from tinydb.storages import JSONStorage
import random
from app.controller.allocation_routes import perform_allocation
from datetime import datetime


db = TinyDB('db.json', storage=JSONStorage, encoding='utf-8', ensure_ascii=False)
random.seed(42)


def seed_data():
    
    db.drop_tables()
    
    shelters_table = db.table('shelters')
    citizens_table = db.table('citizens')
    assignments_table = db.table('assignments') # Clear assignments too

    print("Seeding database...")

    shelter_data = [
        {"id": "S001", "capacity": 5, "risk_level": "Low", "current_occupancy": 0},
        {"id": "S002", "capacity": 4, "risk_level": "Medium", "current_occupancy": 0},
        {"id": "S003", "capacity": 5, "risk_level": "Low", "current_occupancy": 0},
        {"id": "S004", "capacity": 20, "risk_level": "High", "current_occupancy": 0},
        {"id": "S005", "capacity": 4, "risk_level": "High", "current_occupancy": 0},
    ]
    shelters_table.insert_multiple(shelter_data)
    print(f"Added {len(shelter_data)} shelters.")

    citizen_types = ["General", "RiskGroup", "VIP"]
    health_statuses = ["Normal", "At Risk"]
    
    citizens_list = []
    for i in range(1, 31):
        citizen = {
            "id": f"C{i:03d}",
            "age": random.randint(1, 85), 
            "health_status": random.choice(health_statuses),
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": random.choice(citizen_types)
        }
        citizens_list.append(citizen)
    
    citizens_table.insert_multiple(citizens_list)
    perform_allocation()
    print(f"Added {len(citizens_list)} citizens.")

    print("Success: db.json has been populated with English data.")

if __name__ == "__main__":
    seed_data()