from flask import Blueprint, render_template, redirect, request, url_for
from app.model.assignment_model import AssignmentModel
from app.model.citizen_model import CitizenModel
from app.model.shelter_model import ShelterModel
from tinydb import TinyDB, Query

bp = Blueprint('allocation', __name__)
db = TinyDB('db.json', encoding='utf-8')


def perform_allocation():
    AssignmentModel.clear_all()
    ShelterModel.reset_all_occupancy() # ล้างค่า occupancy เป็น 0 ทุกครั้งที่คำนวณใหม่

    # ดึงรายชื่อเรียงตามกฎ: เด็ก/คนชรา > VIP > กลุ่มเสี่ยง > ทั่วไป
    citizens = CitizenModel.get_prioritized_citizens()
    shelters = ShelterModel.get_all()
    
    for citizen in citizens:
        target = ShelterModel.find_suitable_shelter(citizen, shelters)
        
        if target:
            # กรณีมีที่ว่างและเงื่อนไขตรง: บันทึกได้ที่พัก
            AssignmentModel.create(citizen['id'], target['id'], 'ได้ที่พัก')
            target['current_occupancy'] += 1
            ShelterModel.update_occupancy(target['id'], target['current_occupancy'])
        else:
            # กรณีศูนย์เต็มหรือเงื่อนไขไม่ตรง: บันทึก "ตกค้าง" ทันที
            AssignmentModel.create(citizen['id'], None, 'ตกค้าง')

# --- Routes ---

@bp.route('/shelter')
def show_shelters():

    # perform_allocation()

    updated_shelters = ShelterModel.get_all()
    return render_template('allocation.html', shelters=updated_shelters)

@bp.route('/run-allocation')
def run_manual_allocation():
    perform_allocation()
    return redirect(url_for('allocation.show_shelters'))

@bp.route('/report')
def show_report():
    # perform_allocation()
    results = AssignmentModel.get_all()
    
    all_citizens = {c['id']: c for c in CitizenModel.get_all()}
    
    for item in results:
        citizen_info = all_citizens.get(item['citizen_id'])
        if citizen_info:
            item['age'] = citizen_info['age']
            item['type'] = citizen_info['type']
            item['health_status'] = citizen_info['health_status']

    results.sort(key=lambda x: x['citizen_id'])
    
    return render_template('report.html', results=results)