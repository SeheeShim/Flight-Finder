import random
from datetime import datetime, timedelta
from models import Flight
from app import db

# Mock airlines and their common aircraft
AIRLINES = {
    'Korean Air': ['Boeing 777', 'Airbus A330', 'Boeing 787'],
    'Asiana Airlines': ['Airbus A350', 'Boeing 777', 'Airbus A321'],
    'American Airlines': ['Boeing 737', 'Airbus A321', 'Boeing 777'],
    'Delta Air Lines': ['Boeing 757', 'Airbus A330', 'Boeing 767'],
    'United Airlines': ['Boeing 737', 'Boeing 777', 'Airbus A320'],
    'Emirates': ['Airbus A380', 'Boeing 777', 'Airbus A350'],
    'Singapore Airlines': ['Airbus A350', 'Boeing 777', 'Airbus A380'],
    'Japan Airlines': ['Boeing 787', 'Boeing 777', 'Airbus A350'],
    'ANA': ['Boeing 787', 'Boeing 777', 'Airbus A320'],
    'Lufthansa': ['Airbus A350', 'Boeing 747', 'Airbus A320']
}

# Popular airport codes
AIRPORTS = {
    'ICN': 'Seoul Incheon',
    'GMP': 'Seoul Gimpo',
    'LAX': 'Los Angeles',
    'JFK': 'New York JFK',
    'NRT': 'Tokyo Narita',
    'HND': 'Tokyo Haneda',
    'LHR': 'London Heathrow',
    'CDG': 'Paris Charles de Gaulle',
    'DXB': 'Dubai',
    'SIN': 'Singapore',
    'HKG': 'Hong Kong',
    'BKK': 'Bangkok',
    'SYD': 'Sydney'
}

def generate_flight_number(airline):
    """Generate realistic flight number based on airline"""
    prefixes = {
        'Korean Air': 'KE',
        'Asiana Airlines': 'OZ',
        'American Airlines': 'AA',
        'Delta Air Lines': 'DL',
        'United Airlines': 'UA',
        'Emirates': 'EK',
        'Singapore Airlines': 'SQ',
        'Japan Airlines': 'JL',
        'ANA': 'NH',
        'Lufthansa': 'LH'
    }
    prefix = prefixes.get(airline, 'XX')
    number = random.randint(100, 9999)
    return f"{prefix}{number}"

def calculate_duration(departure, arrival):
    """Calculate flight duration in hours and minutes"""
    duration = arrival - departure
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def generate_price(origin, destination, stops):
    """Generate realistic price based on route and stops"""
    base_prices = {
        ('ICN', 'LAX'): 800,
        ('ICN', 'JFK'): 900,
        ('ICN', 'NRT'): 300,
        ('ICN', 'LHR'): 700,
        ('ICN', 'CDG'): 750,
        ('ICN', 'DXB'): 600,
        ('ICN', 'SIN'): 500,
        ('ICN', 'HKG'): 400,
        ('ICN', 'BKK'): 450,
        ('ICN', 'SYD'): 950,
    }
    
    route = (origin, destination)
    reverse_route = (destination, origin)
    
    base_price = base_prices.get(route, base_prices.get(reverse_route, 600))
    
    # Add variation
    variation = random.uniform(0.8, 1.4)
    price = base_price * variation
    
    # Adjust for stops
    if stops == 1:
        price *= 0.8
    elif stops >= 2:
        price *= 0.7
    
    return round(price)

def generate_mock_flights(origin, destination, departure_date, num_flights=15):
    """Generate mock flight data for search results"""
    flights = []
    
    for i in range(num_flights):
        airline = random.choice(list(AIRLINES.keys()))
        aircraft = random.choice(AIRLINES[airline])
        flight_number = generate_flight_number(airline)
        
        # Generate departure time
        departure_hour = random.randint(5, 23)
        departure_minute = random.choice([0, 15, 30, 45])
        departure_time = departure_date.replace(hour=departure_hour, minute=departure_minute)
        
        # Generate flight duration (4-20 hours depending on route)
        base_duration = random.randint(4, 20)
        duration_minutes = random.randint(0, 59)
        arrival_time = departure_time + timedelta(hours=base_duration, minutes=duration_minutes)
        
        # Handle date changes for long flights
        if arrival_time.date() > departure_time.date():
            arrival_time = arrival_time.replace(day=departure_time.day + 1)
        
        duration_str = calculate_duration(departure_time, arrival_time)
        
        # Generate stops (80% direct, 15% 1 stop, 5% 2+ stops)
        stops_chance = random.random()
        if stops_chance < 0.8:
            stops = 0
        elif stops_chance < 0.95:
            stops = 1
        else:
            stops = 2
        
        price = generate_price(origin, destination, stops)
        
        flight = {
            'airline': airline,
            'flight_number': flight_number,
            'origin': origin,
            'destination': destination,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'duration': duration_str,
            'price': price,
            'stops': stops,
            'aircraft': aircraft
        }
        
        flights.append(flight)
    
    return flights

def get_popular_routes():
    """Return popular flight routes"""
    return [
        ('ICN', 'LAX', 'Seoul → Los Angeles'),
        ('ICN', 'JFK', 'Seoul → New York'),
        ('ICN', 'NRT', 'Seoul → Tokyo'),
        ('ICN', 'LHR', 'Seoul → London'),
        ('ICN', 'CDG', 'Seoul → Paris'),
        ('ICN', 'DXB', 'Seoul → Dubai'),
        ('ICN', 'SIN', 'Seoul → Singapore'),
        ('ICN', 'HKG', 'Seoul → Hong Kong'),
        ('ICN', 'BKK', 'Seoul → Bangkok'),
        ('ICN', 'SYD', 'Seoul → Sydney'),
    ]

def get_airport_list():
    """Return list of airports for dropdown"""
    return [(code, f"{code} - {name}") for code, name in AIRPORTS.items()]
