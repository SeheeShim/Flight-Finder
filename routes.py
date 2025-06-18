from flask import render_template, request, jsonify, flash, redirect, url_for
from datetime import datetime, timedelta
import json
from app import app, db
from models import Flight, SearchHistory
from flight_data import generate_mock_flights, get_popular_routes, get_airport_list, AIRPORTS

@app.route('/')
def index():
    """Main search page"""
    popular_routes = get_popular_routes()
    airports = get_airport_list()
    return render_template('index.html', popular_routes=popular_routes, airports=airports)

@app.route('/search', methods=['GET', 'POST'])
def search_flights():
    """Search for flights"""
    if request.method == 'POST':
        try:
            origin = request.form.get('origin')
            destination = request.form.get('destination')
            departure_date_str = request.form.get('departure_date')
            return_date_str = request.form.get('return_date')
            
            # Validate inputs
            if not origin or not destination or not departure_date_str:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('index'))
            
            if origin == destination:
                flash('Origin and destination cannot be the same', 'error')
                return redirect(url_for('index'))
            
            # Parse dates
            departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d')
            return_date = None
            if return_date_str:
                return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
                if return_date < departure_date:
                    flash('Return date cannot be before departure date', 'error')
                    return redirect(url_for('index'))
            
            # Check if departure date is not in the past
            if departure_date.date() < datetime.now().date():
                flash('Departure date cannot be in the past', 'error')
                return redirect(url_for('index'))
            
            # Save search history
            search_record = SearchHistory(
                origin=origin,
                destination=destination,
                departure_date=departure_date.date(),
                return_date=return_date.date() if return_date else None
            )
            db.session.add(search_record)
            db.session.commit()
            
            # Generate mock flight data
            outbound_flights = generate_mock_flights(origin, destination, departure_date)
            return_flights = []
            if return_date:
                return_flights = generate_mock_flights(destination, origin, return_date)
            
            # Sort flights by price by default
            outbound_flights.sort(key=lambda x: x['price'])
            if return_flights:
                return_flights.sort(key=lambda x: x['price'])
            
            return render_template('results.html', 
                                 outbound_flights=outbound_flights,
                                 return_flights=return_flights,
                                 origin=origin,
                                 destination=destination,
                                 departure_date=departure_date_str,
                                 return_date=return_date_str,
                                 origin_name=AIRPORTS.get(origin, origin),
                                 destination_name=AIRPORTS.get(destination, destination))
                                 
        except ValueError as e:
            flash('Invalid date format', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            app.logger.error(f"Search error: {str(e)}")
            flash('An error occurred while searching for flights', 'error')
            return redirect(url_for('index'))
    
    # GET request - redirect to home
    return redirect(url_for('index'))

@app.route('/api/flights/sort', methods=['POST'])
def sort_flights():
    """API endpoint for sorting flights"""
    try:
        data = request.get_json()
        flights = data.get('flights', [])
        sort_by = data.get('sort_by', 'price')
        order = data.get('order', 'asc')
        
        # Define sort functions
        sort_functions = {
            'price': lambda x: x['price'],
            'departure': lambda x: x['departure_time'],
            'duration': lambda x: x['duration'],
            'airline': lambda x: x['airline'],
            'stops': lambda x: x['stops']
        }
        
        if sort_by in sort_functions:
            reverse_order = (order == 'desc')
            flights.sort(key=sort_functions[sort_by], reverse=reverse_order)
        
        return jsonify({'flights': flights, 'status': 'success'})
        
    except Exception as e:
        app.logger.error(f"Sort error: {str(e)}")
        return jsonify({'error': 'Failed to sort flights', 'status': 'error'}), 400

@app.route('/api/flights/filter', methods=['POST'])
def filter_flights():
    """API endpoint for filtering flights"""
    try:
        data = request.get_json()
        flights = data.get('flights', [])
        filters = data.get('filters', {})
        
        filtered_flights = flights
        
        # Filter by price range
        if 'min_price' in filters and filters['min_price']:
            filtered_flights = [f for f in filtered_flights if f['price'] >= float(filters['min_price'])]
        
        if 'max_price' in filters and filters['max_price']:
            filtered_flights = [f for f in filtered_flights if f['price'] <= float(filters['max_price'])]
        
        # Filter by stops
        if 'max_stops' in filters and filters['max_stops'] is not None:
            filtered_flights = [f for f in filtered_flights if f['stops'] <= int(filters['max_stops'])]
        
        # Filter by airlines
        if 'airlines' in filters and filters['airlines']:
            selected_airlines = filters['airlines']
            filtered_flights = [f for f in filtered_flights if f['airline'] in selected_airlines]
        
        return jsonify({'flights': filtered_flights, 'status': 'success'})
        
    except Exception as e:
        app.logger.error(f"Filter error: {str(e)}")
        return jsonify({'error': 'Failed to filter flights', 'status': 'error'}), 400

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash('An internal error occurred', 'error')
    return render_template('index.html'), 500
