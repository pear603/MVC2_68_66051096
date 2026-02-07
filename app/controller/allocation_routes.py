from flask import Blueprint, render_template, redirect, request, url_for
from app.model.assignment_model import AssignmentModel
from app.model.citizen_model import CitizenModel
from app.model.shelter_model import ShelterModel
from tinydb import TinyDB, Query

bp = Blueprint('allocation', __name__)
db = TinyDB('db.json', encoding='utf-8')
assignment_table = db.table('assignments')

def perform_allocation():
    AssignmentModel.clear_all()
    ShelterModel.reset_all_occupancy()
    

    citizens = CitizenModel.get_prioritized_citizens()
    shelters = ShelterModel.get_all()
    
    for citizen in citizens:
        # 2. ให้ ShelterModel ตัดสินใจเลือกศูนย์ที่เหมาะสม
        target = ShelterModel.find_suitable_shelter(citizen['health_status'], shelters)
        
        if target:
            # 3. ให้ AssignmentModel บันทึกผล
            AssignmentModel.create(citizen['id'], target['id'], 'ได้ที่พัก')
            
            # 4. อัปเดตสถานะความจุผ่าน ShelterModel
            target['current_occupancy'] += 1
            ShelterModel.update_occupancy(target['id'], target['current_occupancy'])
        else:
            AssignmentModel.create(citizen['id'], None, 'ตกค้าง')
# --- Routes ---

@bp.route('/shelter')
def show_shelters():

    perform_allocation()

    updated_shelters = ShelterModel.get_all()
    return render_template('allocation.html', shelters=updated_shelters)

@bp.route('/run-allocation')
def run_manual_allocation():
    perform_allocation()
    return redirect(url_for('allocation.show_shelters'))

@bp.route('/report')
def show_report():
    # 1. ดึงข้อมูลการจัดสรรทั้งหมด
    results = AssignmentModel.get_all()
    
    # 2. ดึงข้อมูลประชาชนทั้งหมดมาทำเป็น Dictionary เพื่อให้ค้นหาได้ง่าย (Lookup Table)
    all_citizens = {c['id']: c for c in CitizenModel.get_all()}
    
    # 3. นำข้อมูลประชาชนไปใส่ในแต่ละผลการจัดสรร
    for item in results:
        citizen_info = all_citizens.get(item['citizen_id'])
        if citizen_info:
            item['age'] = citizen_info['age']
            item['type'] = citizen_info['type']
            item['health_status'] = citizen_info['health_status']

    # 4. เรียงลำดับตาม ID ก่อนส่งไป View
    results.sort(key=lambda x: x['citizen_id'])
    
    return render_template('report.html', results=results)