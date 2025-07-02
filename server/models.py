from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CostCentre(db.Model):
    __tablename__ = 'cost_centres'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), unique=True, nullable=False)
    per_trip = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<CostCentre {self.label}>"


class DailyEntry(db.Model):
    __tablename__ = 'daily_logs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    trips = db.Column(db.Integer, default=0)
    route = db.Column(db.String(100))
    avg_trip_time = db.Column(db.Float)
    fuel_spent = db.Column(db.Float)
    fuel_litres = db.Column(db.Float)
    total_kilometers = db.Column(db.Float)
    fuel_station = db.Column(db.String(50))
    vehicle_condition = db.Column(db.String(50))

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "trips": self.trips,
            "route": self.route,
            "avgTripTime": self.avg_trip_time,
            "fuelSpent": self.fuel_spent,
            "fuelLitres": self.fuel_litres,
            "totalKilometers": self.total_kilometers,
            "fuelStation": self.fuel_station,
            "vehicleCondition": self.vehicle_condition,
        }
    
    def __repr__(self):
        return f"<DailyEntry {self.date}, Trips: {self.trips}, Route: {self.route}, Avg Trip Time: {self.avg_trip_time}, Fuel Spent: {self.fuel_spent}, Fuel Litres: {self.fuel_litres}, Total Kilometers: {self.total_kilometers}, Fuel Station: {self.fuel_station}, Vehicle Condition: {self.vehicle_condition}, >"

class MonthlySummary(db.Model):
    __tablename__ = 'monthly_summaries'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_trips = db.Column(db.Integer, default=0)
    working_days = db.Column(db.Integer, default=0)
    monthly_revenue = db.Column(db.Numeric(12, 2), default=0)
    avg_per_day = db.Column(db.Numeric(12, 2), default=0)
    best_day = db.Column(db.Date)
    max_trips = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Numeric(10, 2), default=0)

    __table_args__ = (
        db.UniqueConstraint('month', 'year', name='unique_month_year'),
    )

    def __repr__(self):
        return f"<MonthlySummary {self.month}/{self.year}>"


class CostSummary(db.Model):
    __tablename__ = 'cost_summary'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    centre_id = db.Column(db.Integer, db.ForeignKey('cost_centres.id', ondelete='CASCADE'), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), default=0)

    centre = db.relationship('CostCentre', backref=db.backref('summaries', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('month', 'year', 'centre_id', name='unique_cost_summary'),
    )

    def __repr__(self):
        return f"<CostSummary {self.month}/{self.year} - {self.centre.label}>"
