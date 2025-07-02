import os

from flask import Flask, jsonify, request, render_template
from models import db, DailyEntry
from datetime import datetime
from flask_migrate import Migrate
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api= Api(app)
@app.route('/')
def index():
    return "<h1>Welcome to the Backend</h1>"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Dashboard KPIs summary
@app.route('/api/dashboard/summary', methods=['GET'])
def dashboard_summary():
    entries = DailyEntry.query.all()
    total_trips = sum(e.trips for e in entries)
    total_revenue = total_trips * 3500
    total_hours = sum(e.trips * (e.avg_trip_time or 0) for e in entries)

    return jsonify({
        "totalTrips": total_trips,
        "totalRevenue": total_revenue,
        "totalHours": round(total_hours, 1),
        "profitEstimate": total_trips * 475
    })

# Get all daily entries
@app.route('/api/daily', methods=['GET'])
def get_daily_data():
    entries = DailyEntry.query.all()
    return jsonify([entry.to_dict() for entry in entries])

# Get a single day's data
@app.route('/api/daily/<date>', methods=['GET'])
def get_single_day(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    entry = DailyEntry.query.filter_by(date=date_obj).first()
    return jsonify(entry.to_dict()) if entry else jsonify({}), 200

# Save or update one day's data
@app.route('/api/daily/<date>', methods=['POST', 'PUT'])
def save_daily_data(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    data = request.get_json()
    entry = DailyEntry.query.filter_by(date=date_obj).first()
    if not entry:
        entry = DailyEntry(date=date_obj)

    entry.trips = data.get('trips', 0)
    entry.route = data.get('route')
    entry.avg_trip_time = data.get('avgTripTime', 0.0)
    entry.fuel_spent = data.get('fuelSpent', 0.0)
    entry.fuel_litres = data.get('fuelLitres', 0.0)
    entry.total_kilometers = data.get('totalKilometers', 0.0)
    entry.fuel_station = data.get('fuelStation')
    entry.vehicle_condition = data.get('vehicleCondition')

    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Saved successfully"}), 200

# Monthly summaries
@app.route('/api/monthly/<int:year>/<int:month>', methods=['GET'])
def get_monthly_summary(year, month):
    entries = DailyEntry.query.filter(
        db.extract('year', DailyEntry.date) == year,
        db.extract('month', DailyEntry.date) == month
    ).all()

    total_trips = sum(e.trips for e in entries)
    working_days = sum(1 for e in entries if e.trips > 0)
    monthly_revenue = total_trips * 3500
    total_hours = sum(e.trips * (e.avg_trip_time or 0) for e in entries)

    return jsonify({
        "totalTrips": total_trips,
        "workingDays": working_days,
        "monthlyRevenue": monthly_revenue,
        "avgPerDay": monthly_revenue // working_days if working_days else 0,
        "totalHours": round(total_hours, 1)
    })

# Cost Centre Totals
@app.route('/api/cost-centres/<int:year>/<int:month>', methods=['GET'])
def cost_centres(year, month):
    entries = DailyEntry.query.filter(
        db.extract('year', DailyEntry.date) == year,
        db.extract('month', DailyEntry.date) == month
    ).all()

    trip_count = sum(e.trips for e in entries)

    cost_structure = {
        'fuelCost': 1300,
        'fuelInterest': 195,
        'driver': 250,
        'mike': 200,
        'captain': 100,
        'boss': 100,
        'truck': 478,
        'capex': 502,
        'profit': 475,
    }

    totals = {k: v * trip_count for k, v in cost_structure.items()}
    totals['totalTrips'] = trip_count
    totals['totalRevenue'] = trip_count * 3500

    return jsonify(totals)

# Static route list for dropdowns
@app.route('/api/routes', methods=['GET'])
def get_routes():
    return jsonify(["Nairobi-Mombasa", "Nairobi-Kisumu", "Nairobi-Nakuru"])

# Static fuel station list
@app.route('/api/fuel-stations', methods=['GET'])
def get_fuel_stations():
    return jsonify(["Total", "Shell", "National Oil", "Rubis"])

# (Optional) Login route placeholder
@app.route('/api/login', methods=['POST'])
def login():
    return jsonify({"message": "Login not implemented"}), 501

# (Optional) User info placeholder
@app.route('/api/user', methods=['GET'])
def get_user():
    return jsonify({"user": "test_user", "role": "admin"})

if __name__ == "__main__":
    app.run(port=5555, debug=True)
