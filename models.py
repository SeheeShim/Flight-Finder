from app import db
from datetime import datetime

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    flight_number = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(10), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stops = db.Column(db.Integer, default=0)
    aircraft = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'airline': self.airline,
            'flight_number': self.flight_number,
            'origin': self.origin,
            'destination': self.destination,
            'departure_time': self.departure_time.strftime('%Y-%m-%d %H:%M'),
            'arrival_time': self.arrival_time.strftime('%Y-%m-%d %H:%M'),
            'duration': self.duration,
            'price': self.price,
            'stops': self.stops,
            'aircraft': self.aircraft
        }

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(10), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    search_time = db.Column(db.DateTime, default=datetime.utcnow)
