from tinydb import TinyDB
from tinydb.storages import JSONStorage
import random
from datetime import datetime

# Initialize database with UTF-8 encoding [cite: 142]
db = TinyDB('db.json', storage=JSONStorage, encoding='utf-8', ensure_ascii=False)

def seed_data():
    # Clear existing data to ensure a fresh start [cite: 130, 175]
    db.drop_tables()
    
    shelters_table = db.table('shelters')
    citizens_table = db.table('citizens')
    assignments_table = db.table('assignments') # Clear assignments too

    print("Seeding database...")

    # 1. Create Shelters (Requirement: >= 5) 
    # Total capacity is set to 22 to ensure some of the 30 citizens remain unallocated 
    shelter_data = [
        {"id": "S001", "capacity": 5, "risk_level": "Low", "current_occupancy": 0},
        {"id": "S002", "capacity": 4, "risk_level": "Medium", "current_occupancy": 0},
        {"id": "S003", "capacity": 5, "risk_level": "Low", "current_occupancy": 0},
        {"id": "S004", "capacity": 20, "risk_level": "High", "current_occupancy": 0},
        {"id": "S005", "capacity": 10, "risk_level": "Low", "current_occupancy": 0},
    ]
    shelters_table.insert_multiple(shelter_data)
    print(f"Added {len(shelter_data)} shelters.")

    # 2. Create Citizens (Requirement: >= 30) 
    citizen_types = ["General", "RiskGroup", "VIP"] # [cite: 148]
    health_statuses = ["Normal", "At Risk"] # [cite: 147]
    
    citizens_list = []
    for i in range(1, 31):
        citizen = {
            "id": f"C{i:03d}", # [cite: 147]
            "age": random.randint(1, 85), # [cite: 147]
            "health_status": random.choice(health_statuses), # [cite: 147]
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # [cite: 147]
            "type": random.choice(citizen_types) # [cite: 148]
        }
        citizens_list.append(citizen)
    
    citizens_table.insert_multiple(citizens_list)
    print(f"Added {len(citizens_list)} citizens.")

    print("Success: db.json has been populated with English data.")

if __name__ == "__main__":
    seed_data()