from flask import Blueprint, flash, render_template, request, redirect, url_for
from datetime import datetime
from app.model.assignment_model import AssignmentModel
from app.model.citizen_model import CitizenModel
from collections import defaultdict
from app.controller.allocation_routes import perform_allocation

citizen_bp = Blueprint('citizen', __name__)

@citizen_bp.route('/')
def index():
    # รับค่าการเรียงลำดับจาก URL Query
    current_sort = request.args.get('sort', 'id')
    all_citizens = CitizenModel.get_all()
    if current_sort == 'age':
        all_citizens.sort(key=lambda x: x['age'], reverse=True)
    else:
        all_citizens.sort(key=lambda x: x['id'])

    grouped = defaultdict(list)
    for c in all_citizens:
        grouped[c['type']].append(c)

    return render_template('registration.html', grouped=grouped, current_sort=current_sort)

@citizen_bp.route('/register', methods=['POST'])
def register():
    # new_id = CitizenModel.get_next_id()
    data = {
        "id": request.form.get('id'),
        "age": int(request.form.get('age') or 0),
        "health_status": request.form.get('health_status'),
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": request.form.get('type')
    }

    if CitizenModel.add_citizen(data):
        AssignmentModel.assign_single(data)
        # flash(f"ลงทะเบียนสำเร็จ: {result_msg}")
        return redirect(url_for('citizen.index'))
    else:
        return "Error: Could not register citizen.", 500