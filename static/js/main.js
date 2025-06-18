// Flight Finder JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize date inputs with today's date as minimum
    const today = new Date().toISOString().split('T')[0];
    const departureDateInput = document.getElementById('departure_date');
    const returnDateInput = document.getElementById('return_date');
    
    if (departureDateInput) {
        departureDateInput.min = today;
        departureDateInput.addEventListener('change', function() {
            if (returnDateInput) {
                returnDateInput.min = this.value;
                if (returnDateInput.value && returnDateInput.value < this.value) {
                    returnDateInput.value = '';
                }
            }
        });
    }
    
    if (returnDateInput) {
        returnDateInput.min = today;
    }

    // Popular route cards functionality
    const popularRouteCards = document.querySelectorAll('.popular-route-card');
    popularRouteCards.forEach(card => {
        card.addEventListener('click', function() {
            const origin = this.dataset.origin;
            const destination = this.dataset.destination;
            
            if (departureDateInput) {
                document.getElementById('origin').value = origin;
                document.getElementById('destination').value = destination;
                
                // Scroll to search form
                document.getElementById('searchForm').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'center'
                });
                
                // Focus on departure date
                setTimeout(() => {
                    departureDateInput.focus();
                }, 500);
            }
        });
    });

    // Form validation
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const origin = document.getElementById('origin').value;
            const destination = document.getElementById('destination').value;
            const departureDate = document.getElementById('departure_date').value;
            
            if (!origin || !destination || !departureDate) {
                e.preventDefault();
                alert('Please fill in all required fields');
                return;
            }
            
            if (origin === destination) {
                e.preventDefault();
                alert('Origin and destination cannot be the same');
                return;
            }
            
            // Show loading state
            const searchBtn = document.getElementById('searchBtn');
            if (searchBtn) {
                searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
                searchBtn.disabled = true;
            }
        });
    }

    // Results page functionality
    if (typeof window.outboundFlights !== 'undefined') {
        initializeResultsPage();
    }
});

