from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.model.citizen_model import CitizenModel
from collections import defaultdict

# สร้าง Blueprint เพื่อแยก Route ออกจาก app.py
citizen_bp = Blueprint('citizen', __name__)

@citizen_bp.route('/')
def index():
    # รับค่าการเรียงลำดับจาก URL Query
    current_sort = request.args.get('sort', 'id')
    all_citizens = CitizenModel.get_all()

    # Logic การเรียงลำดับ
    if current_sort == 'age':
        all_citizens.sort(key=lambda x: x['age'], reverse=True)
    else:
        all_citizens.sort(key=lambda x: x['id'])

    # Logic การจัดกลุ่มตาม Type
    grouped = defaultdict(list)
    for c in all_citizens:
        grouped[c['type']].append(c)

    return render_template('registration.html', grouped=grouped, current_sort=current_sort)

@citizen_bp.route('/register', methods=['POST'])
def register():
    # 1. ให้ Model ช่วยหา ID ตัวถัดไปให้
    new_id = CitizenModel.get_next_id()
    
    # 2. รับค่าอื่นๆ จาก Form (ไม่ต้องรับ ID แล้ว)
    data = {
        "id": new_id,
        "age": int(request.form.get('age') or 0),
        "health_status": request.form.get('health_status'),
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": request.form.get('type')
    }
    
    # 3. บันทึกข้อมูล
    if CitizenModel.add_citizen(data):
        return redirect(url_for('citizen.index'))
    else:
        return "Error: Could not register citizen.", 500