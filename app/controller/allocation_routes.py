# from flask import Blueprint, render_template, redirect, request, url_for
# from app.model.citizen_model import CitizenModel
# from app.model.shelter_model import ShelterModel
# from tinydb import TinyDB, Query

# bp = Blueprint('allocation', __name__)
# db = TinyDB('db.json')
# assignment_table = db.table('assignments')

# @bp.route('/run-allocation')
# def run_allocation():
#     assignment_table.truncate() # ล้างข้อมูลเก่า
    
#     citizens = CitizenModel.get_all()
#     shelters = ShelterModel.get_all()
    
#     # 1. กฎ: เด็ก (<=12) และผู้สูงอายุ (>=60) ได้รับการจัดสรรก่อน
#     def priority_score(c):
#         if c['age'] <= 12 or c['age'] >= 60: 
#             return 0  # ลำดับสูงสุด
#         if c['type'] == 'VIP': return 1
#         if c['type'] == 'RiskGroup': return 2
#         return 3

#     sorted_citizens = sorted(citizens, key=priority_score)

#     for citizen in sorted_citizens:
#         # 2. กฎ: ศูนย์พักพิงที่เต็มแล้วไม่สามารถรับเพิ่มได้ [Requirement จากรูป]
#         # เปลี่ยน 'current' เป็น 'current_occupancy' ให้ตรงกับ Model
#         available_shelters = [s for s in shelters if s['current_occupancy'] < s['capacity']]
        
#         # 3. กฎ: ผู้มีความเสี่ยงด้านสุขภาพต้องส่งไปยังศูนย์ความเสี่ยงต่ำ [Requirement จากรูป]
#         if citizen['health_status'] == 'At Risk': 
#             available_shelters = [s for s in available_shelters if s['risk_level'] == 'ต่ำ']

#         if available_shelters:
#             target_shelter = available_shelters[0]
            
#             assignment_table.insert({
#                 'citizen_id': citizen['id'],
#                 'shelter_id': target_shelter['id'],
#                 'status': 'ได้ที่พัก'
#             })
            
#             # อัปเดตจำนวนคนพักปัจจุบัน
#             target_shelter['current_occupancy'] += 1
#             ShelterModel.update_occupancy(target_shelter['id'], target_shelter['current_occupancy'])
#         else:
#             assignment_table.insert({
#                 'citizen_id': citizen['id'],
#                 'shelter_id': None,
#                 'status': 'ตกค้าง'
#             })

#     return redirect(url_for('allocation.show_shelters')) # เปลี่ยนไปหน้าแสดงผลศูนย์

# @bp.route('/shelters')
# def show_shelters():
#     # ดึงข้อมูล Shelter ล่าสุดมาแสดงผล
#     shelters = ShelterModel.get_all()
#     return render_template('allocation.html', shelters=shelters)

# @bp.route('/report')
# def show_report():
#     results = assignment_table.all()
#     return render_template('report.html', results=results)

# @bp.route('/')
# def index():
#     # รับค่าการเรียงลำดับจาก Query String (ค่าเริ่มต้นคือเรียงตาม id)
#     sort_by = request.args.get('sort', 'id')
#     all_citizens = CitizenModel.get_all()

#     # Logic การเรียงลำดับ (Sorting)
#     if sort_by == 'age':
#         # เรียงตามอายุเพื่อดูความสำคัญ (เด็ก/ผู้สูงอายุ) 
#         all_citizens = sorted(all_citizens, key=lambda x: x['age'])
#     elif sort_by == 'id':
#         all_citizens = sorted(all_citizens, key=lambda x: x['id'])

#     # Logic การแยกตามประเภทประชาชน (Grouping) 
#     grouped_citizens = {
#         'VIP': [c for c in all_citizens if c['type'] == 'VIP'],
#         'RiskGroup': [c for c in all_citizens if c['type'] == 'RiskGroup'],
#         'General': [c for c in all_citizens if c['type'] == 'General']
#     }

#     return render_template('registration.html', grouped=grouped_citizens, current_sort=sort_by)

from flask import Blueprint, render_template, redirect, request, url_for
from app.model.citizen_model import CitizenModel
from app.model.shelter_model import ShelterModel
from tinydb import TinyDB, Query

bp = Blueprint('allocation', __name__)
db = TinyDB('db.json')
assignment_table = db.table('assignments')

# --- ฟังก์ชันภายในสำหรับการจัดสรร (Internal Logic) ---
def perform_allocation():
    """ฟังก์ชันกลางสำหรับรันระบบจัดสรรตาม Business Rules"""
    assignment_table.truncate() # ล้างข้อมูลเก่า
    
    citizens = CitizenModel.get_all()
    shelters = ShelterModel.get_all()
    
    # รีเซ็ตจำนวนคนพักใน Shelter เป็น 0 ก่อนคำนวณใหม่ (เพื่อให้ข้อมูลถูกต้องเสมอ)
    for s in shelters:
        ShelterModel.update_occupancy(s['id'], 0)
        s['current_occupancy'] = 0

    # 1. จัดลำดับความสำคัญ: เด็ก (<=12) และผู้สูงอายุ (>=60) มาก่อน
    def priority_score(c):
        if c['age'] <= 12 or c['age'] >= 60: return 0
        if c['type'] == 'VIP': return 1
        if c['type'] == 'RiskGroup': return 2
        return 3

    sorted_citizens = sorted(citizens, key=priority_score)

    for citizen in sorted_citizens:
        # 2. คัดกรองศูนย์ที่ยังไม่เต็ม [Requirement: ศูนย์ที่เต็มแล้วรับเพิ่มไม่ได้]
        available_shelters = [s for s in shelters if s.get('current_occupancy', 0) < s['capacity']]
        
        # 3. เงื่อนไขสุขภาพ [Requirement: ผู้มีความเสี่ยงสุขภาพต้องไปศูนย์ความเสี่ยงต่ำ]
        if citizen.get('health_status') == 'At Risk':
            available_shelters = [s for s in available_shelters if s.get('risk_level') == 'ต่ำ']

        if available_shelters:
            target_shelter = available_shelters[0]
            assignment_table.insert({
                'citizen_id': citizen['id'],
                'shelter_id': target_shelter['id'],
                'status': 'ได้ที่พัก'
            })
            # อัปเดตตัวแปรใน memory และ database
            target_shelter['current_occupancy'] += 1
            ShelterModel.update_occupancy(target_shelter['id'], target_shelter['current_occupancy'])
        else:
            assignment_table.insert({
                'citizen_id': citizen['id'], 'shelter_id': None, 'status': 'ตกค้าง'
            })

# --- Routes ---

@bp.route('/shelters')
def show_shelters():
    """แสดงหน้าศูนย์พักพิง โดยรันการจัดสรรให้อัตโนมัติ"""
    # รันการจัดสรรทันทีที่โหลดหน้านี้
    perform_allocation()
    
    # ดึงข้อมูลล่าสุดหลังจากจัดสรรแล้วมาแสดงผล
    updated_shelters = ShelterModel.get_all()
    return render_template('allocation.html', shelters=updated_shelters)

@bp.route('/run-allocation')
def run_manual_allocation():
    """ปุ่มสำหรับกดรันใหม่ด้วยตัวเอง (Manual)"""
    perform_allocation()
    return redirect(url_for('allocation.show_shelters'))