# Flight Price Comparison Application

## Overview

This is a Flask-based web application for flight price comparison. It allows users to search for flights, compare prices across different airlines, and view search results in an organized interface. The application includes mock flight data generation for demonstration purposes and features a clean, responsive web interface.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python 3.11
- **Database**: SQLAlchemy ORM with support for both SQLite (development) and PostgreSQL (production)
- **Deployment**: Gunicorn WSGI server with autoscale deployment target
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **Styling**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript for form interactions and date validation

### Database Schema
- **Flight Model**: Stores flight information including airline, route, timing, pricing, and aircraft details
- **SearchHistory Model**: Tracks user search patterns for analytics and user experience improvements

## Key Components

### Core Application (`app.py`)
- Flask application factory with SQLAlchemy configuration
- Database initialization and table creation
- Proxy fix middleware for deployment compatibility
- Environment-based configuration for database URLs and session secrets

### Data Models (`models.py`)
- **Flight**: Primary entity storing flight details with JSON serialization support
- **SearchHistory**: Tracks user search behavior with temporal data

### Route Handlers (`routes.py`)
- Main search page rendering with popular routes and airport data
- Flight search functionality with form validation
- Mock flight data generation and filtering

### Mock Data Generation (`flight_data.py`)
- Realistic airline and aircraft data
- Popular airport codes and names
- Flight number generation algorithms

### Frontend Assets
- **Templates**: Responsive HTML templates with Bootstrap integration
- **Static Files**: Custom CSS for enhanced styling and JavaScript for form interactions

## Data Flow

1. **User Search Request**: User submits search form with origin, destination, and travel dates
2. **Input Validation**: Server validates form data including date constraints and airport codes
3. **Search History Recording**: Valid searches are logged to SearchHistory table
4. **Flight Data Generation**: Mock flights are generated based on search criteria
5. **Results Display**: Filtered and sorted flight results are rendered in results template

## External Dependencies

### Python Packages
- **Flask**: Web framework and templating
- **Flask-SQLAlchemy**: Database ORM integration
- **Gunicorn**: Production WSGI server
- **Psycopg2-binary**: PostgreSQL database adapter
- **Email-validator**: Input validation utilities
- **Werkzeug**: WSGI utilities and security middleware

### Frontend Dependencies
- **Bootstrap 5**: CSS framework with dark theme
- **Font Awesome**: Icon library
- **CDN-based delivery**: External CSS/JS resources

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Flask development server with debug mode
- File-based session storage

### Production Environment
- PostgreSQL database with connection pooling
- Gunicorn WSGI server with autoscale deployment
- Environment variable configuration
- ProxyFix middleware for reverse proxy compatibility

### Replit Configuration
- Nix package manager for system dependencies
- Automated deployment with port binding
- Workflow automation for application startup

## Changelog

- June 18, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.