function initializeResultsPage() {
    let currentFlights = [...window.outboundFlights];
    let filteredFlights = [...currentFlights];
    
    // Initialize airline filters
    initializeAirlineFilters();
    
    // Sort functionality
    const sortBySelect = document.getElementById('sortBy');
    const sortOrderBtn = document.getElementById('sortOrder');
    
    if (sortBySelect) {
        sortBySelect.addEventListener('change', applySorting);
    }
    
    if (sortOrderBtn) {
        sortOrderBtn.addEventListener('click', function() {
            const currentOrder = this.dataset.order;
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            this.dataset.order = newOrder;
            
            // Update icon
            const icon = this.querySelector('i');
            if (newOrder === 'asc') {
                icon.className = 'fas fa-sort-amount-up';
            } else {
                icon.className = 'fas fa-sort-amount-down';
            }
            
            applySorting();
        });
    }
    
    // Filter functionality
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');
    
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }
    
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }
    
    // Real-time filter updates
    document.getElementById('minPrice')?.addEventListener('input', debounce(applyFilters, 500));
    document.getElementById('maxPrice')?.addEventListener('input', debounce(applyFilters, 500));
    document.getElementById('maxStops')?.addEventListener('change', applyFilters);
    
    function initializeAirlineFilters() {
        const airlines = [...new Set(currentFlights.map(f => f.airline))].sort();
        const airlineFiltersContainer = document.getElementById('airlineFilters');
        
        if (airlineFiltersContainer) {
            airlineFiltersContainer.innerHTML = '';
            airlines.forEach(airline => {
                const checkboxDiv = document.createElement('div');
                checkboxDiv.className = 'form-check';
                checkboxDiv.innerHTML = `
                    <input class="form-check-input airline-checkbox" type="checkbox" 
                           value="${airline}" id="airline-${airline.replace(/\s+/g, '-')}">
                    <label class="form-check-label" for="airline-${airline.replace(/\s+/g, '-')}">
                        ${airline}
                    </label>
                `;
                airlineFiltersContainer.appendChild(checkboxDiv);
            });
            
            // Add event listeners to checkboxes
            const checkboxes = airlineFiltersContainer.querySelectorAll('.airline-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', applyFilters);
            });
        }
    }
    
    function applySorting() {
        const sortBy = sortBySelect?.value || 'price';
        const order = sortOrderBtn?.dataset.order || 'asc';
        
        showLoading();
        
        setTimeout(() => {
            const sortFunctions = {
                'price': (a, b) => a.price - b.price,
                'departure': (a, b) => new Date(a.departure_time) - new Date(b.departure_time),
                'duration': (a, b) => parseDuration(a.duration) - parseDuration(b.duration),
                'airline': (a, b) => a.airline.localeCompare(b.airline),
                'stops': (a, b) => a.stops - b.stops
            };
            
            const sortFunction = sortFunctions[sortBy];
            if (sortFunction) {
                filteredFlights.sort(sortFunction);
                if (order === 'desc') {
                    filteredFlights.reverse();
                }
            }
            
            displayFlights(filteredFlights);
            hideLoading();
        }, 300);
    }
    
    function applyFilters() {
        const minPrice = parseFloat(document.getElementById('minPrice')?.value) || 0;
        const maxPrice = parseFloat(document.getElementById('maxPrice')?.value) || Infinity;
        const maxStops = document.getElementById('maxStops')?.value;
        const selectedAirlines = Array.from(document.querySelectorAll('.airline-checkbox:checked'))
            .map(cb => cb.value);
        
        showLoading();
        
        setTimeout(() => {
            filteredFlights = currentFlights.filter(flight => {
                // Price filter
                if (flight.price < minPrice || flight.price > maxPrice) {
                    return false;
                }
                
                // Stops filter
                if (maxStops !== '' && flight.stops > parseInt(maxStops)) {
                    return false;
                }
                
                // Airline filter
                if (selectedAirlines.length > 0 && !selectedAirlines.includes(flight.airline)) {
                    return false;
                }
                
                return true;
            });
            
            // Apply current sorting
            applySorting();
        }, 300);
    }
    
    function clearFilters() {
        document.getElementById('minPrice').value = '';
        document.getElementById('maxPrice').value = '';
        document.getElementById('maxStops').value = '';
        
        const checkboxes = document.querySelectorAll('.airline-checkbox');
        checkboxes.forEach(cb => cb.checked = false);
        
        filteredFlights = [...currentFlights];
        applySorting();
    }
    
    function displayFlights(flights) {
        const resultsContainer = document.getElementById('flightResults');
        const noResultsDiv = document.getElementById('noResults');
        const flightCountElement = document.getElementById('flightCount');
        
        if (flightCountElement) {
            flightCountElement.textContent = flights.length;
        }
        
        if (flights.length === 0) {
            if (resultsContainer) resultsContainer.style.display = 'none';
            if (noResultsDiv) noResultsDiv.style.display = 'block';
            return;
        }
        
        if (noResultsDiv) noResultsDiv.style.display = 'none';
        if (resultsContainer) resultsContainer.style.display = 'block';
        
        if (resultsContainer) {
            resultsContainer.innerHTML = flights.map(flight => createFlightCard(flight)).join('');
        }
    }
    
    function createFlightCard(flight) {
        const departureTime = flight.departure_time.split(' ')[1];
        const arrivalTime = flight.arrival_time.split(' ')[1];
        const stopsDisplay = flight.stops === 0 ? 
            '<i class="fas fa-plane flight-icon"></i>' : 
            `<span class="stops-badge">${flight.stops} stop${flight.stops > 1 ? 's' : ''}</span>`;
        
        return `
            <div class="flight-card card mb-3" data-price="${flight.price}" 
                 data-airline="${flight.airline}" data-stops="${flight.stops}">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <div class="flight-info">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h6 class="airline-name mb-0">
                                        ${flight.airline}
                                        <span class="text-muted ms-2">${flight.flight_number}</span>
                                    </h6>
                                    <span class="badge bg-secondary">${flight.aircraft}</span>
                                </div>
                                
                                <div class="flight-route">
                                    <div class="d-flex align-items-center">
                                        <div class="time-info text-center">
                                            <div class="departure-time h5 mb-0">${departureTime}</div>
                                            <small class="text-muted">${flight.origin}</small>
                                        </div>
                                        
                                        <div class="flight-path mx-3 flex-grow-1">
                                            <div class="flight-duration text-center">
                                                <small class="text-muted">${flight.duration}</small>
                                            </div>
                                            <div class="flight-line position-relative">
                                                <hr class="my-1">
                                                ${stopsDisplay}
                                            </div>
                                        </div>
                                        
                                        <div class="time-info text-center">
                                            <div class="arrival-time h5 mb-0">${arrivalTime}</div>
                                            <small class="text-muted">${flight.destination}</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4 text-md-end">
                            <div class="price-info">
                                <div class="price h4 text-primary mb-2">$${flight.price}</div>
                                <button class="btn btn-primary btn-sm">Select Flight</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    function showLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        const resultsContainer = document.getElementById('flightResults');
        
        if (loadingIndicator) loadingIndicator.style.display = 'block';
        if (resultsContainer) resultsContainer.style.opacity = '0.5';
    }
    
    function hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        const resultsContainer = document.getElementById('flightResults');
        
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        if (resultsContainer) resultsContainer.style.opacity = '1';
    }
    
    function parseDuration(duration) {
        // Parse duration string like "5h 30m" to minutes
        const matches = duration.match(/(\d+)h\s*(\d+)m/);
        if (matches) {
            return parseInt(matches[1]) * 60 + parseInt(matches[2]);
        }
        return 0;
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle flight selection (placeholder functionality)
document.addEventListener('click', function(e) {
    if (e.target.textContent === 'Select Flight') {
        e.preventDefault();
        alert('Flight selection functionality would be implemented here. This would typically redirect to a booking page or add the flight to a cart.');
    }
});
