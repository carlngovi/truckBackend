from app import app, db
from models import DailyEntry
from datetime import datetime

# Sample daily data
sample_daily_data = {
    '2025-06-02': {'trips': 8, 'fuelSpent': 10500, 'fuelLitres': 85.2, 'totalKilometers': 680, 'route': 'nairobi-mombasa', 'avgTripTime': 2.5},
    '2025-06-03': {'trips': 6, 'fuelSpent': 7800, 'fuelLitres': 63.4, 'totalKilometers': 510, 'route': 'nairobi-kisumu', 'avgTripTime': 3.0},
    '2025-06-04': {'trips': 8, 'fuelSpent': 10200, 'fuelLitres': 82.9, 'totalKilometers': 665, 'route': 'nairobi-mombasa', 'avgTripTime': 2.5},
    '2025-06-05': {'trips': 9, 'fuelSpent': 11700, 'fuelLitres': 95.1, 'totalKilometers': 765, 'route': 'nairobi-mombasa', 'avgTripTime': 2.3},
    '2025-06-06': {'trips': 7, 'fuelSpent': 9100, 'fuelLitres': 74.0, 'totalKilometers': 595, 'route': 'local-delivery', 'avgTripTime': 1.5},
}

def seed_data():
    with app.app_context():
        db.session.query(DailyEntry).delete()  # Optional: clear table before seeding

        for date_str, data in sample_daily_data.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            log = DailyEntry(
                date=date,
                trips=data['trips'],
                route=data['route'],
                avg_trip_time=data['avgTripTime'],
                fuel_spent=data['fuelSpent'],
                fuel_litres=data['fuelLitres'],
                total_kilometers=data['totalKilometers'],
                fuel_station='Total',               # Hardcoded placeholder
                vehicle_condition='Good'            # Hardcoded placeholder
            )

            db.session.add(log)

        db.session.commit()
        print("✅ Seeded daily logs for June 2025")

if __name__ == "__main__":
    seed_data()
