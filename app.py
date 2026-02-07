import os
from flask import Flask, render_template
from app.model.citizen_model import CitizenModel
from app.controller.allocation_routes import bp as allocation_bp
from app.model.shelter_model import ShelterModel
from app.controller.citizen_routes import citizen_bp

template_dir = os.path.abspath('app/templates')
app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(allocation_bp)
app.register_blueprint(citizen_bp)

@app.route('/')
def index():
    citizens = CitizenModel.get_all()
    return render_template('registration.html', citizens=citizens)
# app.register_blueprint(citizen_bp)


if __name__ == '__main__':
    app.run(debug=True)